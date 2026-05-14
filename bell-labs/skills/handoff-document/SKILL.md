---
slug: handoff-document
name: Handoff Document
description: Three-stage productization enforced as one skill with three required stages — (1) lab-model spec, (2) pre-production design with interfaces and tolerances, (3) user-ready handoff with test fixtures, runbook, rollback. Cannot ship stage 3 without stages 1 and 2 on file.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Handoff Document

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Owned by the Translator role.

## When to fire

Fire when a Director continuation review has explicitly marked a thread as *candidate for Translator handoff*. That review note is the required trigger; the Translator does not self-select threads for handoff. The Director's marking means: the research is mature enough that the boundary between lab and user is now the primary concern.

Do not fire based on a TM being "done" — maturity for research purposes and maturity for handoff purposes are different judgments. The Director makes the second judgment.

## Inputs

- All matured TMs in the thread, read in full. The Translator must understand the artifact at lab depth before writing a user-facing description.
- The disclosure from `invention-disclosure` if one exists in `memoranda/disclosure/`.
- The user's `MISSION.md` at the company root. Stage 3 must connect the artifact back to the declared mission; the user-owner named in stage 3 should be consistent with the mission's named stakeholders.

## Outputs

Three files under `handoff/<thread-slug>/`, each requiring a peer-signed witness before the next stage begins:

- `handoff/<thread-slug>/stage-1-lab-model.md`
- `handoff/<thread-slug>/stage-2-pre-production.md`
- `handoff/<thread-slug>/stage-3-handoff.md`

The `<thread-slug>` matches the thread's slug as recorded in the Director's continuation-review note.

## Procedure

### Stage 1: `stage-1-lab-model.md`

Write for a technically sophisticated reader who was not on the research thread. Sections:

1. **Lab-model summary** — one paragraph: what the artifact is, what problem it addresses, what the key insight is.
2. **Originating TMs cited** — a list of every TM in the thread, by filename and title. No orphan artifacts.
3. **What the artifact is** — file, running service, document, algorithm, trained model, or other. Be specific; "a solution" is not a type.
4. **Demonstrated behavior** — what the artifact actually does, as observed in the experiments. Cite the TMs where behavior was demonstrated.
5. **Known limitations** — what the artifact cannot do, what conditions it has not been tested under, what assumptions it carries. Honest enumeration here prevents stage 3 from surprising the user.

Commit `stage-1-lab-model.md`. Route to a peer (not the Translator) for witness sign-off. The witness reads the full file and countersigns with structured critique. **Stage 2 cannot begin until stage 1 is witness-signed.**

### Stage 2: `stage-2-pre-production.md`

Write for an engineer who will integrate or deploy the artifact. Sections:

1. **External interfaces** — API surface, file formats, environment variables, configuration schema. List every interface. If there are none, state that explicitly and explain why.
2. **Tolerances and edge cases** — input ranges, error conditions, concurrency assumptions, load limits. What happens at the boundary?
3. **Failure modes** — what breaks, how it breaks, what the observable symptom is, and whether failure is recoverable or fatal.
4. **What is not covered** — explicitly name what this pre-production spec does not address. This section prevents the user from assuming completeness.

Commit `stage-2-pre-production.md`. Route to a peer for witness sign-off. **Stage 3 cannot begin until stage 2 is witness-signed.**

### Stage 3: `stage-3-handoff.md`

Write for the named user-owner — the person at the user's end who will own this artifact post-handoff. Sections:

1. **User-facing summary** — what this artifact does, in plain language, without lab jargon. One to two paragraphs.
2. **Test fixtures** — concrete, runnable tests that the user-owner can execute to verify the artifact is working. Not descriptions of tests; actual fixtures (commands, inputs, expected outputs, pass criteria).
3. **Runbook** — step-by-step operations: how to start it, how to stop it, how to update it, how to check that it is healthy.
4. **Rollback procedure** — what the user-owner does if they want to stop using this artifact or revert to a previous state. Write this even if the artifact is read-only: "stop using it" is a procedure that requires steps.
5. **Named user-owner** — the specific person (name and role) at the user's end who owns this artifact post-handoff. "TBD" fails check.

Commit `stage-3-handoff.md`. Route to a peer for witness sign-off.

## Invariants

- `handoff/<thread>/stage-3-handoff.md` is rejected by `make check` if stages 1 and 2 are not both present and witness-signed in the same directory.
- The Translator cannot witness their own stages. Route to a peer on a different team for each stage.
- Stage 3 must name a specific user-owner by name and role. "TBD" fails check; so does "the user" or "the stakeholder."
- Each stage's witness block follows the TM witness convention: peer name, date, one-sentence-minimum structured critique.
- Stage 2 cannot begin before stage 1 is signed. Stage 3 cannot begin before stage 2 is signed. This sequencing is enforced, not advisory.

## Anti-patterns

- **"Ship stage 3 by reusing the TM body."** The three stages serve different audiences. A TM is written for the lab; stage 3 is written for the user-owner. Reusing TM prose produces a stage 3 that the user cannot act on.

- **"Elide the rollback procedure because the artifact is read-only."** Write the rollback anyway. The question "what does the user do if they want to stop using this?" always has an answer. "Delete the file" is a rollback procedure; write it.

- **"Skip stage 2 because the interfaces are obvious."** Write them down. The act of writing surfaces assumptions about what is obvious. What is obvious to the Translator after weeks on the thread is not obvious to the engineer who encounters the artifact six months later.

- **"Translator witnesses own stage."** Forbidden. Route each stage to a peer on a different team.

- **"Name user-owner as 'TBD'."** Forbidden. If the user-owner is genuinely unknown, escalate to the Director before writing stage 3. A stage 3 without a named owner has no one responsible for its post-handoff health.

- **"Collapse the three stages into one document."** The three-stage structure forces three distinct audiences and three distinct peer reviews. Collapsing them into one document collapses the quality gates. This is the failure mode every Bell Labs imitator commits; do not commit it.
