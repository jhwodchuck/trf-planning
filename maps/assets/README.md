# Static viewer assets

`pass-layout-aerial-naip-2022-context-v2.jpg` is the offline backdrop for
`viewer/pass-layout.html`.

- Source: Texas Geographic Information Office / USDA NAIP 2022
- Service: `NAIP/NAIP22_NCCIR_60cm`
- Bounding box (WGS84): `-95.84753348955002,30.255112027019997,-95.84527380905,30.25639971322`
- Local-coordinate extent: `x -250..450 ft`, `y -100..350 ft`
- ArcGIS export and committed display size: `1400 × 900`
- Format: JPEG
- Retrieved: 2026-07-27
- Display registration: affine-warped in `viewer/pass-layout.html` using the
  same local-foot/WGS84 transform as the road geometry
- Status: planning context only; not survey-grade

The source imagery is 60 cm per pixel. The wider roughly 700 × 450 ft extent
lets the pass-layout tool reveal surrounding roads, clearings, and trees when
the user zooms out. The 230 × 200 ft planning coordinate area is positioned
inside this larger context image; pass coordinates and saved layouts remain
unchanged. The source file remains an axis-aligned WGS84 export; the viewer
applies the inverse affine transform to correct rotation and skew. No resize can
create additional site detail.
