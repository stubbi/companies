---
slug: weekly-summary
name: Weekly Summary
description: Compose the company-level weekly digest — what shipped, what's blocked, what needs attorney review.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Weekly Summary

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream `anthropics/claude-for-legal`. Owned by the CEO role.

## When to fire

Once a week, on a fixed cadence (default: Monday morning) — or on demand when the GC or supervising attorney asks for a portfolio-wide read. This is a coordination artifact, not legal work product.

## Inputs

- The matter ledger for the prior 7 days (or since the last summary), spanning all 4 teams and 12 specialists.
- Each practice's recent activity:
  - `commercial-legal`: contracts reviewed; renewals approaching; escalations sent; deviation log additions; deal-debrief findings.
  - `corporate-legal`: matters opened / closed; closing-checklist status; entity-compliance deadlines hit / approaching; data-room watcher activity.
  - `employment-legal`: hires reviewed; terminations reviewed; open investigations; open leaves with upcoming statutory deadlines; international-expansion stages reached.
  - `privacy-legal`: PIAs opened / completed; DSAR queue (received vs. responded vs. overdue); DPA reviews; policy-monitor drift flags.
  - `ai-governance-legal`: AI use cases triaged; AIAs run; vendor-AI reviews; AI policy-monitor drift flags.
  - `regulatory-legal`: reg-feed digest highlights; new gaps opened; gaps closed; NPRM comment-period status.
  - `product-legal`: launches reviewed; "is this a problem?" volume; marketing-claims checks; launch-watcher upcoming.
  - `ip-legal`: clearance / FTO triages run; C&Ds drafted; portfolio renewals approaching; IP-clause reviews.
  - `litigation-legal`: matters opened / closed; demand letters drafted (with send-gate status); subpoenas received / triaged; chronologies built; legal holds issued / refreshed / released; portfolio status (risk distribution, stale matters).
  - `law-student` / `legal-clinic`: only included if active in the prior week.
  - `legal-builder-hub`: skills evaluated; skills installed (with security-review timestamp).
- Escalations sent to humans in the prior 7 days, with response status.

## Outputs

A single Markdown digest, organized by team:

```markdown
# Legal-Services Weekly Summary — week of <date>

## At a glance

- Matters shipped: <n> (across <m> practices)
- Matters opened: <n>
- Matters blocked / awaiting attorney review: <n>
- Escalations sent: <n>; awaiting response: <m>
- Drift flags this week: <n> (privacy: x, AI: y, regulatory: z)

## Commercial & Transactions
### commercial-legal — <one-line headline>
- <bullet>
- <bullet>
### corporate-legal — <one-line headline>
- <bullet>
### employment-legal — <one-line headline>
- <bullet>

## Regulatory & Compliance
…

## IP & Disputes
…

## Legal Academy & Tooling
…

## Awaiting attorney review

- <matter ID> — <one-line>; specialist: <agent>; days waiting: <n>
- …

## Escalations & deadlines for the coming week

- <matter ID> — <deadline>, <jurisdiction>, <what's needed>
- …
```

## What stays OUT

- **Privileged work-product details.** The summary surfaces *that* a matter exists and *what* its status is; it never reproduces privileged advice, draft litigation strategy, demand-letter language, deposition outlines, or investigation findings. If a matter is sealed under privilege, the summary lists it by matter ID only.
- **Counterparty-identifying detail** when distribution of the summary goes beyond the matter's privileged circle. A matter touching active sensitive negotiations or a regulator investigation gets summarized in aggregate only.
- **Client-identifying detail** in clinic / supervising-attorney contexts unless the recipient has the clinic's authorization.
- **Anything outside the prior 7-day window** — the summary is a snapshot, not a portfolio dump.

## Boundaries

- The CEO produces this summary; the CEO does not interpret it. Whether a flag is "concerning" or "routine" is for the supervising attorney to call.
- The CEO never aggregates across matters in a way that would create a new privilege issue. If two matters share counsel and one is privileged, the aggregation does not break privilege — but if combining them would identify a privileged matter, omit the privileged one.
- The CEO never recommends an action in this summary. Recommendations belong to the responsible attorney; the summary's job is visibility.

## Output protocol

Write the digest to a fixed location (e.g., `~/legal-services/weekly/<YYYY-MM-DD>.md`) and route it to the supervising attorney / GC. Update the matter audit log with a one-line entry per matter referenced.
