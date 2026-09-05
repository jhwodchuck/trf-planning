# TRF Clan Map — release gates

Last updated: **2026-09-05**

Status: **Checklist prepared; unchecked items are unverified, not automatically failed.**

## Before the leader-feedback post

- [ ] Jason confirms the intended Facebook group and its rules; no assumed admin endorsement.
- [ ] Clean https://trf-map.vercel.app/ opens in a logged-out phone browser with no Vercel account, temporary share link, or special cookie.
- [ ] The same link opens from a Facebook draft/in-app browser, and a normal-browser fallback is understandable.
- [ ] Current map/list content matches the post: historical markers are clearly not confirmed current boundaries.
- [ ] The post comes from Jason's own account, and he can receive message requests. A verified persistent site contact is addressed in MAP-003.
- [ ] One controlled preview submission travels through the proxy and is acknowledged without public disclosure; production test data is not fabricated.
- [ ] Jason approves the wording and any screenshot, especially references to a future saved edition.

## Before mass in-camp distribution

- [ ] MAP-001 identifies the app source and repeatable deployment/rollback.
- [ ] Loading failure, slow network, and no-WebGL tests pass (MAP-002).
- [ ] Search/list/View on map is usable on phone and keyboard without opening an edit workflow (MAP-007).
- [ ] Real-device checks cover Android Chrome, iPhone Safari, Facebook's in-app browser, portrait/landscape, keyboard-open forms, and text zoom. Record devices/versions.
- [ ] Claim/new submission identity, retries, response loss, duplicate prevention, useful error states, and success confirmation pass on preview (MAP-005).
- [ ] A moderator can review a fixture, publish only allowed fields, and see correct public results; reject/remove paths and conflicting claims are handled without automatically awarding a campsite.
- [ ] Unauthorized users cannot read raw submissions or private moderation data. Test fixtures with nonempty approved features, not just an empty public collection.
- [ ] Server-side validation, appropriate abuse controls, and request-origin behavior are checked in the actual backend. No uncontrolled live stress test.
- [ ] Leader/field checks establish the publication status of each location; disputed, uncertain, moved, and opted-out camps are represented appropriately.
- [ ] Imagery, overlay, and redistribution permissions/attribution are recorded for the release.
- [ ] PMTiles range/ETag behavior, cold/warm visit bytes, and path-specific caching are measured (MAP-006).
- [ ] A documented traffic/transfer estimate is compared with current account quotas. Alerting and a rollback/fallback plan exist; no paid upgrade is assumed.
- [ ] Saved image/PDF passes the complete airplane-mode and print tests in [export-spec.md](export-spec.md).
- [ ] Status/date/contact/unofficial caveats survive exports and social crops. The QR points to the clean durable URL.
- [ ] Facebook's link preview is checked with the actual public artwork and current metadata (MAP-011).

## During and after sharing

Keep a private correction queue and review message requests. Separate a broken-site report from a location correction, privacy request, disputed authority, or old downloaded copy. Acknowledge without promising a change that has not yet been reviewed. Track publication changes with public-safe revision notes, not Messenger transcripts.

Review aggregate error rates and transfer/request use without collecting unnecessary personal data. Schedule release refreshes around actual data changes; do not promise updates in drafts that lack an owner/process. Retest a normal guest session after deployments.

## Sign-off record to complete

| Area | Owner | Status | Evidence required |
| --- | --- | --- | --- |
| Outreach wording and public contact | Jason | Pending | Approved draft/contact destination |
| Anonymous and real-device access | Implementing agent + human tester | Pending | Device/browser/build/date and results |
| Submission/moderation/privacy | App maintainer | Pending | Preview tests with sanitized fixtures |
| Location accuracy and inclusion | Jason + relevant clan representatives | Pending | Private verification, public-safe status |
| Capacity/caching and rollback | App maintainer | Pending | Measured report and current quota check |
| Saved edition and rights | Map maintainer + Jason | Pending | Approved snapshot, permissions, offline/print results |

This checklist makes no claim of TRF approval, existing uptime targets, measured visitor numbers, or an unlimited free hosting guarantee.
