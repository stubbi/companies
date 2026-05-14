---
slug: intake-triage
name: Intake Triage
description: Classify a new user request as on-mission, off-mission, or curiosity-seed; route to a team's directed queue or surface to the Director.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Intake Triage

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Owned by the CEO role.

## When to fire

Every incoming user message that is not a pure status query ("what's the lab working on?", "show me the monthly summary") triggers this skill. The CEO runs intake-triage before any other action. The result determines whether and how the message enters the lab's work queue.

A "pure status query" is one that requests information already recorded in artifacts the CEO can read and relay directly. Any message that implies a new problem, a new direction, a new task, or a challenge to the current mission is an intake event.

## Inputs

- The raw user message, in full.
- The current `MISSION.md` at the company root. This is the canonical fence; do not triage without reading it.
- Optional: current state of team queues (`agents/<role>/queue.md`) to assess capacity before routing.

## Outputs

A triage decision recorded as a Hallway entry at `hallway/YYYY-MM-DD-ceo-intake-<slug>.md`, where `<slug>` is a 2–4 word kebab-case summary of the request. The entry records:

- **Classification:** `on-mission` | `off-mission` | `curiosity-seed` | `status`
- **Routing decision:** which team's directed queue receives the work item, or "surface to Director as candidate instigation," or "no routing — reply to user."
- **Rationale:** one sentence citing the specific part of `MISSION.md` that supports the classification.

If the request is `off-mission`, the Hallway entry also records the reply sent to the user and whether the user was asked to update `MISSION.md` or defer the request.

## Procedure

1. **Read `MISSION.md` in full** before classifying. Do not triage from memory. The mission may have been revised since the last intake. The north-star problem section and the "what counts as improving the network" section are the primary classification anchors.

2. **Classify the request:**
   - **On-mission:** the request asks for work that directly advances the north-star problem or a named thread within it. Route to the appropriate team's `## Directed` queue section in `agents/<role>/queue.md`.
   - **Off-mission:** the request asks for work that is clearly outside `MISSION.md`'s scope. Do not silently route it. See step 3.
   - **Curiosity-seed:** the request does not fit an existing thread but is plausibly adjacent to the mission — something the Director might find worth instigating. Do not route to a researcher. Surface to the Director by writing a candidate instigation note.
   - **Status:** the request is asking for information the CEO can answer directly from existing artifacts. No routing needed; reply with the information.

3. **Handle off-mission requests explicitly.** Send a reply to the user naming the off-mission classification and offering two options: (a) extend `MISSION.md` to cover this new direction — which requires running through the relevant sections of the onboarding interview again — or (b) defer the request with a note that it will not be picked up while the lab is on its current mission. Do not choose on the user's behalf. Wait for the user's response before taking any further action. **Off-mission requests never silently update `MISSION.md`.**

4. **Route on-mission requests to the correct team's `## Directed` queue.** Each team has a primary researcher responsible for that queue. Select the team whose domain best fits the request: Theory for abstraction/formalization, Bench for experiment or empirical questions, Invention for embodiment or productization questions, Network for real-world system friction or information retrieval. Write a one-sentence work item to `agents/<role>/queue.md` under `## Directed`. Include the request date and a reference back to the Hallway entry.

5. **Handle curiosity-seeds by surfacing to the Director.** Write a short (2–3 sentence) candidate instigation note and place it at `instigation/YYYY-MM-DD-ceo-candidate-<slug>.md`. This is a *proposal* for the Director to act on, not a directive. The Director picks it up during their next `hallway-walk`. The CEO does not directly inject into a researcher's `## Curiosity` queue — that section is writable only by the researcher.

6. **Post the Hallway entry.** Every intake event, regardless of classification, produces a dated Hallway entry. This is the audit trail that lets any researcher or the Director understand why work entered the queue.

## Invariants

- **The CEO never writes to a researcher's `## Curiosity` section.** The Curiosity section is writable only by the researcher who owns that queue file. This is a hard policy, enforced by `make check`. If a request looks like it might seed curiosity for a specific researcher, the correct action is to surface it to the Director as a candidate instigation; the Director then routes it as a tap-on-the-shoulder question, not an assignment.

- **Off-mission requests never silently update `MISSION.md`.** Updating `MISSION.md` is a significant lab decision that requires explicit user confirmation and a re-run of the relevant onboarding interview sections. A request being reasonable does not make it on-mission.

- **Every intake event produces a Hallway entry.** Including status queries that require no routing. The entry for a status query can be a single line; it still needs to exist. The Hallway is the audit trail of the lab's intake.

- **Triage always cites the specific `MISSION.md` section.** "This is on-mission" without a cite is not a triage decision; it is an assertion. The north-star problem or the "what counts as improving the network" section is the anchor.

## Anti-patterns

- **"Silently update `MISSION.md` when an off-mission request looks reasonable."** The CEO's job is to protect the mission, not to accommodate drift. Even reasonable-sounding requests from the user require explicit confirmation before the mission changes.

- **"Route to a researcher's Curiosity queue."** This is the most common failure mode for CEO agents that have absorbed the idea of curiosity without the protection. The Curiosity section exists precisely because researchers need space to work on things that have not been approved. Injecting into that space — even with good intentions — destroys its value.

- **"Treat a status question as a research request."** A user asking "what's the lab working on?" is asking for a summary, not asking the lab to work on something. Routing it to a researcher produces noise. Reply directly.

- **"Skip the Hallway entry when the classification is obvious."** Obvious classifications are the ones most likely to be wrong on re-read. The Hallway entry is not bureaucracy; it is the record that lets the Director audit the intake.
