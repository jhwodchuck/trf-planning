# TRF Clan Map — community launch and agent handoff

Last updated: **2026-09-05**

Status: **Outreach drafts prepared; review findings open; no Facebook posts or messages sent.**

Public address: https://trf-map.vercel.app/

## Start here

| File | Purpose | Status | Source |
| --- | --- | --- | --- |
| [Facebook group post](facebook-post.md) | Themed announcement, shorter alternative, and follow-up comment | Draft for Jason to post | Owner request; reviewed live site |
| [Messenger drafts](messenger-drafts.md) | Informal one-to-one messages for leaders Jason already knows | Templates; personalize privately | Owner request; no verified recipient identities supplied |
| [Site review](site-review.md) | Findings, strengths, limits of testing, and launch recommendation | HTTP/content and delivered-code review complete | [Evidence record](evidence.md) |
| [Agent backlog](agent-backlog.md) | Prioritized tasks with reproduction guidance and acceptance criteria | Open; not implemented | Site review |
| [Export specification](export-spec.md) | Phone-friendly saved map and printable edition | Proposed; no export created in this change | Owner's in-camp distribution goal |
| [Launch checklist](launch-checklist.md) | Separate gates for leader outreach and mass in-camp distribution | Not signed off | Site review and export specification |
| [Evidence record](evidence.md) | URLs, build identifiers, observations, and primary technical references | Sanitized record | Reads made September 5, 2026 |

## Recommended positioning

Introduce this as a **community map being checked and corrected for 2026**, not a completed or verified campground navigation product. The reviewed public data contained **38 historical 2025 markers and zero confirmed 2026 boundaries**. These are time-stamped observations, not constants to hard-code into launch copy.

The leader outreach can help establish names, locations, and permission to appear. Wider in-camp distribution should follow the access, submission, reliability, and export checks. Thousands of prospective users are the intended audience, not a measured adoption or capacity claim.

## Scope and guardrails for the next agent

This change adds documentation only. It does not deploy, modify map data, approve locations, submit test claims, send messages, purchase a domain, or change account names.

This repository is public. Do not commit Messenger transcripts, a personal contact roster, contact emails, phone numbers, private submission IDs, session/share tokens, or raw submissions. Fill message placeholders privately.

The checked-in root [vercel.json](../../vercel.json) proxies to a Cloudflare Worker. Existing [CLAUDE.md](../../CLAUDE.md) describes the separate planning-document site. The exact source repository/path and deployment commit for the live Worker have **not** been established. Resolve MAP-001 before editing production code; do not mistake the older static planning viewers for this app.

Keep `jhwodchuck` as Jason's account identity. Use the clean Vercel address in participant-facing copy. Do not weaken authentication, expose private data, enable GPS tracking, or add paid services to satisfy this handoff.

## Information still needed

Jason's approved public contact destination; the exact Facebook group name/rules; private recipient names/clans; the Worker source location; real-device and anonymous-browser test results; export imagery provenance and release sign-off.
