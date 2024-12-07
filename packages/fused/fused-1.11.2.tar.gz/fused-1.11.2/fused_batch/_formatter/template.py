from __future__ import annotations

import uuid
from functools import partial
from html import escape
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Tuple

from jinja2 import BaseLoader, FileSystemLoader, PackageLoader
from xarray.core.options import _get_boolean_with_default

from fused_batch._formatter.common import icon
from fused_batch._templates.loaders import RegisteredLoader, UrlLoader

if TYPE_CHECKING:
    from fused_batch._templates import FusedTemplate


def collapsible_section(
    name,
    inline_details: str = "",
    details: str = "",
    n_items: Optional[int] = None,
    enabled: bool = True,
    collapsed: bool = False,
):
    # "unique" id to expand/collapse the section
    data_id = "section-" + str(uuid.uuid4())

    has_items = n_items is not None and n_items
    n_items_span = "" if n_items is None else f" <span>({n_items})</span>"
    enabled_str = "" if enabled and has_items else "disabled"
    collapsed_str = "" if collapsed or not has_items else "checked"
    tip = " title='Expand/collapse section'" if enabled else ""

    return (
        f"<input id='{data_id}' class='xr-section-summary-in' "
        f"type='checkbox' {enabled_str} {collapsed_str}>"
        f"<label for='{data_id}' class='xr-section-summary' {tip}>"
        f"{name}:{n_items_span}</label>"
        f"<div class='xr-section-inline-details'>{inline_details}</div>"
        f"<div class='xr-section-details'>{details}</div>"
    )


def _mapping_section(
    mapping,
    name: str,
    details_func: Callable[[Any], str],
    max_items_collapse,
    expand_option_name,
    enabled: bool = True,
):
    n_items = len(mapping)
    expanded = _get_boolean_with_default(
        expand_option_name, n_items < max_items_collapse
    )
    collapsed = not expanded

    return collapsible_section(
        name,
        details=details_func(mapping),
        n_items=n_items,
        enabled=enabled,
        collapsed=collapsed,
    )


def summarize_template(
    template_name: str,
    template: FusedTemplate,
    loader: Optional[BaseLoader] = None,
    *,
    is_index: bool = False,
    dtype=None,
):
    cssclass_idx = " class='xr-has-index'" if is_index else ""
    code_lines = template.source.splitlines()
    dims_str = f"LOCs:{len(code_lines)}"
    name = escape(str(template_name))
    dtype = ""

    # "unique" ids required to expand/collapse subsections
    attrs_id = "attrs-" + str(uuid.uuid4())
    data_id = "data-" + str(uuid.uuid4())
    chunk_repr_disabled = "disabled" if template.source is None else ""

    # Convert DataFrame to HTML udf
    # TODO: escape html characters # escape(inline_variable_array_repr(variable, 35))
    if isinstance(loader, FileSystemLoader):
        preview = f"files {loader.searchpath}"
    elif isinstance(loader, PackageLoader):
        preview = f"package {loader.package_name}"
    elif isinstance(loader, UrlLoader):
        preview = f"url {loader.url}"
    elif isinstance(loader, RegisteredLoader):
        preview = "registered"
    else:
        preview = "unknown source"
    defaults = [f"<li>{k}: <code>{v}</code></li>" for k, v in template.defaults.items()]

    # if isinstance(table.parent.inputs[0], fused.models.internal.dataset.DatasetInput):
    attrs_ul = f"""
    <h4 style="margin-left: 20px;">Defaults</h4>
    <ul style="margin-top: 0; margin-bottom: 0px;">
    {''.join(defaults)}
    </ul>
     """  # summarize_attrs(var.attrs)
    rendered_code = "\n".join(
        [f'<span class="fused-udf-body">{line}</span>' for line in code_lines]
    )
    data_repr = f"""<div class="fused-udf-body-wrapper"><pre class="fused-udf-body"><code>{rendered_code}</code></pre></div>"""
    # data_repr = f'<div align="center" style="overflow-x:auto;">123</div>'
    # else:
    #     data_repr = ""
    # data_repr = ""
    attrs_icon = icon("icon-file-text2")
    code_icon = icon("icon-code")

    return (
        f"<div class='xr-var-name'><span{cssclass_idx}>{name}</span></div>"
        f"<div class='xr-var-dims'>{dims_str}</div>"
        f"<div class='xr-var-dtype'>{dtype}</div>"
        f"<div class='xr-var-preview xr-preview'>{preview}</div>"
        f"<input id='{attrs_id}' class='xr-var-attrs-in' "
        f"type='checkbox'>"
        f"<label for='{attrs_id}' title='Show/Hide attributes'>"
        f"{attrs_icon}</label>"
        f"<input id='{data_id}' class='xr-var-data-in' type='checkbox' {chunk_repr_disabled}>"
        f"<label for='{data_id}' title='Show/Hide data repr'>"
        f"{code_icon}</label>"
        f"<div class='xr-var-attrs'>{attrs_ul}</div>"
        f"<div class='xr-var-data'>{data_repr}</div>"
    )


def summarize_templates(
    templates: Dict[str, Tuple[FusedTemplate, Optional[BaseLoader]]]
):
    li_items = []
    for template_name, template_and_loader in templates.items():
        template, loader = template_and_loader
        li_content = summarize_template(
            template_name=template_name,
            template=template,
            loader=loader,
            is_index=False,
        )
        li_items.append(f"<li class='xr-var-item'>{li_content}</li>")

    vars_li = "".join(li_items)

    return f"<ul class='xr-var-list'>{vars_li}</ul>"


template_section = partial(
    _mapping_section,
    name="Templates",
    details_func=summarize_templates,
    max_items_collapse=25,
    expand_option_name="display_expand_coords",
)
