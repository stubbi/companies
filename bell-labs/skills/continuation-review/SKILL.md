---
slug: continuation-review
name: Continuation Review
description: Weekly review with the CEO — which threads continue, which need a math consult, which are candidates for the Translator, which are at risk. Read-only on curiosity threads.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Continuation Review

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Owned by the Director of Research role.

## When to fire

Weekly, jointly with the CEO. Run after the weekly Colloquium entries are posted and before the Director posts any instigation questions for the new cycle. The review informs what instigations and budget adjustments make sense this week.

Do not skip a week because the thread list appears unchanged. The review is a deliberate act, not a monitoring task — its value is in the joint reading, not the diff.

## Inputs

- The active-thread list from the CEO's most recent `patron-budget` artifact at `memoranda/budget/YYYY-MM.md`. This is the canonical thread list for the review; do not add threads not in the budget.
- All Colloquium entries for the current week at `colloquium/YYYY-WW.md`.
- The Director's walk notes from the past week (`hallway/YYYY-MM-DD-director-walk.md` for each day of the current cycle).
- Optional: open instigation memos from the current cycle (`instigation/`) to note any that received responses.

## Outputs

A continuation memo at `memoranda/continuation/YYYY-WW.md` (ISO week number of the review date). The memo records, for each Directed thread in the budget:

- **Status:** progressing / stalled / at risk / ready for handoff.
- **Budget note:** cycles consumed vs. budget named in `memoranda/budget/YYYY-MM.md`.
- **Recommendation:** one of — continue as-is | pivot (name the proposed change) | route to Mathematician for a math-consultancy pull | handoff to Translator | recommend sunset (does not execute sunset; defers to `project-sunset` skill).

The memo ends with a **summary line** signed jointly: "Director of Research and CEO, YYYY-MM-DD."

## Procedure

1. **Walk the Directed threads with the CEO.** For each thread named in the active `patron-budget`, read the Colloquium entry, the relevant walk-note references, and any instigation responses from this week.

2. **For each thread, note progress vs. budget.** "Progress" means at least one new Hallway entry, one new TM draft, or a clear blocker named (a named blocker is progress — it means the researcher is not spinning). Silence across all three is the stall signal.

3. **Flag candidates for specialist routing:**
   - **Mathematician consult:** the thread has an open formalization question that is blocking progress and the Theorist has not resolved it in two cycles. Name the specific open question.
   - **Translator handoff:** the thread has a matured TM (signed + witnessed) and a user-ready embodiment is plausible within one or two more cycles. Name the TM.
   - **Sunset candidate:** the thread has consumed more than its named budget without producing a witnessed TM or a named open question that justifies continued spend. Flag as a recommendation — do not execute.

4. **Do not name Curiosity threads in this artifact.** Curiosity threads are not in the `patron-budget` and are not reviewed at this layer. If a Curiosity thread appears to have matured into something a researcher wants to bring to Directed, that is the researcher's own promotion — it does not enter the continuation review uninvited.

5. **Write the continuation memo to `memoranda/continuation/YYYY-WW.md`.** One entry per Directed thread. Status, budget note, recommendation. End with the joint sign-off line.

## Invariants

- **No Curiosity thread appears by name in this artifact.** The continuation review operates over the Directed budget only. Naming a Curiosity thread here — even approvingly — breaches the two-track protection and must not be done.

- **Sunset is recommended here, not executed.** The continuation memo may flag a thread as a sunset candidate. The actual sunset memo is produced only by the `project-sunset` skill, which has its own inputs, structure, and sign-off. A recommendation in the continuation memo does not substitute for the sunset memo.

- **The Director does not override the CEO's budget.** The Director proposes — the recommendation column of the continuation memo is advisory. If the CEO disagrees with a recommendation, the CEO's view prevails and the Director notes the disagreement in the memo. The Director never unilaterally reassigns or terminates a thread named in the `patron-budget`.

- **Do not skip a week because nothing changed.** A week where every thread is "continue as-is" still produces a memo. "No changes recommended" is a valid and expected outcome; the memo is the record that the review happened.

## Anti-patterns

- **"Name a Curiosity thread by name in the continuation memo."** Even a positive mention ("the Theorist's curiosity thread on X looks exciting") introduces a review layer over protected work. The memo is silent on Curiosity.

- **"Sunset a thread inline in the continuation review without a `project-sunset` memo."** Writing "thread X is hereby closed" in the continuation memo is not a sunset — it is an erasure. The sunset memo is what makes closing a thread safe; it cannot be skipped.

- **"Override a CEO budget decision unilaterally."** If the CEO budgeted three more cycles for a stalled thread and the Director disagrees, the Director records the disagreement in the memo and stops there. The CEO decides.

- **"Skip a week because nothing changed."** The weekly cadence is not contingent on change. The review is an act of deliberate attention, not a change-detection trigger.
