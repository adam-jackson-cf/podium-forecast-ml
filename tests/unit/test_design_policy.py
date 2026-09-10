"""Behavioral positive and negative examples for custom design constraints."""

from pathlib import Path

import pytest

from verification.architecture import check_architecture
from verification.policy import Policy, load_policy
from verification.python_design import check_python
from verification.repository import check_comments, check_repository
from verification.test_execution import check_test_bypass


@pytest.fixture
def policy() -> Policy:
    """Use the real canonical policy for behavioral checks."""
    return load_policy(Path(__file__).resolve().parents[2] / "quality-policy.toml")


@pytest.mark.parametrize(
    "source",
    [
        "for race in races:\n    score(race)\nfor race in races:\n    publish(race)",
        "scores = [score(race) for race in races]",
        "while pending:\n    advance()",
        "async def fetch():\n    async for race in races:\n        await score(race)",
    ],
)
def test_independent_iteration_passes(source: str, policy: Policy) -> None:
    assert not list(check_python("scores.py", source, policy))


@pytest.mark.parametrize(
    "source",
    [
        "for race in races:\n    for runner in race:\n        score(runner)",
        "scores = [score(runner) for race in races for runner in race]",
        "scores = [[score(runner) for runner in race] for race in races]",
        "for race in races:\n    scores = {runner: score(runner) for runner in race}",
        "while pending:\n    while retries:\n        advance()",
        "async def fetch():\n    async for race in races:\n"
        "        for runner in race:\n            score(runner)",
    ],
)
def test_nested_iteration_requires_decomposition(source: str, policy: Policy) -> None:
    assert {finding.rule for finding in check_python("scores.py", source, policy)} == {"PY001"}


@pytest.mark.parametrize("name", ["RaceManager", "helper", "prepare_data", "ForecastProcessor"])
def test_generic_declarations_require_specific_responsibilities(name: str, policy: Policy) -> None:
    assert list(check_python("scores.py", f"def {name}():\n    pass", policy))


@pytest.mark.parametrize("name", ["RaceSnapshot", "calculate_probability", "DatasetManifest"])
def test_specific_declarations_pass(name: str, policy: Policy) -> None:
    assert not list(check_python("scores.py", f"class {name}:\n    pass", policy))


@pytest.mark.parametrize(
    ("layer", "source"),
    [
        ("domain", "from dataclasses import dataclass"),
        ("application", "from podium_forecasting.ports import ForecastStore"),
        ("adapters", "import boto3"),
        ("entrypoints", "from podium_forecasting.adapters import storage"),
        ("application", "from ..ports import ForecastStore"),
    ],
)
def test_allowed_dependencies_pass(layer: str, source: str, policy: Policy) -> None:
    assert not list(check_architecture(f"src/podium_forecasting/{layer}/scores.py", source, policy))


@pytest.mark.parametrize(
    ("layer", "source"),
    [
        ("domain", "import boto3"),
        ("domain", "from podium_forecasting.adapters import storage"),
        ("application", "from ..adapters import storage"),
        ("ports", "from podium_forecasting.application import evaluate"),
        ("application", "from podium_forecasting import adapters"),
        ("adapters", "from podium_forecasting.entrypoints import cli"),
    ],
)
def test_forbidden_dependencies_fail(layer: str, source: str, policy: Policy) -> None:
    assert list(check_architecture(f"src/podium_forecasting/{layer}/scores.py", source, policy))


@pytest.mark.parametrize(
    "comment", ["# noqa: E501", "# type: ignore[arg-type]", "# pragma: no cover"]
)
def test_suppression_comments_fail(comment: str) -> None:
    assert list(check_comments("scores.py", f"score = 1 {comment}"))
    assert not list(check_comments("fixture.py", repr(comment)))


@pytest.mark.parametrize(
    "source",
    ["pytest.skip('missing service')", "@pytest.mark.skipif(True)\ndef test_score(): pass"],
)
def test_tests_cannot_silently_disappear(source: str) -> None:
    assert list(check_test_bypass("test_scores.py", source))
    assert not list(check_test_bypass("test_fixture.py", repr(source)))


def test_unregistered_technology_fails_before_implementation(
    tmp_path: Path, policy: Policy
) -> None:
    (tmp_path / "score.ts").write_text("export const score = 1", encoding="utf-8")
    assert {finding.rule for finding in check_repository(tmp_path, policy)} == {"FILE001"}


def test_generated_environments_are_not_maintained_sources(tmp_path: Path, policy: Policy) -> None:
    generated = tmp_path / ".venv"
    generated.mkdir()
    (generated / "foreign.ts").write_text("", encoding="utf-8")
    (tmp_path / "scores.py").write_text("probability = 0.5", encoding="utf-8")
    assert not check_repository(tmp_path, policy)


