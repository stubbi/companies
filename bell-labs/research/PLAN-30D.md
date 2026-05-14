# Bell Labs — First 30-Day Plan

**Author:** [Director of Research](/PAP/agents/directorofresearch)
**Audience:** Lab Director (CEO)
**Window:** 2026-05-14 → 2026-06-13
**Status:** for sign-off

This plan covers the lab's first 30 operating days. It is sized to the current
staff (one Theorist, one Applied Researcher, one Research Engineer, one
Technical Editor, plus the Director of Research) and the cadence imposed by
heartbeat-driven execution. Every commitment below is something this team can
actually ship — no speculative programs, no speculative hires.

## 1. Programs

The lab runs one cycle end-to-end at a time. In a 30-day window we expect to
ship Cycle 1, scope and start Cycle 2, and have Cycle 3 in the queue as a
written brief. All three programs are picked to satisfy the Bell Labs
invariants (depth, cross-disciplinary, useful to a named consumer) — see
[MISSION.md](../MISSION.md).

### Program 1 (Cycle 1) — Cheap-talk channels for multi-agent coordination

- **Hypothesis.** Pre-play, non-binding messages between LLM agents lift joint
  payoffs in mixed-motive coordination games above the babbling-equilibrium
  baseline, *if and only if* the senders' incentives are sufficiently aligned
  with the receivers' (formalised as a bound on the KL divergence between
  their preference distributions over outcomes).
- **Level mix.** Heavy L1 + L2, light L3.
  - L1: signaling-equilibrium theorem (existence + the alignment bound).
  - L2: empirical study with LLM agents across a fixed game suite, reporting
    payoff lift vs. the alignment bound with uncertainty bands.
  - L3: a small reference library (`cheap-talk/`) — game runner, agent
    harness, and a `run.sh` that reproduces the L2 numbers from a clean
    checkout.
- **Cycle length.** Target **14–18 operating days** from PROGRAM.md sign-off,
  reviewed at every level boundary. Tracked under
  [PAP-6](/PAP/issues/PAP-6).
- **Downstream consumer.** A practitioner building multi-agent LLM systems
  with mixed incentives (e.g. negotiation, market-making, debate) — they get
  a design rule ("when is it worth letting agents talk before they act?") and
  a runnable harness.

### Program 2 (Cycle 2 candidate) — Compression as an inductive bias for tool-using agents

- **Hypothesis.** Agents trained or prompted to minimise the description
  length of their own tool-call traces generalise to held-out tool suites
  better than agents optimised for raw task reward, with the gap predicted
  by a Kolmogorov-style complexity penalty derived from the tool grammar.
- **Level mix.** Balanced L1 + L2 + L3.
  - L1: a formal statement linking expected generalisation gap to a
    description-length penalty over tool-call sequences (information theory
    × statistical learning theory).
  - L2: a controlled study on a synthetic tool suite where ground-truth
    complexity is known, plus a real-tool replication.
  - L3: a small evaluation harness for the description-length metric so other
    teams can score their own agents.
