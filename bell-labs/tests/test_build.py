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
    # Bell Labs is original synthesis — no upstream block in fixture
    assert m.upstream is None
    # Bell Labs has no usage_restriction
    assert m.usage_restriction is None
    assert "alpha" in m.agents
    # alpha is a top-level coordinator in the bell-labs fixture (no team)
    assert m.agents["alpha"].team is None
    assert m.agents["alpha"].skills == ["skill-port"]
    assert "beta" in m.agents
    assert m.agents["beta"].team == "team-a"
    assert "skill-port" in m.skills
    assert m.skills["skill-port"].port_original is True
    assert m.skills["skill-port"].upstream_path is None
    assert "team-a" in m.teams


def test_team_coordinator_picks_lone_top_level_agent():
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    # Fixture has exactly one top-level agent (alpha has no team) → alpha is coordinator
    assert team_coordinator(m) == "alpha"


def test_compute_content_hash_is_sha256_hex():
    content = b"hello world"
    h = compute_content_hash(content)
    # sha256("hello world")
    assert h == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"


def test_load_manifest_accepts_no_upstream():
    """Bell Labs is original synthesis — manifest has no `upstream:` block."""
    fixture = Path(__file__).parent / "fixtures" / "manifest_minimal.yaml"
    m = load_manifest(fixture)
    assert m.upstream is None  # not raised, just absent
    assert m.affiliation is None or isinstance(m.affiliation, str)
