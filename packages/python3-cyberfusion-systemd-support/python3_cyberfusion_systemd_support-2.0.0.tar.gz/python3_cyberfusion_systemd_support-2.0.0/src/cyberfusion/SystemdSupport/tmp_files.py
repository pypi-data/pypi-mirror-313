"""Classes for systemd tmp files."""

import os
import subprocess
from typing import Optional

SYSTEMCTL_TMPFILES_BIN = os.path.join(os.path.sep, "bin", "systemd-tmpfiles")


class TmpFileConfigurationFile:
    """Represents tmp file configuration file."""

    def __init__(self, path: str) -> None:
        """Set attributes."""
        self.path = path

    def create(self) -> None:
        """Create tmp files."""
        subprocess.run([SYSTEMCTL_TMPFILES_BIN, "--create", self.path], check=True)


class TmpFileConfigurationLine:
    """Represents tmp file configuration line."""

    TYPE_DIRECTORY_CREATE = "d"

    def __init__(
        self,
        type_: str,
        path: str,
        *,
        mode: str,
        user: str,
        group: str,
        age: Optional[str] = None,
    ) -> None:
        """Set attributes."""
        self.type = type_
        self.path = path
        self.mode = mode
        self.user = user
        self.group = group
        self.age = age

    def __str__(self) -> str:
        """Get line for in configuration."""
        return (
            self.type
            + " "
            + self.path
            + " "
            + self.mode
            + " "
            + self.user
            + " "
            + self.group
            + " "
            + (self.age if self.age else "-")
        )
