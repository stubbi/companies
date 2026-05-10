---
slug: weekly-summary
name: Weekly Summary
description: Compose the company-level weekly digest — what shipped, what's blocked, what needs review.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.2.0
---

# Weekly Summary

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream `anthropics/financial-services`. Owned by the CEO role.

## When to fire

Once per week (recommended cadence: Friday afternoon or Monday morning), or on-demand from a stakeholder request.

## Inputs

- All work items closed, blocked, or escalated since the last summary.
- The current backlog (open items, ordered by priority).
- Any human-overrides or escalation outcomes since the last summary.

## Outputs

A short markdown digest, written as a comment / note on a designated weekly summary item, with this structure:

```markdown
# Week of <YYYY-MM-DD>

## Shipped
- <agent>: <one-line description> (<link>)

## In flight
- <agent>: <work item> (<status, ETA>)

## Blocked / awaiting review
- <work item> — <what's blocking, who needs to act>

## Escalated to human
- <work item> — <decision needed>

## Next week
- <priority items, in order>
```

## How to compose

1. **Walk the week's work**, oldest to newest. Group by team, then by agent.
2. **For "Shipped":** include the deliverable in one line — what it was, who got it. No process narration.
3. **For "In flight":** include status (% complete or stage) and ETA. If ETA slipped, say so explicitly.
4. **For "Blocked":** name the blocker and the unblocking action required. If the unblock is on a human, list them by name.
5. **For "Escalated":** include the decision needed and the recommendation made. Don't restate the analysis — link to it.
6. **For "Next week":** the top 3-5 items by priority. If there's a deadline, name it.

## Style

- **Short.** Aim for one screen. Cut paragraphs that don't add information.
- **Concrete.** "Pitch deck for Acme delivered" beats "Coverage team active on Acme account."
- **Honest about misses.** If a model slipped two days, say "two days late, blocked on missing GP package." Do not paper over.
- **No agent self-praise.** The summary is for stakeholders, not agent vanity.

## Boundaries

- Never include client identifiers, deal codenames, or material non-public information without checking the requester's access level.
- Numbers in summary (deal sizes, valuations, performance) must be sourced — link to the underlying artifact, not the agent's recollection.
- Don't editorialize on portfolio performance or investment outcomes; that's the analysts' and PMs' job.
