# Legal Services Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port `anthropics/claude-for-legal` @ `9cecd91b0f26f732d18315afc3c9bb5ff99e0fbb` into the `stubbi/companies` catalog as a sibling to `financial-services` and `academic-research`.

**Architecture:** Manifest-driven (single `manifest.yaml` is canonical). `scripts/build.py` regenerates `COMPANY.md`, `teams/*/TEAM.md`, `agents/*/AGENTS.md`, `skills/*/SKILL.md` (for upstream-referenced skills), and `images/org-chart.{dot,png}`. Port-original CEO skill files are hand-authored and left untouched by build. `scripts/check.py` validates schema, cross-references, and content-hash drift against pinned upstream.

**Tech Stack:** Python 3.11+, PyYAML, pytest, GitHub Hub CLI (`gh`) for upstream fetches, Graphviz `dot` for org chart.

**Working directory:** `/Users/jannesstubbemann/repos/companies` on branch `legal-services` (already created).

**Spec:** `docs/superpowers/specs/2026-05-15-legal-services-design.md`.

---

## File Structure

| Path | Responsibility |
|---|---|
| `legal-services/manifest.yaml` | Canonical source — 13 agents, 4 teams, 154 skills, upstream pin |
| `legal-services/Makefile` | `build` / `check` / `test` / `bump` / `clean` targets |
| `legal-services/pyproject.toml` | Python package metadata + pytest config |
| `legal-services/LICENSE` | Apache-2.0 (matches upstream) |
| `legal-services/NOTICE` | Upstream attribution + deferred-feature note |
| `legal-services/.gitignore` | Skip Python build artifacts |
| `legal-services/scripts/__init__.py` | Empty (package marker) |
| `legal-services/scripts/build.py` | Manifest → markdown generator (adapted from `financial-services`) |
| `legal-services/scripts/check.py` | Schema + cross-ref + content-hash validator |
| `legal-services/scripts/extract_upstream_metadata.py` | One-shot helper: fetch upstream SKILL.md frontmatter, emit starter YAML for manifest skills block |
| `legal-services/tests/__init__.py` | Empty |
| `legal-services/tests/fixtures/manifest_minimal.yaml` | Small fixture for unit tests |
| `legal-services/tests/test_build.py` | Unit tests for build pipeline |
| `legal-services/tests/test_check.py` | Unit tests for validators |
| `legal-services/skills/intake-triage/SKILL.md` | CEO port-original |
| `legal-services/skills/cross-practice-coordination/SKILL.md` | CEO port-original |
| `legal-services/skills/escalation-routing/SKILL.md` | CEO port-original |
| `legal-services/skills/weekly-summary/SKILL.md` | CEO port-original |
| `legal-services/skills/<plugin>--<bare>/SKILL.md` | Generated × 150 (upstream-referenced) |
| `legal-services/agents/<slug>/AGENTS.md` | Generated × 13 |
| `legal-services/teams/<slug>/TEAM.md` | Generated × 4 |
| `legal-services/COMPANY.md` | Generated |
| `legal-services/images/org-chart.{dot,png}` | Generated |
| `legal-services/README.md` | Hand-authored (port of `financial-services/README.md` template) |
| `README.md` (top-level) | Bump `companies-3-22c55e` → `companies-4-22c55e`; insert `### [Legal Services]` block after Bell Labs |

---

## Task 1: Scaffold the company directory

**Files:**
- Create: `legal-services/Makefile`
- Create: `legal-services/pyproject.toml`
- Create: `legal-services/LICENSE`
- Create: `legal-services/NOTICE`
- Create: `legal-services/.gitignore`
- Create: `legal-services/scripts/__init__.py` (empty)
- Create: `legal-services/tests/__init__.py` (empty)

- [ ] **Step 1: Create the Makefile.**

Write `legal-services/Makefile`:

```makefile
.PHONY: build check test bump clean

build:
	python -m scripts.build

check:
	python -m scripts.check

test:
	pytest -v

# Update the upstream SHA pin in manifest.yaml, then rebuild + recheck.
# Usage: make bump SHA=<new-sha>
bump:
	@test -n "$(SHA)" || (echo "ERROR: pass SHA=<new-sha>" >&2; exit 1)
	sed -i.bak -E 's/^( {2}commit: ).*/\1$(SHA)/' manifest.yaml
	rm manifest.yaml.bak
	$(MAKE) build
	$(MAKE) check

clean:
	rm -rf COMPANY.md teams/ agents/ images/
	# Note: `skills/` is intentionally NOT cleaned because it contains port-original SKILL.md
	# files (CEO-owned) that must survive a regeneration. The build script overwrites
	# upstream-referenced SKILL.md in place.
```

- [ ] **Step 2: Create the pyproject.toml.**

Write `legal-services/pyproject.toml`:

```toml
[project]
name = "legal-services"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["pyyaml>=6.0"]

[project.optional-dependencies]
dev = ["pytest>=7.0"]

[tool.setuptools.packages.find]
include = ["scripts*"]

[tool.pytest.ini_options]
pythonpath = ["."]
```

- [ ] **Step 3: Create the LICENSE.**

Copy the upstream LICENSE (Apache-2.0) verbatim. Run:

```bash
cp /tmp/claude-for-legal/LICENSE legal-services/LICENSE
```

Confirm: `head -3 legal-services/LICENSE` shows the Apache 2.0 header.

- [ ] **Step 4: Create the NOTICE file.**

Write `legal-services/NOTICE`:

```
legal-services — Community port of anthropics/claude-for-legal

This package is a community port of Anthropic's "Claude for Legal" reference
agents and skills (https://github.com/anthropics/claude-for-legal) into the
Agent Companies format used by the stubbi/companies catalog.

Upstream:
  Repository:    anthropics/claude-for-legal
  Pinned commit: 9cecd91b0f26f732d18315afc3c9bb5ff99e0fbb (2026-05-12)
  License:       Apache-2.0 (preserved by this port)

Skill content is referenced upstream by content-hashed path, not vendored.
Run `make check` to verify upstream files have not drifted from the pinned hashes.

Deferred from this port (v0.1.0):
  * Per-plugin scheduled-agent .md files under each plugin's agents/ directory
    (e.g., commercial-legal/agents/deal-debrief.md). These represent managed-agent
    cron workflows; will be added in a follow-up release.
  * The top-level managed-agent-cookbooks/ directory (renewal-watcher,
    docket-watcher, launch-radar, reg-monitor, diligence-grid).
  * MCP server inventory (CONNECTORS.md / .mcp.json) — these belong to runtime
    configuration, not to the company manifest.

This port is not affiliated with or endorsed by Anthropic, PBC. "Claude" is a
trademark of Anthropic, PBC; this package's use of the name in upstream-attribution
contexts is purely descriptive.

Maintained by Jannes Stubbemann <jannes@paperclip.inc>.
```

- [ ] **Step 5: Create the .gitignore.**

Write `legal-services/.gitignore`:

```
__pycache__/
*.pyc
.pytest_cache/
*.egg-info/
build/
dist/
.venv/
```

- [ ] **Step 6: Create empty package markers.**

```bash
touch legal-services/scripts/__init__.py legal-services/tests/__init__.py
mkdir -p legal-services/tests/fixtures
```

- [ ] **Step 7: Commit.**

```bash
git add legal-services/Makefile legal-services/pyproject.toml legal-services/LICENSE \
        legal-services/NOTICE legal-services/.gitignore \
        legal-services/scripts/__init__.py legal-services/tests/__init__.py
git commit -m "legal-services: repo scaffolding (Makefile, pyproject, LICENSE, NOTICE)"
```

---

## Task 2: Test fixture

**Files:**
- Create: `legal-services/tests/fixtures/manifest_minimal.yaml`

- [ ] **Step 1: Write the fixture.**

Write `legal-services/tests/fixtures/manifest_minimal.yaml`:

```yaml
schema: agentcompanies/v1
slug: test-co
name: Test Co
description: Fixture for legal-services build/check unit tests.
version: 0.1.0
license: Apache-2.0
authors: [{name: Test, email: t@example.com}]
goals: [Test]
tags: [test]
upstream:
  repo: example/upstream
  commit: deadbeef
  license: Apache-2.0
affiliation: "Test"
teams:
  team-a:
    name: Team A
    description: Test team
agents:
  alpha:
    name: Alpha
    title: Alpha Specialist
    team: team-a
    description: Test agent — wraps the alpha-legal plugin.
    skills: [alpha-legal--review]
skills:
  alpha-legal--review:
    name: Review
    description: Test upstream-referenced skill.
```

Note: the agent `alpha` "wraps" a notional `alpha-legal` plugin. The skill slug `alpha-legal--review` exercises the new `--` namespace parsing.

- [ ] **Step 2: Commit.**

```bash
git add legal-services/tests/fixtures/manifest_minimal.yaml
git commit -m "legal-services: test fixture (minimal manifest with namespaced slug)"
```

