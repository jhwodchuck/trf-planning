# Saved and printable campground map — proposed specification

Last updated: **2026-09-05**

Status: **Proposed implementation contract; not an existing download or completed export.**

Goal: let campers use a useful version of the public map after losing reception, and let the same information be shared without exposing submission/contact records. This responds to Jason's intended audience, not measured campground network conditions.

## First release

Provide a phone-friendly downloadable image plus a printable PDF, linked from a visible Save map action. Generate both from one reviewed, versioned public snapshot. Consider a light-background overview plus sector/detail sheets and a name index rather than shrinking every name onto one crowded page. A screenshot of the app's floating controls is not the release artifact.

Do not require a full offline PWA for the first release. A downloaded, self-contained image/PDF can satisfy the saved-edition use case. An interactive offline mode needs its own caching, tile coverage, storage, refresh, and eviction tests; a manifest or cached home page alone is insufficient.

## Required content

| Element | Acceptance | Status | Source |
| --- | --- | --- | --- |
| Identity | TRF Clan Map; explicit community-made/not official wording | Proposed | Owner request; review |
| Version and currency | Season, revision, generated timestamp/time zone, data-as-of date, stable release filename | Proposed | Review recommendation |
| Accuracy | Historical/pending/confirmed legend using text and shapes, not color alone; approximate-location caveat | Required to preserve | Live public data/UI |
| Orientation | North arrow, appropriate scale bar, readable reference grid, reviewed roads/landmarks | Proposed | Camp lookup use case |
| Lookup | Alphabetical clan index with stable public IDs and grid/sector references | Proposed | MAP-007 |
| Contact | Contact Jason instructions with an owner-verified destination, not just whoever shared the file | Proposed | MAP-003 |
| Return path | Printed clean URL plus tested QR code; QR is supplementary because it needs connectivity | Proposed | Public site address |
| Attribution | Imagery/artwork credits and licenses/permissions suitable for redistribution | Unverified gate | E8; provenance review required |
| Disclaimer | Not a reservation, boundary survey, proof of occupancy, or emergency-navigation tool | Required | Live public data/UI |

Do not turn an old label center into an invented camp polygon. Do not draw precise-looking boundaries from schematic artwork. Prefer confirmed current locations for the main participant edition; where coverage is incomplete, either clearly include historical references as a different layer/edition or disclose the gaps. Never silently label all entries 2026-confirmed.

## Data and privacy contract

Use a public allowlist: public clan ID, approved display name, appropriate public geometry, approved public note, publication status, and relevant public update date. Do not export contact names/emails, raw submissions, review notes, session tokens, order details, private household/equipment planning records, or unapproved proposed boundaries. A filename containing private-data is not itself a useful privacy classification.

Moderation must produce one explicit public release snapshot. Generate map, legend, counts, and index from it; validate counts and IDs against the export rather than assuming every label fit on the canvas. An opt-out removes a listing from the live dataset and future editions according to the approved process. Explain that previously downloaded or reshared copies cannot be recalled.

## Build and delivery

Use content/versioned asset names and a small release manifest with checksum, file size, revision, included area/statuses, and download URLs. Choose file-size budgets after measuring representative phones and rendering quality; do not promise an unmeasured download size. Avoid generating a large export separately for each visitor. Host public release assets with a reviewed cache policy and a stable latest-release landing page.

Confirm that satellite tiles, schematic artwork, fonts, and symbols permit the proposed online and downloadable uses. Existing planning documentation does not establish permission for the live Worker's assets. No infringement is alleged by this review; the permission chain is simply unverified. Use alternative suitably licensed/public-domain sources if necessary.

## Release acceptance

Download on Android and iPhone, enable airplane mode, close and reopen the file, and verify every sheet/image remains usable. Check names, roads, legend, index, contact, and QR at normal phone zoom and actual paper size. Test grayscale/low-ink print output, clipping, dense labels, and long clan names. Open the PDF in common viewers; no JavaScript or external network fetch should be necessary to see the map.

Compare the generated release with the approved data snapshot, field/leader checks, and permissions record. Withhold a release labeled final while these gates remain open. Follow [launch-checklist.md](launch-checklist.md).
