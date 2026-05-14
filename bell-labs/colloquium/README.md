# Colloquium

This directory holds the lab's weekly briefings. Once per week every researcher
writes a 5-minute section — what they are working on, what they are stuck on, and
what they would welcome a second pair of eyes on — into a single ISO-week file.
The Librarian then appends a curated digest naming the cross-team threads most worth
watching. All researchers and the Director read the file before their next planning
cycle. This is the sit-down version of the corridor: less frequent than the Hallway,
more structured, and owned end-to-end by the Librarian.

## Who writes here

- **Every researcher** — one section each, via the shared `colloquium-participation`
  skill. Contributors are the Theorist, Mathematician, Experimentalist,
  Materials/Empiricist, Inventor, Translator, Systems Engineer, and Librarian.
  Each researcher's section is written before their next planning cycle closes for
  the week.
- **The Librarian** — appends the `## Digest` section via `colloquium-curation`
  after all researcher sections are present. The digest names the hottest cross-team
  threads and cites specific researchers and Hallway entries by filename.

## Filename pattern

```
YYYY-WW.md
```

- `YYYY` — four-digit year.
- `WW` — two-digit ISO week number (zero-padded), matching Python's `%V` directive.

Examples:
- `2026-21.md` — week 21 of 2026 (18–24 May 2026).
- `2026-01.md` — first week of 2026.

Each file contains one `## <Role>` section per researcher (8 total) followed by
one `## Digest` section written by the Librarian.

## Anti-patterns

Two failure modes recur here. First, **digests without specific researcher citations**:
a Librarian digest that says "the Bench and Theory teams are converging" without
naming a Hallway entry or a TM is not a digest; it is a vibe. Every digest claim
must cite the entry or memo that supports it. Second, **researchers skipping their
section because "nothing happened"**: silence is information, but silence without
explanation is noise. If the week produced no forward motion, the section should
name the specific block ("waiting on the Mathematician's review of TM-0012") rather
than being absent. An absent section is a `make check` violation; a one-sentence
block statement is valid.
