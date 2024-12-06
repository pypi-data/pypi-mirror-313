from __future__ import annotations
from pathlib import Path as _Path
import pylinks as _pylinks

import pybadger
from pybadger.protocol import AttrDict as _AttrDict


class Badge(pybadger.Badge):
    """Shields.IO Badge."""

    def _generate_full_url(
        self,
        url: _pylinks.url.URL,
        params: _AttrDict,
    ) -> _pylinks.url.URL:

        def snake_to_camel(string):
            components = string.split('_')
            return ''.join([components[0]] + [x.title() for x in components[1:]])

        def process_logo(logo) -> str | None:
            if not logo:
                return
            logo = str(logo)
            logo_type = params.get("logo_type")
            logo_media_type = params.get("logo_media_type")
            if not logo_type:
                if logo.startswith("data:"):
                    logo_type = "data"
                elif logo.startswith(("http://", "https://")):
                    logo_type = "url"
                elif _Path(logo).exists():
                    logo_type = "file"
                else:
                    logo_type = "name"
            if logo_type in ("data", "name"):
                return logo
            if logo_media_type:
                logo_media_type = _pylinks.media_type.parse(f"image/{logo_media_type}")
            data_uri = _pylinks.uri.data.create_from_path(
                path_type=logo_type,
                path=logo,
                media_type=logo_media_type,
                guess_media_type=True,
                base64=True,
            )
            return str(data_uri)

        for param, param_processor in (
            ("label", None),
            ("style", None),
            ("color", None),
            ("label_color", None),
            ("logo_color", None),
            ("logo_width", None),
            ("logo_size", None),
            ("logo", process_logo),
            ("cache_seconds", None),
        ):
            if param in params:
                shields_param_name = snake_to_camel(param)
                value = params[param]
                value_processed = param_processor(value) if param_processor else value
                if value_processed is not None:
                    url.queries[shields_param_name] = value_processed
        return url
