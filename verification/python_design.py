"""AST design checks beyond standard Ruff and mypy rules."""

import ast
from collections.abc import Iterable

from verification.findings import Finding
from verification.policy import Policy

LOOPS = (ast.For, ast.AsyncFor, ast.While)
COMPREHENSIONS = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)


class DesignVisitor(ast.NodeVisitor):
    """Reject excessive iteration nesting."""

    def __init__(self, path: str, policy: Policy) -> None:
        self.path = path
        self.policy = policy
        self.depth = 0
        self.findings: list[Finding] = []

    def visit(self, node: ast.AST) -> None:
        """Keep loop depth lexical, including comprehension generators."""
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

    def loop_increment(self, node: ast.AST) -> int:
        """Count iteration constructs, including multiple comprehension clauses."""
        if isinstance(node, LOOPS):
            return 1
        if isinstance(node, COMPREHENSIONS):
            return len(node.generators)
        return 0


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