def test_generic_module_names_are_rejected(tmp_path: Path, policy: Policy) -> None:
    (tmp_path / "utils.py").write_text("", encoding="utf-8")
    assert {finding.rule for finding in check_repository(tmp_path, policy)} == {"PY002"}


def test_invalid_syntax_cannot_pass(policy: Policy) -> None:
    assert {finding.rule for finding in check_python("scores.py", "def broken(", policy)} == {
        "PY000"
    }


def test_nested_function_iteration_has_its_own_execution_scope(policy: Policy) -> None:
    source = (
        "for race in races:\n    def score_runners():\n"
        "        for runner in race:\n            score(runner)"
    )
    assert not list(check_python("scores.py", source, policy))


@pytest.mark.parametrize("path", ["src/rogue.py", "src/other/scores.py"])
def test_production_modules_cannot_escape_layer_checks(path: str, policy: Policy) -> None:
    assert list(check_architecture(path, "import boto3", policy))


def test_package_initializer_cannot_hide_an_adapter_dependency(policy: Policy) -> None:
    assert list(check_architecture("src/podium_forecasting/__init__.py", "import boto3", policy))


@pytest.mark.parametrize(
    "source",
    [
        "open('snapshot.json')",
        "import os as operating\noperating.getenv('RACE_DATE')",
        "from os import environ as settings\nregion = settings['AWS_REGION']",
        "from subprocess import run as execute\nexecute(['forecast'])",
        "from pathlib import Path as FilePath\nFilePath('snapshot').read_text()",
        "from pathlib import Path\nPath.write_text(Path('snapshot'), 'result')",
        "import urllib.request as request\nrequest.urlopen('https://example.invalid')",
        "import urllib.request\nurllib.request.urlopen('https://example.invalid')",
    ],
)
def test_core_layers_reject_configured_direct_effects_and_import_aliases(
    source: str, policy: Policy
) -> None:
    findings = list(
        check_architecture("src/podium_forecasting/application/forecast.py", source, policy)
    )
    assert "ARCH003" in {finding.rule for finding in findings}


@pytest.mark.parametrize(
    ("path", "source"),
    [
        (
            "src/podium_forecasting/domain/race.py",
            "from pathlib import Path\nlocation = Path('snapshots') / 'race.json'",
        ),
        (
            "src/podium_forecasting/ports/snapshots.py",
            "from pathlib import PurePath\n"
            "def suffix(path: PurePath) -> str:\n    return path.suffix",
        ),
        (
            "src/podium_forecasting/adapters/storage.py",
            "from pathlib import Path\ncontent = Path('snapshot').read_text()",
        ),
    ],
)
def test_pure_path_operations_and_adapter_owned_effects_pass(
    path: str, source: str, policy: Policy
) -> None:
    assert not list(check_architecture(path, source, policy))


def test_effect_check_is_bounded_to_direct_calls(policy: Policy) -> None:
    source = "from pathlib import Path\nlocation = Path('snapshot')\nlocation.read_text()"
    assert not list(check_architecture("src/podium_forecasting/domain/race.py", source, policy))


def test_relative_imports_in_package_initializers_respect_layers(policy: Policy) -> None:
    assert list(
        check_architecture(
            "src/podium_forecasting/domain/__init__.py", "from ..adapters import storage", policy
        )
    )


@pytest.mark.parametrize(
    "source",
    [
        "import pytest as checks\nchecks.skip('missing')",
        "from pytest import skip as omit\nomit('missing')",
        "import unittest as checks\n@checks.skip('missing')\nclass Scenario: pass",
        "pytest.importorskip('optional')",
        "self.skipTest('missing')",
    ],
)
def test_aliases_cannot_hide_test_bypasses(source: str) -> None:
    assert list(check_test_bypass("test_scores.py", source))


@pytest.mark.parametrize("source", ["data = []", "def calculate(data):\n    return data"])
def test_owned_bindings_must_name_their_content(source: str, policy: Policy) -> None:
    assert list(check_python("scores.py", source, policy))


@pytest.mark.parametrize(
    ("filename", "source"),
    [
        ("scripts/build.sh", "# shellcheck disable=SC2086"),
        ("infra/terraform/modules/storage/main.tf", "# checkov:skip=CKV_AWS_1:later"),
        ("containers/Dockerfile", "# hadolint ignore=DL3008"),
    ],
)
def test_infrastructure_cannot_suppress_gates(
    tmp_path: Path, policy: Policy, filename: str, source: str
) -> None:
    target = tmp_path / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source, encoding="utf-8")
    assert {finding.rule for finding in check_repository(tmp_path, policy)} == {"GATE001"}


def test_source_symlinks_cannot_escape_repository(tmp_path: Path, policy: Policy) -> None:
    (tmp_path / "scores.py").symlink_to("/nonexistent/external.py")
    assert {finding.rule for finding in check_repository(tmp_path, policy)} == {"FILE002"}
