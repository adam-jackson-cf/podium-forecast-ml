"""Actionable design-check findings."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Finding:
    """A rule violation with a source location and remediation context."""

    path: str
    line: int
    rule: str
    message: str

    def render(self) -> str:
        """Render a terminal and editor-friendly diagnostic."""
        return f"{self.path}:{self.line}: {self.rule} {self.message}"
