import ast
from pathlib import Path
from typing import Optional

from fused_batch._str_utils import table_to_name

from ..internal import (
    DatasetInput,
    DatasetInputV2,
    DatasetInputV2Type,
    DatasetOutput,
    DatasetOutputV2,
)


def stringify_named_params(params):
    return [k + "=" + repr(v) for k, v in params.items()]


def structure_params(params, separator=", "):
    return separator.join([param for param in params])


def stringify_headers(headers):
    if not headers:
        return "[]"
    else:
        for header in headers:
            if hasattr(header, "source_file"):
                delattr(header, "source_file")
        return str(headers)


def stringify_input(input) -> str:
    if isinstance(input, str):
        return repr(input)
    elif isinstance(input, DatasetInputV2):
        op_fn: Optional[str] = None
        if input.operation == DatasetInputV2Type.ZIP:
            op_fn = "fused_batch.zip_tables"
        elif input.operation == DatasetInputV2Type.UNION:
            op_fn = "fused_batch.union_tables"

        any_has_sidecar = any([t.read_sidecar_files for t in input.tables])
        # TODO: cache locally

        if len(input.tables) == 1 and not any_has_sidecar:
            return repr(str(input.tables[0].url))
        elif op_fn:
            if any_has_sidecar:
                read_sidecar = repr(
                    [table_to_name(t) for t in input.tables if t.read_sidecar_files]
                )
                read_sidecar_fragment = f", read_sidecar={read_sidecar}"
            else:
                read_sidecar_fragment = ""
            return f"{op_fn}({repr([str(t.url) for t in input.tables])}{read_sidecar_fragment})"
    elif isinstance(input, DatasetInput):
        # Note this is rewriting from V1 to V2 style

        base_path = input.base_path.rstrip("/")

        if len(input.tables) == 1:
            return repr(f"{base_path}/{input.tables[0]}")

        return f"fused_batch.zip_tables([{', '.join([repr(f'{base_path}/{t}') for t in input.tables])}])"

    return repr(input)


def stringify_output(output) -> Optional[str]:
    if isinstance(output, DatasetOutputV2):
        return repr(output.url) if output.url is not None else None

    if isinstance(output, DatasetOutput):
        # It could be tricky to render a DatasetOutput, so special case the empty output
        if output.base_path is None and output.table is None:
            return None
        elif output.base_path is not None and output.table is not None:
            return repr(Path(output.base_path) / output.table)
        else:
            return repr(output.base_path or output.table)

    return repr(output)


def extract_parameters(src):
    # Parse the input string into an AST (Abstract Syntax Tree)
    parsed_ast = ast.parse(src)

    all_parameters = []
    named_parameters = {}

    # Find all function definitions in the AST
    function_defs = [
        node
        for node in ast.walk(parsed_ast)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    # Assume the first function is the target function
    target_function = function_defs[0]

    for arg in target_function.args.args:
        param_name = arg.arg
        # named_parameters[param_name] = None  # Initialize with None
        all_parameters.append(param_name)

    for keyword in target_function.args.kwonlyargs:
        param_name = keyword.arg
        # named_parameters[param_name] = None  # Initialize with None

    for param, default in zip(
        target_function.args.args[
            len(target_function.args.args) - len(target_function.args.defaults) :
        ],
        target_function.args.defaults,
    ):
        # Extract the default value if it's a string, number, or None
        # TODO: Handle more types
        if isinstance(
            default,
            (
                ast.Str,
                ast.Num,
                ast.NameConstant,
                ast.Tuple,
                ast.List,
                ast.Dict,
                ast.Set,
            ),
        ):
            named_parameters[param.arg] = ast.literal_eval(default)

    positional_parameters = [
        param for param in all_parameters if param not in named_parameters
    ]

    return positional_parameters, named_parameters
