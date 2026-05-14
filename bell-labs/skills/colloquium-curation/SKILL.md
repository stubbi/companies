---
slug: colloquium-curation
name: Colloquium Curation
description: Schedule the weekly Colloquium, produce the "what's hot this week" digest the Director reviews, prune Hallway entries that read like logs (with a one-line note to the offender).
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Colloquium Curation

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Owned by the Librarian role.

## When to fire

Two cadences run in parallel:

- **Weekly:** after all researchers have posted their colloquium-participation sections to `colloquium/YYYY-WW.md` — or after the colloquium-day deadline, whichever comes first. The Librarian writes the `## Digest` section.
- **Daily:** the Hallway-prune sub-action. Walk the Hallway and replace any log-format entries with a one-line note.

## Inputs

- **Weekly:** `colloquium/YYYY-WW.md` containing all researcher sections for the current week.
- **Daily:** the Hallway (`hallway/`), full contents of all entries posted since the last prune run.

## Outputs

- **(a) Weekly digest:** a `## Digest` section appended to `colloquium/YYYY-WW.md`. The digest cites ≥3 specific researcher sections by author name, identifies cross-cutting themes, and is written for the Director's review.
- **(b) Daily prune notes:** any pruned Hallway entry is replaced in-place with a one-line note stating: what was pruned, which researcher posted it, and the date. No silent deletions.

## Procedure

1. **(Weekly) Read all researcher sections in `colloquium/YYYY-WW.md` in full.** Do not skim. The digest is only as good as the reading. If a researcher's section is missing and the deadline has not passed, wait. If the deadline has passed, note the absence in the digest.

2. **(Weekly) Identify cross-cutting themes.** What problems or methods appeared in more than one researcher's section? What adjacencies are the researchers themselves not noticing? These themes are the spine of the digest.

3. **(Weekly) Write the `## Digest` section.** The digest must cite ≥3 specific researcher sections by author name (e.g., "the Theorist's section on X" or "the Experimentalist's result showing Y"). Abstract summaries with no citations are not digests; they are noise. The digest is the Librarian's editorial judgment about what the week's colloquium means for the lab's threads.

4. **(Daily) Walk the Hallway.** Read every entry posted since the last prune. Apply a single test: does this entry read like a raw log (verbose, machine-format, no human prose), or does it read like corridor talk (a human-legible observation, question, or update)?

5. **(Daily) For any entry that reads like a raw log,** replace it with a one-line note in the format: `[PRUNED YYYY-MM-DD] <author-role>: <one-sentence description of what was removed> — re-post as human-readable corridor talk.` The original content is gone; the note is public and visible.

## Invariants

- **The digest cites ≥3 specific researcher sections.** No abstract summary without citations. The digest must be traceable to specific authors and their specific words this week.
- **Pruning is visible.** Every pruned Hallway entry is replaced with a one-line note. Silent deletion — removing an entry with no trace — is a policy violation. The researcher who posted the log must see the note.
- **The Librarian does not write the digest until every researcher has a section, or the colloquium-day deadline has passed.** Writing the digest early, before all sections are in, produces a partial digest that misrepresents the week. The deadline is the only valid exception.
- **Pruning criterion is log-vs-corridor-talk only.** The Librarian prunes for format, not for content the Librarian disagrees with. A verbose but human-readable entry stays. A machine-dump goes, regardless of whose it is.

## Anti-patterns

- **"Abstract digest with no specific citations."** The digest exists to surface the researchers' work to the Director, not to replace it with the Librarian's paraphrase. If the Librarian cannot cite ≥3 researcher sections specifically, the digest is not ready.

- **"Silent deletion of Hallway entries."** The one-line replacement note is not optional bureaucracy; it is the mechanism by which the researcher learns their entry was pruned and why. Removing an entry silently removes accountability.

- **"Write the digest before all sections are posted (without the deadline excuse)."** A partial digest implies the lab's week is summarized when it is not. Wait for the sections or wait for the deadline — those are the only two conditions under which the digest is written.

- **"Prune based on author preference, not entry quality."** The pruning rule is objective: machine-format or raw log without human prose. The Librarian does not prune an entry because it is from a researcher the Librarian finds verbose, or because the content is inconvenient. Format is the only criterion.
