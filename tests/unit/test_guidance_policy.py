"""Accepted and rejected guidance loading contracts and stack gate coverage."""

from dataclasses import replace
from pathlib import Path

import pytest

from verification.guidance import check_guidance, role_problem, skill_problem
from verification.locations import check_location
from verification.policy import Policy, load_policy


@pytest.fixture
def policy() -> Policy:
    return load_policy(Path(__file__).resolve().parents[2] / "quality-policy.toml")


def test_well_formed_skill_loads_without_semantic_rewriting(policy: Policy) -> None:
    source = (
        '---\nname: scoring\ndescription: "Use when implementing scoring."\n---\n'
        "# Guidance\nKeep types explicit."
    )
    assert skill_problem(source, "scoring", policy.max_skill_words) is None


@pytest.mark.parametrize(
    "source",
    [
        "# Missing frontmatter",
        "---\nname: [broken\n---\nBody",
        "---\nname: other\ndescription: Use when scoring.\n---\nBody",
        "---\nname: scoring\ndescription: Always load this.\n---\nBody",
        "---\nname: scoring\ndescription: Use when scoring.\n---\n",
    ],
)
def test_unloadable_skills_fail(source: str, policy: Policy) -> None:
    assert skill_problem(source, "scoring", policy.max_skill_words) is not None


def test_guidance_cannot_exceed_disclosure_budget(policy: Policy) -> None:
    source = "---\nname: scoring\ndescription: Use when scoring.\n---\n" + "word " * (
        policy.max_skill_words + 1
    )
    assert skill_problem(source, "scoring", policy.max_skill_words) is not None


def role_source(policy: Policy) -> str:
    return "\n".join(f"{field}: Assigned responsibility." for field in policy.role_fields)


def test_complete_role_contract_loads(policy: Policy) -> None:
    assert role_problem(role_source(policy), policy) is None


@pytest.mark.parametrize("omitted", ["Authority", "Evidence", "Stop condition", "Output"])
def test_incomplete_role_contracts_fail(omitted: str, policy: Policy) -> None:
    source = role_source(policy).replace(f"{omitted}: Assigned responsibility.", "")
    assert role_problem(source, policy) is not None


def test_empty_and_overlong_roles_fail(policy: Policy) -> None:
    assert role_problem("", policy) is not None
    assert role_problem(role_source(policy), replace(policy, max_role_words=1)) is not None


def test_dispatch_references_must_resolve(tmp_path: Path, policy: Policy) -> None:
    role = tmp_path / ".agents" / "roles" / "reviewer.md"
    role.parent.mkdir(parents=True)
    role.write_text(role_source(policy), encoding="utf-8")
    dispatch = tmp_path / "AGENTS.md"
    dispatch.write_text("Read `.agents/roles/reviewer.md`.", encoding="utf-8")
    assert not list(check_guidance(tmp_path, policy))
    role.unlink()
    assert {finding.rule for finding in check_guidance(tmp_path, policy)} == {"GUIDE003"}


def test_malformed_skill_fails_repository_scan(tmp_path: Path, policy: Policy) -> None:
    skill = tmp_path / ".agents" / "skills" / "scoring" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text("not frontmatter", encoding="utf-8")
    assert {finding.rule for finding in check_guidance(tmp_path, policy)} == {"GUIDE001"}


def test_incomplete_role_fails_repository_scan(tmp_path: Path, policy: Policy) -> None:
    role = tmp_path / ".agents" / "roles" / "reviewer.md"
    role.parent.mkdir(parents=True)
    role.write_text("Objective: Review.", encoding="utf-8")
    assert {finding.rule for finding in check_guidance(tmp_path, policy)} == {"GUIDE002"}


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
