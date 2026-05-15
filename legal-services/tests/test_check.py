import yaml
from pathlib import Path
import pytest

from scripts.check import (
    parse_frontmatter,
    validate_frontmatter,
    check_cross_references,
    ValidationError,
)


def test_parse_frontmatter_extracts_yaml_block():
    text = "---\nslug: foo\nname: Foo\n---\nbody\n"
    fm = parse_frontmatter(text)
    assert fm["slug"] == "foo"
    assert fm["name"] == "Foo"


def test_parse_frontmatter_no_frontmatter_raises():
    with pytest.raises(ValidationError, match="frontmatter"):
        parse_frontmatter("no frontmatter\n")


def test_parse_frontmatter_unterminated_raises():
    with pytest.raises(ValidationError, match="unterminated"):
        parse_frontmatter("---\nslug: foo\n")


def test_validate_frontmatter_company_requires_fields():
    fm = {"schema": "agentcompanies/v1", "slug": "x"}
    with pytest.raises(ValidationError, match="missing required fields"):
        validate_frontmatter("company", fm)


def test_validate_frontmatter_unknown_kind_raises():
    with pytest.raises(ValidationError, match="unknown kind"):
        validate_frontmatter("bogus", {})


def test_check_cross_references_detects_dangling_skill(tmp_path):
    agents_dir = tmp_path / "agents" / "alpha"
    agents_dir.mkdir(parents=True)
    (agents_dir / "AGENTS.md").write_text(
        "---\nslug: alpha\nname: Alpha\ntitle: A\nreportsTo: x\nskills: [ghost]\n---\n"
    )
    (tmp_path / "skills").mkdir()
    with pytest.raises(ValidationError, match="missing skill"):
        check_cross_references(tmp_path)


def test_check_cross_references_passes_when_skill_present(tmp_path):
    agents_dir = tmp_path / "agents" / "alpha"
    agents_dir.mkdir(parents=True)
    (agents_dir / "AGENTS.md").write_text(
        "---\nslug: alpha\nname: Alpha\ntitle: A\nreportsTo: x\nskills: [present]\n---\n"
    )
    (tmp_path / "skills" / "present").mkdir(parents=True)
    check_cross_references(tmp_path)  # no raise