---

## Task 3: Build pipeline — manifest loading + frontmatter helpers (TDD)

**Files:**
- Create: `legal-services/scripts/build.py`
- Create: `legal-services/tests/test_build.py`

This task ports the parts of `financial-services/scripts/build.py` that change minimally — dataclasses, manifest loader, frontmatter renderer, hash helper. The behavior is identical; only the module location changes.

- [ ] **Step 1: Write the failing test for `load_manifest`.**

Write `legal-services/tests/test_build.py`:

```python
import yaml
from pathlib import Path
from scripts.build import load_manifest


def test_load_manifest_returns_structured_object():
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    assert m.slug == "test-co"
    assert m.upstream.commit == "deadbeef"
    assert "alpha" in m.agents
    assert m.agents["alpha"].team == "team-a"
    assert m.agents["alpha"].skills == ["alpha-legal--review"]
    assert "alpha-legal--review" in m.skills
    assert "team-a" in m.teams
```

- [ ] **Step 2: Run test — expect ImportError.**

```bash
cd legal-services && pytest tests/test_build.py::test_load_manifest_returns_structured_object -v
```

Expected: `ModuleNotFoundError: No module named 'scripts.build'`.

- [ ] **Step 3: Implement the dataclasses + load_manifest.**

Write `legal-services/scripts/build.py`:

```python
"""Build script for the legal-services Agent Company package.

Generates COMPANY.md, TEAM.md, AGENTS.md, SKILL.md files plus the org-chart
image from the canonical manifest.yaml. Adapted from
financial-services/scripts/build.py.
"""
from __future__ import annotations

import base64
import hashlib
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent

# Separator used in skill slugs to namespace by upstream plugin.
# Example: "commercial-legal--review" → plugin "commercial-legal", bare "review".
NAMESPACE_SEP = "--"


@dataclass
class Author:
    name: str
    email: str


@dataclass
class Upstream:
    repo: str
    commit: str
    license: str


@dataclass
class Team:
    name: str
    description: str


@dataclass
class Agent:
    name: str
    title: str
    description: str
    skills: list[str]
    team: str | None = None  # None = top-level (reports to company)


@dataclass
class Skill:
    name: str
    description: str
    port_original: bool = False  # True = hand-authored in this repo, not from upstream


@dataclass
class Manifest:
    schema: str
    slug: str
    name: str
    description: str
    version: str
    license: str
    authors: list[Author]
    goals: list[str]
    tags: list[str]
    upstream: Upstream
    affiliation: str
    teams: dict[str, Team]
    agents: dict[str, Agent]
    skills: dict[str, Skill]


def load_manifest(path: Path) -> Manifest:
    raw: dict[str, Any] = yaml.safe_load(path.read_text())
    return Manifest(
        schema=raw["schema"],
        slug=raw["slug"],
        name=raw["name"],
        description=raw["description"],
        version=raw["version"],
        license=raw["license"],
        authors=[Author(**a) for a in raw["authors"]],
        goals=list(raw["goals"]),
        tags=list(raw["tags"]),
        upstream=Upstream(**raw["upstream"]),
        affiliation=raw["affiliation"],
        teams={k: Team(**v) for k, v in raw["teams"].items()},
        agents={k: Agent(**v) for k, v in raw["agents"].items()},
        skills={k: Skill(**v) for k, v in raw["skills"].items()},
    )


def compute_content_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _frontmatter(data: dict[str, Any]) -> str:
    return "---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n"
```

- [ ] **Step 4: Run test — expect PASS.**

```bash
cd legal-services && pytest tests/test_build.py::test_load_manifest_returns_structured_object -v
```

Expected: PASS.

- [ ] **Step 5: Add a test for `compute_content_hash`.**

Append to `legal-services/tests/test_build.py`:

```python
from scripts.build import compute_content_hash


def test_compute_content_hash_is_sha256_hex():
    h = compute_content_hash(b"hello world")
    assert h == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
```

- [ ] **Step 6: Run — expect PASS.**

```bash
cd legal-services && pytest tests/test_build.py -v
```

- [ ] **Step 7: Commit.**

```bash
git add legal-services/scripts/build.py legal-services/tests/test_build.py
git commit -m "legal-services: build.py — manifest loader + dataclasses + hash helper"
```

---

## Task 4: Build pipeline — namespaced upstream path resolver (TDD)

This task implements the **key difference** from `financial-services`: deriving the upstream path from a namespaced skill slug.

**Files:**
- Modify: `legal-services/scripts/build.py`
- Modify: `legal-services/tests/test_build.py`

- [ ] **Step 1: Write the failing test.**

Append to `legal-services/tests/test_build.py`:

```python
from scripts.build import upstream_path_for_skill, NAMESPACE_SEP


def test_upstream_path_for_namespaced_slug():
    assert (
        upstream_path_for_skill("commercial-legal--review")
        == "commercial-legal/skills/review/SKILL.md"
    )
    assert (
        upstream_path_for_skill("law-student--socratic-drill")
        == "law-student/skills/socratic-drill/SKILL.md"
    )


def test_upstream_path_for_skill_with_no_namespace_raises():
    import pytest

    with pytest.raises(ValueError, match="not namespaced"):
        upstream_path_for_skill("orphan-slug")


def test_upstream_path_for_skill_double_dashed_bare_works():
    """A bare skill slug may itself contain a single dash. Only the FIRST '--' splits."""
    assert (
        upstream_path_for_skill("ai-governance-legal--use-case-triage")
        == "ai-governance-legal/skills/use-case-triage/SKILL.md"
    )
```

- [ ] **Step 2: Run — expect ImportError.**

```bash
cd legal-services && pytest tests/test_build.py::test_upstream_path_for_namespaced_slug -v
```

- [ ] **Step 3: Implement `upstream_path_for_skill`.**

Append to `legal-services/scripts/build.py`:

```python
def upstream_path_for_skill(slug: str) -> str:
    """Derive the upstream SKILL.md path from a namespaced manifest slug.

    Slug format: "<plugin>--<bare-skill>"; the bare-skill portion may itself
    contain single dashes (e.g., "use-case-triage"), so we split on the FIRST
    occurrence of the namespace separator only.
    """
    if NAMESPACE_SEP not in slug:
        raise ValueError(f"skill slug {slug!r} is not namespaced (missing {NAMESPACE_SEP!r})")
    plugin, bare = slug.split(NAMESPACE_SEP, 1)
    return f"{plugin}/skills/{bare}/SKILL.md"
```

- [ ] **Step 4: Run — expect PASS.**

```bash
cd legal-services && pytest tests/test_build.py -v
```

- [ ] **Step 5: Commit.**

```bash
git add legal-services/scripts/build.py legal-services/tests/test_build.py
git commit -m "legal-services: build.py — namespaced upstream path resolver"
```

---

## Task 5: Build pipeline — fetch helpers (network)

**Files:**
- Modify: `legal-services/scripts/build.py`

These helpers shell out to `gh api`. They're not unit-tested here — the integration test happens in `make check` once real upstream is involved. The helper signatures mirror `financial-services/scripts/build.py` exactly.

- [ ] **Step 1: Add `fetch_upstream_file` to `build.py`.**

Append to `legal-services/scripts/build.py`:

```python
def fetch_upstream_file(repo: str, commit: str, path: str) -> bytes:
    """Fetch raw bytes of a file from upstream at the pinned commit."""
    out = subprocess.run(
        ["gh", "api", f"repos/{repo}/contents/{path}?ref={commit}", "--jq", ".content"],
        check=True, capture_output=True, text=True,
    )
    return base64.b64decode(out.stdout.strip())
```

- [ ] **Step 2: Commit.**

```bash
git add legal-services/scripts/build.py
git commit -m "legal-services: build.py — fetch_upstream_file helper"
```

---

## Task 6: Build pipeline — emit_company (TDD)

**Files:**
- Modify: `legal-services/scripts/build.py`
- Modify: `legal-services/tests/test_build.py`

The COMPANY.md body needs the legal-specific Boundaries paragraph (not the finance one).

- [ ] **Step 1: Write the failing test.**

Append to `legal-services/tests/test_build.py`:

```python
from scripts.build import emit_company


def test_emit_company_produces_valid_yaml_frontmatter(tmp_path):
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    out_path = tmp_path / "COMPANY.md"
    emit_company(m, out_path)

    text = out_path.read_text()
    assert text.startswith("---\n")
    fm_end = text.find("\n---\n", 4)
    assert fm_end > 0
    fm = yaml.safe_load(text[4:fm_end])
    assert fm["schema"] == "agentcompanies/v1"
    assert fm["slug"] == "test-co"
    assert fm["license"] == "Apache-2.0"
    assert fm["metadata"]["upstream"]["commit"] == "deadbeef"

    body = text[fm_end + len("\n---\n"):]
    assert "Test Co" in body
    # Boundaries paragraph must be legal-flavored (attorney review, not investment advice).
    assert "attorney" in body.lower()
    assert "investment" not in body.lower()
```

