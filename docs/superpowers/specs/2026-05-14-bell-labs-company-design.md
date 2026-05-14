# Design — Bell Labs Agent Company

**Status:** brainstormed; awaiting user review before implementation plan.
**Author:** Jannes Stubbemann (jannes@paperclip.inc — matching catalog convention; existing manifests use this address)
**Date:** 2026-05-14
**Target:** new company directory `bell-labs/` in [`stubbi/companies`](https://github.com/stubbi/companies).
**Format precedent:** Agent Companies schema `agentcompanies/v1`, as used by `academic-research/` and `financial-services/`.

---

## 1. Vision

> "Anyone should have their own Bell Labs at hand."

Bell Labs (1925–1984) is the only industrial-research organization in history that consistently produced foundational science *and* shipped product. Modern attempts to recreate it — PARC, MSR, Google X, DeepMind, Janelia, FROs — each copy one or two principles cleanly and drop the rest. The integrated **five-archetype model with a captive translator-to-manufacturing layer** has not been recreated.

This company is an opinionated, *agentic* translation: a 10-agent industrial-research lab that the user installs into Paperclip with `npx companies.sh add stubbi/companies/bell-labs`. On first run, the lab interviews the user to capture a durable north-star problem ("their network") and writes `MISSION.md`. Everything afterwards is in service of that mission, with a Bell Labs operating discipline: technical memoranda as the unit of intellectual record, a Hallway with forced cross-archetype traversal, a separated patron (CEO) and instigator (Director of Research), two-track operation (directed work + a self-owned curiosity queue protected by policy), and a load-bearing Translator role that turns matured memoranda into user-deliverable artifacts.

This is an *aspiration with scaffolding*, not a recreation. The hard parts of Bell Labs — taste, patience, mentorship — are exactly where current agents are weakest. The design tries to encode those properties structurally (forced traversal, named iteration budgets, witnessed memos, the anti-firing sunset memo) rather than hoping configuration confers them.

## 2. Manifest identity

```yaml
schema: agentcompanies/v1
slug: bell-labs
name: Bell Labs
description: >
  10-agent industrial-research lab modeled on Bell Labs (1925–1984). CEO is a
  Kelly-style patron and a separate Director of Research is the Pierce-style
  instigator. Researchers cover the five Bell Labs archetypes — theorist,
  experimentalist, inventor, translator, and wise head — plus a systems engineer
  who brokers problems from the user's real "network" and a librarian who runs
  the colloquium and pushes prior memos into active threads. Two-track
  operation: every researcher runs a CEO-directed queue and a self-owned
  curiosity queue; the curiosity queue is protected by policy. Output is the
  Technical Memorandum.
version: 0.1.0
license: MIT
authors:
  - name: Jannes Stubbemann
    email: jannes@paperclip.inc
tags: [research, invention, industrial-research, bell-labs, technical-memo,
       directed-curiosity, long-horizon]
```

No `upstream:` block. This is an original synthesis, not a port of an external repo. All skills are `port_original: true`. License is MIT (same as the catalog wrapper); there is no upstream license to preserve.

**Goals (manifest `goals:`):**

1. Carry out long-horizon (months to years) research arcs in service of the user's declared north-star mission, staging every output as a dated, witnessed Technical Memorandum for human review.
2. Preserve Bell Labs' five-archetype structure with a separated patron (CEO) and instigator (Director of Research), plus the systems-engineer and librarian boundary roles every modern imitator has dropped.
3. Encode forced cross-archetype traversal — the Hallway, the weekly Colloquium, and Director's walks — as policy, not vibe. Each researcher's workflow blocks on reading other teams' recent work before planning.

## 3. The Hallway — forced-traversal architecture

The single biggest differentiator of Bell Labs vs. every modern imitator was that researchers *could not avoid each other*. The Murray Hill building (opened 1941) had corridors so long they vanished to a point; doors were open; the supply department, the library, and the cafeteria sat across disciplinary boundaries. PARC copied the talent and missed the corridor. Calico has the patience and no corridor. We cannot lay corridors in YAML, but we can encode *forced traversal* as policy.

Four structural elements, each named in the manifest and owned by a specific agent:

### 3.1 The Hallway (`hallway/`)

Append-only feed of work-in-progress notes. *Distinct from finished Technical Memoranda.* Every researcher posts short entries: bench observations, half-formed conjectures, "I'm stuck on X," "this experiment didn't behave," "the Materials team's last note might apply here." Dated, attributed, never deleted. The Hallway is not finished work — it is the conversation in the corridor on the way to the cafeteria.

### 3.2 Forced traversal at planning time

The policy hook that distinguishes a Hallway from a Slack channel. Before *any* researcher agent picks its next action — directed *or* curiosity — its workflow requires it to read the last N Hallway entries from *other teams* and explicitly note (in its own next entry) which influenced its plan. The Theorist cannot plan without seeing the Experimentalist's last three notes. Skipping is not an option; "I read these, none changed my plan" is. This is encoded in the shared `hallway-traversal` skill and is **blocking**, not advisory. Enforced by `make check`.

### 3.3 The weekly Colloquium (`colloquium/`)

Owned by the Librarian. Every researcher posts a 5-minute briefing — "what I'm working on, what I'm stuck on, what I'd love a second pair of eyes on" — into `colloquium/YYYY-WW.md`. All researchers (and the Director) read it before their next planning cycle. This is the sit-down version of the corridor.

### 3.4 The Director's walks (`instigation/`)

The Director of Research's primary daily action is *not* directing — it is reading the Hallway and instigating. When the Director sees a Pierce-style opportunity ("Bardeen, have you talked to Brattain about surface states?"), they post an `instigation/` entry: a one-paragraph reframing question routed to a specific researcher. The receiving agent *must respond* but is free to *reject* the instigation. Rate-limited to ≤1 instigation per researcher per cycle. Tap-on-the-shoulder, not assignment.

### Anti-cargo-cult notes

- The Hallway is *not* logs. Verbose traces get pruned by the Librarian with a one-line note to the offender. The TM is for thoroughness; the Hallway is for visibility.
- Forced traversal scales sub-linearly: each researcher reads ~10–15 entries, not the whole history. The Librarian curates a "what's hot this week" digest the Director overrides if needed.
- Director instigation is rate-limited. Too many shoulder-taps is just middle management.

## 4. Teams and agents

Four teams plus two company-level wise heads. Ten agents total — 2 wise heads + 8 researchers across 4 teams.

### 4.1 Wise Heads (company-level, no `team:` field)

**CEO — Patron** (Mervin Kelly archetype).
Conducts the onboarding mission interview, writes and protects `MISSION.md`, manages intake routing, defends iteration budgets against ship-pressure, and produces a monthly state-of-the-lab summary for the user. Does *not* instigate research questions — Kelly explicitly did not. Patron, not boss.
Skills: `onboarding-mission-interview`, `intake-triage`, `patron-budget`, `escalation-routing`, `monthly-summary`.

**Director of Research — Instigator** (John Pierce archetype).
The lab's taste organ. Reads the Hallway daily, runs the weekly continuation review with the CEO, posts instigation questions (rate-limited), and signs every project sunset. The only agent allowed to inject into a researcher's *directed* queue mid-stream — and even that arrives as a question.
Skills: `hallway-walk`, `instigation-question`, `continuation-review`, `project-sunset`.

### 4.2 Theory team

**Theorist** (Shannon archetype). Builds the abstraction: the right invariant, the right reduction, the right mathematical object. Writes the long, BSTJ-shaped TMs that name a thing for the first time.
Specialized skills: `abstraction-build`.

**Mathematician** (Tukey / Fry archetype). 25%-of-cycles internal consultant. Any other team can pull the Mathematician in by filing a `consult-request/`; the Mathematician must accept unless their own queue is blocked. Owns rigor flow across the lab.
Specialized skills: `math-consultancy`.

### 4.3 Bench team

**Experimentalist** (Brattain archetype). Designs and runs the experiment that disconfirms or confirms. In an agentic setting: code experiments, simulations, ablations, controlled tests. Pre-registers the prediction in a Hallway entry before running.
Specialized skills: `experiment-design`.

**Materials / Empiricist** (Pearson / Teal archetype). Surveys what's already out there (datasets, libraries, prior art, instruments) and probes specific empirical questions to characterize the "material" being worked on.
Specialized skills: `empirical-probe`.

### 4.4 Invention team

**Inventor** (Bardeen / Hamming archetype). Sees a working principle and embodies it in a device, algorithm, or artifact. Writes the invention disclosure paired with a TM.
Specialized skills: `invention-disclosure`.

**Translator** (Western Electric liaison archetype). The load-bearing role every modern imitator drops. Takes a matured TM and runs the 3-stage productization. Owns the boundary between research and user-deliverable.
Specialized skills: `handoff-document` (one skill, three required stages internally).

### 4.5 Network team

**Systems Engineer** (problem broker). Watches the user's real-world "network" (whatever the mission named) and surfaces friction back to the lab as candidate problems on `problem-board/`. Problems are *proposed*, not assigned. The Director picks them up during `hallway-walk`.
Specialized skills: `problem-broker`.

**Librarian** (active routing). Not a storage bin: a *push* service. Reads every new TM and Hallway entry, pushes relevant prior work to active threads, runs the weekly Colloquium, curates the "what's hot" digest, prunes Hallway entries that read like logs.
Specialized skills: `library-push`, `colloquium-curation`.

### 4.6 Shared researcher core (referenced by all 8 researchers)

`technical-memorandum`, `hallway-traversal`, `two-track-operation`, `colloquium-participation`.

### 4.7 Org-chart sketch

```
                       User's MISSION.md
                              |
                       CEO ─── Director
                       │       │
        ┌──────────────┼───────┼──────────────┐
        │              │       │              │
     Theory         Bench   Invention      Network
     ├ Theorist     ├ Exp   ├ Inventor     ├ Sys Eng
     └ Math (25%)   └ Mat   └ Translator   └ Librarian
                              │              ↑
                              └─→ Handoff ───┘
                                  (via Hallway,
                                   weekly Colloquium)
```

## 5. Skills (22, all port-original)

### CEO-owned (5)
- `onboarding-mission-interview` — first-run wizard; turns user intent into `MISSION.md` (north-star, 1y/5y arcs, sunset conditions). Refuses to finish until the mission has a real fence.
- `intake-triage` — classify a new request as on-mission / off-mission / curiosity-seed; route to a team's directed queue or surface to the Director.
- `patron-budget` — name the iteration budget for each active thread; resist ship-pressure; produce the budget-defense memo when challenged.
- `escalation-routing` — package context and route real blockers to the user.
- `monthly-summary` — Kelly-style state-of-the-lab note: shipped, mid-arc, sunset, heating curiosity threads. No Gantt.

### Director-of-Research-owned (4)
- `hallway-walk` — daily: read last 24h of Hallway; identify cross-team adjacencies.
- `instigation-question` — Pierce-style one-paragraph reframing routed to a researcher; rate-limited ≤1 / researcher / cycle.
- `continuation-review` — weekly with CEO; read-only on curiosity threads.
- `project-sunset` — write the sunset memo: what we learned, where people redeploy, why it isn't a failure.

### Shared researcher core (4)
- `technical-memorandum` — canonical output. Dated, signed, witness-countersigned by a peer agent. Abstract → problem → prior TMs → method → result → open questions. ≤10 pages.
- `hallway-traversal` — workflow precondition; blocking. Read last N entries from other teams, post your own, note influences (incl. "none did").
- `two-track-operation` — directed (60%) + curiosity (40%) split; protection invariant: Director never overrides curiosity; promotion requires researcher consent.
- `colloquium-participation` — write weekly briefing into `colloquium/YYYY-WW.md`, read everyone else's before next planning cycle.

### Theory team
- `abstraction-build` (Theorist) — propose the right invariant / reduction / mathematical object. Outputs a Theory TM.
- `math-consultancy` (Mathematician) — pull-mode skill; must accept unless own queue is blocked. Output is a witnessed addendum TM attributed to both teams.

### Bench team
- `experiment-design` (Experimentalist) — turn a question into a falsifiable test; pre-register prediction in Hallway *before* running; result becomes a TM regardless of outcome.
- `empirical-probe` (Materials) — survey datasets/libraries/prior-art/instruments; output is the materials TM + curated source list pushed to the Librarian.

### Invention team
- `invention-disclosure` (Inventor) — patent-disclosure-shaped artifact paired with a TM. Conception date, witness sign-off, prior-art delta, claims sketch, reproducibility statement. The lab does not file patents; the form is used to force concreteness.
- `handoff-document` (Translator) — 3-stage productization, enforced as one skill with three required stages: (1) lab-model spec, (2) pre-production design with interfaces and tolerances, (3) user-ready handoff with test fixtures, runbook, rollback. Cannot ship stage 3 without stages 1 and 2 on file.

### Network team
- `problem-broker` (Systems Engineer) — watch the user's real-world "network"; surface friction as candidate problems on `problem-board/`. Proposed, not assigned.
- `library-push` (Librarian) — on every new TM/Hallway entry, search prior memos for relevance and push top-K to relevant researcher queues as citation suggestions. Not search; push.
- `colloquium-curation` (Librarian) — schedule the weekly Colloquium, produce the "what's hot" digest, prune Hallway entries that read like logs.

## 6. Operating cadence

### 6.1 Per-cycle loop (every action by every researcher)

1. `hallway-traversal` — read last N entries from other teams; post own short note.
2. Choose next action from *directed* or *curiosity* queue, per the 60/40 default split (configurable per researcher).
3. Do the action. If it produces a result, write a TM (witnessed by a peer agent who reads and signs with structured critique). If half-result, write a Hallway entry.
4. Librarian's `library-push` fires on the new TM/Hallway entry; adjacent researchers receive citation suggestions.

### 6.2 Weekly loop

- Each researcher writes a 5-minute briefing into `colloquium/YYYY-WW.md`.
- Librarian curates "what's hot this week."
- Director runs `continuation-review` with CEO; read-only on curiosity threads.
- Director posts ≤1 `instigation-question` per researcher.

### 6.3 Monthly loop

- CEO writes `monthly-summary` for the user.
- Patron-budget review: CEO names iteration budgets for each active thread for the next month; writes budget-defense memo if any thread was challenged.

### 6.4 Two-track mechanics

- Each researcher's queue file lives at `agents/<role>/queue.md` with two named sections: `## Directed` and `## Curiosity`.
- The Directed section is writable by the CEO (via `intake-triage`) and the Director (only via `instigation-question`, only as a suggestion the researcher can decline).
- The Curiosity section is writable *only by the researcher*. Hard policy. Enforced by `make check`.
- Curiosity items can be *promoted* to Directed only with the researcher's own consent, captured as a one-line addendum in the queue file.

### 6.5 Escalation policy

**Escalates to user (via CEO):**
- Real blocker requiring a real-world action (paid API, dataset, hardware decision).
- Sunset touching the user's mission directly (Director writes the sunset memo first; CEO routes).
- Monthly summary, on schedule.
- Anything the user flagged at onboarding.

**Does not escalate:**
- Curiosity threads that didn't pan out (internal sunset; lesson lives in the TM).
- Director instigations the researcher declined (Hallway-visible only).
- Hallway entries pruned by the Librarian.

## 7. Boundaries & anti-cargo-cult guardrails

The README's `## Boundaries` section will state:

- The lab drafts memos, prototypes, proposals, and handoff docs *for human review*. It does not ship to the user's production systems on its own authority, file actual patents, submit to actual journals, or claim peer-review.
- The wild-duck / curiosity track is freedom of *method*, not freedom of *fence*. Curiosity threads must still trace a plausible link to `MISSION.md`. The Librarian flags drift.
- The Director never overrides a researcher's curiosity queue.
- Mervin Kelly is not on staff. Patience, taste, and mentorship are *configured*, not magic the configuration confers. The lab is an aspiration with scaffolding.
- "Bell Labs" is a name homage. This is not affiliated with Nokia / Nokia Bell Labs.

### `make check` enforces

- Every researcher's `queue.md` has both sections and only the researcher has written to Curiosity.
- Every TM has a peer witness signature.
- Every TM cites at least one Hallway entry or prior TM (no orphan claims).
- Director `instigation-question` rate ≤ 1 per researcher per cycle.
- Translator stage 3 has stages 1 and 2 on file in `handoff/`.

## 8. Directory layout

```
bell-labs/
├── COMPANY.md              # generated from manifest
├── MISSION.md              # written by onboarding-mission-interview at install
├── manifest.yaml           # canonical source
├── teams/                  # 4 team manifests (generated)
├── agents/                 # 9 AGENTS.md files (generated)
│   └── <role>/queue.md     # per-researcher two-track queue (created at first use)
├── skills/                 # 22 SKILL.md files (port-original, hand-authored)
├── hallway/                # YYYY-MM-DD-<author>-<slug>.md short notes (runtime)
├── colloquium/             # YYYY-WW.md weekly briefings + Librarian digest (runtime)
├── memoranda/              # signed Technical Memoranda (runtime, primary output)
├── handoff/                # 3-stage Translator outputs per thread (runtime)
├── problem-board/          # Systems Engineer's candidate problems (runtime)
├── instigation/            # Director's tap-on-the-shoulder notes (runtime)
├── sunsets/                # project sunset memos (runtime)
├── images/                 # org chart (generated)
├── LICENSE                 # MIT
└── NOTICE                  # name-homage note re: Nokia Bell Labs
```

Runtime directories are empty at install (each ships with a `README.md` explaining its role) and accumulate as the lab works.

## 9. Translation matrix — Bell Labs principle → this design

Condensed from the research brief. "Fidelity risk" flags translations where the agentic version is fragile or cargo-cult-prone.

| Bell Labs principle | This design | Fidelity risk |
|---|---|---|
| Long hallways force collision | The Hallway + blocking `hallway-traversal` precondition | Medium — only works if entries stay short and human-readable (Librarian prunes) |
| Critical mass + co-location | 8 active researchers across 4 teams; shared scratchpad | Low |
| Supply department / craftsmen | Implicit: agents use the platform's tool/sandbox layer | Low — the cheapest principle to copy |
| Tap-on-the-shoulder problem assignment | Director's `instigation-question`; ≤1 per researcher per cycle | High — requires real taste; LLM "PMs" tend to over-prescribe |
| Useful freedom / narrow fence | `MISSION.md` as durable fence; method is free inside | Medium — fence must be defended at onboarding |
| Phenotype hiring (curiosity + hands + head) | Persona descriptions per agent emphasize the trait combination | Medium-high — character is hard to evaluate in a config |
| Juniors paired with masters | Peer-witness signature on every TM; Director's continuation review | Medium — rotation kills it; persistence must be preserved |
| 5–25 year horizons | Named `patron-budget` per thread, defended in writing | Very high — incentives push every system toward short loops |
| Technical Memoranda culture | `technical-memorandum` as canonical output, witnessed | Low — trivial to enforce, high payoff |
| BSTJ / publication norm | Memoranda are first-class artifacts in `memoranda/`; user-shareable | Medium — depends on user's willingness to read long-form |
| Internal colloquia | Weekly `colloquium/YYYY-WW.md` + Librarian digest | Low-medium |
| Mathematical Research consultancy | Mathematician at 25% pull-rate, must accept | Medium — quality of theorist agent is the limiter |
| Systems engineers as problem brokers | Systems Engineer + `problem-board/` | High — this is the boundary modern attempts miss; the design weights it explicitly |
| Western Electric handoff | Translator + `handoff-document` 3-stage skill | Medium — easy to spec, hard to make actually own quality |
| Patent disclosure flow | `invention-disclosure` artifact paired with TM | Low |
| Department heads decide hiring + problems | Team manifests + Director continuation review | High — governance churn destroys multi-year arcs |
| Lab directors approve continuation | Director + CEO weekly continuation review | Medium |
| Sunset by reassignment, not firing | `project-sunset` memo as anti-firing artifact | Medium-low |
| 1956 Consent Decree (mandatory openness) | Memoranda are user-visible by default | Low-medium |
| Monopoly-rent funding base | The user's commitment to the mission *is* the patient capital | Very high — this is *the* structural condition; without it, the rest decays |
| Kelly as patron, not boss | CEO explicitly separated from instigator; `patron-budget` skill | High — cultural posture, easily lost under product pressure |
| "Improve the network" north star | `MISSION.md` written at onboarding | Medium — tempting to multiplex; one company should have one mission |
| Library as active routing | Librarian's `library-push` (push, not search) | Low-medium |

## 10. Open questions deferred to implementation

These are decisions I would prefer to resolve while writing the skills, not now:

- **Witness countersignature mechanism.** "Peer agent reads and signs" needs a concrete protocol — which peer (random within team? rotation? Director-assigned?) and what counts as a valid critique. To be decided in `technical-memorandum/SKILL.md`.
- **Forced-traversal N.** Default "last N Hallway entries from other teams" needs a number. Probably N=10, configurable in `manifest.yaml`.
- **Curiosity-queue seeding.** How does a researcher seed the curiosity queue at onboarding before there is any Hallway history? Probably from `MISSION.md` + the agent's archetype literature.
- **Sunset trigger.** Who or what triggers a sunset review? The Director on continuation review, or a calendar (e.g. quarterly), or a budget exhaustion. Probably all three; the Director writes the memo regardless.
- **Org-chart image.** `images/orgchart.svg` — generation pattern follows the existing companies; nothing novel.
- **`make check` rules.** The five enforcements in §7 each need a concrete Python check in `scripts/check.py` shared with the rest of the catalog.
- **Onboarding refusal.** What if the user *won't* declare a mission? `onboarding-mission-interview` must refuse gracefully — explain that without a fence the lab is just chat, and exit. Phrasing matters; design it explicitly.

## 11. Non-goals

- This is not a generic invention lab for one-off prompts. It is a *durable-mission* lab. Users who want one-shot ideation should use a different company.
- It does not file patents, submit to journals, or sign user-binding documents.
- It does not replace the academic-research or financial-services companies. Those are narrower; this is a broader research-org template the user steers via `MISSION.md`.
- It is not a recreation. Bell Labs ran on monopoly rents, the AT&T technical surface, and Mervin Kelly. We have none of those. We have scaffolding, opinionated structure, and the discipline of writing things down.

## 12. References

Research synthesized into this design. (Full set in the conversation transcript that produced this spec.)

- Jon Gertner, *The Idea Factory: Bell Labs and the Great Age of American Innovation* (2012).
- Mervin Kelly, "The Bell Telephone Laboratories — An Example of an Institute of Creative Technology" (1950).
- Brian Potter, "What Would It Take to Recreate Bell Labs?" — Construction Physics.
- areoform, "Why Bell Labs Worked" — 1517 Fund Substack.
- Watzinger, Fackler, Nagler, Schnitzer, "How Antitrust Enforcement Can Spur Innovation: Bell Labs and the 1956 Consent Decree," *American Economic Journal: Economic Policy* (2020).
- Computer History Museum / ETHW / APS milestones on transistor, photovoltaic, CCD, cellular.
- Shannon, "A Mathematical Theory of Communication," BSTJ (1948).
- D. H. Ring, "Mobile Telephony — Wide Area Coverage," internal TM (1947).
- Ritchie, "The Evolution of the Unix Time-sharing System."
- HHMI Janelia model documentation; Convergent Research / FRO model.
- Collison & Cowen, "We Need a New Science of Progress," *The Atlantic* (2019).
