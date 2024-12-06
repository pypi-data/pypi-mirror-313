from typing import Any
from htmlmin import minify


def compress_html(html: str, **kwargs: Any) -> str:
    return minify(html, **kwargs)
