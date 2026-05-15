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


from scripts.build import compute_content_hash


def test_compute_content_hash_is_sha256_hex():
    h = compute_content_hash(b"hello world")
    assert h == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"


from scripts.build import upstream_path_for_skill


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
