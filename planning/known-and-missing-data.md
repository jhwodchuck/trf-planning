# Known and Missing Site Data

Last updated: **2026-07-27**

## Current design intent

- Requested area target: about 600 sq ft, subject to TRF confirmation.
- Working location: immediately north/northeast of Havok camp beside the adjacent access road; orientation only, not an exact boundary.
- Camper nose/hitch: south.
- Camper door and stairs: west, away from the road.
- Road-side slides: east.
- Canopy: west/southwest side; current map template uses 15 × 10 ft.
- Generators: two Cummins Onan P4500i units.
- Temporary screening: near the camper front/south area, without enclosing generator exhaust or cooling airflow.

## Resolved camper identification

The owner supplied a manufacturer data-plate photograph on 2026-07-27. The public transcription is in [`../equipment/evidence/2012-wildcat-data-plate.md`](../equipment/evidence/2012-wildcat-data-plate.md).

- Manufacturer model code: **`WCP29MK`**.
- Repository model designation: **29MK**, not 293MK.
- GVWR: **12,275 lb**.
- Front/rear GAWR: **5,200 lb each**.
- Tires: **ST235/80R16/E**.
- Rims: **16X6.0JJ**.

The full VIN and unit identifier are withheld from this public repository. The data plate resolves identification but does not provide body or slide-out dimensions.

## Critical unresolved inputs

| Priority | Input | Why it matters |
|---|---|---|
| Critical | Exact assigned/requested boundary | Regional GIS and approximate location cannot establish usable dimensions |
| Critical | Written 600-versus-525-sq-ft ruling | Controls feasibility and submission geometry |
| Critical | Actual camper body and deployed dimensions | Current template and published dimensional references still differ |
| Critical | Safe generator operating location | CO/fire clearance may exceed available space |
| High | Physical road edge and setback | East-side slides face the road |
| High | Canopy product dimensions and anchoring | Current 15 × 10 value must be verified |
| High | Fence/screen dimensions and approval | Affects area, egress, ventilation, and rule compliance |
| High | F-250 cab and parking requirement | Vehicle is roughly 19–22 ft long depending cab |
| Medium | Trees, roots, branch height, slope, ditches, drainage, and utilities | Affects access, leveling, anchors, and placement |
| Medium | Neighbor boundaries/openings | Affects egress and generator safety |

## Area worksheet

| Object/zone | Current reference | Verified value |
|---|---:|---:|
| RV body | Template: 31 ft 6 in × 8 ft 4 in; published Sterling 29MK reference: about 31 ft 7 in × 8 ft | Model `WCP29MK` verified; dimensions not measured |
| Approximate deployed RV zone | Current template: 31 ft 6 in × 14 ft 3 in |  |
| Canopy | Current template: 15 × 10 ft |  |
| Current stepped requested area | About 598.9 sq ft |  |
| Two generator bodies | About 6.2 sq ft total, excluding clearances |  |
| Generator safety/operating zone | Unknown and potentially dominant |  |
| Fence feet/posts/gate | Unknown |  |
| Truck if onsite | Roughly 19.3–22.2 ft long |  |
| Emergency paths/utilities | Unknown |  |

## Required reconciliation

Before using the current SVG footprint as final:

1. Field-measure camper body, slides, stairs, awning, stabilizers, hitch, and rear extremity.
2. Explain and resolve the 8-ft versus 8-ft-4-in width difference.
3. Verify the 15 × 10 canopy and all anchors/legs.
4. Confirm the 598.9-sq-ft stepped shape is accepted by TRF.
5. Locate the actual road edge and apply the 10-ft setback to the nearest deployed object.
6. Add generator clearances, openings, fuel, cords, and screen.
7. Add truck/access geometry or document off-plot parking.

## Data format

Store measurements in `planning/site-survey.csv` using:

```text
id,category,description,value,unit,start_reference,end_reference,source_date,source_type,confidence,notes
```

Confidence values: `verified-field`, `verified-document`, `published`, `scale-derived`, or `assumed`.

## Gate for a final plan

Do not label a drawing final until the exact boundary, written TRF interpretation, camper measurements, canopy/screen dimensions, and generator operating location are verified.