- [ ] **Step 2: Run — expect ImportError.**

- [ ] **Step 3: Implement `emit_company`.**

Append to `legal-services/scripts/build.py`:

```python
BOUNDARIES_BODY = (
    "Nothing in this package constitutes legal advice. Every output is a draft\n"
    "for attorney review — not a legal conclusion, not a substitute for a lawyer.\n"
    "These agents draft work product (memos, redlines, claim charts, deposition\n"
    "outlines, review reports, policies, classifications) for review by a\n"
    "qualified attorney. They do not file briefs, send demand letters, issue\n"
    "legal holds, or take positions on behalf of any party; every output is\n"
    "staged for human sign-off. The attorney using the package — not the\n"
    "package, and not Anthropic — is responsible for the legal positions taken\n"
    "in their work product."
)


def emit_company(m: Manifest, out_path: Path) -> None:
    fm = {
        "schema": m.schema,
        "slug": m.slug,
        "name": m.name,
        "description": m.description,
        "version": m.version,
        "license": m.license,
        "authors": [{"name": a.name, "email": a.email} for a in m.authors],
        "goals": m.goals,
        "tags": m.tags,
        "metadata": {
            "upstream": {
                "repo": m.upstream.repo,
                "commit": m.upstream.commit,
                "license": m.upstream.license,
            },
            "affiliation": m.affiliation,
        },
    }
    body_lines = [
        f"# {m.name}",
        "",
        m.description,
        "",
        "## Boundaries",
        "",
        BOUNDARIES_BODY,
        "",
        "## Teams",
        "",
    ]
    for slug, team in m.teams.items():
        body_lines.append(f"- **{team.name}** (`teams/{slug}/TEAM.md`) — {team.description}")
    body_lines.append("")
    out_path.write_text(_frontmatter(fm) + "\n".join(body_lines) + "\n")
```

- [ ] **Step 4: Run — expect PASS.**

```bash
cd legal-services && pytest tests/test_build.py -v
```

- [ ] **Step 5: Commit.**

```bash
git add legal-services/scripts/build.py legal-services/tests/test_build.py
git commit -m "legal-services: build.py — emit_company with legal Boundaries paragraph"
```

---

## Task 7: Build pipeline — team_coordinator + emit_teams (TDD)

**Files:**
- Modify: `legal-services/scripts/build.py`
- Modify: `legal-services/tests/test_build.py`

This logic is identical to financial-services. Port it verbatim with adapted tests.

- [ ] **Step 1: Write the failing tests.**

Append to `legal-services/tests/test_build.py`:

```python
from scripts.build import emit_teams, Agent


def test_emit_teams_creates_one_file_per_team_no_coordinator(tmp_path):
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    emit_teams(m, tmp_path)
    team_path = tmp_path / "team-a" / "TEAM.md"
    assert team_path.exists()
    text = team_path.read_text()
    fm_end = text.find("\n---\n", 4)
    fm = yaml.safe_load(text[4:fm_end])
    assert fm["slug"] == "team-a"
    assert fm["includes"] == ["../../agents/alpha/AGENTS.md"]
    assert fm["reportsTo"] == "../../COMPANY.md"


def test_emit_teams_reports_to_coordinator_when_single_top_level_agent(tmp_path):
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    m.agents["ceo"] = Agent(
        name="CEO",
        title="Chief Executive Officer",
        description="Top-level coordinator.",
        skills=["intake-triage"],
        team=None,
    )
    emit_teams(m, tmp_path)
    fm_text = (tmp_path / "team-a" / "TEAM.md").read_text()
    fm_end = fm_text.find("\n---\n", 4)
    fm = yaml.safe_load(fm_text[4:fm_end])
    assert fm["reportsTo"] == "../../agents/ceo/AGENTS.md"
```

- [ ] **Step 2: Run — expect ImportError.**

- [ ] **Step 3: Implement `team_coordinator` + `emit_teams`.**

Append to `legal-services/scripts/build.py`:

```python
def team_coordinator(m: Manifest) -> str | None:
    """Return the single top-level agent (team=None) that coordinates the teams, if any.

    Convention: if exactly one top-level agent exists, teams report to it.
    With zero or multiple top-level agents, teams report directly to the company.
    """
    top_level = [s for s, a in m.agents.items() if a.team is None]
    return top_level[0] if len(top_level) == 1 else None


def emit_teams(m: Manifest, teams_root: Path) -> None:
    team_agents: dict[str, list[str]] = {t: [] for t in m.teams}
    for agent_slug, agent in m.agents.items():
        if agent.team is None:
            continue
        team_agents[agent.team].append(agent_slug)

    coordinator = team_coordinator(m)
    reports_to = (
        f"../../agents/{coordinator}/AGENTS.md" if coordinator else "../../COMPANY.md"
    )

    for slug, team in m.teams.items():
        out_dir = teams_root / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        fm = {
            "slug": slug,
            "name": team.name,
            "description": team.description,
            "reportsTo": reports_to,
            "includes": [
                f"../../agents/{a}/AGENTS.md" for a in sorted(team_agents[slug])
            ],
        }
        body = f"\n# {team.name}\n\n{team.description}\n"
        (out_dir / "TEAM.md").write_text(_frontmatter(fm) + body)
```

- [ ] **Step 4: Run — expect PASS.**

- [ ] **Step 5: Commit.**

```bash
git add legal-services/scripts/build.py legal-services/tests/test_build.py
git commit -m "legal-services: build.py — team_coordinator + emit_teams"
```

---

## Task 8: Build pipeline — emit_agents (TDD)

**Files:**
- Modify: `legal-services/scripts/build.py`
- Modify: `legal-services/tests/test_build.py`

The differences from financial-services:
- Specialist agent URL: `https://github.com/<repo>/tree/<sha>/<agent-slug>` (not `plugins/agent-plugins/<agent-slug>`).
- Tags: `["legal", "<team-slug>"]` for specialists; `["legal", "executive"]` for top-level CEO.

- [ ] **Step 1: Write the failing tests.**

Append to `legal-services/tests/test_build.py`:

```python
from scripts.build import emit_agents


def test_emit_agents_specialist_url_uses_agent_slug_as_plugin_dir(tmp_path):
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    emit_agents(m, tmp_path)
    agent_md = (tmp_path / "alpha" / "AGENTS.md").read_text()
    fm_end = agent_md.find("\n---\n", 4)
    fm = yaml.safe_load(agent_md[4:fm_end])
    assert fm["slug"] == "alpha"
    assert fm["reportsTo"] == "../../teams/team-a/TEAM.md"
    assert fm["skills"] == ["alpha-legal--review"]
    # URL points at the upstream plugin directory by agent slug.
    assert fm["metadata"]["sources"][0]["url"] == (
        "https://github.com/example/upstream/tree/deadbeef/alpha"
    )
    assert "legal" in fm["tags"]
    assert "team-a" in fm["tags"]


def test_emit_agents_top_level_agent_is_port_original(tmp_path):
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    m.agents["ceo"] = Agent(
        name="CEO",
        title="Chief Executive Officer",
        description="Top-level coordinator.",
        skills=["intake-triage"],
        team=None,
    )
    emit_agents(m, tmp_path)
    fm_text = (tmp_path / "ceo" / "AGENTS.md").read_text()
    fm_end = fm_text.find("\n---\n", 4)
    fm = yaml.safe_load(fm_text[4:fm_end])
    assert fm["reportsTo"] == "../../COMPANY.md"
    assert fm["metadata"]["sources"] == [{"mode": "port-original"}]
    assert fm["tags"] == ["legal", "executive"]
```

- [ ] **Step 2: Run — expect ImportError.**

- [ ] **Step 3: Implement `emit_agents`.**

Append to `legal-services/scripts/build.py`:

```python
def emit_agents(m: Manifest, agents_root: Path) -> None:
    for slug, agent in m.agents.items():
        out_dir = agents_root / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        if agent.team is None:
            reports_to = "../../COMPANY.md"
            tags = ["legal", "executive"]
            sources = [{"mode": "port-original"}]
        else:
            reports_to = f"../../teams/{agent.team}/TEAM.md"
            tags = ["legal", agent.team]
            sources = [
                {
                    "url": f"https://github.com/{m.upstream.repo}/tree/{m.upstream.commit}/{slug}",
                    "mode": "referenced",
                }
            ]
        fm = {
            "slug": slug,
            "name": agent.name,
            "title": agent.title,
            "reportsTo": reports_to,
            "skills": list(agent.skills),
            "tags": tags,
            "metadata": {"sources": sources},
        }
        body = f"\n# {agent.name}\n\n{agent.description.strip()}\n"
        (out_dir / "AGENTS.md").write_text(_frontmatter(fm) + body)
```

