"""Enforce dependency direction before pipeline components are introduced."""

import ast
import sys
from collections.abc import Iterable
from pathlib import PurePosixPath

from verification.findings import Finding
from verification.policy import Policy

PACKAGE_LAYER_PARTS = 2
SOURCE_MODULE_PARTS = 3


def imported_modules(tree: ast.AST, module: str) -> Iterable[tuple[str, int]]:
    """Resolve explicit absolute and relative imports to dotted module names."""
    for node in ast.walk(tree):
        yield from imports_at_node(node, module)


def imports_at_node(node: ast.AST, module: str) -> Iterable[tuple[str, int]]:
    """Resolve one import statement without hiding relative layer dependencies."""
    if isinstance(node, ast.Import):
        yield from ((alias.name, node.lineno) for alias in node.names)
    if isinstance(node, ast.ImportFrom):
        prefix = node.module or ""
        if node.level:
            prefix = ".".join([*module.split(".")[: -node.level], prefix]).strip(".")
        yield from ((f"{prefix}.{alias.name}", node.lineno) for alias in node.names)


def violation(target: str, layer: str, policy: Policy) -> str | None:
    """Classify the requested dependency against the canonical layer contract."""
    parts = target.split(".")
    if parts[0] == policy.package:
        if len(parts) < PACKAGE_LAYER_PARTS or parts[1] not in policy.layers[layer]:
            return f"{layer} cannot import {target}; use an allowed layer or a port."
    elif layer in {"domain", "ports", "application"} and parts[0] not in sys.stdlib_module_names:
        return f"{layer} cannot import external dependency {target}; introduce a port."
    return None


def check_architecture(path: str, source: str, policy: Policy) -> Iterable[Finding]:
    """Validate package placement and import direction for production Python."""
    parts = PurePosixPath(path).with_suffix("").parts
    if parts[0] != "src":
        return
    if len(parts) < SOURCE_MODULE_PARTS or parts[:2] != ("src", policy.package):
        yield Finding(path, 1, "ARCH001", "Place production modules inside the canonical package.")
        return
    layer = "domain" if parts[-1] == "__init__" and len(parts) == SOURCE_MODULE_PARTS else parts[2]
    if layer not in policy.layers:
        yield Finding(path, 1, "ARCH001", "Place production modules inside a declared layer.")
        return
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return  # Syntax is reported by the Python parser check.
    module = ".".join(parts[1:])
    for target, line in imported_modules(tree, module):
        message = violation(target, layer, policy)
        if message:
            yield Finding(path, line, "ARCH002", message)
