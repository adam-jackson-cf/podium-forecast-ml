"""Fail closed when new files escape the declared verification surface."""

import io
import re
import tokenize
from collections.abc import Iterable
from pathlib import Path

from verification.architecture import check_architecture
from verification.findings import Finding
from verification.guidance import check_guidance
from verification.locations import check_location
from verification.policy import Policy
from verification.python_design import check_python
from verification.test_execution import check_test_bypass

SUPPRESSION = re.compile(
    r"noqa|type:\s*ignore|mypy:\s*ignore|ruff:\s*noqa|pragma:\s*no\s*cover|"
    r"nosec|checkov:\s*skip|tfsec:ignore|shellcheck\s+disable|hadolint\s+ignore|"
    r"sqlfluff:\s*(?:disable|ignore)",
    re.IGNORECASE,
)


def check_comments(path: str, source: str) -> Iterable[Finding]:
    """Reject suppression comments; quoted examples remain legitimate test input."""
    try:
        comments = tokenize.generate_tokens(io.StringIO(source).readline)
        for token in comments:
            if token.type == tokenize.COMMENT and SUPPRESSION.search(token.string):
                yield Finding(
                    path, token.start[0], "GATE001", "Resolve the finding; do not suppress it."
                )
    except (tokenize.TokenError, IndentationError):
        return  # Syntax is reported by the Python parser check.


def check_file(path: Path, root: Path, policy: Policy) -> Iterable[Finding]:
    """Apply the registered checks to one maintained repository file."""
    relative = path.relative_to(root).as_posix()
    if path.is_symlink():
        yield Finding(relative, 1, "FILE002", "Keep maintained sources inside the repository.")
        return
    if path.suffix not in policy.allowed_suffixes and path.name not in policy.allowed_names:
        yield Finding(relative, 1, "FILE001", "Register this file type and its verification first.")
        return
    yield from check_location(relative, policy)
    if path.suffix != ".py":
        yield from check_configuration_comments(path, relative)
        return
    if path.stem in policy.forbidden_names:
        yield Finding(relative, 1, "PY002", "Name the module for its specific responsibility.")
    source = path.read_text(encoding="utf-8")
    yield from check_comments(relative, source)
    yield from check_python(relative, source, policy)
    yield from check_architecture(relative, source, policy)
    yield from check_test_bypass(relative, source)


def check_repository(root: Path, policy: Policy) -> list[Finding]:
    """Walk maintained files without inspecting generated environments or caches."""
    findings: list[Finding] = []
    for directory, child_directories, filenames in root.walk():
        child_directories[:] = sorted(set(child_directories) - policy.ignored_directories)
        findings.extend(check_directory(directory, filenames, root, policy))
    findings.extend(check_guidance(root, policy))
    return findings


def check_directory(
    directory: Path, filenames: list[str], root: Path, policy: Policy
) -> Iterable[Finding]:
    """Apply per-file verification within a maintained directory."""
    for filename in sorted(filenames):
        yield from check_file(directory / filename, root, policy)


def check_configuration_comments(path: Path, relative: str) -> Iterable[Finding]:
    """Do not allow language-specific suppression comments in infrastructure."""
    checked_suffixes = {
        ".sh",
        ".sql",
        ".tf",
        ".tfvars",
        ".hcl",
        ".yaml",
        ".yml",
        ".toml",
        ".Dockerfile",
    }
    if path.suffix not in checked_suffixes and path.name != "Dockerfile":
        return
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if SUPPRESSION.search(line):
            yield Finding(
                relative, line_number, "GATE001", "Resolve the finding; do not suppress it."
            )
