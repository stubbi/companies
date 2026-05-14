---
slug: experiment-design
name: Experiment Design
description: Turn a question into a falsifiable experiment (code, simulation, ablation, controlled test). Pre-register the prediction in a Hallway entry before running; result becomes a TM regardless of outcome.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Experiment Design

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Owned by the Experimentalist role.

## When to fire

A question is concrete enough to falsify — someone can state what observation would prove it wrong. Typical triggers: a Theorist TM that names a testable consequence ("error rate should fall below threshold T on inputs where property P holds"), a Hallway entry asking "does this actually generalize?", or a Director instigation that crystallizes a bench question. Do not fire on vague questions ("see what happens"); those must be sharpened first. A question that cannot be pre-registered cannot be experimented on under this skill.

## Inputs

- The question to falsify, stated as a single sentence. Must include a measurable quantity and a direction (e.g. "model accuracy on X drops by ≥5% when Y is varied").
- Any prior TMs or Hallway entries that motivated the question (the Theorist's TM, a Bench Hallway note, a Director instigation entry).
- The current `MISSION.md`, to confirm the experiment is on-mission.

## Outputs

Two artifacts, in order:

1. **Pre-registration Hallway entry** at `hallway/YYYY-MM-DD-experimentalist-prereg-<slug>.md` — written *before* running the experiment. Contains the prediction and the kill criterion. Immutable after the experiment runs.
2. **Experiment TM** at `memoranda/TM-NNNN-experiment-<slug>.md` — written after running. Contains the method, the result, and an explicit verdict on the kill criterion. Cites the pre-registration entry in **Prior TMs cited**.

## Procedure

1. **State the prediction precisely.** Complete the sentence: *"I predict that [measurable quantity] will [change / stay / exceed] by [specific amount] when [variable] is [changed to / held at]."* Vague predictions ("performance should improve") fail this step. If the question cannot be stated in this form, stop and post a Hallway entry asking the Theorist to sharpen it.

2. **State the kill criterion.** Name the specific observation that would falsify the prediction: *"If [quantity] does not [change] by at least [threshold], the prediction is not supported."* The kill criterion must be specific enough that running the experiment can give a binary answer: supported / not supported / inconclusive (when measurement error prevents a clear reading).

3. **Post the pre-registration Hallway entry.** Timestamp it. The entry records the prediction and the kill criterion verbatim. Once the experiment runs, this entry is immutable — do not edit it to match the result, do not delete it if the result is negative.

4. **Run the experiment.** In an agentic context, this is: write the code, run the simulation, perform the ablation, or execute the controlled test. Keep the setup description precise enough that a peer could reproduce it — input data, model version, random seed, hardware, software versions. If setup must deviate from the pre-registration during execution, document the deviation in the TM; do not revise the pre-registration.

5. **Write the Experiment TM.** Use the `technical-memorandum` skill for the full eight-section structure. In the **Result** section, report the kill criterion outcome explicitly: *predicted* (the observation matched the prediction), *not predicted* (the observation falsified it), or *inconclusive* (measurement error or setup issue prevented a clear reading). Cite the pre-registration Hallway entry by filename in **Prior TMs cited**. A failed prediction is a complete result — write the TM with the same care as a successful one.

## Invariants

- **The TM's Prior TMs cited section must cite the pre-registration Hallway entry.** An Experiment TM with no pre-registration citation fails `make check` and is treated as a retrospective hypothesis.

- **The kill criterion must be specific enough to produce a binary answer.** "Model performance is better" is not a kill criterion. "F1 on held-out set exceeds 0.82" is. The Experimentalist is responsible for ensuring the criterion is measurable before posting the pre-registration.

- **Failure TMs are the highest-value TMs.** A "not predicted" result is not a failure of the Experimentalist — it is the most informative outcome the lab can produce. It eliminates a hypothesis, focuses the Theorist's attention, and is the result Bell Labs is most famous for not suppressing. Skip the failure TM and you have destroyed the lab's most valuable output.

- **The pre-registration is immutable post-run.** Do not edit the Hallway entry after the experiment begins. Deviations from the protocol belong in the TM, not in a rewritten pre-registration.

## Anti-patterns

- **"Retrospective hypothesis"** — writing the prediction after observing the result. Pre-registration exists precisely to prevent this. The timestamp on the Hallway entry is the evidence the prediction was written first.

- **"Soft kill criterion like 'see what happens'."** If the kill criterion cannot be evaluated as binary, the experiment cannot falsify anything. Post a sharpened kill criterion or escalate to the Theorist.

- **"Skip the TM when the experiment failed."** Failure TMs are the highest-value TMs. An undocumented negative result forces the next researcher to repeat the experiment. A documented negative result is a citation.

- **"Modify the pre-registration after running."** The pre-registration's value comes entirely from its immutability. Retroactively correcting it turns the entire record into post-hoc rationalization.

- **"Run the experiment without a pre-registration entry."** The experiment may still yield a result, but the result is scientifically worthless as a confirmation — it cannot be distinguished from data-dredging. Post the pre-registration first, no exceptions.
