# Group Pass Allocation and Household Roster

Last updated: **2026-08-16**

## Planning baseline

- Use **600 sq ft per qualifying pass** for all working layouts.
- Each pass contributes its own 600 sq ft allocation, and those allocations do **not** need to form one compact or contiguous household polygon.
- Compactness, neat rectangles, and land-use efficiency are **not planning goals**.
- Prefer disconnected, stepped, narrow, or irregular polygons when they claim more practical usable area around roads, trees, drainage, neighboring camps, or other constraints.
- Gaps between claimed polygons may remain unallocated; do not shrink the requested pass areas merely to eliminate gaps.
- Final placement must retain roadway setbacks, access, drainage, emergency egress, and any conditions imposed by TRF.

## Household roster

| Household | Primary shelter and major support equipment | Passes | Planning allocation | Household notes |
|---|---|---:|---:|---|
| C. and S. | 12 × 16 ft main tent, 8 × 8 ft end-room, and 10 × 13 ft canopy | 1 | **600 sq ft** | [Planning notes](households/cs.md) |
| B. and G. | 13 × 26 ft primary tent and approximate 10 × 20 ft closet tent with two generic generator placeholders staged between them; 20 × 30 ft community tent in the second | 2 | **1,200 sq ft** | [Planning notes](households/bg.md) |
| A. | Sleeping tent and Yoga Tent canopy | 1 | **600 sq ft** | [Planning notes](a-site-notes.md) |
| M. and E. | Camper; temporary mirrored S./S. pass used until actual geometry is known | 2 | **1,200 sq ft** | [Planning notes](households/me.md) |
| S. and S. | Camper and 16 ft flatbed shower trailer | 2 | **1,200 sq ft** | [Planning notes](households/ss.md) |
| J. and C. | Camper | 1 | **600 sq ft** | [Planning notes](households/jc.md) |
| S. and T. | 20 ft diameter yurt, straight 2 × 50 ft allocation connector, and handicap portapotty | 1 | **600 sq ft** | [Planning notes](households/st.md) |
| **Total** | 3 camper households, 3 tent-based households, 1 yurt-based household, and 1 shower trailer | **10** | **6,000 sq ft** |  |

## Current master map

- [Interactive group map v0.1](../maps/viewer/index.html) — "Group site v0.1" overlay in the merged map viewer
- [Scale drawing v0.1](../maps/overlays/group-site-v0.1.svg) — historical printable reference; use the interactive/georeferenced maps for the accepted arrangement
- [Georeferenced group geometry](../maps/data/group-site-v0.1.geojson)
- [Map assumptions and limitations](group-site-map-v0.1.md)

The v0.1 map preserves ten separate 600 sq ft pass polygons. Only J. and C.'s site is tied to the supplied road controls; all other positions remain conceptual.

The accepted default preserves independently movable amenity pieces while making the field boundary simple. A.'s Yoga / smoking-tent section and sleeping section form a 25 × 24 ft outer rectangle. S. and S.'s fire-pit end is joined to its revised 393 sq ft shower/water section by a straight **3 × 35 ft**, **105 sq ft** connector. S. and T.'s portapotty end is joined to the 20 ft circular yurt by a straight **2 × 50 ft**, **100 sq ft** connector at one 35° bearing, keeping the portapotty section near its prior position and leaving **85.8407 sq ft** reserved for yurt entry, platform edge, anchors, ropes, or setup clearance. The freeform default, GeoJSON, and KML use this same arrangement.

## Allocation summary

- **Camper households:** M. and E.; S. and S.; J. and C..
- **Camper-household passes:** 5.
- **Camper-household planning area:** 3,000 sq ft.
- **Tent-based households:** C. and S.; B. and G.; A.; S. and T..
- **Tent-household passes:** 5.
- **Tent-household planning area:** 3,000 sq ft.
- **Shared-support equipment currently identified:** S. and S.'s 16 ft flatbed shower trailer.
- **Total households:** 7.
- **Total passes:** 10.
- **Total planning area:** 6,000 sq ft.

## Master-layout objective

The optimization target is **maximum practical claimed area and useful placement**, not minimum perimeter, compactness, symmetry, or visual neatness.

