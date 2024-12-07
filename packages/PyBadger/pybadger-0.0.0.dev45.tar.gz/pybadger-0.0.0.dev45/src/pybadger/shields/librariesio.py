from typing import Literal as _Literal
import pylinks as _pylinks

from pybadger import shields as _shields


class LibrariesIOBadger(_shields.Badger):
    """Shields.io badge generator for Libraries.io.

    References
    ----------
    - [Libraries.io](https://libraries.io/)
    """

    def __init__(
        self,
        platform: str | None = None,
        package: str | None = None,
        scope: str | None = None,
        validate_urls: bool = False,
    ):
        """Create a Libraries.io badger.

        Parameters
        ----------
        platform : str, default: 'pypi'
            Name of the platform where the package is distributed, e.g. 'pypi', 'npm', etc.
        package : str
            Name of the package.
        scope : str, optional
            The scope of the npm package, e.g., `@babel`.
        """
        super().__init__(base_path="librariesio")
        if platform and package:
            self._link = _pylinks.site.lib_io.package(platform=platform, package=package, validate=validate_urls)
            self._endpoint_key = f"{platform}/{scope}/{package}" if scope else f"{platform}/{package}"
        self._logo = {"logo": "librariesdotio", "logo_color": "#337AB7"}
        return

    def dependency_status(self, version: str | None = None) -> _shields.Badge:
        """Dependency status.

        Paramaters
        ----------
        version : str, optional
            A specific version to query.

        Notes
        -----
        - The right-hand text shows either 'up to date', or '{number} out of date'.

        References
        ----------
        - [Shields.io API - Libraries.io dependency status for latest release](https://shields.io/badges/libraries-io-dependency-status-for-latest-release)
        - [Shields.io API - Libraries.io dependency status for specific release](https://shields.io/badges/libraries-io-dependency-status-for-specific-release)
        """
        return self.create(
            path=f"release/{self._endpoint_key}{f"/{version}" if version else ""}",
            params={"label": "Dependencies"} | self._logo,
            attrs_img={
                "alt": "Dependency Status",
                "title": "Status of the project's dependencies.",
            },
            attrs_a={"href": self._link.dependencies(version=version) if version else self._link.homepage},
        )

    def dependency_status_github(self, user: str, repo: str) -> _shields.Badge:
        """Dependency status for the package, according to Libraries.io.

        References
        ----------
        - [Shields.io API - Libraries.io dependency status for GitHub repo](https://shields.io/badges/libraries-io-dependency-status-for-git-hub-repo)
        """
        return self.create(
            path=f"github/{user}/{repo}",
            params={"label": "Dependencies"} | self._logo,
            attrs_img={
                "alt": "Dependency Status",
                "title": "Status of the project's dependencies.",
            },
        )

    def dependents(self, repo: bool = False) -> _shields.Badge:
        """
        Number of packages or repositories that depend on this package.

        Parameters
        ----------
        repo : bool, default: False
            Whether to query repositories (True) or packages (False).

        References
        ----------
        - [Shields.io API - Dependent repos (via Libraries.io)](https://shields.io/badges/dependent-repos-via-libraries-io)
        - [Shields.io API - Dependent repos (via Libraries.io), scoped npm package](https://shields.io/badges/dependent-repos-via-libraries-io-scoped-npm-package)
        - [Shields.io API - Dependents (via Libraries.io)](https://shields.io/badges/dependents-via-libraries-io)
        - [Shields.io API - Dependents (via Libraries.io), scoped npm package](https://shields.io/badges/dependents-via-libraries-io-scoped-npm-package)
        """
        return self.create(
            path=f"{"dependent-repos" if repo else "dependents"}/{self._endpoint_key}",
            params={"label": "Dependents"} | self._logo,
            attrs_img={
                "alt": "Dependents",
                "title": f"Number of {'repositories' if repo else 'packages'} that depend on us.",
            },
            attrs_a={"href": self._link.homepage},
        )

    def source_rank(self) -> _shields.Badge:
        """SourceRank ranking of the package.

        References
        ----------
        - [Shields.io API - Libraries.io SourceRank](https://shields.io/badges/libraries-io-source-rank)
        """
        return self.create(
            path=f"sourcerank/{self._endpoint_key}",
            params={"label": "SourceRank"} | self._logo,
            attrs_img={
                "alt": "SourceRank",
                "title": (
                    "Ranking of the source code according to libraries.io SourceRank algorithm. "
                    "Click to see more details on libraries.io website."
                ),
            },
            attrs_a={"href": self._link.source_rank},
        )
