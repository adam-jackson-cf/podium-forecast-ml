"""Accepted and rejected guidance loading contracts and stack gate coverage."""

from pathlib import Path

import pytest

from verification.guidance import agent_problem, check_guidance, skill_problem
from verification.locations import check_location
from verification.policy import Policy, load_policy


@pytest.fixture
def policy() -> Policy:
    return load_policy(Path(__file__).resolve().parents[2] / "quality-policy.toml")


def skill_source(name: str = "scoring") -> str:
    return (
        f'---\nname: "{name}"\n'
        'description: "Use when implementing scoring."\n---\n'
        "# Guidance\n\nKeep types explicit."
    )


def agent_source(name: str = "design_reviewer", *, instructions: str | None = None) -> str:
    body = (
        instructions
        or """# Task
Review the proposed design.

## Input
Use the supplied change and evidence.

## Rules
Return a verdict and stop when evidence is missing.

## Output
Report the verdict and actionable findings."""
    )
    return (
        f'name = "{name}"\n'
        'description = "Review a proposed design against repository constraints."\n'
        f'developer_instructions = """{body}"""\n'
    )


def test_well_formed_skill_loads_without_semantic_rewriting(policy: Policy) -> None:
    assert (
        skill_problem(skill_source(), "scoring", policy.max_skill_words, policy.max_skill_lines)
        is None
    )


@pytest.mark.parametrize(
    "source,directory",
    [
        ("# Missing frontmatter", "scoring"),
        ('---\nname: "[broken"\n---\n# Guidance\nBody', "scoring"),
        (
            '---\nname: "other"\ndescription: "Use when scoring."\n---\n# Guidance\nBody',
            "scoring",
        ),
        (
            "---\nname: scoring\ndescription: 'Use when scoring.'\n---\n# Guidance\nBody",
            "scoring",
        ),
        (
            '---\nname: "scoring"\ndescription: "Always load this."\n---\n# Guidance\nBody',
            "scoring",
        ),
        (
            '---\nname: "scoring"\ndescription: "Use when scoring."\n---\nBody',
            "scoring",
        ),
        (
            '---\nname: "scoring"\ndescription: "Use when scoring."\n---\n# Guidance',
            "scoring",
        ),
    ],
)
def test_unloadable_skills_fail(source: str, directory: str, policy: Policy) -> None:
    assert (
        skill_problem(source, directory, policy.max_skill_words, policy.max_skill_lines) is not None
    )


@pytest.mark.parametrize("limit", ["words", "lines"])
def test_guidance_cannot_exceed_disclosure_budget(limit: str, policy: Policy) -> None:
    source = skill_source()
    if limit == "words":
        source += " word" * policy.max_skill_words
    else:
        source += "\nRule." * policy.max_skill_lines
    assert (
        skill_problem(source, "scoring", policy.max_skill_words, policy.max_skill_lines) is not None
    )


def test_complete_agent_contract_loads(policy: Policy) -> None:
    assert agent_problem(agent_source(), "design_reviewer", policy.max_agent_words) is None


@pytest.mark.parametrize(
    "source,stem",
    [
        ("not = [toml", "design_reviewer"),
        (
            agent_source().replace(
                'description = "Review a proposed design against repository constraints."\n',
                "",
            ),
            "design_reviewer",
        ),
        (agent_source() + 'extra = "field"\n', "design_reviewer"),
        (agent_source("DesignReviewer"), "DesignReviewer"),
        (agent_source("test_reviewer"), "design_reviewer"),
        (
            agent_source().replace(
                'description = "Review a proposed design against repository constraints."',
                'description = ""',
            ),
            "design_reviewer",
        ),
    ],
)
def test_invalid_agent_envelopes_fail(source: str, stem: str, policy: Policy) -> None:
    assert agent_problem(source, stem, policy.max_agent_words) is not None


@pytest.mark.parametrize("heading", ["# Task", "## Input", "## Rules", "## Output"])
def test_agent_contract_requires_each_populated_section(heading: str, policy: Policy) -> None:
    source = agent_source().replace(f"{heading}\n", "")
    assert agent_problem(source, "design_reviewer", policy.max_agent_words) is not None


def test_agent_contract_rejects_an_empty_section(policy: Policy) -> None:
    instructions = agent_source().replace(
        "## Rules\nReturn a verdict and stop when evidence is missing.\n\n## Output",
        "## Rules\n\n## Output",
    )
    assert agent_problem(instructions, "design_reviewer", policy.max_agent_words) is not None


def test_agent_instructions_cannot_exceed_disclosure_budget(policy: Policy) -> None:
    instructions = (
        """# Task
Review.
## Input
Use evidence.
## Rules
"""
        + "word " * policy.max_agent_words
        + """
## Output
Report."""
    )
    source = agent_source(instructions=instructions)
    assert agent_problem(source, "design_reviewer", policy.max_agent_words) is not None


def write_guidance_tree(root: Path) -> None:
    skill = root / "agent-guidance" / "skills" / "scoring" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(skill_source(), encoding="utf-8")
    agent = root / "agent-guidance" / "agents" / "design_reviewer.toml"
    agent.parent.mkdir(parents=True)
    agent.write_text(agent_source(), encoding="utf-8")


