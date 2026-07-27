# Site control and road setback geometry

Checked: 2026-07-27

This record converts the user-supplied campsite and road coordinates into planning-grade control geometry. It is not a boundary survey or a substitute for measuring the physical road edge in the field.

## Supplied coordinates

All coordinates are assumed to be WGS84 decimal degrees.

| ID | Description | Latitude | Longitude |
|---|---|---:|---:|
| `P1_USER_SW` | User-described southwest boundary reference | 30.255805000 | -95.846180000 |
| `ROAD_A` | Northern road reference point | 30.255863424 | -95.846123341 |
| `ROAD_B` | Southern road reference point | 30.255803765 | -95.846125353 |

The campsite is on the west side of the road.

## Derived road alignment

- Distance between `ROAD_B` and `ROAD_A`: approximately **21.707 ft**.
- True bearing from `ROAD_B` northward to `ROAD_A`: **1.676721 degrees**.
- Equivalent southbound bearing: **181.676721 degrees**.
- Perpendicular direction into the campsite, toward the west: **271.676721 degrees**.

The road and road-facing campsite edges should therefore be drawn nearly north-south, rotated about **1.68 degrees east of true north**.

## Parallel setback lines

The derived lines are west of the straight road reference line.

### Minimum 10-foot setback

| End | Latitude | Longitude |
|---|---:|---:|
| South | 30.255669500 | -95.846161565 |
| North | 30.255999298 | -95.846150445 |

### Preferred 14-foot setback

| End | Latitude | Longitude |
|---|---:|---:|
| South | 30.255669822 | -95.846174229 |
| North | 30.255999620 | -95.846163108 |

These are 120-foot planning segments extrapolated from the two supplied road points. The observed road segment itself is only about 21.7 feet long, so the road must be checked for curvature before relying on the extrapolated portions.

## Relationship of the supplied boundary reference to the road

The perpendicular distance from `P1_USER_SW` to the straight road reference line is approximately **17.269 ft west**.

That point is therefore:

- **7.269 ft beyond** the minimum 10-foot line; and
- **3.269 ft beyond** the preferred 14-foot line.

This result assumes the road coordinates represent the physical road edge nearest the campsite. If they represent the road centerline, the setback must instead be measured from the west edge of the traveled road.

## Corner-label conflict to resolve before drawing the 600 sq ft boundary

If `P1_USER_SW` is literally the southwest corner, a conventional boundary aligned with the road would extend north and east from it. Only about **3.269 ft** remains between that point and the preferred 14-foot line. A 600 sq ft rectangle using that width would need to be approximately **183.54 ft long**, which is not a practical campsite shape.

Even using only the 10-foot minimum, the available width would be about **7.269 ft**, requiring approximately **82.54 ft of length** for 600 sq ft.

The supplied point works much better as the **southeast, road-side south corner** of the requested boundary, with the 600 sq ft polygon extending north and west. Under that interpretation, the entire boundary can remain at least 17.269 ft from the straight road line at the south corner.

No final 600 sq ft polygon is established in this record. The final shape should be a measured stepped polygon sized around the deployed camper, canopy, stairs, generator area, screening, and required access rather than an arbitrary rectangle.

## Repository geometry

The corresponding points and derived lines are stored in:

- `maps/data/site-control-road-setbacks.geojson`

## Field verification

Before final placement:

1. Confirm both road coordinates lie on the road edge nearest the campsite, not the centerline.
2. Measure at least two longer-spaced points along the same edge if possible.
3. Check whether the road curves over the full length of the proposed site.
4. Mark the 10-foot and preferred 14-foot offsets with a tape measured perpendicular to the physical road edge.
5. Recheck every boundary vertex after the 600 sq ft polygon is laid out.
