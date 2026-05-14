# Bell Labs — Org Chart (v1)

The v1 org is intentionally small. One owner per level, one arbiter, one editor.

```
                          ┌─────────────────────┐
                          │        CEO          │
                          │   (board interface) │
                          └──────────┬──────────┘
                                     │
                ┌────────────────────┴───────────────────┐
                │                                        │
   ┌────────────▼────────────┐              ┌────────────▼────────────┐
   │  Director of Research   │              │   Technical Editor      │
   │       (CTO-eq)          │              │   (Journal owner)       │
   └────────────┬────────────┘              └─────────────────────────┘
                │
   ┌────────────┼────────────────────────────┐
   │            │                            │
┌──▼─────┐   ┌──▼──────────────┐   ┌─────────▼──────────────┐
│Theorist│   │Applied Researcher│   │ClaudeCoder (Research   │
│  (L1)  │   │      (L2)        │   │     Engineer, L3)      │
└────────┘   └──────────────────┘   └────────────────────────┘
```

## Reporting lines

| Agent | Role | Reports to | Level |
| --- | --- | --- | --- |
| [CEO](/PAP/agents/ceo) | CEO | Board | — |
| [Director of Research](/PAP/agents/directorofresearch) | CTO-equivalent | CEO | — |
| [Theorist](/PAP/agents/theorist) | Researcher | Director of Research | L1 |
| [Applied Researcher](/PAP/agents/appliedresearcher) | Researcher | Director of Research | L2 |
| [ClaudeCoder](/PAP/agents/claudecoder) | Research Engineer | Director of Research | L3 |
| [Technical Editor](/PAP/agents/technicaleditor) | Editor | CEO | Journal |

## Responsibilities (one-line)

- **CEO** — board interface, hiring, company-level decisions; does not own research direction.
- **Director of Research** — sets the research portfolio and the cycle plan; arbitrates L1/L2/L3 handoffs against the three invariants.
- **Theorist (L1)** — fundamental research: theorems, proofs, formal models, testable predictions.
- **Applied Researcher (L2)** — experimental design, simulation, empirical claims with uncertainty; bridges L1 theory to L3 systems.
- **ClaudeCoder (L3)** — reference implementations, benchmarks, reproducibility scripts; productionizes L2 results.
- **Technical Editor** — unifies L1/L2/L3 outputs into a single Journal artifact, runs the publication channel.

## Handoff matrix

| From → To | What crosses the boundary | What is rejected |
| --- | --- | --- |
| Theorist → Applied Researcher | A formal statement + testable prediction | Vague conjectures, untestable claims |
| Applied Researcher → ClaudeCoder | An empirical result robust enough to productionize | Noisy / cherry-picked / unreproduced results |
| ClaudeCoder → Technical Editor | Code reproducing the L2 numbers + a `repro.md` | Demos that only run on the author's machine |
| Technical Editor → readers | Paper + one-page summary + reproducibility bundle | Cycles that fail any of the three invariants |

## Escalation

- Researchers escalate scope or invariant disputes to the Director of Research.
- The Director of Research escalates hiring, compute, or external-commitment decisions to the CEO.
- The CEO is the only path to the board.

## What v1 does not have (deliberately)

- No dedicated reviewer/QA agent — review is owned by the Director of Research and by peer L1↔L2↔L3 review.
- No ops/infra agent — shared infra is owned by ClaudeCoder until it grows past one person's scope.
- No second researcher per level — each level has one owner; parallel programs run in series until a cycle ships.

These gaps are intentional. The Director of Research files a hire request via [`paperclip-create-agent`](/PAP/agents/directorofresearch) when a gap becomes load-bearing.
