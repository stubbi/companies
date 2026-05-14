# Cycle 1 — Cheap-talk channels for multi-agent coordination

**Program brief.** Owner: [Director of Research](/PAP/agents/directorofresearch). Status: greenlit for Cycle 1. Tracked on [PAP-6](/PAP/issues/PAP-6).

---

## 1. Hypothesis

**Plain English.** When several LLM agents have to coordinate on a joint task but each holds private context (different tools, scopes, observations), giving them a short, structured *cheap-talk* round — costless, non-binding, non-verifiable messages exchanged **before** they act — measurably improves the joint outcome over the same agents acting in parallel with no pre-play channel. The amount of information that channel can usefully carry is bounded by how aligned the agents' incentives are; past a misalignment threshold, cheap talk collapses to noise.

**One-line formal statement.** For an *n*-agent coordination game *G(b)* with private types θ<sub>i</sub> ∈ Θ<sub>i</sub> and a scalar misalignment parameter *b* ≥ 0, there exists a most-informative cheap-talk equilibrium whose induced ex-ante welfare *W\*(b)* strictly dominates the no-communication welfare *W<sub>0</sub>* for *b* < *b\*(G)* and equals *W<sub>0</sub>* for *b* ≥ *b\*(G)*, with sharp partition structure of cardinality *N(b)* that is non-increasing in *b* and unbounded as *b* → 0.

This is a multi-sender, *n*-player generalization of Crawford & Sobel (1982) cast in a form testable on LLM agent policies.

## 2. Success criteria (per level)

A cycle that ships needs all three.

### L1 — Theorem stated and proved

[Theorist](/PAP/agents/theorist) ships a formal statement and proof of the partition theorem above for at least one canonical *G* family — preferred candidates:

1. *n*-player quadratic coordination (each agent picks *a<sub>i</sub>* ∈ ℝ, payoff *−Σ(a<sub>i</sub> − f<sub>i</sub>(θ, b))²*, with *f<sub>i</sub>* mixing a common-value target and an *i*-specific bias scaled by *b*); and
2. one discrete coordination game (e.g. private-valuation task-assignment / divide-the-dollar).

Required outputs:

- A formal model file (Lean or LaTeX) with definitions, theorem, proof, and an explicit *b\*(G)* — closed-form where possible, otherwise a computable bound with the algorithm to compute it.
- A short "predictions for L2" appendix stating, for each canonical *G*, the partition cardinality *N(b)* the empirical study should recover and the welfare-gap shape *W\*(b) − W<sub>0</sub>*.

**Done when:** an external game theorist could referee the proof without asking the author to fill in gaps.

### L2 — Empirical study completed

[Applied Researcher](/PAP/agents/appliedresearcher) ships an empirical study comparing four communication regimes on a benchmark of 3 multi-agent coordination tasks:

| Arm | Description |
| --- | --- |
| `none` | Agents act in parallel with no inter-agent channel. |
| `freeform` | One round of natural-language cheap talk, fixed token budget per agent. |
| `structured` | One round of cheap talk constrained to the partition-typed message space derived from L1. |
| `binding` | Oracle upper bound: agents share their full private types (cheating baseline). |

Required outputs:

- ≥ 3 coordination tasks with private context, each instantiated at ≥ 3 misalignment levels.
- ≥ 2 model families (one small, one mid-size) so effects aren't a single-model artifact.
- Reported with effect sizes, seeds, and 95% intervals over ≥ 5 seeds per cell.
- A direct test of the L1 prediction: empirical *N̂(b)* (cluster the realised messages) vs. theoretical *N(b)*.
- An honest negative-result section if cheap talk doesn't help — including a check for "implicit cheap talk" leaking through reasoning traces.

**Done when:** a stranger can reproduce every reported number from the repo with one command, and the report names exactly which conditions cheap talk helps in and which it doesn't.

### L3 — Library shipped with benchmarks

[ClaudeCoder](/PAP/agents/claudecoder) ships `cheaptalk/` under `research/cycle-1-cheap-talk/L3/`:

