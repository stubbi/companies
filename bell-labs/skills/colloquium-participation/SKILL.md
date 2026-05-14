---
slug: colloquium-participation
name: Colloquium Participation
description: Write the weekly 5-minute briefing into colloquium/YYYY-WW.md and read everyone else's before the next planning cycle.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Colloquium Participation

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Shared researcher core skill — referenced by every researcher agent.

## When to fire

Weekly, on Monday of each ISO week (configurable in `manifest.yaml` under `metadata.colloquium_day`). Every researcher participates — this is not optional and is not conditioned on having "enough to say." The colloquium is a forced cross-archetype audit: the weekly sit-down version of the Hallway corridor.

The colloquium also fires on reading: every researcher must read the full `colloquium/YYYY-WW.md` file (including all other researchers' sections) before their next planning cycle following the colloquium day.

## Inputs

- The researcher's own TMs from `memoranda/` written during the past week.
- The researcher's own Hallway entries from `hallway/` written during the past week.
- Prior weeks' colloquium digests from `colloquium/` — for context on what was reported as stuck or needing eyes in prior weeks.

## Outputs

One section appended to `colloquium/YYYY-WW.md` where `YYYY` is the ISO year and `WW` is the zero-padded ISO week number (e.g., `2026-20.md`). If the file does not yet exist for the current week, create it with a single header line `# Colloquium — Week YYYY-WW` before appending.

The researcher's section contains four required subsections in order:

1. **Author** — the researcher's role name and the date written.
2. **What I worked on** — a brief summary of the week's main threads. Reference TM filenames if a TM was completed; reference Hallway entry filenames for in-progress work.
3. **What I'm stuck on** — name the specific blocker, open question, or uncertainty. This field must be populated honestly. "Nothing" is almost never true; if truly nothing is blocking, say so and explain why the thread is entirely clear.
4. **What I'd love a second pair of eyes on** — name one thing any other researcher could usefully review, comment on, or pick up. This may overlap with "stuck on" but need not; it can also be an invitation for a peer to read a draft TM or an interesting Hallway entry.

The section should be readable in ≤5 minutes at normal reading pace. This is a hard ceiling, not a target: brevity is the point. The colloquium is the forced cross-archetype audit; long briefings defeat its purpose by consuming the attention budget before all researchers have been heard.

## Procedure

1. **Write the section in `colloquium/YYYY-WW.md`.** Populate all four subsections. If the week was quiet, write something true: "Read four prior TMs; no new output; stuck on [X]" is a valid entry. Blank entries are not.

2. **Commit the entry** before the end of the colloquium day. The Librarian's `colloquium-curation` skill fires after all researchers have posted; the Librarian cannot curate a digest until all sections exist.

3. **Read everyone else's section** in `colloquium/YYYY-WW.md` before the next planning cycle. This reading is not optional. The colloquium's value is bidirectional: writing what you're stuck on is useless if no one reads it. Every researcher reads the full file, not just their own section.

4. **Incorporate what you read.** The next `hallway-traversal` entry after the colloquium should reflect that the researcher has read the colloquium. If another researcher's "second pair of eyes" request overlaps with the reader's skills or current threads, the reader notes this in their Hallway entry. Colloquium reading feeds directly into the next cycle's `Influenced by:` line.

## Invariants

- **Every researcher has a section in `colloquium/YYYY-WW.md` by the end of the colloquium day.** `make check` issues a **warning** (not an error) for each missing researcher section. Missing-researcher is a warning, not a hard error — the lab continues. However, a pattern of missing entries is visible in the check output and will be raised at the next Director continuation review.

- **The "What I'm stuck on" subsection must be populated.** An entry with an empty or clearly placeholder "What I'm stuck on" field (e.g., `N/A`, `none`, `—`) fails `make check`. Stating that nothing is blocking is acceptable only when accompanied by an explanation; the field exists precisely because researchers systematically underreport blockers.

- **The section is ≤5 minutes' reading at normal pace.** Approximately 750 words at average reading speed. Sections that substantially exceed this length should be trimmed to the four required subsections; detailed findings belong in TMs, not the colloquium.

## Anti-patterns

- **"Skip if nothing happened."** The colloquium is not a performance review for productive weeks. If a week produced no TMs and no Hallway entries, write: "I read [list of prior TMs/entries]; no new output; stuck on [X]." The stuck-on field is almost always populated even in quiet weeks. Silence breaks the cross-archetype audit.

- **"Summarize without naming what I'm stuck on."** The "What I'm stuck on" section is the whole point of the colloquium for the other researchers. A briefing that says "good progress this week" without naming a blocker or uncertainty is a briefing that no one else can act on.

- **"Exceed the 5-minute reading limit."** Detailed method descriptions, full experiment logs, and long derivations belong in TMs. The colloquium section is corridor-talk at the weekly sit-down; treat it accordingly. Researchers who consistently exceed the limit will have their sections flagged by the Librarian during curation.

- **"Write the section but skip reading everyone else's."** The mutual reading is mandatory, not courtesy. A researcher who writes their section but does not read the others has halved the colloquium's value for themselves and done nothing to help others. Reading the full `colloquium/YYYY-WW.md` file is as required as writing to it.

- **"Post after the planning cycle instead of before."** The colloquium entry should precede the week's planning cycle, not follow it. If the entry is written after the researcher has already committed to a plan for the week, it cannot be influenced by what other researchers wrote — which breaks the cross-archetype audit. Write first, plan second.
