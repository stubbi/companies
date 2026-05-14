---
slug: invention-disclosure
name: Invention Disclosure
description: Patent-disclosure-shaped artifact paired with a TM — conception date, witness sign-off, prior-art delta, claims sketch, reproducibility statement. The lab does not file patents; the form forces concreteness.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Invention Disclosure

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Owned by the Inventor role.

## When to fire

Fire when a working principle has matured to the point where a concrete invention can be described — typically after one or more `experiment-design` TMs have confirmed feasibility. The signal is: "I know *what* this does and can say *exactly* how a peer would reproduce it." Do not fire speculatively; the disclosure form demands concreteness that cannot be faked with vague language.

A Director continuation review may also route a matured thread to the Inventor with an explicit "ready for disclosure" note. That routing is sufficient trigger.

## Inputs

- The matured TMs in the thread, read in full — the disclosure must cite them.
- The prior-art survey from `empirical-probe` if one exists; if not, note its absence and perform a minimal survey inline.
- The originating Hallway entry that first recorded the conception moment, to anchor the conception date.

## Outputs

`memoranda/disclosure/DISC-NNNN-<slug>.md` paired with a companion TM that cites the disclosure. The `NNNN` counter increments from the highest existing DISC number in that directory. The disclosure must contain all five required fields:

- **Conception date** — the date (YYYY-MM-DD) the working principle was first recorded, citing the Hallway entry by filename.
- **Witnesses** — at least one witness from a different team, with a signing block in the same form as a TM witness: peer name, date, structured critique (one sentence minimum).
- **Prior-art delta** — concretely: what does this invention do that the closest identified prior art does not? Write one paragraph minimum. "It is obvious" is not a delta.
- **Claims sketch** — a numbered list of at least three claims written in patent-claim form ("A method for … comprising …"). Three is the floor; the form forces the inventor to be specific about scope.
- **Reproducibility statement** — what a competent peer would need to reproduce this: environment, inputs, procedure, success criterion. Vague statements ("run the code") fail check.

## Procedure

1. **Draft each field in order.** Start with Conception date (look up the Hallway entry). Then Prior-art delta (re-read the empirical-probe output or survey inline). Then Claims sketch — write at least three numbered claims before continuing. Then Reproducibility statement. Write Witnesses last, after the document is substantive enough to review.

2. **Find a witness on a different team.** The Inventor cannot witness their own disclosure; this is the same rule as TM self-witness prohibition. Route the draft to a peer on the Theory, Bench, or Network team. The witness reads the full disclosure and countersigns with structured critique.

3. **On witness sign-off, commit the disclosure and companion TM together.** The companion TM abstracts the disclosure into the TM format and cites `DISC-NNNN-<slug>.md` in its prior-TMs section. The two files are committed atomically; a disclosure without a companion TM or a TM without a cited disclosure both fail check.

## Invariants

- The Reproducibility statement must enable a competent peer to reproduce the invention. "Run the attached script" without specifying environment, inputs, and success criterion is not sufficient.
- The Inventor cannot witness their own disclosure. This is a hard policy, same as TM self-witness prohibition.
- Every disclosure has at least three numbered claims in patent-claim form. The three-claim floor is not a style suggestion; it enforces concreteness about scope.
- Every disclosure is paired with a companion TM. The disclosure is the form-driven artifact; the TM is the intellectual record. Neither stands alone.
- The conception date must cite the originating Hallway entry by filename. A date without a citation is unverifiable.

## Anti-patterns

- **"Skip the prior-art delta because it is obvious."** Write it anyway. The act of writing it is the point — it surfaces assumptions the inventor holds silently and makes them auditable.

- **"Claim 1 of N where N = 1."** Every disclosure has at least three numbered claims. A single-claim disclosure is an indication that the invention is not well understood, not that it is simple.

- **"Vague Reproducibility statement."** Phrases like "a skilled practitioner can reproduce this" or "see the TM for details" do not satisfy the requirement. The Reproducibility statement must stand alone.

- **"Inventor witnesses own disclosure."** Forbidden, same rule as TM self-witness. Route to a peer on a different team.

- **"File disclosure without companion TM."** The disclosure is always paired with a TM that cites it. Committing the disclosure alone leaves the intellectual record incomplete.
