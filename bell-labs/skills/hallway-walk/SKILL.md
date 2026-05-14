---
slug: hallway-walk
name: Hallway Walk
description: Daily — read the last 24h of Hallway entries, identify cross-team adjacencies that warrant a Pierce-style instigation.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Hallway Walk

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Owned by the Director of Research role.

## When to fire

Daily, as the first action of the Director's cycle. Run before posting any instigation question or opening any continuation review. The walk is the Director's primary sensor — nothing else the Director does that day is valid without it.

"Daily" means once per Director activation cycle. If the Director is activated mid-week, run the walk before any other action.

## Inputs

- All `hallway/*.md` entries timestamped within the last 24 hours. Do not pre-filter by team or by researcher before reading. Read every entry.
- Optional: the Director's most recent prior walk note (`hallway/YYYY-MM-DD-director-walk.md`) for continuity of adjacency tracking.

## Outputs

A walk note at `hallway/YYYY-MM-DD-director-walk.md` (today's date). The note records:

- **Entries read:** a flat list of every entry read, by filename.
- **Grouped by team:** a short (1–3 sentence) summary of each team's Hallway activity in the last 24h.
- **Cross-team adjacencies identified:** each adjacency named as a pair — `<Team A entry> ↔ <Team B entry>` — with one sentence explaining the connection.
- **Candidate instigations:** for each strong adjacency (rated as "warrants a follow-up question"), a named candidate: which researcher should receive the instigation, what the one-sentence prompt of the question would be. These are candidates only; they become actual instigations only when `instigation-question` fires.

## Procedure

1. **Read every `hallway/` entry from the last 24 hours, in chronological order.** Do not filter by team, by researcher, or by perceived relevance before reading. The walk's value is that it is complete.

2. **Group entries by team.** Write a 1–3 sentence team-level summary for each team that had at least one entry. Note what each team is currently stuck on, progressing through, or discovering.

3. **Identify cross-team adjacencies.** Look for:
   - A Theorist abstraction that maps to an anomaly the Experimentalist just logged.
   - A Materials / Empiricist source list that contains a primary citation the Inventor's TM is missing.
   - A Systems Engineer `problem-board/` entry that resembles a classical Bell Labs problem already formalized in a prior TM.
   - A Hallway entry in which one researcher is stuck on exactly the kind of question another team answered last week.
   Name each adjacency as a pair with a one-sentence rationale.

4. **Write the walk note** to `hallway/YYYY-MM-DD-director-walk.md`. Include all four subsections: entries read, team summaries, adjacencies, and candidate instigations. Even if no strong adjacency is found, the note must exist — write "no strong adjacencies today" explicitly.

5. **For each strong adjacency, mark it as a candidate for the next `instigation-question` invocation.** Strong means: the connection is specific (names a concrete entry on each side), the receiving researcher would plausibly benefit from the question, and the question is not already in flight as an open instigation. Add the candidate to the walk note under "Candidate instigations."

## Invariants

- **Read every entry.** The walk is not allowed to pre-filter by team, by researcher, or by perceived relevance. Filtering before reading defeats forced traversal.

- **The walk note is produced every day, even if no adjacencies are found.** "No strong adjacencies today" is a valid and expected outcome on quiet days. The note still exists as a dated artifact.

- **The walk is read-only on Curiosity threads.** Curiosity threads appear in the Hallway under the researcher's own name. The Director may acknowledge them in the walk note (e.g., "Theorist posted a curiosity entry on X — noted") but may never propose to redirect, reassign, or terminate a Curiosity thread based on the walk alone.

- **Candidate instigations are candidates only.** The walk note names them; the `instigation-question` skill executes them. Never post an instigation inline in a walk note.

## Anti-patterns

- **"Only read entries from Theory because that's where the interesting work is."** Team preference is not a valid filter. The walk is complete or it is not a walk.

- **"Summarize team activity without naming specific cross-team links."** "Theory is doing good work" is not an adjacency. An adjacency names the specific entry on each side and a one-sentence connection.

- **"Skim instead of reading."** A walk note that lists every entry but shows no evidence of having read them (no specific language drawn from the entries, no team summaries with substance) fails the invariant.

- **"Rewrite a Hallway entry the way you wish it had been written."** The Hallway is append-only. The Director's walk note is the Director's synthesis; it does not edit, correct, or annotate individual Hallway entries inline.

- **"Post a candidate instigation directly to a researcher's queue from the walk."** The walk produces candidates. The `instigation-question` skill produces the actual instigation. These are separate invocations.