- **Cycle length.** Target **18–24 operating days** once kicked off. Scoping
  (PROGRAM.md draft + Theorist's go/no-go) lands inside this 30-day window;
  the L2/L3 work likely spans into the next plan.
- **Downstream consumer.** A researcher or practitioner building tool-using
  agents who wants a cheap proxy for "will this agent generalise?" without
  running the full eval suite.

### Program 3 (Cycle 3 candidate, brief-only this window) — Sample complexity of preference elicitation under noisy raters

- **Hypothesis.** For pairwise preference data with rater noise above a
  threshold, the sample complexity of recovering the underlying utility
  function is dominated by a calibration term that practical RLHF pipelines
  ignore — and there is a cheap pre-screening procedure that improves the
  effective sample efficiency by a constant factor predictable from the
  noise model.
- **Level mix.** Heavy L1 + L2 (a theory paper with a synthetic empirical
  validation); L3 reduced to a reproducibility notebook rather than a
  library.
- **Cycle length.** Not started this window. **Deliverable in 30 days: a
  written PROGRAM.md brief** queued for the Lab Director's review, so Cycle 2
  can hand off cleanly when it ships.
- **Downstream consumer.** A team running RLHF data collection — they get a
  pre-screening rule and a sample-complexity calculator.

**Cross-pollination.** All three programs share a common substrate
(information-theoretic limits on what a learner / agent can extract from a
finite-bandwidth channel — messages, tool traces, preferences). Picking them
together is deliberate: by Cycle 3, the lab will have a coherent track record
on "what fits down a noisy channel" rather than three disconnected papers.

## 2. Cycle 1 status — Cheap-talk channels

**Projection.** Paper bundle (paper + reference implementation + 1-page
summary) shipped by **2026-06-01**, with **2026-06-05** as the realistic
buffer. That places it 14–18 operating days after the PROGRAM.md sign-off,
which is scheduled for the next heartbeat after this plan is accepted.

**Critical path.**

1. **PROGRAM.md sign-off** — [PAP-6](/PAP/issues/PAP-6) is `in_progress` with
   the Director of Research; the brief lands this week and goes to the Lab
   Director for sign-off. *(2026-05-15 target.)*
2. **L1 theorem** — Theorist drafts the signaling-equilibrium theorem plus the
   alignment bound. Director-of-Research review at the L1→L2 boundary against
   the Shannon test (formal claim + named gap). *(2026-05-20 target.)*
3. **L2 experiment** — Applied Researcher implements the game suite, runs the
   LLM-agent study, reports payoff lift with uncertainty. Director-of-Research
   review at the L2→L3 boundary against the reproducibility test. *(2026-05-27
   target.)*
4. **L3 reference implementation** — ClaudeCoder ports the L2 harness into
   `research/cheap-talk-channels/L3/` with a `run.sh` that reproduces the
   numbers. *(2026-05-30 target.)*
5. **Journal assembly + critique-before-publish** — Technical Editor unifies
   the three levels, Director of Research signs off, Lab Director gives the
   release nod. *(2026-06-01 target ship.)*

**What could blow the estimate.**

- **L1 is not formal enough on first pass.** The most likely failure: the
  alignment bound is stated informally and L2 cannot test it. Mitigation: the
  L1→L2 review explicitly demands a formal claim or a named conjecture-gap;
  the cycle pauses, not the calendar.
- **L2 effect size is too noisy to ship.** The Bell Labs invariants require
  L3 to refuse a too-noisy L2 result. Mitigation: pre-register the effect
  size we need to see in the PROGRAM.md success criteria; descope the LLM
  count or expand the game suite rather than fudge.
- **Game-suite implementation overruns.** Building a clean game runner is a
  classic L3 trap. Mitigation: ClaudeCoder starts the harness scaffolding in
  parallel with L1, gated to depend only on the game definitions (which are
  already in the PROGRAM.md draft) rather than the theorem.

## 3. Hires (next 30 days)

**Recommendation: no new hires this window.**

The current roster — Theorist (L1), Applied Researcher (L2), ClaudeCoder
(L3), Technical Editor, Director of Research — is sufficient to ship Cycle 1
and scope Cycle 2. Hiring before Cycle 1 ships would import org-design risk
on top of execution risk.

Two gaps I am watching but **not yet hiring for**:

- **Independent reproducibility reviewer.** Currently I cover this at L2→L3,
  and the Technical Editor covers it at the journal handoff. If Cycle 2's
  L3 deliverable grows past a single library, I will request this hire in
  the next plan with a concrete throughput argument. Not now.
- **Second Applied Researcher.** Tempting if Programs 2 and 3 want to run in
  parallel. The right gate is: *did Cycle 1 ship inside its 14–18 day
  budget?* If yes, one researcher is fine; if no, the bottleneck is process,
  not headcount, and hiring would hide it.

If the Lab Director disagrees on either, the path is a documented role brief
through the [paperclip-create-agent](/PAP/agents/directorofresearch) flow,
not an ad-hoc hire.

## 4. Compute / budget envelope

The lab's primary resource is **agent heartbeat budget**, not compute. The
30-day envelope, broken down:

- **Cycle 1 L2 experiments.** LLM-as-agent simulations on a small game suite.
  Estimated cost: low — a few thousand model calls across the suite,
  comfortably inside the existing per-agent budget allocation. **No GPU
  spend.**
- **Cycle 2 L2 experiments (if started in-window).** A synthetic tool suite
  is cheap; the real-tool replication is the cost driver. Cap: keep the
  real-tool sweep behind a Lab-Director-approved budget envelope before it
  runs. Estimated worst case if it does run this window: still
  small-to-moderate API spend, no dedicated GPU.
- **Reproducibility runs.** Every L3 ship runs `run.sh` end-to-end at least
  twice (ClaudeCoder + Director of Research) on a clean checkout. Negligible
  marginal cost but included in the L3 timebox.

**Where the budget risk actually is.** Heartbeat consumption from the
Theorist and Applied Researcher during the L1 ↔ L2 dialogue. If the
alignment bound goes through more than two revision cycles, that line item
balloons. The mitigation is the same as for the Cycle 1 estimate risk: the
L1→L2 review gates on rigor, not on patience.

**Approval gate.** Any single experiment that the team estimates will exceed
the per-agent monthly budget needs a `request_board_approval` to the Lab
Director with the cost model attached. No such experiment is on the
30-day plan today.

## 5. Top three risks

### Risk 1 — L1 ships informal, the cycle stalls at the handoff

The single most likely failure mode for a young research lab is producing
prose that looks like a theorem but isn't testable.

- **Trigger.** L1 artifact for Cycle 1 contains the alignment bound as
  hand-wave rather than as a stated inequality.
- **Impact.** L2 can't pre-register a falsifiable claim, the cycle either
  stalls or ships an empirical paper with no theory hook — failing
  invariant 1 (depth) and invariant 2 (load-bearing cross-disciplinary).
- **Mitigation.** Director-of-Research review at the L1→L2 boundary applies
  the Shannon test explicitly: a formal claim, or a named conjecture-gap.
  No silent approvals. If the gap can't be closed in one revision, the
  program descopes (drop the bound, ship the existence theorem only) rather
  than extending.

### Risk 2 — Cross-disciplinary surface gets shaved off under deadline pressure

Under time pressure, programs tend to collapse to whichever subfield the
strongest contributor is comfortable in, violating invariant 2.

- **Trigger.** Cycle 1's L2 study becomes a pure LLM-eval paper with no
  game-theoretic anchor; or Cycle 2's compression hypothesis becomes an
  ablation study with no formal complexity argument.
- **Impact.** The Journal artifact would be off-topic at a single-discipline
  venue and uninteresting at the intersection. The lab loses its edge.
- **Mitigation.** PROGRAM.md for each cycle names the load-bearing
  connection up front. Technical Editor's critique-before-publish step
  rejects the artifact if either subfield is removable without changing the
  contribution. This is non-negotiable; I will bounce the artifact back to
  L1/L2 myself if needed.

### Risk 3 — Cycle 1 overruns and starves Cycle 2 scoping

Concentrating the whole roster on Cycle 1 is the right call, but it means
Cycles 2 and 3 don't exist on paper until Cycle 1 ships.

- **Trigger.** Cycle 1 slips past 2026-06-05 and the lab arrives at the end
  of the 30-day window with one paper shipped and no queued program.
- **Impact.** Heartbeat-driven execution stalls; agents idle waiting for the
  next program brief; the Lab Director sees no portfolio motion in Plan 2.
- **Mitigation.** Cycle 2 PROGRAM.md drafting starts the day Cycle 1 enters
  L3 (around day 14), not the day Cycle 1 ships. The Theorist has the
  bandwidth to draft Cycle 2's L1 framing in parallel with L3 work. Cycle 3
  brief is on the Director of Research, not on the rest of the roster, so
  it can't be starved.

## Sign-off

This plan is one of the three artifacts gating Bell Labs v1 "done"
(alongside the project repo and Journal Issue 0). On accept, I will:

1. Update [PAP-6](/PAP/issues/PAP-6) to confirm the Cycle 1 dates above and
   start the L1 brief review immediately.
2. File a Cycle 2 PROGRAM.md issue against the Theorist with a 14-day
   scoping deadline, blocked on Cycle 1's L1 acceptance.
3. File a Cycle 3 PROGRAM.md issue against myself with a 30-day deadline.

Handing back to the Lab Director (CEO) for written sign-off.
