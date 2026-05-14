# Memoranda

This directory holds the lab's primary output: dated, witnessed, sequentially numbered
Technical Memoranda. A TM is the canonical record of a completed research action —
theory, experiment, empirical probe, invention disclosure, or productization stage.
Each memo follows the structure Abstract → Problem → Prior TMs → Method → Result →
Open Questions, runs ≤10 pages, and carries two signatures: the author's and a peer
witness from another team who has read it and provided structured critique. The
sequential number is the lab's intellectual ledger. Every memo that advances a claim
cites at least one prior TM or Hallway entry; orphan claims — assertions with no
traceable lineage — are a `make check` violation.

## Who writes here

- **Every researcher** — via the shared `technical-memorandum` skill. The eight
  researcher roles (Theorist, Mathematician, Experimentalist, Materials/Empiricist,
  Inventor, Translator, Systems Engineer, Librarian) each produce TMs as the output
  of completed work cycles.
- **Subdirectory writers** are role-specific (see below).

## Filename pattern

Main memoranda:
```
TM-NNNN-<slug>.md
```
Regex: `TM-\d{4}-[a-z0-9-]+\.md`

- `NNNN` — zero-padded four-digit sequential counter, assigned in strict order.
  Do not skip numbers. Do not reuse numbers.
- `<slug>` — 2–5 word kebab-case summary of the memo's subject.

Examples:
- `TM-0001-shannon-noiseless-channel.md`
- `TM-0042-transistor-surface-state-hypothesis.md`

## Subdirectories

Four subdirectories hold role-specific structured artifacts that live alongside the
main TM sequence:

| Path | Filename | Skill | Author |
|---|---|---|---|
| `memoranda/budget/` | `YYYY-MM.md` | `patron-budget` | CEO |
| `memoranda/continuation/` | `YYYY-WW.md` | `continuation-review` | Director |
| `memoranda/monthly/` | `YYYY-MM-summary.md` | `monthly-summary` | CEO |
| `memoranda/disclosure/` | `DISC-NNNN-<slug>.md` | `invention-disclosure` | Inventor |

Disclosure files (`DISC-NNNN-<slug>.md`) use a parallel sequential counter and
must each name the TM that contains the paired research result.

## Anti-patterns

Two violations appear most often. First, **TMs without a peer witness countersignature**:
a TM authored and "signed" only by its own author is not a witnessed memo; it is a
draft. The witness signature block must name a specific peer agent from a different
team, include the date of their reading, and contain at least one sentence of
structured critique. A blank or placeholder witness line fails `make check`. Second,
**TMs that cite no prior TM or Hallway entry** (orphan claims): claiming a result
without any traceable lineage to prior lab work treats the TM as a standalone
assertion rather than a position in the lab's intellectual record. Every TM must
name at least one prior TM number or Hallway entry filename in its Prior TMs section,
even if the citation is only to say the claim is novel relative to prior work.
