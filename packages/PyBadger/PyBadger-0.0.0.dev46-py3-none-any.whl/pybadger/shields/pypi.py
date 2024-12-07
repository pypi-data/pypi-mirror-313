from typing import Literal as _Literal
import pylinks as _pylinks

from pybadger import shields as _shields


class PyPIBadger(_shields.Badger):
    """Shields.io badge generator for PyPI."""

    def __init__(
        self,
        package: str,
        pypi_base_url: str = "https://pypi.org",
        validate_urls: bool = False,
    ):
        """Create a PyPI badger.

        Parameters
        ----------
        package : str
            Name of the package.
        pypi_base_url : str, default: 'https://pypi.org'
            Base URL of the PyPI website.
        """
        super().__init__(base_path="pypi")
        self._package = package
        self._pypi_base_url = pypi_base_url
        self._link = _pylinks.site.pypi.package(name=package, validate=validate_urls)
        return

    def downloads(self, period: _Literal["m", "w", "d"] = "m") -> _shields.Badge:
        """Number of downloads.

        Parameters
        ----------
        period : {'m', 'w', 'd'}, default: 'm'
            Period to display the number of downloads.
            - 'm': Monthly
            - 'w': Weekly
            - 'd': Daily

        References
        ----------
        [Shields.io API - PyPI Downloads](https://shields.io/badges/py-pi-downloads)
        [Shields.io API - Pepy Total Downloads](https://shields.io/badges/pepy-total-downlods)
        """
        period_name = {"d": "day", "w": "week", "m": "month"}
        return self.create(
            path=f"d{period}/{self._package}",
            params={"label": "Downloads", "logo": "pypi"},
            attrs_img={
                "alt": "PyPI Downloads",
                "title": (
                    f"Number of downloads of all releases from PyPI, per {period_name[period]}. "
                    f"Click to see more details on PyPI."
                ),
            },
            attrs_a={"href": f"https://pepy.tech/projects/{self._package}"},
        )

    def license(self) -> _shields.Badge:
        """Package license.

        References
        ----------
        [Shields.io API - PyPI License](https://shields.io/badges/py-pi-license)
        """
        return self.create(
            path=f"l/{self._package}",
            queries={"pypiBaseUrl": self._pypi_base_url},
            params={"label": "License"},
            attrs_img={
                "alt": "License",
                "title": "License of the package."
            },
            attrs_a={"href": self._link.homepage},
        )

    def distribution_format(self) -> _shields.Badge:
        """Format of the distribution package.

        References
        ----------
        [Shields.io API - PyPI Format](https://shields.io/badges/py-pi-format)
        """
        return self.create(
            path=f"format/{self._package}",
            queries={"pypiBaseUrl": self._pypi_base_url},
            params={"label": "Distribution Format"},
            attrs_img={
                "alt": "Distribution Format",
                "title": "Format of the distribution package."
            },
            attrs_a={"href": self._link.homepage},
        )

    def development_status(self) -> _shields.Badge:
        """Development status.

        References
        ----------
        [Shields.io API - PyPI Status](https://shields.io/badges/py-pi-status)
        """
        return self.create(
            path=f"status/{self._package}",
            queries={"pypiBaseUrl": self._pypi_base_url},
            params={"label": "Development Status"},
            attrs_img={
                "alt": "Development Status",
                "title": "Development phase of the package."
            },
            attrs_a={"href": self._link.homepage},
        )

    def implementation(self) -> _shields.Badge:
        """Python implementation used to build the package.

        References
        ----------
        - [Shields.io API - PyPI Implementation](https://shields.io/badges/py-pi-implementation)
        """
        return self.create(
            path=f"implementation/{self._package}",
            queries={"pypiBaseUrl": self._pypi_base_url},
            params={"label": "Python Implementation"},
            attrs_img={
                "alt": "Python Implementation",
                "title": "Python implementation used to build the package."
            },
            attrs_a={"href": self._link.homepage},
        )

    def python_versions(self) -> _shields.Badge:
        """Supported Python versions read from trove classifiers.

        References
        ----------
        - [Shields.io API - Python Version](https://shields.io/badges/py-pi-python-version)
        """
        return self.create(
            path=f"pyversions/{self._package}",
            queries={"pypiBaseUrl": self._pypi_base_url},
            params={"label": "Supports Python"},
            attrs_img={
                "alt": "Supported Python Versions",
                "title": "Supported Python versions of the latest package release."
            },
            attrs_a={"href": self._link.homepage},
        )

    def version(self) -> _shields.Badge:
        """Package version.

        References
        ----------
        - [Shields.io API - PyPI Version](https://shields.io/badges/py-pi-version)
        """
        return self.create(
            path=f"v/{self._package}",
            params={"label": "Latest Version"},
            attrs_img={"alt": "Latest Version", "title": "Latest release version of the package."},
            attrs_a={"href": self._link.homepage},
        )
