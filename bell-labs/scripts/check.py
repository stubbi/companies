"""Validation script for the Bell Labs Agent Company package."""
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


SHARED_RESEARCHER_CORE = {
    "technical-memorandum",
    "hallway-traversal",
    "two-track-operation",
    "colloquium-participation",
}

CEO_REQUIRED_SKILLS = {
    "onboarding-mission-interview", "intake-triage", "patron-budget",
    "escalation-routing", "monthly-summary",
}


def check_skill_files_present(package_root: Path, manifest: dict) -> None:
    """Every manifest skill has a skills/<slug>/SKILL.md file."""
    skills_dir = package_root / "skills"
    for slug in manifest.get("skills", {}):
        path = skills_dir / slug / "SKILL.md"
        if not path.exists():
            raise ValidationError(f"manifest skill {slug!r} has no SKILL.md at {path}")


def check_agent_skill_references(manifest: dict) -> None:
    """Every skill listed under an agent must exist in manifest.skills."""
    declared = set(manifest.get("skills", {}))
    for agent_slug, agent in manifest.get("agents", {}).items():
        for skill in agent.get("skills", []):
            if skill not in declared:
                raise ValidationError(
                    f"agent {agent_slug!r}: references undeclared skill {skill!r}"
                )


def check_team_assignments(manifest: dict) -> None:
    """Every agent's team: value must be a declared team slug."""
    declared = set(manifest.get("teams", {}))
    for agent_slug, agent in manifest.get("agents", {}).items():
        team = agent.get("team")
        if team is not None and team not in declared:
            raise ValidationError(
                f"agent {agent_slug!r}: team {team!r} is not declared in manifest.teams"
            )


def check_shared_researcher_core(manifest: dict) -> None:
    """Every agent with a team: field must list all four shared core skills."""
    for slug, agent in manifest.get("agents", {}).items():
        if "team" not in agent:
            continue  # company-level wise heads (CEO, Director) skip this check
        missing = SHARED_RESEARCHER_CORE - set(agent.get("skills", []))
        if missing:
            raise ValidationError(
                f"agent {slug!r}: missing shared researcher core skills "
                f"{sorted(missing)}; every researcher must reference all of "
                f"{sorted(SHARED_RESEARCHER_CORE)}"
            )


def check_ceo_skills(manifest: dict) -> None:
    """The CEO has exactly the 5 patron skills — no shared researcher core."""
    ceo = manifest.get("agents", {}).get("ceo")
    if ceo is None:
        return  # not bell-labs; skip
    skills = set(ceo.get("skills", []))
    if skills != CEO_REQUIRED_SKILLS:
        extra = skills - CEO_REQUIRED_SKILLS
        missing = CEO_REQUIRED_SKILLS - skills
        raise ValidationError(
            f"CEO skills mismatch — missing {sorted(missing)} extra {sorted(extra)}; "
            "CEO is patron-only, no shared researcher core."
        )


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
    """Run all checks. Exits 0 on success, 1 on first ValidationError."""
    try:
        # 1. Schema validation across every manifest
        for kind, glob in [
            ("company", "COMPANY.md"),
            ("team", "teams/*/TEAM.md"),
            ("agent", "agents/*/AGENTS.md"),
            ("skill", "skills/*/SKILL.md"),
        ]:
            for path in ROOT.glob(glob):
                fm = parse_frontmatter(path.read_text())
                validate_frontmatter(kind, fm)

        # 2. Cross-references
        check_cross_references(ROOT)

        # 3. Content-hash freshness (network — slow)
        check_content_hashes(ROOT)

        # 4. Bell-Labs-specific invariants
        with open(ROOT / "manifest.yaml") as f:
            manifest = yaml.safe_load(f)
        check_skill_files_present(ROOT, manifest)
        check_agent_skill_references(manifest)
        check_team_assignments(manifest)
        check_shared_researcher_core(manifest)
        check_ceo_skills(manifest)

    except ValidationError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        return 1
    print("OK: schema, cross-references, content hashes, bell-labs invariants all valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
