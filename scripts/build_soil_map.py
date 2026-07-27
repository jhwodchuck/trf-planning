#!/usr/bin/env python3
"""Build an NRCS soil-map sheet for the broad TRF planning envelope.

This is a reconnaissance product. It identifies mapped soil-unit context but does not
replace a Web Soil Survey AOI report, geotechnical investigation, drainage study, or
field verification of trafficability.
"""

from __future__ import annotations

import io
import json
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
IMAGE_SIZE = (2400, 2400)
TIMEOUT = 180

NAIP = "https://imagery.geographic.texas.gov/server/rest/services/NAIP/NAIP22_NCCIR_60cm/ImageServer/exportImage"
NRCS_WMS_ENDPOINTS = (
    "https://SDMDataAccess.sc.egov.usda.gov/Spatial/SDM.wms",
    "https://sdmdataaccess.sc.egov.usda.gov/Spatial/SDM.wms",
)


def session() -> requests.Session:
    retry = Retry(
        total=5,
        connect=5,
        read=5,
        backoff_factor=1.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
    )
    result = requests.Session()
    result.headers.update({"User-Agent": "trf-planning-map-builder/1.0"})
    result.mount("https://", HTTPAdapter(max_retries=retry))
    return result


def get_image(client: requests.Session, url: str, params: dict[str, Any]) -> Image.Image:
    response = client.get(url, params=params, timeout=TIMEOUT)
    response.raise_for_status()
    content_type = response.headers.get("content-type", "").lower()
    if "image" not in content_type and not response.content.startswith(b"\x89PNG"):
        text = response.text[:500].replace("\n", " ")
        raise RuntimeError(f"Expected image response from {url}; received {content_type}: {text}")
    image = Image.open(io.BytesIO(response.content))
    image.load()
    return image.convert("RGBA")


def aerial(client: requests.Session) -> Image.Image:
    bbox = ",".join(str(value) for value in AOI_BBOX)
    params = {
        "f": "image",
        "bbox": bbox,
        "bboxSR": "4326",
        "imageSR": "4326",
        "size": f"{IMAGE_SIZE[0]},{IMAGE_SIZE[1]}",
        "format": "png32",
        "transparent": "false",
    }
    return get_image(client, NAIP, params).resize(IMAGE_SIZE, Image.Resampling.LANCZOS)


def soil_overlay(client: requests.Session) -> tuple[Image.Image, str]:
    bbox = ",".join(str(value) for value in AOI_BBOX)
    attempts: list[str] = []
    variants = (
        {
            "service": "WMS",
            "version": "1.1.1",
            "request": "GetMap",
            "layers": "MapunitPoly",
            "styles": "",
            "srs": "EPSG:4326",
            "bbox": bbox,
            "width": str(IMAGE_SIZE[0]),
            "height": str(IMAGE_SIZE[1]),
            "format": "image/png",
            "transparent": "true",
        },
        {
            "service": "WMS",
            "version": "1.3.0",
            "request": "GetMap",
            "layers": "MapunitPoly",
            "styles": "",
            "crs": "CRS:84",
            "bbox": bbox,
            "width": str(IMAGE_SIZE[0]),
            "height": str(IMAGE_SIZE[1]),
            "format": "image/png",
            "transparent": "true",
        },
    )
    for endpoint in NRCS_WMS_ENDPOINTS:
        for params in variants:
            try:
                return get_image(client, endpoint, params).resize(IMAGE_SIZE, Image.Resampling.LANCZOS), endpoint
            except Exception as exc:  # keep all endpoint diagnostics for the report
                attempts.append(f"{endpoint} WMS {params['version']}: {exc!r}")
    raise RuntimeError("; ".join(attempts))


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    )
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def decorate(image: Image.Image) -> Image.Image:
    title_height = 150
    footer_height = 130
    canvas = Image.new("RGB", (image.width, image.height + title_height + footer_height), "white")
    canvas.paste(image.convert("RGB"), (0, title_height))
    draw = ImageDraw.Draw(canvas)
    draw.text((45, 28), "TRF planning envelope — NRCS mapped soil units", fill="black", font=font(52, True))
    draw.text((45, 92), "Aerial context with Soil Data Access MapunitPoly overlay", fill="black", font=font(30))
    footer_y = image.height + title_height
    draw.rectangle((0, footer_y, canvas.width, canvas.height), fill="white")
    draw.text(
        (45, footer_y + 22),
        "Planning-grade reconnaissance only. Confirm drainage, ponding, bearing conditions, and vehicle access in the field.",
        fill="black",
        font=font(27, True),
    )
    draw.text(
        (45, footer_y + 68),
        f"AOI WGS84: {AOI_BBOX} | imagery: Texas NAIP 2022 | soils: USDA NRCS Soil Data Access",
        fill="black",
        font=font(24),
    )
    return canvas


def main() -> int:
    GENERATED.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "aoi_bbox_wgs84": AOI_BBOX,
        "output": "10-nrcs-soil-map.png",
        "status": "failed",
        "warning": "Planning-grade soil-unit context; not a site-specific engineering or drainage determination.",
    }
    try:
        client = session()
        base = aerial(client)
        overlay, endpoint = soil_overlay(client)
        composed = Image.alpha_composite(base.convert("RGBA"), overlay)
        output = GENERATED / "10-nrcs-soil-map.png"
        decorate(composed).save(output, optimize=True)
        report.update({"status": "ok", "nrcs_endpoint": endpoint, "size_bytes": output.stat().st_size})
    except Exception as exc:
        report["error"] = repr(exc)
        (GENERATED / "soil-build-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        raise

    (GENERATED / "soil-build-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