def test_root_and_scoped_dispatch_references_resolve(tmp_path: Path, policy: Policy) -> None:
    write_guidance_tree(tmp_path)
    (tmp_path / "AGENTS.md").write_text(
        "| Work | Read |\n| - | - |\n| Scoring | `agent-guidance/skills/scoring/SKILL.md` |",
        encoding="utf-8",
    )
    scope = tmp_path / "tests"
    scope.mkdir()
    (scope / "AGENTS.md").write_text(
        "Review with `agent-guidance/agents/design_reviewer.toml`.", encoding="utf-8"
    )
    assert not list(check_guidance(tmp_path, policy))


def test_missing_dispatch_reference_fails(tmp_path: Path, policy: Policy) -> None:
    (tmp_path / "AGENTS.md").write_text(
        "Read `agent-guidance/agents/missing_reviewer.toml`.", encoding="utf-8"
    )
    assert {finding.rule for finding in check_guidance(tmp_path, policy)} == {"GUIDE003"}


@pytest.mark.parametrize("symlink_part", ["file", "directory", "ancestor"])
def test_dispatch_rejects_symlink_paths(tmp_path: Path, policy: Policy, symlink_part: str) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "design_reviewer.toml").write_text(agent_source(), encoding="utf-8")
    guidance = tmp_path / "agent-guidance"
    agents = guidance / "agents"
    if symlink_part == "ancestor":
        guidance.symlink_to(outside, target_is_directory=True)
        (outside / "agents").mkdir()
        (outside / "agents" / "design_reviewer.toml").write_text(agent_source(), encoding="utf-8")
    elif symlink_part == "directory":
        guidance.mkdir()
        agents.symlink_to(outside, target_is_directory=True)
    else:
        guidance.mkdir()
        agents.mkdir()
        (agents / "design_reviewer.toml").symlink_to(outside / "design_reviewer.toml")
    (tmp_path / "AGENTS.md").write_text(
        "Read `agent-guidance/agents/design_reviewer.toml`.", encoding="utf-8"
    )
    assert "GUIDE003" in {finding.rule for finding in check_guidance(tmp_path, policy)}


def test_dispatch_rejects_escape_even_when_target_exists(tmp_path: Path, policy: Policy) -> None:
    target = tmp_path / "outside.toml"
    target.write_text(agent_source(), encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text(
        "Read `agent-guidance/agents/../../outside.toml`.", encoding="utf-8"
    )
    assert {finding.rule for finding in check_guidance(tmp_path, policy)} == {"GUIDE003"}


def test_malformed_canonical_assets_fail_repository_scan(tmp_path: Path, policy: Policy) -> None:
    skill = tmp_path / "agent-guidance" / "skills" / "scoring" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text("not frontmatter", encoding="utf-8")
    agent = tmp_path / "agent-guidance" / "agents" / "design_reviewer.toml"
    agent.parent.mkdir(parents=True)
    agent.write_text('name = "design_reviewer"', encoding="utf-8")
    assert {finding.rule for finding in check_guidance(tmp_path, policy)} == {
        "GUIDE001",
        "GUIDE002",
    }


@pytest.mark.parametrize("directory", [".agents/skills", ".agents/roles", ".codex/agents"])
def test_auto_discovery_guidance_is_rejected(
    tmp_path: Path, policy: Policy, directory: str
) -> None:
    discovered = tmp_path / directory / "instruction.md"
    discovered.parent.mkdir(parents=True)
    discovered.write_text("conditional guidance", encoding="utf-8")
    assert {finding.rule for finding in check_guidance(tmp_path, policy)} == {"GUIDE004"}


def test_auto_discovery_parent_symlink_is_rejected_without_traversal(
    tmp_path: Path, policy: Policy
) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    (tmp_path / ".agents").symlink_to(outside, target_is_directory=True)
    assert {finding.rule for finding in check_guidance(tmp_path, policy)} == {"GUIDE004"}


def test_isolated_fixture_without_guidance_remains_valid(tmp_path: Path, policy: Policy) -> None:
    (tmp_path / "module.py").write_text("value = 1\n", encoding="utf-8")
    assert not list(check_guidance(tmp_path, policy))


@pytest.mark.parametrize(
    "path",
    [
        "scripts/verify.sh",
        "containers/Dockerfile",
        "containers/worker.Dockerfile",
        "infra/terraform/modules/storage/main.tf",
        "infra/terraform/modules/storage/tests/security.tfvars",
        ".tflint.hcl",
        "infra/terraform/modules/storage/.terraform.lock.hcl",
        "infra/terraform/modules/storage/tests/contracts.tftest.hcl",
    ],
)
def test_registered_gate_locations_pass(path: str, policy: Policy) -> None:
    assert not list(check_location(path, policy))


@pytest.mark.parametrize(
    "path",
    [
        "nested/run.sh",
        "scripts/nested/run.sh",
        "Dockerfile",
        "containers/nested/worker.Dockerfile",
        "infra/terraform/modules/ungoverned/main.tf",
        "infra/terraform/modules/ungoverned/tests/security.tfvars",
        "other.hcl",
        "infra/terraform/modules/storage/ungoverned/main.tf",
        "infra/terraform/modules/storage/tests/main.tf",
        "infra/terraform/modules/storage/tests/unchecked.tfvars",
        "infra/terraform/modules/storage/tests/nested/contracts.tftest.hcl",
        "infra/terraform/modules/storage/tests/unchecked.hcl",
    ],
)
def test_new_executable_locations_require_gate_expansion(path: str, policy: Policy) -> None:
    assert {finding.rule for finding in check_location(path, policy)} == {"FILE003"}