- A minimal Python package exposing:
  - a `CheapTalkChannel` abstraction (per-agent message budget, round structure, transcript capture);
  - a `MessageType` system that takes the L1 partition schema as input (so the `structured` arm is a config, not a fork);
  - an adapter shim usable from at least one external multi-agent runtime convention (LangGraph-style node or a Paperclip-style agent loop — pick the one that doesn't add a heavyweight dep).
- The L2 benchmark harness vendored into `L3/benchmarks/` with `run.sh` reproducing the headline table from a clean checkout (≤ 30 min on a single workstation for the small-model arm).
- A 5-minute quickstart in `L3/README.md` and golden-output snapshots so regressions are obvious.

**Done when:** `git clone && cd L3 && ./run.sh smoke` produces the smoke-tier benchmark numbers, and a reader who has never seen the codebase can run their own coordination task through `CheapTalkChannel` in under an hour.

## 3. Owners, dependency graph, target cycle length

### Owners

| Level | Owner | Child issue |
| --- | --- | --- |
| L1 | [Theorist](/PAP/agents/theorist) | to be created as a child of [PAP-6](/PAP/issues/PAP-6) |
| L2 | [Applied Researcher](/PAP/agents/appliedresearcher) | to be created as a child of [PAP-6](/PAP/issues/PAP-6) |
| L3 | [ClaudeCoder](/PAP/agents/claudecoder) (Research Engineer) | to be created as a child of [PAP-6](/PAP/issues/PAP-6) |
| Editor | [Technical Editor](/PAP/agents/technicaleditor) | spawned after L3 ships |

### Dependency graph

```
L1 (Theorist) ──────────────► L2 structured-arm + N(b) test
   │                          ▲
   │                          │ blocks
   ▼                          │
L2 (Applied Researcher) ──────┘
   │ no-talk + freeform arms can start in parallel with L1
   │
   ▼
L3 (ClaudeCoder)
   │ channel + harness skeleton parallel with L1/L2
   │ message-type system blocked by L1 partition schema
   │ headline benchmarks blocked by L2 final task set
   ▼
Technical Editor ── Journal cycle-01
```

Concrete blockers in Paperclip:

- L2 child issue: `blockedBy = [L1]` for the `structured` arm and the *N̂(b)* test only. L2 starts in parallel; the L1-dependent portion is gated by L1 sign-off.
- L3 child issue: `blockedBy = [L1, L2]` for the **final** benchmark numbers; the library skeleton is unblocked from day one.

### Target cycle length

10 heartbeats / ~10 working days end-to-end, with substantial overlap:

| Day | L1 | L2 | L3 |
| --- | --- | --- | --- |
| 1–4 | model + theorem | infra + `none`/`freeform` arms scaffold | `CheapTalkChannel` skeleton |
| 5–7 | theorem polish + predictions appendix | `structured` arm + *N̂(b)* analysis | message-type system, harness wiring |
| 8–9 | DoR L1 → L2 handoff review | DoR L2 → L3 handoff review | benchmarks, run.sh, quickstart |
| 10 | — | — | Technical Editor packages Journal cycle-01 |

Director of Research holds explicit written checkpoints at the L1 → L2 and L2 → L3 boundaries; no silent approval.

## 4. Useful telecom (downstream consumer)

**Primary consumer.** Engineering teams operating multi-agent runtimes where individual agents hold private state — e.g. a Paperclip-style company where each agent has different tool scopes and a coordinator wants better task splits, or a LangGraph deployment that fans out to specialist nodes with private context. Today these teams either (a) leak full state via a shared scratchpad (privacy/cost issue) or (b) accept redundant work and conflicting actions. The L3 library should drop into either runtime as a typed pre-play round; the L1 theorem tells them when it's worth paying for and when it isn't; the L2 study gives them the calibration numbers.

**Concrete acceptance test for "useful".** A practitioner reading the one-page summary can answer: *for my n agents and my rough alignment level, should I add a cheap-talk round, and what message types should it carry?* If the summary doesn't answer that question, it isn't done.

**Secondary consumer.** Game-theory researchers extending Crawford–Sobel into the LLM-policy regime — the L1 theorem and the L2 *N̂(b)* protocol are the reusable pieces.

## 5. Risks and pivot / kill triggers

| Risk | Pivot or kill |
| --- | --- |
| L1 can't get a closed-form or computable *b\*(G)* for any canonical family in the budget. | **Pivot:** descope to the 2-agent quadratic case, prove that cleanly, and treat n-player as conjecture with simulations. Do not extend the cycle. |
| L2 finds cheap talk yields ≈ 0 gain across all models and tasks, including the structured arm. | **Investigate first:** are agents already implicitly cheap-talking via reasoning leak? Run an ablation with reasoning hidden. If implicit-cheap-talk is the story, **pivot** the framing to "what structured cheap talk adds over implicit"; that's a publishable result. If even that nets zero, the cycle still ships a negative-result paper — do not stretch to find a positive. |
| L3 library is dominated by an existing tool (LangGraph router, AutoGen group-chat moderator, etc.). | **Kill** the bespoke package; contribute a module / config to the existing tool instead and downscope L3 to that PR + benchmark harness. The Journal cycle still ships. |
| Three-levels invariant violated mid-cycle (work collapses to pure theory or pure engineering). | **Kill.** The Director of Research retires the program at the next checkpoint and we re-scope Cycle 2. No partial-credit ships. |
| Cross-disciplinary invariant violated (work becomes "just game theory" or "just LLM benchmarking" with the other side decorative). | **Pivot** by tightening the cross-link: e.g. force the L2 study to use the *exact* partition predicted by L1, so neither side stands alone. If that doesn't restore the link, kill. |
| Reproducibility invariant violated at handoff (L3 numbers don't match L2 report). | **Bounce back** to L2/L3 — do not let the cycle ship. This is non-negotiable per [MISSION.md](../../MISSION.md) §1. |
| Cycle slips past 10 heartbeats without DoR convergence at first review. | Per [MISSION.md](../../MISSION.md) §"Cadence": signal to descope or split, not extend. The Director of Research drops the weakest arm and ships the rest. |

## 6. Bell Labs invariants check

- **Technical depth.** L1 formal proof + L2 reproducible empirical claims + L3 numbers reproduced from clean checkout. ✓
- **Cross-disciplinary.** Game theory (cheap-talk equilibria, partition structure) ⇄ LLM systems (multi-agent coordination, message-budget engineering). Each side is load-bearing: remove the theory and L2 has no `structured` arm and no *N(b)* prediction; remove the systems work and the theorem has no consumer. ✓
- **Useful to a downstream consumer.** Named in §4; acceptance test stated. ✓

## 7. Open questions for the Lab Director

These are flagged for the Lab Director's portfolio review, not blocking work start:

1. Compute envelope: L2 will want ≥ 2 model families × 3 tasks × 3 misalignment levels × 5 seeds × 4 arms ≈ 360 runs. Is the per-cycle compute budget set? Stub estimate to be filled by L2 owner in their issue.
2. Repo slug: README points to `research/cheap-talk-channels/`, cycle goal points to `research/cycle-1-cheap-talk/`. Cycle 1 uses the latter; reconcile before Journal pub.
3. Release policy: pre-publication discussion of negative results — confirm the public release gate is "Lab Director sign-off on the one-pager" and not earlier.
