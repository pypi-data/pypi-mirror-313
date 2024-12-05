"""PyBadger base badge."""

from __future__ import annotations

import htmp as _htmp
import pylinks as _pylinks

from pybadger.protocol import AttrDict as _AttrDict


class Badge:
    """Base Badge.

    All platform-specific badges inherit from this class.
    """
    def __init__(
        self,
        base_url: str | _pylinks.url.URL,
        params_light: _AttrDict = None,
        params_dark: _AttrDict = None,
        attrs_img: _AttrDict = None,
        attrs_a: _AttrDict = None,
        attrs_picture: _AttrDict = None,
        attrs_source_light: _AttrDict = None,
        attrs_source_dark: _AttrDict = None,
        attrs_span: _AttrDict = None,
        attrs_div: _AttrDict = None,
        default_light: bool = True,
        merge_params: bool = True,
    ):
        self.base_url = _pylinks.url.create(str(base_url))
        self.params_light = params_light or {}
        self.params_dark = params_dark or {}
        self.attrs_img = attrs_img or {}
        self.attrs_a = attrs_a or {}
        self.attrs_picture = attrs_picture or {}
        self.attrs_source_light = attrs_source_light or {}
        self.attrs_source_dark = attrs_source_dark or {}
        self.attrs_span = attrs_span or {}
        self.attrs_div = attrs_div or {}
        self.default_light = default_light
        self.merge_params = merge_params
        return

    def url(
        self,
        params: _AttrDict = None,
        light: bool | None = None,
        merge_params: bool | None = None,
    ) -> _pylinks.url.URL:
        if params is None:
            default_light = light if light is not None else self.default_light
            merge_params = merge_params if merge_params is not None else self.merge_params
            if default_light:
                params = self.params_light
                params_other = self.params_dark
            else:
                params = self.params_dark
                params_other = self.params_light
            if merge_params:
                params = params_other | params
        url = self.base_url.copy()
        return self._generate_full_url(url, params)

    def img(
        self,
        params: _AttrDict = None,
        attrs_img: _AttrDict = None,
        attrs_a: _AttrDict = None,
        attrs_span: _AttrDict = None,
        attrs_div: _AttrDict = None,
        light: bool | None = None,
        merge_params: bool | None = None,
    ) -> _htmp.Element:
        url = self.url(params=params, light=light, merge_params=merge_params)
        attrs_img = attrs_img if isinstance(attrs_img, dict) else self.attrs_img
        img = _htmp.element.img(src=str(url), **attrs_img)
        return self._add_to_containers(img, attrs_a, attrs_span, attrs_div)

    def picture(
        self,
        params_light: _AttrDict = None,
        params_dark: _AttrDict = None,
        attrs_img: _AttrDict = None,
        attrs_a: _AttrDict = None,
        attrs_picture: _AttrDict = None,
        attrs_source_light: _AttrDict = None,
        attrs_source_dark: _AttrDict = None,
        attrs_span: _AttrDict = None,
        attrs_div: _AttrDict = None,
        default_light: bool = True,
        merge_params: bool = True
    ) -> _htmp.Element:
        params_light = params_light or self.params_light
        params_dark = params_dark or self.params_dark
        if merge_params:
            params_light = params_dark | params_light
            params_dark = params_light | params_dark
        picture = _htmp.elementor.picture_color_scheme(
            self.url(params_light),
            self.url(params_dark),
            attrs_picture if isinstance(attrs_picture, dict) else self.attrs_picture,
            attrs_source_light if isinstance(attrs_source_light, dict) else self.attrs_source_light,
            attrs_source_dark if isinstance(attrs_source_dark, dict) else self.attrs_source_dark,
            attrs_img if isinstance(attrs_img, dict) else self.attrs_img,
            default_light if default_light is not None else self.default_light,
        )
        return self._add_to_containers(picture, attrs_a, attrs_span, attrs_div)

    def unset_all(self) -> Badge:
        self.unset_params()
        self.unset_attrs()
        return self

    def unset_params(self) -> Badge:
        self.params_light = {}
        self.params_dark = {}
        return self

    def unset_attrs(self) -> Badge:
        self.attrs_img = {}
        self.attrs_a = {}
        self.attrs_picture = {}
        self.attrs_source_light = {}
        self.attrs_source_dark = {}
        self.attrs_span = {}
        self.attrs_div = {}
        return self

    def set(
        self,
        params_light: _AttrDict = None,
        params_dark: _AttrDict = None,
        attrs_img: _AttrDict = None,
        attrs_a: _AttrDict = None,
        attrs_picture: _AttrDict = None,
        attrs_source_light: _AttrDict = None,
        attrs_source_dark: _AttrDict = None,
        attrs_span: _AttrDict = None,
        attrs_div: _AttrDict = None,
    ) -> Badge:
        self.set_params(params_light, params_dark)
        self.set_attrs(attrs_img, attrs_a, attrs_picture, attrs_source_light, attrs_source_dark, attrs_span, attrs_div)
        return self

    def set_params(self, light: dict | None = None, dark: dict | None = None) -> Badge:
        params_input = locals()
        for param_type in ("light", "dark"):
            params = params_input[param_type]
            if params is not None:
                new_params = getattr(self, f"params_{param_type}") | params
                setattr(self, f"params_{param_type}", new_params)
        return self

    def set_attrs(
        self,
        img: _AttrDict = None,
        a: _AttrDict = None,
        picture: _AttrDict = None,
        source_light: _AttrDict = None,
        source_dark: _AttrDict = None,
        span: _AttrDict = None,
        div: _AttrDict = None,
    ) -> Badge:
        attrs_input = locals()
        for attr_type in ("img", "a", "picture", "source_light", "source_dark", "span", "div"):
            attrs = attrs_input[attr_type]
            if attrs is not None:
                new_attrs = getattr(self, f"attrs_{attr_type}") | attrs
                setattr(self, f"attrs_{attr_type}", new_attrs)
        return self

    def display(self):
        from IPython.display import HTML, display
        display(HTML(str(self)))
        return

    def __str__(self):
        element = self.picture() if bool(self.params_light) and bool(self.params_dark) else self.img()
        return str(element)

    def __add__(self, other):
        if other is None:
            return self
        if not isinstance(other, Badge):
            raise TypeError("Only badges can be added to badges.")
        return Badge(
            base_url=other.base_url or self.base_url,
            params_light=self.params_light | other.params_light,
            params_dark=self.params_dark | other.params_dark,
            attrs_img=self.attrs_img | other.attrs_img,
            attrs_a=self.attrs_a | other.attrs_a,
            attrs_picture=self.attrs_picture | other.attrs_picture,
            attrs_source_light=self.attrs_source_light | other.attrs_source_light,
            attrs_source_dark=self.attrs_source_dark | other.attrs_source_dark,
            attrs_span=self.attrs_span | other.attrs_span,
            attrs_div=self.attrs_div | other.attrs_div,
            default_light=self.default_light or other.default_light,
            merge_params=self.merge_params or other.merge_params,
        )

    def _add_to_containers(self, element, attrs_a, attrs_span, attrs_div):
        for container_attrs, container_default_attrs, container_gen in (
            (attrs_a, self.attrs_a, _htmp.element.a),
            (attrs_span, self.attrs_span, _htmp.element.span),
            (attrs_div, self.attrs_div, _htmp.element.div),
        ):
            container_attrs = container_attrs if isinstance(container_attrs, dict) else container_default_attrs
            if container_attrs:
                element = container_gen(element, container_attrs)
        return element

    @staticmethod
    def _generate_full_url(url: _pylinks.url.URL, params: dict[str, str | bool]) -> _pylinks.url.URL:
        url.queries |= params
        return url
