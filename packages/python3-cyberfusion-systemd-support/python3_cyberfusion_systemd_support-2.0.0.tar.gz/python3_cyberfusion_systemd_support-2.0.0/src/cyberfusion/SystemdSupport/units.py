"""Classes for systemd units."""

import glob
import os
import subprocess
from functools import wraps
from typing import Callable, Optional, TypeVar, cast

from cyberfusion.SystemdSupport._constants import SYSTEMCTL_BIN
from cyberfusion.SystemdSupport.manager import SystemdManager

F = TypeVar("F", bound=Callable[..., None])


BASE_DIRECTORY_SYSTEMD_UNITS = os.path.join(os.path.sep, "etc", "systemd", "system")


def reload_manager(f: F) -> F:
    """Reload manager configuration if needed.."""

    @wraps(f)
    def wrapper(
        self: "Unit",
        *args: tuple,
        **kwargs: dict,
    ) -> None:
        if self.needs_reload:
            SystemdManager.daemon_reload()

        f(self, *args, **kwargs)

    return cast(F, wrapper)


class Unit:
    """Represents unit."""

    SUFFIX_SERVICE = "service"

    def __init__(self, name: str) -> None:
        """Set attributes."""
        self.name = name

    def get_property(self, name: str) -> Optional[str]:
        """Get unit property from systemd."""
        output = subprocess.run(
            [SYSTEMCTL_BIN, "-P", name, "show", self.name],
            check=True,
            stdout=subprocess.PIPE,
            text=True,
        ).stdout.rstrip()

        if output == "":
            return None

        return output

    @property
    def drop_in_directory(self) -> str:
        """Get path to drop-in directory."""
        return self.get_drop_in_directory(self.name)

    @property
    def needs_reload(self) -> bool:
        """Get if manager needs to be reloaded for unit."""

        # systemd itself decides that daemon-reload is needed

        if self.get_property("NeedDaemonReload") == "yes":
            return True

        # Drop-in directory was added after the latest daemon-reload (systemd
        # does not detect it itself in that case, see: https://github.com/systemd/systemd/issues/31752)

        if (
            os.path.isdir(self.drop_in_directory)
            and glob.glob(os.path.join(self.drop_in_directory, "*.conf"))
            and self.get_property("DropInPaths") is None
        ):
            return True

        return False

    def disable(self) -> None:
        """Disable unit."""
        if not self.is_enabled:
            return

        subprocess.run([SYSTEMCTL_BIN, "disable", self.name], check=True)

    def enable(self) -> None:
        """Enable unit."""
        if self.is_enabled:
            return

        subprocess.run([SYSTEMCTL_BIN, "enable", self.name], check=True)

    @reload_manager
    def stop(self) -> None:
        """Stop unit."""
        if not self.is_active:
            return

        subprocess.run([SYSTEMCTL_BIN, "stop", self.name], check=True)

    @reload_manager
    def restart(self) -> None:
        """Restart unit."""
        subprocess.run([SYSTEMCTL_BIN, "restart", self.name], check=True)

    @reload_manager
    def reload(self) -> None:
        """Reload unit."""
        subprocess.run([SYSTEMCTL_BIN, "reload", self.name], check=True)

    @property
    def is_active(self) -> bool:
        """Get if unit is active."""
        try:
            subprocess.run(
                [SYSTEMCTL_BIN, "is-active", "--quiet", self.name], check=True
            )
        except subprocess.CalledProcessError:
            return False

        return True

    @property
    def is_enabled(self) -> bool:
        """Get if unit is enabled."""
        try:
            subprocess.run(
                [SYSTEMCTL_BIN, "is-enabled", "--quiet", self.name], check=True
            )
        except subprocess.CalledProcessError:
            return False

        return True

    @staticmethod
    def get_drop_in_directory(unit_name: str) -> str:
        """Get unit override directory."""
        return os.path.join(BASE_DIRECTORY_SYSTEMD_UNITS, unit_name + ".d")
