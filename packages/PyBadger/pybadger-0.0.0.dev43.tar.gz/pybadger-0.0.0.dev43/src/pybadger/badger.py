"""PyBadger badge generator."""

from typing import Literal as _Literal

import pylinks as _pylinks

import pybadger as _pybadger
from pybadger.protocol import AttrDict as _AttrDict, Stringable as _Stringable


class Badger:
    """Badge generator."""
    def __init__(
        self,
        base_url: _Stringable,
        badge: _Literal["shields", "pepy"] = "shields",
    ):
        """Instantiate a new Badge generator.

        Parameters
        ----------
        base_url : str
            Base URL of the badge generator web API.
        badge : {'shields', 'pepy'}, default: 'shields'
            Type of the badge to generate.
        """
        self._base_url = _pylinks.url.create(str(base_url))
        self._badge = _pybadger.shields.Badge if badge == "shields" else _pybadger.pepy.Badge
        return

    def create(
        self,
        path: _Stringable | None = None,
        queries: _AttrDict = None,
        params: _AttrDict = None,
        attrs_img: _AttrDict = None,
        attrs_a: _AttrDict = None,
        attrs_picture: _AttrDict = None,
        attrs_source_light: _AttrDict = None,
        attrs_source_dark: _AttrDict = None,
    ) -> _pybadger.Badge:
        """Create a Badge.

        Parameters
        ----------
        path : str
            Path to the API endpoint of the badge,
            i.e., what comes after `base_path`.
        queries : dict, optional
            Main URL queries for the badge.
            These are attributes that should always be added to the badge URL.
        params : dict, optional
            Additional URL queries for the badge.
            These can be replaced after the badge creation,
            and can be different in light and dark themes.
        attrs_img : dict, optional
            Attributes for the HTML `img` element.
        attrs_a : dict, optional
            Attributes for the HTML `a` element.
        attrs_picture : dict, optional
            Attributes for the HTML `picture` element.
        attrs_source_light : dict, optional
            Attributes for the HTML `source` element of the light theme.
        attrs_source_dark : dict, optional
            Attributes for the HTML `source` element of the dark theme.
        """
        url = self._base_url / path
        url.queries |= queries or {}
        return self._badge(
            base_url=url,
            params_light=params,
            attrs_img=attrs_img,
            attrs_a=attrs_a,
            attrs_picture=attrs_picture,
            attrs_source_light=attrs_source_light,
            attrs_source_dark=attrs_source_dark,
        )
