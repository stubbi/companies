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
