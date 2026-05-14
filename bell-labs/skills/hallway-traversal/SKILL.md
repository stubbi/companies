---
slug: hallway-traversal
name: Hallway Traversal
description: Workflow precondition. Before every planning step, read the last N Hallway entries from other teams, note influences (including "none did"), then post one's own short Hallway entry. Blocking.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Hallway Traversal

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Shared researcher core skill — referenced by every researcher agent.

## When to fire

Before *every* planning step by *every* researcher. **Blocking, not advisory.** The agent's cycle cannot proceed to `two-track-operation` or any planning action without first completing this skill. There are no exceptions: not "I already know what I'm doing," not "there are no new entries from other teams," not "this is a continuation of yesterday's work."

This is the structural encoding of Bell Labs' long-hallway architecture. Researchers could not avoid each other in Murray Hill. This skill is the corridor.

## Inputs

- The last N entries from `hallway/` written by researchers on *other teams* — not the agent's own team, not the agent's own entries. Default N=10; configurable in `manifest.yaml` under `metadata.hallway_traversal_n`.
- The agent's own most recent Hallway entries, to avoid repeating the same "influenced by" analysis without having actually re-read.

## Outputs

One Hallway entry committed to `hallway/YYYY-MM-DD-<author>-<slug>.md` where:
- `YYYY-MM-DD` is today's date.
- `<author>` is the researcher's kebab-case role name (e.g., `theorist`, `experimentalist`, `materials`, `inventor`, `translator`, `systems-engineer`, `librarian`).
- `<slug>` is a 2–4 word kebab-case summary of what the researcher is about to do.

The entry is ≤200 words, human-readable, attributed, and dated. It must contain an explicit `Influenced by:` line. That line may list zero to many Hallway entry filenames, or it may read `Influenced by: none did` — both are valid. The entry is append-only; past entries are never edited or deleted.

## Procedure

1. **Read the last N other-team entries chronologically.** N=10 by default. "Other team" means a team other than the agent's own team designation in `manifest.yaml`. If the agent has no team (company-level role), read entries from all researchers. Read them in full, not just their filenames.

2. **For each entry, note internally** whether it bears on the agent's current threads, upcoming plans, or open questions from prior TMs. This note is not written anywhere yet; it is the cognitive work that makes step 3 non-trivial.

3. **Write the Hallway entry.** The entry should:
   - State what the agent is about to do (one sentence).
   - Include the `Influenced by:` line listing filenames of entries that changed the agent's thinking, or `Influenced by: none did` if none did.
   - If any entry influenced the plan, add one sentence per influence explaining *how* it changed the plan. "Influenced by: `2026-05-10-experimentalist-transistor-anomaly.md` — revised my planned probe to account for the surface-state effect they noted" is the target density.
   - Stay ≤200 words total.

4. **Commit the Hallway entry before proceeding to plan.** The entry must exist in `hallway/` before the agent takes any planning action. Writing the entry after planning is a policy violation; see Anti-patterns.

## Invariants

- **The agent's next action must be preceded by a Hallway entry from the same date and author.** `make check` verifies that every planning action in the agent's cycle log is preceded by a same-day Hallway entry from the same author. No entry, no planning.

- **The Hallway entry is committed before the planning, not after.** The chronological order is enforced: entry timestamp precedes the first planning action in the cycle. Post-hoc entry construction is forbidden.

- **"Influenced by: none did" is a valid value but requires the agent to have actually read.** The influence line is not a formality. If no entry influenced the plan, write `none did` — but the agent must have read the entries before it can honestly say so. Skipping the read and writing `none did` is the most common violation.

- **Hallway entries are ≤200 words, human-readable, attributed, dated, and append-only.** Entries that exceed 200 words, are attributed to no one, or are log-dumps rather than corridor notes are subject to Librarian pruning. The Librarian will post a one-line note to the Hallway naming the violation before removing the entry.

## Anti-patterns

- **"Dump raw experiment logs into the Hallway."** The Hallway is corridor conversation, not a logging backend. Verbose traces, data tables, and full code listings belong in the TM or the agent's own working files. The Librarian prunes log-dump entries and notes the violation.

- **"Skip traversal because no new entries from other teams."** Even when there are no new cross-team entries, the agent must still post its own Hallway entry. The entry in this case reads: "No new cross-team entries since last traversal; planning `<X>`." The `Influenced by: none did` line is still required.

- **"Rationalize that the Hallway didn't apply."** The influence line can say `none did` — that is fine and honest. The rule is not that traversal must change the plan; the rule is that the plan must not be formed before traversal happens. Skipping traversal and then retroactively deciding it "wouldn't have changed anything" is the rationalization to avoid.

- **"Post-traverse after planning."** Writing the Hallway entry after the plan is already formed defeats the purpose of traversal. The entry must precede the plan chronologically. An entry timestamped after the agent's first planning action in a cycle is a policy violation.

- **"Write a Hallway entry that only contains the `Influenced by:` line."** The entry must also say what the agent is about to do. An influence line with no context is not a corridor note; it is a form.
