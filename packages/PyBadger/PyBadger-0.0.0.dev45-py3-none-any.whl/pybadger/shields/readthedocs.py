import pylinks as _pylinks

from pybadger import shields as _shields


class ReadTheDocsBadger(_shields.Badger):
    """Shields.io badge generator for ReadTheDocs."""

    def __init__(self, name: str, validate_urls: bool = False):
        """Create a ReadTheDocs badger.

        Parameters
        ----------
        name : str
            The name of the project on Read The Docs.
        """
        super().__init__(base_path="readthedocs")
        self._name = name
        self._link = _pylinks.site.readthedocs.project(name=name, validate=validate_urls)
        return

    def build_status(self, version: str | None = None) -> _shields.Badge:
        """Create a website build status badge.

        Parameters
        ----------
        version : str, optional
            A specific version of the website to query.
            If not provided, the latest version will be queried.
        """
        return self.create(
            path=f"{self._name}{f'/{version}' if version else ''}",
            params={"label": "Website", "logo": "readthedocs"},
            attrs_img={
                "alt": "Website Build Status",
                "title": "Website build status. Click to see more details on the ReadTheDocs platform.",
            },
            attrs_a={"href": self._link.build_status},
        )
