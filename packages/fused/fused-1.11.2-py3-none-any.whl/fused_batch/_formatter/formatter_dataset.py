"""Vendored from xarray
https://github.com/pydata/xarray/blob/f4e0523be0ce8babaa8eff38365e5308b1fdb76b/xarray/core/formatting_html.py
"""

from __future__ import annotations

import uuid
import warnings
from functools import partial
from html import escape
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

import numpy as np
from xarray.core.formatting import short_data_repr
from xarray.core.options import _get_boolean_with_default

from fused_batch._formatter.common import (
    copyable_text,
    format_number,
    icon,
    load_static_files,
)
from fused_batch._formatter.noraise import noraise

if TYPE_CHECKING:
    from fused_batch.models.api import Dataset
    from fused_batch.models.api.dataset import Table


def short_data_repr_html(array):
    """Format "data" for DataArray and Variable."""
    internal_data = getattr(array, "variable", array)._data
    if hasattr(internal_data, "_repr_html_"):
        return internal_data._repr_html_()
    text = escape(short_data_repr(array))
    return f"<pre>{text}</pre>"


def format_dims(dims, dims_with_index):
    if not dims:
        return ""

    dim_css_map = {
        dim: " class='xr-has-index'" if dim in dims_with_index else "" for dim in dims
    }

    dims_li = "".join(
        f"<li><span{dim_css_map[dim]}>" f"{escape(str(dim))}</span>: {size}</li>"
        for dim, size in dims.items()
    )

    return f"<ul class='xr-dim-list'>{dims_li}</ul>"


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


def table_totals(table: Table):
    # TODO: maybe make this a method on the dataset?
    total_bounds = [np.inf, np.inf, -np.inf, -np.inf]

    sum_area = 0.0
    sum_length = 0.0
    sum_area_utm = 0.0
    sum_length_utm = 0.0
    sum_num_coords = 0
    sum_num_rows = 0

    if table.chunk_metadata:
        for meta in table.chunk_metadata:
            sum_area += meta.sum_area
            sum_length += meta.sum_length

            if meta.sum_area_utm is not None:
                sum_area_utm += meta.sum_area_utm

            if meta.sum_length_utm is not None:
                sum_length_utm += meta.sum_length_utm

            sum_num_coords += meta.num_coords
            sum_num_rows += meta.num_rows

            if meta.bbox_minx < total_bounds[0]:
                total_bounds[0] = meta.bbox_minx

            if meta.bbox_miny < total_bounds[1]:
                total_bounds[1] = meta.bbox_miny

            if meta.bbox_maxx > total_bounds[2]:
                total_bounds[2] = meta.bbox_maxx

            if meta.bbox_maxy > total_bounds[3]:
                total_bounds[3] = meta.bbox_maxy

    return (
        sum_area,
        sum_length,
        sum_area_utm,
        sum_length_utm,
        sum_num_coords,
        sum_num_rows,
        total_bounds,
    )


