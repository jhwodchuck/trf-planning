#!/usr/bin/env python3
"""Build georeferenced group geometry from the saved freeform pass layout."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from build_pass_svgs import (
    CONNECTOR_PARTS,
    DETACHED_PARTS,
    LAYOUT_PASSES,
    MARGIN_FT,
    PASSES,
    Equipment,
    Pass,
)
from build_road_geometry import to_geo


ROOT = Path(__file__).resolve().parents[1]
SAVED_PATH = ROOT / "maps" / "overlays" / "passes" / "saved-camp-v0.1.json"
GEOJSON_PATH = ROOT / "maps" / "data" / "group-site-v0.1.geojson"
REFERENCE_ROLES = {"road_edge", "setback_10", "setback_14", "west_limit"}


def closed(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return points if points[0] == points[-1] else [*points, points[0]]


def rectangle(x: float, y: float, width: float, height: float):
    return [
        (x, y),
        (x + width, y),
        (x + width, y + height),
        (x, y + height),
    ]


def ellipse_polygon(
    center_x: float,
    center_y: float,
    radius_x: float,
    radius_y: float,
    vertices: int = 72,
):
    return [
        (
            center_x + radius_x * math.cos(2 * math.pi * index / vertices),
            center_y + radius_y * math.sin(2 * math.pi * index / vertices),
        )
        for index in range(vertices)
    ]


def transform_points(
    points: list[tuple[float, float]],
    pass_definition: Pass,
    saved_position: dict[str, Any],
) -> list[tuple[float, float]]:
    bbox_width, bbox_height = pass_definition.bbox()
    view_width = bbox_width + 2 * MARGIN_FT
    view_height = bbox_height + 2 * MARGIN_FT
    center_x = saved_position["x_ft"] + view_width / 2
    center_y = saved_position["y_ft"] + view_height / 2
    angle = math.radians(saved_position.get("rotation_deg", 0))
    cosine, sine = math.cos(angle), math.sin(angle)

    transformed = []
    for x, y in points:
        absolute_x = saved_position["x_ft"] + MARGIN_FT + x
        absolute_y = saved_position["y_ft"] + MARGIN_FT + y
        delta_x, delta_y = absolute_x - center_x, absolute_y - center_y
        transformed.append(
            (
                center_x + delta_x * cosine - delta_y * sine,
                center_y + delta_x * sine + delta_y * cosine,
            )
        )
    return transformed


def polygon_feature(
    feature_id: str,
    name: str,
    role: str,
    local_points: list[tuple[float, float]],
    pass_definition: Pass,
    saved_position: dict[str, Any],
    **properties: Any,
):
    transformed = transform_points(
        closed(local_points), pass_definition, saved_position
    )
    return {
        "type": "Feature",
        "properties": {
            "id": feature_id,
            "name": name,
            "role": role,
            **properties,
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [to_geo(transformed)],
        },
    }


def line_feature(
    equipment: Equipment,
    pass_definition: Pass,
    saved_position: dict[str, Any],
):
    assert equipment.line is not None
    x1, y1, x2, y2 = equipment.line
    transformed = transform_points(
        [(x1, y1), (x2, y2)], pass_definition, saved_position
    )
    return {
        "type": "Feature",
        "properties": {
            "id": equipment.id,
            "name": equipment.label,
            "role": (
                "equipment_line"
                if equipment.role == "eq"
                else "equipment_line_placeholder"
            ),
            "status": equipment.status,
            "dimensions_ft": equipment.dims_label,
            "color": equipment.fill,
            "source_pass_id": pass_definition.id,
        },
        "geometry": {
            "type": "LineString",
            "coordinates": to_geo(transformed),
        },
    }


def equipment_features(
    equipment: Equipment,
    pass_definition: Pass,
    saved_position: dict[str, Any],
):
    if equipment.line is not None:
        return [line_feature(equipment, pass_definition, saved_position)]

    features = []
    if equipment.ellipse is not None:
        center_x, center_y, radius_x, radius_y = equipment.ellipse
        if equipment.buffer_ft:
            buffer = equipment.buffer_ft
            features.append(
                polygon_feature(
                    f"{equipment.id}_buffer",
                    f"{equipment.label} provisional clearance",
                    "clearance_placeholder",
                    ellipse_polygon(
                        center_x,
                        center_y,
                        radius_x + buffer,
                        radius_y + buffer,
                    ),
                    pass_definition,
                    saved_position,
                    status="Planning buffer only; verify actual operating clearance.",
                    source_pass_id=pass_definition.id,
                )
            )
        features.append(
            polygon_feature(
                equipment.id,
                equipment.label,
                "known_equipment"
                if equipment.role == "eq"
                else "equipment_placeholder",
                ellipse_polygon(center_x, center_y, radius_x, radius_y),
                pass_definition,
                saved_position,
                status=equipment.status,
                dimensions_ft=equipment.dims_label,
                color=equipment.fill,
                source_pass_id=pass_definition.id,
            )
        )
        return features

    assert equipment.rect is not None
    x, y, width, height = equipment.rect
    if equipment.buffer_ft:
        buffer = equipment.buffer_ft
        features.append(
            polygon_feature(
                f"{equipment.id}_buffer",
                f"{equipment.label} provisional clearance",
                "clearance_placeholder",
                rectangle(
                    x - buffer,
                    y - buffer,
                    width + 2 * buffer,
                    height + 2 * buffer,
                ),
                pass_definition,
                saved_position,
                status="Planning buffer only; verify actual operating clearance.",
                source_pass_id=pass_definition.id,
            )
        )

    features.append(
        polygon_feature(
            equipment.id,
            equipment.label,
            "known_equipment"
            if equipment.role == "eq"
            else "equipment_placeholder",
            rectangle(x, y, width, height),
            pass_definition,
            saved_position,
            status=equipment.status,
            dimensions_ft=equipment.dims_label,
            color=equipment.fill,
            source_pass_id=pass_definition.id,
        )
    )
    return features


def pass_features(pass_definition: Pass, saved_position: dict[str, Any]):
    if pass_definition.polygon is not None:
        boundary = pass_definition.polygon
    elif pass_definition.ellipse is not None:
        boundary = ellipse_polygon(*pass_definition.ellipse)
    else:
        assert pass_definition.rect is not None
        boundary = rectangle(0, 0, *pass_definition.rect)

    is_connector = pass_definition.kind == "connector"
    features = [
        polygon_feature(
            pass_definition.id,
            pass_definition.name,
            "connector" if is_connector else "pass",
            boundary,
            pass_definition,
            saved_position,
            area_sqft=pass_definition.area_sqft,
            status=(
                "Accepted allocation connector; width is planning-only and not confirmed accessible."
                if is_connector
                else "Accepted saved layout; planning-grade georeferencing, not a survey."
            ),
            layout_note=pass_definition.area_note,
            color=pass_definition.color,
            source=pass_definition.source,
            saved_x_ft=saved_position["x_ft"],
            saved_y_ft=saved_position["y_ft"],
            rotation_deg=saved_position.get("rotation_deg", 0),
            z=saved_position.get("z"),
            connector_width_ft=(
                round(pass_definition.connector_width_ft, 4)
                if pass_definition.connector_width_ft
                else None
            ),
            connector_length_ft=(
                round(pass_definition.connector_length_ft, 4)
                if pass_definition.connector_length_ft
                else None
            ),
        )
    ]
    for equipment in pass_definition.equipment:
        features.extend(
            equipment_features(equipment, pass_definition, saved_position)
        )
    return features


def main() -> int:
    saved = json.loads(SAVED_PATH.read_text(encoding="utf-8"))
    current = json.loads(GEOJSON_PATH.read_text(encoding="utf-8"))
    accepted_positions = {
        **saved.get("passes", {}),
        **saved.get("detached_parts", {}),
        **saved.get("connectors", {}),
    }
    accepted_definitions = [*LAYOUT_PASSES, *DETACHED_PARTS, *CONNECTOR_PARTS]
    saved_ids = set(accepted_positions)
    accepted_ids = {pass_definition.id for pass_definition in accepted_definitions}
    if saved_ids != accepted_ids:
        raise ValueError(
            "Saved layout IDs do not match pass definitions: "
            f"missing={sorted(accepted_ids - saved_ids)}, "
            f"extra={sorted(saved_ids - accepted_ids)}"
        )

    references = [
        feature
        for feature in current["features"]
        if feature.get("properties", {}).get("role") in REFERENCE_ROLES
    ]
    layout_features = []
    for pass_definition in accepted_definitions:
        layout_features.extend(
            pass_features(
                pass_definition, accepted_positions[pass_definition.id]
            )
        )

    output = {
        "type": "FeatureCollection",
        "name": "TRF group site map v0.1",
        "properties": {
            "created_on": "2026-08-16",
            "status": (
                "Generated from the accepted reattached freeform layout through "
                "the shared planning-grade local-foot/WGS84 affine transform."
            ),
            "layout_source": str(SAVED_PATH.relative_to(ROOT)).replace("\\", "/"),
            "saved_at_local": saved.get("saved_at_local"),
            "planning_baseline": "600 sq ft per pass",
            "passes": len(PASSES),
            "households": 7,
            "total_planning_area_sqft": sum(
                pass_definition.area_sqft for pass_definition in PASSES
            ),
            "warning": (
                "All positions are planning-grade and must be field-verified; "
                "this is not a survey or assigned boundary."
            ),
        },
        "features": [*layout_features, *references],
    }
    GEOJSON_PATH.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"Wrote {len(layout_features)} layout features and "
        f"{len(references)} references to {GEOJSON_PATH.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
