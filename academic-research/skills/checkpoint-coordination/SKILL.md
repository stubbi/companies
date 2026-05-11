---
slug: checkpoint-coordination
name: Checkpoint Coordination
description: Surface ARS's 10 decision-heavy checkpoints + 2 integrity-gate acknowledgements as user-facing prompts; do not advance without explicit confirmation.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Checkpoint Coordination

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream `Imbad0202/academic-research-skills`. Owned by the CEO role.

## When to fire

Whenever `pipeline-orchestration` flags `checkpoint_required: true` for the next stage transition. Holds the pipeline at a clean boundary until the user confirms.

## Checkpoint catalog

ARS defines two classes of checkpoint. **Both** require user confirmation before the pipeline advances.

### Decision-heavy checkpoints (10 — user chooses a branch)

| # | Stage | What the user decides |
|---|---|---|
| 1 | 1. RESEARCH | RQ Brief + Methodology Blueprint |
| 2 | 2. WRITE | Outline approval before drafting |
| 3 | 3. REVIEW | Editorial decision (Accept / Minor / Major / Reject) |
| 4 | 3 → 4 Revision Coaching | Revision strategy (≤ 8 Socratic rounds; may skip) |
| 5 | 4. REVISE | Revision changes confirmed |
| 6 | 3'. RE-REVIEW | Verification-review decision |
| 7 | 3' → 4' Residual Coaching | Residual-issue trade-offs (≤ 5 Socratic rounds; may skip) |
| 8 | 4'. RE-REVISE | Content frozen — no further review loop |
| 9 | 5. FINALIZE | Output format selection (MD / DOCX / LaTeX / PDF) |
| 10 | 6. PROCESS SUMMARY | Language confirmation + collaboration quality review |

### Integrity-gate acknowledgements (2 — user acknowledges a machine report)

| # | Stage | What the user acknowledges |
|---|---|---|
| ✓ 1 | 2.5 INTEGRITY | Integrity Report PASS/FAIL + any SUSPECTED flags |
| ✓ 2 | 4.5 FINAL INTEGRITY | Final Integrity Report PASS + populated Material Passport |

## How to coordinate

1. **Surface the artifacts** the user needs to evaluate. For decision-heavy checkpoints, show what's being approved (RQ brief, outline, decision letter, format choice). For integrity acks, show the machine report verbatim.
2. **State the branches** explicitly. "Accept this RQ to proceed to Stage 2, or revise it for another Stage 1 pass." Don't bury the choice in prose.
3. **Wait for an explicit signal.** Confirmation must be unambiguous ("approve", "yes, proceed", a chosen format). Silence is not consent. Vague acknowledgements ("looks fine I guess") get a clarifying re-prompt.
4. **Surface the Socratic skip explicitly** at checkpoints 4 and 7. The user should know they can engage in dialogue *or* say "just fix it" to skip — both are valid.
5. **Record the decision** in the work item (what was approved, by whom, when, against which artifact version). Pipeline-orchestration consumes this to advance.

## Boundaries

- Do not advance the pipeline on inferred consent. Never on silence.
- Do not summarise integrity reports — show them verbatim. Summaries hide SUSPECTED flags.
- If the user pushes back on an integrity gate FAIL, do not override. Escalate via `escalation-routing`.
- At checkpoint 10 (Stage 6), the user reviews collaboration quality — do not minimise or spin the AI Self-Reflection Report.

## Output protocol

Write the checkpoint outcome as a structured note: `{checkpoint: <#>, stage: <stage-id>, decision: <user's choice>, artifact_version: <hash or rev>, confirmed_at: <ISO timestamp>}`. Then re-enqueue `pipeline-orchestration` to advance to the next stage.
