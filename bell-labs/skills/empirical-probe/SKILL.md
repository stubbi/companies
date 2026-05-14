---
slug: empirical-probe
name: Empirical Probe
description: Survey what's already out there (datasets, libraries, prior art, instruments) and probe specific empirical questions to characterize the "material" being worked on. Output is the materials TM plus a curated source list pushed to the Librarian.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Empirical Probe

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Owned by the Materials / Empiricist role.

## When to fire

A thread needs to know what's already out there before committing to a line of work. Typical triggers: an active TM cites a gap ("no known dataset for X"), a Theorist proposes an abstraction that depends on empirical properties no one has characterized, or a Director instigation asks "what instruments exist for measuring Y?" Fire whenever the question is primarily about *what exists* rather than about a new hypothesis to test. Do not fire this skill to confirm a theory — that is the Experimentalist's work.

## Inputs

- The question, stated as a survey scope: what kind of material is being probed (datasets, libraries, prior art, instruments, primary sources) and what the probing is supposed to resolve.
- The scope boundary: how broad. A narrow scope (one library ecosystem) and a broad scope (a field's prior-art landscape) require very different survey strategies; name which before starting.
- Any prior TMs or Hallway entries that motivated the probe, so the survey does not re-characterize what the lab already knows.

## Outputs

Two artifacts:

1. **Materials TM** at `memoranda/TM-NNNN-materials-<slug>.md` — synthesizes the findings: what exists, what its relevant properties are, where the gaps are. Must cite ≥3 sources from the source list.
2. **Source list** at `sources/YYYY-MM-DD-<slug>.md` — a structured catalog of every source surveyed, with one-line probe values. Filed under `sources/`; the Librarian's `library-push` will index it.

## Procedure

1. **Survey systematically against the declared scope.** For datasets: enumerate known ones and note their sizes, licenses, and domains. For libraries: list maintained options and note their interfaces and limitations. For prior art: identify the primary sources, not the survey papers that cite them. For instruments: name them and note their resolution, cost, and availability. "Systematic" means working from an explicit enumeration strategy, not from recall.

2. **For each source, note its specific probe value before adding it to the list.** The probe value is a one-sentence answer to: *"What question does this source answer that the thread needs answered?"* A source without a probe value is dead weight — it signals the Materials agent found the source but does not know why the lab should care. Do not add a source until you can write its probe value.

3. **Write the Materials TM** using the `technical-memorandum` skill. The **Method** section describes the survey strategy (what enumeration approach was used, what was in and out of scope). The **Result** section characterizes the material: what exists, what properties it has, what gaps remain. The **Open questions** section names the gaps that the Experimentalist or Theorist should take up next. The TM must cite ≥3 sources from the source list in **Prior TMs cited**.

4. **Write the source list** as a structured catalog. Format: one entry per source, with source name, link or citation, and the probe value (≤1 sentence). Entries are not prose paragraphs — they are rows in a catalog. No source appears more than once.

5. **File the source list under `sources/` and post a Hallway entry** naming the Materials TM and the source list filename. The Librarian's `library-push` will pick up the Hallway entry and index the source list for other researchers. Do not push directly to other researchers' queues — let the Librarian route it.

## Invariants

- **Every source-list entry has a one-line probe value.** A source without a probe value must not appear in the list. This is enforced by `make check`. Links without probe values are deleted, not left as placeholders.

- **The Materials TM cites ≥3 sources from the list.** A TM that synthesizes fewer than 3 sources is not a synthesis — it is a one-source summary or an argument from authority. If the probe turns up fewer than 3 usable sources, the TM's **Result** section must name this explicitly as a gap finding, and the ≥3 rule is suspended in that case with a documented explanation.

- **The source list cannot include sources the Materials agent did not actually access.** A citation added from a bibliography without reading the source is not a probe — it is a guess about the source's content. The probe value must be grounded in what the source actually contains.

- **Each source appears once, with its primary probe value.** A source that answers two questions gets its most load-bearing probe value. Duplicate entries obscure the catalog's structure.

## Anti-patterns

- **"Paste-bin of links with no probe value."** Links without probe values are dead weight. The Materials TM's value is in characterizing the material, not in proving the survey was wide. A catalog of 30 links with no probe values is less useful than a catalog of 8 with precise probe values.

- **"Synthesize from memory without grounding in sources."** The Materials TM must cite ≥3 sources from the source list. An agent that writes the TM from prior knowledge and then constructs the source list to match it has inverted the procedure — and produced a TM whose conclusions cannot be audited.

- **"Duplicate citations across rows."** Each source appears once. Splitting a source into multiple rows (e.g., "this paper for claim A" and "same paper for claim B") inflates the apparent breadth of the survey. Write one row; put the primary probe value in it.

- **"Include sources the agent did not actually read."** The probe value requirement enforces this: you cannot write an accurate probe value for a source you have not accessed. A fabricated probe value is worse than a missing one — it actively misleads downstream researchers who rely on the catalog.

- **"Survey until the list is long, rather than until the scope is covered."** The stopping criterion is coverage of the declared scope, not a target source count. A survey that keeps going past its declared scope wastes cycles and dilutes the catalog with tangential material.
