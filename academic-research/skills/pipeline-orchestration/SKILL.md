---
slug: pipeline-orchestration
name: Pipeline Orchestration
description: Walk the user through the linear stage handoffs (1 → 2 → 2.5 → 3 → … → 6); enforce the 2-revision-loop hard cap.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Pipeline Orchestration

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream `Imbad0202/academic-research-skills`. Owned by the CEO role.

## When to fire

After `intake-triage` has chosen a mode + entry stage, and again after each stage owner reports their stage complete. Drives the linear ARS pipeline state machine from the CEO's seat.

## Pipeline contract

The ARS pipeline has a fixed stage order with a hard cap on revision loops:

```
1. RESEARCH    → researcher
2. WRITE       → writer
2.5 INTEGRITY  → integrity-officer  [MANDATORY gate, max 3 retries]
3. REVIEW      → reviewer
[3 → 4 Revision Coaching, max 8 Socratic rounds, user may skip]
4. REVISE      → writer
3'. RE-REVIEW  → reviewer  [narrow team]
[3' → 4' Residual Coaching, max 5 Socratic rounds, user may skip]
4'. RE-REVISE  → writer    [content frozen after this]
4.5 FINAL INTEGRITY → integrity-officer  [MANDATORY zero-tolerance gate]
5. FINALIZE    → writer
6. PROCESS SUMMARY → integrity-officer
```

**Hard cap:** maximum 1 RE-REVISE round → 2 revision loops total across Stages 4 + 4'. This is non-negotiable — see `two_stage_review_protocol.md` upstream.

## Outputs (per handoff)

```yaml
current_stage: <stage-id>
next_stage: <stage-id>
next_agent: <agent-slug>
revision_loop_count: <0 | 1 | 2>            # 2 = at the cap; no more 3'/4' loops permitted
checkpoint_required: true | false           # if true, hand off to checkpoint-coordination first
```

## How to orchestrate

1. **At each stage completion**, record the stage owner's deliverables in the work item, then determine `next_stage` from the contract above.
2. **Before any stage advance**, check whether the next transition crosses a checkpoint (10 decision-heavy + 2 integrity-gate acks — see the `checkpoint-coordination` skill for the canonical list). If so, enqueue `checkpoint-coordination` and pause.
3. **At Stage 3 outcome**, branch on the editorial decision: Accept → 4.5; Minor/Major → 3→4 Revision Coaching → 4; Reject → end pipeline (notify user, do not retry).
4. **At Stage 3' outcome**, branch: Accept/Minor → 4.5; Major → 3'→4' Residual Coaching → 4'.
5. **Enforce the cap**: if `revision_loop_count == 2` and the reviewer wants another round, escalate via `escalation-routing`. The pipeline does not silently loop.
6. **At any integrity gate FAIL** with retries exhausted, escalate via `escalation-routing`. Do not advance.

## Boundaries

- The CEO does not run any stage's skill — only marks the handoff and pings the next agent.
- Do not skip the integrity gates (2.5 / 4.5). Even at the user's request, surface the risk and require explicit override.
- Do not silently retry an integrity gate more than 3 times at 2.5 or any times at 4.5 — that's frame-lock by another name.
- If the user wants to inspect a stage's intermediate artifacts mid-pipeline, pause cleanly. Do not let the pipeline race ahead of the user.

## Output protocol

After each stage owner reports done, write a short orchestration note on the work item (current_stage, next_stage, next_agent, revision_loop_count) and tag the next agent. If a checkpoint is required, tag yourself with `checkpoint-coordination` instead and wait.
