#!/usr/bin/env python3
"""Build separate FEMA flood and USFWS wetland map sheets for the TRF AOI.

This is a resilient second pass for hazard layers. It retries transient ArcGIS
failures and keeps flood and wetland outputs independent so one service outage
does not erase both maps.
"""

from __future__ import annotations

import io
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from PIL import Image, ImageDraw, ImageFont
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "maps" / "generated"
AOI_BBOX = (-95.865, 30.243, -95.823, 30.286)  # west, south, east, north
OUTPUT_SIZE = (2400, 2400)
DOWNLOAD_SIZE = (1800, 1800)
TIMEOUT = 180

NAIP = "https://imagery.geographic.texas.gov/server/rest/services/NAIP/NAIP22_NCCIR_60cm/ImageServer/exportImage"
FEMA_NFHL = "https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/export"
USFWS_WETLANDS = "https://fwsprimary.wim.usgs.gov/server/rest/services/Wetlands/MapServer/export"

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "trf-planning-hazard-map-builder/1.0"})
retry = Retry(
    total=6,
    connect=6,
    read=6,
    backoff_factor=2,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=frozenset({"GET"}),
    raise_on_status=False,
)
SESSION.mount("https://", HTTPAdapter(max_retries=retry))


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def fetch_image(url: str, *, transparent: bool, layers: str | None = None) -> Image.Image:
    params: dict[str, Any] = {
        "bbox": ",".join(map(str, AOI_BBOX)),
        "bboxSR": 4326,
        "imageSR": 4326,
        "size": f"{DOWNLOAD_SIZE[0]},{DOWNLOAD_SIZE[1]}",
        "format": "png32" if transparent else "jpgpng",
        "transparent": "true" if transparent else "false",
        "f": "image",
        "dpi": 96,
    }
    if "ImageServer" in url:
        params["interpolation"] = "RSP_BilinearInterpolation"
    if layers:
        params["layers"] = layers

    response = SESSION.get(url, params=params, timeout=TIMEOUT)
    response.raise_for_status()
    content_type = response.headers.get("content-type", "")
    if "image" not in content_type.lower() and not response.content.startswith(b"\x89PNG"):
        raise RuntimeError(f"Expected image response, received {content_type}: {response.text[:250]}")
    image = Image.open(io.BytesIO(response.content)).convert("RGBA")
    if image.size != OUTPUT_SIZE:
        image = image.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)
    return image


def placeholder(message: str) -> Image.Image:
    image = Image.new("RGBA", OUTPUT_SIZE, (238, 238, 232, 255))
    draw = ImageDraw.Draw(image)
    draw.multiline_text((100, 260), message, font=font(30), fill=(90, 35, 25, 255), spacing=16)
    return image


def decorate(image: Image.Image, title: str, subtitle: str) -> Image.Image:
    image = image.convert("RGBA")
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rectangle((0, 0, image.width, 150), fill=(255, 255, 255, 234))
    draw.rectangle((0, image.height - 115, image.width, image.height), fill=(255, 255, 255, 234))
    draw.text((45, 28), title, font=font(48, True), fill=(20, 25, 20, 255))
    draw.text((45, 91), subtitle, font=font(24), fill=(45, 50, 45, 255))

    nx, ny = image.width - 95, 65
    draw.polygon([(nx, ny - 38), (nx - 22, ny + 20), (nx, ny + 8), (nx + 22, ny + 20)], fill=(20, 20, 20, 255))
    draw.text((nx - 13, ny + 23), "N", font=font(25, True), fill=(20, 20, 20, 255))

    center_lat = (AOI_BBOX[1] + AOI_BBOX[3]) / 2
    meters_per_degree_lon = 111_320 * math.cos(math.radians(center_lat))
    degrees = 304.8 / meters_per_degree_lon
    pixels = degrees / (AOI_BBOX[2] - AOI_BBOX[0]) * image.width
    x0, y0 = 55, image.height - 63
    draw.line((x0, y0, x0 + pixels, y0), fill=(0, 0, 0, 255), width=9)
    draw.line((x0, y0 - 12, x0, y0 + 12), fill=(0, 0, 0, 255), width=4)
    draw.line((x0 + pixels, y0 - 12, x0 + pixels, y0 + 12), fill=(0, 0, 0, 255), width=4)
    draw.text((x0, y0 + 16), "1,000 ft", font=font(22, True), fill=(0, 0, 0, 255))

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    footer = f"Planning-grade screening only • AOI {AOI_BBOX} • Generated {generated}"
    draw.text((350, image.height - 70), footer, font=font(20), fill=(20, 20, 20, 255))
    return image


