import pylinks as _pylinks

import pybadger as _pybadger


class Badger(_pybadger.Badger):
    """Shields Badge generator."""

    def __init__(self, base_path: str | None = None):
        """Instantiate a new Shields badge generator.

        Parameters
        ----------
        base_path : str, optional
            Common base path for the API endpoint.
        """
        super().__init__(
            base_url=_pylinks.url.create("https://img.shields.io") / base_path,
            badge="shields",
        )
        return
