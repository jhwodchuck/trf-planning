#!/usr/bin/env python3
"""Build standalone SVGs for pass sections and detached amenity pieces, plus a
manifest that the interactive drag-layout tool reads.

This script does not touch any network service. It is the shared source for
the current standalone pass pieces and their manifest, so each piece can be
refined independently and freely repositioned on a separate master canvas.

Run:
    python scripts/build_pass_svgs.py

Outputs:
    maps/overlays/passes/<id>.svg           one file per draggable piece
    maps/overlays/passes/passes-manifest.json
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "maps" / "overlays" / "passes"

# Pixels-per-foot used inside each standalone pass SVG. Independent of the
# master drag tool's on-screen scale -- the manifest carries real feet, and
# the master tool sizes each <img> from those, not from this constant.
SCALE = 16
# Uniform breathing room (feet) added on every side of a pass's true
# bounding box so strokes/labels are not clipped at the SVG's own edge.
MARGIN_FT = 0.5


@dataclass
class Equipment:
    id: str
    label: str
    role: str  # css class: eq (confirmed/estimate) or placeholder
    status: str
    # A rect (x, y, w, h), ellipse (cx, cy, rx, ry), or line
    # (x1, y1, x2, y2), all relative to
    # the pass's own bounding-box origin (its top-left corner, before margin).
    rect: tuple[float, float, float, float] | None = None
    ellipse: tuple[float, float, float, float] | None = None
    line: tuple[float, float, float, float] | None = None
    fill: str = "#3d85c6"
    dims_label: str = ""
    # Optional planning buffer around nominal equipment geometry. Used to
    # show unverified rainfly, rope, anchor, foot, or ballast clearance.
    buffer_ft: float = 0.0
    label_anchor: tuple[float, float] | None = None
    label_rotation: float = 0.0
    show_label: bool = True


@dataclass
class Pass:
    id: str
    name: str
    color: str
    area_sqft: float
    source: str
    # Rectangle boundary (w, h), ellipse (cx, cy, rx, ry), OR an explicit
    # polygon, all relative to the pass's own bounding-box origin (0, 0).
    rect: tuple[float, float] | None = None
    ellipse: tuple[float, float, float, float] | None = None
    polygon: list[tuple[float, float]] | None = None
    area_note: str = ""
    equipment: list[Equipment] = field(default_factory=list)
    annotations: list[tuple[float, float, str]] = field(default_factory=list)
    # Anchor point (relative to the bbox origin) for the household name/area
    # labels. Defaults to the bbox center, which is always inside a rect
    # boundary but can fall in the notch of a non-rectangular polygon, so
    # notched passes (e.g. jc) must set this explicitly.
    label_anchor: tuple[float, float] | None = None
    label_rotation: float = 0.0
    # Optional one-line boundary label for shallow/wide pass drawings where
    # the standard three-line household/area/note block would cover equipment.
    compact_label: str = ""
    # Where this pass's bounding-box top-left sits in the original
    # group-site-v0.1.svg local layout (feet). Used only as the manifest's
    # default position so the master tool opens matching the current README
    # arrangement.
    default_bbox_origin: tuple[float, float] = (0.0, 0.0)
    # Freeform-layout metadata. PASSES remains the connected source geometry
    # used by the georeferenced builder; LAYOUT_PASSES and DETACHED_PARTS below
    # may split selected passes into independently draggable planning pieces.
    kind: str = "pass"
    parent_pass_id: str = ""
    pass_allocation_sqft: float = 600.0
    walkway_reserve_sqft: float = 0.0
    setup_clearance_reserve_sqft: float = 0.0
    reserve_note: str = ""

    def bbox(self) -> tuple[float, float]:
        if self.rect is not None:
            return self.rect
        if self.ellipse is not None:
            _cx, _cy, radius_x, radius_y = self.ellipse
            return (2 * radius_x, 2 * radius_y)
        assert self.polygon is not None
        xs = [p[0] for p in self.polygon]
        ys = [p[1] for p in self.polygon]
        return (max(xs) - min(xs), max(ys) - min(ys))


PASSES: list[Pass] = [
    Pass(
        id="jc",
        name="J. + C.",
        color="#e69138",
        area_sqft=600,
        area_note="598.875 sq ft RV + canopy equipment footprint, plus 1.125 sq ft boundary buffer",
        source="planning/households/jc.md",
        polygon=[
            (29.25, 31.5),
            (29.25, 0),
            (15, 0),
            (15, 21.4167),
            (0, 21.4167),
            (0, 31.5),
        ],
        default_bbox_origin=(140.75, 73.5),
        label_anchor=(7.5, 22.25),
        compact_label="J. + C. — 600 sq ft — floorplan-derived Wildcat layout",
        equipment=[
            Equipment(
                id="jc_rv_envelope",
                label="Conservative deployed envelope",
                role="placeholder",
                status="31.5 x 14.25 ft planning envelope; not the literal camper outline",
                rect=(15, 0, 14.25, 31.5),
                fill="#d9e8f7",
                dims_label="31.5 x 14.25 ft",
                label_anchor=(22.125, 1.4),
            ),
            Equipment(
                id="jc_rv_body",
                label="Wildcat body",
                role="eq",
                status="approximately 8 x 29.5 ft floorplan-derived body within the conservative envelope; exact model and dimensions require field verification",
                rect=(17.585, 2, 8, 29.5),
                fill="#f0f2f4",
                dims_label="approx. 8 x 29.5 ft",
                label_anchor=(21.585, 16.75),
                label_rotation=90,
            ),
            Equipment(
                id="jc_slide_kitchen",
                label="Kitchen slide",
                role="placeholder",
                status="floorplan-derived west-side projection; approximately 25 in in the detailed planning schematic; field verify",
                rect=(15.5, 5.75, 2.085, 7.75),
                fill="#9bc3e6",
                dims_label="~25 in west",
                label_rotation=90,
            ),
            Equipment(
                id="jc_slide_living",
                label="Living / dinette slide",
                role="placeholder",
                status="floorplan-derived east-side projection; approximately 38 in in the detailed planning schematic; field verify",
                rect=(25.585, 5.25, 3.165, 12.25),
                fill="#9bc3e6",
                dims_label="~38 in east",
                label_rotation=90,
            ),
            Equipment(
                id="jc_slide_bedroom",
                label="Bedroom slide",
                role="placeholder",
                status="floorplan-derived east-side projection; approximately 29 in in the detailed planning schematic; field verify",
                rect=(25.585, 20.5, 2.415, 6.75),
                fill="#9bc3e6",
                dims_label="~29 in east",
                label_rotation=90,
            ),
            Equipment(
                id="jc_entry_steps",
                label="Entry + steps west",
                role="placeholder",
                status="floorplan-derived west-side entry; stair projection requires field measurement",
                line=(17.585, 23.1, 15.5, 24.4),
                fill="#a56200",
                label_anchor=(15.2, 22.7),
                show_label=True,
            ),
            Equipment(
                id="jc_hitch",
                label="Hitch / front south",
                role="placeholder",
                status="floorplan-derived orientation; exact hitch geometry requires measurement",
                line=(21.585, 29.4, 21.585, 31.25),
                fill="#303941",
                label_anchor=(22.2, 29.0),
                show_label=True,
            ),
            Equipment(
                id="jc_canopy",
                label="Canopy",
                role="eq",
                status="working template; dimensions must be verified",
                rect=(0, 21.4167, 15, 10),
                fill="#f6b26b",
                dims_label="15 x 10 ft",
            ),
        ],
        annotations=[
            (27.5, 30.5, "Road / east side"),
            (13.0, 20.5, "Entry / west side"),
        ],
    ),
    Pass(
        id="ss_camper",
        name="S. + S. — Camper",
        color="#93c47d",
        area_sqft=600,
        source="equipment/ss-kz-connect-se-c312bhkse.md",
        polygon=[
            (0, 0),
            (12, 0),
            (12, 4),
            (15, 4),
            (15, 12),
            (12, 12),
            (12, 17.5),
            (20, 17.5),
            (20, 29.5),
            (12, 29.5),
            (12, 40),
            (0, 40),
        ],
        default_bbox_origin=(105, 40),
        label_anchor=(7.7, 33.5),
        equipment=[
            Equipment(
                id="ss_camper_body",
                label="Camper body",
                role="eq",
                status="published manufacturer dimensions; model year/VIN not yet confirmed",
                rect=(3.7, 1.625, 8, 36.75),
                fill="#3d85c6",
                dims_label="36 ft 9 in x 8 ft (rear bumper to coupler)",
                label_anchor=(7.7, 20),
                label_rotation=90,
            ),
            Equipment(
                id="ss_camper_slide_bunk",
                label="Rear bunkhouse slide",
                role="placeholder",
                status="scale-derived from floorplan artwork; not measured on this unit; unsuitable for approval",
                rect=(0.6, 2.4, 3.1, 7.9),
                fill="#a9c9e8",
                dims_label="~3 ft 1 in projection (estimate)",
                label_rotation=90,
            ),
            Equipment(
                id="ss_camper_slide_main",
                label="Main living slide",
                role="placeholder",
                status="scale-derived from floorplan artwork; not measured on this unit; unsuitable for approval",
                rect=(0, 12.2, 3.7, 15.4),
                fill="#a9c9e8",
                dims_label="~3 ft 9 in projection (estimate)",
                label_rotation=90,
            ),
            Equipment(
                id="ss_rear_service_zone",
                label="Rear service bay",
                role="placeholder",
                status="provisional 3 x 8 ft service bay; appliance doors, griddle, and step projections require measurement",
                rect=(12, 4, 3, 8),
                fill="#f6b26b",
                dims_label="3 x 8 ft provisional",
                label_rotation=90,
            ),
            Equipment(
                id="ss_rug_zone",
                label="Rug zone",
                role="placeholder",
                status="working assumption; confirm actual rug dimensions and placement",
                rect=(12, 17.5, 8, 12),
                fill="#d9b38c",
                dims_label="8 x 12 ft provisional",
                label_anchor=(16, 22),
            ),
            Equipment(
                id="ss_rear_steps",
                label="Rear steps",
                role="placeholder",
                status="floorplan-derived location; projection requires measurement",
                rect=(11.7, 9.5, 3.3, 2),
                fill="#c58b55",
                dims_label="projection TBD",
                show_label=False,
            ),
            Equipment(
                id="ss_main_steps",
                label="Main steps",
                role="placeholder",
                status="floorplan-derived location; projection requires measurement",
                rect=(11.7, 27.5, 3.3, 2),
                fill="#c58b55",
                dims_label="projection TBD",
                show_label=False,
            ),
            Equipment(
                id="ss_awning",
                label="18 ft awning",
                role="placeholder",
                status="published length; projection and support locations require measurement",
                line=(12, 11.5, 12, 29.5),
                fill="#2e7d32",
                dims_label="projection TBD",
                label_anchor=(12.6, 20.5),
                label_rotation=90,
            ),
            Equipment(
                id="ss_rear_door",
                label="Rear door",
                role="placeholder",
                status="floorplan-derived location; verify on actual unit",
                line=(11.7, 9.7, 11.7, 11.1),
                fill="#a56200",
                label_anchor=(14, 10.4),
                label_rotation=90,
            ),
            Equipment(
                id="ss_main_door",
                label="Main door",
                role="placeholder",
                status="floorplan-derived location; verify on actual unit",
                line=(11.7, 27.9, 11.7, 29.3),
                fill="#a56200",
                label_anchor=(14, 28.6),
                label_rotation=90,
            ),
        ],
    ),
    Pass(
        id="ss_shower",
        name="S. + S. — Pass B / Shower",
        color="#93c47d",
        area_sqft=600,
        source="equipment/ss-16ft-shower-trailer.md",
        polygon=[
            (0, 0),
            (24, 0),
            (24, 18),
            (13.5, 18),
            (13.5, 40),
            (17.1, 40),
            (17.1, 50),
            (6.9, 50),
            (6.9, 40),
            (10.5, 40),
            (10.5, 18),
            (0, 18),
        ],
        area_note="432 + 66 + 102 = 600 sq ft",
        default_bbox_origin=(125, 150),
        label_anchor=(12, 16.2),
        equipment=[
            Equipment(
                id="ss_shower_trailer",
                label="Assumed utility-trailer deck",
                role="placeholder",
                status="16 ft stated deck length with 7 ft planning width; actual deck and maximum fender width require measurement",
                rect=(4, 0, 16, 7),
                fill="#245b24",
                dims_label="16 x 7 ft planning assumption",
                label_anchor=(12, 3.5),
            ),
            Equipment(
                id="ss_shower_ramp",
                label="Full-width rear ramp",
                role="placeholder",
                status="full-width fold-down ramp confirmed; 4 ft deployed depth is a planning assumption requiring measurement",
                rect=(20, 0, 4, 7),
                fill="#f6b26b",
                dims_label="7 x 4 ft assumed deployed",
                label_anchor=(22, 3.5),
                label_rotation=90,
            ),
            Equipment(
                id="ss_shower_tongue",
                label="Tongue / jack allowance",
                role="placeholder",
                status="provisional 4 ft centerline allowance; actual coupler, A-frame, jack, and tow-clearance geometry unknown",
                line=(0, 4.5, 4, 4.5),
                fill="#555555",
                dims_label="4 ft assumed",
                label_anchor=(2, 3.5),
            ),
            Equipment(
                id="ss_shower_left_wheel",
                label="Wheel/fender allowance",
                role="placeholder",
                status="provisional only; axle, tires, fenders, stabilizers, and maximum trailer width require measurement",
                rect=(10, 0, 4, 1),
                fill="#555555",
                show_label=False,
            ),
            Equipment(
                id="ss_shower_right_wheel",
                label="Wheel/fender allowance",
                role="placeholder",
                status="provisional only; axle, tires, fenders, stabilizers, and maximum trailer width require measurement",
                rect=(10, 6, 4, 1),
                fill="#555555",
                show_label=False,
            ),
            Equipment(
                id="ss_water_trailer",
                label="IBC water trailer",
                role="placeholder",
                status="provisional 5 x 8 ft deck assumption for the stated small 8 ft trailer; actual deck, fenders, axle, load rating, and overall length TBD",
                rect=(9.5, 7, 5, 8),
                fill="#6fa8dc",
                dims_label="assumed 5 x 8 ft deck",
                show_label=False,
            ),
            Equipment(
                id="ss_water_tote",
                label="IBC water tote",
                role="placeholder",
                status="provisional 4 x 4 ft planning footprint on the water trailer; actual tote dimensions, capacity, restraint, fill, vent, valve, and loaded weight TBD",
                rect=(10, 9, 4, 4),
                fill="#3d85c6",
                dims_label="assumed 4 x 4 ft",
                label_anchor=(12, 11),
                label_rotation=90,
            ),
            Equipment(
                id="ss_water_trailer_tongue",
                label="Water-trailer tongue",
                role="placeholder",
                status="provisional 3 ft centerline allowance; actual coupler, A-frame, jack, and tow-clearance geometry unknown",
                line=(12, 15, 12, 18),
                fill="#555555",
                dims_label="3 ft assumed",
                label_anchor=(12, 17),
                show_label=False,
            ),
            Equipment(
                id="ss_water_trailer_left_wheel",
                label="Water-trailer wheel/fender",
                role="placeholder",
                status="provisional only; axle, tires, fenders, stabilizers, and maximum trailer width require measurement",
                rect=(8.5, 10, 1, 2),
                fill="#555555",
                show_label=False,
            ),
            Equipment(
                id="ss_water_trailer_right_wheel",
                label="Water-trailer wheel/fender",
                role="placeholder",
                status="provisional only; axle, tires, fenders, stabilizers, and maximum trailer width require measurement",
                rect=(14.5, 10, 1, 2),
                fill="#555555",
                show_label=False,
            ),
            Equipment(
                id="ss_fire_pit",
                label="Fire pit",
                role="placeholder",
                status="provisional 3 x 3 ft fire-pit footprint inside a 10.2 x 10 ft end zone; actual pit, spark, fuel, extinguisher, and combustible clearances plus festival approval TBD",
                rect=(10.5, 43.5, 3, 3),
                fill="#cc4125",
                dims_label="3 x 3 ft assumed",
            ),
        ],
        annotations=[
            (12, 8.2, "Water trailer T'd into shower trailer"),
            (12, 29, "22 ft connector leg"),
            (12, 41.5, "10.2 x 10 ft fire-pit end zone"),
        ],
    ),
    Pass(
        id="me_camper",
        name="M. + E. — Mirrored Camper",
        color="#6fa8dc",
        area_sqft=600,
        source="planning/households/me.md",
        polygon=[
            (20, 0),
            (8, 0),
            (8, 4),
            (5, 4),
            (5, 12),
            (8, 12),
            (8, 17.5),
            (0, 17.5),
            (0, 29.5),
            (8, 29.5),
            (8, 40),
            (20, 40),
        ],
        default_bbox_origin=(55, 50),
        label_anchor=(12.3, 33.5),
        equipment=[
            Equipment(
                id="me_camper_placeholder",
                label="Mirrored reference body",
                role="placeholder",
                status="temporary mirror of S./S. reference only; not evidence of M./E. camper dimensions",
                rect=(8.3, 1.625, 8, 36.75),
                fill="#3d85c6",
                dims_label="36.75 x 8 ft placeholder",
                label_anchor=(12.3, 20),
                label_rotation=90,
            ),
            Equipment(
                id="me_slide_bunk_placeholder",
                label="Mirrored bunk slide",
                role="placeholder",
                status="temporary mirrored estimate only; actual slide count, side, length, and projection unknown",
                rect=(16.3, 2.4, 3.1, 7.9),
                fill="#a9c9e8",
                dims_label="reference only",
                label_rotation=90,
            ),
            Equipment(
                id="me_slide_main_placeholder",
                label="Mirrored main slide",
                role="placeholder",
                status="temporary mirrored estimate only; actual slide count, side, length, and projection unknown",
                rect=(16.3, 12.2, 3.7, 15.4),
                fill="#a9c9e8",
                dims_label="reference only",
                label_rotation=90,
            ),
            Equipment(
                id="me_rear_service_placeholder",
                label="Mirrored service bay",
                role="placeholder",
                status="temporary mirror only; actual doors, kitchen, appliances, and steps unknown",
                rect=(5, 4, 3, 8),
                fill="#f6b26b",
                dims_label="3 x 8 ft reference",
                label_rotation=90,
            ),
            Equipment(
                id="me_rug_placeholder",
                label="Mirrored rug bay",
                role="placeholder",
                status="temporary 8 x 12 ft mirrored planning zone; actual need and dimensions unknown",
                rect=(0, 17.5, 8, 12),
                fill="#d9b38c",
                dims_label="8 x 12 ft reference",
                label_anchor=(4, 22),
            ),
            Equipment(
                id="me_rear_steps_placeholder",
                label="Mirrored rear steps",
                role="placeholder",
                status="temporary mirror only; actual door and step geometry unknown",
                rect=(5, 9.5, 3.3, 2),
                fill="#c58b55",
                show_label=False,
            ),
            Equipment(
                id="me_main_steps_placeholder",
                label="Mirrored main steps",
                role="placeholder",
                status="temporary mirror only; actual door and step geometry unknown",
                rect=(5, 27.5, 3.3, 2),
                fill="#c58b55",
                show_label=False,
            ),
            Equipment(
                id="me_awning_placeholder",
                label="Mirrored awning",
                role="placeholder",
                status="temporary 18 ft mirrored reference only; actual awning unknown",
                line=(8, 11.5, 8, 29.5),
                fill="#2e7d32",
                dims_label="reference only",
                label_anchor=(7.4, 20.5),
                label_rotation=-90,
            ),
            Equipment(
                id="me_rear_door_placeholder",
                label="Mirrored rear door",
                role="placeholder",
                status="temporary mirror only; actual doors unknown",
                line=(8.3, 9.7, 8.3, 11.1),
                fill="#a56200",
                label_anchor=(6, 10.4),
                label_rotation=-90,
            ),
            Equipment(
                id="me_main_door_placeholder",
                label="Mirrored main door",
                role="placeholder",
                status="temporary mirror only; actual doors unknown",
                line=(8.3, 27.9, 8.3, 29.3),
                fill="#a56200",
                label_anchor=(6, 28.6),
                label_rotation=-90,
            ),
        ],
    ),
    Pass(
        id="me_support",
        name="M. + E. — Pass B / Support",
        color="#6fa8dc",
        area_sqft=600,
        source="planning/households/me.md",
        rect=(20, 30),
        default_bbox_origin=(101, 85),
        equipment=[],
    ),
    Pass(
        id="a",
        name="A.",
        color="#76a5af",
        area_sqft=600,
        source="planning/a-site-notes.md",
        polygon=[
            (0, 0),
            (25, 0),
            (25, 12),
            (18.5, 12),
            (18.5, 37),
            (6.5, 37),
            (6.5, 12),
            (0, 12),
        ],
        default_bbox_origin=(100, 116),
        label_anchor=(12.5, 14.8),
        annotations=[(12.5, 17.2, "8.5 ft nominal aisle")],
        equipment=[
            Equipment(
                id="a_sleep",
                label="Sleeping tent",
                role="eq",
                status="confirmed",
                rect=(2.5, 1, 20, 10),
                fill="#76a5af",
                dims_label="20 x 10 ft (rotated)",
                buffer_ft=0.5,
            ),
            Equipment(
                id="a_yoga",
                label="Yoga Tent (COVERPRO canopy)",
                role="eq",
                status="confirmed; bottom-aligned in T stem with 8.5 ft nominal separation",
                rect=(7.5, 19.5, 10, 17),
                fill="#3d85c6",
                dims_label="10 x 17 ft",
                buffer_ft=0.5,
            ),
        ],
    ),
    Pass(
        id="cs",
        name="C. + S.",
        color="#ffd966",
        area_sqft=600,
        source="planning/households/cs.md",
        rect=(40, 15),
        area_note="40 x 15 = 600 sq ft; equipment = 386 sq ft",
        default_bbox_origin=(75, 115),
        label_anchor=(20, 0.7),
        compact_label="C. + S. — 600 sq ft — 40 x 15 ft pass",
        annotations=[
            (22.5, 14.55, "Tent doors / vestibules TBD"),
        ],
        equipment=[
            Equipment(
                id="cs_row_border",
                label="Equipment-row border",
                role="eq",
                status="continuous planning border around the complete canopy, tent, and add-on row",
                rect=(0, 1, 39, 13),
                fill="none",
                show_label=False,
            ),
            Equipment(
                id="cs_canopy_placeholder",
                label="Planning canopy",
                role="placeholder",
                status="10 x 13 ft user-reported planning size; manufacturer/model, leg spacing, anchors, ropes, ballast, and exact relationship to tent require confirmation",
                rect=(0.5, 2.5, 13, 10),
                fill="#f1c232",
                dims_label="10 x 13 ft reported",
                buffer_ft=0.5,
            ),
            Equipment(
                id="cs_tent_main",
                label="Main tent",
                role="eq",
                status="12 x 16 ft user-reported planning size; exact deployed footprint requires measurement",
                rect=(14.5, 1.5, 16, 12),
                fill="#e6b800",
                dims_label="12 x 16 ft reported",
                buffer_ft=0.5,
                label_anchor=(22.5, 7.5),
            ),
            Equipment(
                id="cs_tent_addon",
                label="Add-on room",
                role="eq",
                status="8 x 8 ft user-reported size attached to one end; centered alignment is a planning assumption",
                rect=(30.5, 3.5, 8, 8),
                fill="#d9a900",
                dims_label="8 x 8 ft reported",
                buffer_ft=0.5,
            ),
        ],
    ),
    Pass(
        id="bg_primary",
        name="B. + G. — Pass A / Two Tents",
        color="#c27ba0",
        area_sqft=600,
        area_note="538 sq ft nominal tents; only 62 sq ft remains for all clearance and access",
        source="planning/households/bg.md",
        polygon=[
            (0, 0),
            (27, 0),
            (27, 30),
            (6, 30),
            (6, 19),
            (24, 19),
            (24, 13),
            (0, 13),
        ],
        default_bbox_origin=(75, 160),
        label_anchor=(13.5, 11.5),
        equipment=[
            Equipment(
                id="bg_primary_tent",
                label="Primary tent",
                role="eq",
                status="confirmed for planning",
                rect=(0.5, 0, 26, 13),
                fill="#a64d79",
                dims_label="26 x 13 ft (rotated)",
                buffer_ft=0.5,
            ),
            Equipment(
                id="bg_community_tent",
                label="Dressing / closet tent",
                role="placeholder",
                status="estimate; replacement model TBD",
                rect=(6.5, 19.5, 20, 10),
                fill="#c27ba0",
                dims_label="approx. 20 x 10 ft (rotated)",
                buffer_ft=0.5,
            ),
            Equipment(
                id="bg_generator_1",
                label="G1",
                role="placeholder",
                status="generic 2 x 2 ft space reservation; B./G. generator model, dimensions, fuel, exhaust, and operating clearances unknown",
                rect=(24.5, 13.5, 2, 2),
                fill="#cc0000",
                dims_label="",
            ),
            Equipment(
                id="bg_generator_2",
                label="G2",
                role="placeholder",
                status="generic 2 x 2 ft space reservation; B./G. generator model, dimensions, fuel, exhaust, and operating clearances unknown",
                rect=(24.5, 16.5, 2, 2),
                fill="#cc0000",
                dims_label="",
            ),
        ],
    ),
    Pass(
        id="bg_community",
        name="B. + G. — Pass B / Community Tent",
        color="#c27ba0",
        area_sqft=600,
        area_note="20 x 30 ft tent fills the nominal pass; operational clearance remains unresolved",
        source="planning/households/bg.md",
        rect=(20, 30),
        default_bbox_origin=(77, 0),
        equipment=[
            Equipment(
                id="bg_community_tent",
                label="Community tent",
                role="placeholder",
                status="20 x 30 ft specified by user; rainfly, stakes, guy lines, and entrances unverified",
                rect=(0, 0, 20, 30),
                fill="#8e5f83",
                dims_label="20 x 30 ft",
                buffer_ft=0.5,
            ),
        ],
    ),
    Pass(
        id="st",
        name="S. + T.",
        color="#b4a7d6",
        area_sqft=600,
        area_note="264 + 120 + 216 = 600 sq ft",
        source="planning/households/st.md",
        polygon=[
            (0, 0),
            (12, 0),
            (12, 22),
            (8, 22),
            (8, 52),
            (12, 52),
            (12, 70),
            (0, 70),
            (0, 52),
            (4, 52),
            (4, 22),
            (0, 22),
        ],
        default_bbox_origin=(130, 120),
        label_anchor=(6, 54.5),
        annotations=[(6, 37, "4 x 30 ft connector path")],
        equipment=[
            Equipment(
                id="st_tent",
                label="Primary tent",
                role="eq",
                status="legacy assumed 10 x 20 ft tent in the connected geographic reference",
                rect=(1, 1, 10, 20),
                fill="#8e7cc3",
                dims_label="10 x 20 ft",
                buffer_ft=0.5,
            ),
            Equipment(
                id="st_portapotty",
                label="Handicap Portapotty",
                role="eq",
                status="legacy assumed 6 x 6 ft ADA unit in the connected geographic reference",
                rect=(3, 62, 6, 6),
                fill="#674ea7",
                dims_label="6 x 6 ft ADA",
                buffer_ft=0.5,
            ),
        ],
    ),
]


def pass_by_id(pass_id: str) -> Pass:
    return next(pass_definition for pass_definition in PASSES if pass_definition.id == pass_id)


def equipment_by_id(pass_definition: Pass, equipment_id: str) -> Equipment:
    return next(equipment for equipment in pass_definition.equipment if equipment.id == equipment_id)


def shifted_equipment(equipment: Equipment, origin_x: float, origin_y: float) -> Equipment:
    rect = equipment.rect
    if rect is not None:
        x, y, width, height = rect
        rect = (x - origin_x, y - origin_y, width, height)
    ellipse = equipment.ellipse
    if ellipse is not None:
        cx, cy, rx, ry = ellipse
        ellipse = (cx - origin_x, cy - origin_y, rx, ry)
    line = equipment.line
    if line is not None:
        x1, y1, x2, y2 = line
        line = (x1 - origin_x, y1 - origin_y, x2 - origin_x, y2 - origin_y)
    anchor = equipment.label_anchor
    if anchor is not None:
        anchor = (anchor[0] - origin_x, anchor[1] - origin_y)
    return replace(
        equipment,
        rect=rect,
        ellipse=ellipse,
        line=line,
        label_anchor=anchor,
    )


_a_source = pass_by_id("a")
_st_source = pass_by_id("st")
_ss_shower_source = pass_by_id("ss_shower")

_st_yurt_area_sqft = round(math.pi * 10**2, 4)
_st_setup_clearance_reserve_sqft = round(600 - _st_yurt_area_sqft - 100 - 100, 4)

# The freeform tool intentionally stages three amenity sections separately so
# households can arrange them before connector walkways are designed. The
# connected PASSES definitions above remain unchanged for the current
# georeferenced map. Visible piece area plus unplaced connector/setup reserve
# still totals exactly 600 sq ft for every qualifying pass.
_a_core = Pass(
    id="a",
    name="A. — Sleeping Camp",
    color=_a_source.color,
    area_sqft=300,
    area_note="300 sq ft section; Yoga / smoking tent detached",
    source=_a_source.source,
    rect=(25, 12),
    default_bbox_origin=_a_source.default_bbox_origin,
    compact_label="A. — sleeping section — 300 sq ft",
    label_anchor=(12.5, 11.5),
    equipment=[equipment_by_id(_a_source, "a_sleep")],
    kind="pass_section",
    parent_pass_id="a",
)

_st_core = Pass(
    id="st",
    name="S. + T. — 20 ft Yurt",
    color=_st_source.color,
    area_sqft=_st_yurt_area_sqft,
    area_note="20 ft diameter circle; entry and anchor envelope unverified",
    source=_st_source.source,
    ellipse=(10, 10, 10, 10),
    default_bbox_origin=_st_source.default_bbox_origin,
    compact_label="20 ft yurt — 314.16 sq ft",
    label_anchor=(10, 10),
    kind="pass_section",
    parent_pass_id="st",
    walkway_reserve_sqft=100,
    setup_clearance_reserve_sqft=_st_setup_clearance_reserve_sqft,
    reserve_note="Up to 100 sq ft for a future connector plus 85.8407 sq ft for yurt entry, platform edge, anchors, ropes, or setup clearance",
)

_ss_shower_core = Pass(
    id="ss_shower",
    name="S. + S. — Shower Section",
    color=_ss_shower_source.color,
    area_sqft=432,
    area_note="432 sq ft section; 66 sq ft reserved for a future walkway",
    source=_ss_shower_source.source,
    rect=(24, 18),
    default_bbox_origin=_ss_shower_source.default_bbox_origin,
    label_anchor=(12, 16.2),
    equipment=[
        equipment
        for equipment in _ss_shower_source.equipment
        if equipment.id != "ss_fire_pit"
    ],
    annotations=[(12, 8.2, "Water trailer T'd into shower trailer")],
    kind="pass_section",
    parent_pass_id="ss_shower",
    walkway_reserve_sqft=66,
)

LAYOUT_PASSES: list[Pass] = [
    _ss_shower_core if pass_definition.id == "ss_shower" else
    _a_core if pass_definition.id == "a" else
    _st_core if pass_definition.id == "st" else
    pass_definition
    for pass_definition in PASSES
]

DETACHED_PARTS: list[Pass] = [
    Pass(
        id="a_yoga",
        name="A. — Yoga / Smoking Tent (detached)",
        color=_a_source.color,
        area_sqft=300,
        source=_a_source.source,
        rect=(12, 25),
        default_bbox_origin=(106.5, 128),
        compact_label="Detached Yoga / smoking section — 300 sq ft",
        label_anchor=(6, 1),
        equipment=[shifted_equipment(equipment_by_id(_a_source, "a_yoga"), 6.5, 12)],
        kind="detached_part",
        parent_pass_id="a",
    ),
    Pass(
        id="st_portapotty",
        name="S. + T. — Portapotty End (detached)",
        color=_st_source.color,
        area_sqft=100,
        source=_st_source.source,
        rect=(10, 10),
        default_bbox_origin=(135, 165),
        compact_label="Detached portapotty end — 100 sq ft",
        label_anchor=(5, 1),
        equipment=[
            Equipment(
                id="st_portapotty",
                label="Handicap Portapotty",
                role="eq",
                status="assumed 6 x 6 ft ADA unit; door direction, turning space, servicing route, and accessible approach remain unverified",
                rect=(2, 2, 6, 6),
                fill="#674ea7",
                dims_label="6 x 6 ft ADA",
            )
        ],
        kind="detached_part",
        parent_pass_id="st",
    ),
    Pass(
        id="ss_firepit",
        name="S. + S. — Fire-pit End (detached)",
        color=_ss_shower_source.color,
        area_sqft=102,
        source=_ss_shower_source.source,
        rect=(10.2, 10),
        default_bbox_origin=(131.9, 190),
        compact_label="Detached fire-pit end — 102 sq ft",
        label_anchor=(5.1, 1),
        equipment=[shifted_equipment(equipment_by_id(_ss_shower_source, "ss_fire_pit"), 6.9, 40)],
        kind="detached_part",
        parent_pass_id="ss_shower",
    ),
]

STYLE = """
text{font-family:Arial,Helvetica,sans-serif;fill:#151515}
.title{font-size:15px;font-weight:700}.sub{font-size:9px}
.label{font-size:11px;font-weight:700}.small{font-size:9px}.tiny{font-size:8px}
.pass{stroke:#222;stroke-width:2;fill-opacity:.28}
.eq{stroke-width:2;fill-opacity:.5;stroke:#333}
.placeholder{stroke-width:2;stroke-dasharray:6 4;fill-opacity:.2;stroke:#333}
.clearance{fill:none;stroke:#555;stroke-width:2;stroke-dasharray:5 4}
"""

DETACHED_STYLE = ".detached{stroke:#0b5394;stroke-width:2;stroke-dasharray:8 5;fill-opacity:.22}"


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_pass(p: Pass) -> str:
    bbox_w, bbox_h = p.bbox()
    view_w = bbox_w + 2 * MARGIN_FT
    view_h = bbox_h + 2 * MARGIN_FT
    px_w = round(view_w * SCALE)
    px_h = round(view_h * SCALE)

    def X(x: float) -> float:
        return round((x + MARGIN_FT) * SCALE, 1)

    def Y(y: float) -> float:
        return round((y + MARGIN_FT) * SCALE, 1)

    parts: list[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{px_w}" height="{px_h}" '
        f'viewBox="0 0 {px_w} {px_h}" role="img" aria-labelledby="title desc">'
    )
    if p.kind == "pass":
        parts.append(f'<title id="title">{esc(p.name)} — 600 sq ft pass</title>')
        parts.append(
            '<desc id="desc">Standalone provisional pass drawing, decomposed from '
            "the public group-site planning overlay.</desc>"
        )
    else:
        title_kind = "detached planning section" if p.kind == "detached_part" else "planning section"
        parts.append(f'<title id="title">{esc(p.name)} — {title_kind}</title>')
        parts.append(
            '<desc id="desc">Standalone provisional planning drawing for the '
            "freeform camp arrangement tool.</desc>"
        )
    style = STYLE + (DETACHED_STYLE if p.kind == "detached_part" else "")
    parts.append(f"<defs><style>{style}</style></defs>")
    # Boundary
    boundary_class = "detached" if p.kind == "detached_part" else "pass"
    if p.polygon is not None:
        pts = " ".join(f"{X(x)},{Y(y)}" for x, y in p.polygon)
        parts.append(f'<polygon points="{pts}" class="{boundary_class}" fill="{p.color}"/>')
    elif p.ellipse is not None:
        cx, cy, rx, ry = p.ellipse
        parts.append(
            f'<ellipse cx="{X(cx)}" cy="{Y(cy)}" rx="{rx * SCALE:g}" ry="{ry * SCALE:g}" '
            f'class="{boundary_class}" fill="{p.color}"/>'
        )
    else:
        w, h = p.rect  # type: ignore[misc]
        pts = " ".join(f"{X(px)},{Y(py)}" for px, py in [
            (0, 0), (w, 0), (w, h), (0, h)
        ])
        parts.append(f'<polygon points="{pts}" class="{boundary_class}" fill="{p.color}"/>')

    # Equipment
    for eq in p.equipment:
        cls = "eq" if eq.role == "eq" else "placeholder"
        if eq.ellipse is not None:
            cx, cy, rx, ry = eq.ellipse
            if eq.buffer_ft:
                b = eq.buffer_ft
                parts.append(
                    f'<ellipse cx="{X(cx)}" cy="{Y(cy)}" rx="{(rx + b) * SCALE:g}" ry="{(ry + b) * SCALE:g}" '
                    f'class="clearance" aria-label="{esc(eq.label)} provisional clearance zone"/>'
                )
            parts.append(
                f'<ellipse cx="{X(cx)}" cy="{Y(cy)}" rx="{rx * SCALE:g}" ry="{ry * SCALE:g}" '
                f'class="{cls}" fill="{eq.fill}"/>'
            )
            anchor_x, anchor_y = eq.label_anchor if eq.label_anchor is not None else (cx, cy)
            lx, ly = X(anchor_x), Y(anchor_y)
            if eq.show_label:
                parts.append(
                    f'<text x="{lx}" y="{ly - 5}" text-anchor="middle" class="tiny">{esc(eq.label)}</text>'
                )
                if eq.dims_label:
                    parts.append(
                        f'<text x="{lx}" y="{ly + 8}" text-anchor="middle" class="tiny">{esc(eq.dims_label)}</text>'
                    )
        elif eq.rect is not None:
            x, y, w, h = eq.rect
            if eq.buffer_ft:
                b = eq.buffer_ft
                buffer_pts = " ".join(f"{X(px)},{Y(py)}" for px, py in [
                    (x - b, y - b),
                    (x + w + b, y - b),
                    (x + w + b, y + h + b),
                    (x - b, y + h + b),
                ])
                parts.append(
                    f'<polygon points="{buffer_pts}" class="clearance" '
                    f'aria-label="{esc(eq.label)} provisional clearance zone"/>'
                )
            pts = " ".join(f"{X(px)},{Y(py)}" for px, py in [
                (x, y), (x + w, y), (x + w, y + h), (x, y + h)
            ])
            parts.append(f'<polygon points="{pts}" class="{cls}" fill="{eq.fill}"/>')
            anchor_x, anchor_y = eq.label_anchor if eq.label_anchor is not None else (x + w / 2, y + h / 2)
            lx, ly = X(anchor_x), Y(anchor_y)
            transform = (
                f' transform="rotate({eq.label_rotation:g} {lx} {ly})"'
                if eq.label_rotation
                else ""
            )
            if eq.show_label:
                parts.append(
                    f'<text x="{lx}" y="{ly - 5}" text-anchor="middle" class="tiny"{transform}>{esc(eq.label)}</text>'
                )
                if eq.dims_label:
                    parts.append(
                        f'<text x="{lx}" y="{ly + 8}" text-anchor="middle" class="tiny"{transform}>{esc(eq.dims_label)}</text>'
                    )
        elif eq.line is not None:
            x1, y1, x2, y2 = eq.line
            parts.append(
                f'<line x1="{X(x1)}" y1="{Y(y1)}" x2="{X(x2)}" y2="{Y(y2)}" '
                f'stroke="{eq.fill}" stroke-width="6" stroke-linecap="round"/>'
            )
            anchor_x, anchor_y = eq.label_anchor if eq.label_anchor is not None else (max(x1, x2) + 1, (y1 + y2) / 2)
            lx, ly = X(anchor_x), Y(anchor_y)
            transform = (
                f' transform="rotate({eq.label_rotation:g} {lx} {ly})"'
                if eq.label_rotation
                else ""
            )
            if eq.show_label:
                parts.append(f'<text x="{lx}" y="{ly - 3}" class="tiny"{transform}>{esc(eq.label)}</text>')
                if eq.dims_label:
                    parts.append(f'<text x="{lx}" y="{ly + 9}" class="tiny"{transform}>{esc(eq.dims_label)}</text>')

    for x, y, label in p.annotations:
        parts.append(
            f'<text x="{X(x)}" y="{Y(y)}" text-anchor="middle" '
            f'class="tiny">{esc(label)}</text>'
        )

    # Boundary labels
    anchor_x, anchor_y = p.label_anchor if p.label_anchor is not None else (bbox_w / 2, bbox_h / 2)
    label_x = X(anchor_x)
    label_x_name = label_x - 10 if p.label_rotation else label_x
    label_x_area = label_x + 10 if p.label_rotation else label_x
    label_y_name = Y(anchor_y) - 14
    label_y_area = Y(anchor_y) + 4
    name_transform = (
        f' transform="rotate({p.label_rotation:g} {label_x_name} {label_y_name})"'
        if p.label_rotation
        else ""
    )
    area_transform = (
        f' transform="rotate({p.label_rotation:g} {label_x_area} {label_y_area})"'
        if p.label_rotation
        else ""
    )
    if p.compact_label:
        parts.append(
            f'<text x="{label_x}" y="{Y(anchor_y)}" text-anchor="middle" '
            f'class="small">{esc(p.compact_label)}</text>'
        )
    else:
        parts.append(
            f'<text x="{label_x_name}" y="{label_y_name}" text-anchor="middle" class="label"{name_transform}>{esc(p.name)}</text>'
        )
        parts.append(
            f'<text x="{label_x_area}" y="{label_y_area}" text-anchor="middle" class="small"{area_transform}>{p.area_sqft:g} sq ft'
            f'{" pass" if not p.area_note else ""}</text>'
        )
        if p.area_note:
            parts.append(
                f'<text x="{label_x}" y="{label_y_area + 12}" text-anchor="middle" class="tiny">{esc(p.area_note)}</text>'
            )

    parts.append("</svg>")
    return "\n".join(parts)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {
        "generated_by": "scripts/build_pass_svgs.py",
        "note": (
            "Freeform local layout data for maps/viewer/pass-layout.html. Not "
            "georeferenced. Three amenity sections are detached for staging; "
            "their parent-pass connector or setup-clearance area remains "
            "unplaced. default_x_ft/default_y_ft use each SVG viewBox top-left."
        ),
        "margin_ft": MARGIN_FT,
        "scale_px_per_ft_in_files": SCALE,
        "planning_summary": {
            "households": 7,
            "passes": len(PASSES),
            "total_planning_area_sqft": sum(pass_definition.area_sqft for pass_definition in PASSES),
            "detached_parts": len(DETACHED_PARTS),
            "visible_piece_area_sqft": sum(piece.area_sqft for piece in [*LAYOUT_PASSES, *DETACHED_PARTS]),
            "walkway_reserve_sqft": sum(piece.walkway_reserve_sqft for piece in LAYOUT_PASSES),
            "setup_clearance_reserve_sqft": sum(piece.setup_clearance_reserve_sqft for piece in LAYOUT_PASSES),
            "unplaced_reserve_sqft": sum(
                piece.walkway_reserve_sqft + piece.setup_clearance_reserve_sqft
                for piece in LAYOUT_PASSES
            ),
        },
        "passes": [],
        "detached_parts": [],
    }

    def emit_piece(p: Pass, collection: str) -> None:
        svg = render_pass(p)
        out_path = OUT_DIR / f"{p.id}.svg"
        out_path.write_text(svg + "\n", encoding="utf-8")

        bbox_w, bbox_h = p.bbox()
        view_w = round(bbox_w + 2 * MARGIN_FT, 4)
        view_h = round(bbox_h + 2 * MARGIN_FT, 4)
        ox, oy = p.default_bbox_origin

        piece_data = {
            "id": p.id,
            "name": p.name,
            "file": f"{p.id}.svg",
            "color": p.color,
            "area_sqft": p.area_sqft,
            "kind": p.kind,
            "parent_pass_id": p.parent_pass_id or p.id,
            "pass_allocation_sqft": p.pass_allocation_sqft,
            "walkway_reserve_sqft": p.walkway_reserve_sqft,
            "bbox_width_ft": round(bbox_w, 4),
            "bbox_height_ft": round(bbox_h, 4),
            "viewbox_width_ft": view_w,
            "viewbox_height_ft": view_h,
            "default_x_ft": round(ox - MARGIN_FT, 4),
            "default_y_ft": round(oy - MARGIN_FT, 4),
        }
        unplaced_reserve = p.walkway_reserve_sqft + p.setup_clearance_reserve_sqft
        if p.setup_clearance_reserve_sqft:
            piece_data["setup_clearance_reserve_sqft"] = p.setup_clearance_reserve_sqft
        if unplaced_reserve:
            piece_data["unplaced_reserve_sqft"] = unplaced_reserve
        if p.reserve_note:
            piece_data["reserve_note"] = p.reserve_note
        manifest[collection].append(piece_data)

    for p in LAYOUT_PASSES:
        emit_piece(p, "passes")
    for p in DETACHED_PARTS:
        emit_piece(p, "detached_parts")

    manifest_path = OUT_DIR / "passes-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(
        f"Wrote {len(LAYOUT_PASSES)} pass SVGs, {len(DETACHED_PARTS)} detached "
        f"piece SVGs, and {manifest_path.name} to {OUT_DIR}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
