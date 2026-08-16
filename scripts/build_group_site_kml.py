"""Build a local Google Earth overlay from the group-site GeoJSON.

The generated KML contains only project-owned planning geometry. It does not
embed, download, or reproduce Google Earth imagery.
"""

from __future__ import annotations

import json
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "maps" / "data" / "group-site-v0.1.geojson"
OUTPUT = ROOT / "maps" / "overlays" / "group-site-v0.1.kml"
KML_NS = "http://www.opengis.net/kml/2.2"
ET.register_namespace("", KML_NS)

ROLE_COLORS = {
    "pass": ("ff3869e6", "553869e6"),
    "connector": ("ff1f4c6d", "998fc2d9"),
    "rv": ("ff86523d", "6686523d"),
    "canopy": ("ff0098ff", "660098ff"),
    "tent": ("ff5d9b45", "665d9b45"),
    "tent_estimate": ("ff8e5dbe", "448e5dbe"),
    "road_edge": ("ff00d0f5", "00000000"),
    "west_limit": ("ffd4bc00", "00000000"),
    "setback_10": ("ff3d26d7", "00000000"),
    "setback_14": ("ff288cf2", "00000000"),
}
DEFAULT_STYLE = ("ff777777", "33777777")


def k(tag: str) -> str:
    return f"{{{KML_NS}}}{tag}"


def add_text(parent: ET.Element, tag: str, value: object) -> ET.Element:
    element = ET.SubElement(parent, k(tag))
    element.text = str(value)
    return element


def coordinate_text(coordinates: list[list[float]]) -> str:
    return " ".join(f"{lon:.9f},{lat:.9f},0" for lon, lat, *_ in coordinates)


def add_geometry(parent: ET.Element, geometry: dict) -> None:
    geometry_type = geometry["type"]
    coordinates = geometry["coordinates"]
    if geometry_type == "Point":
        point = ET.SubElement(parent, k("Point"))
        add_text(point, "coordinates", coordinate_text([coordinates]))
    elif geometry_type == "LineString":
        line = ET.SubElement(parent, k("LineString"))
        add_text(line, "tessellate", 1)
        add_text(line, "coordinates", coordinate_text(coordinates))
    elif geometry_type == "Polygon":
        polygon = ET.SubElement(parent, k("Polygon"))
        add_text(polygon, "tessellate", 1)
        boundary = ET.SubElement(polygon, k("outerBoundaryIs"))
        ring = ET.SubElement(boundary, k("LinearRing"))
        add_text(ring, "coordinates", coordinate_text(coordinates[0]))
    else:
        raise ValueError(f"Unsupported geometry type: {geometry_type}")


def add_style(document: ET.Element, role: str, line_color: str, fill_color: str) -> None:
    style = ET.SubElement(document, k("Style"), id=f"role-{role}")
    line = ET.SubElement(style, k("LineStyle"))
    add_text(line, "color", line_color)
    add_text(line, "width", 3)
    polygon = ET.SubElement(style, k("PolyStyle"))
    add_text(polygon, "color", fill_color)
    label = ET.SubElement(style, k("LabelStyle"))
    add_text(label, "scale", 0.8)


def main() -> None:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    root = ET.Element(k("kml"))
    document = ET.SubElement(root, k("Document"))
    add_text(document, "name", "TRF 2026 group site plan v0.1")
    add_text(
        document,
        "description",
        "Provisional planning geometry only. Compare locally with the dated "
        "2025-10-20 Google Earth view; do not treat these polygons as surveyed "
        "or approved campsite boundaries.",
    )

    roles = sorted(
        {feature["properties"].get("role", "other") for feature in data["features"]}
    )
    for role in roles:
        add_style(document, role, *ROLE_COLORS.get(role, DEFAULT_STYLE))

    for feature in data["features"]:
        properties = feature["properties"]
        role = properties.get("role", "other")
        placemark = ET.SubElement(document, k("Placemark"))
        add_text(placemark, "name", properties.get("name", properties.get("id", role)))
        add_text(placemark, "styleUrl", f"#role-{role}")
        description_bits = [
            f"{key}: {value}".rstrip()
            for key, value in properties.items()
            if key not in {"name"} and value is not None
        ]
        add_text(placemark, "description", "\n".join(description_bits))
        extended = ET.SubElement(placemark, k("ExtendedData"))
        for key, value in properties.items():
            if value is None or isinstance(value, (dict, list)):
                continue
            datum = ET.SubElement(extended, k("Data"), name=key)
            add_text(datum, "value", value)
        add_geometry(placemark, feature["geometry"])

    ET.indent(root, space="  ")
    OUTPUT.write_text(
        ET.tostring(root, encoding="unicode", xml_declaration=True),
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
