"""Vendored from xarray
https://github.com/pydata/xarray/blob/f4e0523be0ce8babaa8eff38365e5308b1fdb76b/xarray/core/formatting_html.py
"""

from __future__ import annotations

import uuid
from functools import partial
from html import escape
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

from xarray.core.options import _get_boolean_with_default

from fused_batch._formatter.common import format_number, icon, load_static_files
from fused_batch._formatter.formatter_dataset import tables_section
from fused_batch._options import options as OPTIONS

if TYPE_CHECKING:
    from fused_batch._project import Project


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


def summarize_folder(
    folder_name: str,
    folder: Project,
    *,
    is_index: bool = False,
):
    cssclass_idx = " class='xr-has-index'" if is_index else ""

    tables_folders_str = f"tables:{format_number(len(folder.tables))} folders:{format_number(len(folder.folders))}"

    # "unique" ids required to expand/collapse subsections
    attrs_id = "attrs-" + str(uuid.uuid4())
    data_id = "data-" + str(uuid.uuid4())
    chunk_repr_disabled = "disabled" if True else ""

    attrs_ul = f"""
    <ul style="margin-top: 0; margin-bottom: 0px;">
    {fused_project_repr(folder)}
    </ul>
    """
    data_repr = ""

    attrs_icon = icon("icon-file-text2")
    code_icon = icon("icon-code")

    return (
        f"<div class='xr-var-name'><span{cssclass_idx}>{folder_name}</span></div>"
        f"<div class='xr-var-dims'>{tables_folders_str}</div>"
        f"<div class='xr-var-dtype'></div>"
        f"<div class='xr-var-preview xr-preview'></div>"
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


def summarize_folders(folders: Dict[str, Project]):
    li_items = []
    for folder_name, folder in folders.items():
        li_content = summarize_folder(
            folder_name=folder_name,
            folder=folder,
            is_index=False,
        )
        li_items.append(f"<li class='xr-var-item'>{li_content}</li>")

    vars_li = "".join(li_items)

    return f"<ul class='xr-var-list'>{vars_li}</ul>"


folder_section = partial(
    _mapping_section,
    name="Folders",
    details_func=summarize_folders,
    max_items_collapse=25,
    expand_option_name="display_expand_coords",
)


def summarize_virtual_folders(folders: List[str]):
    li_items = []

    attrs_icon = icon("icon-file-text2")
    code_icon = icon("icon-code")

    for folder_name in folders:
        li_content = (
            f"<div class='xr-var-name'><span>{folder_name}</span></div>"
            f"<div class='xr-var-dims'></div>"
            f"<div class='xr-var-dtype'></div>"
            f"<div class='xr-var-preview xr-preview'></div>"
            f"<input class='xr-var-attrs-in' type='checkbox' disabled>"
            f"<label title='Show/Hide attributes'>"
            f"{attrs_icon}</label>"
            f"<input class='xr-var-data-in' type='checkbox' disabled>"
            f"<label title='Show/Hide data repr'>"
            f"{code_icon}</label>"
            f"<div class='xr-var-attrs'></div>"
            f"<div class='xr-var-data'></div>"
        )
        li_items.append(f"<li class='xr-var-item'>{li_content}</li>")

    vars_li = "".join(li_items)

    return f"<ul class='xr-var-list'>{vars_li}</ul>"


virtual_folder_section = partial(
    _mapping_section,
    name="Virtual Folders",
    details_func=summarize_virtual_folders,
    max_items_collapse=25,
    expand_option_name="display_expand_coords",
)


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


def fused_project_repr(
    project: Project,
) -> str:
    obj_type = f"fused_batch.Project: {project.base_path}"
    header_components = [f"<div class='xr-obj-type'>{escape(obj_type)}</div>"]

    if OPTIONS.show.materialize_virtual_folders:
        project._materialize_all_virtual_folders()

    sections: List[str] = []

    if project.tables:
        sections.append(tables_section(project.tables))
    if project.folders:
        sections.append(folder_section(project.folders))
    if project.virtual_folders:
        sections.append(virtual_folder_section(project.virtual_folders))

    if not sections:
        # There is nothing whatsoever in the project (totally empty).
        # Display something so it's clear there's 0 items.
        # This can occur if the user opens a project in lazy mode or
        # using a path that doesn't exist.
        sections.append(tables_section({}))

    return _obj_repr(project, header_components, sections)
