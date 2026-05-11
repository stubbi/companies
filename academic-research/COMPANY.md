---
schema: agentcompanies/v1
slug: academic-research
name: Academic Research
description: 5-agent research-paper company — research, write, review, revise, finalize
  — driven by the ARS pipeline. CEO handles intake and orchestrates the linear stage
  handoffs and user-confirmation checkpoints. Ported from Imbad0202/academic-research-skills
  into the Agent Companies format.
version: 0.1.0
license: CC-BY-NC-4.0
authors:
- name: Jannes Stubbemann
  email: jannes@paperclip.inc
goals:
- Draft full academic papers (research → write → review → revise → finalize) for human
  researcher review.
- Enforce ARS's two integrity gates (2.5 + 4.5) and the 7-mode AI failure checklist
  before any output is finalized.
- Stage every output for human sign-off — no agent here submits to a journal, signs
  an authorship statement, or makes editorial decisions on the user's behalf.
tags:
- research
- academic
- papers
- literature-review
- peer-review
- non-commercial
metadata:
  upstream:
    repo: Imbad0202/academic-research-skills
    commit: 58dad474572ea63ca7f204d582632acc413a0efd
    license: CC-BY-NC-4.0
  affiliation: Community port. Not affiliated with or endorsed by Imbad0202 or the
    ARS authors.
  usage_restriction: 'Non-commercial use only. Upstream is licensed CC BY-NC 4.0;
    this port preserves

    that restriction. You may use it for personal research, academic work, and

    non-commercial collaboration. You may not use it as part of a commercial

    service, paid offering, or to produce work-for-hire.'
---
# Academic Research

5-agent research-paper company — research, write, review, revise, finalize — driven by the ARS pipeline. CEO handles intake and orchestrates the linear stage handoffs and user-confirmation checkpoints. Ported from Imbad0202/academic-research-skills into the Agent Companies format.

## Usage restriction

Non-commercial use only. Upstream is licensed CC BY-NC 4.0; this port preserves
that restriction. You may use it for personal research, academic work, and
non-commercial collaboration. You may not use it as part of a commercial
service, paid offering, or to produce work-for-hire.

## Boundaries

Nothing in this package constitutes peer-reviewed scholarship on its own. These agents draft research artifacts (literature searches, methodology blueprints, outlines, drafts, review reports, revision plans, formatted manuscripts) for review by a qualified human researcher. They do not submit to journals, sign authorship statements, make editorial decisions, or attest to research integrity on the user's behalf; every output is staged for human sign-off. The pipeline's integrity gates (2.5 / 4.5) and the 7-mode AI failure checklist are mandatory and not skippable.

## Teams

- **Research** (`teams/research/TEAM.md`) — Stage 1 — literature search, methodology blueprint, annotated bibliography, synthesis, devil's-advocate review.
- **Writing & Revision** (`teams/writing/TEAM.md`) — Stages 2 / 4 / 4' / 5 — outline, draft, revise after review, re-revise, and finalize to MD/DOCX/LaTeX/PDF.
- **Review** (`teams/review/TEAM.md`) — Stages 3 / 3' — first-round review (EIC + 3 reviewers + devil's advocate) and verification re-review with R&R traceability.
- **Integrity & Pipeline** (`teams/integrity/TEAM.md`) — Stages 2.5 / 4.5 / 6 — 7-mode AI failure checklist, claim verification, Material Passport, and process summary.

