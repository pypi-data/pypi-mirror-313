from pybadger import shields as _shields


class PePyBadger(_shields.Badger):
    """Shields.io badge generator for Pepy."""

    def __init__(
        self,
        package: str,
    ):
        """Create a Pepy badger."""
        super().__init__(base_path="pepy")
        self._package = package
        return

    def total_downloads(self) -> _shields.Badge:
        """Create a badge for number of total downloads.

        References
        ----------
        [Shields.io API - Pepy Total Downloads](https://shields.io/badges/pepy-total-downlods)
        """
        return self.create(
            path=f"dt/{self._package}",
            params={"label": "Downloads", "logo": "pypi"},
            attrs_img={
                "alt": "PyPI Downloads",
                "title": (
                    "Total number of downloads of all releases from PyPI. "
                    "Click to see more details on pypi.org."
                ),
            },
            attrs_a={"href": f"https://pepy.tech/projects/{self._package}"},
        )
