"""Exercise the production external-check entrypoint against isolated repositories."""

import os
import shutil
import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest
import yaml

REPOSITORY = Path(__file__).resolve().parents[2]
CHECK_CONTRACTS = REPOSITORY / "scripts" / "check-contracts.sh"


@pytest.fixture
def external_check_root(tmp_path: Path) -> Path:
    for relative_path in (
        Path("pyproject.toml"),
        Path("src/podium_forecasting"),
        Path(".github/workflows"),
        Path("infra/local/compose.yaml"),
    ):
        source = REPOSITORY / relative_path
        destination = tmp_path / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, destination, dirs_exist_ok=True)
        else:
            shutil.copyfile(source, destination)
    return tmp_path


def run_external_checks(root: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["DOCKER_HOST"] = "unix:///tmp/podium-no-docker-daemon.sock"
    return subprocess.run(
        [CHECK_CONTRACTS, root],
        cwd=REPOSITORY,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


def test_complete_safe_fixture_passes_without_a_docker_daemon(external_check_root: Path) -> None:
    result = run_external_checks(external_check_root)
    assert result.returncode == 0, result.stderr


def test_package_cycle_blocks_the_external_gate(external_check_root: Path) -> None:
    package = external_check_root / "src/podium_forecasting"
    alpha = package / "alpha"
    beta = package / "beta"
    alpha.mkdir()
    beta.mkdir()
    (alpha / "__init__.py").write_text("import podium_forecasting.beta\n", encoding="utf-8")
    (beta / "__init__.py").write_text("import podium_forecasting.alpha\n", encoding="utf-8")

    result = run_external_checks(external_check_root)

    assert result.returncode != 0
    assert "Package siblings remain acyclic BROKEN" in result.stdout
    assert "It could be made acyclic" in result.stdout


def test_risky_workflow_blocks_the_external_gate(external_check_root: Path) -> None:
    workflow = external_check_root / ".github/workflows/risky.yaml"
    workflow.write_text(
        """name: Risky
on: push
permissions: {}
jobs:
  risky:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@main
""",
        encoding="utf-8",
    )

    result = run_external_checks(external_check_root)

    assert result.returncode != 0
    assert "unpinned-uses" in result.stdout


def test_malformed_workflow_blocks_the_external_gate(external_check_root: Path) -> None:
    workflow = external_check_root / ".github/workflows/malformed.yaml"
    workflow.write_text("name: [unterminated\n", encoding="utf-8")

    result = run_external_checks(external_check_root)

    assert result.returncode != 0
    assert "failed to load" in result.stderr.lower()


def remove_package(root: Path) -> None:
    shutil.rmtree(root / "src/podium_forecasting")


def remove_config(root: Path) -> None:
    (root / "pyproject.toml").unlink()


def remove_workflows(root: Path) -> None:
    shutil.rmtree(root / ".github/workflows")


def remove_compose(root: Path) -> None:
    (root / "infra/local/compose.yaml").unlink()


def empty_package(root: Path) -> None:
    for source in (root / "src/podium_forecasting").rglob("*.py"):
        source.write_text("", encoding="utf-8")


def empty_config(root: Path) -> None:
    (root / "pyproject.toml").write_text("", encoding="utf-8")


def empty_workflows(root: Path) -> None:
    for workflow in (root / ".github/workflows").glob("*.yaml"):
        workflow.write_text("", encoding="utf-8")


def empty_compose(root: Path) -> None:
    (root / "infra/local/compose.yaml").write_text("", encoding="utf-8")


@pytest.mark.parametrize(
    ("invalidate_required_input", "diagnostic"),
    [
        (remove_package, "nonempty podium_forecasting Python package"),
        (remove_config, "nonempty pyproject.toml"),
        (remove_workflows, "workflow directory with nonempty YAML input"),
        (remove_compose, "nonempty Compose file"),
        (empty_package, "nonempty podium_forecasting Python package"),
        (empty_config, "nonempty pyproject.toml"),
        (empty_workflows, "workflow directory with nonempty YAML input"),
        (empty_compose, "nonempty Compose file"),
    ],
    ids=[
        "missing-package",
        "missing-config",
        "missing-workflows",
        "missing-compose",
        "empty-package",
        "empty-config",
        "empty-workflows",
        "empty-compose",
    ],
)
def test_missing_or_empty_required_input_blocks_before_scanning(
    external_check_root: Path,
    invalidate_required_input: Callable[[Path], None],
    diagnostic: str,
) -> None:
    invalidate_required_input(external_check_root)

    result = run_external_checks(external_check_root)

    assert result.returncode != 0
    assert diagnostic in result.stderr


def test_malformed_compose_blocks_the_rendered_policy_pipeline(external_check_root: Path) -> None:
    compose_file = external_check_root / "infra/local/compose.yaml"
    compose_file.write_text("services: [unterminated\n", encoding="utf-8")

    result = run_external_checks(external_check_root)

    assert result.returncode != 0
    assert "yaml" in result.stderr.lower()


def test_unsafe_service_in_optional_profile_blocks_the_external_gate(
    external_check_root: Path,
) -> None:
    compose_file = external_check_root / "infra/local/compose.yaml"
    compose = yaml.safe_load(compose_file.read_text(encoding="utf-8"))
    compose["services"]["unsafe-optional"] = {
        "image": compose["services"]["postgres"]["image"],
        "privileged": True,
        "profiles": ["unsafe-verification"],
        "networks": ["foundation"],
    }
    compose_file.write_text(yaml.safe_dump(compose, sort_keys=False), encoding="utf-8")

    result = run_external_checks(external_check_root)

    assert result.returncode != 0
    assert "COMPOSE002" in result.stderr
