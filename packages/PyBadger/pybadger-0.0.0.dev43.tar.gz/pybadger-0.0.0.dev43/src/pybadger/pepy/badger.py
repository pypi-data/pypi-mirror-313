import pylinks as _pylinks

import pybadger as _pybadger


class Badger(_pybadger.Badger):
    """PePy Badge generator."""

    def __init__(self, base_path: str | None = None):
        """Instantiate a new PePy badge generator.

        Parameters
        ----------
        base_path : str, optional
            Common base path for the API endpoint.
        """
        super().__init__(
            base_url=_pylinks.url.create("https://static.pepy.tech/personalized-badge") / base_path,
            badge="pepy",
        )
        return