- [ ] **Step 4: Run — expect PASS.**

- [ ] **Step 5: Commit.**

```bash
git add legal-services/scripts/build.py legal-services/tests/test_build.py
git commit -m "legal-services: build.py — emit_agents (specialist URL uses agent slug)"
```

---

## Task 9: Build pipeline — emit_skills (TDD)

**Files:**
- Modify: `legal-services/scripts/build.py`
- Modify: `legal-services/tests/test_build.py`

`emit_skills` differs from financial-services by:
- No `canonical_owner` parameter (single owner per skill, derived from namespaced slug).
- Upstream path is `upstream_path_for_skill(slug)`.

- [ ] **Step 1: Write the failing tests.**

Append to `legal-services/tests/test_build.py`:

```python
from scripts.build import emit_skills, Skill


def test_emit_skills_upstream_referenced_writes_thin_pointer(tmp_path):
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    hashes = {"alpha-legal--review": "abc123"}
    emit_skills(m, content_hashes=hashes, skills_root=tmp_path)
    skill_path = tmp_path / "alpha-legal--review" / "SKILL.md"
    assert skill_path.exists()
    text = skill_path.read_text()
    fm_end = text.find("\n---\n", 4)
    fm = yaml.safe_load(text[4:fm_end])
    assert fm["slug"] == "alpha-legal--review"
    src = fm["metadata"]["sources"][0]
    assert src["repo"] == "example/upstream"
    assert src["commit"] == "deadbeef"
    assert src["path"] == "alpha-legal/skills/review/SKILL.md"
    assert src["mode"] == "referenced"
    assert src["contentHash"] == "abc123"


def test_emit_skills_port_original_preserved(tmp_path):
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    m.skills["intake-triage"] = Skill(
        name="Intake Triage",
        description="Hand-authored.",
        port_original=True,
    )
    out_dir = tmp_path / "intake-triage"
    out_dir.mkdir(parents=True)
    original = "---\nslug: intake-triage\nname: Intake Triage\ndescription: Hand-authored.\n---\nbody\n"
    (out_dir / "SKILL.md").write_text(original)

    emit_skills(m, content_hashes={}, skills_root=tmp_path)
    assert (out_dir / "SKILL.md").read_text() == original


def test_emit_skills_port_original_missing_file_raises(tmp_path):
    import pytest

    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    m.skills["intake-triage"] = Skill(
        name="Intake Triage",
        description="Hand-authored.",
        port_original=True,
    )
    with pytest.raises(SystemExit, match="(?i)port-original"):
        emit_skills(m, content_hashes={}, skills_root=tmp_path)
```

- [ ] **Step 2: Run — expect TypeError (signature mismatch) or ImportError.**

- [ ] **Step 3: Implement `emit_skills`.**

Append to `legal-services/scripts/build.py`:

```python
def emit_skills(
    m: Manifest,
    content_hashes: dict[str, str],
    skills_root: Path,
) -> None:
    for slug, skill in m.skills.items():
        out_dir = skills_root / slug
        if skill.port_original:
            # Hand-authored skill — must exist; build never regenerates it.
            if not (out_dir / "SKILL.md").exists():
                raise SystemExit(
                    f"Port-original skill {slug!r} declared in manifest but "
                    f"{out_dir / 'SKILL.md'} is missing. Author the file before running build."
                )
            continue
        upstream_path = upstream_path_for_skill(slug)
        out_dir.mkdir(parents=True, exist_ok=True)
        fm = {
            "slug": slug,
            "name": skill.name,
            "description": skill.description,
            "version": "0.1.0",
            "metadata": {
                "sources": [
                    {
                        "repo": m.upstream.repo,
                        "commit": m.upstream.commit,
                        "path": upstream_path,
                        "mode": "referenced",
                        "contentHash": content_hashes[slug],
                    }
                ]
            },
        }
        body = (
            f"\n# {skill.name}\n\n"
            f"> Skill content lives upstream at the path above (commit `{m.upstream.commit}`).\n"
            f"> Pull the upstream file before invocation; do not edit this manifest in place.\n"
        )
        (out_dir / "SKILL.md").write_text(_frontmatter(fm) + body)
```

- [ ] **Step 4: Run — expect PASS.**

- [ ] **Step 5: Commit.**

```bash
git add legal-services/scripts/build.py legal-services/tests/test_build.py
git commit -m "legal-services: build.py — emit_skills (no canonical_owner)"
```

---

## Task 10: Build pipeline — org chart + main (TDD)

**Files:**
- Modify: `legal-services/scripts/build.py`
- Modify: `legal-services/tests/test_build.py`

Org-chart logic is identical to financial-services (port verbatim). The `main` function orchestrates the full build.

- [ ] **Step 1: Write the failing tests.**

Append to `legal-services/tests/test_build.py`:

```python
from scripts.build import emit_org_chart_dot


def test_org_chart_dot_contains_company_team_agent_edges():
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    dot = emit_org_chart_dot(m)
    assert "digraph" in dot
    assert '"team-a"' in dot
    assert '"alpha"' in dot
    assert '"team-a" -> "alpha"' in dot
    assert f'"{m.slug}" -> "team-a"' in dot


def test_org_chart_with_single_top_level_agent_routes_teams_through_coordinator():
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    m.agents["ceo"] = Agent(
        name="CEO",
        title="CEO",
        description="d",
        skills=["intake-triage"],
        team=None,
    )
    dot = emit_org_chart_dot(m)
    assert f'"{m.slug}" -> "ceo"' in dot
    assert '"ceo" -> "team-a"' in dot
    assert f'"{m.slug}" -> "team-a"' not in dot
    assert '"None"' not in dot
```

- [ ] **Step 2: Run — expect ImportError.**

- [ ] **Step 3: Implement `emit_org_chart_dot`, `render_org_chart`, and `main`.**

Append to `legal-services/scripts/build.py`:

```python
def emit_org_chart_dot(m: Manifest) -> str:
    lines = [
        "digraph org {",
        "  rankdir=TB;",
        '  node [shape=box, style=rounded, fontname="Helvetica"];',
        f'  "{m.slug}" [label="{m.name}", style="rounded,filled", fillcolor="#e8f0fe"];',
    ]
    coordinator = team_coordinator(m)

    top_level = [(s, a) for s, a in m.agents.items() if a.team is None]
    for agent_slug, agent in top_level:
        lines.append(
            f'  "{agent_slug}" [label="{agent.name}", style="rounded,filled", fillcolor="#dcfce7"];'
        )
        lines.append(f'  "{m.slug}" -> "{agent_slug}";')

    team_parent = coordinator if coordinator else m.slug
    for team_slug, team in m.teams.items():
        lines.append(
            f'  "{team_slug}" [label="{team.name}", fillcolor="#fef3c7", style="rounded,filled"];'
        )
        lines.append(f'  "{team_parent}" -> "{team_slug}";')

    for agent_slug, agent in m.agents.items():
        if agent.team is None:
            continue
        lines.append(f'  "{agent_slug}" [label="{agent.name}"];')
        lines.append(f'  "{agent.team}" -> "{agent_slug}";')
    lines.append("}")
    return "\n".join(lines) + "\n"


def render_org_chart(dot_text: str, out_png: Path) -> None:
    out_png.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["dot", "-Tpng", "-o", str(out_png)],
        input=dot_text, text=True, check=True,
    )


def main() -> None:
    m = load_manifest(ROOT / "manifest.yaml")
    print(f"Building {m.slug} v{m.version} from manifest…")

    upstream_skills = {k: v for k, v in m.skills.items() if not v.port_original}
    port_original_skills = {k: v for k, v in m.skills.items() if v.port_original}

    hashes: dict[str, str] = {}
    for slug in upstream_skills:
        path = upstream_path_for_skill(slug)
        content = fetch_upstream_file(m.upstream.repo, m.upstream.commit, path)
        hashes[slug] = compute_content_hash(content)
        print(f"  hashed {slug} ← {path}")

    if port_original_skills:
        print(f"  port-original skills (hand-authored): {sorted(port_original_skills)}")

    emit_company(m, ROOT / "COMPANY.md")
    emit_teams(m, ROOT / "teams")
    emit_agents(m, ROOT / "agents")
    emit_skills(m, hashes, ROOT / "skills")

    dot = emit_org_chart_dot(m)
    (ROOT / "images").mkdir(exist_ok=True)
    (ROOT / "images" / "org-chart.dot").write_text(dot)
    render_org_chart(dot, ROOT / "images" / "org-chart.png")

    print("Build complete.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run — expect PASS.**

```bash
cd legal-services && pytest tests/test_build.py -v
```

- [ ] **Step 5: Commit.**

```bash
git add legal-services/scripts/build.py legal-services/tests/test_build.py
git commit -m "legal-services: build.py — org-chart + main orchestrator"
```

---

## Task 11: Validator — check.py (TDD)

**Files:**
- Create: `legal-services/scripts/check.py`
- Create: `legal-services/tests/test_check.py`

Identical to `financial-services/scripts/check.py` (same schema, same checks). Port verbatim.

- [ ] **Step 1: Write failing tests.**

Write `legal-services/tests/test_check.py`:

```python
import yaml
from pathlib import Path
import pytest

