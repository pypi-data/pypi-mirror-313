"""PyBadger"""
from __future__ import annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING
from types import FunctionType as _FunctionType, MethodType as _MethodType
import inspect as _inspect

from pybadger.badge import Badge
from pybadger.badger import Badger
from pybadger import shields, pepy, protocol

if _TYPE_CHECKING:
    from typing import Literal
    from pybadger.protocol import AttrDict


def create(
    platform: Literal["shields", "pepy"] = "shields",
    service: str = "generic",
    endpoint: str | None = None,
    args: dict | None = None,
    params_light: AttrDict = None,
    params_dark: AttrDict = None,
    attrs_img: AttrDict = None,
    attrs_a: AttrDict = None,
    attrs_picture: AttrDict = None,
    attrs_source_light: AttrDict = None,
    attrs_source_dark: AttrDict = None,
    attrs_span: AttrDict = None,
    attrs_div: AttrDict = None,
    default_light: bool = True,
    merge_params: bool = True,
    use_defaults: bool = True
) -> Badge:
    def get_kwargs(function):
        params = []
        required_params = []
        func_sig = _inspect.signature(function)
        for param_name, param in func_sig.parameters.items():
            params.append(param_name)
            if param.default is _inspect.Parameter.empty:
                required_params.append(param_name)
        for param in required_params:
            if param not in args:
                raise TypeError(f"Missing required parameter '{param}' for service '{service}', endpoint {endpoint}")
        return {param: args[param] for param in params if param in args}

    module = {"shields": shields, "pepy": pepy}[platform]
    try:
        func = getattr(module, service)
    except AttributeError:
        raise AttributeError(f"Service '{service}' not found in '{platform}'")
    if not isinstance(func, _FunctionType):
        raise TypeError(f"Service '{service}' is not callable")
    args = args or {}
    func_val = func(**get_kwargs(func))
    if not endpoint:
        if not isinstance(func_val, Badge):
            raise TypeError("Returned value is not a badge")
        badge = func_val
    else:
        try:
            endpoint_func = getattr(func_val, endpoint)
        except AttributeError:
            raise AttributeError(f"Endpoint '{endpoint}' not found in returned value")
        if not isinstance(endpoint_func, _MethodType):
            raise TypeError(f"Endpoint '{endpoint}' is not callable")
        badge = endpoint_func(**get_kwargs(endpoint_func))
    if not use_defaults:
        badge.unset_all()
    badge.default_light = default_light
    badge.merge_params = merge_params

    badge.set(
        params_light=params_light,
        params_dark=params_dark,
        attrs_img=attrs_img,
        attrs_a=attrs_a,
        attrs_picture=attrs_picture,
        attrs_source_light=attrs_source_light,
        attrs_source_dark=attrs_source_dark,
        attrs_span=attrs_span,
        attrs_div=attrs_div
    )
    return badge
