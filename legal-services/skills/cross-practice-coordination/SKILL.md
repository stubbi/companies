---
slug: cross-practice-coordination
name: Cross-Practice Coordination
description: Coordinate handoffs when work spans multiple practice areas (e.g., M&A diligence touching IP + employment + privacy).
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Cross-Practice Coordination

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream `anthropics/claude-for-legal`. Owned by the CEO role.

## When to fire

After `intake-triage` flagged the matter as multi-practice (2+ specialists from different practice areas). The CEO uses this skill to sequence handoffs so specialists don't block each other, duplicate work, or — worst — produce work product that contradicts another practice's position on the same matter.

## Inputs

- The triage decision from `intake-triage` (primary agent, secondary agents, deadline, priority, jurisdiction, privilege posture).
- The matter itself.

## Outputs

A coordination plan, recorded on the matter:

```yaml
sequence:
  - step: 1
    agent: <agent-slug>
    skill: <skill-slug>
    inputs: <what they need to start>
    outputs: <what they produce, by when>
    privilege: <how privilege is preserved across this handoff>
  - step: 2
    agent: <agent-slug>
    ...
checkpoints:
  - after_step: 1
    review: <what the CEO checks before unblocking step 2>
deconflict_protocol: <rule for resolving disagreements between specialists>
final_deliverable_owner: <agent that owns the deliverable to the requester>
human_signoff_required_before: [<artifact>, ...]
```

## How to plan a multi-practice workflow

1. **Identify the deliverable.** Who owns the output that goes to the requester? That agent runs last and produces the final artifact.
2. **Walk back the dependency chain.** What does the deliverable need? Each input becomes a step earlier in the sequence, owned by whichever specialist produces it. Example for an M&A diligence run touching IP + employment + privacy:
   - Final: `corporate-legal` produces the diligence memo + disclosure schedule.
   - Inputs: `ip-legal` produces the IP portfolio + clearance findings; `employment-legal` produces the workforce diligence (restrictive covenants, leave-tracker exposure, open investigations); `privacy-legal` produces the processing-activity inventory and DPA-stack review.
   - Sequence: parallel ip-legal + employment-legal + privacy-legal → merge into corporate-legal.
3. **Identify shared inputs.** If two specialists need the same artifact (e.g., the target's processing-activity inventory feeds both privacy-legal and ai-governance-legal), produce it once and fan out — don't have two practices repeat it.
4. **Preserve privilege across handoffs.** Specialists hand each other *summaries and citations*, not full privileged workproduct, unless the matter is run as a unified privileged investigation under common interest. Note the privilege posture explicitly at each step.
5. **Define a deconflict protocol.** When specialists disagree (e.g., privacy-legal thinks the new feature requires a PIA; product-legal thinks the risk calibration says no), the disagreement itself is the deliverable to the CEO. Do not pick a side automatically; surface it for attorney review.

## Common multi-practice patterns

- **M&A diligence on a target with US + EU workforce and a data-stack.** Threads: corporate-legal (lead), ip-legal, employment-legal, privacy-legal. Watch for: privilege boundary when the target's outside counsel is producing privileged materials under common interest.
- **Product launch touching privacy + AI + regulated industry.** Threads: product-legal (lead), privacy-legal, ai-governance-legal, regulatory-legal. Watch for: AI inventory updates feeding the AI policy monitor.
- **Internal investigation with employment + privacy + litigation dimensions.** Threads: employment-legal (lead under privilege), privacy-legal (DSAR exposure, retention conflicts), litigation-legal (hold issuance, anticipated litigation). Watch for: privilege preservation; investigation log must remain attorney work product.
- **Counterparty demand crossing IP + commercial.** Threads: litigation-legal (lead), ip-legal (IP portfolio cross-check), commercial-legal (underlying contract terms, FRE 408 awareness). Watch for: send-gate on any counter-response.

## Boundaries

- The CEO sequences but does not perform. Each specialist still owns their own skill calls.
- The CEO does not resolve cross-practice legal disagreements. When specialists conflict, the deliverable is the conflict itself, surfaced for attorney review.
- The CEO never relaxes the privilege posture across a handoff. If preserving privilege requires routing through outside counsel, escalate.
- The CEO never speeds up a workflow by collapsing a checkpoint. Checkpoints exist because the next step's output depends on the prior step's review.

## Output protocol

Write the coordination plan to the matter as a comment / note. Enqueue step 1's specialist skill. After each checkpoint, the CEO re-reviews against the plan; only then does step N+1's specialist get unblocked.
