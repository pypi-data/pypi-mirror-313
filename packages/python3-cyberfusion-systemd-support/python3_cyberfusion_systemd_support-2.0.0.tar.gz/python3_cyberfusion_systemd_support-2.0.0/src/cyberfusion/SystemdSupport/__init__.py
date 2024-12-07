"""Classes for systemd."""

import subprocess
from typing import List

from cyberfusion.SystemdSupport._constants import SYSTEMCTL_BIN
from cyberfusion.SystemdSupport.units import Unit


class Systemd:
    """Represents systemd."""

    def __init__(self) -> None:
        """Do nothing."""
        pass

    def search_units(self, string: str) -> List[Unit]:
        """Search units."""
        output = []

        units = subprocess.run(
            [
                SYSTEMCTL_BIN,
                "list-units",
                "--plain",
                "--type",
                "service",
                "--all",
                string,
                "--no-pager",
                "--no-legend",
            ],
            check=True,
            stdout=subprocess.PIPE,
            text=True,
        ).stdout.splitlines()

        for unit in units:
            name = unit.split()[0]

            output.append(Unit(name))

        return output
