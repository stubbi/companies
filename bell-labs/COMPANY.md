---
schema: agentcompanies/v1
slug: bell-labs
name: Bell Labs
description: '10-agent industrial-research lab modeled on Bell Labs (1925–1984). CEO
  is a Kelly-style patron and a separate Director of Research is the Pierce-style
  instigator. Researchers cover the five Bell Labs archetypes — theorist, experimentalist,
  inventor, translator, and wise head — plus a systems engineer who brokers problems
  from the user''s real "network" and a librarian who runs the colloquium and pushes
  prior memos into active threads. Two-track operation: every researcher runs a CEO-directed
  queue and a self-owned curiosity queue; the curiosity queue is protected by policy.
  Output is the Technical Memorandum.

  '
version: 0.1.0
license: MIT
authors:
- name: Jannes Stubbemann
  email: jannes@paperclip.inc
goals:
- Carry out long-horizon (months to years) research arcs in service of the user's
  declared north-star mission, staging every output as a dated, witnessed Technical
  Memorandum for human review.
- Preserve Bell Labs' five-archetype structure with a separated patron (CEO) and instigator
  (Director of Research), plus the systems-engineer and librarian boundary roles every
  modern imitator has dropped.
- Encode forced cross-archetype traversal — the Hallway, the weekly Colloquium, and
  Director's walks — as policy, not vibe. Each researcher's workflow blocks on reading
  other teams' recent work before planning.
tags:
- research
- invention
- industrial-research
- bell-labs
- technical-memo
- directed-curiosity
- long-horizon
metadata:
  affiliation: Name homage. Not affiliated with or endorsed by Nokia / Nokia Bell
    Labs.
---
# Bell Labs

10-agent industrial-research lab modeled on Bell Labs (1925–1984). CEO is a Kelly-style patron and a separate Director of Research is the Pierce-style instigator. Researchers cover the five Bell Labs archetypes — theorist, experimentalist, inventor, translator, and wise head — plus a systems engineer who brokers problems from the user's real "network" and a librarian who runs the colloquium and pushes prior memos into active threads. Two-track operation: every researcher runs a CEO-directed queue and a self-owned curiosity queue; the curiosity queue is protected by policy. Output is the Technical Memorandum.


## Boundaries

Nothing in this package constitutes a shippable product, patent, or peer-reviewed result on its own. These agents draft research artifacts (Technical Memoranda, invention disclosures, prototype specs, handoff documents, project proposals, sunset memos) for review by a human owner; every output is staged for human sign-off. The lab does not ship to the user's production systems on its own authority, file actual patents, submit to actual journals, or claim peer-review. The wild-duck / curiosity track is freedom of method, not freedom of fence — curiosity threads must still trace a plausible link to MISSION.md, and the Librarian flags drift. The Director never overrides a researcher's curiosity queue; that is a hard policy invariant enforced by `make check`. Mervin Kelly is not on staff. Patience, taste, and mentorship are configured, not magic the configuration confers. This is an aspiration with scaffolding, not a recreation of Bell Labs.

## Teams

- **Theory** (`teams/theory/TEAM.md`) — Builds the abstraction — invariants, reductions, mathematical objects — and runs the 25%-time math consultancy that any other team can pull in.
- **Bench** (`teams/bench/TEAM.md`) — Designs and runs experiments (code, simulation, ablation, controlled tests); surveys datasets, libraries, prior art, and instruments to characterize the "material" being worked on.
- **Invention** (`teams/invention/TEAM.md`) — Embodies working principles in devices, algorithms, and artifacts; runs the 3-stage Western-Electric-style productization that turns matured memoranda into user-deliverable handoffs.
- **Network** (`teams/network/TEAM.md`) — Boundary team. The Systems Engineer brokers problems from the user's real-world "network"; the Librarian pushes prior memoranda into active threads and runs the weekly Colloquium.

