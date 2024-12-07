"""Classes for systemd manager."""

import subprocess

from cyberfusion.SystemdSupport._constants import SYSTEMCTL_BIN


class SystemdManager:
    """Represents systemd manager."""

    @staticmethod
    def daemon_reload() -> None:
        """Reload manager configuration."""
        subprocess.run([SYSTEMCTL_BIN, "daemon-reload"], check=True)
