"""Apply the user-supplied hard western limit to group-site geometry."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "maps" / "data" / "group-site-v0.1.geojson"
NORTH = (-95.84648888888889, 30.255794444444444)
SOUTH = (-95.84651111111111, 30.255452777777776)

# Local-foot affine transform already used by group-site-v0.1.geojson.
DLON_DX, DLON_DY = 3.16848999e-06, -9.27499914e-08
DLAT_DX, DLAT_DY = -8.01159969e-08, -2.7369e-06

SHIFTS_FT = {
    "me_camper": (21, 20),
    "me_camper_placeholder": (21, 20),
    "me_slide_bunk_placeholder": (21, 20),
    "me_slide_main_placeholder": (21, 20),
    "me_service_placeholder": (21, 20),
    "me_rug_placeholder": (21, 20),
    "me_awning_placeholder": (21, 20),
    "me_rear_door_placeholder": (21, 20),
    "me_main_door_placeholder": (21, 20),
    "me_support": (71, 45),
    "bg_primary": (55, 40),
    "bg_primary_tent": (55, 40),
    "bg_closet_tent": (55, 40),
    "bg_closet": (27, -20),
    "bg_community_tent": (27, -20),
}
EXEMPT_ROLES = {"road_edge", "setback_10", "setback_14", "west_limit"}


def translate(value: object, dlon: float, dlat: float) -> object:
    if isinstance(value, list) and len(value) >= 2 and all(
        isinstance(item, (int, float)) for item in value[:2]
    ):
        return [value[0] + dlon, value[1] + dlat, *value[2:]]
    if isinstance(value, list):
        return [translate(item, dlon, dlat) for item in value]
    return value


def coordinates(value: object):
    if isinstance(value, list) and len(value) >= 2 and all(
        isinstance(item, (int, float)) for item in value[:2]
    ):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from coordinates(item)


def boundary_lon(lat: float) -> float:
    return NORTH[0] + (lat - NORTH[1]) * (SOUTH[0] - NORTH[0]) / (SOUTH[1] - NORTH[1])


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    if data["properties"].get("west_limit_applied"):
        raise SystemExit("West-limit migration already applied; refusing to translate twice.")

    for feature in data["features"]:
        feature_id = feature["properties"].get("id")
        if feature_id not in SHIFTS_FT:
            continue
        dx, dy = SHIFTS_FT[feature_id]
        dlon = DLON_DX * dx + DLON_DY * dy
        dlat = DLAT_DX * dx + DLAT_DY * dy
        feature["geometry"]["coordinates"] = translate(
            feature["geometry"]["coordinates"], dlon, dlat
        )
        feature["properties"]["west_limit_relocation_ft"] = [dx, dy]

    data["features"] = [
        feature for feature in data["features"]
        if feature["properties"].get("id") != "west_limit"
    ]
    data["features"].append({
        "type": "Feature",
        "properties": {
            "id": "west_limit",
            "name": "Hard western limit",
            "role": "west_limit",
            "status": "no planned pass or equipment may lie west",
            "source": (
                '30°15\'20.86"N 95°50\'47.36"W to '
                '30°15\'19.63"N 95°50\'47.44"W'
            ),
            "note": "The planning constraint uses the infinite alignment through these endpoints.",
        },
        "geometry": {"type": "LineString", "coordinates": [list(NORTH), list(SOUTH)]},
    })
    data["properties"]["west_limit_applied"] = True
    data["properties"]["west_limit_rule"] = (
        "No pass or equipment coordinate may lie west of the line through the two user controls."
    )

    violations = []
    for feature in data["features"]:
        props = feature["properties"]
        if props.get("role") in EXEMPT_ROLES:
            continue
        for lon, lat, *_ in coordinates(feature["geometry"]["coordinates"]):
            if lon < boundary_lon(lat) - 1e-10:
                violations.append((props.get("id"), lon, lat, boundary_lon(lat)))
    if violations:
        detail = "\n".join(
            f"{item[0]}: {item[1]},{item[2]} west of {item[3]}"
            for item in violations[:20]
        )
        raise SystemExit(f"West-limit violations remain:\n{detail}")

    PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Applied hard west limit and validated {len(data['features'])} features.")


if __name__ == "__main__":
    main()
