# TRF Clan Map — actionable agent backlog

Last updated: **2026-09-05**

Status: **All tasks open. Documentation only; none are represented as fixed.**

Use the [review](site-review.md) for scope and [evidence](evidence.md) for exact observed assets. Component names below come from delivered bundles; their original repository paths are unknown. Do not edit minified production bundles or guess a Next.js source path. Locate source first. Reproduce against the current build because another agent may have changed it.

## MAP-001 — identify source and reproducible deployment

**P1 · Handoff gap · E8.** The root vercel.json describes the proxy, but CLAUDE.md documents a different static planning site. GitHub searches did not locate PrivateCampMap source; that is not proof no source exists elsewhere.

Locate the actual Worker app repository, branch, source commit, build commands, deployment configuration, and public-data publication path. Document the distinction between trf-map and trf-planning, the Vercel wrapper, and upstream Worker. Do not replace the older planning viewers.

**Done when:** an agent can build the matching app in an isolated checkout, identify the responsible source files for this backlog, run its tests, deploy a preview, and use a documented rollback procedure. Keep secret values out of docs. Cross-link this handoff from the actual app's agent instructions. Preserve existing planning guidance.

## MAP-002 — usable loading, failure, and no-WebGL states

**P1 · Code-derived defect · E9.** Location-fetch catch handlers reset counts to null, the same value used for loading. Map error events only change a status-dot class; the dot is aria-hidden. The map constructor is not locally guarded.

**Reproduce:** on a preview, block clan-areas.geojson; separately block both historical sources; disable WebGL; simulate a request that never completes. Check the visible and announced status, not just HTTP status.

**Expected:** distinguish loading, partial data, error, and ready. Show Retry and a usable clan-list/saved-map alternative. Preserve already usable data.

**Done when:** failures leave loading within a documented timeout; a readable error is announced without reliance on color; retry recovers without duplicate listeners; no-WebGL still permits finding contact/list information; automated tests cover all three data failure cases and map initialization failure.

## MAP-003 — direct Jason contact and removal route

**P1 · Content/UX gap · E1–E4.** Privacy currently sends users to the person/channel that shared the map and asks for a confirmation ID. No direct named contact is present in reviewed screens.

Add a persistent Report a problem / Contact Jason action and an explicit correction/removal path to map, list, form, privacy, and future exports. Obtain Jason's approved public Facebook/profile/contact destination; do not infer it from his GitHub handle. A historic listing must be reportable without a submission ID, new polygon, or account.

**Done when:** a new visitor can find the contact route from mobile home and privacy; an exact URL is owner-verified; a non-Facebook alternative or clearly described fallback is considered; IDs and personal details are requested privately only where needed; no fake m.me link or personal contact details are added to the public repository. Removal instructions distinguish live changes from copies already downloaded.

## MAP-004 — downloadable camp edition

**P1 for in-camp/export launch · Feature gap · E1, E7, E9.** No visible save/export flow was found. The manifest describes app presentation; it does not demonstrate offline availability.

Implement the [export specification](export-spec.md), starting with a reviewed, downloadable map image and printable edition rather than silently preloading a potentially large tile archive. Make the download discoverable on mobile. A saved file may be enough for the first release; a full offline web app is a separate option.

**Done when:** map content, legend, status, version/date, public contact, and index remain usable in airplane mode after download; confirmed and historical information remain distinct; public-only export serialization is tested; displayed file size and imagery permissions are documented. Do not call a browser bookmark an offline download.

## MAP-005 — preserve claims and make submissions resilient

**P1 before form-focused promotion · Code-derived risks · E10.** In the delivered form, a rejected fetch of the historical API goes to the outer catch instead of trying the static fallback. When claim data stays unresolved, submissionType is chosen from the nullable loaded claim, allowing new-location instead of claim-existing. The submission fetch has no client deadline or visible recovery for an indefinitely pending request.

**Reproduce in preview:** open a real fixture claim URL, reject rather than return HTTP 500 from its API fetch, then inspect the form's intended submission payload without touching production. Delay a valid POST beyond the chosen deadline. Simulate a successful save whose response is lost.

**Done when:** claim identity survives loading/retry and is never silently reclassified; a network failure attempts the intended fallback or clearly blocks/requires an explicit change of intent; request timeout preserves the form; server-side idempotency/reconciliation prevents duplicate records after response loss; errors and success/confirmation ID are accessible. Verify geometry bounds, finite coordinates, self-intersection/degeneracy, length limits, authorization, spam/rate handling, and Origin checks in the backend. Client checks do not prove server checks exist. Add an easy privacy/contact link near consent.

## MAP-006 — range, caching, and realistic capacity

**P1 before mass traffic · Config finding plus unverified capacity · E8–E12.** The root route sets x-vercel-enable-rewrite-caching to 0 for every path. Sampled Vercel responses were MISS, including immutable assets. Cloudflare did report HIT for some assets, so do not describe all layers as uncached.

Measure a cold and warm real visit, then several pans/zooms, including PMTiles byte-range traffic. Confirm 206, Content-Range, body length, stable ETag, and different range contents across two offsets through both proxy and origin. Verify an invalid range safely and check that cache behavior cannot substitute one range for another. Do not download the entire archive just to inspect its header.

Propose a path-specific policy: cache proven public versioned assets/exports appropriately; use short freshness/invalidation for public status data; never shared-cache private review data, authentication responses, or submission POSTs. Review current platform defaults rather than copying old blanket advice; the explicit opt-out is the verified configuration here.

