---
slug: cross-team-coordination
name: Cross-Team Coordination
description: Sequence handoffs when work spans multiple teams.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.2.0
---

# Cross-Team Coordination

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream `anthropics/financial-services`. Owned by the CEO role.

## When to fire

After `intake-triage` flagged the request as cross-team (2+ agents from different teams). The CEO uses this to plan and sequence the handoffs so specialists don't block each other or duplicate work.

## Inputs

- The triage decision from `intake-triage` (primary agent, secondary agents, deadline, priority).
- The work request itself.

## Outputs

A coordination plan, recorded on the work item:

```yaml
sequence:
  - step: 1
    agent: <agent-slug>
    skill: <skill>
    inputs: <what they need to start>
    outputs: <what they produce, by when>
  - step: 2
    agent: <agent-slug>
    ...
checkpoints:
  - after_step: 1
    review: <what the CEO checks before unblocking step 2>
final_handoff: <agent that owns the deliverable>
```

## How to plan a multi-team workflow

1. **Identify the deliverable.** Who owns the output that goes to the requester? That agent runs last.
2. **Walk back the dependency chain.** What does the deliverable need? Each input becomes a step earlier in the sequence, owned by whichever agent produces it.
3. **Identify shared dependencies** (the same comps run feeds the pitch *and* the model — run it once, fan out to both consumers).
4. **Set checkpoints** at every team boundary. The CEO reviews artifacts before unblocking the next step. This catches "this isn't what I needed" before it propagates.
5. **Allocate buffer for the deadline.** Cross-team work always takes longer than serial estimates suggest.

## Common coordination patterns

| Workflow | Sequence |
|---|---|
| Full pitch | market-researcher (sector) → model-builder (DCF + comps) → pitch-agent (deck) → meeting-prep-agent (briefing) |
| Earnings update with re-rating | earnings-reviewer (note + model update) → market-researcher (peer impact) → pitch-agent if a fresh client take is needed |
| Quarterly close + statement | gl-reconciler (recon) → month-end-closer (accruals + variance) → valuation-reviewer (NAV) → statement-auditor (LP statement) |
| New LP onboarding + first capital call | kyc-screener (onboarding pack) → valuation-reviewer (capital call schedule) → statement-auditor (initial statement format) |

## Boundaries

- The CEO does not write the artifacts — only sequences them.
- If a checkpoint reveals a problem (wrong inputs, missing data, off-thesis output), invoke `escalation-routing` rather than papering over it.
- If the workflow doesn't match a known pattern, plan it explicitly rather than improvising at runtime.
