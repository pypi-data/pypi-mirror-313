"""Vendored from xarray
https://github.com/pydata/xarray/blob/f4e0523be0ce8babaa8eff38365e5308b1fdb76b/xarray/core/formatting_html.py
"""

from __future__ import annotations

import json
import uuid
from functools import partial
from html import escape
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Sequence, Union

from pydantic import BaseModel
from xarray.core.formatting import short_data_repr
from xarray.core.options import _get_boolean_with_default

from fused_batch._formatter.common import copyable_text, icon, load_static_files
from fused_batch._formatter.udf import udf_section

if TYPE_CHECKING:
    from fused_batch.models.api import (
        JobConfig,
        JobStepConfig,
        JoinJobStepConfig,
        JoinSinglefileJobStepConfig,
        MapJobStepConfig,
        PartitionJobStepConfig,
        UdfJobStepConfig,
    )
    from fused_batch.models.internal import (
        AnyDatasetInput,
        AnyDatasetOutput,
        DatasetInput,
        DatasetInputV2,
        DatasetInputV2Table,
    )
    from fused_batch.models.udf import AnyBaseUdf


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
    **kwargs,
):
    n_items = len(mapping)
    expanded = _get_boolean_with_default(
        expand_option_name, n_items < max_items_collapse
    )
    collapsed = not expanded

    return collapsible_section(
        name,
        details=details_func(mapping, **kwargs),
        n_items=n_items,
        enabled=enabled,
        collapsed=collapsed,
    )


def _obj_repr(obj, header_components, sections, sections_class="xr-sections"):
    """Return HTML repr of an xarray object.

    If CSS is not injected (untrusted notebook), fallback to the plain text repr.

    """
    header = f"<div class='xr-header'>{''.join(h for h in header_components)}</div>"
    sections = "".join(
        f"<li class='xr-section-item'>{s}</li>" for s in sections if s is not None
    )

    icons_svg, css_style = load_static_files()
    return (
        "<div>"
        f"{icons_svg}<style>{css_style}</style>"
        f"<pre class='xr-text-repr-fallback'>{escape(repr(obj))}</pre>"
        "<div class='xr-wrap' style='display:none'>"
        f"{header}"
        f"<ul class='{sections_class}'>{sections}</ul>"
        "</div>"
        "</div>"
    )


def get_dataset_input_settings(input: AnyDatasetInput) -> str:
    results = ""
    for key, value in input.model_dump().items():
        if key == "tables":
            continue
        results += f"<li>{key}: <code>{value}</code></li>"
    return results


def _format_v2_table(table: DatasetInputV2Table) -> str:
    read_sidecar_files = " (w/ sidecar)" if table.read_sidecar_files else ""
    cache_locally = "(cache locally)" if table.cache_locally else ""
    return f"<code>{str(table.url)}</code>{read_sidecar_files}{cache_locally}"


def summarize_input(
    input_name: str,
    input: Union[str, DatasetInput],
    *,
    is_index: bool = False,
    dtype=None,
):
    is_dataset_input = not isinstance(input, str)
    cssclass_idx = " class='xr-has-index'" if is_index else ""
    dims_str = f"tables:{len(input.tables)}" if is_dataset_input else ""
    name = escape(str(input_name))
    dtype = ""

    # "unique" ids required to expand/collapse subsections
    attrs_id = "attrs-" + str(uuid.uuid4())

    # Convert DataFrame to HTML table
    # TODO: escape html characters # escape(inline_variable_array_repr(variable, 35))
    preview = f"[{', '.join(input.tables)}]" if is_dataset_input else ""

    attrs_ul = f"""
    <h4 style="margin-left: 20px;">Inputs</h4>
    <ul style="margin-top: 0; margin-bottom: 0px;">
    {''.join([f'<li><code>{t}</code></li>' for t in input.tables]) if is_dataset_input else f'<li>{input}</li>'}
    </ul>
    """
    if is_dataset_input:
        attrs_ul += f"""
            <h4 style="margin-left: 20px;">Settings</h4>
            <ul style="margin-top: 0; margin-bottom: 0px;">
            {get_dataset_input_settings(input)}
            </ul>
            """

    attrs_icon = icon("icon-file-text2")

    return (
        f"<div class='xr-var-name'><span{cssclass_idx}>{name}</span></div>"
        f"<div class='xr-var-dims'>{dims_str}</div>"
        f"<div class='xr-var-dtype'>{dtype}</div>"
        f"<div class='xr-var-preview xr-preview'>{preview}</div>"
        f"<input id='{attrs_id}' class='xr-var-attrs-in' "
        f"type='checkbox'>"
        f"<label for='{attrs_id}' title='Show/Hide attributes'>"
        f"{attrs_icon}</label>"
        f"<label></label>"
        f"<div class='xr-var-attrs'>{attrs_ul}</div>"
    )


