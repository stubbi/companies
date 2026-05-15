# Legal Services — Agent Company port of `anthropics/claude-for-legal`

**Status:** Approved (2026-05-15)
**Catalog slug:** `legal-services`
**Upstream:** [`anthropics/claude-for-legal`](https://github.com/anthropics/claude-for-legal) @ `9cecd91b0f26f732d18315afc3c9bb5ff99e0fbb` (2026-05-12)
**Upstream license:** Apache-2.0

## Goal

Port `anthropics/claude-for-legal` into the `stubbi/companies` catalog as a sibling to `financial-services`. Preserve upstream by reference (no vendoring); enforce strong attorney-review boundaries; ship a `make build` / `make check` / `make test` loop that drift-detects against the pinned upstream.

## Non-goals (v0.1.0)

- Per-plugin scheduled-agent `.md` files (e.g., `commercial-legal/agents/deal-debrief.md`). Documented in NOTICE as upstream features not yet ported.
- Top-level `managed-agent-cookbooks/` (5 cookbooks). Same disposition.
- `CONNECTORS.md` MCP server list. The upstream `.mcp.json` belongs to runtime, not to the company manifest.
- Port-original skills beyond the four CEO-owned coordination skills.

## Structure

### Agents and teams

13 agents — 1 port-original CEO + 12 specialists (one per upstream practice-area plugin) — in 4 teams.

| Team slug | Team name | Agents |
|---|---|---|
| commercial-transactions | Commercial & Transactions | `commercial-legal`, `corporate-legal`, `employment-legal` |
| regulatory-compliance | Regulatory & Compliance | `privacy-legal`, `ai-governance-legal`, `regulatory-legal`, `product-legal` |
| ip-disputes | IP & Disputes | `ip-legal`, `litigation-legal` |
| academy-tooling | Legal Academy & Tooling | `law-student`, `legal-clinic`, `legal-builder-hub` |

Specialist agent names map 1:1 to upstream plugin directory names. Agent titles use the plugin's practice-area phrasing (e.g., `Commercial Contracts Specialist`, `M&A and Corporate Specialist`, `Litigation Portfolio Manager`).

The CEO is top-level (no team). The four teams report to the CEO via `reportsTo: ../../agents/ceo/AGENTS.md` (same pattern as `financial-services` and `academic-research`).

### CEO skills (port-original)

| Slug | Purpose |
|---|---|
| `intake-triage` | Classify inbound matters and route to the right practice area. |
| `cross-practice-coordination` | Coordinate handoffs when work spans practice areas (e.g., M&A diligence touching IP + employment + privacy). |
| `escalation-routing` | When a specialist hits a blocker, decide between retry, reassign, or escalate-to-human. |
| `weekly-summary` | Compose the company-level weekly digest — what shipped, what's blocked, what needs review. |

These exactly mirror the precedent set by `financial-services/scripts/build.py` and `academic-research/manifest.yaml` for the CEO role.

### Specialist skills (upstream-referenced)

Total: 150 upstream skills (sum of `<plugin>/skills/*/SKILL.md` across the 12 plugins).

Per-plugin skill counts (from upstream HEAD `9cecd91b`):

| Plugin / Agent | Skills |
|---|---|
| `commercial-legal` | 12 |
| `corporate-legal` | 13 |
| `employment-legal` | 20 |
| `privacy-legal` | 9 |
| `product-legal` | 7 |
| `regulatory-legal` | 9 |
| `ai-governance-legal` | 10 |
| `ip-legal` | 12 |
| `litigation-legal` | 19 |
| `law-student` | 13 |
| `legal-clinic` | 16 |
| `legal-builder-hub` | 10 |
| **Total** | **150** |

### Skill slug namespacing

Unlike `financial-services` (where many upstream agents share the same file for shared skills like `xlsx-author`), `claude-for-legal` ships **different files with the same skill slug** across plugins — `cold-start-interview`, `customize`, and `matter-workspace` each appear in 12 plugins, customized to each practice area. `use-case-triage`, `reg-gap-analysis`, and `policy-monitor` each appear in 2 plugins (`privacy-legal` and `ai-governance-legal`) with different content.

To preserve these as distinct skills, we namespace every upstream-referenced skill with its plugin slug, joined by `--`:

- Manifest key + folder: `commercial-legal--review`
- Upstream path: `commercial-legal/skills/review/SKILL.md`
- Filesystem: `legal-services/skills/commercial-legal--review/SKILL.md`

The `--` separator avoids ambiguity (no plugin slug contains `--`) and is filesystem-safe. The four CEO port-original skills stay un-namespaced (`intake-triage`, etc.) because they have no upstream owner.

## Layout

```
legal-services/
├── COMPANY.md                          # generated
├── teams/<slug>/TEAM.md                # generated × 4
├── agents/<slug>/AGENTS.md             # generated × 13 (CEO + 12 specialists)
├── skills/<slug>/SKILL.md              # generated × 150 upstream-referenced;
│                                       # hand-authored × 4 port-original
├── manifest.yaml                       # canonical source — edit this, run `make build`
├── scripts/__init__.py
├── scripts/build.py                    # manifest generator (adapted from financial-services)
├── scripts/check.py                    # validator
├── Makefile                            # build / check / test / bump
├── pyproject.toml
├── images/org-chart.dot                # generated
├── images/org-chart.png                # generated
├── tests/                              # pytest unit tests for the generator
├── LICENSE                             # Apache-2.0 (matches upstream)
└── NOTICE                              # upstream attribution + deferred-feature note
```

## Build pipeline

`scripts/build.py` is adapted from `financial-services/scripts/build.py`. Differences:

1. **No canonical-owner resolution.** Each upstream-referenced skill has exactly one upstream file (determined by the namespace prefix). Drop the `resolve_canonical_paths` and `fetch_upstream_skill_inventory` machinery.
2. **New upstream path pattern.** From a manifest slug `commercial-legal--review`, derive plugin = `commercial-legal`, bare = `review`, path = `commercial-legal/skills/review/SKILL.md`.
3. **Specialist agent metadata.** Each specialist agent's `metadata.sources[0].url` points to `https://github.com/anthropics/claude-for-legal/tree/<sha>/<plugin>`.
4. **Tags.** Specialist agents tag `["legal", "<team-slug>"]`; CEO tags `["legal", "executive"]`.

Everything else (Manifest dataclasses, frontmatter rendering, COMPANY/TEAM/AGENTS emission, org-chart DOT, port-original SKILL.md guard) carries over unchanged.

`scripts/check.py` is essentially identical to `financial-services/scripts/check.py`:

1. Schema validation against `REQUIRED_FIELDS`.
2. Cross-reference check: every skill named in an `AGENTS.md` must have a corresponding `skills/<slug>/SKILL.md`.
3. Content-hash freshness: for every `referenced` source, fetch upstream at the pinned commit and verify `sha256` matches.

## Tests

`tests/` mirrors `financial-services/tests/` structure:

- `tests/fixtures/manifest_minimal.yaml` — small fixture (1 CEO, 2 specialists across 1 team, 1 port-original skill, 2 upstream-referenced skills) with a `--`-namespaced slug.
- `tests/test_build.py` — exercises `load_manifest`, `emit_company`, `emit_teams`, `emit_agents`, `emit_skills` (port-original path); the upstream fetch is stubbed.
- `tests/test_check.py` — exercises `parse_frontmatter`, `validate_frontmatter`, `check_cross_references`, error paths.

Network-bound checks (`check_content_hashes`) are tested via the actual `make check` (CI), not in pytest.

## Boundaries

Adapted from the upstream README's attorney-review paragraph:

> Nothing in this package constitutes legal advice. Every output is a draft for
> attorney review — not a legal conclusion, not a substitute for a lawyer. These
> agents draft work product (memos, redlines, claim charts, deposition outlines,
> review reports, policies, classifications) for review by a qualified attorney.
> They do not file briefs, send demand letters, issue legal holds, or take
> positions on behalf of any party; every output is staged for human sign-off.
> The attorney using the package — not the package, and not Anthropic — is
> responsible for the legal positions taken in their work product.

The COMPANY.md and `README.md` both surface this paragraph (with a `> [!IMPORTANT]` callout in the README). The top-level `stubbi/companies` README links to the company's `Boundaries` section in its catalog entry, mirroring `financial-services` and `academic-research`.

## Catalog integration

- Top-level `README.md`: bump `companies-3-22c55e` → `companies-4-22c55e`; insert a `### [Legal Services](./legal-services)` block between `Academic Research` and `Bell Labs` (alphabetical-ish ordering by name; matches existing `Financial Services` → `Academic Research` → `Bell Labs` ordering, with `Legal Services` slotting after `Bell Labs` since it's the newest port).

Actually, ordering is currently: Financial Services → Academic Research → Bell Labs, in PR-merge order rather than alphabetical. **We append `Legal Services` after `Bell Labs`** for consistency with the existing merge-order convention.

- The block follows the same template (Source row, Agents/Skills/License table, paragraph summary, Boundaries pull-quote, "Community port" disclaimer).

## Version & affiliation

- `version: 0.1.0` (first port).
- `affiliation: "Community port. Not affiliated with or endorsed by Anthropic."`
- License: `Apache-2.0` (matches upstream).

## Open questions

None at design time. All scope and naming decisions are committed per the design review.

## References

- Prior ports for shape: [`financial-services`](../../../financial-services/) (canonical reference), [`academic-research`](../../../academic-research/).
- Prior port specs for documentation pattern: `docs/superpowers/specs/2026-05-14-bell-labs-company-design.md`.