@noraise(incompat_version_message="Table formatting failed", default="")
def summarize_table(
    table_name: str,
    table: Optional[Table],
    *,
    is_index: bool = False,
    dtype=None,
):
    cssclass_idx = " class='xr-has-index'" if is_index else ""
    name = escape(str(table_name))
    if table is None:
        return (
            f"<div class='xr-var-name'><span{cssclass_idx}>{name}</span></div>"
            f"<div class='xr-var-dims'></div>"
            f"<div class='xr-var-dtype'></div>"
            f"<div class='xr-var-preview xr-preview'></div>"
            f"<div class='xr-var-attrs'></div>"
            f"<div class='xr-var-data'></div>"
        )
    dims_str = f"files:{format_number(table.num_files)}, chunks:{format_number(table.num_chunks)}"
    dtype = f"rows:{format_number(table.num_rows)}"

    # "unique" ids required to expand/collapse subsections
    attrs_id = "attrs-" + str(uuid.uuid4())
    data_id = "data-" + str(uuid.uuid4())
    chunk_repr_disabled = "disabled" if table.sample is None else ""

    # Convert DataFrame to HTML table
    # TODO: escape html characters # escape(inline_variable_array_repr(variable, 35))
    preview = f"[{', '.join(table.column_names)}]"

    def get_parent_inputs(table: Table):
        s = []

        if table.parent is None:
            return ""

        inputs = table.parent.inputs
        if len(inputs) == 1:
            if isinstance(inputs[0], list):
                if len(inputs[0]) < 6:
                    for input in inputs:
                        s.append(f"<li>Input: <code>{input}</code></li>")
                else:
                    n_more = len(inputs[0]) - 4
                    s.append(f"<li>Input: <code>{inputs[0][0]}</code></li>")
                    s.append(f"<li>Input: <code>{inputs[0][1]}</code></li>")
                    s.append(f"<li>... {n_more} more ...</li>")
                    s.append(f"<li>Input: <code>{inputs[0][-2]}</code></li>")
                    s.append(f"<li>Input: <code>{inputs[0][-1]}</code></li>")
            else:
                s.append(
                    f"<li>Input: <code>{dataset_to_url(table.parent.inputs[0])}</code></li>"
                )
        else:
            s.append(f"<li>Left Input: <code>{dataset_to_url(inputs[0])}</code></li>")
            s.append(f"<li>Right Input: <code>{dataset_to_url(inputs[1])}</code></li>")
        return "".join(s)
        # def dataset_to_name(inputs[0]):

    def dataset_to_url(dataset):
        if dataset is None:
            return None
        elif isinstance(dataset, str):
            return dataset
        elif dataset.type == "v2":  # DatasetInputType.V2
            return [str(t.url) for t in dataset.tables]
        else:
            return repr(dataset)

    if table.table_schema.fields:
        table_schema = [
            f"<li><code>{field.name}</code>: {field.type}</li>"
            for field in table.table_schema.fields
        ]
    else:
        # If we don't have the schema information, we can at least show the column names
        table_schema = [f"<li><code>{col}</code></li>" for col in table.column_names]

    def get_parent_copy(table: Table):
        if table.parent:
            copyable = copyable_text(
                f"fused_batch.experimental.job({repr(table.parent.job.model_dump_json())}, content_type='json')",
                show_text=False,
            )
            return f"<li>Copy job configuration as Python {copyable}</li>"
        else:
            return ""

    def parent_udf(table: Table):
        if table.parent and "udf" in table.parent.job.model_dump():
            return f"""<li>UDF name: <code>{table.parent.job.udf.name}</code></li>
                <li>Lines of code: {format_number(len(table.parent.job.udf.code.splitlines()))}</li>"""
        else:
            return "<li>There is no UDF.</li>"

    def get_parent_exec(table: Table):
        result = ""
        if table.parent and table.parent.time_taken:
            result += f"<li>Time taken (seconds): <code>{table.parent.time_taken:.2f}</code></li>"
        if table.parent and table.parent.job_id:
            result += f"<li>Job ID: {copyable_text(table.parent.job_id)}</li>"
        return result

    def get_parent_type(table: Table) -> str:
        if table.parent:
            return f"Parent: {table.parent.job.type}"
        else:
            return "Parent"

    attrs_ul = f"""
    <h4 style="margin-left: 20px;">Table Schema</h4>
    <ul style="margin-top: 0; margin-bottom: 0px;">
    {''.join(table_schema)}
    </ul>
    <h4 style="margin-left: 20px;">{get_parent_type(table)}</h4>
    <ul style="margin-top: 0; margin-bottom: 0px;">
    {get_parent_exec(table)}
    {get_parent_inputs(table)}
    {get_parent_copy(table)}
    </ul>
    <h4 style="margin-left: 20px;">UDF</h4>
    <ul style="margin-top: 0; margin-bottom: 0px;">
    {parent_udf(table)}
    </ul>
     """  # summarize_attrs(var.attrs)
    # {table.parent.udf_code}

    if hasattr(table, "sample") and table.sample is not None:
        sample = table.sample.copy()
        if "geometry" in sample.columns:
            with warnings.catch_warnings():
                # Ignore "Geometry column does not contain geometry."
                # Because we're converting the geometry column to a string
                warnings.filterwarnings(
                    action="ignore", message="Geometry column does not contain geometry"
                )
                sample["geometry"] = sample.geometry.map(lambda x: str(x)[:25] + "...")
        html_table = sample.to_html()
        data_repr = f'<div align="center" style="overflow-x:auto;">{html_table}</div>'
    else:
        data_repr = ""

    attrs_icon = icon("icon-file-text2")
    data_icon = icon("icon-database")

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
        f"{data_icon}</label>"
        f"<div class='xr-var-attrs'>{attrs_ul}</div>"
        f"<div class='xr-var-data'>{data_repr}</div>"
    )