def summarize_input_v2(
    input_name: str,
    input: DatasetInputV2,
    *,
    is_index: bool = False,
    dtype=None,
):
    cssclass_idx = " class='xr-has-index'" if is_index else ""
    dims_str = f"tables:{len(input.tables)}"
    name = escape(str(input_name))
    dtype = f"{input.operation.value}" if input.operation else "?"

    attrs_id = "attrs-" + str(uuid.uuid4())

    # TODO: escape html characters # escape(inline_variable_array_repr(variable, 35))
    preview = f"[{', '.join([t.url for t in input.tables])}]"

    attrs_ul = f"""
    <h4 style="margin-left: 20px;">Inputs</h4>
    <ul style="margin-top: 0; margin-bottom: 0px;">
    {''.join([f'<li>{_format_v2_table(t)}</li>' for t in input.tables])}
    </ul>
    """
    attrs_ul += f"""
        <h4 style="margin-left: 20px;">Settings</h4>
        <ul style="margin-top: 0; margin-bottom: 0px;">
        {get_dataset_input_settings(input)}
        </ul>
        """

    attrs_icon = icon("icon-file-text2")

    return (
        f"<div class='xr-var-name'><span{cssclass_idx}>{name}</span></div>"
        f"<div class='xr-var-dims'>{dims_str}</div>"
        f"<div class='xr-var-dtype'>{dtype}</div>"
        f"<div class='xr-var-preview xr-preview'>{preview}</div>"
        f"<input id='{attrs_id}' class='xr-var-attrs-in' "
        f"type='checkbox'>"
        f"<label for='{attrs_id}' title='Show/Hide attributes'>"
        f"{attrs_icon}</label>"
        f"<label></label>"
        f"<div class='xr-var-attrs'>{attrs_ul}</div>"
    )


def summarize_output(
    output_name: str,
    output: AnyDatasetOutput,
    *,
    is_index: bool = False,
    dtype=None,
):
    cssclass_idx = " class='xr-has-index'" if is_index else ""
    dims_str = ""
    name = escape(str(output_name))
    dtype = ""

    attrs_id = "attrs-" + str(uuid.uuid4())

    if hasattr(output, "url"):  # v2
        preview = f"{output.url}" if output.url else ""
    else:
        preview = repr(output)

    def get_dataset_output_settings(output: AnyDatasetOutput) -> str:
        results = ""
        for key, value in output.model_dump().items():
            results += f"<li>{key}: <code>{value}</code></li>"
        return results

    attrs_ul = f"""
        <h4 style="margin-left: 20px;">Settings</h4>
        <ul style="margin-top: 0; margin-bottom: 0px;">
        {get_dataset_output_settings(output)}
        </ul>
        """

    attrs_icon = icon("icon-file-text2")

    return (
        f"<div class='xr-var-name'><span{cssclass_idx}>{name}</span></div>"
        f"<div class='xr-var-dims'>{dims_str}</div>"
        f"<div class='xr-var-dtype'>{dtype}</div>"
        f"<div class='xr-var-preview xr-preview'>{preview}</div>"
        f"<input id='{attrs_id}' class='xr-var-attrs-in' "
        f"type='checkbox'>"
        f"<label for='{attrs_id}' title='Show/Hide attributes'>"
        f"{attrs_icon}</label>"
        f"<label></label>"
        f"<div class='xr-var-attrs'>{attrs_ul}</div>"
    )


