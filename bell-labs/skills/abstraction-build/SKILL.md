---
slug: abstraction-build
name: Abstraction Build
description: Given a messy phenomenon or stuck experiment, propose the right invariant, reduction, or mathematical object. Outputs a Theory TM.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Abstraction Build

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Owned by the Theorist role.

## When to fire

A stuck experiment, a messy phenomenon, or a Hallway entry from the Bench team that smells like an unnamed invariant — for example, "the model fails for these inputs but not those; I can't characterize why." The Theorist does not wait for a clean, well-posed phenomenon. Messy data is normal. Shannon abstracted from messy crypto, not from a clean whiteboard problem.

Fire this skill whenever a pattern surfaces that has no name yet, or when a named pattern is failing to predict new observations. A good trigger is a Bench-team Hallway entry that uses the phrase "for some reason" or "we're not sure why" — that phrase is an unnamed invariant looking for a theorist.

## Inputs

- The originating phenomenon, as a TM or Hallway entry from any team. This is the primary input; do not proceed without reading it in full.
- Adjacent TMs from `memoranda/` that touch the same area — the Theorist pulls these during `hallway-traversal` before planning.
- The current `MISSION.md`, to confirm the proposed abstraction traces back to the lab's north-star problem. An abstraction with no traceable connection to the mission belongs on the Curiosity track, not the Directed track.

## Outputs

A Theory TM at `memoranda/TM-NNNN-abstraction-<slug>.md`, following the eight-section structure defined in `technical-memorandum`. The TM must:

- Propose a named invariant, reduction, or mathematical object.
- Cite the originating phenomenon in the **Prior TMs cited** section.
- Name the candidate abstractions that were considered and rejected, with one-sentence explanations of why each was set aside.
- State at least one testable consequence — an experiment the Experimentalist could run to disconfirm the proposed abstraction.

A Hallway entry is also posted when the TM is committed, summarizing the proposed abstraction in one sentence and linking to the new TM filename. The Hallway entry is the signal to the Librarian to push the TM to any researcher whose active thread touches the same phenomenon.

## Procedure

1. **Read the originating phenomenon in full.** Do not abstract from a summary or a one-line Hallway entry. The details that look like noise are often the load-bearing constraint. Read the adjacent TMs pulled during `hallway-traversal` before generating candidates — not after. Prior work constrains which candidates are genuinely new.

2. **Generate ≥2 candidate abstractions.** For each candidate, complete the sentence: *"This abstraction predicts X, which was not assumed in the originating phenomenon."* A candidate that cannot complete this sentence is a re-labeling, not an abstraction — set it aside without counting it as a candidate.

3. **For each viable candidate, state explicitly what new observation it would predict.** What does this abstraction tell us about the world that we did not already know from the originating phenomenon? Write this prediction down before evaluating the candidates; predictions written after evaluation are post-hoc stories.

4. **Select the candidate that predicts more than it was designed for.** Shannon's information theory was valuable not because it explained the one problem it was designed for, but because it explained cryptography, telegraphy, and noise with the same formula. Prefer the abstraction whose predictive surface extends beyond the originating phenomenon.

5. **Post a Hallway entry naming the proposed abstraction before writing the full TM.** A one-paragraph preview lets the Director and the Bench team see the abstraction early. If the Bench team immediately spots a disconfirming example, it is better to know before writing the full TM than after.

6. **Write the Theory TM.** Use the `technical-memorandum` skill for the full eight-section structure. In the **Method** section, include the list of candidate abstractions and the one-sentence reason each non-selected candidate was set aside. This is transparency about the search, not an appendix.

## Invariants

- **The chosen abstraction must have at least one testable consequence.** The consequence must be specific enough that the Experimentalist could design an experiment to attempt disconfirmation. "The model should perform better" is not a testable consequence; "on inputs where property P holds, error rate should fall below threshold T" is. The Theorist writes the testable consequence in the TM's **Open questions** section as an explicit invitation to the Experimentalist.

- **The originating phenomenon must be cited in Prior TMs.** The TM is not an independent contribution; it is a response to something. If no prior TM exists for the originating phenomenon, cite the Hallway entry that recorded it. A Theory TM with no Prior TMs entry fails `make check`.

- **Unsuccessful candidates must be named briefly.** The method section must record what was rejected and why. One sentence per rejected candidate is sufficient; more is encouraged if the rejection was non-obvious. Transparency about the search is not optional — it is what distinguishes a result from an assertion.

- **The abstraction must produce a TM, not just a Hallway entry.** An unnamed invariant captured only in the Hallway is not an abstraction; it is an observation. The abstraction becomes part of the lab's permanent record only when it is written as a witnessed TM.

## Anti-patterns

- **"Propose an abstraction with no testable consequence."** An untestable abstraction is a definition, not a theory. The Theorist's job is to narrow the space of possible worlds, not to rename the one we are in.

- **"Skip the originating phenomenon citation."** Every abstraction is a response to something. Failing to cite the origin severs the lineage and makes the TM an orphan claim that `make check` will reject.

- **"Claim novelty without naming what was rejected."** A theory that does not report its alternatives cannot be evaluated. The reader cannot tell whether the chosen abstraction was the obvious first idea or the survivor of a genuine search.

- **"Wait for a clean phenomenon before abstracting."** Waiting for clean data is waiting for data that will never arrive. Shannon did not wait for a clean information channel; he abstracted from the mess. Messy phenomena are normal inputs, not deferrals.

- **"Propose a candidate abstraction and immediately discard it without stating its predictive scope."** The procedure requires stating what each candidate predicts before selecting one. Discarding a candidate silently — without writing down what it would have predicted — means the search cannot be audited. Even rejected candidates contribute to the TM's credibility.

- **"Route the abstraction TM to the same Theorist or Mathematician for witness countersignature."** A Theorist's preferred witness is from a different team, per `technical-memorandum`. Getting a Bench or Network researcher to countersign an abstraction TM is not a convenience; it is the quality gate that catches abstractions that predict nothing observable.
