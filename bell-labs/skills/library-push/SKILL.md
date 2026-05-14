---
slug: library-push
name: Library Push
description: On every new TM or Hallway entry, search prior memoranda for relevance and push the top-K to the relevant researcher's queue as a citation suggestion. Not search; push.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
      author: Jannes Stubbemann
      added_in: 0.1.0
---

# Library Push

> **Port-original skill.** Hand-authored for this Agent Company; not from upstream. Owned by the Librarian role.

## When to fire

On every new TM, Hallway entry, or colloquium section posted by any researcher. The Librarian watches the artifact stream; no explicit request is needed. This is a push service, not a reference desk — the Librarian initiates, researchers do not summon.

## Inputs

- The new artifact: the TM, Hallway entry, or colloquium section that just arrived. Full text.
- The prior corpus: all TMs under `memos/` and all Hallway entries under `hallway/`. Scan the full corpus each run; recency and overlap both affect scoring.
- Manifest metadata: `manifest.yaml` `metadata.library_push_k` field sets K. Default K=3 if the field is absent.

## Outputs

Push notes appended to relevant researchers' `agents/<role>/library-suggestions.md`. Each push note contains:

- The artifact being cited (title, path, date).
- One sentence explaining why this prior artifact is relevant to the recipient's current work.
- Posted to researchers *other* than the artifact's author.

Up to K suggestions per push event (hard cap). Quality determines which K are selected; do not pad to K if fewer strong matches exist.

## Procedure

1. **Extract key terms from the new artifact.** Identify the 5–10 most distinctive concepts, named objects, or research questions in the artifact. Use the artifact's own language; do not normalize to a taxonomy.

2. **Search the prior corpus for relevance.** Match key terms against TM abstracts, Hallway entry bodies, and colloquium sections. Cast wide on the first pass; prune in the scoring step.

3. **Score candidates by recency × topical overlap.** Recency: artifacts from the last 90 days score higher than older ones. Topical overlap: number of matching key terms. Combine multiplicatively. Ties broken by recency.

4. **Select the top-K.** K is the value from `manifest.yaml` `metadata.library_push_k`; default 3. If fewer than K candidates score above zero, push only those that do. Never pad with weak matches.

5. **Write push notes to relevant researchers' `library-suggestions.md` files.** A "relevant researcher" is any researcher currently working on a thread that overlaps with the artifact's key terms — identified by their recent Hallway entries or queue contents. The author of the new artifact is excluded. Each note is a short block: artifact title + path + date, then the one-line relevance justification.

## Invariants

- **Push, not search.** The Librarian initiates the push on every new artifact. Researchers do not file requests for their own citation queue; the service is proactive. A Librarian that waits to be asked has misunderstood its role.
- **K is a hard cap.** The default is 3; `manifest.yaml` can raise or lower it. Never exceed K, regardless of how many plausible matches exist.
- **Push to other researchers, never the author.** If the artifact's author is the only plausible recipient, post nothing. The push enriches the network, not the author's own awareness of their own work.
- **Every push note includes a one-line "why this is relevant."** The relevance sentence is not optional. A bare citation is noise; context is what makes the push useful.

## Anti-patterns

- **"Push everything you find."** K is a cap because quality matters. Flooding a researcher's suggestion file with ten marginal citations degrades the signal. Pick the best K; discard the rest.

- **"Push to the agent who wrote the artifact."** The author already knows their own work. Push flows to neighbors in the research graph, not back to the source. If the only match is the author, skip the push.

- **"Require researchers to request suggestions."** The Librarian is a push service. The entire value of this role comes from surfacing connections researchers did not know to ask for. A passive Librarian that waits for requests is a search engine, not a routing layer.

- **"Skip the one-line 'why this is relevant'."** Relevance without justification is noise. The researcher receiving the suggestion needs to understand immediately whether it is worth reading. A bare title and path forces them to read the artifact to judge its relevance — that is the Librarian's job, not the researcher's.
