---
slug: technical-memorandum
name: Technical Memorandum
description: Canonical output. Dated, signed, witness-countersigned by a peer agent. Abstract → problem → prior TMs → method → result → open questions. ≤10 pages.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Technical Memorandum

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Shared researcher core skill — referenced by every researcher agent.

## When to fire

Any time a researcher produces a result worth recording. The default is *always* — write a TM whenever a cycle produces a conclusion, a negative finding, a working prototype, a partial result, or a reframing of a prior question. The cost of writing a TM is lower than the cost of an orphan claim floating in the Hallway or a researcher's head.

A "result worth recording" includes: a confirmed or refuted hypothesis; a working or broken implementation; a mathematical derivation; a literature summary with a new synthesis; a failed experiment with a clear explanation of why. If in doubt, write the TM.

Half-results that are not yet ready for a witnessed record go to the Hallway instead. A half-result that survives two more cycles becomes a TM regardless.

## Inputs

- The result itself: data, code, derivation, conclusion, or partial finding.
- Prior TMs from `memoranda/` that motivated or are superseded by this work. At least one prior TM or Hallway entry must be cited; see Invariants.
- The researcher's own Hallway entries from the current cycle — these form the living context for the Abstract.
- The current `MISSION.md`, to confirm the TM traces back to the north-star problem.

## Outputs

A file at `memoranda/TM-NNNN-<slug>.md` where `NNNN` is the next sequential 4-digit integer (zero-padded: `TM-0001`, `TM-0042`, etc.) and `<slug>` is a 2–5 word kebab-case summary of the subject.

The file contains the following required sections in order:

1. **Title** — the TM's full title, the date (ISO 8601), and the author's role name.
2. **Witness** — the peer countersignature block (see Procedure). Must be non-empty before the TM is committed to `memoranda/`.
3. **Abstract** — ≤200 words. The single-paragraph answer to "what is this TM about and what did you find?"
4. **Problem** — the question or gap this TM addresses. One to three paragraphs.
5. **Prior TMs cited** — a list of `TM-NNNN` references and/or Hallway entry filenames. ≥1 required. Can include the researcher's own prior TMs.
6. **Method** — what the researcher did: the experiment, derivation, search strategy, or construction procedure.
7. **Result** — what was found, including negative or partial results. Do not suppress null results.
8. **Open questions** — things this TM does not settle. Every TM has open questions; that is the whole point of writing things down.

## Procedure

1. **Draft the TM** with all eight sections populated. The Witness block should be marked `[pending countersignature]` at this stage. Do not leave any section empty, including Open questions.

2. **Choose a peer agent for the witness countersignature.** Default rule: choose a researcher from a *different team*. A Theorist's witness is preferentially a Bench or Network researcher, not the Mathematician (same team). An Experimentalist's witness is preferentially a Theory or Invention researcher. The Director can override this default during continuation review by naming a specific witness.

3. **Send the draft to the chosen peer.** The peer reads the draft in full and returns a structured critique with exactly these four required fields:
   - *Claim under examination* — restate, in the peer's own words, the central claim of the TM.
   - *What I would do differently* — one or more methodological suggestions.
   - *What I think is wrong* — identify gaps, errors, or over-interpretations. This field must be populated; "nothing is wrong" is not a valid entry — the peer must at least identify the weakest link.
   - *Sign or refuse-to-sign* — either `SIGNED` or `REFUSED: <one-sentence reason>`.

4. **On `REFUSED`:** the author incorporates the critique, updates the draft, and resubmits to the same peer. After three refusals on the same TM, escalate to the Director: write a one-paragraph escalation note at `instigation/YYYY-MM-DD-<author>-tm-dispute-<slug>.md` and wait for Director guidance before proceeding.

5. **On `SIGNED`:** fill in the Witness block with the peer's role name, the date of signing, and the structured critique verbatim. Commit the TM to `memoranda/`. Post a short Hallway entry noting the new TM's filename and one-sentence summary.

## Invariants

- **The Witness block must be non-empty.** The block must contain the peer's role name, the countersignature date, and the structured critique verbatim (all four fields). A TM with an empty or `[pending countersignature]` Witness block may not be committed to `memoranda/`. Enforced by `make check`.

- **Prior TMs cited must list ≥1 prior TM or Hallway entry — no orphan claims.** Every TM must trace its lineage. If no prior TM exists, cite the Hallway entry that motivated the work. A TM with an empty Prior TMs section fails `make check`.

- **TM filename matches `TM-\d{4}-[a-z0-9-]+\.md`.** The four-digit zero-padded sequence number is mandatory. Files that do not match this pattern are not recognized by `make check` as valid memoranda.

- **Author cannot witness their own TM.** Self-witness is unconditionally forbidden. The peer listed in the Witness block must be a different agent than the author listed in the Title. Enforced by `make check`.

## Anti-patterns

- **"Self-witness."** The author counter-signs their own TM to move faster. Forbidden; `make check` will catch it. If no peer is available, escalate to the Director — do not forge the witness.

- **"Refuse-to-sign loop > 3 attempts."** Three refusals on the same TM indicates a substantive dispute that the author and peer cannot resolve alone. Escalate to the Director; do not keep cycling indefinitely with the same peer.

- **"TM with empty Open questions."** A TM that claims to have no open questions is either the end of all science or a sign the author stopped thinking. Every TM has open questions; populate the section honestly.

- **"Skip the Witness block to move faster."** An unwitnessed TM is not a TM; it is a Hallway entry that overestimates itself. The witnessing step exists precisely because it is inconvenient — that friction is the quality gate.

- **"Cite TMs that don't exist."** References to `TM-NNNN` identifiers that do not correspond to actual files in `memoranda/` are fabrications. Check that cited TMs exist before committing.

- **"Suppress null results."** A negative finding is a result. A TM that reports a failed experiment with a clear explanation of why is more valuable than silence. Write the TM.
