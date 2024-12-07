"""Helpers for ferm custom lines."""


class CustomLine:
    """Represents custom line."""

    def __init__(self, *, contents: str) -> None:
        """Set attributes."""
        self.contents = contents

    def __str__(self) -> str:
        """Get string representation."""
        return self.contents