def summarize_ingest_input(
    input: str,
    *,
    is_index: bool = False,
):
    cssclass_idx = " class='xr-has-index'" if is_index else ""
    name = escape(str(input))

    return (
        f'<div class="xr-var-name" style="grid-column: 1 / -2;"><span{cssclass_idx}>{name}</span></div>'
        f"{copyable_text(name, show_text=False)}"
    )


def summarize_inputs(
    inputs: List[Union[str, AnyDatasetInput]],
    names: Sequence[str] = ("input",),
):
    li_items = []
    if len(names) < len(inputs):
        names = ["input"] * len(inputs)

    for name, input in zip(names, inputs):
        if not isinstance(input, str) and input.type == "v2":  # DatasetInputType.V2
            # v2
            li_content = summarize_input_v2(name, input, is_index=False)
            li_items.append(f"<li class='xr-var-item'>{li_content}</li>")
        else:
            # v1 or string
            li_content = summarize_input(name, input, is_index=False)
            li_items.append(f"<li class='xr-var-item'>{li_content}</li>")

    vars_li = "".join(li_items)

    return f"<ul class='xr-var-list'>{vars_li}</ul>"


def summarize_ingest_inputs(inputs: List[str]):
    li_items = []
    for input in inputs:
        li_content = summarize_ingest_input(input, is_index=False)
        li_items.append(f"<li class='xr-var-item'>{li_content}</li>")

    vars_li = "".join(li_items)

    return f'<ul class="xr-var-list">{vars_li}</ul>'


def summarize_outputs(outputs: List[AnyDatasetOutput]):
    li_items = []
    for output in outputs:
        output_name = output.table if output.table else "(not set)"

        li_content = summarize_output(output_name, output, is_index=False)
        li_items.append(f"<li class='xr-var-item'>{li_content}</li>")

    vars_li = "".join(li_items)

    return f"<ul class='xr-var-list'>{vars_li}</ul>"


inputs_section = partial(
    _mapping_section,
    name="Inputs",
    details_func=summarize_inputs,
    max_items_collapse=25,
    expand_option_name="display_expand_coords",
)

ingest_inputs_section = partial(
    _mapping_section,
    name="Inputs",
    details_func=summarize_ingest_inputs,
    max_items_collapse=25,
    expand_option_name="display_expand_coords",
)

output_section = partial(
    _mapping_section,
    name="Outputs",
    details_func=summarize_outputs,
    max_items_collapse=25,
    expand_option_name="display_expand_coords",
)


def get_object_settings(obj: BaseModel, exclude: Sequence[str] = ()) -> str:
    def _format_kv(key: str, val: Any) -> str:
        if key in exclude:
            return ""
        return f"<li>{key}: <code>{val}</code></li>"

    return f"<ul>{''.join([_format_kv(key, val) for key, val in obj.model_dump().items()])}</ul>"


def _collect_udfs(
    config: JobStepConfig, *, names: Sequence[str] = ("udf",)
) -> Dict[str, AnyBaseUdf]:
    results = {}
    for udf_name in names:
        if hasattr(config, udf_name):
            udf_attr = getattr(config, udf_name)
            if udf_attr is not None:
                results[udf_attr.name] = udf_attr
    return results


def fused_ingestion_repr(ingest: PartitionJobStepConfig) -> str:
    obj_type = f"fused_batch.{ingest.__class__.__name__}: {ingest.name or ingest.output or ingest.output_metadata}"
    header_components = [
        f"<div class='xr-obj-type'>{escape(obj_type)}</div>",
        get_object_settings(ingest, exclude=["input", "type"]),
    ]

    inputs = ingest.input if isinstance(ingest.input, list) else [ingest.input]

    sections: List[str] = [
        ingest_inputs_section(inputs),
    ]

    return _obj_repr(ingest, header_components, sections)