def save_png(name: str, image: Image.Image) -> None:
    GENERATED.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(GENERATED / name, "PNG", optimize=True)


def build_overlay_sheet(base: Image.Image, overlay: Image.Image | None, title: str, subtitle: str, failure: str | None) -> Image.Image:
    if overlay is None:
        return decorate(placeholder(f"The live source could not be downloaded during this build.\n{failure or 'Unknown error'}"), title, subtitle)
    result = base.copy()
    result.alpha_composite(overlay)
    return decorate(result, title, subtitle)


def main() -> int:
    statuses: list[dict[str, Any]] = []

    try:
        base = fetch_image(NAIP, transparent=False)
        statuses.append({"source": "Texas NAIP 2022 hazard-map base", "ok": True, "detail": "downloaded"})
    except Exception as exc:
        base = placeholder(f"NAIP base imagery unavailable.\n{exc}")
        statuses.append({"source": "Texas NAIP 2022 hazard-map base", "ok": False, "detail": repr(exc)})

    flood: Image.Image | None = None
    flood_error: str | None = None
    try:
        flood = fetch_image(FEMA_NFHL, transparent=True, layers="show:28")
        statuses.append({"source": "FEMA NFHL flood-hazard zones", "ok": True, "detail": "downloaded"})
    except Exception as exc:
        flood_error = repr(exc)
        statuses.append({"source": "FEMA NFHL flood-hazard zones", "ok": False, "detail": flood_error})

    wetlands: Image.Image | None = None
    wetlands_error: str | None = None
    try:
        wetlands = fetch_image(USFWS_WETLANDS, transparent=True)
        statuses.append({"source": "USFWS National Wetlands Inventory", "ok": True, "detail": "downloaded"})
    except Exception as exc:
        wetlands_error = repr(exc)
        statuses.append({"source": "USFWS National Wetlands Inventory", "ok": False, "detail": wetlands_error})

    flood_sheet = build_overlay_sheet(
        base,
        flood,
        "TRF FEMA flood-hazard screening",
        "NAIP base with FEMA National Flood Hazard Layer zones; not a guarantee against flooding",
        flood_error,
    )
    save_png("05-fema-flood-hazard.png", flood_sheet)

    wetlands_sheet = build_overlay_sheet(
        base,
        wetlands,
        "TRF wetland screening",
        "NAIP base with USFWS National Wetlands Inventory; not a jurisdictional determination",
        wetlands_error,
    )
    save_png("06-usfws-wetlands.png", wetlands_sheet)

    if flood is not None or wetlands is not None:
        composite = base.copy()
        if flood is not None:
            composite.alpha_composite(flood)
        if wetlands is not None:
            composite.alpha_composite(wetlands)
        composite = decorate(
            composite,
            "TRF flood and wetland screening",
            "NAIP base with available FEMA flood and USFWS wetland layers",
        )
    else:
        composite = decorate(
            placeholder(f"FEMA: {flood_error}\n\nUSFWS: {wetlands_error}"),
            "TRF flood and wetland screening",
            "Both live hazard services failed during this build",
        )
    save_png("07-flood-wetlands-composite.png", composite)
    save_png("05-flood-wetlands.png", composite)  # Backward-compatible filename.

    report_path = GENERATED / "build-report.json"
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        report = {"aoi_bbox_wgs84": AOI_BBOX, "sources": []}
    report["hazard_layer_rebuild_at"] = datetime.now(timezone.utc).isoformat()
    report["hazard_sources"] = statuses
    report["hazard_outputs"] = [
        "05-fema-flood-hazard.png",
        "06-usfws-wetlands.png",
        "07-flood-wetlands-composite.png",
        "05-flood-wetlands.png",
    ]
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    failures = sum(not status["ok"] for status in statuses)
    print(f"Hazard map pass complete with {failures} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
