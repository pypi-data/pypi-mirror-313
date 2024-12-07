import pylinks as _pylinks

import pybadger
from pybadger.protocol import AttrDict as _AttrDict


class Badge(pybadger.Badge):
    """PePy Badge."""

    def _generate_full_url(
        self,
        url: _pylinks.url.URL,
        params: _AttrDict,
    ) -> _pylinks.url.URL:
        """Generate the full URL for the badge.

        References
        ----------
        - [pepy.domain.model.BadgeStyle](https://github.com/psincraian/pepy/blob/5199022173562ed0118f947c6c58371e2dd2aaec/pepy/domain/model.py#L161)
        """
        for param in (
            "left_text",
            "left_color",
            "right_color",
            "units",
        ):
            if param in params:
                url.queries[param] = params[param]
        return url
