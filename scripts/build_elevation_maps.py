#!/usr/bin/env python3
"""Build USGS 3DEP elevation-derived map sheets for the TRF planning AOI."""

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
AOI_BBOX = (-95.865, 30.243, -95.823, 30.286)
IMAGE_SIZE = (2400, 2400)
TIMEOUT = 180
SERVICE = "https://elevation.nationalmap.gov/arcgis/rest/services/3DEPElevation/ImageServer/exportImage"

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "trf-planning-3dep-map-builder/1.0"})
SESSION.mount(
    "https://",
    HTTPAdapter(
        max_retries=Retry(
            total=6,
            connect=6,
            read=6,
            backoff_factor=2,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset({"GET"}),
            raise_on_status=False,
        )
    ),
)


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


def fetch_rendering(raster_function: str) -> Image.Image:
    params: dict[str, Any] = {
        "bbox": ",".join(map(str, AOI_BBOX)),
        "bboxSR": 4326,
        "imageSR": 4326,
        "size": f"{IMAGE_SIZE[0]},{IMAGE_SIZE[1]}",
        "format": "png32",
        "transparent": "false",
        "interpolation": "RSP_BilinearInterpolation",
        "renderingRule": json.dumps({"rasterFunction": raster_function}),
        "f": "image",
    }
    response = SESSION.get(SERVICE, params=params, timeout=TIMEOUT)
    response.raise_for_status()
    content_type = response.headers.get("content-type", "")
    if "image" not in content_type.lower() and not response.content.startswith(b"\x89PNG"):
        raise RuntimeError(f"Expected image response, received {content_type}: {response.text[:250]}")
    image = Image.open(io.BytesIO(response.content)).convert("RGBA")
    if image.size != IMAGE_SIZE:
        image = image.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
    return image


def placeholder(message: str) -> Image.Image:
    image = Image.new("RGBA", IMAGE_SIZE, (238, 238, 232, 255))
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
    footer = f"USGS 3DEP planning visualization • AOI {AOI_BBOX} • Generated {generated}"
    draw.text((350, image.height - 70), footer, font=font(20), fill=(20, 20, 20, 255))
    return image


def save_png(name: str, image: Image.Image) -> None:
    GENERATED.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(GENERATED / name, "PNG", optimize=True)


def main() -> int:
    products = [
        (
            "08-3dep-tinted-hillshade.png",
            "Hillshade Elevation Tinted",
            "TRF 3DEP tinted hillshade",
            "Bare-earth elevation context from the USGS 3D Elevation Program",
        ),
        (
            "09-3dep-slope.png",
            "Slope Map",
            "TRF 3DEP slope map",
            "Flat areas are gray; shallow slopes yellow; steeper slopes red-brown",
        ),
        (
            "10-3dep-2ft-contours.png",
            "Preset 2ft Contour Interval",
            "TRF 3DEP two-foot contours",
            "Detailed planning context; verify exact grades with field measurements",
        ),
        (
            "11-3dep-5ft-contours.png",
            "Preset 5ft Contour Interval",
            "TRF 3DEP five-foot contours",
            "Broader terrain and drainage context; not a survey-grade contour map",
        ),
    ]

    statuses: list[dict[str, Any]] = []
    for filename, raster_function, title, subtitle in products:
        try:
            image = fetch_rendering(raster_function)
            statuses.append({"source": f"USGS 3DEP {raster_function}", "ok": True, "detail": "downloaded"})
        except Exception as exc:
            image = placeholder(f"USGS 3DEP rendering failed.\nFunction: {raster_function}\n{exc}")
            statuses.append({"source": f"USGS 3DEP {raster_function}", "ok": False, "detail": repr(exc)})
        save_png(filename, decorate(image, title, subtitle))

    report_path = GENERATED / "build-report.json"
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        report = {"aoi_bbox_wgs84": AOI_BBOX, "sources": []}
    report["elevation_layer_build_at"] = datetime.now(timezone.utc).isoformat()
    report["elevation_sources"] = statuses
    report["elevation_outputs"] = [product[0] for product in products]
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    failures = sum(not status["ok"] for status in statuses)
    print(f"3DEP map pass complete with {failures} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
