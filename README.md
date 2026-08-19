# TRF Planning

Planning documents and site-plan assets for Texas Renaissance Festival camping.

## Planning baseline

- Use **600 sq ft per qualifying pass** for every working layout and group-site calculation.
- Pass allocations may be contiguous, separated, stepped, narrow, or irregular.
- Compactness and land-use efficiency are **not goals**; prefer arrangements that preserve more practical claimed area, even when they create gaps or disconnected boxes.
- Do not maintain a separate 525 sq ft planning version unless this assumption is explicitly changed.
- Final setup must still follow the dimensions and conditions TRF actually approves.

## Group allocation

- [Group pass allocation and household roster](planning/group-pass-allocation.md) — seven households, ten passes, 6,000 sq ft total planning area, shelter types, major support equipment, disconnected-allocation rules, and links to every household record
- [Interactive map + group site map v0.1](maps/viewer/index.html) — aerial overlay with ten 600 sq ft pass polygons, known structures, placeholders, road, and setbacks, merged with the broader GIS viewer (parcels, streets, flood, wetlands, drawing tools)
- [Scale group site map v0.1](maps/overlays/group-site-v0.1.svg) — historical printable reference; use the interactive/georeferenced maps for the accepted reattached arrangement
- [2025 occupied-camp imagery reference](planning/2025-camp-layout-reference.md) and [Google Earth KML overlay](maps/overlays/group-site-v0.1.kml) — compare the dated 2025-10-20 camp scene with the 2026 candidate polygons without rehosting Google's imagery
- [Pass layout tool](maps/viewer/pass-layout.html) — drag, rotate, and rearrange the ten pass sections, three detached amenity sections, and two accepted walkway connectors ([`maps/overlays/passes/`](maps/overlays/passes/)) on a freeform canvas
- [Group site map assumptions](planning/group-site-map-v0.1.md) — status, known dimensions, strategy, and limitations

## Current concept

- Working location: immediately north/northeast of Havok camp beside the adjacent access road; exact boundary still required.
- User-supplied site reference: `30.255805, -95.846180`.
- Camper nose/hitch south; entry door west, away from the road.
- Road-side living/bedroom slides east.
- 15 × 10 ft working canopy template on the west/southwest side; dimensions must be verified.
- Two Cummins Onan P4500i generators with temporary visual screening that must not form an enclosure.
- Current stepped footprint template: about 598.9 sq ft, subject to TRF approval and field verification.

## Planning records

### Maps and geometry

- [TRF site-planning map pack](maps/README.md) — official campground reference, interactive aerial/topographic/GIS viewer, source catalog, GeoJSON area, and automated static-map builder
- [Interactive map viewer](maps/viewer/index.html) — aerial imagery, USGS topography, parcels, streets, FEMA flood zones, wetlands, drawing, measurement, GeoJSON import/export, and the group site map v0.1 overlay
- [Pass layout tool](maps/viewer/pass-layout.html) and [per-pass SVGs](maps/overlays/passes/) — each 600 sq ft pass as its own editable drawing, freely draggable and rotatable on a freeform master canvas
- [Road control and setback geometry](planning/site-control-road-setback.md) — supplied road points, true bearing, 10 ft and 14 ft parallel offsets, and the current corner-label conflict
- [Road and setback GeoJSON](maps/data/site-control-road-setbacks.geojson) — map-ready supplied points, road alignment, perpendicular measurement, and derived setback lines
- [2025 occupied-camp imagery reference](planning/2025-camp-layout-reference.md) — dated Google Earth evidence, observed clearing/road constraints, anchor offset, and 2026 planning consequences
- [Google Earth KML overlay](maps/overlays/group-site-v0.1.kml) — the current project-owned GeoJSON plan converted for local comparison against the dated imagery
- [Dimensioned campsite footprint](maps/overlays/requested-campsite-footprint.svg) — scale-controlled RV and 10 × 15 ft canopy working template
- [Known and missing site data](planning/known-and-missing-data.md) — assumptions, dimensional conflicts, and final-plan gates
- [Field site survey checklist](planning/site-survey-checklist.md) — boundary, terrain, access, camper, generator, and photo measurements

### Group and household units

- [Household roster and allocations](planning/group-pass-allocation.md) — authoritative pass count, 600 sq ft-per-pass totals, major equipment, and non-contiguous planning rules
- [C. and S.](planning/households/cs.md) — exact 600 sq ft T-shaped pass with reported approximately 20 × 20 ft tent-plus-add-on and 10 × 13 ft canopy
- [B. and G.](planning/households/bg.md) — primary and closet tents in an offset pass with two generic generator placeholders between them; models, dimensions, and operation remain unresolved; 20 × 30 ft community tent in the second pass
- [A.](planning/a-site-notes.md) — confirmed 10 × 20 ft sleeping tent and 10 × 17 ft Yoga Tent, one pass, 600 sq ft
- [M. and E.](planning/households/me.md) — camper, two passes, 1,200 sq ft; temporary mirrored camper-pass placeholder pending actual geometry
- [S. and S.](planning/households/ss.md) — KZ Connect SE C312BHKSE camper working reference plus 16 ft flatbed shower trailer, two passes, 1,200 sq ft
- [J. and C.](planning/households/jc.md) — camper, one pass, 600 sq ft
- [S. and T.](planning/households/st.md) — 20 ft diameter yurt and handicap portapotty, one pass, 600 sq ft

### Rules and submission

- [Authoritative source index](docs/source-index.md) — TRF, manufacturer, and government references
- [TRF Website Local Corpus](docs/trf-corpus/README.md) — complete local Markdown mirror and index of texrenfest.com
- [2026 TRF requirements](docs/trf-2026-requirements.md) — dates, land-request package, official-source conflicts, rules, and questions for TRF
- [TRF Order #6034 record](docs/order-6034.md) — sanitized Diamond and Ruby season-pass purchase, completion requirements, and Camping Will Call record
- [Submission checklist](docs/submission-checklist.md) — readiness checklist for approval drawings and field setup

### Equipment

- [Cummins Onan P4500i generator inventory](equipment/cummins-onan-p4500i.md) — two generators, electrical capability, operating footprint, CO/fire constraints, and readiness checklist
- [Anker SOLIX S2000 power station inventory](equipment/anker-solix-s2000.md) — battery specifications, charging limits, and camper-use planning
- [2012 Wildcat dimensional baseline](equipment/2012-wildcat-dimensional-baseline.md) — floor plan, requested rotation, model conflict, and measurements needed
- [S. and S. camper floor plan](equipment/ss-kz-connect-se-c312bhkse.md) — KZ Connect SE C312BHKSE working identification, manufacturer floor plan, published dimensions, and measurements needed for site placement
- [S. and S. shower trailer](equipment/ss-16ft-shower-trailer.md) — sideways shower trailer, perpendicular 8 ft IBC trailer, and a straight 3 × 35 ft connector to a provisional fire-pit end; dimensions and clearances pending
- [2018 Ford F-250 long-bed baseline](equipment/2018-ford-f250-long-bed.md) — cab-specific lengths and maneuvering inputs

## Critical blockers

1. Final interpretation of the supplied boundary reference, plus field verification of the physical road edge and curvature.
2. Camper model/data-plate verification and deployed field measurements.
3. Exact canopy and screening dimensions/anchoring approval.
4. A generator operating location that satisfies manual and CO/fire safety guidance.
5. Shower-trailer width, overall length, enclosure, water, greywater, utility, privacy, and access measurements.
6. Remaining unknown tent, canopy, camper, and household adjacency details.

Do not label a layout final until those blockers and the applicable TRF approval conditions are resolved.
