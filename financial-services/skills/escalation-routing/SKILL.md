---
slug: escalation-routing
name: Escalation Routing
description: When a specialist reports a blocker, decide between retry, reassign, or escalate-to-human.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.2.0
---

# Escalation Routing

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream `anthropics/financial-services`. Owned by the CEO role.

## When to fire

A specialist agent reports a blocker, fails a task, or signals it's hit something it can't handle. The CEO routes the response.

## Inputs

- The blocker report: what was attempted, what went wrong, what the agent thinks the next step is.
- Recent activity log for the agent.
- The original work request and any cross-team coordination plan in flight.

## Outputs

A routing decision recorded on the work item:

```yaml
decision: retry | reassign | escalate-to-human | abandon
reason: <one-line rationale>
follow_up:
  - <action>
  - <action>
notify: [<requester>, <other agents>]   # who needs to know
```

## Decision rules

1. **Retry** when the failure is transient or fixable with a small adjustment:
   - Tool-call timeout, rate limit, intermittent network error → retry with backoff
   - Missing one input that's recoverable → fetch the input, retry
   - Output didn't match the requested format → re-prompt with the format spec

   **Cap retries at 2.** Beyond that, the failure is structural — escalate or reassign.

2. **Reassign** when the right agent for the work isn't the one currently holding it:
   - Triage was wrong (model-builder picked up something better suited to valuation-reviewer)
   - Scope expanded mid-task and now belongs to a different team
   - Specialist is overloaded and a peer can pick it up

3. **Escalate-to-human** when the blocker requires a decision agents can't make:
   - **Always** for: investment recommendations, trade execution, ledger postings, onboarding approvals, regulatory filings, legal interpretations.
   - When inputs are ambiguous about a regulated boundary (e.g., a request implicitly asks the model-builder to *decide* the assumptions for a real investment, not just *build* the model).
   - When external data is unavailable / rate-limited / missing and the work can't proceed without it.
   - When the agent reports it's been told something that contradicts a Boundaries rule in COMPANY.md.

4. **Abandon** when the work is stale, no longer needed, or superseded by a later request. Always log why.

## Escalation note format

When escalating to a human, include:
- The original request (link)
- What the agents tried (links to attempts)
- The specific decision needed from the human
- A short, fair recommendation (the CEO is the agent voice, not the decision-maker — but the human deserves a recommendation)

## Boundaries

- The CEO never overrides a Boundaries rule. If a specialist refused a task because it crossed a boundary, the CEO escalates rather than re-routing to a different specialist who might not catch the issue.
- The CEO does not perform the work itself even if the team is jammed. Better to escalate than to fake competence on a domain it doesn't own.
