# Handoff

This directory holds the Translator's 3-stage productization artifacts, one
subdirectory per research thread. The handoff package is the load-bearing artifact
that ships to the user: it takes a matured Technical Memorandum and walks it through
lab-model specification, pre-production design, and user-ready delivery. Each stage
is a distinct document that must exist and carry a witness signature before the next
stage can be authored. Stage 3 is the only artifact in the lab that is addressed
directly to the user as an owner; if it names "TBD" in the user-owner field, it
fails `make check`.

## Who writes here

- **The Translator** — exclusively, via the `handoff-document` skill. No other
  agent writes stage files. The Librarian may push citation suggestions to the
  Translator's queue but does not write into `handoff/`.

## Directory layout per thread

```
handoff/<thread-slug>/
    stage-1-lab-model.md
    stage-2-pre-production.md
    stage-3-handoff.md
```

- `<thread-slug>` is the kebab-case name of the research thread, matching the slug
  used in the relevant TMs (e.g., `handoff/surface-state-amplifier/`).
- Stage files are named exactly as above; no date prefix is used because the thread
  slug already scopes the directory.

## Stage requirements

| Stage | Document | Required before next |
|---|---|---|
| 1 | Lab-model spec — translates the TM's abstract result into an engineering model with named interfaces and assumptions. | Witness signature on stage-1 file. |
| 2 | Pre-production design — interfaces, tolerances, test fixtures, and integration contracts. | Witness signature on stage-2 file. |
| 3 | User-ready handoff — runbook, rollback procedure, acceptance criteria, named user-owner. | Stages 1 and 2 on file with valid witness signatures. |

Witness signatures follow the same format as TM witnesses: peer agent name, date,
and at least one sentence of structured critique.

## Anti-patterns

Two failure modes define the boundary between a real handoff and a repackaged memo.
First, **shipping stage 3 by reusing the TM body**: stage 3 must be authored
independently of the TM it derives from. Copying the TM's Abstract and Method
sections wholesale into `stage-3-handoff.md` and adding a runbook header is not
productization; it is transcription. The Translator's job is translation, which
requires the document to be restructured for a different audience with different
needs. Second, **eliding the rollback section because the artifact is read-only**:
every stage-3 document must include an explicit rollback procedure naming the steps
to reverse deployment, even if those steps are "restore the previous version from
`handoff/<thread-slug>/stage-2-pre-production.md`." The claim that the artifact is
read-only or cannot be rolled back is not an acceptable substitute; it is the kind
of reasoning that makes handoffs unsafe.
