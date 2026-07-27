# Known and Missing Site Data

Last updated: **2026-07-27**

## Planning baseline

Use **600 sq ft per qualifying pass** for all working layouts, area calculations, and group-site arrangements. Do not maintain a parallel 525 sq ft planning version unless Jason explicitly changes this assumption.

This is a planning convention. Final field setup must still follow the dimensions and conditions TRF actually approves.

## Current design intent

- Requested area target: **600 sq ft per pass**.
- Working location: immediately north/northeast of Havok camp beside the adjacent access road; orientation only, not an exact boundary.
- Camper nose/hitch: south.
- Camper door and stairs: west, away from the road.
- Road-side slides: east.
- Canopy: west/southwest side; current map template uses 15 × 10 ft.
- Generators: two Cummins Onan P4500i units.
- Temporary screening: near the camper front/south area, without enclosing generator exhaust or cooling airflow.

## Critical unresolved inputs

| Priority | Input | Why it matters |
|---|---|---|
| Critical | Exact assigned/requested boundary | Regional GIS and approximate location cannot establish usable dimensions |
| Critical | Camper model and actual deployed dimensions | Current template and published references differ |
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
| Planning allowance per pass | 600 sq ft | 600 sq ft |
| RV body | Template: 31 ft 6 in × 8 ft 4 in; published Sterling reference differs |  |
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

1. Confirm exact camper model from data plate/title.
2. Field-measure body, slides, stairs, awning, and stabilizers.
3. Explain and resolve the 8-ft versus 8-ft-4-in width difference.
4. Verify the 15 × 10 canopy and all anchors/legs.
5. Keep the final requested polygon at or below **600 sq ft**.
6. Locate the actual road edge and apply the 10-ft setback to the nearest deployed object.
7. Add generator clearances, openings, fuel, cords, and screen.
8. Add truck/access geometry or document off-plot parking.

## Data format

Store measurements in `planning/site-survey.csv` using:

```text
id,category,description,value,unit,start_reference,end_reference,source_date,source_type,confidence,notes
```

Confidence values: `verified-field`, `verified-document`, `published`, `scale-derived`, or `assumed`.

## Gate for a final plan

Do not label a drawing final until the exact boundary, camper measurements, canopy/screen dimensions, generator operating location, and TRF approval conditions are verified.
