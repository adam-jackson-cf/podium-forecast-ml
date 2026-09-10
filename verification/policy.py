"""Load the canonical, version-controlled design policy."""

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import cast


@dataclass(frozen=True)
class Policy:
    """Validated policy inputs shared by the deterministic checks."""

    max_loop_depth: int
    forbidden_names: frozenset[str]
    ignored_directories: frozenset[str]
    allowed_suffixes: frozenset[str]
    allowed_names: frozenset[str]
    package: str
    layers: dict[str, list[str]]
    restricted_effect_layers: frozenset[str]
    forbidden_effect_references: frozenset[str]
    forbidden_effect_calls: frozenset[str]
    locations: dict[str, list[str]]
    max_skill_words: int
    max_role_words: int
    role_fields: list[str]


def load_policy(path: Path) -> Policy:
    """Read the repository-owned policy; invalid configuration fails closed."""
    with path.open("rb") as stream:
        document = tomllib.load(stream)
    python = document["python"]
    files = document["files"]
    architecture = document["architecture"]
    return Policy(
        max_loop_depth=int(python["max_loop_depth"]),
        forbidden_names=frozenset(python["forbidden_names"]),
        ignored_directories=frozenset(files["ignored_directories"]),
        allowed_suffixes=frozenset(files["allowed_suffixes"]),
        allowed_names=frozenset(files["allowed_names"]),
        package=str(architecture["package"]),
        layers=cast("dict[str, list[str]]", architecture["allowed"]),
        restricted_effect_layers=frozenset(architecture["effects"]["restricted_layers"]),
        forbidden_effect_references=frozenset(architecture["effects"]["forbidden_references"]),
        forbidden_effect_calls=frozenset(architecture["effects"]["forbidden_calls"]),
        locations=cast("dict[str, list[str]]", files["locations"]),
        max_skill_words=int(document["guidance"]["max_skill_words"]),
        max_role_words=int(document["guidance"]["max_role_words"]),
        role_fields=list(document["guidance"]["role_fields"]),
    )
