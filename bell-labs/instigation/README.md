# Instigation

This directory holds the Director of Research's tap-on-the-shoulder notes — the
Pierce-style reframing questions routed to specific researchers. Each entry is a
single paragraph that poses a question, names the receiving researcher, and
explains why the Director thinks the question is worth the researcher's attention
right now. The receiving researcher must acknowledge the instigation and is free to
decline it; a decline is recorded but never followed up by the Director. Instigations
are rate-limited to at most one per researcher per cycle. Entries here are proposed
redirections of *directed* work, not overrides of curiosity queues — the Director
never injects into a researcher's `## Curiosity` section.

## Who writes here

- **The Director of Research** — exclusively, via the `instigation-question` skill,
  which fires during or after `hallway-walk`. No other agent writes to `instigation/`.
  The CEO may write *candidate* instigation notes (when surfacing curiosity-seeds
  from `intake-triage`) but places them here with a `ceo-candidate-` prefix to
  distinguish proposals from active instigations; the Director decides whether to
  act on them.

## Filename pattern

```
YYYY-MM-DD-<receiving-researcher>-<slug>.md
```

- `YYYY-MM-DD` — ISO date the instigation was written.
- `<receiving-researcher>` — kebab-case role name of the researcher the question is
  directed to: `theorist`, `mathematician`, `experimentalist`, `materials`,
  `inventor`, `translator`, `systems-engineer`, or `librarian`.
- `<slug>` — 2–4 word kebab-case summary of the question's subject.

Examples:
- `2026-05-15-experimentalist-surface-state-question.md`
- `2026-06-03-theorist-channel-capacity-reframe.md`
- `2026-05-20-ceo-candidate-compression-seed.md` (CEO proposal, not yet acted on)

## Anti-patterns

Three failure modes define the line between instigation and middle management.
First, **directives instead of questions**: an entry that says "Experimentalist should
run a surface-state sweep before the next TM" is an assignment; an entry that says
"Have you considered whether the anomaly in TM-0004 might be a surface-state effect?"
is an instigation. The Director poses questions; the researcher decides what to do
with them. Second, **broadcast to a team instead of one researcher**: an instigation
addressed to "the Bench team" or "Theory and Bench" is not an instigation; it is
a meeting request. Each entry names exactly one receiving researcher. Third,
**follow-up after a decline**: when a researcher declines an instigation, the Director
records the acknowledgement and stops. Sending a follow-up question, referencing the
declined instigation in the next cycle's entry, or escalating the decline to the CEO
converts tap-on-the-shoulder into pressure — which is precisely what the rate limit
and the decline protocol exist to prevent.
