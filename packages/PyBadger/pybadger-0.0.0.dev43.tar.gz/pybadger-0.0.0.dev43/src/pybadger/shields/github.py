from typing import Literal

import pylinks as _pylinks

from pybadger import shields as _shields


class GitHubBadger(_shields.Badger):
    """Shields.io badge generator for GitHub."""

    def __init__(
        self,
        user: str,
        repo: str,
        validate_urls: bool = False,
    ):
        """Create a GitHub badger.

        Parameters
        ----------
        user : str
            GitHub username.
        repo : str
            GitHub repository name.
        """
        super().__init__(base_path="github")
        self._user = user
        self._repo = repo
        self._repo_link = _pylinks.site.github.user(user).repo(repo, validate=validate_urls)
        self._endpoint_key = f"{user}/{repo}"
        return

    def commit_activity(
        self,
        interval: Literal["t", "y", "m", "w"] = "t",
        author_filter: str | None = None,
        branch: str | None = None,
    ) -> _shields.Badge:
        """Number of commits in a branch.

        Parameters
        ----------
        interval : {'t', 'y', 'm', 'w'}, default: 't'
            Interval of time to calculate the number of commits.
            - 't': total
            - 'y': last year
            - 'm': last month
            - 'w': last week
        author_filter : str, optional
            A GitHub username to only count commits by that user.
        branch: str, optional
            A specific branch to count commits in.
            If not provided, the default (i.e., main) branch of the repository is used.
            If the branch is not provided here but a default value is set
            in the `branch` attribute of this instance, that branch will be used.
            To use the default repository branch regardless of whether a default value is set or not,
            set this argument to an empty string.

        References
        ----------
        - [Shields.io API - GitHub commit activity](https://shields.io/badges/git-hub-commit-activity)
        - [Shields.io API - GitHub commit activity (branch)](https://shields.io/badges/git-hub-commit-activity-branch)
        """
        path = f"commit-activity/{interval}/{self._endpoint_key}"
        if branch:
            path += f"/{branch}"
            link = self._repo_link.branch(branch).commits
        else:
            link = self._repo_link.commits
        interval_text = {"y": "year", "m": "month", "w": "week"}
        title = (
            f"{'Total number' if interval == 't' else 'Number'} of commits "
            f"""{f"in branch '{branch}' " if branch else ''}"""
            f"{f'in the last {interval_text[interval]}' if interval != 't' else ''}. "
            "Click to see the full list of commits."
        )
        return self.create(
            path=path,
            queries={"authorFilter": author_filter},
            params={"label": "Commits"},
            attrs_img={"alt": f"Commits/{interval_text[interval].title()}" if interval != 't' else "Total commits", "title": title},
            attrs_a={"href": link},
        )

    def commits_difference(
        self,
        base: str,
        head: str,
    ) -> _shields.Badge:
        """Number of commits between two references, i.e., branches, tags, or hashes.

        Parameters
        ----------
        base : str
            The base reference.
        head : str
            The head reference.

        References
        ----------
        - [Shields.io API - GitHub commits difference between two branches/tags/commits](https://shields.io/badges/git-hub-commits-difference-between-two-branches-tags-commits)
        """
        return self.create(
            path=f"commits-difference/{self._endpoint_key}",
            queries={"base": base, "head": head},
            params={"label": "Commits Difference"},
            attrs_img={
                "alt": "Commits difference",
                "title": (
                    f"Number of commits between '{base}' and '{head}'. "
                    f"Click to see the full list of commits."
                )
            },
            attrs_a={"href": self._repo_link.compare(base, head)},
        )

    def commits_since_latest_release(
        self,
        include_prereleases: bool = True,
        sort: Literal["date", "semver"] = "date",
        filter: str | None = None,
        branch: str | None = None,
    ) -> _shields.Badge:
        """Number of commits since the latest release.

        Parameters
        ----------
        include_prereleases : bool, default: True
            Whether to include prereleases.
        sort : {'date', 'semver'}, default: 'date'
            Sort the releases by date or by Semantic Versioning.
        filter : str, optional
            Filter the tags/release names before selecting the latest from the list.
            Two constructs are available:
            - `*` is a wildcard matching zero or more characters.
            - `!` negates the whole pattern.
        branch: str, optional
            A specific branch to look for releases.
            If not provided, the default (i.e., main) branch of the repository is used.
            If the branch is not provided here but a default value is set
            in the `branch` attribute of this instance, that branch will be used.
            To use the default repository branch regardless of whether a default value is set or not,
            set this argument to an empty string.

        References
        ----------
        - [Shields.io API - GitHub commits since latest release](https://shields.io/badges/git-hub-commits-since-latest-release)
        - [Shields.io API - GitHub commits since latest release (branch)](https://shields.io/badges/git-hub-commits-since-latest-release-branch)
        """
        path = f"commits-since/{self._endpoint_key}/latest"
        if branch:
            path += f"/{branch}"
            link = self._repo_link.branch(branch).commits
        else:
            link = self._repo_link.commits
        return self.create(
            path=path,
            queries={"include_prereleases": include_prereleases, "sort": sort, "filter": filter},
            params={"label": "Commits Since Latest Release"},
            attrs_img={
                "alt": "Commits since latest release",
                "title": (
                    f"Number of commits since the latest release{' on branch ' + branch if branch else ''}. "
                    "Click to see the full list of commits."
                )
            },
            attrs_a={"href": link},
        )

    def commits_since_tag(
        self,
        tag: str,
        branch: str | None = None,
    ) -> _shields.Badge:
        """Number of commits since a specific tag.

        Parameters
        ----------
        tag : str
            The tag.
        branch: str, optional
            A specific branch to look for the tagged version.
            If not provided, the default (i.e., main) branch of the repository is used.
            If the branch is not provided here but a default value is set
            in the `branch` attribute of this instance, that branch will be used.
            To use the default repository branch regardless of whether a default value is set or not,
            set this argument to an empty string.

        References
        ----------
        - [Shields.io API - GitHub commits since tagged version](https://shields.io/badges/git-hub-commits-since-tagged-version)
        - [Shields.io API - GitHub commits since tagged version (branch)](https://shields.io/badges/git-hub-commits-since-tagged-version-branch)
        """
        path = f"commits-since/{self._endpoint_key}/{tag}"
        if branch:
            path += f"/{branch}"
            link = self._repo_link.branch(branch).commits
        else:
            link = self._repo_link.commits
        return self.create(
            path=path,
            params={"label": f"Commits Since {tag}"},
            attrs_img={
                "alt": f"Commits since tag '{tag}'",
                "title": (
                    f"Number of commits since tag '{tag}'{' on branch ' + branch if branch else ''}. "
                    "Click to see the full list of commits."
                )
            },
            attrs_a={"href": link},
        )

    def contributors(self, include_anon: bool = True) -> _shields.Badge:
        """Number of contributors.

        References
        ----------
        - [Shields.io API - GitHub contributors](https://shields.io/badges/git-hub-contributors)
        """
        metric = "contributors-anon" if include_anon else "contributors"
        return self.create(
            path=f"{metric}/{self._endpoint_key}",
            params={"label": "Contributors"},
            attrs_img={
                "alt": "Repository contributors",
                "title": "Total number of contributors. Click to see the full list of contributors."
            },
            attrs_a={"href": self._repo_link.contributors()}
        )

    def created_at(
        self,
    ) -> _shields.Badge:
        """Date of repository creation.

        References
        ----------
        - [Shields.io API - GitHub created at](https://shields.io/badges/git-hub-created-at)
        """
        return self.create(
            path=f"created-at/{self._endpoint_key}",
            params={"label": "Created"},
            attrs_img={
                "alt": "Repository creation date",
                "title": "Repository creation date."
            },
        )

    def last_commit(
        self,
        path: str | None = None,
        display_timestamp: Literal["author", "committer"] = "author",
        branch: str | None = None,
    ) -> _shields.Badge:
        """Time of the last commit (of a file) in a branch.

        Parameters
        ----------
        path : str, optional
            A specific path in the repository to check for the last commit.
            If not provided, the last commit of the branch is selected.
        display_timestamp : {'author', 'committer'}, default: 'author'
            Whether to display the author's timestamp or the committer's timestamp.
        branch: str, optional
            A specific branch to look for the last commit.
            If not provided, the default (i.e., main) branch of the repository is used.
            If the branch is not provided here but a default value is set
            in the `branch` attribute of this instance, that branch will be used.
            To use the default repository branch regardless of whether a default value is set or not,
            set this argument to an empty string.

        References
        ----------
        - [Shields.io API - GitHub last commit](https://shields.io/badges/git-hub-last-commit)
        - [Shields.io API - GitHub last commit (branch)](https://shields.io/badges/git-hub-last-commit-branch)
        """
        api_path = f"last-commit/{self._endpoint_key}"
        if branch:
            api_path += f"/{branch}"
            link = self._repo_link.branch(branch).commits
        else:
            link = self._repo_link.commits
        return self.create(
            path=api_path,
            queries={"path": path, "display_timestamp": display_timestamp},
            params={"label": "Last Commit"},
            attrs_img={
                "alt": "Last commit",
                "title": (
                    f"Time of the last commit{' on branch ' + branch if branch else ''}. "
                    "Click to see the full list of commits."
                )
            },
            attrs_a={"href": link},
        )

    def release_date(
        self,
        include_prereleases: bool = True,
        display_date: Literal["created_at", "published_at"] = "published_at",
    ) -> _shields.Badge:
        """Date of the latest release.

        Parameters
        ----------
        include_prereleases : bool, default: True
            Whether to include prereleases.
        display_date : {'created_at', 'published_at'}, default: 'created_at'
            Whether to display the creation date of the release or the publication date.

        References
        ----------
        - [Shields.io API - GitHub release date](https://shields.io/badges/git-hub-release-date)
        """
        path = f"{"release-date-pre" if include_prereleases else "release-date"}/{self._endpoint_key}"
        return self.create(
            path=path,
            queries={"display_date": display_date},
            params={"label": "Latest Release"},
            attrs_img={
                "alt": "Latest release date",
                "title": (
                    "Latest release date. "
                    "Click to see more details in the Releases section of the repository."
                )
            },
            attrs_a={"href": self._repo_link.releases(tag="latest")},
        )

    def language_count(self) -> _shields.Badge:
        """Number of programming languages used in the repository.

        References
        ----------
        - [Shields.io API - GitHub language count](https://shields.io/badges/git-hub-language-count)
        """
        return self.create(
            path=f"languages/count/{self._endpoint_key}",
            params={"label": "Languages"},
            attrs_img={
                "alt": "Programming Languages",
                "title": (
                    "Number of programming languages used in the project."
                )
            },
        )

    def search_hits(self, query: str) -> _shields.Badge:
        """Number of search hits in the repository.

        Parameters
        ----------
        query : str
            The search query.

        References
        ----------
        - [Shields.io API - GitHub search hit counter](https://shields.io/badges/git-hub-search-hit-counter)
        """
        return self.create(
            path=f"search/{self._endpoint_key}/{query}",
            params={"label": query},
            attrs_img={
                "alt": "Search Hits ({query})",
                "title": f"Number of search hits for query '{query}' in the repository.",
            },
        )

    def top_language(
        self,
    ) -> _shields.Badge:
        """The top language in the repository, and its share in percent.

        References
        ----------
        - [Shields.io API - GitHub top language](https://shields.io/badges/git-hub-top-language)
        """
        return self.create(
            path=f"languages/top/{self._endpoint_key}",
            attrs_img={
                "alt": "Top Programming Language",
                "title": "Percentage of the most used programming language in the repository."
            },
        )

    def workflow_status(
        self,
        workflow: str,
        branch: str | None = None,
        event: str | None = None,
    ) -> _shields.Badge:
        """Status of a GitHub Actions workflow.

        Parameters
        ----------
        workflow : str
            The name of the workflow file, e.g., 'ci.yaml'.
        branch : str, optional
            The branch to check the workflow status for.
            If not provided, the default (i.e., main) branch of the repository is used.
            If the branch is not provided here but a default value is set
            in the `branch` attribute of this instance, that branch will be used.
            To use the default repository branch regardless of whether a default value is set or not,
            set this argument to an empty string.
        event : str, optional
            The event that triggered the workflow.

        References
        ----------
        - [Shields.io API - GitHub workflow status](https://shields.io/badges/git-hub-workflow-status)
        """
        return self.create(
            path=f"actions/workflow/status/{self._endpoint_key}/{workflow}",
            queries={"branch": branch, "event": event},
            params={"label": "Workflow"},
            attrs_img={
                "alt": "Workflow Status",
                "title": (
                    f"Status of the GitHub Actions workflow '{workflow}'"
                    f"{f' on branch {branch}' if branch else ''}"
                    f"{f' for event {event}' if event else ''}."
                    "Click to see more details in the Actions section of the repository."
                ),
            },
            attrs_a={
                "href": (
                    self._repo_link.branch(branch).workflow(workflow)
                    if branch else self._repo_link.workflow(workflow)
                ),
            },
        )

    def branch_check_runs(
        self,
        branch: str,
        name_filter: str | None = None,
    ) -> _shields.Badge:
        """Status of GitHub Actions check-runs for a branch.

        Parameters
        ----------
        branch : str
            Branch name.
        name_filter : str, optional
            Name of a specific check-run.

        References
        ----------
        - [Shields.io API - GitHub branch check runs](https://shields.io/badges/git-hub-branch-check-runs)
        """
        return self.create(
            path=f"check-runs/{self._endpoint_key}/{branch}",
            queries={"nameFilter": name_filter},
            params={"label": "Check Runs"},
            attrs_img={
                "alt": "Check-Runs Status",
                "title": (
                    f"Status of GitHub Actions check-runs on branch '{branch}'"
                    f"{f' for check-run {name_filter}' if name_filter else ''}."
                ),
            },
        )

    def downloads_all_releases(self, asset: str | None = None) -> _shields.Badge:
        """Number of downloads of all releases.

        Parameters
        ----------
        asset : str, optional
            Name of a specific asset to query.

        References
        ----------
        - [Shields.io API - GitHub Downloads (all assets, all releases)](https://shields.io/badges/git-hub-downloads-all-assets-all-releases)
        - [Shields.io API - GitHub Downloads (specific asset, all releases)](https://shields.io/badges/git-hub-downloads-specific-asset-all-releases)
        """
        return self.create(
            path=f"downloads/{self._endpoint_key}/{asset if asset else 'total'}",
            params={"label": "Downloads", "logo": "github"},
            attrs_img={
                "alt": "GitHub Downloads",
                "title": "Number of downloads of all releases from GitHub.",
            },
            attrs_a={"href": self._repo_link.releases()},
        )

    def downloads_release(
        self,
        asset: str | None = None,
        tag: str | Literal["latest"] = "latest",
        include_prereleases: bool = True,
        sort: Literal["date", "semver"] = "date",
    ) -> _shields.Badge:
        """
        Number of downloads of a GitHub release.

        Parameters
        ----------
        asset : str, optional
            Name of a specific asset to query.
        tag : str, default: "latest"
            Release tag to query. Setting to 'latest' will query the latest release.
        include_prereleases : bool, default: True
            Whether to include pre-releases.
        sort : {'date', 'semver'}, default: 'date'
            Sort the releases by date or by Semantic Versioning.
            Only applicable if `tag` is set to 'latest'.

        References
        ----------
        - [Shields.io API - GitHub Downloads (all assets, latest release)](https://shields.io/badges/git-hub-downloads-all-assets-latest-release)
        - [Shields.io API - GitHub Downloads (all assets, specific tag)](https://shields.io/badges/git-hub-downloads-all-assets-specific-tag)
        - [Shields.io API - GitHub Downloads (specific asset, latest release)](https://shields.io/badges/git-hub-downloads-specific-asset-latest-release)
        - [Shields.io API - GitHub Downloads (specific asset, specific tag)](https://shields.io/badges/git-hub-downloads-specific-asset-specific-tag)
        """
        return self.create(
            path=(
                f"{"downloads-pre" if tag == "latest" and include_prereleases else "downloads"}/"
                f"{self._endpoint_key}/{tag}/{asset if asset else 'total'}"
            ),
            queries={"sort": sort} if tag == "latest" else None,
            params={"label": "Downloads", "logo": "github"},
            attrs_img={
                "alt": "GitHub Downloads",
                "title": (
                    f"Number of downloads from GitHub for the "
                    f"{'latest release' if tag == 'latest' else f'release tag {tag}'}. "
                    f"Click to see more details in the 'Releases' section of the repository."
                )
            },
            attrs_a={"href": self._repo_link.releases(tag=tag)},
        )

    def issue_search_hits(self, query: str) -> _shields.Badge:
        """Number of search hits for a query in issues/pull requests.

        Parameters
        ----------
        query : str
            The search query.
            For example, `type:issue is:closed label:bug`.
            For a full list of available filters and allowed values,
            see GitHub's documentation on [Searching issues and pull requests](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests).

        References
        ----------
        - [Shields.io API - GitHub issue custom search in repo](https://shields.io/badges/git-hub-issue-custom-search-in-repo)
        """
        return self.create(
            path=f"issues-search/{self._endpoint_key}",
            queries={"query": query},
            params={"label": query},
            attrs_img={
                "alt": f"Search Hits ({query})",
                "title": f"Number of search hits for query '{query}' in repository issues/pulls."
            },
        )

    def issue_details(
        self,
        kind: Literal["issues", "pulls"],
        number: int,
        property: Literal["state", "title", "author", "label", "comments", "age", "last-update", "milestone"],
    ) -> _shields.Badge:
        """Details of an issue or pull request.

        Parameters
        ----------
        kind : {'issues', 'pulls'}
            Whether to query issues or pull requests.
        number : int
            The issue or pull request number.
        property : {'state', 'title', 'author', 'label', 'comments', 'age', 'last-update', 'milestone'}
            The property to display.

        References
        ----------
        - [Shields.io API - GitHub issue/pull reqyest detail](https://shields.io/badges/git-hub-issue-pull-request-detail)
        """
        return self.create(
            path=f"{kind}/detail/{property}/{self._endpoint_key}/{number}",
            params={"label": f"{property.capitalize()} (#{number})"},
            attrs_img={
                "alt": "Issue Details",
                "title": f"{property.capitalize()} of the issue/pull number {number}.",
            },
        )

    def issue_count(
        self,
        kind: Literal["issues", "pulls"],
        state: Literal["open", "closed"] = "open",
        label: str | None = None,
        show_state: bool = True,
    ):
        """Number of open/closed issues or pull requests.

        Parameters
        ----------
        kind : {'issues', 'pulls'}
            Whether to query issues or pull requests.
        state : {'open', 'closed'}, default: 'open'
            Whether to query open or closed issues/pull requests.
        label : str, optional
            A specific GitHub label to filter issues/pulls.
        show_state : bool, default: True
            Whether to display the queried state on the right-hand side of the badge.
        """
        variant = {
            ("issues", "open", True): "issues",
            ("issues", "open", False): "issues-raw",
            ("issues", "closed", True): "issues-closed",
            ("issues", "closed", False): "issues-closed-raw",
            ("pulls", "open", True): "issues-pr",
            ("pulls", "open", False): "issues-pr-raw",
            ("pulls", "closed", True): "issues-pr-closed",
            ("pulls", "closed", False): "issues-pr-closed-raw",
        }
        return self.create(
            path=f"{variant[(kind, state, show_state)]}/{self._endpoint_key}{f'/{label}' if label else ''}",
            params={
                "label": (
                    f"{kind.capitalize() if show_state else 
                    f'{state.capitalize()} {kind.capitalize()}'}{f' ({label})' if label else ''}"
                )
            },
            attrs_img={
                "alt": f"{state.capitalize()} {kind.capitalize()} Count",
                "title": f"Number of {state} {kind}{f' with label {label}' if label else ''}.",
            },
        )

    def license(
        self,
        filename: str = "LICENSE",
        branch: str = "main",
    ) -> _shields.Badge:
        """License of the GitHub repository.

        Parameters
        ----------
        filename : str, default: 'LICENSE'
            Name of the license file in the GitHub branch.
            This is used to create a link to the license.
        branch : str, default: 'main'
            The branch to look for the license file.
            This is used to create a link to the license.

        References
        ----------
        - [Shields.io API - GitHub license](https://shields.io/badges/git-hub-license)
        """
        return self.create(
            path=f"license/{self._endpoint_key}",
            params={"label": "License"},
            attrs_img={
                "alt": "License",
                "title": f"Project license. Click to read the complete license.",
            },
            attrs_a={"href": self._repo_link.branch(branch).file(filename)},
        )

    def deployment_status(self, environment: str) -> _shields.Badge:
        """Deployment status of a GitHub environment.

        Parameters
        ----------
        environment : str
            The name of the deployment environment.

        References
        ----------
        - [Shields.io API - GitHub deployments](https://shields.io/badges/git-hub-deployments)
        """
        return self.create(
            path=f"deployments/{self._endpoint_key}/{environment}",
            params={"label": f"CD {environment}"},
            attrs_img={
                "alt": "Deployment Status",
                "title": f"Deployment status for '{environment}' environment."
            },
            attrs_a={"href": self._repo_link.homepage / "deployments" / environment}
        )

    def discussion_count(
        self,
    ) -> _shields.Badge:
        """Number of discussions in the GitHub repository.

        References
        ----------
        - [Shields.io API - GitHub discussions](https://shields.io/badges/git-hub-discussions)
        """
        return self.create(
            path=f"discussions/{self._endpoint_key}",
            params={"label": "Discussions"},
            attrs_img={
                "alt": "Discussion Count",
                "title": f"Number of discussions. Click to open the Discussions section of the repository.",
            },
            attrs_a={"href": self._repo_link.discussions()},
        )

    def discussion_search_hits(self, query: str) -> _shields.Badge:
        """Number of search hits for a query in discussions.

        Parameters
        ----------
        query : str
            The search query.
            For example, `is:answered answered-by:someUsername`.
            For a full list of available filters and allowed values,
            see GitHub's documentation on [Searching discussions](https://docs.github.com/en/search-github/searching-on-github/searching-discussions).

        References
        ----------
        - [Shields.io API - GitHub discussions custom search in repo](https://shields.io/badges/git-hub-discussions-custom-search-in-repo)
        """
        return self.create(
            path=f"discussions-search/{self._endpoint_key}",
            queries={"query": query},
            params={"label": query},
            attrs_img={
                "alt": f"Discussions Search Hits ({query})",
                "title": f"Number of search hits for query '{query}' in repository discussions.",
            },
        )

    def code_size(self) -> _shields.Badge:
        """Code size in bytes.

        References
        ----------
        - [Shields.io API - GitHub code size in bytes](https://shields.io/badges/git-hub-code-size-in-bytes)
        """
        return self.create(
            path=f"languages/code-size/{self._endpoint_key}",
            params={"label": "Code Size"},
            attrs_img={
                "alt": "Code Size",
                "title": "Code size"
            },
        )

    def dir_count(
        self,
        path: str | None = None,
        typ: Literal["file", "dir"] | None = None,
        extension: str | None = None,
    ) -> _shields.Badge:
        """Number of files/subdirectories directly in a directory (not recursive).

        Parameters
        ----------
        path : str, optional
            A path to count the files/directories in.
            If not provided, the count is for the root directory.
        typ : {'file', 'dir'}, optional
            Whether to count files or directories.
            If not provided, both files and directories are counted.
            Note that due to GitHub API's limit, if a directory contains more than 1000 files,
            the badge will show an inaccurate count.
        extension : str, optional
            Count only files with a specific extension.
            Specify the extension without a leading dot.
            Only applicable if `typ` is `file`.

        References
        ----------
        - [Shields.io API - GitHub repo file or directory count](https://shields.io/badges/git-hub-repo-file-or-directory-count)
        - [Shields.io API - GitHub repo file or directory count (in path)](https://shields.io/badges/git-hub-repo-file-or-directory-count-in-path)
        """
        things = (
            "files and directories" if not typ else (
                "directories" if typ == "dir" else f"{f'{extension.upper()} ' if extension else ''}files"
            )
        )
        return self.create(
            path=f"directory-file-count/{self._endpoint_key}{f'/{path}' if path else ''}",
            queries={"type": typ, "extension": extension},
            params={"label": "Files"},
            attrs_img={
                "alt": "File Count",
                "title": f"Number of {things} in the {path if path else 'root'} directory",
            },
        )

    def repo_size(
        self,
    ) -> _shields.Badge:
        """Total size of the repository in bytes.

        References
        ----------
        - [Shields.io API - GitHub repo size](https://shields.io/badges/git-hub-repo-size)
        """
        return self.create(
            path=f"repo-size/{self._endpoint_key}",
            params={"label": "Repo Size"},
            attrs_img={
                "alt": "Repository Size",
                "title": f"Total size of the repository."
            },
        )

    def forks(
        self,
    ) -> _shields.Badge:
        """Number of repository forks.

        References
        ----------
        - [Shields.io API - GitHub forks](https://shields.io/badges/git-hub-forks)
        """
        return self.create(
            path=f"forks/{self._endpoint_key}",
            params={"label": "Forks"},
            attrs_img={
                "alt": "Forks",
                "title": f"Number of repository forks",
            },
        )

    def stars(self) -> _shields.Badge:
        """Number of repository stars.

        References
        ----------
        - [Shields.io API - GitHub Repo stars](https://shields.io/badges/git-hub-repo-stars)
        """
        return self.create(
            path=f"stars/{self._endpoint_key}",
            params={"label": "Stars"},
            attrs_img={
                "alt": "Stars",
                "title": f"Number of repository stars",
            },
        )

    def watchers(self) -> _shields.Badge:
        """Number of repository watchers.

        References
        ----------
        - [Shields.io API - GitHub watchers](https://shields.io/badges/git-hub-watchers)
        """
        return self.create(
            path=f"watchers/{self._endpoint_key}",
            params={"label": "Watchers"},
            attrs_img={
                "alt": "Repository Watchers",
                "title": "Number of repository watchers"
            },
        )

    def version(
        self,
        source: Literal["tag", "release"] = "release",
        display_name: Literal["tag", "release"] | None = "release",
        sort: Literal["date", "semver"] = "date",
        filter: str | None = None,
        include_prereleases: bool = True,
    ) -> _shields.Badge:
        """Latest version of the software.

        Parameters
        ----------
        source : {'tag', 'release'}, default: 'release'
            Whether to get the latest version from tags or releases.
        display_name : {'tag', 'release'}, default: 'release'
            Whether to display the tag name or release name.
            Only applicable if `source` is set to 'release'.
        sort : {'date', 'semver'}, default: 'date'
            Sort the releases by date or by Semantic Versioning.
        filter : str, optional
            Filter the tags/release names before selecting the latest from the list.
            Two constructs are available:
            - `*` is a wildcard matching zero or more characters.
            - `!` negates the whole pattern.
        include_prereleases : bool, default: True
            Whether to include pre-releases.

        References
        ----------
        - [Shields.io API - GitHub Release](https://shields.io/badges/git-hub-release)
        - [Shields.io API - GitHub Tag](https://shields.io/badges/git-hub-tag)
        """
        queries = {"sort": sort, "filter": filter, "include_prereleases": include_prereleases}
        if source == "release":
            queries["display_name"] = display_name
        return self.create(
            path=f"v/{source}/{self._endpoint_key}",
            queries=queries,
            params={"label": "Latest Version"},
            attrs_img={
                "alt": "Latest Version",
                "title": (
                    f"Latest version of the package. "
                    f"Click to see more details in the 'Releases' section of the repository.",
                )
            },
            attrs_a={"href": self._repo_link.releases(tag="latest")},
        )

    def milestone_count(self, state: Literal["open", "closed", "all"] = "all") -> _shields.Badge:
        """Number of milestones in the repository.

        Parameters
        ----------
        state : {'open', 'closed', 'all'}, default: 'all'
            Whether to count open, closed, or all milestones.

        References
        ----------
        - [Shields.io API - GitHub number of milestones](https://shields.io/badges/git-hub-number-of-milestones)
        """
        return self.create(
            path=f"milestones/{state}/{self._endpoint_key}",
            params={"label": f"{state.upper()} Milestones"},
            attrs_img={
                "alt": "Milestone Count",
                "title": (
                    f"Number of {state} milestones. "
                    f"Click to see more details in the Milestones section of the repository.",
                )
            },
            attrs_a={"href": self._repo_link.milestones(state=state if state == "closed" else "open")},
        )