**Done when:** cold/warm transferred bytes and request counts are recorded; the PMTiles range tests pass; a documented traffic model covers the intended audience; actual Hobby/Cloudflare quotas and alerts are checked without upgrading plans. For illustration only, 5,000 visits times 10 MB is roughly 50 GB; 10 MB is not a measured site value. Run load testing only on an approved preview/staging target with an agreed request cap. No production flood. Record results, not claims of unlimited free capacity.

## MAP-007 — make Find your clan a visitor workflow

**P1 for in-camp lookup · Markup/CSS finding · E2, E11.** The list is an alphabetized historical inventory, but each clan's only action is confirm/correct. There is no in-page search or per-clan View on map action. The header Clan list link is hidden at <=640px; other list links still exist in Layers and the empty-confirmed-state card, so the list is not wholly absent on phones.

Add a prominent mobile search/list entry point, case-insensitive name filtering, an accessible empty result, and View on map links carrying a stable public clan ID. Opening one should center/highlight the intended public feature. Keep correction separate and secondary. Show current public status from the same source as the map.

**Done when:** phone, keyboard, and screen-reader users can find a specific clan without starting a submission; deep links and Back work; links survive exports; invalid IDs show a friendly fallback; search and the list remain useful without WebGL.

## MAP-008 — correct Fit markers behavior

**P2 · Code-derived defect · E9.** The button calls A(map), which fits a fixed v bounding box. Another function, j(map, featureCollection), actually computes historical bounds. The current label promises marker fitting, not a fixed overview.

**Reproduce:** pan away; hide a layer; click Fit markers; compare bounds with visible features, including approved-polygon fixtures and an empty set.

**Done when:** it fits visible public points and polygons, accommodates overlays on small screens, and has a sensible empty-state fallback. Alternatively label the current action Campground overview and provide a distinct true marker-fit action. Add bounds tests; do not animate excessively with reduced-motion preference.

## MAP-009 — remove load-order state races

**P2 · Code-derived risk · E9, E10.** Public-map load callbacks hard-code all layers on at opacity .62. Toggle effects do nothing before layers exist and need not rerun on readiness. In the form, early claim-specific easeTo can be overwritten by a later unconditional campground fitBounds.

**Reproduce:** delay map readiness while historical data returns quickly; change toggles/opacity, or open a claim URL. Then release map loading. Also reverse request order.

**Done when:** initial and subsequent map state use the latest React state; requested claim remains selected/centered after load; draft geometry is applied once its source exists; timing tests exercise both orderings. Do not reset a user's chosen view after interaction.

## MAP-010 — mobile and keyboard usability pass

**P2 · Code/CSS risks; browser reproduction still required · E9, E11, E12.** No Escape/focus-trap/focus-return logic was found in the layer component. Mobile CSS hides the status explanation; form labels and hints use small rem sizes, and persistent overlays can compete for limited screen area. Do not call these a completed WCAG audit or an observed screenshot overlap.

Use 360px and 390px portrait, short landscape, desktop, 200% text zoom, keyboard-only, and a screen reader. Include the Facebook in-app browser and the on-screen keyboard on an actual phone. Keep the existing Add center point path.

**Done when:** the drawer has intentional focus behavior and Escape dismissal; background content is appropriately inert when modal; focus returns to its opener; toggles have large labeled hit areas; essential approximation/status text is available on mobile; banners can be dismissed or collapsed without hiding the only list/contact entry; form/map controls remain reachable when the keyboard is open. Check contrast against actual map imagery rather than the CSS palette alone.

## MAP-011 — truthful Facebook link-preview artwork

**P2 · Metadata gap · E1.** Home has OG title/description/canonical but no og:image. Do not assume Facebook's current rendered card from HTML alone.

Add an approved absolute-URL image showing the real product, readable title, community/unofficial identity, and historical/2026-confirmation context. Supply useful image alt metadata and an appropriate card type. Do not display an invented finished map or private submission details.

**Done when:** the clean public URL yields the intended preview in Facebook's sharing debugger and a manual draft post; crop/text work on a phone; the image and HTML can be fetched without authentication; preview refresh procedures are documented.

## MAP-012 — synchronize public review status

**P2 · Observed content mismatch · E2, E6.** The Havok historical API feature was claim-pending, while its list card still gave generic needs-2026-confirmation text. The list identifies itself as a historical inventory, so this is an incomplete current-status presentation, not proof data was lost.

Use a shared public status model for list, marker popup, exports, and review publication. Keep historical reference, pending review, confirmed, and removed distinct; define which statuses are included in each export. Do not auto-confirm a historic marker because a form was submitted.

**Done when:** fixture transitions propagate consistently across public surfaces within the documented cache window, without leaking reviewer notes or contact fields. Test a newly added clan that was not in the 2025 inventory and a removal that must also disappear from future exports.

## Required verification work beyond these findings

See [launch-checklist.md](launch-checklist.md). In particular, anonymous access and successful submissions are not certified by the authenticated fetches used for this review. Imagery/overlay rights and real-world location accuracy require separate evidence. Add failures discovered in those checks as new tasks rather than retroactively labeling them observed here.

For each completed task, record the actual source paths/commit, changed behavior, tests performed, and evidence. Re-test against the deployed preview; do not close a task on code inspection alone when its acceptance criteria require a browser or backend.
