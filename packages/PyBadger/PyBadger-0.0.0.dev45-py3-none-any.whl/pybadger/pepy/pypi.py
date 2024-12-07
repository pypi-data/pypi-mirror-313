from typing import Literal as _Literal

from pybadger import pepy as _pepy


class PyPIBadger(_pepy.Badger):

    def __init__(
        self,
        package: str,
    ):
        """Instantiate a PyPI badge generator.

        Parameters
        ----------
        package : str
            PyPI package name.
        """
        super().__init__(base_path=package)
        self._package = package
        return

    def downloads(
        self,
        period: _Literal["total", "month", "week"] = "total",
    ) -> _pepy.Badge:
        """Number of downloads for a PyPI package.

        Parameters
        ----------
        period : {'total', 'month', 'week'}, default: 'total'
            Time period to query.

        References
        ----------
        - [PePy Source Code](https://github.com/psincraian/pepy/blob/master/pepy/application/badge_service.py)
        """
        return self.create(
            queries={"period": period, "units": units},
            params={
                "left_text": "Total Downloads" if period == "total" else f"Downloads/{period.capitalize()}"
            },
            attrs_a={"href": f"https://pepy.tech/project/{self._package}"}
        )
