#!/usr/bin/env python3
"""Build a reproducible TRF site-planning map pack from public GIS services.

The outputs are planning aids, not survey products. The AOI is intentionally broad
until the exact Havok-area campsite anchor is measured or otherwise verified.
"""

from __future__ import annotations

import io
import json
import math
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import requests
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "maps" / "generated"
DATA = ROOT / "maps" / "data"

# west, south, east, north — approximate planning envelope only.
AOI_BBOX = (-95.865, 30.243, -95.823, 30.286)
IMAGE_SIZE = (2400, 2400)
TIMEOUT = 120

NAIP = "https://imagery.geographic.texas.gov/server/rest/services/NAIP/NAIP22_NCCIR_60cm/ImageServer/exportImage"
USGS_TOPO = "https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/export"
USGS_IMAGERY_TOPO = "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryTopo/MapServer/export"
USGS_RELIEF = "https://basemap.nationalmap.gov/arcgis/rest/services/USGSShadedReliefOnly/MapServer/export"
FEMA_NFHL = "https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/export"
USFWS_WETLANDS = "https://fwsprimary.wim.usgs.gov/server/rest/services/Wetlands/MapServer/export"
GRIMES_FEATURES = "https://services8.arcgis.com/fpr21jaV02YtR7tv/ArcGIS/rest/services/GrimesCADWebService/FeatureServer"

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "trf-planning-map-builder/1.0 (public GitHub workflow)"})


@dataclass
class SourceResult:
    source: str
    ok: bool
    detail: str


REPORT: list[SourceResult] = []


def record(source: str, ok: bool, detail: str) -> None:
    REPORT.append(SourceResult(source, ok, detail))
    print(f"[{'ok' if ok else 'warn'}] {source}: {detail}")


def request(url: str, *, params: dict[str, Any] | None = None) -> requests.Response:
    response = SESSION.get(url, params=params, timeout=TIMEOUT)
    response.raise_for_status()
    return response


def arcgis_image(url: str, *, transparent: bool = False, layers: str | None = None) -> Image.Image:
    params: dict[str, Any] = {
        "bbox": ",".join(map(str, AOI_BBOX)),
        "bboxSR": 4326,
        "imageSR": 4326,
        "size": f"{IMAGE_SIZE[0]},{IMAGE_SIZE[1]}",
        "format": "png32" if transparent else "jpgpng",
        "transparent": "true" if transparent else "false",
        "f": "image",
    }
    if "ImageServer" in url:
        params["interpolation"] = "RSP_BilinearInterpolation"
    if layers:
        params["layers"] = layers
    response = request(url, params=params)
    image = Image.open(io.BytesIO(response.content)).convert("RGBA")
    if image.size != IMAGE_SIZE:
        image = image.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
    return image


def query_feature_layer(layer: int, name: str, out_fields: str) -> dict[str, Any]:
    url = f"{GRIMES_FEATURES}/{layer}/query"
    params = {
        "where": "1=1",
        "geometry": ",".join(map(str, AOI_BBOX)),
        "geometryType": "esriGeometryEnvelope",
        "inSR": 4326,
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": out_fields,
        "returnGeometry": "true",
        "outSR": 4326,
        "f": "geojson",
    }
    response = request(url, params=params)
    data = response.json()
    if data.get("type") != "FeatureCollection":
        raise RuntimeError(f"Unexpected {name} response: {str(data)[:300]}")
    return data


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def lonlat_to_pixel(lon: float, lat: float) -> tuple[float, float]:
    west, south, east, north = AOI_BBOX
    x = (lon - west) / (east - west) * IMAGE_SIZE[0]
    y = (north - lat) / (north - south) * IMAGE_SIZE[1]
    return x, y


def geometry_paths(geometry: dict[str, Any]) -> Iterable[list[tuple[float, float]]]:
    kind = geometry.get("type")
    coordinates = geometry.get("coordinates", [])
    if kind == "Polygon":
        for ring in coordinates:
            yield [lonlat_to_pixel(*point[:2]) for point in ring]
    elif kind == "MultiPolygon":
        for polygon in coordinates:
            for ring in polygon:
                yield [lonlat_to_pixel(*point[:2]) for point in ring]
    elif kind == "LineString":
        yield [lonlat_to_pixel(*point[:2]) for point in coordinates]
    elif kind == "MultiLineString":
        for line in coordinates:
            yield [lonlat_to_pixel(*point[:2]) for point in line]


def draw_geojson(image: Image.Image, geojson: dict[str, Any], *, color: tuple[int, int, int, int], width: int) -> None:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for feature in geojson.get("features", []):
        geometry = feature.get("geometry") or {}
        for path in geometry_paths(geometry):
            if len(path) > 1:
                draw.line(path, fill=color, width=width, joint="curve")
    image.alpha_composite(overlay)


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


