"""Exercise the actual policy command against isolated repositories."""

import shutil
import subprocess
import sys
from pathlib import Path


def test_cli_distinguishes_clean_and_invalid_repositories(tmp_path: Path) -> None:
    repository = Path(__file__).resolve().parents[2]
    shutil.copyfile(repository / "quality-policy.toml", tmp_path / "quality-policy.toml")
    source = tmp_path / "scores.py"
    source.write_text("probability = 0.5\n", encoding="utf-8")
    command = [sys.executable, "-m", "verification", str(tmp_path)]
    clean = subprocess.run(command, cwd=repository, capture_output=True, text=True, check=False)
    assert clean.returncode == 0, clean.stderr
    source.write_text(
        "for race in races:\n    for runner in race:\n        score(runner)\n", encoding="utf-8"
    )
    invalid = subprocess.run(command, cwd=repository, capture_output=True, text=True, check=False)
    assert invalid.returncode != 0
    assert "PY001" in invalid.stderr
    assert "scores.py:" in invalid.stderr
