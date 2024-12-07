"""Vendored from xarray
https://github.com/pydata/xarray/blob/f4e0523be0ce8babaa8eff38365e5308b1fdb76b/xarray/core/formatting_html.py
"""

from __future__ import annotations

from html import escape
from typing import TYPE_CHECKING, Dict, List, Tuple

from jinja2 import BaseLoader

from fused_batch._formatter.common import load_static_files
from fused_batch._formatter.template import template_section

if TYPE_CHECKING:
    from fused_batch._templates import FusedTemplate


def _obj_repr(obj, header_components, sections):
    """Return HTML repr of an xarray object.

    If CSS is not injected (untrusted notebook), fallback to the plain text repr.

    """
    header = f"<div class='xr-header'>{''.join(h for h in header_components)}</div>"
    sections = "".join(f"<li class='xr-section-item'>{s}</li>" for s in sections)

    icons_svg, css_style = load_static_files()
    return (
        "<div>"
        f"{icons_svg}<style>{css_style}</style>"
        f"<pre class='xr-text-repr-fallback'>{escape(repr(obj))}</pre>"
        "<div class='xr-wrap' style='display:none'>"
        f"{header}"
        f"<ul class='xr-sections'>{sections}</ul>"
        "</div>"
        "</div>"
    )


def fused_templates_repr(
    name: str, templates: Dict[str, Tuple[FusedTemplate, BaseLoader]]
) -> str:
    obj_type = f"fused_batch.templates.{name}"
    header_components = [f"<div class='xr-obj-type'>{escape(obj_type)}</div>"]

    sections: List[str] = [
        template_section(templates),
    ]
    return _obj_repr(templates, header_components, sections)


def fused_template_repr(template: FusedTemplate) -> str:
    obj_type = f"fused_batch.templates.{template.__class__.__name__}: {template.name}"
    header_components = [f"<div class='xr-obj-type'>{escape(obj_type)}</div>"]

    templates = {template.name: (template, None)}

    sections: List[str] = [
        template_section(templates),
    ]
    return _obj_repr(templates, header_components, sections)
