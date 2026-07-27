# Generated planning maps

This directory is populated by `.github/workflows/build-maps.yml`.

Generated outputs:

- `01-aerial-parcels.png` — NAIP aerial imagery with Grimes CAD parcel outlines.
- `02-usgs-topographic.png` — USGS topographic map sheet.
- `03-usgs-imagery-topo.png` — USGS imagery with topographic labels.
- `04-usgs-shaded-relief.png` — terrain-relief reconnaissance sheet.
- `05-fema-flood-hazard.png` — NAIP aerial imagery with FEMA NFHL flood-hazard zones.
- `06-usfws-wetlands.png` — NAIP aerial imagery with USFWS National Wetlands Inventory data.
- `07-flood-wetlands-composite.png` — combined flood/wetland screening sheet using whichever live layers were available.
- `08-3dep-tinted-hillshade.png` — USGS 3DEP bare-earth tinted hillshade.
- `09-3dep-slope.png` — USGS 3DEP slope visualization.
- `10-3dep-2ft-contours.png` — USGS 3DEP two-foot contour visualization.
- `11-3dep-5ft-contours.png` — USGS 3DEP five-foot contour visualization.
- `05-flood-wetlands.png` — backward-compatible copy of the combined hazard sheet.
- `build-report.json` — timestamp, area of interest, source status, hazard-source status, elevation-source status, and any download failures.

These are planning aids, not survey products, flood guarantees, or jurisdictional wetland determinations. The configured area of interest is broad until the exact Havok-area campsite location is pinned down.
