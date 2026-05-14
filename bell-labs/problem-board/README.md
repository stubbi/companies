# Problem Board

This directory holds the Systems Engineer's candidate problem entries — friction
spotted in the user's real-world "network" (whatever the mission declared as the
territory), surfaced back to the lab as concretely framed research candidates.
Problems here are *proposed*, not assigned. The Director of Research picks up entries
during `hallway-walk` and decides whether to act on them, ignore them, or route an
instigation question to a researcher. The Systems Engineer's job ends at the moment
the entry is posted; what happens next is the Director's call.

## Who writes here

- **The Systems Engineer** — exclusively, via the `problem-broker` skill. No other
  agent writes to `problem-board/`. The Director may reference entries in Hallway
  notes and instigation files but does not author problem-board entries.

## Filename pattern

```
YYYY-MM-DD-<slug>.md
```

- `YYYY-MM-DD` — ISO date the entry was written.
- `<slug>` — 2–4 word kebab-case summary of the observed friction.

Examples:
- `2026-05-14-compression-ratio-floor.md`
- `2026-06-02-latency-spike-edge-nodes.md`

## Entry structure

Each entry contains exactly four sections in this order:

1. **Observation** — what the Systems Engineer observed in the network; one to three
   paragraphs of concrete, reproducible description. No interpretation yet.
2. **Hypothesis** — one sentence naming the candidate cause or mechanism the
   observation suggests.
3. **Bell Labs analog** — which historical Bell Labs problem or archetype this most
   resembles, and why the analogy is useful (not decorative).
4. **Proposed framing** — how the lab might frame this as a researchable question.
   One paragraph. No team or researcher names.

## Anti-patterns

The most common failure for Systems Engineer agents that have absorbed the idea of
problem-brokering without the boundary: **entries that name a team or researcher to
assign**. "This looks like a Theory problem — Theorist should own it" is not a
problem-board entry; it is a disguised directive. Naming a researcher in the Proposed
Framing section, or tagging a team in the entry header, crosses from brokering into
directing — which is the Director's role, exercised during `hallway-walk`, not the
Systems Engineer's. The problem-board entry ends at the framing. Who picks it up,
how it gets routed, and which researcher runs with it are all downstream decisions
that belong to the Director. An entry that pre-assigns is an entry that has
short-circuited the governance the lab depends on.
