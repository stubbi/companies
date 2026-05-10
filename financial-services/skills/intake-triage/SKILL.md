---
slug: intake-triage
name: Intake Triage
description: Classify an incoming work request and route it to the right team.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.2.0
---

# Intake Triage

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream `anthropics/financial-services`. Owned by the CEO role.

## When to fire

Any new work request that arrives without an explicit team / agent assignment. This is the first skill the CEO runs on incoming items.

## Inputs

- The raw request: an issue body, a meeting outcome, an inbound email, a Slack message, or any free-text task description.
- Optional context: requester role, deadline, related deal / portfolio, attachments.

## Outputs

A triage decision, written back as a short note on the request, with these fields:

```yaml
team: coverage-advisory | research-modeling | fund-admin-finance-ops | operations-onboarding | escalate
primary_agent: <agent-slug>
secondary_agents: [<agent-slug>, ...]   # for cross-team work; CEO will coordinate via cross-team-coordination
priority: P0 | P1 | P2 | P3
deadline: <ISO date or "asap" or "best-effort">
boundaries: [<note>, ...]                # call out anything that requires human sign-off
```

## How to triage (decision tree)

1. **Is this a deal pitch / coverage activity?** → `coverage-advisory`. Pitch decks, comps, precedent transactions, meeting prep all live here. Primary: `pitch-agent` for full pitches, `meeting-prep-agent` for briefings.
2. **Is this research, modeling, or earnings analysis?** → `research-modeling`. Sector research, earnings reviews, DCF / LBO / 3-statement work. Primary: `market-researcher`, `earnings-reviewer`, or `model-builder` based on the artifact requested.
3. **Is this fund admin / NAV / GL / valuation?** → `fund-admin-finance-ops`. Includes month-end close, statement audit, valuation review, GL reconciliation. Primary depends on the workflow.
4. **Is this KYC or client onboarding?** → `operations-onboarding`. Primary: `kyc-screener`.
5. **Does it span 2+ teams?** Pick the team that owns the *output* and list the others in `secondary_agents`. Then enqueue `cross-team-coordination`.
6. **Does it require a decision the agents can't make?** (Investment recommendations, trade execution, ledger postings, onboarding approval, regulatory filings.) → `escalate`. Note the boundary and route to a human.

## Boundaries

- The CEO does not perform the triaged work — only routes it.
- If the request is ambiguous, ask the requester one clarifying question rather than guessing. Don't over-interpret.
- Investment / legal / regulatory recommendations always escalate, even if the request looks routine.

## Output protocol

Write the triage decision as a comment / note on the work item, and tag the primary agent for pickup. If `cross-team-coordination` is needed, enqueue that skill on yourself before the specialists start.