from scripts.check import (
    parse_frontmatter,
    validate_frontmatter,
    check_cross_references,
    ValidationError,
)


def test_parse_frontmatter_extracts_yaml_block():
    text = "---\nslug: foo\nname: Foo\n---\nbody\n"
    fm = parse_frontmatter(text)
    assert fm["slug"] == "foo"
    assert fm["name"] == "Foo"


def test_parse_frontmatter_no_frontmatter_raises():
    with pytest.raises(ValidationError, match="frontmatter"):
        parse_frontmatter("no frontmatter\n")


def test_parse_frontmatter_unterminated_raises():
    with pytest.raises(ValidationError, match="unterminated"):
        parse_frontmatter("---\nslug: foo\n")


def test_validate_frontmatter_company_requires_fields():
    fm = {"schema": "agentcompanies/v1", "slug": "x"}
    with pytest.raises(ValidationError, match="missing required fields"):
        validate_frontmatter("company", fm)


def test_validate_frontmatter_unknown_kind_raises():
    with pytest.raises(ValidationError, match="unknown kind"):
        validate_frontmatter("bogus", {})


def test_check_cross_references_detects_dangling_skill(tmp_path):
    # Layout: one agent references skill "ghost" but the skills/ dir has nothing.
    agents_dir = tmp_path / "agents" / "alpha"
    agents_dir.mkdir(parents=True)
    (agents_dir / "AGENTS.md").write_text(
        "---\nslug: alpha\nname: Alpha\ntitle: A\nreportsTo: x\nskills: [ghost]\n---\n"
    )
    (tmp_path / "skills").mkdir()
    with pytest.raises(ValidationError, match="missing skill"):
        check_cross_references(tmp_path)


def test_check_cross_references_passes_when_skill_present(tmp_path):
    agents_dir = tmp_path / "agents" / "alpha"
    agents_dir.mkdir(parents=True)
    (agents_dir / "AGENTS.md").write_text(
        "---\nslug: alpha\nname: Alpha\ntitle: A\nreportsTo: x\nskills: [present]\n---\n"
    )
    (tmp_path / "skills" / "present").mkdir(parents=True)
    check_cross_references(tmp_path)  # no raise
```

- [ ] **Step 2: Run — expect ImportError.**

- [ ] **Step 3: Implement `check.py`.**

Write `legal-services/scripts/check.py`:

```python
"""Validation script for the legal-services Agent Company package."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

import yaml

from scripts.build import fetch_upstream_file

ROOT = Path(__file__).resolve().parent.parent


class ValidationError(Exception):
    pass


REQUIRED_FIELDS: dict[str, set[str]] = {
    "company": {"schema", "slug", "name", "description", "version", "license", "authors"},
    "team": {"slug", "name", "description", "includes"},
    "agent": {"slug", "name", "title", "reportsTo", "skills"},
    "skill": {"slug", "name", "description"},
}


def validate_frontmatter(kind: str, fm: dict[str, Any]) -> None:
    required = REQUIRED_FIELDS.get(kind)
    if required is None:
        raise ValidationError(f"unknown kind: {kind}")
    missing = required - set(fm)
    if missing:
        raise ValidationError(f"{kind} missing required fields: {sorted(missing)}")


def parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        raise ValidationError("file does not start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValidationError("frontmatter is unterminated")
    return yaml.safe_load(text[4:end])


def check_cross_references(package_root: Path) -> None:
    skills_dir = package_root / "skills"
    available = {p.name for p in skills_dir.iterdir() if p.is_dir()} if skills_dir.exists() else set()

    agents_dir = package_root / "agents"
    if not agents_dir.exists():
        return
    for agent_md in agents_dir.glob("*/AGENTS.md"):
        fm = parse_frontmatter(agent_md.read_text())
        for skill in fm.get("skills", []):
            if skill not in available:
                raise ValidationError(
                    f"{agent_md.relative_to(package_root)}: references missing skill {skill!r}"
                )


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check_content_hashes(package_root: Path) -> None:
    skills_dir = package_root / "skills"
    if not skills_dir.exists():
        return
    for skill_md in skills_dir.glob("*/SKILL.md"):
        fm = parse_frontmatter(skill_md.read_text())
        sources = fm.get("metadata", {}).get("sources", [])
        for src in sources:
            if src.get("mode") != "referenced":
                continue
            actual = _sha256(fetch_upstream_file(src["repo"], src["commit"], src["path"]))
            expected = src.get("contentHash")
            if actual != expected:
                raise ValidationError(
                    f"{skill_md.relative_to(package_root)}: contentHash {expected!r} "
                    f"does not match upstream sha256 {actual!r} at {src['path']}"
                )


def main() -> int:
    try:
        for kind, glob in [
            ("company", "COMPANY.md"),
            ("team", "teams/*/TEAM.md"),
            ("agent", "agents/*/AGENTS.md"),
            ("skill", "skills/*/SKILL.md"),
        ]:
            for path in ROOT.glob(glob):
                fm = parse_frontmatter(path.read_text())
                validate_frontmatter(kind, fm)

        check_cross_references(ROOT)
        check_content_hashes(ROOT)

    except ValidationError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        return 1
    print("OK: schema, cross-references, content hashes all valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run — expect PASS.**

```bash
cd legal-services && pytest -v
```

- [ ] **Step 5: Commit.**

```bash
git add legal-services/scripts/check.py legal-services/tests/test_check.py
git commit -m "legal-services: check.py — schema + cross-ref + content-hash validators"
```

---

## Task 12: Extract upstream skill metadata (one-shot helper)

**Files:**
- Create: `legal-services/scripts/extract_upstream_metadata.py`

This helper is **not** part of `make build` or `make check`. It's a one-shot tool that fetches upstream SKILL.md frontmatter and emits starter YAML for the `skills:` block in `manifest.yaml`. The maintainer reviews and edits before committing the manifest.

- [ ] **Step 1: Write the script.**

Write `legal-services/scripts/extract_upstream_metadata.py`:

```python
"""One-shot helper: fetch upstream SKILL.md frontmatter and emit starter YAML
for the legal-services manifest skills block.

Usage:
    python -m scripts.extract_upstream_metadata > /tmp/skills-block.yaml

Then review and paste into manifest.yaml. NOT run by `make build`.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

from scripts.build import fetch_upstream_file


UPSTREAM_REPO = "anthropics/claude-for-legal"
UPSTREAM_COMMIT = "9cecd91b0f26f732d18315afc3c9bb5ff99e0fbb"

PLUGINS = [
    "commercial-legal",
    "corporate-legal",
    "employment-legal",
    "privacy-legal",
    "product-legal",
    "regulatory-legal",
    "ai-governance-legal",
    "ip-legal",
    "litigation-legal",
    "law-student",
    "legal-clinic",
    "legal-builder-hub",
]


def list_plugin_skills(plugin: str) -> list[str]:
    """Return the bare skill slugs (subdirs of <plugin>/skills/) for one plugin.

    Uses the git tree API instead of the contents API for batched discovery.
    """
    import subprocess

    out = subprocess.run(
        [
            "gh", "api",
            f"repos/{UPSTREAM_REPO}/git/trees/{UPSTREAM_COMMIT}?recursive=1",
            "--jq",
            f'.tree[] | select(.path | test("^{re.escape(plugin)}/skills/[^/]+/SKILL\\\\.md$")) | .path',
        ],
        check=True, capture_output=True, text=True,
    )
    skills = []
    for line in out.stdout.splitlines():
        # plugin/skills/<bare>/SKILL.md
        parts = line.split("/")
        skills.append(parts[2])
    return sorted(skills)


def title_from_slug(slug: str) -> str:
    """Convert kebab-case to Title Case."""
    return " ".join(w.capitalize() for w in slug.split("-"))


def first_sentence(description: str) -> str:
    """Return the first sentence of a multi-line description string, trimmed."""
    flat = " ".join(description.split())
    m = re.match(r"^(.+?[.!?])(?:\s|$)", flat)
    return (m.group(1) if m else flat).strip()


def extract_skill_metadata(plugin: str, bare: str) -> tuple[str, str]:
    """Fetch <plugin>/skills/<bare>/SKILL.md and return (display_name, description)."""
    path = f"{plugin}/skills/{bare}/SKILL.md"
    content = fetch_upstream_file(UPSTREAM_REPO, UPSTREAM_COMMIT, path).decode("utf-8")
    if not content.startswith("---\n"):
        return title_from_slug(bare), f"Upstream skill at {path}."
    end = content.find("\n---\n", 4)
    fm = yaml.safe_load(content[4:end]) or {}
    raw_desc = fm.get("description", "") or ""
    return title_from_slug(bare), first_sentence(raw_desc)


