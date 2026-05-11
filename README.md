<div align="center">

# stubbi/companies

**Hand-crafted [Paperclip](https://github.com/paperclipai/paperclip) Agent Companies, ready to deploy.**

[![CI](https://github.com/stubbi/companies/actions/workflows/ci.yml/badge.svg)](https://github.com/stubbi/companies/actions/workflows/ci.yml)
[![License: MIT (wrapper)](https://img.shields.io/badge/wrapper-MIT-yellow.svg)](LICENSE)
[![Powered by Paperclip](https://img.shields.io/badge/powered_by-Paperclip-2563eb)](https://github.com/paperclipai/paperclip)
[![Companies](https://img.shields.io/badge/companies-2-22c55e)](#companies)

</div>

---

## Quick start

```bash
npx companies.sh add stubbi/companies/financial-services
```

That's it — your Paperclip instance now has an 11-agent finance company on the board, with org chart, teams, and skills wired up.

[How does this work?](#how-it-works) · [What's an Agent Company?](#whats-an-agent-company) · [Browse the catalog](#companies)

---

## What's an Agent Company?

An **Agent Company** is a fully-configured team of AI agents — org chart, teams, skills, governance — packaged so you can `import` it into [Paperclip](https://github.com/paperclipai/paperclip) and have a working AI workforce in minutes. Each company in this repo is:

- **Domain-specific.** Finance, legal, research, ops — not generic prompt wrappers.
- **Skill-loaded.** Every agent ships with the workflows it needs to do its job.
- **Runtime-agnostic.** Works with Claude Code, Codex, Gemini, OpenCode, Cursor, Pi, and Hermes via Paperclip's adapter chain — Claude is the reference runtime, others run with varying skill polish.
- **Boundary-aware.** Agents know what they can and cannot decide; outputs are staged for human sign-off where regulation requires it.
- **Provenance-honest.** Community ports are pinned by upstream commit SHA, hashed for drift detection, and preserve upstream license + attribution. Nothing is vendored or forked.

## How it works

```bash
npx companies.sh add stubbi/companies/<company-slug>
```

`companies.sh` resolves the path to a directory in this repo, validates the company manifest, and imports the team into your Paperclip instance. Each company directory is self-contained:

```
<company-slug>/
├── COMPANY.md          # company-level manifest (generated)
├── teams/              # team manifests (generated)
├── agents/             # one AGENTS.md per role (generated)
├── skills/             # one SKILL.md per skill — generated for upstream-referenced,
│                       # hand-authored for port-original
├── manifest.yaml       # canonical source — edit this, run `make build`
├── images/             # org chart (generated)
├── LICENSE             # company-level license
└── NOTICE              # upstream attribution where applicable
```

Companies that port an external repo (like `financial-services`) ship a `make bump SHA=<new-sha>` workflow that re-fetches upstream by content hash and re-generates the manifest. The pinned SHA is the contract.

## Companies

### [Financial Services](./financial-services)

> Community port of [`anthropics/financial-services`](https://github.com/anthropics/financial-services) (Anthropic's "Claude for Financial Services") into the Agent Companies format. Runtime-agnostic; Claude is the reference runtime, Codex / Gemini / OpenCode / Hermes / Cursor / Pi are supported via the adapter chain with varying skill polish.

```bash
npx companies.sh add stubbi/companies/financial-services
```

| | |
|---|---|
| **Agents** | 11 (1 CEO + 10 specialists across 4 teams) |
| **Skills** | 31 referenced upstream + 4 port-original (CEO-owned) |
| **License** | Apache-2.0 |
| **Source** | [`anthropics/financial-services`](https://github.com/anthropics/financial-services) at pinned commit `57772c3f` |

The CEO handles intake triage, cross-team coordination, escalation routing, and weekly summaries. Specialists cover coverage & advisory, research & modeling, fund admin & finance ops, and KYC. Every output is staged for human sign-off — agents do not execute trades, post to a ledger, or approve onboarding.

[Company README →](./financial-services/README.md)

> **Boundaries.** Nothing in `financial-services` constitutes investment, legal, tax, or accounting advice. These agents draft analyst work product (models, memos, research notes, reconciliations) for review by a qualified professional. They do not make investment recommendations, execute transactions, bind risk, post to a ledger, or approve onboarding. You are responsible for verifying outputs and for compliance with the laws and regulations that apply to your firm. See the [company's Boundaries section](./financial-services/README.md#boundaries) for full detail.

> **Community port. Not affiliated with or endorsed by Anthropic.** "Claude" is a trademark of Anthropic, PBC.

### [Academic Research](./academic-research)

> Community port of [`Imbad0202/academic-research-skills`](https://github.com/Imbad0202/academic-research-skills) (the ARS pipeline) into the Agent Companies format. Runtime-agnostic via the Paperclip adapter chain — Claude is the reference runtime, others run with varying skill polish.

```bash
npx companies.sh add stubbi/companies/academic-research
```

| | |
|---|---|
| **Agents** | 5 (1 CEO + 4 stage owners across 4 teams) |
| **Skills** | 4 referenced upstream + 4 port-original (CEO-owned) |
| **License** | ![NC](https://img.shields.io/badge/CC%20BY--NC%204.0-non--commercial-orange) |
| **Source** | [`Imbad0202/academic-research-skills`](https://github.com/Imbad0202/academic-research-skills) at pinned commit `58dad474` |

The CEO handles intake triage, pipeline orchestration, checkpoint coordination, and escalation. Stage owners cover Research (Stage 1), Writing & Revision (Stages 2 / 4 / 4' / 5), Review (Stages 3 / 3'), and Integrity & Pipeline (Stages 2.5 / 4.5 / 6). Every output is staged for human sign-off — agents do not submit to journals, sign authorship statements, or attest to research integrity. The pipeline's two integrity gates and 7-mode AI failure checklist are mandatory and not skippable.

[Company README →](./academic-research/README.md)

> ⚠️ **Non-commercial use only.** Upstream is licensed CC BY-NC 4.0 and this port preserves that restriction. Personal research, academic work, and non-commercial collaboration: yes. Commercial services, paid offerings, work-for-hire: no. See the [company's LICENSE](./academic-research/LICENSE) and [NOTICE](./academic-research/NOTICE).

> **Boundaries.** Nothing in `academic-research` constitutes peer-reviewed scholarship on its own. These agents draft research artifacts (literature searches, methodology blueprints, outlines, drafts, review reports, formatted manuscripts) for review by a qualified human researcher. They do not submit to journals, sign authorship statements, make editorial decisions, or attest to research integrity on the user's behalf. See the [company's Boundaries section](./academic-research/README.md#boundaries) for full detail.

> **Community port. Not affiliated with or endorsed by Imbad0202 or the ARS authors.**

---

## Repo conventions

- **Top-level wrapper** is MIT — the README, layout, top-level docs, and CI scaffolding.
- **Each company** ships its own `LICENSE` and `NOTICE`. Read those before deploying — community ports preserve upstream license terms (typically Apache-2.0 for Anthropic ports).
- **Regulated domains** (finance, legal, medical) have a `Boundaries` section in the company README. Read it before assigning real work.
- **Bumping a port:** `cd <company> && make bump SHA=<new-sha>` rewrites the manifest, regenerates all artifacts, and re-validates content hashes against the new upstream commit.
- **Validation:** every company has `make build`, `make check`, and `make test` targets. CI runs `make test` and `make check` on every PR.

## Contributing

This is a personal catalog with one maintainer and one taste. I'm happy to merge well-scoped fixes — typos, link rot, schema drift, upstream SHA bumps. For new companies, the cleanest path is **your own `<your-username>/companies` repo**: `companies.sh` installs are repo-agnostic, so you don't need a PR here. Self-published catalogs let you keep your own bump cadence and curatorial voice.

If you do want to contribute to this catalog, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Related

- [Paperclip](https://github.com/paperclipai/paperclip) — open-source orchestration for zero-human companies. The runtime these companies plug into.
- [paperclipai/companies](https://github.com/paperclipai/companies) — official Paperclip catalog (16+ companies). Companies submitted there go through maintainer review.
- [VectifyAI/PageIndex](https://github.com/VectifyAI/PageIndex) — vectorless tree-traversal retrieval over long PDFs. Useful when your agents work with long professional documents.

## License

Top-level wrapper: [MIT](LICENSE). Individual companies have their own licenses — see each company's `LICENSE` file. Where individual companies operate in regulated domains (finance, legal, medical), each company's README documents the appropriate boundaries — read those before deploying.

---

<div align="center">

Made with care by [Jannes Stubbemann](https://github.com/stubbi). Powered by [Paperclip](https://github.com/paperclipai/paperclip).

</div>
