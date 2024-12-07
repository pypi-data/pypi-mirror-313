"""Dynamically create badges using the shields.io API.

References
----------
* https://shields.io/
* https://github.com/badges/shields
"""

from typing import Literal as _Literal

from pybadger.protocol import AttrDict as _AttrDict, Stringable as _Stringable
from pybadger.shields.badge import Badge
from pybadger.shields.badger import Badger
from pybadger.shields.binder import BinderBadger
from pybadger.shields.codecov import CodeCovBadger
from pybadger.shields.conda import CondaBadger
from pybadger.shields.discord import DiscordBadger
from pybadger.shields.github import GitHubBadger
from pybadger.shields.librariesio import LibrariesIOBadger
from pybadger.shields.pepy import PePyBadger
from pybadger.shields.pypi import PyPIBadger
from pybadger.shields.readthedocs import ReadTheDocsBadger
from pybadger.shields.repodynamics import RepoDynamicsBadger


def generic(
    path: _Stringable,
    queries: _AttrDict = None,
) -> Badge:
    return Badger().create(
        path=path,
        queries=queries,
    )


def static(message: str) -> Badge:
    """Create a static badge with custom text.

    Parameters
    ----------
    message : str
        The text on the (right side of the) badge.
        When `ShieldsSettings.label` is not set in `shields_settings`,
        the badge will only have one side.
    """
    return Badger().create(
        path="static/v1",
        queries={"message": message},
        params={"label": ""},
        attrs_img={"alt": message},
    )


def dynamic(
    url: str,
    query: str,
    prefix: str | None = None,
    suffix: str | None = None,
    typ: _Literal["json", "toml", "xml", "yaml"] | None = None,
) -> Badge:
    """Create a dynamic badge with custom text extracted from a data file.

    Parameters
    ----------
    typ : {'json', 'toml', 'xml', 'yaml'}
        Type of the file.
    url : str
        URL of the file, e.g., `https://raw.githubusercontent.com/repodynamics/pybadger/main/pyproject.toml`
    query : str
        A [JSONPath](https://jsonpath.com/) expression (for JSON, TOML, and YAML files)
        or an [XPath](https://devhints.io/xpath) selector (for XML files)
        to query the file, e.g., `$.name`, `//slideshow/slide[1]/title`.
    prefix : str, optional
        Prefix to append to the extracted value.
    suffix : str, optional
        Suffix to append to the extracted value.

    Notes
    -----
    - For XML documents that use a default namespace prefix,
    the local-name function must be used to construct the query.
    For example, `/*[local-name()='myelement']` rather than `/myelement`.
    - Useful resource for XPath selectors: [XPather](http://xpather.com/)

    References
    ----------
    - [Shields.io API - Dynamic JSON Badge](https://shields.io/badges/dynamic-json-badge)
    - [Shields.io API - Dynamic TOML Badge](https://shields.io/badges/dynamic-toml-badge)
    - [Shields.io API - Dynamic XML Badge](https://shields.io/badges/dynamic-xml-badge)
    - [Shields.io API - Dynamic YAML Badge](https://shields.io/badges/dynamic-yaml-badge)
    """
    if not typ:
        typ = url.split(".")[-1]
        if typ == "yml":
            typ = "yaml"
        if typ not in ["json", "toml", "xml", "yaml"]:
            raise ValueError("Could not determine the file type. Please specify the 'typ' parameter.")
    return Badger().create(
        path=f"badge/dynamic/{typ}",
        queries={
            "url": url,
            "query": query,
            "prefix": prefix,
            "suffix": suffix,
        },
        params={"label": ""},
    )


def endpoint(url: str) -> Badge:
    """Create a dynamic badge with custom text retrieved from a JSON endpoint.

    Parameters
    ----------
    url : str
        URL of the JSON endpoint. For the complete response schema, see References.
        Example response: `{ "schemaVersion": 1, "label": "hello", "message": "sweet world", "color": "orange" }`

    References
    ----------
    - [Shields.io API - Endpoint Badge](https://shields.io/badges/endpoint-badge)
    """
    return Badger().create(path="endpoint", queries={"url": url})


