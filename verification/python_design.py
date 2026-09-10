"""AST design checks beyond standard Ruff and mypy rules."""

import ast
import re
from collections.abc import Iterable

from verification.findings import Finding
from verification.policy import Policy

LOOPS = (ast.For, ast.AsyncFor, ast.While)
COMPREHENSIONS = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
DEFINITIONS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


class DesignVisitor(ast.NodeVisitor):
    """Reject excessive iteration nesting and generic declaration names."""

    def __init__(self, path: str, policy: Policy) -> None:
        self.path = path
        self.policy = policy
        self.depth = 0
        self.findings: list[Finding] = []

    def visit(self, node: ast.AST) -> None:
        """Keep loop depth lexical, including comprehension generators."""
        if isinstance(node, DEFINITIONS):
            self.check_name(node)
        self.check_binding(node)
        previous_depth = self.depth
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            self.depth = 0
        increment = self.loop_increment(node)
        self.depth += increment
        if isinstance(node, (*LOOPS, *COMPREHENSIONS)) and self.depth > self.policy.max_loop_depth:
            self.findings.append(
                Finding(
                    self.path, node.lineno, "PY001", "Extract nested iteration into a named step."
                )
            )
        self.generic_visit(node)
        self.depth = previous_depth

    def check_binding(self, node: ast.AST) -> None:
        """Require owned variables and parameters to name their content."""
        if (
            isinstance(node, (ast.Name, ast.arg))
            and binding_name(node) in self.policy.forbidden_names
        ):
            self.findings.append(
                Finding(self.path, node.lineno, "PY002", "Name the specific domain responsibility.")
            )

    def loop_increment(self, node: ast.AST) -> int:
        """Count iteration constructs, including multiple comprehension clauses."""
        if isinstance(node, LOOPS):
            return 1
        if isinstance(node, COMPREHENSIONS):
            return len(node.generators)
        return 0

    def check_name(self, node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> None:
        """Require declarations to identify a responsibility rather than a generic bucket."""
        words = re.sub(r"([a-z])([A-Z])", r"\1_\2", node.name).lower().strip("_").split("_")
        if words[-1] in self.policy.forbidden_names:
            self.findings.append(
                Finding(self.path, node.lineno, "PY002", "Name the specific domain responsibility.")
            )


def check_python(path: str, source: str, policy: Policy) -> Iterable[Finding]:
    """Parse real syntax and return deterministic design findings."""
    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError as error:
        yield Finding(path, error.lineno or 1, "PY000", str(error.msg))
        return
    visitor = DesignVisitor(path, policy)
    visitor.visit(tree)
    yield from visitor.findings


def binding_name(node: ast.AST) -> str:
    """Identify names owned by this module, excluding imported API attributes."""
    if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
        return node.id
    if isinstance(node, ast.arg):
        return node.arg
    return ""
