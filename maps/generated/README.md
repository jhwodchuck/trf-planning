# Generated planning maps

This directory is populated by `.github/workflows/build-maps.yml`.

Expected outputs:

- `01-aerial-parcels.png` — NAIP aerial imagery with Grimes CAD parcel outlines.
- `02-usgs-topographic.png` — USGS topographic map sheet.
- `03-usgs-imagery-topo.png` — USGS imagery with topographic labels.
- `04-usgs-shaded-relief.png` — terrain-relief reconnaissance sheet.
- `05-flood-wetlands.png` — aerial imagery with FEMA flood-hazard and USFWS wetland overlays.
- `build-report.json` — timestamp, area of interest, source status, and any download failures.

These are planning aids, not survey products. The configured area of interest is broad until the exact Havok-area campsite location is pinned down.
