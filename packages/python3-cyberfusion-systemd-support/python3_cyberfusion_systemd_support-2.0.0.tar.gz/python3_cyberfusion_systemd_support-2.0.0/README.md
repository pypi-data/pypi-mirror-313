# python3-cyberfusion-systemd-support

Library for [systemd](https://systemd.io/).

# Install

## PyPI

Run the following command to install the package from PyPI:

    pip3 install python3-cyberfusion-systemd-support

Next, ensure you are working on a system that ships systemd.

## Debian

Run the following commands to build a Debian package:

    mk-build-deps -i -t 'apt -o Debug::pkgProblemResolver=yes --no-install-recommends -y'
    dpkg-buildpackage -us -uc

# Configure

No configuration is supported.

# Usage

## Units

```python
from cyberfusion.SystemdSupport.units import Unit

unit = Unit(f"example.{Unit.SUFFIX_SERVICE}")

unit.disable()
unit.stop()
unit.enable()
unit.restart()
unit.reload()

print(unit.is_active)
print(unit.is_enabled)
```

## Tmp files

```python
from cyberfusion.SystemdSupport.tmp_files import TmpFileConfigurationLine, TmpFileConfigurationFile

tmp_file_configuration_line = str(TmpFileConfigurationLine(type_="d", path="/tmp/example", mode="0755", user="example", group="example"))
tmp_file_configuration_file = TmpFileConfigurationFile(path="/etc/tmpfiles.d/example.conf")

tmp_file_configuration_file.create()
```
