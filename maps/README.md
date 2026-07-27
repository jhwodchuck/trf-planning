# TRF Site-Planning Map Pack

This folder is the map workspace for planning a campsite in the Texas Renaissance Festival Fields of New Market campground.

This folder is deployed as-is to **https://trf-planning.vercel.app/** (Vercel project `trf-planning`, root directory `maps/`, static — no build step). `vercel.json` in this folder rewrites `/` to `viewer/group-site-v0.1.html` so the live root matches this folder's `index.html` nav landing point; every other path mirrors the file layout below (`viewer/pass-layout.html`, `data/*.geojson`, etc.). Redeploy after changing anything under `maps/` — Vercel does not watch this repo automatically.

## Start here

1. Open `viewer/provisional-site.html` for the current site-specific aerial overlay with the proposed boundary, RV zone, canopy, road reference, and 10- and 14-foot setback lines.
2. Open `overlays/provisional-site-on-aerial.svg` for a static aerial-overlay view.
3. Open `viewer/index.html` for the broader interactive map with aerial imagery, USGS topography, parcels, streets, FEMA flood data, and wetlands.
4. Review `reference/official/2026-season-pass-plotting-map.html` for the official season-pass camping, parking, and restricted-area planning context.
5. Review `reference/official/2026-campground-map.html` for roads, numbered campground areas, gates, services, and emergency exits.
6. Use `overlays/requested-campsite-footprint.svg` as the original dimensioned, scale-controlled RV and canopy footprint template.
7. Review the static files in `generated/` after the map-build workflow runs.
8. Open `viewer/pass-layout.html` to drag, rotate, and rearrange the ten individual 600 sq ft pass drawings in `overlays/passes/` on a freeform (non-georeferenced) canvas.

## Current map inventory

| Map or layer | Primary planning use | Status |
|---|---|---|
| Provisional site-specific aerial overlay | Shows the current 598.9 sq ft stepped boundary, RV zone, canopy, road line, and setbacks at the supplied coordinates | Added; field verification required |
| Per-pass SVGs and drag-layout tool | Ten standalone 600 sq ft pass drawings (`overlays/passes/`) that can be independently refined and freely repositioned on `viewer/pass-layout.html` | Added; freeform, not georeferenced |
| Official 2026 Season Pass Plotting Map v3.2 | Broad season-pass camping, parking, and restricted-area context | Live official reference |
| Official 2026 campground map | Camp roads, numbered campground areas, gates, emergency exits, water, showers, cabins, first aid, restrooms, and landmarks | Live official reference |
| NAIP aerial imagery | Trees, clearings, roads, drainage traces, and current ground context | In viewers and generated maps |
| USGS topographic map | Terrain, hydrography, roads, and elevation context | In viewer and generated map |
| USGS shaded relief | Slope and drainage pattern reconnaissance | Generated map |
| Grimes CAD parcels | Parcel boundaries and public-road context | In viewer and downloaded as GeoJSON |
| FEMA NFHL | Flood-hazard screening | In viewer and generated map |
| USFWS wetlands | Wetland and low-area screening | In viewer and generated map |
| USDA NRCS SSURGO / Web Soil Survey | Soil drainage, ponding, flooding frequency, and engineering limitations | Source registered; AOI report still needed |
| Site control and road references | Geographic placement and parallel setback construction | Three user-supplied points recorded; field verification and more control points still needed |
| Utility locations | Safe placement of stakes, ballast, generators, and temporary infrastructure | Missing; verify with TRF and field locate before work |

## Current site control

All coordinates below are user-supplied WGS84 decimal-degree planning references.

- Supplied site point: `30.255805, -95.846180`
- Northern road point: `30.255863424245597, -95.84612334146146`
- Southern road point: `30.255803765364604, -95.84612535311821`
- Campsite side: west of the road
- Derived road bearing: approximately `1.68°` east of true north
- Supplied point to straight road reference: approximately `17.27 ft`
- Margin beyond the preferred 14-foot setback: approximately `3.27 ft`

The working overlay uses the supplied site point as the **road-side southeast/southern anchor**, with the footprint extending north and west. A literal southwest-corner interpretation would leave only about 3.27 feet between that point and the preferred setback line and would not create a practical campsite.

The corresponding vector geometry is stored in:

- `data/provisional-site-footprint.geojson`
- `data/site-control-road-setbacks.geojson`

The observed road sample is only about 21.7 feet long. Confirm whether the road curves over the full site length and confirm that both road points represent the physical road edge nearest the campsite rather than its centerline.

## Current working footprint

The current site-specific overlay uses:

- Approximate deployed RV zone: 31 ft 6 in long x 14 ft 3 in wide.
- Canopy: 15 ft east-west x 10 ft north-south on the west/southwest side.
- Camper long axis approximately parallel to the road.
- Camper hitch/front toward the south.
- Door facing west, away from the road.
- Stepped requested area: about 598.9 sq ft.

No phone numbers, email addresses, order numbers, or signed application documents are stored in this public repository.

## Accuracy rules

- Treat both official TRF graphics as planning/orientation maps, not scale drawings.
- Treat aerial, parcel, flood, wetland, soil, and topo layers as planning-grade screening data.
- Treat the supplied coordinates as planning control until checked on the ground.
- Do not infer an exact campsite boundary from imagery alone.
- Keep all physical boundaries and structures at least 10 ft from roadways unless TRF provides a different written site-specific direction.
- Use 14 ft as the preferred planning offset where the measured ground allows it.
- Confirm the final site, roadway edge, tree trunks, drainage, utilities, and usable ground in the field before finalizing the layout.

## Automated map build

The workflow in `.github/workflows/build-maps.yml` runs `scripts/build_map_pack.py`. It downloads the current public GIS layers for the configured area of interest, creates static PNG map sheets, saves selected vector layers as GeoJSON, and writes a build report. Generated outputs are committed back to `maps/generated/` and `maps/data/` when repository permissions allow it.

The broad map-builder area of interest should eventually be tightened around the site-specific control geometry after the road edge and boundary are verified in the field.
