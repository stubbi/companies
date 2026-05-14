import pytest

from scripts.check import (
    ValidationError,
    check_cross_references,
    parse_frontmatter,
    validate_frontmatter,
)


def test_validate_frontmatter_rejects_missing_required_field():
    bad = {"slug": "x", "title": "X-er", "reportsTo": "../../teams/t/TEAM.md", "skills": ["s"]}  # missing name
    with pytest.raises(ValidationError, match="name"):
        validate_frontmatter("agent", bad)


def test_validate_frontmatter_accepts_complete_agent():
    good = {
        "slug": "x", "name": "X", "title": "X-er",
        "reportsTo": "../../teams/t/TEAM.md", "skills": ["s"],
    }
    validate_frontmatter("agent", good)  # no exception


def test_validate_frontmatter_rejects_unknown_kind():
    with pytest.raises(ValidationError, match="unknown kind"):
        validate_frontmatter("nonsense", {})


def test_parse_frontmatter_rejects_missing_opener():
    with pytest.raises(ValidationError, match="frontmatter"):
        parse_frontmatter("no frontmatter here")


def test_parse_frontmatter_rejects_unterminated():
    with pytest.raises(ValidationError, match="unterminated"):
        parse_frontmatter("---\nslug: x\nname: y\n")


def test_check_cross_references_rejects_missing_skill(tmp_path):
    (tmp_path / "agents" / "alpha").mkdir(parents=True)
    (tmp_path / "agents" / "alpha" / "AGENTS.md").write_text(
        "---\nkind: agent\nslug: alpha\nname: Alpha\ntitle: A\n"
        "reportsTo: ../../teams/t/TEAM.md\nskills: [does-not-exist]\n---\n"
    )
    (tmp_path / "skills").mkdir()  # empty
    with pytest.raises(ValidationError, match="does-not-exist"):
        check_cross_references(tmp_path)


def test_check_cross_references_passes_when_all_resolve(tmp_path):
    (tmp_path / "agents" / "alpha").mkdir(parents=True)
    (tmp_path / "agents" / "alpha" / "AGENTS.md").write_text(
        "---\nkind: agent\nslug: alpha\nname: Alpha\ntitle: A\n"
        "reportsTo: ../../teams/t/TEAM.md\nskills: [present]\n---\n"
    )
    (tmp_path / "skills" / "present").mkdir(parents=True)
    (tmp_path / "skills" / "present" / "SKILL.md").write_text(
        "---\nkind: skill\nslug: present\nname: P\ndescription: x\n---\n"
    )
    check_cross_references(tmp_path)  # no exception


def test_check_content_hashes_noop_when_no_referenced_skills(tmp_path):
    """No referenced skills = no upstream fetch needed."""
    from scripts.check import check_content_hashes
    # An empty skills dir contains no SKILL.md files, so check_content_hashes is a no-op.
    (tmp_path / "skills").mkdir()
    check_content_hashes(tmp_path)  # must not raise


# ── New bell-labs-specific checks ──────────────────────────────────────────


def test_check_skill_files_present_raises_when_file_missing(tmp_path):
    from scripts.check import check_skill_files_present, ValidationError
    # manifest declares "my-skill" but no skills/my-skill/SKILL.md exists
    manifest = {"skills": {"my-skill": {"name": "My Skill", "description": "x"}}}
    (tmp_path / "skills" / "my-skill").mkdir(parents=True)
    # intentionally do NOT create SKILL.md
    with pytest.raises(ValidationError, match="my-skill"):
        check_skill_files_present(tmp_path, manifest)


def test_check_skill_files_present_passes_when_all_present(tmp_path):
    from scripts.check import check_skill_files_present
    manifest = {"skills": {"ok-skill": {"name": "OK Skill", "description": "x"}}}
    skill_dir = tmp_path / "skills" / "ok-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nslug: ok-skill\n---\n")
    check_skill_files_present(tmp_path, manifest)  # must not raise


def test_check_agent_skill_references_raises_for_undeclared_skill():
    from scripts.check import check_agent_skill_references, ValidationError
    bad = {
        "agents": {
            "alpha": {"name": "Alpha", "title": "A", "skills": ["ghost-skill"]},
        },
        "skills": {"real-skill": {}},
    }
    with pytest.raises(ValidationError, match="ghost-skill"):
        check_agent_skill_references(bad)


def test_check_agent_skill_references_passes_when_all_declared():
    from scripts.check import check_agent_skill_references
    good = {
        "agents": {
            "alpha": {"name": "Alpha", "title": "A", "skills": ["real-skill"]},
        },
        "skills": {"real-skill": {}},
    }
    check_agent_skill_references(good)  # must not raise


def test_check_team_assignments_raises_for_unknown_team():
    from scripts.check import check_team_assignments, ValidationError
    bad = {
        "agents": {
            "alpha": {"name": "Alpha", "title": "A", "team": "phantom-team", "skills": []},
        },
        "teams": {"real-team": {"name": "Real", "description": "x", "includes": []}},
    }
    with pytest.raises(ValidationError, match="phantom-team"):
        check_team_assignments(bad)


def test_check_team_assignments_passes_for_declared_team():
    from scripts.check import check_team_assignments
    good = {
        "agents": {
            "alpha": {"name": "Alpha", "title": "A", "team": "real-team", "skills": []},
        },
        "teams": {"real-team": {"name": "Real", "description": "x", "includes": []}},
    }
    check_team_assignments(good)  # must not raise


def test_shared_researcher_core_required_on_every_researcher():
    from scripts.check import check_shared_researcher_core, ValidationError
    bad = {
        "agents": {
            "ceo": {"name": "CEO", "title": "Patron", "skills": ["intake-triage"]},
            "theorist": {"name": "Theorist", "title": "T", "team": "theory",
                         "skills": ["abstraction-build"]},  # missing shared core
        },
        "skills": {"intake-triage": {}, "abstraction-build": {}},
    }
    with pytest.raises(ValidationError, match="theorist"):
        check_shared_researcher_core(bad)


def test_shared_researcher_core_passes_when_all_core_present():
    from scripts.check import check_shared_researcher_core
    good = {
        "agents": {
            "theorist": {
                "name": "Theorist", "title": "T", "team": "theory",
                "skills": [
                    "abstraction-build", "technical-memorandum",
                    "hallway-traversal", "two-track-operation", "colloquium-participation",
                ],
            },
        },
    }
    check_shared_researcher_core(good)  # must not raise


def test_check_ceo_skills_raises_for_wrong_skillset():
    from scripts.check import check_ceo_skills, ValidationError
    bad = {
        "agents": {
            "ceo": {"name": "CEO", "title": "Patron",
                    "skills": ["intake-triage", "technical-memorandum"]},  # wrong set
        },
    }
    with pytest.raises(ValidationError, match="CEO"):
        check_ceo_skills(bad)


def test_check_ceo_skills_passes_for_exact_patron_skills():
    from scripts.check import check_ceo_skills
    good = {
        "agents": {
            "ceo": {
                "name": "CEO", "title": "Patron",
                "skills": [
                    "onboarding-mission-interview", "intake-triage",
                    "patron-budget", "escalation-routing", "monthly-summary",
                ],
            },
        },
    }
    check_ceo_skills(good)  # must not raise
