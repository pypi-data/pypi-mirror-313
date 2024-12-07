# python3-cyberfusion-ferm-support

Library for [ferm](http://ferm.foo-projects.org/).

# Install

## PyPI

Run the following command to install the package from PyPI:

    pip3 install python3-cyberfusion-ferm-support

## Debian

Run the following commands to build a Debian package:

    mk-build-deps -i -t 'apt -o Debug::pkgProblemResolver=yes --no-install-recommends -y'
    dpkg-buildpackage -us -uc

# Configure

No configuration is supported.

# Usage

## Example

```python
from cyberfusion.FermSupport.configuration import Configuration

c = Configuration(path="/etc/ferm/vars.d/example.conf")

c.add_variable(
    name="EXAMPLE",
    values=["2001:0db8::/32"]
)

c.save()
```
