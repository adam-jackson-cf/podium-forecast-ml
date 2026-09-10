"""Ensure executable files cannot escape the locations covered by stack gates."""

from collections.abc import Iterable
from fnmatch import fnmatchcase
from pathlib import PurePosixPath

from verification.findings import Finding
from verification.policy import Policy


def matches_location(path: PurePosixPath, location: str) -> bool:
    """Match an exact file, direct directory, or filename pattern in one directory."""
    pattern = PurePosixPath(location)
    if "*" in pattern.name:
        return path.parent == pattern.parent and fnmatchcase(path.name, pattern.name)
    return path.as_posix() == location or path.parent.as_posix() == location


def check_location(relative: str, policy: Policy) -> Iterable[Finding]:
    """Require gate expansion before onboarding another executable directory."""
    path = PurePosixPath(relative)
    locations = policy.locations.get(path.name, policy.locations.get(path.suffix))
    if locations is not None and not any(
        matches_location(path, location) for location in locations
    ):
        yield Finding(
            relative, 1, "FILE003", "Expand the stack gate before adding this file location."
        )
