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


def _frontmatter(data: dict[str, Any]) -> str:
    return "---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n"


def fetch_upstream_file(repo: str, commit: str, path: str) -> bytes:
    """Fetch raw bytes of a file from upstream at the pinned commit."""
    out = subprocess.run(
        ["gh", "api", f"repos/{repo}/contents/{path}?ref={commit}", "--jq", ".content"],
        check=True, capture_output=True, text=True,
    )
    return base64.b64decode(out.stdout.strip())


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
