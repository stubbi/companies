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
