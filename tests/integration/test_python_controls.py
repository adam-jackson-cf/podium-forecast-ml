"""Run pinned Ruff and mypy against isolated behavior fixtures."""

import shutil
import subprocess
from pathlib import Path

import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
UV = shutil.which("uv")


def run_tool(*arguments: str, cwd: Path = REPOSITORY) -> subprocess.CompletedProcess[str]:
    """Use the locked environment and production configuration."""
    assert UV is not None
    return subprocess.run(
        [UV, "run", "--project", str(REPOSITORY), "--frozen", "--no-sync", *arguments],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.parametrize(
    ("source", "rule"),
    [
        ("try:\n    raise RuntimeError\nexcept Exception:\n    pass\n", "BLE001"),
        ("from datetime import datetime\nnow = datetime.now()\n", "DTZ005"),
        ("import logging\nname = 'race'\nlogging.info(f'forecast {name}')\n", "G004"),
        ("import pytest\nwith pytest.raises(ValueError):\n    int('race')\n", "PT011"),
        (
            "import pytest\nwith pytest.raises(ValueError, match='bad'):\n"
            "    int('race')\n    int('runner')\n",
            "PT012",
        ),
    ],
)
def test_production_ruff_configuration_rejects_new_bad_behaviors(
    tmp_path: Path, source: str, rule: str
) -> None:
    fixture = tmp_path / "fixture.py"
    fixture.write_text(source, encoding="utf-8")
    result = run_tool("ruff", "check", "--config", str(REPOSITORY / "pyproject.toml"), str(fixture))
    assert result.returncode != 0
    assert rule in result.stdout


def test_production_ruff_configuration_accepts_valid_patterns(tmp_path: Path) -> None:
    fixture = tmp_path / "fixture.py"
    fixture.write_text(
        "import logging\n"
        "from datetime import UTC, datetime\n\n"
        "logging.info('forecast %s', datetime.now(tz=UTC))\n",
        encoding="utf-8",
    )
    result = run_tool("ruff", "check", "--config", str(REPOSITORY / "pyproject.toml"), str(fixture))
    assert result.returncode == 0, result.stdout


@pytest.mark.parametrize(
    ("source", "error_code"),
    [
        (
            "from enum import Enum\n\nclass State(Enum):\n    READY = 'ready'\n"
            "    FAILED = 'failed'\n\ndef label(state: State) -> str:\n"
            "    match state:\n        case State.READY:\n            return 'ready'\n",
            "exhaustive-match",
        ),
        (
            "class Pending:\n    def __await__(self):\n        yield\n        return 1\n\n"
            "def start() -> Pending:\n    return Pending()\n\n"
            "def consume() -> None:\n    start()\n",
            "unused-awaitable",
        ),
    ],
)
def test_production_mypy_configuration_enables_optional_checks(
    tmp_path: Path, source: str, error_code: str
) -> None:
    package = tmp_path / "podium_forecasting" / "domain"
    package.mkdir(parents=True)
    fixture = package / "fixture.py"
    fixture.write_text(source, encoding="utf-8")
    result = run_tool(
        "mypy", "--config-file", str(REPOSITORY / "pyproject.toml"), str(fixture), cwd=tmp_path
    )
    assert result.returncode != 0
    assert f"[{error_code}]" in result.stdout


def test_core_any_checks_are_scoped_to_production_package(tmp_path: Path) -> None:
    package = tmp_path / "podium_forecasting" / "application"
    package.mkdir(parents=True)
    core = package / "forecast.py"
    core.write_text("from typing import Any\nvalue: Any = 1\n", encoding="utf-8")
    result = run_tool(
        "mypy", "--config-file", str(REPOSITORY / "pyproject.toml"), str(core), cwd=tmp_path
    )
    assert result.returncode != 0
    assert "[explicit-any]" in result.stdout


def test_production_mypy_configuration_accepts_typed_core_and_adapter_any(tmp_path: Path) -> None:
    core_package = tmp_path / "podium_forecasting" / "domain"
    adapter_package = tmp_path / "podium_forecasting" / "adapters"
    core_package.mkdir(parents=True)
    adapter_package.mkdir(parents=True)
    (core_package / "race.py").write_text(
        "def race_name(number: int) -> str:\n    return str(number)\n", encoding="utf-8"
    )
    (adapter_package / "client.py").write_text(
        "from typing import Any\nresponse: Any = {'status': 'ready'}\n", encoding="utf-8"
    )
    result = run_tool(
        "mypy",
        "--config-file",
        str(REPOSITORY / "pyproject.toml"),
        str(tmp_path / "podium_forecasting"),
        cwd=tmp_path,
    )
    assert result.returncode == 0, result.stdout
