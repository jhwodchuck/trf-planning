#!/usr/bin/env python3
"""Build one standalone, self-contained SVG per 600 sq ft pass, plus a manifest
that the interactive drag-layout tool (maps/viewer/pass-layout.html) reads.

This script does not touch any network service. It decomposes the same
provisional geometry already committed in maps/overlays/group-site-v0.1.svg
and maps/data/group-site-v0.1.geojson into one file per pass so each can be
refined independently and then freely repositioned on a separate master
canvas, without being tied to the georeferenced viewer/geometry.

Run:
    python scripts/build_pass_svgs.py

Outputs:
    maps/overlays/passes/<id>.svg           one file per pass
    maps/overlays/passes/passes-manifest.json
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
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
    # Either a rect (x, y, w, h) or a line (x1, y1, x2, y2), all relative to
    # the pass's own bounding-box origin (its top-left corner, before margin).
    rect: tuple[float, float, float, float] | None = None
    line: tuple[float, float, float, float] | None = None
    fill: str = "#3d85c6"
    dims_label: str = ""
    # Optional planning buffer around nominal equipment geometry. Used to
    # show unverified rainfly, rope, anchor, foot, or ballast clearance.
    buffer_ft: float = 0.0


@dataclass
class Pass:
    id: str
    name: str
    color: str
    area_sqft: float
    source: str
    # Rectangle boundary (w, h) OR an explicit polygon, both relative to the
    # pass's own bounding-box origin (0, 0).
    rect: tuple[float, float] | None = None
    polygon: list[tuple[float, float]] | None = None
    area_note: str = ""
    equipment: list[Equipment] = field(default_factory=list)
    annotations: list[tuple[float, float, str]] = field(default_factory=list)
    # Anchor point (relative to the bbox origin) for the household name/area
    # labels. Defaults to the bbox center, which is always inside a rect
    # boundary but can fall in the notch of a non-rectangular polygon, so
    # notched passes (e.g. jason_catrina) must set this explicitly.
    label_anchor: tuple[float, float] | None = None
    # Where this pass's bounding-box top-left sits in the original
    # group-site-v0.1.svg local layout (feet). Used only as the manifest's
    # default position so the master tool opens matching the current README
    # arrangement.
    default_bbox_origin: tuple[float, float] = (0.0, 0.0)

    def bbox(self) -> tuple[float, float]:
        if self.rect is not None:
            return self.rect
        assert self.polygon is not None
        xs = [p[0] for p in self.polygon]
        ys = [p[1] for p in self.polygon]
        return (max(xs) - min(xs), max(ys) - min(ys))


PASSES: list[Pass] = [
    Pass(
        id="jason_catrina",
        name="Jason + Catrina",
        color="#e69138",
        area_sqft=600,
        area_note="598.875 sq ft RV + canopy equipment footprint, plus 1.125 sq ft boundary buffer",
        source="planning/households/jason-and-catrina.md",
        polygon=[
            (29.25, 31.5),
            (29.25, 0),
            (15, 0),
            (15, 21.4167),
            (0, 21.4167),
            (0, 31.5),
        ],
        default_bbox_origin=(140.75, 73.5),
        label_anchor=(15.05, 17.63),
        equipment=[
            Equipment(
                id="jason_rv",
                label="Wildcat deployed zone",
                role="eq",
                status="working measurement; camper model/data-plate not yet confirmed",
                rect=(15, 0, 14.25, 31.5),
                fill="#3d85c6",
                dims_label="31.5 x 14.25 ft",
            ),
            Equipment(
                id="jason_canopy",
                label="Canopy",
                role="eq",
                status="working template; dimensions must be verified",
                rect=(0, 21.4167, 15, 10),
                fill="#f6b26b",
                dims_label="15 x 10 ft",
            ),
        ],
    ),
    Pass(
        id="shane_camper",
        name="Shane + Sabrina — Pass A / Camper",
        color="#93c47d",
        area_sqft=600,
        source="planning/households/shane-and-sabrina.md",
        rect=(20, 30),
        default_bbox_origin=(110, 40),
        equipment=[
            Equipment(
                id="shane_camper_placeholder",
                label="Camper",
                role="placeholder",
                status="not to scale; actual deployed dimensions required",
                rect=(3, 4, 14, 22),
                fill="#4d8c4d",
                dims_label="dimensions required",
            ),
        ],
    ),
    Pass(
        id="shane_shower",
        name="Shane + Sabrina — Pass B / Shower",
        color="#93c47d",
        area_sqft=600,
        source="equipment/shane-sabrina-16ft-shower-trailer.md",
        rect=(20, 30),
        default_bbox_origin=(85, 30),
        equipment=[
            Equipment(
                id="shane_shower_trailer",
                label="16 ft flatbed shower trailer",
                role="placeholder",
                status="length confirmed; width and overall coupler length TBD",
                line=(10, 7, 10, 23),
                fill="#245b24",
                dims_label="16 ft long; width TBD",
            ),
        ],
    ),
    Pass(
        id="mc_camper",
        name="MC + Elizabeth — Pass A / Camper",
        color="#6fa8dc",
        area_sqft=600,
        source="planning/households/mc-and-elizabeth.md",
        rect=(20, 30),
        default_bbox_origin=(55, 50),
        equipment=[
            Equipment(
                id="mc_camper_placeholder",
                label="Camper",
                role="placeholder",
                status="not to scale; actual deployed dimensions required",
                rect=(3, 4, 14, 22),
                fill="#3d85c6",
                dims_label="dimensions required",
            ),
        ],
    ),
    Pass(
        id="mc_support",
        name="MC + Elizabeth — Pass B / Support",
        color="#6fa8dc",
        area_sqft=600,
        source="planning/households/mc-and-elizabeth.md",
        rect=(20, 30),
        default_bbox_origin=(30, 40),
        equipment=[],
    ),
    Pass(
        id="amanda",
        name="Amanda",
        color="#76a5af",
        area_sqft=600,
        source="planning/amanda-site-notes.md",
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
                id="amanda_sleep",
                label="Sleeping tent",
                role="eq",
                status="confirmed",
                rect=(2.5, 1, 20, 10),
                fill="#76a5af",
                dims_label="20 x 10 ft (rotated)",
                buffer_ft=0.5,
            ),
            Equipment(
                id="amanda_yoga",
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
        id="chris_sallie",
        name="Chris + Sallie",
        color="#ffd966",
        area_sqft=600,
        source="planning/households/chris-and-sallie.md",
        rect=(20, 30),
        default_bbox_origin=(75, 115),
        equipment=[
            Equipment(
                id="chris_tent",
                label="Tent",
                role="eq",
                status="confirmed",
                rect=(2, 8, 16, 20),
                fill="#e6b800",
                dims_label="16 x 20 ft",
            ),
            Equipment(
                id="chris_canopy_placeholder",
                label="Canopy",
                role="placeholder",
                status="not to scale; dimensions required — do not infer 10x10",
                rect=(0, 0, 20, 6),
                fill="#f1c232",
                dims_label="dimensions required",
            ),
        ],
    ),
    Pass(
        id="birdie_primary",
        name="Birdie + Gustav — Pass A / Primary Tent",
        color="#c27ba0",
        area_sqft=600,
        source="planning/households/birdie-and-gustav.md",
        rect=(20, 30),
        default_bbox_origin=(45, 120),
        equipment=[
            Equipment(
                id="birdie_primary_tent",
                label="Primary tent",
                role="eq",
                status="confirmed for planning",
                rect=(3.5, 2, 13, 26),
                fill="#a64d79",
                dims_label="13 x 26 ft",
            ),
        ],
    ),
    Pass(
        id="birdie_closet",
        name="Birdie + Gustav — Pass B / Closet Tent",
        color="#c27ba0",
        area_sqft=600,
        source="planning/households/birdie-and-gustav.md",
        rect=(20, 30),
        default_bbox_origin=(20, 110),
        equipment=[
            Equipment(
                id="birdie_closet_tent",
                label="Closet tent",
                role="placeholder",
                status="estimate; replacement model TBD",
                rect=(5, 5, 10, 20),
                fill="#c27ba0",
                dims_label="approx. 10 x 20 ft",
            ),
        ],
    ),
    Pass(
        id="stephane_true",
        name="Stephane + True",
        color="#b4a7d6",
        area_sqft=600,
        source="planning/households/stephane-and-true.md",
        rect=(20, 30),
        default_bbox_origin=(130, 120),
        equipment=[
            Equipment(
                id="stephane_tent_placeholder",
                label="Tent",
                role="placeholder",
                status="not to scale; dimensions required",
                rect=(5, 6, 10, 18),
                fill="#8e7cc3",
                dims_label="dimensions required",
            ),
        ],
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
    parts.append(f'<title id="title">{esc(p.name)} — 600 sq ft pass</title>')
    parts.append(
        f'<desc id="desc">Standalone provisional pass drawing, decomposed from '
        f"maps/overlays/group-site-v0.1.svg. Source record: {esc(p.source)}.</desc>"
    )
    parts.append(f"<defs><style>{STYLE}</style></defs>")
    parts.append(f'<rect width="{px_w}" height="{px_h}" fill="#f6f5f0"/>')

    # Boundary
    if p.polygon is not None:
        pts = " ".join(f"{X(x)},{Y(y)}" for x, y in p.polygon)
        parts.append(f'<polygon points="{pts}" class="pass" fill="{p.color}"/>')
    else:
        w, h = p.rect  # type: ignore[misc]
        pts = " ".join(f"{X(px)},{Y(py)}" for px, py in [
            (0, 0), (w, 0), (w, h), (0, h)
        ])
        parts.append(f'<polygon points="{pts}" class="pass" fill="{p.color}"/>')

    # Equipment
    for eq in p.equipment:
        cls = "eq" if eq.role == "eq" else "placeholder"
        if eq.rect is not None:
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
            lx, ly = X(x + w / 2), Y(y + h / 2)
            parts.append(
                f'<text x="{lx}" y="{ly - 5}" text-anchor="middle" class="tiny">{esc(eq.label)}</text>'
            )
            if eq.dims_label:
                parts.append(
                    f'<text x="{lx}" y="{ly + 8}" text-anchor="middle" class="tiny">{esc(eq.dims_label)}</text>'
                )
        elif eq.line is not None:
            x1, y1, x2, y2 = eq.line
            parts.append(
                f'<line x1="{X(x1)}" y1="{Y(y1)}" x2="{X(x2)}" y2="{Y(y2)}" '
                f'stroke="{eq.fill}" stroke-width="6" stroke-linecap="round"/>'
            )
            lx, ly = X(max(x1, x2) + 1), Y((y1 + y2) / 2)
            parts.append(f'<text x="{lx}" y="{ly - 3}" class="tiny">{esc(eq.label)}</text>')
            if eq.dims_label:
                parts.append(f'<text x="{lx}" y="{ly + 9}" class="tiny">{esc(eq.dims_label)}</text>')

    for x, y, label in p.annotations:
        parts.append(
            f'<text x="{X(x)}" y="{Y(y)}" text-anchor="middle" '
            f'class="tiny">{esc(label)}</text>'
        )

    # Boundary labels
    anchor_x, anchor_y = p.label_anchor if p.label_anchor is not None else (bbox_w / 2, bbox_h / 2)
    label_x = X(anchor_x)
    label_y_name = Y(anchor_y) - 14
    label_y_area = Y(anchor_y) + 4
    parts.append(
        f'<text x="{label_x}" y="{label_y_name}" text-anchor="middle" class="label">{esc(p.name)}</text>'
    )
    parts.append(
        f'<text x="{label_x}" y="{label_y_area}" text-anchor="middle" class="small">{p.area_sqft:g} sq ft'
        f'{" pass" if not p.area_note else ""}</text>'
    )
    if p.area_note:
        parts.append(
            f'<text x="{label_x}" y="{label_y_area + 12}" text-anchor="middle" class="tiny">{esc(p.area_note)}</text>'
        )

    # Footer / provenance
    parts.append(
        f'<text x="{X(0)}" y="{px_h - 6}" class="tiny">Source: {esc(p.source)} — generated by scripts/build_pass_svgs.py</text>'
    )

    parts.append("</svg>")
    return "\n".join(parts)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {
        "generated_by": "scripts/build_pass_svgs.py",
        "note": (
            "Freeform local layout data for maps/viewer/pass-layout.html. Not "
            "georeferenced. default_x_ft/default_y_ft reproduce the arrangement "
            "already committed in maps/overlays/group-site-v0.1.svg, expressed "
            "as the top-left corner of each pass SVG's own viewBox (which "
            "includes a fixed margin around the true 600 sq ft boundary)."
        ),
        "margin_ft": MARGIN_FT,
        "scale_px_per_ft_in_files": SCALE,
        "passes": [],
    }

    for p in PASSES:
        svg = render_pass(p)
        out_path = OUT_DIR / f"{p.id}.svg"
        out_path.write_text(svg + "\n", encoding="utf-8")

        bbox_w, bbox_h = p.bbox()
        view_w = round(bbox_w + 2 * MARGIN_FT, 4)
        view_h = round(bbox_h + 2 * MARGIN_FT, 4)
        ox, oy = p.default_bbox_origin

        manifest["passes"].append(
            {
                "id": p.id,
                "name": p.name,
                "file": f"{p.id}.svg",
                "color": p.color,
                "area_sqft": p.area_sqft,
                "bbox_width_ft": round(bbox_w, 4),
                "bbox_height_ft": round(bbox_h, 4),
                "viewbox_width_ft": view_w,
                "viewbox_height_ft": view_h,
                "default_x_ft": round(ox - MARGIN_FT, 4),
                "default_y_ft": round(oy - MARGIN_FT, 4),
                "source": p.source,
            }
        )

    manifest_path = OUT_DIR / "passes-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {len(PASSES)} pass SVGs and {manifest_path.name} to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
