from pathlib import Path

from scripts.build import (
    compute_content_hash,
    load_manifest,
    team_coordinator,
)


def test_load_manifest_returns_structured_object():
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    assert m.slug == "test-co"
    assert m.upstream.commit == "deadbeef"
    assert m.usage_restriction.startswith("Non-commercial")
    assert "alpha" in m.agents
    assert m.agents["alpha"].team == "team-a"
    assert m.agents["alpha"].skills == ["skill-1"]
    assert "skill-1" in m.skills
    assert m.skills["skill-1"].upstream_path == "skill-1/SKILL.md"
    assert m.skills["skill-1"].port_original is False
    assert m.skills["skill-port"].port_original is True
    assert m.skills["skill-port"].upstream_path is None
    assert "team-a" in m.teams


def test_team_coordinator_picks_lone_top_level_agent():
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    # Fixture has no top-level agent (alpha has team=team-a) → no coordinator
    assert team_coordinator(m) is None


def test_compute_content_hash_is_sha256_hex():
    content = b"hello world"
    h = compute_content_hash(content)
    # sha256("hello world")
    assert h == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
