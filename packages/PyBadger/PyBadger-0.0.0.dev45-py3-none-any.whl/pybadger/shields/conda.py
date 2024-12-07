import pylinks as _pylinks

from pybadger import shields as _shields


class CondaBadger(_shields.Badger):
    """Shields.io badge generator for Conda."""

    def __init__(
        self,
        package: str,
        channel: str = "conda-forge",
        validate_urls: bool = False,
    ):
        """Create a Conda badger.

        Parameters
        ----------
        package : str
            Package name.
        channel : str, default: 'conda-forge'
            Channel name.
        """
        super().__init__(base_path="conda")
        self._params = {
            "logo": "condaforge" if channel == "conda-forge" else "anaconda",
            "logo_color": "#000000" if channel == "conda-forge" else "#44A833",
        }
        self._link = _pylinks.site.conda.package(name=package, channel=channel, validate=validate_urls)
        self._endpoint_key = f"{channel}/{package}"
        return

    def downloads(self) -> _shields.Badge:
        """Create a badge for number of total downloads.

        References
        ----------
        [Shields.io API - Conda Downloads](https://shields.io/badges/conda-downloads)
        """
        return self.create(
            path=f"d/{self._endpoint_key}",
            params={"label": "Conda Downloads"} | self._params,
            attrs_a={"href": self._link.homepage},
            attrs_img={
                "alt": "Conda Downloads",
                "title": "Number of downloads for the Conda distribution. Click to see more details.",
            },
        )

    def license(self) -> _shields.Badge:
        """Create a badge for package license.

        References
        ----------
        [Shields.io API - Conda License](https://shields.io/badges/conda-license)
        """
        return self.create(
            path=f"l/{self._endpoint_key}",
            params={"label": "Conda Package License"} | self._params,
            attrs_a={"href": self._link.homepage},
            attrs_img={
                "alt": "License",
                "title": "License of the Conda distribution. Click to see more details.",
            },
        )

    def platform(self) -> _shields.Badge:
        """Create a badge for supported platforms.

        References
        ----------
        [Shields.io API - Conda Platform](https://shields.io/badges/conda-platform)
        """
        return self.create(
            path=f"p/{self._endpoint_key}",
            params={"label": "Supported Platforms"} | self._params,
            attrs_a={"href": self._link.homepage},
            attrs_img={
                "alt": "Supported Platforms",
                "title": "Supported platforms for the Conda distribution. Click to see more details.",
            },
        )

    def version(self) -> _shields.Badge:
        """Create a badge for package version.

        References
        ----------
        [Shields.io API - Conda Version](https://shields.io/badges/conda-version)
        """
        return self.create(
            path=f"v/{self._endpoint_key}",
            params={"label": "Version"} | self._params,
            attrs_a={"href": self._link.homepage},
            attrs_img={
                "alt": "Conda Package Version",
                "title": "Package version of the Conda distribution. Click to see more details.",
            },
        )