def summarize_tables(tables: Dict[str, Table]):
    li_items = []
    for table_name, table in tables.items():
        li_content = summarize_table(table_name, table, is_index=False)
        li_items.append(f"<li class='xr-var-item'>{li_content}</li>")

    vars_li = "".join(li_items)

    return f"<ul class='xr-var-list'>{vars_li}</ul>"


tables_section = partial(
    _mapping_section,
    name="Tables",
    details_func=summarize_tables,
    max_items_collapse=25,
    expand_option_name="display_expand_coords",
)


@noraise(incompat_version_message="Geometry formatting failed", default="")
def geometry_section(dataset: Dataset):
    geometry_table_name = "main" if "main" in dataset.tables else None
    if geometry_table_name is None and dataset.tables:
        geometry_table_name = sorted(dataset.tables.keys())[0]

    table = dataset.tables.get(geometry_table_name)
    return geometry_section_table(table)


@noraise(incompat_version_message="Geometry table formatting failed", default="")
def status_section_table(table: Table) -> str:
    if table.status:
        return collapsible_section(
            "Status",
            inline_details=f"""<span style="background-color: red;">{table.status}</span><br>Please check that the table exists.""",
            enabled=False,
            collapsed=True,
        )
    elif table.chunk_metadata is None:
        how_much_meta = "No" if table.num_files == 0 else "Minimal"
        return collapsible_section(
            "Status",
            inline_details=f"{how_much_meta} metadata loaded -- call <code>refresh()</code>",
            enabled=False,
            collapsed=True,
        )


@noraise(incompat_version_message="Geometry table formatting failed", default="")
def geometry_section_table(table: Optional[Table] = None):
    if table is not None:
        (
            sum_area,
            sum_length,
            sum_area_utm,
            sum_length_utm,
            sum_num_coords,
            sum_num_rows,
            total_bounds,
        ) = table_totals(table)

        return collapsible_section(
            "Geometry",
            inline_details=f"files:{format_number(table.num_files)}, chunks:{format_number(table.num_chunks)}, rows:{format_number(sum_num_rows)}, area: {sum_area_utm:.2E} m<sup>2</sup> length:{sum_length_utm:.2E} m <div>bbox=({total_bounds[0]:.6f}, {total_bounds[1]:.6f}, {total_bounds[2]:.6f}, {total_bounds[3]:.6f})</div>",
            enabled=False,
            collapsed=True,
        )
    else:
        return collapsible_section(
            "Geometry",
            inline_details="",
            enabled=False,
            collapsed=False,
        )


def fused_dataset_repr(dataset: Dataset) -> str:
    obj_type = f"fused_batch.Dataset: {dataset.base_path}"
    header_components = [f"<div class='xr-obj-type'>{escape(obj_type)}</div>"]

    sections: List[str] = [
        geometry_section(dataset),
        tables_section(dataset.tables),
    ]

    return _obj_repr(dataset, header_components, sections)


def fused_table_repr(table: Table) -> str:
    obj_type = f"fused_batch.Table: {table.name}"
    header_components = [f"<div class='xr-obj-type'>{escape(obj_type)}</div>"]

    sections: List[str] = [
        geometry_section_table(table),
        tables_section({table.name: table}),
    ]

    if table.status or table.chunk_metadata is None:
        sections.insert(0, status_section_table(table))

    return _obj_repr(table, header_components, sections)
