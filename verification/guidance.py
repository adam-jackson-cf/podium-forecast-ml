"""Check that progressive guidance can be loaded; semantic quality remains review work."""

import re
from collections.abc import Iterable
from pathlib import Path

import yaml

from verification.findings import Finding
from verification.policy import Policy

GUIDANCE_REFERENCE = re.compile(r"\.agents/(?:skills|roles)/[A-Za-z0-9_./-]+")


def skill_problem(source: str, directory: str, word_limit: int) -> str | None:
    """Validate skill frontmatter and bounded body without interpreting its instructions."""
    header, delimiter, body = source.partition("\n---\n")
    if not source.startswith("---\n") or not delimiter:
        return "Provide YAML frontmatter delimited by separate --- lines."
    try:
        metadata: object = yaml.safe_load(header.removeprefix("---\n"))
    except yaml.YAMLError:
        return "Correct malformed YAML frontmatter."
    if not isinstance(metadata, dict) or metadata.get("name") != directory:
        return "Set the skill name to its containing directory name."
    description = metadata.get("description")
    if not isinstance(description, str) or not re.match(r"(?i)^use when\s+\S.+", description):
        return "Provide a description starting with Use when and a specific activation condition."
    if not body.strip() or len(body.split()) > word_limit:
        return "Provide a nonempty skill body within the configured disclosure limit."
    return None


def check_skill(path: Path, root: Path, policy: Policy) -> Iterable[Finding]:
    """Inspect a skill entrypoint using the canonical disclosure limits."""
    if path.is_symlink():
        return  # Repository file traversal reports symlinks without reading their targets.
    problem = skill_problem(
        path.read_text(encoding="utf-8"), path.parent.name, policy.max_skill_words
    )
    if problem:
        yield Finding(path.relative_to(root).as_posix(), 1, "GUIDE001", problem)


def role_problem(source: str, policy: Policy) -> str | None:
    """Require the role contract fields already used by the repository briefs."""
    if not source.strip() or len(source.split()) > policy.max_role_words:
        return "Provide a nonempty role brief within the configured disclosure limit."
    missing = [field for field in policy.role_fields if not re.search(rf"(?m)^{field}: \S", source)]
    if missing:
        return f"Provide role contract fields: {', '.join(missing)}."
    return None


def check_role(path: Path, root: Path, policy: Policy) -> Iterable[Finding]:
    """Verify required authority, evidence and stop boundaries can be loaded."""
    if path.is_symlink():
        return
    problem = role_problem(path.read_text(encoding="utf-8"), policy)
    if problem:
        yield Finding(path.relative_to(root).as_posix(), 1, "GUIDE002", problem)


def check_references(root: Path) -> Iterable[Finding]:
    """Verify root dispatch paths stay within the repository guidance tree."""
    instructions = root / "AGENTS.md"
    if not instructions.is_file() or instructions.is_symlink():
        return
    for reference in GUIDANCE_REFERENCE.findall(instructions.read_text(encoding="utf-8")):
        target = (root / reference).resolve()
        if not target.is_relative_to((root / ".agents").resolve()) or not target.is_file():
            yield Finding(
                "AGENTS.md", 1, "GUIDE003", f"Repair the missing guidance reference {reference}."
            )


def check_guidance(root: Path, policy: Policy) -> Iterable[Finding]:
    """Check existing instruction assets without demanding them in isolated code fixtures."""
    for path in sorted((root / ".agents" / "skills").glob("*/SKILL.md")):
        yield from check_skill(path, root, policy)
    for path in sorted((root / ".agents" / "roles").glob("*.md")):
        yield from check_role(path, root, policy)
    yield from check_references(root)
