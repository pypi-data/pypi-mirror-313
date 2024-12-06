from typing import Literal as _Literal

from pybadger import shields as _shields


class CodeCovBadger(_shields.Badger):
    """Shields.io badge generator for CodeCov."""

    def __init__(
        self,
        vcs_name: _Literal["github", "gh", "gitlab", "gl", "bitbucket", "bb"],
        user: str,
        repo: str,
        token: str | None = None,
    ):
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
        super().__init__(base_path="codecov/c")
        self._token = token
        vsc_abbr = {"github": "gh", "gitlab": "gl", "bitbucket": "bb"}.get(vcs_name, vcs_name)
        self._link = f"https://codecov.io/{vsc_abbr}/{user}/{repo}"
        self._path = f"{vcs_name}/{user}/{repo}"
        return

    def coverage(
        self,
        flag: str | None = None,
        branch: str | None = None,
    ) -> _shields.Badge:
        """Create a code coverage badge.

        Parameters
        ----------
        flag : str, optional
            A specific flag to query.
        branch : str, optional
            Name of a specific branch to query.

        References
        ----------
        [Shields.io API - Codecov](https://shields.io/badges/codecov)
        [Shields.io API - Codecov (with branch)](https://shields.io/badges/codecov-with-branch)
        """
        if branch:
            link = f"{self._link}/branch/{branch}"
            path = f"{self._path}/{branch}"
        else:
            link = self._link
            path = self._path
        return self.create(
            path=path,
            queries={"token": self._token, "flag": flag},
            params={"label": "Test Coverage", "logo": "codecov"},
            attrs_a={"href": link},
            attrs_img={
                "alt": "Test Coverage",
                "title": "Source code coverage by the test suite. Click to see more details on codecov.io.",
            },
        )
