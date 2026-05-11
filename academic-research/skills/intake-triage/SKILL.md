---
slug: intake-triage
name: Intake Triage
description: Classify an incoming research request and route to the correct ARS pipeline mode.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Intake Triage

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream `Imbad0202/academic-research-skills`. Owned by the CEO role.

## When to fire

The first skill the CEO runs on any new research request. Decides which ARS pipeline mode to invoke and which stage owner picks up first.

## Inputs

- The raw request: a research question, a "review this draft", a "do a literature search on X", a "format this paper for venue Y", a manuscript file.
- Optional context: target venue, deadline, existing materials (RQ brief, draft, prior reviews, literature corpus), discipline.

## Outputs

A triage decision recorded as a short note on the request:

```yaml
mode: full | lit-review-only | revision-only | fact-check | format-only | abstract-only
primary_agent: researcher | writer | reviewer | integrity-officer
entry_stage: 1 | 2 | 3 | 4 | 5
boundaries: [<note>, ...]                # call out anything that requires human sign-off
literature_corpus_present: true | false  # triggers v3.6.5 corpus-first flow if true
target_venue: <ICLR | NeurIPS | Nature | Science | ACL | EMNLP | other | none>
deadline: <ISO date or "best-effort">
```

## How to triage (decision tree)

1. **Does the user have a research question but no draft?** → `mode: full`, `entry_stage: 1`, `primary_agent: researcher`. Full pipeline (1 → 2 → 2.5 → 3 → 4 → 4.5 → 5 → 6).
2. **Does the user only want a literature review?** → `mode: lit-review-only`, `entry_stage: 1`, `primary_agent: researcher`. Stops after Stage 1 deliverables.
3. **Does the user have a draft + reviewer comments?** → `mode: revision-only`, `entry_stage: 4`, `primary_agent: writer`. Skips Stage 1-3 if RQ + methodology are settled.
4. **Does the user want claims fact-checked?** → `mode: fact-check`, `entry_stage: 2.5`, `primary_agent: integrity-officer`. Runs the integrity gate against an existing draft.
5. **Does the user want format conversion only?** → `mode: format-only`, `entry_stage: 5`, `primary_agent: writer`. Pandoc/tectonic render with venue disclosure.
6. **Does the user want an abstract written from a draft?** → `mode: abstract-only`, `entry_stage: 2`, `primary_agent: writer`. Bilingual-abstract sub-mode.

## Boundaries

- The CEO does not perform the triaged work — only routes it.
- If the request is ambiguous about target venue or methodology, ask the user one clarifying question rather than guessing. The wrong methodology choice cascades through every later stage.
- Authorship questions (whose name on the paper, whose contribution counts) always escalate to a human. Never attempt to resolve them inside the pipeline.
- If the request mentions a deadline tighter than ARS's typical end-to-end runtime for the chosen mode, surface that explicitly so the user can scope down before Stage 1.

## Output protocol

Write the triage decision as a comment / note on the work item, and tag the primary agent for pickup. Then enqueue `pipeline-orchestration` on yourself before the specialist starts so the stage handoffs are tracked.
