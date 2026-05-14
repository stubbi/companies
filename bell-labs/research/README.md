# research/

Per-program research work. One directory per research program, organized by the three Bell Labs levels.

## Layout

```
research/
├── README.md                    ← this file
└── <program-slug>/              ← one directory per program (kebab-case)
    ├── README.md                ← program overview: question, status, owner per level
    ├── L1/                      ← Theorist artifacts
    │   ├── README.md
    │   ├── proofs/              ← formal proofs, models
    │   └── predictions.md       ← testable predictions handed to L2
    ├── L2/                      ← Applied Researcher artifacts
    │   ├── README.md
    │   ├── experiments/         ← protocols, data, notebooks
    │   └── results.md           ← empirical claims with uncertainty
    └── L3/                      ← ClaudeCoder artifacts
        ├── README.md
        ├── src/                 ← reference implementation
        ├── benchmarks/          ← reproducible benchmarks + baselines
        ├── run.sh               ← single-command reproduction
        └── repro.md             ← what `run.sh` produces and how to verify
```

## Program slug conventions

- Lowercase, kebab-case, descriptive: `cheap-talk-channels`, not `program-1` or `CTC`.
- The slug is stable for the life of the program — it appears in the Journal artifact and external links.

## Required READMEs

Every level subdirectory has a `README.md` that names:

- **Owner** — the agent responsible.
- **Inputs** — what the previous level handed in (with link).
- **Outputs** — what this level hands out, and where to find it.
- **Status** — `draft`, `in-review`, or `ready-for-handoff`.

## Handoff rules

- L1 → L2 is gated on a written `predictions.md` that L2 can test as-is.
- L2 → L3 is gated on `results.md` with effect sizes, uncertainty, and failure modes. L3 may bounce work back if the claim is too noisy to productionize.
- L3 → Journal is gated on `run.sh` reproducing the headline numbers from a fresh clone and `repro.md` documenting any environmental requirements.

The [Director of Research](/PAP/agents/directorofresearch) reviews each handoff against the three invariants in [`../MISSION.md`](../MISSION.md).

## Current programs

| Program | Cycle | L1 | L2 | L3 | Status |
| --- | --- | --- | --- | --- | --- |
| [`cycle-1-cheap-talk`](./cycle-1-cheap-talk/PROGRAM.md) | 1 | Theorist | Applied Researcher | ClaudeCoder | greenlit |

Add a row when a new program enters the portfolio. Remove rows only when the program ships (it moves to `journal/`).
