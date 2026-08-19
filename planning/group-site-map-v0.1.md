# TRF Group Site Map v0.1

Last updated: **2026-08-16**

## Files

- `maps/viewer/index.html` — interactive aerial overlay; the "Group site v0.1" toggle in the layer control (merged in from the former standalone `group-site-v0.1.html`, which no longer exists).
- `maps/overlays/group-site-v0.1.svg` — historical printable scale reference; the interactive map, GeoJSON, and KML carry the accepted reattached arrangement.
- `maps/data/group-site-v0.1.geojson` — georeferenced planning geometry.
- `maps/overlays/group-site-v0.1.kml` — local Google Earth overlay generated from the GeoJSON for comparison with the dated 2025 camp imagery.
- `maps/overlays/passes/` — the ten current pass polygons, three detached amenity pieces, and two accepted connectors, generated from the shared definitions in `scripts/build_pass_svgs.py`.
- `maps/viewer/pass-layout.html` — interactive tool for dragging and rotating all fifteen SVG pieces on a freeform (non-georeferenced) canvas; its accepted default is also the source for this georeferenced map.
- `planning/2025-camp-layout-reference.md` — dated 2025 Google Earth reference, observations, and 2026 planning consequences.

## Status

This is a **provisional group planning layout**, not a survey or final TRF submission.

Only J. and C.'s placement is tied to the supplied site anchor and road-control points. The full road edge is a planning-grade curve traced from the offline Texas NAIP 2022 aerial and forced through both supplied controls. All other household positions are conceptual and may move.

The line through 30°15'20.86"N 95°50'47.36"W and 30°15'19.63"N 95°50'47.44"W is a hard western limit. No displayed pass or equipment geometry extends west of its extrapolated alignment.

## Planning totals

- Households: **7**
- Passes: **10**
- Planning area per pass: **600 sq ft**
- Total planning area: **6,000 sq ft**
- Compactness objective: **none**
- Disconnected pass polygons: **allowed and preferred when useful**

## Current known structures represented

| Household | Structure | Planning dimensions/status |
|---|---|---|
| J. and C. | Wildcat deployed zone | 31.5 × 14.25 ft |
| J. and C. | Canopy | 15 × 10 ft |
| A. | Sleeping tent | 10 × 20 ft confirmed |
| A. | Yoga Tent | 10 × 17 ft confirmed |
| A. | Allocation connection | Yoga and sleeping sections share a complete 25 ft boundary and form a 25 × 24 ft outer rectangle; no separate connector area |
| C. and S. | Main tent + add-on room | 12 × 16 ft main tent with 8 × 8 ft room attached at one end; centered alignment is provisional |
| C. and S. | Canopy | 10 × 13 ft, user reported; product and anchoring TBD |
| B. and G. | Primary tent | 13 × 26 ft |
| B. and G. | Closet tent | approximately 10 × 20 ft; replacement TBD |
| B. and G. | Community tent | 20 × 30 ft; fills second nominal pass before operational clearances |
| B. and G. | Two generators | Generic 2 × 2 ft placeholders staged in the waist between personal tents; models/dimensions unknown and not approved to operate there |
| S. and S. | Camper body | 36 ft 9 in × 8 ft published; KZ Connect SE C312BHKSE floorplan-informed, model/VIN unconfirmed |
| S. and S. | Camper slide zones | ~3 ft 1 in and ~3 ft 9 in projections; scale-derived from floorplan artwork, unsuitable for approval |
| S. and S. | Main-entry rug zone | provisional 8 × 12 ft working assumption |
| S. and S. | Shower + water trailers + fire pit | Notched 393 sq ft shower/water section and 102 sq ft fire-pit section, reattached by a straight 3 × 35 ft, 105 sq ft allocation connector; width is planning-only |
| M. and E. | Camper | temporary horizontal mirror of S./S. camper-pass concept; all equipment geometry unverified |
| S. and T. | Yurt + handicap portapotty | 20 ft circular yurt plus an assumed 6 × 6 ft unit in a 10 × 10 ft end, reattached by a straight 2 × 50 ft, 100 sq ft allocation connector at one 35° bearing; the portapotty stays near its prior position, 85.8407 sq ft remains unplaced for yurt setup clearance, and the route is not accessibility confirmation |

## Layout strategy

1. Preserve ten full 600 sq ft pass polygons.
2. Do not force two-pass households into a single compact envelope.
3. Keep J. and C. beside the imagery-traced curved road and its 10-foot/14-foot planning offsets.
4. Use a separate shower-trailer polygon for S. and S. in the initial concept.
5. Use S. and S.'s irregular camper pass with slides on one side, both door/step locations on the other, a 3 × 8 ft rear service bay, and a provisional 8 × 12 ft main-entry rug bay.
6. Use a horizontally mirrored copy of S. and S.'s camper-pass concept as M. and E.'s temporary Pass A placeholder; treat every internal feature as unverified.
7. Use A.'s accepted two-piece 600 sq ft arrangement: the 25 × 12 ft sleeping section and 12 × 25 ft Yoga section each contribute 300 sq ft, share a complete 25 ft allocation boundary, and form a 25 × 24 ft outer rectangle.
8. Put B. and G.'s primary and closet tents together in one offset, connected two-lobe 600 sq ft pass; use their second 20 × 30 ft pass for the community tent.
9. Use the accepted straight connectors: 3 × 35 ft (105 sq ft) from S. and S.'s notched shower section to its fire-pit end, and 2 × 50 ft (100 sq ft) at one 35° bearing from S. and T.'s 20 ft circular yurt to its 10 × 10 ft portapotty end. Keep S. and T.'s remaining 85.8407 sq ft unplaced for yurt setup clearance.
10. Leave gaps outside claimed polygons rather than reducing requested area.
11. Retain a conceptual circulation and emergency-access band through the group.
12. Prefer prior disturbed/occupied clearings visible in the 2025-10-20 imagery, subject to household identification and field verification.
13. Keep every pass and equipment footprint east of the user-supplied hard western limit.

## Known limitations

- The broader group boundary has not been surveyed or assigned.
- Household adjacency preferences have not yet been supplied.
- Terrain, trees, drainage, and utility constraints have not been applied household-by-household.
- Several structures still use placeholders.
- S. and T.'s 20 ft yurt circle is the reported wall/platform footprint only; entry, platform edge, anchors, ropes, and setup clearances still require the exact model and field measurements.
- The two connector rectangles are exact allocation accounting, but their usable width, endpoints, surface, slope, and clearances still require field verification. The 4 ft S. and T. connector is not accessibility confirmation.
- The proposed positions may not match the final usable ground visible during field setup.
- The road curve follows the visible campsite-side edge in the offline NAIP imagery and passes through both supplied controls, but it has not been field surveyed.
- The 2025 imagery shows curved roads and irregular occupied clearings, but visible roofs have not yet been tied to specific households or measured control points.
