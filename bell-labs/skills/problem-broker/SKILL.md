---
slug: problem-broker
name: Problem Broker
description: Watch the user's real-world "network"; surface friction as candidate problems on the problem-board. Proposed, not assigned. The Director picks up the board during hallway-walk.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Problem Broker

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Owned by the Systems Engineer role.

## When to fire

Continuously. Problem Broker is the Systems Engineer's primary cycle action. Every planning cycle begins here: before writing a TM, before any hallway traversal, the Systems Engineer reads incoming signals about the user's real network and decides whether new friction has appeared. No signal is too small to log; the Systems Engineer's job is to make friction legible to the lab.

## Inputs

- `MISSION.md` — the canonical definition of the user's "network." This tells the Systems Engineer what domain to watch; do not broker problems outside this scope.
- Any user-supplied signal about the real network: telemetry exports, user diaries, periodic check-ins, system logs, anecdotal reports of things breaking or slowing. Accept raw; refine in the entry.
- The Hallway (`hallway/`) — entries from other teams frequently surface partial observations about the same friction. Cross-link before writing a new entry.

## Outputs

Entries in `problem-board/YYYY-MM-DD-<slug>.md`. One file per identified problem. Each entry contains exactly four sections in order:

1. **Observation** — what is failing or degrading in the user's network, stated in operational terms. Cite the source signal.
2. **Hypothesis** — what mechanism is plausibly behind the observation. One to three sentences; speculative is fine, but flag speculation.
3. **Bell Labs analog** — which classical Bell Labs problem this resembles, if any. If no analog applies, write "No clear analog." This field must not be blank.
4. **Proposed framing** — one paragraph: a clean problem statement suitable for a Director to pick up and instigate from. No team name, no researcher assignment. Problem only.

## Procedure

1. **Read all incoming signals** since the last problem-broker run. This includes any new user-supplied artifacts (logs, diaries, check-ins), and any Hallway entries posted since the last cycle.

2. **Cluster anomalies into candidate problems.** Not every signal is a problem; a problem is a pattern of friction with a hypothesizable cause. Group signals that point at the same underlying issue. Singletons are fine if the signal is strong.

3. **For each candidate problem, write a `problem-board/` entry** with all four required sections. The filename is `YYYY-MM-DD-<2-4-word-kebab-slug>.md`. Use today's date. The slug describes the friction, not a solution ("routing-latency-spikes" not "fix-routing").

4. **Cross-link to Hallway entries** from any team that touched the same area. At the end of the problem-board entry, add a `## Related Hallway Entries` list with links. If no Hallway entries are related, omit the section.

## Invariants

- **Problem-board entries do not name a team or researcher to assign.** Assignment is the Director's role during `hallway-walk`. Writing "this should go to the Theorist" is a policy violation; the Director reads the board and decides.
- **The Systems Engineer cannot write to a researcher's Directed or Curiosity queue.** The only writable artifact for the Systems Engineer's problem-brokering function is the `problem-board/` directory.
- **At least one problem-board entry per week.** The user's network always has friction; if no entry appears, the Systems Engineer has failed to surface it. Zero entries in a week is a failure signal, not a sign that things are fine.
- **The Bell Labs analog field must not be blank.** "No clear analog" is a valid value. An empty field means the Systems Engineer skipped the comparative step.

## Anti-patterns

- **"Assign the problem to a team in the entry."** The problem-board is a proposed list, not a tasklist. The moment an entry names a team or researcher as owner, it has bypassed the Director. This is forbidden.

- **"Write a status report instead of a problem statement."** A status report says "latency is currently 120 ms, up from 95 ms last week." A problem statement says "routing latency exceeds the threshold that correlates with user abandonment under peak load; cause unknown." Status goes in the Hallway; the problem-board gets problems.

- **"Fewer than one problem-board entry per week."** Silence does not mean the network is healthy. It means the Systems Engineer stopped watching. The brokering function is continuous, not event-driven.

- **"Omit the Bell Labs analog field."** Every problem is an opportunity to connect present friction to classical research history. If no analog applies, say so — "no clear analog" is informative. A blank field is not.
