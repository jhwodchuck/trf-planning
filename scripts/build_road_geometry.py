"""Build the shared curved-road edge and setback geometry from local feet."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GROUP_PATH = ROOT / "maps" / "data" / "group-site-v0.1.geojson"
CONTROL_PATH = ROOT / "maps" / "data" / "site-control-road-setbacks.geojson"

DLON_DX, DLON_DY = 3.16849e-06, -9.275e-08
DLAT_DX, DLAT_DY = -8.0116e-08, -2.7369e-06
LON_0 = -95.846406043 - DLON_DX * 95 - DLON_DY * -20
LAT_0 = 30.2561531212 - DLAT_DX * 95 - DLAT_DY * -20

# Campsite-side road edge supplied by the user on 2026-07-27 while tracing the
# current Google Maps satellite view. Points run from the southwest road
# segment east around the bend, then north past HAVOK.
ROAD_EDGE_WGS84 = [
    (30.255345018897092, -95.84685074785044),
    (30.25534849418894, -95.84654497602352),
    (30.255339226743747, -95.8464698741713),
    (30.25531605812693, -95.84641622999114),
    (30.255278988328673, -95.84636929133352),
    (30.255153877656273, -95.84622981646508),
    (30.25515503608915, -95.84620969989751),
    (30.25517241258076, -95.84618153670293),
    (30.25525002753905, -95.84615069129934),
    (30.255311424402922, -95.84611582258225),
    (30.2553716627981, -95.84607961276063),
    (30.25543305958592, -95.84605547287957),
    (30.255492139477614, -95.84606217840208),
    (30.255624200283474, -95.84609436491019),
    (30.255705290164002, -95.84611850479125),
    (30.255788696828425, -95.84612252810477),
    (30.255872103422007, -95.84612252810477),
    (30.255925390930827, -95.84610241153722),
    (30.255958985215003, -95.84610911705973),
    (30.255967094178448, -95.84612252810477),
    (30.25600416371702, -95.84619494774799),
    (30.256040074819158, -95.84625529745067),
    (30.256070193797925, -95.84629016616778),
    (30.256120005934868, -95.84632369378036),
    (30.256173293309207, -95.84634783366144),
]


def to_local(points):
    determinant = DLON_DX * DLAT_DY - DLON_DY * DLAT_DX
    result = []
    for latitude, longitude in points:
        delta_lon = longitude - LON_0
        delta_lat = latitude - LAT_0
        x = (delta_lon * DLAT_DY - DLON_DY * delta_lat) / determinant
        y = (DLON_DX * delta_lat - delta_lon * DLAT_DX) / determinant
        result.append((x, y))
    return result


ROAD_LOCAL = to_local(ROAD_EDGE_WGS84)


def offset_curve(points: list[tuple[float, float]], distance_ft: float):
    normals = []
    for first, second in zip(points, points[1:]):
        dx, dy = second[0] - first[0], second[1] - first[1]
        length = (dx * dx + dy * dy) ** 0.5
        # Local y increases south/down in the viewer. The campsite is on the
        # right-hand side of the supplied southwest-to-north road trace:
        # north of its eastbound leg and west of its northbound leg.
        normals.append((dy / length, -dx / length))

    result = []
    for index, point in enumerate(points):
        if index == 0:
            nx, ny = normals[0]
        elif index == len(points) - 1:
            nx, ny = normals[-1]
        else:
            nx = normals[index - 1][0] + normals[index][0]
            ny = normals[index - 1][1] + normals[index][1]
            length = (nx * nx + ny * ny) ** 0.5
            nx, ny = nx / length, ny / length
        result.append((point[0] + nx * distance_ft, point[1] + ny * distance_ft))
    return result


def to_geo(points):
    return [
        [
            round(LON_0 + DLON_DX * x + DLON_DY * y, 12),
            round(LAT_0 + DLAT_DX * x + DLAT_DY * y, 12),
        ]
        for x, y in points
    ]


def replace_geometry(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    by_id = {feature["properties"].get("id"): feature for feature in data["features"]}

    if path == GROUP_PATH:
        targets = {
            "road_edge": ROAD_LOCAL,
            "setback_10": offset_curve(ROAD_LOCAL, 10),
            "setback_14": offset_curve(ROAD_LOCAL, 14),
        }
    else:
        targets = {
            "ROAD_EDGE_IMAGERY_CURVE": ROAD_LOCAL,
            "ROAD_CURVE_SETBACK_10FT": offset_curve(ROAD_LOCAL, 10),
            "ROAD_CURVE_SETBACK_14FT": offset_curve(ROAD_LOCAL, 14),
        }

    for feature_id, points in targets.items():
        feature = by_id[feature_id]
        if feature_id in {"road_edge", "ROAD_EDGE_IMAGERY_CURVE"}:
            feature["geometry"]["coordinates"] = [
                [longitude, latitude] for latitude, longitude in ROAD_EDGE_WGS84
            ]
        else:
            feature["geometry"]["coordinates"] = to_geo(points)
        feature["properties"]["south_extent_local_y_ft"] = round(
            max(y for _, y in ROAD_LOCAL), 3
        )
        feature["properties"]["extension_status"] = (
            "full curve replaced by 25 user-supplied road-edge coordinates"
        )
        feature["properties"]["southern_extension_source"] = (
            "User trace from current Google Maps satellite view, 2026-07-27"
        )
        feature["properties"]["trace_point_count"] = len(ROAD_EDGE_WGS84)

        if feature_id == "road_edge":
            feature["properties"]["name"] = "User-traced campsite-side road edge"
            feature["properties"]["status"] = (
                "planning-grade coordinate trace from current satellite view"
            )
            feature["properties"]["source"] = (
                "25 user-supplied WGS84 road-edge coordinates, 2026-07-27"
            )
        elif feature_id == "ROAD_EDGE_IMAGERY_CURVE":
            feature["properties"]["label"] = "User-traced campsite-side road edge"
            feature["properties"]["source"] = (
                "25 user-supplied WGS84 road-edge coordinates, 2026-07-27"
            )
            feature["properties"]["status"] = (
                "planning-grade coordinate trace from current satellite view"
            )
        else:
            feature["properties"]["status"] = (
                "approximate perpendicular offset from user-traced road edge; not surveyed"
            )

    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Updated road geometry in {path.relative_to(ROOT)}")


def main() -> None:
    replace_geometry(GROUP_PATH)
    replace_geometry(CONTROL_PATH)


if __name__ == "__main__":
    main()
