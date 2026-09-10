"""Detect test bypass calls and decorators, including ordinary import aliases."""

import ast
from collections.abc import Iterable

from verification.findings import Finding

BYPASS_CALLS = frozenset(
    {
        "pytest.skip",
        "pytest.xfail",
        "pytest.importorskip",
        "pytest.mark.skip",
        "pytest.mark.skipif",
        "pytest.mark.xfail",
        "unittest.skip",
        "unittest.skipIf",
        "unittest.skipUnless",
        "unittest.expectedFailure",
    }
)


def import_aliases(tree: ast.AST) -> dict[str, str]:
    """Resolve static import aliases without evaluating application code."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        aliases.update(aliases_at_node(node))
    return aliases


def aliases_at_node(node: ast.AST) -> dict[str, str]:
    """Read aliases from one absolute import statement."""
    if isinstance(node, ast.Import):
        return {alias.asname or alias.name: alias.name for alias in node.names}
    if isinstance(node, ast.ImportFrom):
        return {alias.asname or alias.name: f"{node.module}.{alias.name}" for alias in node.names}
    return {}


def qualified_name(node: ast.AST, aliases: dict[str, str]) -> str:
    """Resolve a call or decorator target through its attribute chain."""
    if isinstance(node, ast.Name):
        return aliases.get(node.id, node.id)
    if isinstance(node, ast.Attribute):
        return f"{qualified_name(node.value, aliases)}.{node.attr}"
    return ""


def check_test_bypass(path: str, source: str) -> Iterable[Finding]:
    """Reject execution bypasses while allowing quoted negative-test examples."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return
    aliases = import_aliases(tree)
    for node in ast.walk(tree):
        name = qualified_name(node, aliases)
        if isinstance(node, (ast.Name, ast.Attribute)) and (
            name in BYPASS_CALLS or name.endswith(".skipTest")
        ):
            yield Finding(
                path, node.lineno, "GATE002", "Tests must execute or fail, never skip or xfail."
            )
