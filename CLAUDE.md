# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A **planning-document repository**, not an application. It holds the site plan for a group campsite at the Texas Renaissance Festival (Fields of New Market campground, Grimes County, TX): Markdown planning records, GeoJSON site geometry, SVG scale drawings, static Leaflet viewers, and Python scripts that pull public GIS layers into static map sheets.

There is no package manager, test suite, linter, or build system beyond the map scripts. Most "work" here is editing Markdown and hand-authored geometry, and keeping the cross-links between them consistent.

## Commands

Map builders (Python 3.12, deps in `requirements-map.txt`):

```bash
python -m pip install -r requirements-map.txt
```

```bash
python scripts/build_map_pack.py
```

`build_hazard_maps.py` (FEMA flood + USFWS wetlands), `build_elevation_maps.py` (USGS 3DEP), and `build_soil_map.py` (NRCS SSURGO) run the same way and are independent. All four write PNG sheets to `maps/generated/` and a `*build-report.json`; `build_map_pack.py` also refreshes `maps/data/grimes-*.geojson`.

Every script is failure-tolerant by design: a dead ArcGIS service produces a labeled placeholder sheet and a `warn` entry in the build report, and the script still exits 0. **Check the build report, not the exit code**, to know whether a source actually downloaded.

The viewers `fetch()` sibling GeoJSON, so `file://` will not work. Serve the repo:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000/maps/viewer/index.html` (or `provisional-site.html`, `pass-layout.html`, or `maps/all-maps.html`, the map-pack hub page). `index.html` is the merged viewer — parcels/streets/flood/wetlands/drawing tools plus the "Group site v0.1" pass-polygon overlay (there is no separate `group-site-v0.1.html` anymore). Leaflet, esri-leaflet, and all basemaps load from CDNs and live services — the georeferenced viewers require network access. `pass-layout.html` fetches its own aerial backdrop (Texas NAIP 2022, 60 cm/px) from a live ArcGIS ImageServer, so it also needs network access despite having no CDN script dependencies.

Per-pass SVGs and their manifest (no network, no CDN deps):

```bash
python scripts/build_pass_svgs.py
```

On Windows, always pass `encoding="utf-8"` when reading these files from Python; the repo's Markdown and GeoJSON contain em dashes and `×`, and Python's default cp1252 will mojibake them.

## Content model and authority order

Facts flow in one direction; do not let a downstream artifact become the source of truth.

1. **Official TRF sources** — catalogued in [docs/source-index.md](docs/source-index.md), extracted into [docs/trf-2026-requirements.md](docs/trf-2026-requirements.md), with official map copies under `maps/reference/official/` (referenced from the TRF host, never re-hosted).
2. **Planning conventions and household facts** — [planning/group-pass-allocation.md](planning/group-pass-allocation.md) is the authoritative roster (7 households, 10 passes); each household has a record in `planning/households/`, plus [planning/amanda-site-notes.md](planning/amanda-site-notes.md).
3. **Equipment dimensions** — `equipment/*.md`, one file per camper, trailer, generator, or vehicle.
4. **Site control geometry** — [planning/site-control-road-setback.md](planning/site-control-road-setback.md) derives the road bearing and the 10 ft / 14 ft setbacks from three user-supplied coordinates; the numbers there feed `maps/data/*.geojson`.
5. **Drawn artifacts** — `maps/data/*.geojson` (georeferenced), `maps/overlays/*.svg` (scale drawings), `maps/viewer/*.html` (interactive).
6. **Decomposed/freeform artifacts** — `maps/overlays/passes/*.svg` + `passes-manifest.json`, generated from `scripts/build_pass_svgs.py`, and composed interactively in `maps/viewer/pass-layout.html`. This branch is intentionally **not georeferenced** — it exists to test arrangement and adjacency, not to replace the geometry in (5). Edit the `PASSES` data in the script, not the generated files, then rerun it.

When a dimension changes, it must be updated in the household/equipment record **and** in every drawn artifact that already used it, plus the summary tables in `README.md` and `planning/group-site-map-v0.1.md`. Recent commit history is almost entirely this kind of propagation.

## Non-negotiable planning rules

These are project decisions, not preferences. They are restated in `README.md`, the requirements doc, and the roster because tools and drawings keep drifting away from them:

- **600 sq ft per qualifying pass** for every layout and calculation. The official sources conflict (600 vs. 525 sq ft); the conflict is documented, but do **not** produce a parallel 525 sq ft design unless the user explicitly changes the baseline.
- **Compactness is not a goal.** Disconnected, stepped, narrow, or irregular pass polygons are preferred when they claim more usable ground. Never shrink a requested area to close a gap or make a drawing look tidy.
- **Confirmed vs. placeholder is load-bearing.** A dimension is unknown until it appears in a household or equipment record with a source. Draw unknowns as dashed placeholders labeled `DIMENSIONS REQUIRED`; never invent a plausible default (e.g. assuming a canopy is 10 × 10).
- **Nothing is final.** No layout may be labeled final while the blockers listed at the end of `README.md` are open. Everything here is planning-grade, not survey-grade — say so in generated artifacts.
- **This repository is public.** No phone numbers, personal email addresses, order numbers, signatures, or unredacted submission documents. The 2025 submission PDFs referenced by [docs/prior-submissions/README.md](docs/prior-submissions/README.md) are intentionally absent.
- Drawings intended for review must carry the eight elements listed under "Drawing rules" in [docs/project-overview.md](docs/project-overview.md) (date/revision, north arrow, scale bar, dimensions, setbacks, every projection, verified-vs-estimated distinction).

## Conventions

**Markdown records** open with a title, then `Last updated: **YYYY-MM-DD**` (or `Checked:`/`Status:`), then tables with an explicit `Status` and `Source` column, and usually close with an "Information still needed" list and per-file drawing rules. Follow that shape for new records, and update the date when editing.

**GeoJSON** in `maps/data/` is hand-authored planning geometry (except `grimes-*.geojson`, which the workflow overwrites). Each `FeatureCollection` carries a top-level `properties` block with `created_on`, `status`, and a `warning`; each feature has `id`, `name`, and a `role`. `role` is the styling key — `pass`, `rv`, `canopy`, `tent`, `tent_estimate`, `road_edge`, `setback_10`, `setback_14`, `trailer_length`, `*_placeholder`. Optional: `area_sqft`, `dimensions_ft`, `length_ft`, `width_ft`, `status`, `note`, `placement`. **Adding a new role means updating `styleFeature`/`st` in the corresponding viewer HTML and the CSS classes in the matching SVG**, or the feature silently renders with the fallback style.

**Viewers** are single self-contained HTML files (inline CSS/JS, CDN Leaflet, no build step) with a left sidebar carrying the same warnings, metrics, and legend as the Markdown record. Household colors are keyed by feature `id` in `householdColors`.

**AOI bounding box** `(-95.865, 30.243, -95.823, 30.286)` is duplicated as a constant in all four scripts and in `maps/data/map-sources.json`. Change all five together. It is deliberately broad until the campsite anchor is field-verified.

**`maps/data/map-sources.json`** is the catalogue of every external GIS service with its `use` and `limitations`. Add an entry there before wiring a new service into a script.

## Deployment

`maps/` is deployed as a static site to **https://trf-planning.vercel.app/** (Vercel project `trf-planning`, root directory `maps/`, no build step/framework, linked locally via `vercel link` inside `maps/`). `maps/vercel.json` rewrites `/` to `viewer/index.html` (the merged general/group-site viewer); every other path mirrors the folder layout (`viewer/pass-layout.html`, `data/*.geojson`, `overlays/passes/*.svg`, etc.), so the viewers' relative `fetch()` calls work unmodified in production. Nothing outside `maps/` is deployed.

**Vercel serves a matching static file before it ever checks `rewrites`.** That's why the map-pack hub page is `maps/all-maps.html`, not `maps/index.html` — a real `index.html` at that path would shadow the `/` rewrite and silently take over the production root. If you ever need another file literally named `index.html` directly in `maps/`, expect the same collision and rename it instead of fighting the rewrite.

**There is no CI/CD wired to this.** Vercel does not auto-deploy on push — someone must trigger a deployment (`cd maps && vercel deploy --prod --yes`, the dashboard, or the `deploy_to_vercel`/`get_project`/`list_projects` MCP tools — but note `deploy_to_vercel` takes inline file content per call, which is impractical once `maps/data/grimes-*.geojson` (~2.5 MB) or `maps/generated/*.png` are involved; the CLI has no such limit) after merging changes under `maps/`, or the live site drifts from the repo. It has drifted before: a prior production deploy was a single hand-patched copy of `group-site-v0.1.html` (fetching its geojson from a hardcoded `raw.githubusercontent.com/.../main/...` URL instead of the relative path) uploaded on its own, with every other path 404ing. If `https://trf-planning.vercel.app/data/...` or `/viewer/...` ever 404 while `/` works, that ad hoc single-file state is back — redeploy the full `maps/` tree to fix it, and do not reintroduce the GitHub-raw fetch hack.

## Repository layout gotchas

- `data/` and `templates/` are an **earlier version** of `planning/` and `equipment/` (camper, generator, vehicle, site data, survey checklist). Only `docs/project-overview.md` still links to them. `planning/` and `equipment/` are current — prefer them, and treat the `data/` copies as stale unless asked to reconcile the two trees.
- `maps/generated/` and `maps/generated/README.md` are workflow-owned. Don't hand-edit the PNGs or reports. The README there also lists sheets `05`–`11` that the current scripts produce but that are not all committed yet.
- Two GitHub Actions workflows (`build-maps.yml`, `build-soil-map.yml`) run on `workflow_dispatch` and on pushes touching the scripts, `requirements-map.txt`, or `map-sources.json`, then commit refreshed outputs back to `main` with `[skip ci]`. Expect bot commits after touching those paths.