def binder(message: str = "Binder") -> BinderBadger:
    """Create a Binder badger.

    Parameters
    ----------
    message : str, default: "Binder"
        Default message to display on the badge.
    """
    return BinderBadger(message=message)


def codecov(
    vcs_name: _Literal["github", "gh", "gitlab", "gl", "bitbucket", "bb"],
    user: str,
    repo: str,
    token: str | None = None,
) -> CodeCovBadger:
    """Create a CodeCov badger.

    Parameters
    ----------
    vcs_name : {'github', 'gh', 'gitlab', 'gl', 'bitbucket', 'bb'}
        Name of the version control system hosting the repository.
    user : str
        Username of the repository owner.
    repo : str
        Name of the repository.
    token : str, optional
        Token to authenticate with the CodeCov API for private repositories.
        You can find the token under the badge section of your project settings page at
        `https://codecov.io/[vcsName]/[user]/[repo]/settings/badge`.
    """
    return CodeCovBadger(vcs_name=vcs_name, user=user, repo=repo, token=token)


def conda(
    package: str,
    channel: str = "conda-forge",
) -> CondaBadger:
    """Create a Conda badger.

    Parameters
    ----------
    package : str
        Package name.
    channel : str, default: 'conda-forge'
        Channel name.
    """
    return CondaBadger(package=package, channel=channel)


def discord(server_id: str) -> DiscordBadger:
    """Create a Discord badger.

    Parameters
    ----------
    server_id : str
        Server ID of the Discord server (e.g., `102860784329052160`),
        which can be located in the url of the channel.

    Notes
    -----
    A Discord server admin must enable the widget setting on the server for this badge to work.
    This can be done in the Discord app: Server Setting > Widget > Enable Server Widget

    References
    ----------
    [Shields.io API - Discord](https://shields.io/badges/discord)
    """
    return DiscordBadger(server_id=server_id)


def github(
    user: str,
    repo: str,
) -> GitHubBadger:
    """Create a GitHub badger.

    Parameters
    ----------
    user : str
        Username of the repository owner.
    repo : str
        Name of the repository.
    """
    return GitHubBadger(user=user, repo=repo)


def librariesio(
    platform: str | None = None,
    package: str | None = None,
    scope: str | None = None,
) -> LibrariesIOBadger:
    """Create a Libraries.io badger.

    Parameters
    ----------
    platform : str
        Name of the platform where the package is distributed, e.g. 'pypi', 'npm', etc.
    package : str
        Name of the package.
    scope : str, optional
        The scope of the npm package, e.g., `@babel`.
    """
    return LibrariesIOBadger(platform=platform, package=package, scope=scope)


def pepy(package: str) -> PePyBadger:
    """Create a PePy badger.

    Parameters
    ----------
    package : str
        Name of the package.
    """
    return PePyBadger(package=package)


def pypi(
    package: str,
    pypi_base_url: str = "https://pypi.org",
) -> PyPIBadger:
    """Create a PyPI badger.

    Parameters
    ----------
    package : str
        Name of the package.
    pypi_base_url : str, default: 'https://pypi.org'
        Base URL of the PyPI website.
    """
    return PyPIBadger(package=package, pypi_base_url=pypi_base_url)


def readthedocs(name: str) -> ReadTheDocsBadger:
    """Create a ReadTheDocs badger.

    Parameters
    ----------
    name : str
        The name of the project on Read The Docs.
    """
    return ReadTheDocsBadger(name=name)


def repodynamics() -> RepoDynamicsBadger:
    """Create a RepoDynamics badger."""
    return RepoDynamicsBadger()


def website(
    url: str,
    up_message: str | None = None,
    up_color: str | None = None,
    down_message: str | None = None,
    down_color: str | None = None,
):
    return Badger().create(
        path="website",
        queries={k: v for k, v in locals().items() if v is not None},
        attrs_img={"alt": "Website Status", "title": "Server status of our website."},
        attrs_a={"href": url}
    )