def main() -> int:
    lines: list[str] = ["# Generated by scripts/extract_upstream_metadata.py — review before committing."]
    for plugin in PLUGINS:
        bare_slugs = list_plugin_skills(plugin)
        print(f"# {plugin}: {len(bare_slugs)} skills", file=sys.stderr)
        for bare in bare_slugs:
            slug = f"{plugin}--{bare}"
            name, desc = extract_skill_metadata(plugin, bare)
            lines.append(f"  {slug}:")
            lines.append(f"    name: {yaml.safe_dump(name).strip()}")
            lines.append(f"    description: {yaml.safe_dump(desc).strip()}")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Commit.**

```bash
git add legal-services/scripts/extract_upstream_metadata.py
git commit -m "legal-services: extract_upstream_metadata.py — one-shot manifest helper"
```

---

## Task 13: Run the metadata extractor + author the manifest

**Files:**
- Create: `legal-services/manifest.yaml`

- [ ] **Step 1: Run the extractor and save its output.**

```bash
cd legal-services && python -m scripts.extract_upstream_metadata > /tmp/legal-skills-block.yaml 2>/tmp/legal-skills-progress.txt
head /tmp/legal-skills-block.yaml
tail /tmp/legal-skills-progress.txt
```

Expected: stderr shows `# commercial-legal: 12 skills`, etc., totaling 150. stdout contains 150 `<plugin>--<bare>:` blocks.

- [ ] **Step 2: Verify the count.**

```bash
grep -cE '^  [a-z][a-z0-9-]+--[a-z][a-z0-9-]+:$' /tmp/legal-skills-block.yaml
```

Expected: `150`.

- [ ] **Step 3: Hand-author the manifest header and CEO/specialist blocks.**

Write `legal-services/manifest.yaml`:

```yaml
schema: agentcompanies/v1
slug: legal-services
name: Legal Services
description: 13-agent legal company — commercial, regulatory, IP, disputes, and legal-education plugins from anthropics/claude-for-legal, plus a CEO that handles intake, cross-practice coordination, escalation, and weekly summaries. Every output is staged for attorney review.
version: 0.1.0
license: Apache-2.0
authors:
  - name: Jannes Stubbemann
    email: jannes@paperclip.inc
goals:
  - Draft legal work product (memos, redlines, claim charts, deposition outlines, review reports, policies, classifications) for attorney review.
  - Cover the 12 practice-area plugins Anthropic shipped — commercial, corporate, employment, privacy, product, regulatory, AI governance, IP, litigation, plus law-student / legal-clinic / legal-builder-hub on the education side.
  - Stage every output for attorney sign-off — no agent here files briefs, sends demand letters, issues legal holds, or takes legal positions on behalf of any party.
tags: [legal, in-house-counsel, commercial, privacy, regulatory, litigation, ip, employment, ai-governance]

upstream:
  repo: anthropics/claude-for-legal
  commit: 9cecd91b0f26f732d18315afc3c9bb5ff99e0fbb
  license: Apache-2.0

affiliation: "Community port. Not affiliated with or endorsed by Anthropic."

teams:
  commercial-transactions:
    name: Commercial & Transactions
    description: Day-to-day deal docs and workforce contracts — commercial agreements, M&A diligence, employment.
  regulatory-compliance:
    name: Regulatory & Compliance
    description: Rule-tracking and compliance posture — privacy, AI governance, regulatory feeds, product launches.
  ip-disputes:
    name: IP & Disputes
    description: Offensive and defensive workstreams — IP clearance / portfolio / enforcement and full litigation lifecycle.
  academy-tooling:
    name: Legal Academy & Tooling
    description: Education and meta-tooling — law-school work, clinic operations, and discovery / evaluation of community legal skills.

agents:
  ceo:
    name: CEO
    title: Chief Executive Officer
    description: |
      Front-of-house coordinator for the legal-services team. Receives incoming
      matters, classifies them, routes to the right practice area, and orchestrates
      handoffs when work spans practice areas (e.g., an M&A diligence run touching
      IP, employment, and privacy). Handles escalation routing when a specialist
      hits a blocker, and produces the company-level weekly summary. Does not run
      skills the specialists own — no contract redlines, claim charts, DSARs, or
      policy drafts; the CEO coordinates, the practices execute. This role is a
      port-time addition; upstream `anthropics/claude-for-legal` does not model
      an org head.
    skills:
      - intake-triage
      - cross-practice-coordination
      - escalation-routing
      - weekly-summary

  commercial-legal:
    name: Commercial Counsel
    title: Commercial Contracts Specialist
    team: commercial-transactions
    description: |
      Wraps the `commercial-legal` plugin. Reviews vendor agreements, NDAs, and
      SaaS subscriptions against the team's playbook; tracks renewals and cancel-by
      deadlines; routes escalations to the right approver; translates reviews into
      summaries business stakeholders will actually read. Output is staged for
      attorney sign-off before anything goes back to a counterparty.
    skills: [commercial-legal--amendment-history, commercial-legal--cold-start-interview, commercial-legal--customize, commercial-legal--escalation-flagger, commercial-legal--matter-workspace, commercial-legal--nda-review, commercial-legal--renewal-tracker, commercial-legal--review, commercial-legal--review-proposals, commercial-legal--saas-msa-review, commercial-legal--stakeholder-summary, commercial-legal--vendor-agreement-review]

  corporate-legal:
    name: Corporate Counsel
    title: M&A and Corporate Specialist
    team: commercial-transactions
    description: |
      Wraps the `corporate-legal` plugin. Runs M&A diligence at scale with cited
      tabular review; builds disclosure schedules and closing checklists; drafts
      board consents and minutes in house format; tracks entity compliance
      deadlines across jurisdictions; manages phased post-closing integration.
      Output is staged for attorney review.
    # FILL IN from extract output

  employment-legal:
    name: Employment Counsel
    title: Employment Law Specialist
    team: commercial-transactions
    description: |
      Wraps the `employment-legal` plugin. Reviews hires and terminations for
      jurisdiction-specific risk; classifies workers against the controlling
      state test; tracks open leaves and FMLA / CFRA / PFL / ADA deadlines;
      opens and summarizes internal investigations; drafts policies with state
      supplements; plans international expansion (EOR vs. entity). Output is
      staged for attorney sign-off.
    # FILL IN

  privacy-legal:
    name: Privacy Counsel
    title: Privacy & Data Protection Specialist
    team: regulatory-compliance
    description: |
      Wraps the `privacy-legal` plugin. Triages processing activities, generates
      PIAs, reviews DPAs as controller or processor, drafts DSAR responses within
      statutory timelines, and monitors policy drift against practice. Output is
      staged for attorney review.
    # FILL IN

  ai-governance-legal:
    name: AI Governance Counsel
    title: AI Governance Specialist
    team: regulatory-compliance
    description: |
      Wraps the `ai-governance-legal` plugin. Classifies proposed AI use cases
      against the registry, runs Algorithmic Impact Assessments across the
      regimes in scope, reviews vendor AI terms (training-on-data, liability,
      model-change, policy gaps), diffs new AI regulations against current
      governance posture, and sweeps saved AIAs / triage results / vendor reviews
      for AI-policy drift. Output is staged for attorney review.
    # FILL IN

  regulatory-legal:
    name: Regulatory Counsel
    title: Regulatory Affairs Specialist
    team: regulatory-compliance
    description: |
      Wraps the `regulatory-legal` plugin. Watches regulatory feeds and writes
      the Monday-morning digest; diffs specific regulatory changes against the
      indexed policy library; tracks open gaps; drafts marked-up policy
      redrafts that close those gaps (proposals for the policy owner, not
      direct edits to source documents); manages open NPRM comment periods.
      Output is staged for attorney review.
    # FILL IN

  product-legal:
    name: Product Counsel
    title: Product Launch Specialist
    team: regulatory-compliance
    description: |
      Wraps the `product-legal` plugin. Reviews product launches against the
      team's risk calibration, answers "is this a problem?" Slack questions in
      minutes, checks marketing copy for claims that need substantiation, and
      flags upcoming launches that need legal eyes before anyone asks. Output
      is staged for attorney review.
    # FILL IN

  ip-legal:
    name: IP Counsel
    title: Intellectual Property Specialist
    team: ip-disputes
    description: |
      Wraps the `ip-legal` plugin. Runs first-pass trademark clearance and
      freedom-to-operate triage; drafts and triages cease-and-desist letters;
      drafts DMCA takedowns, triages received ones, and drafts §512(g) counter-
      notices; reviews open-source license compliance; reviews IP clauses
      (assignment, ownership, license grants, warranties, indemnities);
      tracks the IP portfolio (registrations, renewals, maintenance fees).
      Output is a triage / draft — not an opinion — staged for attorney review.
    # FILL IN

  litigation-legal:
    name: Litigation Counsel
    title: Litigation Portfolio Manager
    team: ip-disputes
    description: |
      Wraps the `litigation-legal` plugin. Manages the litigation portfolio —
      matter intake, briefings, deadlines, legal holds, demand letters
      (with FRE 408 awareness and an explicit send gate), inbound subpoenas,
      chronologies, deposition prep, brief sections in house style, privilege-log
      first pass. Output is staged for attorney review; nothing is filed, sent,
      or signed without an attorney's sign-off.
    # FILL IN

  law-student:
    name: Law Student
    title: Law-school Study Companion
    team: academy-tooling
    description: |
      Wraps the `law-student` plugin. Drills Socratically; briefs cases; builds
      outlines; runs bar-prep sessions tuned to the student's gaps. Output is a
      study aid — explicitly not legal advice and not a substitute for casebook
      reading or instructor feedback.
    # FILL IN

  legal-clinic:
    name: Legal Clinic Operator
    title: Law-school Clinic Operations Specialist
    team: academy-tooling
    description: |
      Wraps the `legal-clinic` plugin. Sets up the clinic, onboards students,
      runs structured intake, tracks deadlines and handoffs, manages client
      communications, supports supervising attorneys' oversight. Output is
      staged for supervising-attorney review; the supervising attorney remains
      responsible for legal advice given to clinic clients.
    # FILL IN

  legal-builder-hub:
    name: Legal Skill Curator
    title: Legal Skill Discovery & Evaluation Specialist
    team: academy-tooling
    description: |
      Wraps the `legal-builder-hub` plugin. Finds, evaluates, and installs
      community legal skills — with a security review gate before anything is
      installed. Output is an evaluation memo and installation plan, not an
      automated install.
    # FILL IN

skills:
  # CEO port-original skills (hand-authored in this repo, no upstream counterpart):
  intake-triage:
    name: Intake Triage
    description: Receive an incoming matter, classify it (practice area, urgency, scope), and route to the right specialist.
    port_original: true
  cross-practice-coordination:
    name: Cross-practice Coordination
    description: Coordinate handoffs when work spans multiple practice areas (e.g., M&A diligence touching IP + employment + privacy).
    port_original: true
  escalation-routing:
    name: Escalation Routing
    description: When a specialist reports a blocker, decide between retry, reassign, or escalate-to-human.
    port_original: true
  weekly-summary:
    name: Weekly Summary
    description: Compose the company-level weekly digest — what shipped, what's blocked, what needs attorney review.
    port_original: true

  # 150 upstream-referenced skills follow:
  # PASTE the contents of /tmp/legal-skills-block.yaml here (after the comment marker
  # the helper emits at the top). Each block:
  #   <plugin>--<bare>:
  #     name: <Title Case>
  #     description: <first sentence of upstream description>
```

