"""Dynamically create badges using the [PePy](https://www.pepy.tech/) API.

References
----------
- [PePy Website](https://pepy.tech/)
- [PePy Repository](https://github.com/psincraian/pepy)
"""

from pybadger.pepy.badge import Badge
from pybadger.pepy.badger import Badger
from pybadger.pepy.pypi import PyPIBadger


def pypi(package: str, use_defaults: bool = True) -> PyPIBadger:
    """PyPI badge generator."""
    return PyPIBadger(package=package, use_defaults=use_defaults)