def decorate(image: Image.Image, title: str, subtitle: str) -> Image.Image:
    image = image.convert("RGBA")
    draw = ImageDraw.Draw(image, "RGBA")
    top_h, bottom_h = 150, 115
    draw.rectangle((0, 0, image.width, top_h), fill=(255, 255, 255, 232))
    draw.rectangle((0, image.height - bottom_h, image.width, image.height), fill=(255, 255, 255, 232))
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

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    footer = f"Planning-grade only • AOI {AOI_BBOX} • Generated {timestamp}"
    draw.text((350, image.height - 70), footer, font=font(20), fill=(20, 20, 20, 255))
    return image


def placeholder(title: str, message: str) -> Image.Image:
    image = Image.new("RGBA", IMAGE_SIZE, (238, 238, 232, 255))
    draw = ImageDraw.Draw(image)
    draw.text((100, 200), title, font=font(52, True), fill=(30, 30, 30, 255))
    draw.multiline_text((100, 310), message, font=font(28), fill=(70, 40, 30, 255), spacing=14)
    return decorate(image, title, "Source unavailable during this build; see build-report.json")


def fetch_or_placeholder(source: str, title: str, subtitle: str, url: str, **kwargs: Any) -> Image.Image:
    try:
        image = arcgis_image(url, **kwargs)
        record(source, True, "downloaded")
        return decorate(image, title, subtitle)
    except Exception as exc:
        record(source, False, repr(exc))
        return placeholder(title, f"Could not download {source}.\n{exc}")


def save_png(path: Path, image: Image.Image) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(path, "PNG", optimize=True)


def main() -> int:
    GENERATED.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)

    parcels: dict[str, Any] = {"type": "FeatureCollection", "features": []}
    try:
        parcels = query_feature_layer(0, "parcels", "prop_id_text,legal_acreage,legal_desc,city,county,ObjectID_1")
        save_json(DATA / "grimes-parcels.geojson", parcels)
        record("Grimes CAD parcels", True, f"{len(parcels.get('features', []))} features")
    except Exception as exc:
        record("Grimes CAD parcels", False, repr(exc))

    try:
        streets = query_feature_layer(7, "streets", "*")
        save_json(DATA / "grimes-streets.geojson", streets)
        record("Grimes CAD streets", True, f"{len(streets.get('features', []))} features")
    except Exception as exc:
        record("Grimes CAD streets", False, repr(exc))

    try:
        county = query_feature_layer(8, "county boundary", "*")
        save_json(DATA / "grimes-county-boundary.geojson", county)
        record("Grimes county boundary", True, f"{len(county.get('features', []))} features")
    except Exception as exc:
        record("Grimes county boundary", False, repr(exc))

    try:
        aerial = arcgis_image(NAIP)
        record("Texas NAIP 2022", True, "downloaded")
        draw_geojson(aerial, parcels, color=(255, 73, 0, 230), width=5)
        aerial = decorate(aerial, "TRF aerial imagery and parcel context", "Texas NAIP 2022; orange lines are Grimes CAD parcel mapping")
    except Exception as exc:
        record("Texas NAIP 2022", False, repr(exc))
        aerial = placeholder("TRF aerial imagery and parcel context", f"NAIP download failed.\n{exc}")
    save_png(GENERATED / "01-aerial-parcels.png", aerial)

    topo = fetch_or_placeholder("USGS topographic", "TRF topographic context", "USGS The National Map topographic service", USGS_TOPO)
    save_png(GENERATED / "02-usgs-topographic.png", topo)

    imagery_topo = fetch_or_placeholder("USGS imagery topo", "TRF imagery with topographic labels", "USGS imagery/topographic basemap", USGS_IMAGERY_TOPO)
    save_png(GENERATED / "03-usgs-imagery-topo.png", imagery_topo)

    relief = fetch_or_placeholder("USGS shaded relief", "TRF shaded-relief context", "Use for slope and drainage reconnaissance only", USGS_RELIEF)
    save_png(GENERATED / "04-usgs-shaded-relief.png", relief)

    try:
        base = arcgis_image(NAIP)
        flood = arcgis_image(FEMA_NFHL, transparent=True, layers="show:28")
        wetlands = arcgis_image(USFWS_WETLANDS, transparent=True)
        base.alpha_composite(flood)
        base.alpha_composite(wetlands)
        composite = decorate(base, "TRF flood and wetland screening", "NAIP base; FEMA NFHL flood zones; USFWS National Wetlands Inventory")
        record("FEMA NFHL / USFWS wetlands composite", True, "downloaded")
    except Exception as exc:
        record("FEMA NFHL / USFWS wetlands composite", False, repr(exc))
        composite = placeholder("TRF flood and wetland screening", f"Hazard overlay build failed.\n{exc}")
    save_png(GENERATED / "05-flood-wetlands.png", composite)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "aoi_bbox_wgs84": AOI_BBOX,
        "image_size": IMAGE_SIZE,
        "warning": "Planning-grade output; not a survey, approval, utility locate, wetland determination, or guarantee against flooding.",
        "sources": [result.__dict__ for result in REPORT],
    }
    save_json(GENERATED / "build-report.json", report)
    failed = sum(not result.ok for result in REPORT)
    print(f"Map pack complete with {failed} source warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