- [ ] **Step 4: Paste in the 150 generated skill blocks from `/tmp/legal-skills-block.yaml`.**

Splice the helper's output (after stripping its leading comment line) into the manifest beneath the `# 150 upstream-referenced skills follow:` comment. Sort by skill slug for stable diffs.

- [ ] **Step 5: Fill in each specialist agent's `skills:` list.**

For each specialist agent block marked `# FILL IN`, list the agent's namespaced skill slugs as a YAML inline array, sorted alphabetically. Derive from the per-plugin skill subdirs you discovered in Step 1.

Example for `corporate-legal`:

```bash
ls /tmp/claude-for-legal/corporate-legal/skills/ | sort | awk '{printf "corporate-legal--%s, ", $0}'
```

Wrap the resulting comma-list in `[ ... ]` and paste into the `skills:` field.

- [ ] **Step 6: Lint the manifest.**

```bash
python -c "import yaml; yaml.safe_load(open('legal-services/manifest.yaml'))"
```

Expected: no output (silent success).

- [ ] **Step 7: Sanity-check the manifest count.**

```bash
cd legal-services && python3 -c "
import yaml
m = yaml.safe_load(open('manifest.yaml'))
assert len(m['agents']) == 13, len(m['agents'])
assert len(m['teams']) == 4
assert len(m['skills']) == 154, len(m['skills'])
upstream = [s for s,v in m['skills'].items() if not v.get('port_original')]
port_orig = [s for s,v in m['skills'].items() if v.get('port_original')]
assert len(upstream) == 150
assert len(port_orig) == 4
# Every agent's skills must be a subset of declared skills
for slug, agent in m['agents'].items():
    for sk in agent['skills']:
        assert sk in m['skills'], f'{slug} references missing {sk}'
print('OK: 13 agents, 4 teams, 154 skills (150 upstream + 4 port-original); all cross-refs resolve.')
"
```

- [ ] **Step 8: Commit.**

```bash
git add legal-services/manifest.yaml
git commit -m "legal-services: canonical manifest (13 agents, 4 teams, 154 skills)"
```

---

## Task 14: CEO port-original skills

**Files:**
- Create: `legal-services/skills/intake-triage/SKILL.md`
- Create: `legal-services/skills/cross-practice-coordination/SKILL.md`
- Create: `legal-services/skills/escalation-routing/SKILL.md`
- Create: `legal-services/skills/weekly-summary/SKILL.md`

Each port-original SKILL.md has full YAML frontmatter (slug, name, description, version, metadata.sources=`[{mode: port-original}]`) plus an inline body. Follow the pattern from `financial-services/skills/intake-triage/SKILL.md` (if it exists) or the bell-labs port-original skills.

- [ ] **Step 1: Read a reference port-original SKILL.md from a prior port.**

```bash
ls financial-services/skills/intake-triage/ 2>/dev/null && cat financial-services/skills/intake-triage/SKILL.md || \
ls bell-labs/skills/intake-triage/ 2>/dev/null && cat bell-labs/skills/intake-triage/SKILL.md
```

- [ ] **Step 2: Author `intake-triage/SKILL.md`.**

Write `legal-services/skills/intake-triage/SKILL.md`. Frontmatter:

```yaml
---
slug: intake-triage
name: Intake Triage
description: Receive an incoming matter, classify it, and route to the right specialist.
version: 0.1.0
metadata:
  sources:
    - mode: port-original
---
```

Body: explain the triage rubric — practice areas (the 12 specialists), the classification questions ("Is this commercial, regulatory, IP/disputes, or education?"), the routing decision tree (single-practice → direct route; multi-practice → CEO retains coordination), the escalation triggers (regulator deadlines, board exposure, criminal exposure → escalate to human counsel immediately). Keep to ~60–100 lines. Lead with a one-paragraph purpose, then the workflow, then refusal patterns (don't render legal opinions yourself; don't pre-decide jurisdictional questions).

- [ ] **Step 3: Author `cross-practice-coordination/SKILL.md`.**

Same shape. Body covers: when to invoke (matter touches 2+ practice areas); the dispatch pattern (parallel specialist runs vs. sequential hand-offs); merge-and-deconflict step (resolve where specialists disagree → flag for human); the multi-practice matter checklist (privilege boundaries, retention conflicts, conflict-of-interest disclosure).

- [ ] **Step 4: Author `escalation-routing/SKILL.md`.**

Body covers: blocker types (data missing / authority missing / matter outside model competence); retry vs. reassign vs. escalate decision matrix; human-only escalation triggers (any agent uncertainty on privilege, on jurisdiction-of-suit, on demand-letter send authority); audit-log requirements.

- [ ] **Step 5: Author `weekly-summary/SKILL.md`.**

