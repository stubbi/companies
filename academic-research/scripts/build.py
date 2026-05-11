"""Build script for the Academic Research Agent Company package.

Generates COMPANY.md, TEAM.md, AGENTS.md, SKILL.md files plus the org-chart
image from the canonical manifest.yaml. Adapted from financial-services for
ARS's flatter upstream layout (one SKILL.md per top-level package, declared
explicitly per skill in the manifest).
"""
from __future__ import annotations

import base64
import hashlib
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent


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
    upstream_path: str | None = None  # path within upstream repo, e.g. "deep-research/SKILL.md"
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
    usage_restriction: str
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
        usage_restriction=raw["usage_restriction"],
        teams={k: Team(**v) for k, v in raw["teams"].items()},
        agents={k: Agent(**v) for k, v in raw["agents"].items()},
        skills={k: Skill(**v) for k, v in raw["skills"].items()},
    )


def compute_content_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def fetch_upstream_file(repo: str, commit: str, path: str) -> bytes:
    """Fetch raw bytes of a file from upstream at the pinned commit."""
    out = subprocess.run(
        ["gh", "api", f"repos/{repo}/contents/{path}?ref={commit}", "--jq", ".content"],
        check=True, capture_output=True, text=True,
    )
    return base64.b64decode(out.stdout.strip())


def _frontmatter(data: dict[str, Any]) -> str:
    return "---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n"


BOUNDARIES_BODY = (
    "Nothing in this package constitutes peer-reviewed scholarship on its own. "
    "These agents draft research artifacts (literature searches, methodology blueprints, "
    "outlines, drafts, review reports, revision plans, formatted manuscripts) for review "
    "by a qualified human researcher. They do not submit to journals, sign authorship "
    "statements, make editorial decisions, or attest to research integrity on the user's "
    "behalf; every output is staged for human sign-off. The pipeline's integrity gates "
    "(2.5 / 4.5) and the 7-mode AI failure checklist are mandatory and not skippable."
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
            "usage_restriction": m.usage_restriction.strip(),
        },
    }
    body_lines = [
        f"# {m.name}",
        "",
        m.description,
        "",
        "## Usage restriction",
        "",
        m.usage_restriction.strip(),
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
    """The single top-level agent (team=None) that coordinates the teams, if any.

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
            tags = ["academic", "executive"]
            sources = [{"mode": "port-original"}]
        else:
            reports_to = f"../../teams/{agent.team}/TEAM.md"
            tags = ["academic", agent.team]
            sources = [
                {
                    "url": f"https://github.com/{m.upstream.repo}/tree/{m.upstream.commit}",
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
        if skill.port_original:
            # Hand-authored skill — its SKILL.md lives in the repo and must not be regenerated.
            # Verify that the file exists so the build fails fast on missing port-original content.
            out_dir = skills_root / slug
            if not (out_dir / "SKILL.md").exists():
                raise SystemExit(
                    f"Port-original skill {slug!r} declared in manifest but "
                    f"{out_dir / 'SKILL.md'} is missing. Author the file before running build."
                )
            continue
        if not skill.upstream_path:
            raise SystemExit(
                f"Skill {slug!r} is not port-original but has no upstream_path declared in manifest."
            )
        out_dir = skills_root / slug
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
                        "path": skill.upstream_path,
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
        lines.append(f'  "{agent_slug}" [label="{agent.name}", style="rounded,filled", fillcolor="#dcfce7"];')
        lines.append(f'  "{m.slug}" -> "{agent_slug}";')

    team_parent = coordinator if coordinator else m.slug
    for team_slug, team in m.teams.items():
        lines.append(f'  "{team_slug}" [label="{team.name}", fillcolor="#fef3c7", style="rounded,filled"];')
        lines.append(f'  "{team_parent}" -> "{team_slug}";')

    for agent_slug, agent in m.agents.items():
        if agent.team is None:
            continue
        lines.append(f'  "{agent_slug}" [label="{agent.name}"];')
        lines.append(f'  "{agent.team}" -> "{agent_slug}";')
    lines.append("}")
    return "\n".join(lines) + "\n"


def render_org_chart(dot_text: str, out_png: Path) -> None:
    """Render `dot_text` to a PNG via the `dot` CLI."""
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
    for slug, skill in upstream_skills.items():
        if not skill.upstream_path:
            raise SystemExit(f"Skill {slug!r} missing upstream_path")
        content = fetch_upstream_file(m.upstream.repo, m.upstream.commit, skill.upstream_path)
        hashes[slug] = compute_content_hash(content)
        print(f"  hashed {slug} ← {skill.upstream_path}")

    if port_original_skills:
        print(f"  port-original skills (hand-authored): {sorted(port_original_skills)}")

    emit_company(m, ROOT / "COMPANY.md")
    emit_teams(m, ROOT / "teams")
    emit_agents(m, ROOT / "agents")
    emit_skills(m, hashes, ROOT / "skills")

    dot = emit_org_chart_dot(m)
    (ROOT / "images").mkdir(exist_ok=True)
    (ROOT / "images" / "org-chart.dot").write_text(dot)
    try:
        render_org_chart(dot, ROOT / "images" / "org-chart.png")
    except FileNotFoundError:
        print("  (skipping org-chart.png render — `dot` CLI not installed)")

    print("Build complete.")


if __name__ == "__main__":
    main()
