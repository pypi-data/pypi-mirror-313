"""Helpers for ferm variables."""

from typing import List


class Variable:
    """Represents variable."""

    def __init__(self, *, name: str, values: List["VariableValue"]) -> None:
        """Set attributes."""
        self._name = name
        self.values = values

    @property
    def name(self) -> str:
        """Get name."""
        return self._name.upper()

    def __str__(self) -> str:
        """Get string representation."""
        lines = []

        lines.append(f"@def ${self.name} = (")

        for value in self.values:
            lines.append("  " + str(value))

        lines.append(");")

        return "\n".join(lines)


class VariableValue:
    """Represents variable value."""

    def __init__(self, *, content: str) -> None:
        """Set attributes."""
        self.content = content

    def __str__(self) -> str:
        """Get string representation."""
        return self.content