Body covers: what to summarize (matters opened, matters closed, deadlines hit, deadlines missed, escalations, drift flags from each practice's monitor); house format (sections per team); explicit exclusion of privileged work product details from any cross-team summary.

- [ ] **Step 6: Verify all four files parse as valid SKILL.md.**

```bash
for f in legal-services/skills/{intake-triage,cross-practice-coordination,escalation-routing,weekly-summary}/SKILL.md; do
  python3 -c "
import yaml, sys
text = open('$f').read()
assert text.startswith('---\n')
end = text.find('\n---\n', 4)
fm = yaml.safe_load(text[4:end])
assert fm['slug']
assert fm['metadata']['sources'][0]['mode'] == 'port-original'
print('OK:', '$f')
"
done
```

- [ ] **Step 7: Commit.**

```bash
git add legal-services/skills/intake-triage legal-services/skills/cross-practice-coordination \
        legal-services/skills/escalation-routing legal-services/skills/weekly-summary
git commit -m "legal-services: CEO port-original skills (4) — intake, coordination, escalation, summary"
```

---

## Task 15: First build — generate all artifacts

**Files:**
- Output: `legal-services/COMPANY.md`, `teams/*/TEAM.md`, `agents/*/AGENTS.md`, `skills/<150>/SKILL.md`, `images/org-chart.{dot,png}`

- [ ] **Step 1: Run the build.**

```bash
cd legal-services && python -m scripts.build 2>&1 | tee /tmp/legal-build.log
```

Expected: 150 lines like `hashed commercial-legal--review ← commercial-legal/skills/review/SKILL.md`, then "Build complete."

- [ ] **Step 2: Verify counts.**

```bash
ls legal-services/agents | wc -l    # expect 13
ls legal-services/teams | wc -l     # expect 4
ls legal-services/skills | wc -l    # expect 154 (4 port-original + 150 upstream-referenced)
test -f legal-services/COMPANY.md && echo OK
test -f legal-services/images/org-chart.png && echo OK
```

- [ ] **Step 3: Sanity-spot-check a generated artifact.**

```bash
cat legal-services/agents/commercial-legal/AGENTS.md | head -30
cat legal-services/skills/commercial-legal--review/SKILL.md
```

The first should show the agent frontmatter with skills list and the source URL; the second should show a thin upstream-pointer with sha256 content hash.

- [ ] **Step 4: Commit the generated artifacts.**

```bash
git add legal-services/COMPANY.md legal-services/teams/ legal-services/agents/ \
        legal-services/skills/ legal-services/images/
git commit -m "legal-services: generate COMPANY.md, teams/, agents/, skills/, images/ from manifest"
```

---

## Task 16: Validate via `make check`

- [ ] **Step 1: Run `make check`.**

```bash
cd legal-services && make check
```

Expected: `OK: schema, cross-references, content hashes all valid.`

- [ ] **Step 2: If anything fails, diagnose and fix:**

- Schema fail → frontmatter missing fields → check `REQUIRED_FIELDS` against generated files.
- Cross-ref fail → an `AGENTS.md` references a skill slug that doesn't have a corresponding `skills/<slug>/`. Re-derive the agent's skill list.
- Content-hash fail → upstream drift since the pin (or hashing logic bug). Re-fetch with the build script.

No commit needed unless artifacts changed.

---

## Task 17: Author the company README.md

**Files:**
- Create: `legal-services/README.md`

- [ ] **Step 1: Read the template.**

```bash
cat financial-services/README.md
```

- [ ] **Step 2: Write `legal-services/README.md`.**

Follow the same six-section structure: header / Getting Started / Org chart / Agents (table) / Skills (paragraph) / Boundaries / Provenance / Maintenance / Layout. Use the **legal-specific** Boundaries paragraph from `scripts/build.py`'s `BOUNDARIES_BODY` constant. The "agents" table lists all 13 agents with one-line role descriptions and skill counts. The "skills" paragraph notes the namespacing scheme and which slugs are port-original.

Surface the `> [!IMPORTANT]` callout at the top of the README mirroring the upstream README's "every output is a draft for attorney review" framing.

- [ ] **Step 3: Verify it renders.**

```bash
head -40 legal-services/README.md
```

- [ ] **Step 4: Commit.**

```bash
git add legal-services/README.md
git commit -m "legal-services: company README with attorney-review banner"
```

---

## Task 18: Bump top-level catalog README

**Files:**
- Modify: `README.md` (repo root)

- [ ] **Step 1: Read the current catalog README.**

```bash
sed -n '1,40p' README.md
sed -n '/Bell Labs/,/Repo conventions/p' README.md | head -40
```

- [ ] **Step 2: Bump the badge.**

Edit `README.md`:

```diff
-[![Companies](https://img.shields.io/badge/companies-3-22c55e)](#companies)
+[![Companies](https://img.shields.io/badge/companies-4-22c55e)](#companies)
```

- [ ] **Step 3: Append the `### [Legal Services]` block.**

Insert immediately after the Bell Labs block (just before `---\n\n## Repo conventions`). Follow the same template:

```markdown
### [Legal Services](./legal-services)

> Community port of [`anthropics/claude-for-legal`](https://github.com/anthropics/claude-for-legal) (Anthropic's "Claude for Legal") into the Agent Companies format. Covers 12 practice-area plugins — commercial, corporate, employment, privacy, product, regulatory, AI governance, IP, litigation, plus law-student / legal-clinic / legal-builder-hub on the education side. Runtime-agnostic via the Paperclip adapter chain; Claude is the reference runtime.

```bash
npx companies.sh add stubbi/companies/legal-services
```

| | |
|---|---|
| **Agents** | 13 (1 CEO + 12 practice-area specialists across 4 teams) |
| **Skills** | 150 referenced upstream + 4 port-original (CEO-owned) |
| **License** | Apache-2.0 |
| **Source** | [`anthropics/claude-for-legal`](https://github.com/anthropics/claude-for-legal) at pinned commit `9cecd91b` |

The CEO handles intake triage, cross-practice coordination, escalation routing, and weekly summaries. Specialists cover commercial & transactions (commercial / corporate / employment), regulatory & compliance (privacy / AI governance / regulatory / product), IP & disputes (ip / litigation), and legal academy & tooling (law-student / legal-clinic / legal-builder-hub). Every output is staged for attorney sign-off — agents do not file briefs, send demand letters, issue legal holds, or take legal positions on behalf of any party.

[Company README →](./legal-services/README.md)

> **Boundaries.** Nothing in `legal-services` constitutes legal advice. These agents draft work product (memos, redlines, claim charts, deposition outlines, review reports, policies, classifications) for review by a qualified attorney. They do not file briefs, send demand letters, issue legal holds, or take positions on behalf of any party; every output is staged for attorney sign-off. See the [company's Boundaries section](./legal-services/README.md#boundaries) for full detail.

> **Community port. Not affiliated with or endorsed by Anthropic.** "Claude" is a trademark of Anthropic, PBC.
```

- [ ] **Step 4: Verify.**

```bash
grep "companies-4-22c55e" README.md
grep "### \[Legal Services\]" README.md
```

- [ ] **Step 5: Commit.**

```bash
git add README.md
git commit -m "Add Legal Services to top-level catalog; bump companies badge to 4"
```

---

## Task 19: Final review + PR

- [ ] **Step 1: Run the full test + check loop one more time.**

```bash
cd legal-services && make test && make check
```

Both must pass.

- [ ] **Step 2: Review the diff.**

```bash
cd /Users/jannesstubbemann/repos/companies && git log --oneline main..legal-services
git diff --stat main..legal-services
```

Expected: 15-19 commits totaling ~200 file additions.

- [ ] **Step 3: Push the branch.**

```bash
git push -u origin legal-services
```

- [ ] **Step 4: Open the PR.**

```bash
gh pr create --title "Add Legal Services company (port of anthropics/claude-for-legal)" --body "$(cat <<'EOF'
## Summary

- Ports `anthropics/claude-for-legal` @ `9cecd91b` (Apache-2.0) into the catalog as `legal-services` — a sibling to `financial-services` and `academic-research`.
- 13 agents (1 CEO + 12 practice-area specialists across 4 teams), 150 upstream-referenced skills + 4 port-original CEO skills.
- Introduces namespaced flat skill slugs (`<plugin>--<bare>`) to disambiguate the 12-way duplicated framework skills (cold-start-interview, customize, matter-workspace) that upstream ships per practice area.

## Boundaries

Every output is a draft for attorney review — not legal advice, not a legal conclusion, not a substitute for a lawyer. Documented in COMPANY.md, README.md, and the top-level catalog entry.

## Test plan

- [x] `cd legal-services && make test` — unit tests for the build/check pipeline pass
- [x] `cd legal-services && make check` — schema, cross-reference, and content-hash validation against pinned upstream pass
- [x] Generated artifact spot-check (one agent + one skill manifest reviewed)
- [x] Top-level README badge bumped from 3 to 4; Legal Services block appended after Bell Labs

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Step 5: Wait for CI green; review your own diff in the PR; then merge.**

```bash
gh pr view --json statusCheckRollup,mergeable
# Once green:
gh pr merge --squash --delete-branch
```

---

## Self-review checklist (done by plan author after writing)

- [x] Each spec section maps to at least one task:
  - Slug `legal-services`, upstream pin, license → Tasks 1, 13
  - 1 CEO + 12 specialists in 4 teams → Tasks 13, 14, 15
  - Namespaced flat skill slugs (`--`) → Tasks 4, 9, 12
  - Adapted `build.py` (no canonical-owner; new path pattern) → Tasks 3–10
  - Adapted `check.py` → Task 11
  - Hand-authored CEO skills → Task 14
  - Generated artifacts → Task 15
  - Boundaries paragraph → Tasks 6, 17, 18
  - Top-level README bump → Task 18
  - Tests → embedded throughout
- [x] No `TBD` / `TODO` / `implement later` placeholders (the `# FILL IN` markers in the manifest template are filled by Task 13 Step 5, with an exact recipe).
- [x] Function signatures consistent: `emit_skills(m, content_hashes, skills_root)` is the same in every reference.
- [x] Slug separator is `--` everywhere.
- [x] All file paths absolute or repo-relative.
