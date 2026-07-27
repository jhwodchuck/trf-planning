# TRF Site-Planning Map Pack

This folder is the map workspace for planning a campsite in the Texas Renaissance Festival Fields of New Market campground.

## Start here

1. Open `viewer/index.html` in a web browser for an interactive map with aerial imagery, USGS topography, parcels, streets, FEMA flood data, and wetlands.
2. Review `reference/official/2026-season-pass-plotting-map.html` for the official season-pass camping, parking, and restricted-area planning context.
3. Review `reference/official/2026-campground-map.html` for roads, numbered campground areas, gates, services, and emergency exits.
4. Use `overlays/requested-campsite-footprint.svg` as the dimensioned, scale-controlled footprint template for the RV and 10 × 15 ft canopy.
5. Review the static files in `generated/` after the map-build workflow runs.

## Current map inventory

| Map or layer | Primary planning use | Status |
|---|---|---|
| Official 2026 Season Pass Plotting Map v3.2 | Broad season-pass camping, parking, and restricted-area context | Live official reference |
| Official 2026 campground map | Camp roads, numbered camping areas, gates, emergency exits, water, showers, cabins, first aid, restrooms, and landmarks | Live official reference |
| NAIP aerial imagery | Trees, clearings, roads, drainage traces, and current ground context | In viewer and generated map |
| USGS topographic map | Terrain, hydrography, roads, and elevation context | In viewer and generated map |
| USGS shaded relief | Slope and drainage pattern reconnaissance | Generated map |
| Grimes CAD parcels | Parcel boundaries and public-road context | In viewer and downloaded as GeoJSON |
| FEMA NFHL | Flood-hazard screening | In viewer and generated map |
| USFWS wetlands | Wetland and low-area screening | In viewer and generated map |
| USDA NRCS SSURGO / Web Soil Survey | Soil drainage, ponding, flooding frequency, and engineering limitations | Source registered; AOI report still needed |
| Exact campsite survey/control points | Final placement, setbacks, and defensible dimensions | Missing; requires field measurements or surveyed coordinates |
| Utility locations | Safe placement of stakes, ballast, generators, and temporary infrastructure | Missing; verify with TRF and field locate before work |

## Known requested-site reference

The working location description from the prior land-request packet is **immediately north/northeast of the Havok camp, beside the adjacent access road**. That description is useful for orientation, but it is not a coordinate, surveyed boundary, or proof of approval.

The Forest River data plate confirms the camper as model code **`WCP29MK` (29MK, not 293MK)**. The current requested footprint template still uses unverified planning dimensions:

- Fifth-wheel body: 31 ft 6 in long × 8 ft 4 in wide.
- Approximate deployed RV zone: 31 ft 6 in × 14 ft 3 in.
- Canopy: 15 ft × 10 ft on the west side, away from the adjacent road.
- Stepped requested area: about 598.9 sq ft.

The model identification is verified, but the body, hitch, slide, stair, awning, and stabilizer dimensions remain field-measurement inputs. Published Sterling 29MK references commonly list about 31 ft 7 in × 8 ft, so the current template must not be treated as final.

No phone numbers, email addresses, order numbers, full VINs, unit serial numbers, or signed application documents are stored in this public repository.

## Accuracy rules

- Treat both official TRF graphics as planning/orientation maps, not scale drawings.
- Treat aerial, parcel, flood, wetland, soil, and topo layers as planning-grade screening data.
- Do not infer an exact campsite boundary from imagery alone.
- Keep all physical boundaries and structures at least 10 ft from roadways unless TRF provides a different written site-specific direction.
- Confirm the final site, roadway edge, tree trunks, drainage, utilities, and usable ground in the field before finalizing the layout.

## Automated map build

The workflow in `.github/workflows/build-maps.yml` runs `scripts/build_map_pack.py`. It downloads the current public GIS layers for the configured area of interest, creates static PNG map sheets, saves selected vector layers as GeoJSON, and writes a build report. Generated outputs are committed back to `maps/generated/` and `maps/data/` when repository permissions allow it.

The initial area of interest is deliberately broad and approximate. Update `AOI_BBOX` in `scripts/build_map_pack.py` after the exact Havok-area location is identified on aerial imagery or measured in the field.
