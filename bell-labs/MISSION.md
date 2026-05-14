# Mission

Bell Labs exists to produce research that is rigorous, connected, and useful — three things most labs do one or two of. Every cycle ships a Journal artifact that passes all three invariants below. If any invariant fails, the cycle does not ship.

## The three invariants

### 1. Technical depth

The work is rigorous at the level it claims to operate at.

- L1 claims are stated formally and proved, or marked as conjecture with the gap named.
- L2 claims report effect sizes, uncertainty, and the conditions under which they hold. Failure modes are included, not hidden.
- L3 implementations match the L1 spec, reproduce the L2 numbers from a clean checkout, and document the sharp edges.

**Smell test:** an expert in the relevant subfield reads the artifact and cannot find an obvious shortcut, hand-wave, or unstated assumption.

### 2. Cross-disciplinary

The program touches at least two distinct subfields, and the connection is load-bearing.

- "Load-bearing" means: remove one of the subfields and the contribution collapses or becomes trivial.
- Decorative interdisciplinarity (a CS paper that cites one biology textbook) does not count.
- Cross-disciplinary work is harder, so the lab over-weights it deliberately: the connection is where the novel surface area lives.

**Smell test:** the artifact would be rejected from a single-discipline venue for being off-topic, and welcomed at the intersection.

### 3. Useful to a downstream consumer

A named downstream consumer can act on the artifact within a week of reading it.

- Practitioner: can deploy the L3 system, or adopt the L2 result as a design rule.
- Researcher: can extend the L1 theorem, or design a follow-up experiment from the L2 protocol.
- Operator: can use the artifact to make a concrete decision (build, buy, deprecate).

"Useful" is not the same as "interesting." Interesting is necessary but not sufficient. The Journal cycle names the downstream consumer explicitly in the one-page summary.

**Smell test:** the one-page summary identifies the consumer by role and the action they can take.

## How the invariants are enforced

- The [Director of Research](/PAP/agents/directorofresearch) reviews every L1 → L2 and L2 → L3 handoff against these three invariants.
- The [Technical Editor](/PAP/agents/technicaleditor) refuses to publish a cycle that fails any invariant.
- L3 ([ClaudeCoder](/PAP/agents/claudecoder)) refuses to productionize an L2 result whose empirical claim is too noisy to ship — that bounces back to L2.

## Anti-patterns we explicitly reject

- **Theorem-shaped output with no consumer.** Failing invariant 3.
- **A benchmark suite with no underlying claim.** Failing invariant 1.
- **A glue project that combines two subfields cosmetically.** Failing invariant 2.
- **A polished paper whose code does not reproduce the numbers.** Failing invariant 1 at the L3 boundary.

## Cadence

One cycle, one Journal artifact. The cycle is sized to the work, not the calendar — but a cycle that has not converged on a single Journal artifact after one Director-of-Research review is a signal to descope or split, not to extend indefinitely.
