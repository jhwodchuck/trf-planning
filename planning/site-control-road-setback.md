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

## Hard western limit

No pass polygon or equipment footprint may extend west of the line through:

| End | Latitude | Longitude |
|---|---:|---:|
| North | 30°15'20.86"N | 95°50'47.36"W |
| South | 30°15'19.63"N | 95°50'47.44"W |

For constraint checks, the alignment is extrapolated across the full planning canvas. The pass-layout viewer draws it in cyan and automatically moves any dragged, rotated, saved, or imported pass back to the east side.

## Derived road alignment

- Distance between `ROAD_B` and `ROAD_A`: approximately **21.707 ft**.
- True bearing from `ROAD_B` northward to `ROAD_A`: **1.676721 degrees**.
- Equivalent southbound bearing: **181.676721 degrees**.
- Perpendicular direction into the campsite, toward the west: **271.676721 degrees**.

That bearing describes only the short segment between the two supplied controls. It remains useful as measured control, but it is no longer extrapolated as the displayed full road edge.

## User-traced curved road edge

The planning map and pass-layout viewer now use a 25-point WGS84 curve supplied by the user on 2026-07-27 while tracing the campsite-side road edge in the current Google Maps satellite view. This coordinate trace replaces the earlier NAIP/Google Earth visual estimate.

In local viewer feet, the supplied trace begins near `(-36.596, 279.114)` on the southwest road segment, follows the bend east to a maximum local x of about `213.243`, and then turns north to `(113.140, -27.901)` past HAVOK. The earlier incorrect southeast continuation to local `(450, 350)` has been removed.

The coordinates are retained exactly for the road edge in both GeoJSON files. The viewer uses their affine-converted local-foot values. The curved 10-foot and 14-foot lines are approximate campsite-side perpendicular offsets computed from averaged local segment normals. They are suitable for arranging passes on the image, but they are not surveyed boundaries. The original straight observed segment, straight extrapolation, and straight-offset calculations remain in `maps/data/site-control-road-setbacks.geojson` as an audit record.

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

These are the original 120-foot straight planning segments extrapolated from the two supplied road points. They are retained for comparison; the displayed site plan now uses the imagery-traced curve and its curved offsets.

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
- `maps/data/group-site-v0.1.geojson`
- `maps/viewer/pass-layout.html`

## Field verification

Before final placement:

1. Confirm both road coordinates lie on the road edge nearest the campsite, not the centerline.
2. Measure at least two longer-spaced points along the same edge if possible.
3. Check the 25-point coordinate trace against the physical road edge over the full proposed site.
4. Mark the 10-foot and preferred 14-foot offsets with a tape measured perpendicular to the physical road edge.
5. Recheck every boundary vertex after the 600 sq ft polygon is laid out.
