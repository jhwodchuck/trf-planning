# Site Data: Known, Assumed, and Missing

Last updated: **2026-07-27**

## Confirmed design intent from the owner

| Item | Current intent |
|---|---|
| Maximum planning area | 600 sq ft, subject to TRF confirmation |
| Camper front/hitch | South |
| Camper entry door | West, away from road |
| Road | Assumed east/right side of plot |
| Canopy | Along south edge near southwest corner |
| Canopy orientation | Long side perpendicular to camper |
| Generators | Two Cummins Onan P4500i units |
| Generator screening | Temporary fence/screen near camper front to reduce visibility |
| Camper slides | Fully deployed in the operating plan |

## Facts requiring confirmation

| Priority | Item | Why it matters | Required evidence |
|---|---|---|---|
| Critical | Exact requested/assigned plot | All terrain and boundary work depends on it | Marked official map plus coordinates or field stakes |
| Critical | Approved area: 600 or 525 sq ft | Determines whether the concept can fit | Written TRF response |
| Critical | Camper model: 29MK or 293MK | Published dimensions and floor plans differ | VIN/data plate/title photo |
| Critical | Actual deployed camper dimensions | Largest object and roadway-side slides | Field measurements/photos |
| Critical | Generator operating location | CO/fire safety may make concept infeasible | Dimensioned clearance study |
| High | Plot shape and side dimensions | Equal areas can have very different usability | Field survey/approval document |
| High | Road-edge location and setback interpretation | East-side slides may conflict | Field measurement plus TRF response |
| High | Canopy model/dimensions | Determines southwest fit and anchors | Model/manual and measurements |
| High | Fence dimensions/anchoring | Requires approval; affects egress and ventilation | Product data/sketch and TRF response |
| High | F-250 cab and parking requirement | Truck could consume most remaining area | VIN/photo, measurement, TRF response |
| Medium | Trees, roots, slopes, ditches, drainage | Affects leveling, stakes, structures, and access | Site survey and photos |
| Medium | Neighbor positions and occupied openings | Generator and privacy constraints | Assigned plot map/field observation |
| Medium | Utilities and waste handling | Changes hose/cord paths and trip hazards | Site rules and equipment inventory |

## Area budget worksheet

Do not treat estimates as reservations; objects can overlap in plan view only when they do not coexist in the same operating state.

| Object/zone | Estimated area | Verified area | Notes |
|---|---:|---:|---|
| Camper body | 252.7 sq ft |  | Published 31 ft 7 in × 8 ft rectangle |
| Camper slides | about 77–87 sq ft additional |  | Rough scale-derived estimate only |
| Entry stairs/landing |  |  | Must remain clear for egress |
| Canopy |  |  | Need exact roof and anchor footprint |
| Two generator bodies | 6.2 sq ft |  | Excludes all safety clearances |
| Generator operating/safety zone |  |  | Potentially much larger than body footprint |
| Fence/screen feet/posts |  |  | Include gate and setback |
| Fuel and fire protection |  |  | Separate from generators as required |
| Truck, if onsite |  |  | Likely 19.3–22.2 ft long depending cab |
| Walkways/emergency route |  |  | Must remain usable |
| **Total unique occupied/required area** |  |  | Compare with approved limit |

## Candidate plot geometry tests

Once the approved area is known, test multiple shapes rather than assuming a square:

| Area | Example dimensions | Immediate observation |
|---:|---|---|
| 600 sq ft | 20 × 30 ft | Shorter than the published 31-ft-7-in camper length |
| 600 sq ft | 15 × 40 ft | Length works, but width is tight after body, east-side slides, west-side stairs, and circulation |
| 600 sq ft | 12 × 50 ft | Likely too narrow for slides, stairs, and canopy |
| 525 sq ft | 15 × 35 ft | Very constrained with deployed camper and roadway setback |
| 525 sq ft | 10.5 × 50 ft | Impractical width for this arrangement |

These examples demonstrate why exact plot shape matters. They are not proposed boundaries.

## Orientation implications

With the camper floor plan rotated clockwise:

- the hitch/nose points south;
- the door and stairs project west;
- the two side slides project east toward the assumed road;
- the rear slide projects north;
- the canopy occupies the southwest region;
- the proposed generator screen occupies part of the south/front region.

The camper should be shifted and dimensioned only after the eastern road edge and 10-ft setback are known. A plan that places the body correctly but lets east-side slides cross the setback is not valid.

## Data capture format

Store plot measurements in a future `data/site/site-survey.csv` with these columns:

```text
id,category,description,value,unit,start_reference,end_reference,source_date,source_type,confidence,notes
```

Recommended confidence values:

- `verified-field`
- `verified-document`
- `published`
- `scale-derived`
- `assumed`

## Gate for starting the final scaled plan

Do not label a drawing `final` until these five items are complete:

1. Exact plot location and geometry.
2. Written TRF area/rule interpretation.
3. Verified camper model and deployed measurements.
4. Exact canopy/fence dimensions.
5. Safe, dimensioned generator operating location.
