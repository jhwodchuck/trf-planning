# Evidence record — September 5, 2026 review

Last updated: **2026-09-05**

Status: **Sanitized HTTP/content and delivered-code evidence. Not a browser screenshot archive or full security/load audit.**

Live reads below were made through the connected Vercel fetch tool approximately 20:16–20:21 UTC (15:16–15:21 CDT). That tool uses authenticated/share-assisted access. Authentication/share query values, request identifiers, and full response bodies containing those values are intentionally not committed. The evidence supports returned content, not an independent anonymous-access pass.

## Evidence index

| ID | Source | Result / specific observation |
| --- | --- | --- |
| E1 | https://trf-map.vercel.app/ | HTTP 200; TRF Clan Map, Clan list, Submit your clan, Fit markers, Layers; correct canonical and OG text; no og:image; no direct contact or export action in reviewed markup |
| E2 | https://trf-map.vercel.app/clans | HTTP 200; SSR inventory of 38 historical names; card links go to /submit?claim=...; no search input or per-clan view-on-map link; Havok card uses generic needs-confirmation wording |
| E3 | https://trf-map.vercel.app/submit?claim=havok | HTTP 200; form and keyboard/center-point instructions; blank initial SSR fields are not evidence of broken client prefill |
| E4 | https://trf-map.vercel.app/privacy | HTTP 200; private/public data explanation; correction/removal instructions point to whoever shared the map, not a named direct contact |
| E5 | https://trf-map.vercel.app/private-data/clan-areas.geojson | HTTP 200 at 20:20:28 UTC; features=[]; 2026 community-maintained warning and geometry rule |
| E6 | https://trf-map.vercel.app/api/historical-locations | HTTP 200 at 20:20:48 UTC; metadata.count=38; historical-unconfirmed; Havok status=claim-pending; sampled public data contains no contact fields |
| E7 | https://trf-map.vercel.app/site.webmanifest | HTTP 200; standalone display, name/colors/start URL, SVG icon; not an offline test |
| E8 | GitHub main at fcdf1759aab3715229d8cabf9543be664af475ee; root vercel.json, README.md, CLAUDE.md; Vercel project/deployment reads | Root route proxies to original Worker with caching header 0; existing app guidance describes older static planning viewers; live Worker source not located by performed searches |
| E9 | https://trf-map.vercel.app/_next/static/chunks/PrivateCampMap-DUxleltF.js | HTTP 200; delivered map component used for failure-state, bounds, loading-race, and drawer findings |
| E10 | https://trf-map.vercel.app/_next/static/chunks/ClanSubmissionForm-Dln3SYnS.js | HTTP 200; delivered submission component; claim-prefill logic, Add center point, POST path, no client request deadline |
| E11 | https://trf-map.vercel.app/_next/static/css/index.DBEnhecF.css | HTTP 200; mobile <=640px hides header clan-list link and explanatory status span; drawer and fixed-card styling |
| E12 | https://trf-map.vercel.app/_next/static/css/ClanSubmissionForm.7NnR5lpp.css | HTTP 200; responsive map-before-form layout at <=760px, small label/hint rem sizes |

## Version identifiers

Vercel project: trf-map, `prj_gzR4FGSeBAziFTlgDVCRMpGrurAR`.

Wrapper deployment: `dpl_6b4wPTnEF8P1CC6DTPnQvHeXB38y`, READY, production, alias trf-map.vercel.app.

Worker deploymentVersion observed in HTML: `4e3d6a74-029b-44f3-8909-78a68c6ae7cc`. This is a runtime identifier, not a located Git commit.

Delivered map overlay path: `/private-data/official-2026-aligned.png?v=20260905-14-points-10-lines`.

Map tile archive referenced by delivered code: `/private-data/trf-campground-2025-10-20-z13-20.pmtiles`. The archive was not downloaded or range-tested in this review. Its filename does not independently prove capture date or rights.

## Selected observations for reproduction

The root route uses `src: /(?<path>.*)` and `dest: https://trf-private-map.jhwodchuck.workers.dev/$path`, with `x-vercel-enable-rewrite-caching: 0`.

Map code uses null for both pending and failed counts, and chooses Loading clan locations whenever either count is null. The error event changes an aria-hidden status dot. The Fit markers callback uses a constant campground box; load initialization uses literal layer states and .62 opacity.

Submission code fetches historical data for claim-prefill. It tries a fallback after a non-OK HTTP response, but a rejected initial fetch goes directly to the outer catch. The submitted new/claim type is then selected from the loaded nullable claim state. Backend treatment was not inspected.

On sampled HTML, CSP, X-Frame-Options DENY, X-Content-Type-Options nosniff, a strict-origin-when-cross-origin referrer policy, and a permissions policy disabling geolocation were present. These headers alone do not establish application security.

Sampled JS/CSS assets returned immutable one-year Cache-Control and Cloudflare HIT, with Vercel MISS. Public historical API Cache-Control was public, max-age=30. The wrapper's explicit caching opt-out warrants path-specific review; neither transfer volume nor performance was measured.

## Primary technical references

These explain mechanisms; they are not evidence that the site passed a test.

- [Vercel external-origin caching update, March 30, 2026](https://vercel.com/changelog/vercels-cdn-now-respects-cache-control-headers-from-external-origins-by-default): announces new-project default changes from April 6 and documents path-specific opt-out with header value 0. Older rewrite docs describe a previous default; use the dated update and inspect the actual project/config rather than assuming the old default.
- [Vercel rewrite documentation](https://vercel.com/docs/routing/rewrites): proxy and routing configuration reference.
- [Protomaps PMTiles concepts](https://docs.protomaps.com/pmtiles/): browser readers request relevant archive portions using HTTP Range requests.
- [Protomaps cloud storage](https://docs.protomaps.com/pmtiles/cloud-storage): hosting and header considerations.
- [MDN service-worker tutorial](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Tutorials/CycleTracker/Service_workers): distinguishes manifest presentation from implementing offline behavior.

## Tests not performed

No independent anonymous 200 check, real-device rendering, screenshot audit, offline/airplane-mode run, Facebook preview/in-app-browser test, successful submission POST, moderation round trip, authenticated-data permission probe, HTTP Range test, load test, physical location verification, or imagery license audit. Container DNS failure and web-tool retrieval errors were review-environment limitations and are not counted as production incidents.
