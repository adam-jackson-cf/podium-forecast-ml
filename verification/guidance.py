"""Check that progressive guidance can be loaded; semantic quality remains review work."""

import re
import tomllib
from collections.abc import Iterable, Iterator
from pathlib import Path, PurePosixPath

import yaml

from verification.findings import Finding
from verification.policy import Policy

GUIDANCE_REFERENCE = re.compile(r"`(agent-guidance/[^`\n]+)`")
SKILL_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
AGENT_NAME = re.compile(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*")
AGENT_FIELDS = {"name", "description", "developer_instructions"}
AGENT_HEADINGS = ("# Task", "## Input", "## Rules", "## Output")
AUTO_DISCOVERY_DIRECTORIES = (
    PurePosixPath(".agents/skills"),
    PurePosixPath(".agents/roles"),
    PurePosixPath(".codex/agents"),
)


def skill_problem(source: str, directory: str, word_limit: int, line_limit: int) -> str | None:
    """Validate skill frontmatter and bounded body without interpreting its instructions."""
    header, delimiter, body = source.partition("\n---\n")
    if not source.startswith("---\n") or not delimiter:
        return "Provide YAML frontmatter delimited by separate --- lines."
    try:
        metadata: object = yaml.safe_load(header.removeprefix("---\n"))
    except yaml.YAMLError:
        return "Correct malformed YAML frontmatter."
    problem: str | None = None
    if not isinstance(metadata, dict) or metadata.get("name") != directory:
        problem = "Set the skill name to its containing directory name."
    elif not _quoted_metadata(header, "name") or not _quoted_metadata(header, "description"):
        problem = "Quote the skill name and description in YAML frontmatter."
    elif not isinstance(metadata.get("description"), str) or not re.fullmatch(
        r"Use when\s+\S[^\n]*", metadata["description"]
    ):
        problem = (
            "Provide a one-line description starting with Use when and an activation condition."
        )
    elif len(source.splitlines()) > line_limit or len(body.split()) > word_limit:
        problem = "Keep the skill within the configured disclosure limits."
    elif (
        not (body_lines := body.lstrip("\n").splitlines())
        or body_lines[0] != "# Guidance"
        or not any(line.strip() for line in body_lines[1:])
    ):
        problem = "Start a nonempty skill body with # Guidance."
    return problem


def _quoted_metadata(header: str, field: str) -> bool:
    """Recognise a quoted, single-line YAML scalar for a required field."""
    return bool(re.search(rf"(?m)^{field}:\s*(?:\"[^\"\n]+\"|'[^'\n]+')\s*$", header))


def check_skill(path: Path, root: Path, policy: Policy) -> Iterable[Finding]:
    """Inspect a skill entrypoint using the canonical disclosure limits."""
    if path.is_symlink():
        yield Finding(
            path.relative_to(root).as_posix(),
            1,
            "GUIDE001",
            "Keep skill entrypoints as repository files, not symlinks.",
        )
        return
    problem = skill_problem(
        path.read_text(encoding="utf-8"),
        path.parent.name,
        policy.max_skill_words,
        policy.max_skill_lines,
    )
    if problem:
        yield Finding(path.relative_to(root).as_posix(), 1, "GUIDE001", problem)


def agent_problem(source: str, filename_stem: str, word_limit: int) -> str | None:
    """Validate the loadable TOML agent envelope and instruction sections."""
    try:
        document = tomllib.loads(source)
    except tomllib.TOMLDecodeError:
        return "Correct malformed agent TOML."
    problem: str | None = None
    if set(document) != AGENT_FIELDS:
        problem = (
            "Provide only the required agent fields: name, description, developer_instructions."
        )
    elif not AGENT_NAME.fullmatch(filename_stem) or document["name"] != filename_stem:
        problem = "Set the snake_case agent name to its filename stem."
    elif (
        not isinstance(document["description"], str)
        or not document["description"].strip()
        or "\n" in document["description"]
    ):
        problem = "Provide a nonempty, one-line agent description."
    elif not isinstance(document["developer_instructions"], str):
        problem = "Provide developer_instructions as text."
    elif len(document["developer_instructions"].split()) > word_limit:
        problem = "Keep the agent instructions within the configured disclosure limit."
    else:
        problem = _instruction_sections_problem(document["developer_instructions"])
    return problem


def _instruction_sections_problem(instructions: str) -> str | None:
    """Validate the order and content of the required instruction sections."""
    lines = instructions.splitlines()
    positions = [index for index, heading in enumerate(lines) if heading in AGENT_HEADINGS]
    actual_headings = [line for line in lines if line.startswith("#")]
    if actual_headings != list(AGENT_HEADINGS) or len(positions) != len(AGENT_HEADINGS):
        return "Use the agent sections # Task, ## Input, ## Rules, and ## Output in order."
    if any(
        not _has_content(lines[start + 1 : stop])
        for start, stop in zip(positions, [*positions[1:], len(lines)], strict=True)
    ):
        return "Provide content in every required agent section."
    return None


def _has_content(lines: list[str]) -> bool:
    """Report whether a required section contains non-whitespace text."""
    return any(line.strip() for line in lines)


def check_agent(path: Path, root: Path, policy: Policy) -> Iterable[Finding]:
    """Inspect an agent definition without judging the meaning of its rules."""
    if path.is_symlink():
        yield Finding(
            path.relative_to(root).as_posix(),
            1,
            "GUIDE002",
            "Keep agent definitions as repository files, not symlinks.",
        )
        return
    problem = agent_problem(path.read_text(encoding="utf-8"), path.stem, policy.max_agent_words)
    if problem:
        yield Finding(path.relative_to(root).as_posix(), 1, "GUIDE002", problem)


def _maintained_instruction_files(root: Path, policy: Policy) -> Iterator[Path]:
    """Find root and scoped instruction files without following ignored or symlinked trees."""
    for directory, child_directories, filenames in root.walk():
        child_directories[:] = _maintained_children(directory, child_directories, policy)
        if "AGENTS.md" in filenames:
            path = directory / "AGENTS.md"
            if not path.is_symlink():
                yield path


def _maintained_children(directory: Path, names: list[str], policy: Policy) -> list[str]:
    """Prune ignored and symlinked children before repository traversal descends."""
    return sorted(
        name
        for name in names
        if name not in policy.ignored_directories and not (directory / name).is_symlink()
    )


def _reference_is_file(root: Path, reference: str) -> bool:
    """Resolve a repository guidance reference lexically and reject every symlink component."""
    relative = PurePosixPath(reference)
    if relative.is_absolute() or ".." in relative.parts or "." in relative.parts:
        return False
    parts = relative.parts
    is_skill = (
        len(parts) == len(("agent-guidance", "skills", "name", "SKILL.md"))
        and parts[:2] == ("agent-guidance", "skills")
        and bool(SKILL_NAME.fullmatch(parts[2]))
        and parts[3] == "SKILL.md"
    )
    is_agent = (
        len(parts) == len(("agent-guidance", "agents", "name.toml"))
        and parts[:2] == ("agent-guidance", "agents")
        and parts[2].endswith(".toml")
        and bool(AGENT_NAME.fullmatch(parts[2].removesuffix(".toml")))
    )
    if not (is_skill or is_agent):
        return False
    if _has_symlink_component(root, relative):
        return False
    target = root.joinpath(*relative.parts)
    return target.is_file()


def _has_symlink_component(root: Path, relative: PurePosixPath) -> bool:
    """Check a lexical repository path without traversing beyond a symlink."""
    target = root
    for part in relative.parts:
        target /= part
        if target.is_symlink():
            return True
    return False


def check_references(root: Path, policy: Policy) -> Iterable[Finding]:
    """Verify conditional guidance references from maintained instruction scopes."""
    for instructions in _maintained_instruction_files(root, policy):
        yield from _check_instruction_references(instructions, root)


def _check_instruction_references(instructions: Path, root: Path) -> Iterable[Finding]:
    """Check the conditional paths declared by one instruction scope."""
    relative = instructions.relative_to(root).as_posix()
    for reference in GUIDANCE_REFERENCE.findall(instructions.read_text(encoding="utf-8")):
        if not _reference_is_file(root, reference):
            yield Finding(
                relative,
                1,
                "GUIDE003",
                f"Repair the missing or unsafe guidance reference {reference}.",
            )


def check_auto_discovery_layout(root: Path) -> Iterable[Finding]:
    """Reject project guidance placed where agent runtimes discover it automatically."""
    for relative in AUTO_DISCOVERY_DIRECTORIES:
        directory = root.joinpath(*relative.parts)
        if _has_symlink_component(root, relative):
            yield Finding(
                relative.as_posix(),
                1,
                "GUIDE004",
                "Keep conditional project guidance outside auto-discovery directories.",
            )
            continue
        if directory.is_dir() and any(directory.iterdir()):
            yield Finding(
                relative.as_posix(),
                1,
                "GUIDE004",
                "Keep conditional project guidance outside auto-discovery directories.",
            )


def check_guidance(root: Path, policy: Policy) -> Iterable[Finding]:
    """Check existing instruction assets without demanding them in isolated code fixtures."""
    skills = root / "agent-guidance" / "skills"
    if not _has_symlink_component(root, PurePosixPath("agent-guidance/skills")):
        for path in sorted(skills.glob("*/SKILL.md")):
            yield from check_skill(path, root, policy)
    agents = root / "agent-guidance" / "agents"
    if not _has_symlink_component(root, PurePosixPath("agent-guidance/agents")):
        for path in sorted(agents.glob("*.toml")):
            yield from check_agent(path, root, policy)
    yield from check_references(root, policy)
    yield from check_auto_discovery_layout(root)