def fused_udf_step_repr(step: UdfJobStepConfig) -> str:
    name = step.name
    if not name and step.udf is not None:
        name = step.udf.name
    obj_type = f"fused_batch.{step.__class__.__name__}: {name}"
    header_components = [
        f"<div class='xr-obj-type'>{escape(obj_type)}</div>",
        get_object_settings(step, exclude=["input", "udf", "type"]),
    ]

    inputs = [json.dumps(i) for i in step.input] if step.input is not None else []
    udfs = _collect_udfs(step)

    sections: List[str] = [
        ingest_inputs_section(inputs) if step.input is not None else None,
        udf_section(udfs),
    ]

    return _obj_repr(step, header_components, sections)


def fused_map_repr(map: MapJobStepConfig) -> str:
    output_name = map.output.url if hasattr(map.output, "url") else None
    obj_type = f"fused_batch.{map.__class__.__name__}: {map.name or output_name}"
    header_components = [
        f"<div class='xr-obj-type'>{escape(obj_type)}</div>",
        get_object_settings(map, exclude=["input", "output", "udf", "type"]),
    ]

    inputs = [map.input]
    outputs = [map.output]
    udfs = _collect_udfs(map)

    sections: List[str] = [
        inputs_section(inputs),
        output_section(outputs),
        udf_section(udfs),
    ]

    return _obj_repr(map, header_components, sections)


def fused_join_repr(join: JoinJobStepConfig) -> str:
    output_name = join.output.url if hasattr(join.output, "url") else None
    obj_type = f"fused_batch.{join.__class__.__name__}: {join.name or output_name}"
    header_components = [
        f"<div class='xr-obj-type'>{escape(obj_type)}</div>",
        get_object_settings(
            join,
            exclude=[
                "input_left",
                "input_right",
                "output",
                "udf",
                "type",
            ],
        ),
    ]

    inputs = [join.input_left, join.input_right]
    outputs = [join.output]
    udfs = _collect_udfs(join)

    sections: List[str] = [
        inputs_section(inputs, names=["left", "right"]),
        output_section(outputs),
        udf_section(udfs),
    ]

    return _obj_repr(join, header_components, sections)


def fused_join_singlefile_repr(join: JoinSinglefileJobStepConfig) -> str:
    output_name = join.output.url if hasattr(join.output, "url") else None
    obj_type = f"fused_batch.{join.__class__.__name__}: {join.name or output_name}"
    header_components = [
        f"<div class='xr-obj-type'>{escape(obj_type)}</div>",
        get_object_settings(
            join,
            exclude=[
                "input_left",
                "input_right",
                "output",
                "udf",
                "experimental_read_udf",
                "type",
            ],
        ),
    ]

    inputs = [join.input_left, join.input_right]
    outputs = [join.output]
    udfs = _collect_udfs(join, names=["experimental_read_udf", "udf"])

    sections: List[str] = [
        inputs_section(inputs, names=["left", "right"]),
        output_section(outputs),
        udf_section(udfs),
    ]

    return _obj_repr(join, header_components, sections)


def _get_job_repr(i: int, step: JobStepConfig) -> str:
    if hasattr(step, "_repr_html_"):
        html = step._repr_html_()
    else:
        html = repr(step)
    return f'<li><h4>Step {i}</h4><div style="padding-left: 2em;">{html}</div></li>'


def fused_job_repr(job: JobConfig) -> str:
    return f"""
    <div class='xr-obj-type'>fused.JobConfig: {job.name}</div>
    <ul>
    {''.join([_get_job_repr(step_idx, step) for step_idx, step in enumerate(job.steps)])}
    </ul>
    """
