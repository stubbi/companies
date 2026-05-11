---
slug: escalation-routing
name: Escalation Routing
description: When a stage owner reports a real blocker (integrity FAIL after 3 retries; reviewer Reject; user-rejected outline), escalate to the human researcher with context.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Escalation Routing

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream `Imbad0202/academic-research-skills`. Owned by the CEO role.

## When to fire

The CEO fires this skill only when a stage owner cannot proceed and the issue is not resolvable within the pipeline's normal protocols. This is the off-ramp from the linear pipeline — not a routine handoff.

## What counts as a real blocker

| Trigger | Source | Why it escalates |
|---|---|---|
| Integrity gate 2.5 FAIL after 3 retries | integrity-officer | The 7-mode failure checklist could not be cleared. Pipeline contract forbids further silent retries. |
| Integrity gate 4.5 FAIL | integrity-officer | Zero-tolerance gate — no retries permitted. |
| Reviewer Reject decision at Stage 3 | reviewer | Pipeline ends; the user needs to decide whether to redirect the work, scope down, or abandon. |
| Revision-loop cap hit (2 loops complete) at 3' | reviewer / pipeline-orchestration | Hard cap reached. Further iteration is frame-lock. |
| User rejects outline at checkpoint 2 after 3 attempts | checkpoint-coordination | The pipeline can't second-guess the user's intent indefinitely. |
| Authorship / ethics question raised | any stage | Out of scope for the pipeline by design. |
| Citation hallucination flagged but unresolvable | researcher / writer | Cannot proceed without verifying or removing the claim. |

## What does NOT count as a blocker

- A reviewer Major decision (handle via revision coaching → Stage 4).
- A SUSPECTED flag at 2.5 that becomes CLEAR on retry.
- A user revision request mid-stage (route back to the stage owner via `pipeline-orchestration`).
- An external API blip (deep-research / S2 verification) — retry with backoff first.

Misclassifying these as blockers turns the pipeline into a panic loop. Let the stage owners do their job before escalating.

## Outputs

An escalation packet for the human researcher:

```yaml
trigger: <one of the trigger labels above>
stage: <stage-id where it occurred>
artifact: <pointer to the failing artifact>
machine_report: <verbatim — integrity report, reviewer decision letter, etc.>
attempted_recoveries: [<what the stage owner tried before escalating>]
options_for_user:
  - <option 1: e.g. "Override the integrity gate (not recommended)">
  - <option 2: e.g. "Restart Stage N with revised inputs">
  - <option 3: e.g. "Abandon the pipeline">
suggested_action: <CEO's recommendation, with one-line justification>
```

## Boundaries

- The CEO does not unilaterally override an integrity gate. Override is a user decision, surfaced as an option but never selected by the agent.
- Do not paraphrase the machine_report. Verbatim only — paraphrasing hides SUSPECTED flags and reviewer concerns.
- Do not loop back into the pipeline on the user's behalf. Wait for the user's explicit choice from `options_for_user`.
- If the trigger is an authorship / ethics question, do not propose options at all. Hand the question to the user with no agent-generated framing.

## Output protocol

Write the escalation packet as a high-priority note on the work item. Tag the human researcher (not another agent). Pipeline state remains paused at the failing stage until the user responds.
