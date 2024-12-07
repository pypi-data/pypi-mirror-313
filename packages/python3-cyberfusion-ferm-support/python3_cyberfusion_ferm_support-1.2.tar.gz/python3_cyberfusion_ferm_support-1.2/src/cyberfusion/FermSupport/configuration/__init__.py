"""Helpers for ferm configuration."""

import os
import subprocess
from typing import List

from cyberfusion.Common import find_executable
from cyberfusion.FermSupport.configuration.custom_lines import CustomLine
from cyberfusion.FermSupport.configuration.variables import (
    Variable,
    VariableValue,
)
from cyberfusion.FermSupport.exceptions import ConfigInvalidError
from cyberfusion.SystemdSupport.units import Unit


class Configuration:
    """Represents configuration."""

    def __init__(self, *, path: str) -> None:
        """Set attributes."""
        self.path = path

        self.variables: List[Variable] = []
        self.custom_lines: List[CustomLine] = []

    def add_variable(self, *, name: str, values: List[str]) -> None:
        """Add variable."""
        self.variables.append(
            Variable(
                name=name,
                values=[VariableValue(content=value) for value in values],
            )
        )

    def add_custom_line(self, *, contents: str) -> None:
        """Add custom line."""
        self.custom_lines.append(CustomLine(contents=contents))

    def __str__(self) -> str:
        """Get string representation."""
        return (
            "\n".join([str(line) for line in self.variables + self.custom_lines]) + "\n"
        )

    @property
    def is_valid(self) -> bool:
        """Get if config is valid."""
        try:
            subprocess.run([find_executable("ferm"), "--noexec", self.path], check=True)
        except subprocess.CalledProcessError:
            return False

        return True

    def save(self) -> bool:
        """Get file object."""
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                pass

        original_contents = open(self.path, "r").read()

        with open(self.path, "w") as f:
            f.write(str(self))

        changed = original_contents != open(self.path, "r").read()

        if changed:
            if not self.is_valid:
                raise ConfigInvalidError

            Unit(f"ferm.{Unit.SUFFIX_SERVICE}").restart()

        return changed
