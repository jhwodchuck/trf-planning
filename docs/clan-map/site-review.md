# TRF Clan Map — pre-distribution site review

Last updated: **2026-09-05**

Status: **Review completed within the scope below; fixes and release validation remain open.**

## Recommendation

Use a **leader-confirmation campaign** first. Do not present the current site as a finished, offline-ready guide for thousands of campers. The reviewed data has 38 historical 2025 markers and zero confirmed 2026 boundaries. Gathering corrections is a legitimate launch purpose; broad in-camp navigation needs additional testing and a usable saved edition.

This recommendation is about readiness and positioning, not a claim that the site has failed under load. No capacity test was performed.

## Scope and version

Reviewed the live home page, clan list, privacy page, a claim URL, public location data, web manifest, delivered map/submission JavaScript, and mobile/desktop CSS. Also inspected the Vercel project/deployment and the GitHub proxy configuration. Exact URLs and fingerprints are in [evidence.md](evidence.md).

Reads were made on September 5, 2026, approximately 20:16–20:21 UTC (15:16–15:21 CDT). The Worker reported deployment version `4e3d6a74-029b-44f3-8909-78a68c6ae7cc`. The Vercel wrapper deployment was `dpl_6b4wPTnEF8P1CC6DTPnQvHeXB38y`. The upstream application had changed since the earlier proxy setup; findings here refer to these later assets.

**Important limits:** the Vercel fetch tool uses an authenticated/share-assisted route. Its HTTP 200 responses do not independently establish anonymous access. Container DNS/browser network access failed, and public web retrieval of the Vercel URL was unavailable in this environment. Those are testing limitations, not observed site outages. No live rendered desktop/mobile screenshots, device interactions, Facebook in-app browser session, offline test, successful POST, moderation cycle, load test, or full backend security audit was completed. Responsive findings below are derived from delivered markup/CSS, not a claimed visual pass. No real or fake clan submission was sent.

## What is already in place

| Area | Status | Source |
| --- | --- | --- |
| Clean public-facing URL and upstream routing | Vercel project exists; checked-in route proxies to the original Worker | E1, E8 |
| Historical versus current location distinction | Explicit 2025/2026 caveats in map UI, list, and data | E1, E2, E5, E6 |
| Clan-list alternative | Server-rendered list of 38 historical names with correction links | E2 |
| Submission privacy and review explanation | Visible in form and privacy page; promises require backend verification | E3, E4, E10 |
| Keyboard-assisted boundary drawing | Delivered form supports an Add center point button and keyboard-pan instructions | E3, E10 |
| Responsive form layout | CSS changes to map above form at narrow widths; actual usability untested | E12 |
| Canonical and social text metadata | Correct Vercel URL, titles, descriptions, manifest and favicon | E1, E7 |
| Security headers | CSP, anti-framing, referrer and permissions policies observed on HTML | E1, E3, E4 |

These should be preserved rather than rebuilt blindly.

## Findings to act on

| ID | Priority | Finding | Evidence class / source |
| --- | --- | --- | --- |
| MAP-001 | P1 | The live Worker source/deploy commit is not identified by the reviewed repo documentation. Current CLAUDE.md describes the older planning site. | Handoff gap; E8 |
| MAP-002 | P1 | Failed location fetches leave the same null state as loading, so the UI can keep saying Loading clan locations indefinitely. Map errors only change a hidden-from-accessibility color dot. | Delivered-code finding; E9 |
| MAP-003 | P1 | No direct named maintainer contact in reviewed map/form/privacy UI. Privacy tells people to find whoever shared the map; historical-marker owners may have no submission ID. | Content finding; E1–E4 |
| MAP-004 | P1 for participant distribution | No discoverable saved-map/export flow in reviewed UI. A web manifest is present but is not evidence of offline map functionality. | Feature gap, not an offline runtime test; E1, E7, E9 |
| MAP-005 | P1 before promoting form completion | Submission reliability needs work/verification: no client timeout; a rejected historical fetch skips its fallback; an unresolved claim can be submitted as a new location. | Delivered-code finding, backend not assessed; E10 |
| MAP-006 | P1 before mass use | Root proxy explicitly disables rewrite caching on all paths; all sampled Vercel responses were MISS, while some assets were Cloudflare HIT. Range correctness, bytes per visit, and capacity remain unmeasured. | Configuration finding plus verification gate; E8, E9, E12 |
| MAP-007 | P1 for in-camp lookup | Clan-list cards lead to correction forms rather than a selected map location; no list search was present. The top-level Clan list link is hidden at widths at or below 640px. | Markup/CSS finding; E2, E11 |
| MAP-008 | P2 | Fit markers uses a fixed campground box, not actual visible-feature bounds. A separate function computes historical marker bounds but is not used by that button. | Delivered-code finding; E9 |
| MAP-009 | P2 | Layer/opacity choices made before load can be replaced by hard-coded initial values; claim centering can be overwritten by the form's later load-time fitBounds. | Timing risk derived from code; E9, E10 |
| MAP-010 | P2 | Layer drawer lacks component-level Escape/focus management. Mobile CSS hides the explanatory status sentence; small text and persistent cards need actual phone testing. | Code/CSS finding; no accessibility certification; E9, E11, E12 |
| MAP-011 | P2 | Open Graph text exists but no og:image was present on the home page. No actual Facebook preview test completed. | Metadata finding; E1 |
| MAP-012 | P2 | The historical list gives Havok generic needs-confirmation text while the current API reports claim-pending. The list is labeled a reference inventory, but lacks current review status. | Cross-surface content mismatch; E2, E6 |

P1 means needed before the relevant launch promise, not a confirmed emergency. P2 means important follow-through. Reproduction guidance and definitions of done are in [agent-backlog.md](agent-backlog.md).

## Separate release gates, not proven vulnerabilities

Anonymous access; real-device rendering; successful through-proxy submissions; authorization and moderation; public/private field separation; anti-abuse controls; HTTP Range behavior; actual performance; and imagery redistribution rights are **unverified**, not established failures. Test those deliberately. Never interpret the path name `private-data` as a security boundary: the reviewed files there are public-facing map layers, and their names alone do not imply leaked private submissions.

Only the map's public location endpoints were inspected. No private contact leak was found in those sampled responses, but zero confirmed features cannot prove every future approved-feature serializer is safe.

## For the intended campground audience

Prioritize finding a clan over editing one: a prominent searchable list, View on map action, large readable controls, explicit historical/pending/confirmed labels, and a saved edition. Keep the satellite view as context rather than implying survey accuracy. Use a simple low-ink/export mode instead of relying on a phone screenshot of floating controls.

GPS is not currently enabled: the observed Permissions-Policy includes geolocation=(), and the reviewed map has no location button. Treat a future on-device You are here feature as an optional product/privacy decision, not a hidden change needed to launch. Do not market turn-by-turn or emergency navigation.

See [export specification](export-spec.md) and [launch checklist](launch-checklist.md). No live application behavior was modified by this documentation change.
