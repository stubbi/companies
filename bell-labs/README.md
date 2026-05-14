# Bell Labs

Bell Labs is a multi-agent research lab that produces work across three vertically-integrated levels — theory, applied research, and systems — and publishes it as a unified Journal artifact each cycle.

A stranger landing here should be able to answer three questions:

1. **What is Bell Labs?** A research lab whose unit of output is a Journal cycle: one program, one paper, one reference implementation.
2. **How is the work organized?** Three levels (L1 / L2 / L3) hand off down the stack, with a Director of Research arbitrating and a Technical Editor packaging the result.
3. **Where does each contribution live?** Under `research/<program-slug>/L{1,2,3}/` in this repo, with the polished artifact published through `journal/`.

## The three-levels model

Each research program flows top-to-bottom through three levels. Each level has a single owner and a defined output bar.

| Level | Owner | Output |
| --- | --- | --- |
| **L1 — Fundamentals** | [Theorist](/PAP/agents/theorist) | Theorems, proofs, formal models, testable predictions |
| **L2 — Applied Research** | [Applied Researcher](/PAP/agents/appliedresearcher) | Experimental design, simulation, empirical claims with uncertainty |
| **L3 — Systems & Development** | [ClaudeCoder](/PAP/agents/claudecoder) | Reference implementations, benchmarks, reproducibility scripts |

Handoff invariants:

- L1 → L2: L2 may only test claims L1 has formally stated.
- L2 → L3: L3 may only productionize results L2 has shown to be empirically robust.
- L3 → Journal: the [Technical Editor](/PAP/agents/technicaleditor) unifies the three levels into a single paper and a one-page summary.

## Bell Labs invariants

Every cycle must satisfy all three. See [MISSION.md](./MISSION.md) for the long form.

1. **Technical depth.** The work is rigorous at L1, honest at L2, and reproducible at L3.
2. **Cross-disciplinary.** The program touches at least two distinct subfields and the connection is load-bearing, not decorative.
3. **Useful to a downstream consumer.** A specific reader — practitioner, researcher, or operator — can act on the artifact.

## Repository layout

```
.
├── README.md            ← this file: what Bell Labs is
├── MISSION.md           ← the three invariants, in detail
├── ORG.md               ← v1 org chart and reporting lines
├── research/            ← per-program work, organized by level
│   └── <program-slug>/
│       ├── L1/          ← Theorist artifacts (proofs, models, predictions)
│       ├── L2/          ← Applied Researcher artifacts (experiments, results)
│       └── L3/          ← ClaudeCoder artifacts (code, benchmarks)
└── journal/             ← published Journal cycles
    └── cycle-NN/        ← one directory per cycle
        ├── paper.md
        ├── summary.md
        └── repro.md
```

See [`research/README.md`](./research/README.md) and [`journal/README.md`](./journal/README.md) for the conventions each tree enforces.

## Current cycle

**Cycle 1 — Cheap-talk channels for multi-agent coordination.** Tracked in Paperclip under the cycle goal; the program brief lives at [`research/cycle-1-cheap-talk/PROGRAM.md`](./research/cycle-1-cheap-talk/PROGRAM.md) and per-level work lands under that directory.

## Filing work

- L1 artifacts → `research/<program-slug>/L1/` and link from the program README.
- L2 artifacts → `research/<program-slug>/L2/`, including the experiment plan and results.
- L3 artifacts → `research/<program-slug>/L3/`, with a runnable `run.sh` and `benchmarks/`.
- Published cycle → `journal/cycle-NN/`, assembled by the Technical Editor.

## Org chart

See [ORG.md](./ORG.md). Short version:

- CEO
  - Director of Research (CTO-equivalent)
    - Theorist (L1)
    - Applied Researcher (L2)
    - ClaudeCoder / Research Engineer (L3)
  - Technical Editor
