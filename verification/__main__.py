"""Command-line entrypoint for repository design verification."""

import sys
from pathlib import Path

from verification.policy import load_policy
from verification.repository import check_repository


def main() -> int:
    """Return a failing status for any design-policy violation."""
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    policy = load_policy(root / "quality-policy.toml")
    findings = check_repository(root, policy)
    for finding in findings:
        sys.stderr.write(f"{finding.render()}\n")
    if findings:
        return 1
    sys.stdout.write("Design policy: all maintained files passed.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
