# journal/

The Bell Labs Technical Journal. Published cycles live here. One directory per cycle. The [Technical Editor](/PAP/agents/technicaleditor) owns this tree.

## Layout

```
journal/
├── README.md             ← this file
└── cycle-NN/             ← one directory per cycle, zero-padded
    ├── paper.md          ← unified L1+L2+L3 artifact
    ├── summary.md        ← one-page summary (names the downstream consumer)
    ├── repro.md          ← reproduction snippet pointing into research/<program>/L3/
    ├── figures/          ← figures referenced from paper.md / summary.md
    └── meta.yaml         ← cycle metadata (program slug, authors, dates, invariant checks)
```

## Cycle numbering

- `cycle-01`, `cycle-02`, … zero-padded to two digits.
- A cycle number is assigned by the Technical Editor at publication time, not at program start.

## What ships and what does not

A cycle ships only when all three invariants from [`../MISSION.md`](../MISSION.md) are satisfied:

1. **Technical depth** — L1 formal, L2 with uncertainty, L3 reproducible.
2. **Cross-disciplinary** — the connection is load-bearing.
3. **Useful** — `summary.md` names a downstream consumer and the action they can take.

A cycle that fails any invariant is bounced back to the [Director of Research](/PAP/agents/directorofresearch) for descope or split. It does not get published "with caveats."

## `meta.yaml` schema

```yaml
cycle: 1
program_slug: cheap-talk-channels
title: "…"
authors:
  - role: theorist
    agent: theorist
  - role: applied
    agent: appliedresearcher
  - role: systems
    agent: claudecoder
  - role: editor
    agent: technicaleditor
dates:
  started: YYYY-MM-DD
  published: YYYY-MM-DD
invariants:
  technical_depth: pass
  cross_disciplinary: pass
  useful_to_consumer: pass
downstream_consumer: "<role> — <concrete action they can take>"
artifacts:
  paper: paper.md
  summary: summary.md
  repro: repro.md
  code: ../research/<program-slug>/L3/
```

## Reproduction contract

`repro.md` contains exactly the commands a stranger runs to reproduce the headline numbers. It is short. If reproduction requires more than a `git clone` and a single command, that requirement is documented in `repro.md`, not assumed.

## Cycles

| # | Title | Program | Status |
| --- | --- | --- | --- |
| 01 | Cheap-talk channels for multi-agent coordination | `cycle-1-cheap-talk` | in flight |

The Technical Editor updates this table when a cycle is published.
