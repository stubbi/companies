# Hallway

This directory holds the lab's append-only feed of work-in-progress notes — corridor
conversation, not finished work. Every entry is short (≤200 words), dated, and
attributed. A typical entry says what the author is about to do and which other
researchers' recent notes changed their thinking. The Hallway is distinct from
Technical Memoranda: a TM is thorough and witnessed; a Hallway entry is the
half-formed conjecture or bench observation posted on the way to the cafeteria.
Entries accumulate as the lab runs; they are never edited and never silently deleted.

## Who writes here

- **Every researcher** — via the shared `hallway-traversal` skill, which runs as a
  blocking precondition before every planning step. Authors are the Theorist,
  Mathematician, Experimentalist, Materials/Empiricist, Inventor, Translator,
  Systems Engineer, and Librarian.
- **The Director of Research** — via `hallway-walk`, which produces an entry noting
  cross-team adjacencies spotted during the daily read.
- **The Experimentalist** — also via `experiment-design`, which pre-registers the
  experiment's prediction as a Hallway entry *before* the experiment runs.
- **The CEO** — via `intake-triage` (one entry per intake event, including status
  queries) and `escalation-routing` (one entry when a real blocker is packaged for
  the user).

## Filename pattern

```
YYYY-MM-DD-<author>-<slug>.md
```

- `YYYY-MM-DD` — ISO date the entry was written.
- `<author>` — kebab-case role name: `theorist`, `mathematician`, `experimentalist`,
  `materials`, `inventor`, `translator`, `systems-engineer`, `librarian`,
  `director`, `ceo`.
- `<slug>` — 2–4 word kebab-case summary of the entry's subject.

Examples:
- `2026-05-14-experimentalist-transistor-surface-state.md`
- `2026-05-14-ceo-intake-compression-question.md`
- `2026-05-15-director-adjacency-theory-bench.md`

## Anti-patterns

The Hallway is corridor conversation, not a logging backend. The `hallway-traversal`
skill states this directly: **"Dump raw experiment logs into the Hallway."** Verbose
traces, data tables, and full code listings belong in the TM or the agent's own
working files. The Librarian prunes log-dump entries and posts a one-line note to
the Hallway naming the violation before removing the offending entry. The check
that distinguishes a valid Hallway entry from a log dump: would a researcher from a
*different* discipline understand what you are doing and why from ≤200 words? If not,
it is a log, not corridor talk.
