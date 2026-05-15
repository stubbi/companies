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