A layout is preferable when it:

1. preserves the full 600 sq ft contribution from each pass;
2. uses disconnected boxes or polygons when that avoids wasting claimable ground;
3. wraps around trees, drainage channels, road setbacks, or existing camp features without reducing the total claimed area;
4. places household equipment where it works best even when a household's pass polygons are separated; and
5. leaves unavoidable gaps outside the requested polygons rather than absorbing those gaps into an inefficient compact boundary.

## Master-layout rules

1. Draw every pass allocation as one or more labeled polygons, with the area of each component and the combined pass total shown.
2. For two-pass households, test both contiguous and disconnected arrangements. Prefer whichever provides more useful claimed space and better equipment placement.
3. A two-pass household may use two separate **600 sq ft** polygons, one **1,200 sq ft** polygon, or multiple irregular components totaling **1,200 sq ft**.
4. Show every camper, trailer, tent, canopy, slide-out, stair, awning, guy line, anchor, vehicle, generator, fence, tank, hose, cord, utility system, and major path that affects usable area.
5. Do not count shared roads, required setbacks, intentional gaps, or unapproved outside space toward a household's allocation.
6. Keep required circulation and emergency access, but do not treat general layout efficiency as a design objective.
7. Treat equipment dimensions as unknown until recorded in the household note or another verified equipment file.
8. For S. and S., test using one 600 sq ft polygon primarily for the camper and the second primarily for the shower trailer, while also testing irregular combined arrangements.

## Current confirmation status

### A.

- Sleeping Tent: **10 × 20 ft**.
- Yoga Tent: **10 × 17 ft** COVERPRO canopy.
- Accepted allocation: two independently movable 300 sq ft sections sharing a full 25 ft boundary and forming one 25 × 24 ft outer rectangle; no additional connector area.

### C. and S.

- Main tent: **12 × 16 ft**, nominally **192 sq ft**.
- Add-on room: **8 × 8 ft**, nominally **64 sq ft**; attached at one end, with centered alignment still a planning assumption.
- Canopy: **10 × 13 ft**, nominally **130 sq ft**; product, legs, anchors, ropes, and ballast still require confirmation.

### B. and G.

- Primary tent: **13 × 26 ft**, nominally **338 sq ft**.
- Closet tent: **approximately 10 × 20 ft**, nominally approximately **200 sq ft**; replacement model still TBD.
- Community tent: **20 × 30 ft**, nominally **600 sq ft**; fills the second pass before operational clearances.

### S. and S.

- KZ Connect SE C312BHKSE camper as the working identification; exact year and deployed dimensions still require verification.
- **16 ft flatbed trailer** confirmed for use as a shower facility, with a **full-width fold-down rear ramp**, plus a separate **8 ft trailer carrying an IBC water tote**. Pass B turns the shower trailer sideways, T's the water trailer into it, omits a separate landing zone, and reconnects the notched shower/water section to a 10.2 × 10 ft fire-pit end with a straight 3 × 35 ft connector. All assumed dimensions and fire/utility clearances require measurement and approval.
- Accepted allocation: 393 sq ft shower/water section + 102 sq ft fire-pit section + straight 3 × 35 ft, 105 sq ft connector = **600 sq ft**. The 3 ft connector width is planning-only; all drawn shower/water equipment remains within the notched shower section.

### S. and T.

- Accepted allocation: **20 ft diameter circular yurt piece** (314.1593 sq ft) + 10 × 10 ft portapotty end (100 sq ft) + straight 2 × 50 ft connector (100 sq ft) + unplaced setup reserve (85.8407 sq ft) = **600 sq ft**.
- Yurt: user-reported **20 ft diameter**; exact model, platform, entry, anchor, and total setup envelope remain unverified.
- Handicap Portapotty: **6 × 6 ft** (36 sq ft) ADA-accessible unit assumed inside the opposite end; door direction, turning space, and accessible approach remain unverified. The 2 ft allocation connector is not a confirmed accessible route.

J. and C.'s camper has a separate equipment and site-planning record. M. and E. still need exact structure dimensions, openings, anchoring footprints, vehicles, utilities, and orientation preferences.
