import re
import sys
import warnings
from functools import partial
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    Dict,
    Literal,
    Optional,
    Union,
    overload,
)

if TYPE_CHECKING:
    import geopandas as gpd
    import pandas as pd
    import shapely
    import xarray as xr

from fused.models.udf._eval_result import UdfEvaluationResult
from fused.types import UdfRuntimeError
from fused.warnings import FusedIgnoredWarning

from .core import (
    run_file,
    run_file_async,
    run_shared_file,
    run_shared_file_async,
    run_shared_tile,
    run_shared_tile_async,
    run_tile,
    run_tile_async,
)
from .core._impl._realtime_ops_impl import default_run_engine
from .core._impl._reimports import GeoPandasUdfV2, UdfAccessToken, UdfJobStepConfig

ResultType = Union["xr.Dataset", "pd.DataFrame", "gpd.GeoDataFrame"]


OLD_TOKEN_REGEX = re.compile("^[a-f0-9]{64}$")


def _is_udf_token(maybe_token: str):
    if OLD_TOKEN_REGEX.match(maybe_token):
        return True
    return maybe_token.startswith("UDF_") or maybe_token.startswith("fsh_")


@overload
def run(
    email_or_udf_or_token: Union[
        str, None, UdfJobStepConfig, GeoPandasUdfV2, UdfAccessToken
    ],
    /,
    udf_name: Optional[str],
    *,
    udf: Optional[GeoPandasUdfV2],
    job_step: Optional[UdfJobStepConfig],
    token: Optional[str],
    udf_email: Optional[str],
    x: Optional[int],
    y: Optional[int],
    z: Optional[int],
    _lat: Optional[float],
    _lng: Optional[float],
    bbox: Union["gpd.GeoDataFrame", "shapely.Geometry", None],
    sync: bool = False,
    engine: Optional[Literal["realtime", "batch", "local"]],
    type: Optional[Literal["tile", "file"]],
    parameters: Optional[Dict[str, Any]] = None,
    **kw_parameters,
) -> Coroutine[ResultType, None, None]:
    ...


@overload
def run(
    email_or_udf_or_token: Union[str, None, UdfJobStepConfig, GeoPandasUdfV2],
    /,
    udf_name: Optional[str],
    *,
    udf: Optional[GeoPandasUdfV2],
    job_step: Optional[UdfJobStepConfig],
    token: Optional[str],
    udf_email: Optional[str],
    x: Optional[int],
    y: Optional[int],
    z: Optional[int],
    sync: bool,
    engine: Optional[Literal["realtime", "batch", "local"]],
    type: Optional[Literal["tile", "file"]],
    parameters: Optional[Dict[str, Any]] = None,
    **kw_parameters,
) -> ResultType:
    ...


def run(
    email_or_udf_or_token: Union[
        str, None, UdfJobStepConfig, GeoPandasUdfV2, UdfAccessToken
    ] = None,
    /,
    udf_name: Optional[str] = None,
    *,
    udf: Optional[GeoPandasUdfV2] = None,
    job_step: Optional[UdfJobStepConfig] = None,
    token: Optional[str] = None,
    udf_email: Optional[str] = None,
    x: Optional[int] = None,
    y: Optional[int] = None,
    z: Optional[int] = None,
    sync: bool = True,
    engine: Optional[Literal["realtime", "batch", "local"]] = None,
    type: Optional[Literal["tile", "file"]] = None,
    parameters: Optional[Dict[str, Any]] = None,
    _include_log: Optional[bool] = False,
    **kw_parameters,
):
    """
    Executes a user-defined function (UDF) with various execution and input options.

    This function supports executing UDFs in different environments (realtime, batch, local),
    with different types of inputs (tile coordinates, geographical bounding boxes, etc.), and
    allows for both synchronous and asynchronous execution. It dynamically determines the execution
    path based on the provided parameters.

    Args:
        email_or_udf_or_token: A string that can either be a UDF name, a UDF token, or a direct
            reference to a UDF object. It can also be a UdfJobStepConfig object for detailed
            configuration, or None to specify UDF details in other parameters.
        udf_name: The name of the UDF to execute.
        udf: A GeoPandasUdfV2 object for direct execution.
        job_step: A UdfJobStepConfig object for detailed execution configuration.
        token: A token representing a shared UDF.
        udf_email: The email associated with the UDF.
        x, y, z: Tile coordinates for tile-based UDF execution.
        sync: If True, execute the UDF synchronously. If False, execute asynchronously.
        engine: The execution engine to use ('realtime', 'batch', or 'local').
        type: The type of UDF execution ('tile' or 'file').
        parameters: Additional parameters to pass to the UDF.
        **kw_parameters: Additional parameters to pass to the UDF.

    Raises:
        ValueError: If the UDF is not specified or is specified in more than one way.
        TypeError: If the first parameter is not of an expected type.
        Warning: Various warnings are issued for ignored parameters based on the execution path chosen.

    Returns:
        The result of the UDF execution, which varies based on the UDF and execution path.

    Examples:


        Run a UDF saved in the Fused system:
        ```py
        fused.run(udf_email="username@fused.io", udf_name="my_udf_name")
        ```

        Run a UDF saved in GitHub:
        ```py
        loaded_udf = fused.load("https://github.com/fusedio/udfs/tree/main/public/Building_Tile_Example")
        fused.run(udf=loaded_udf, bbox=bbox)
        ```

        Run a UDF saved in a local directory:
        ```py
        loaded_udf = fused.load("/Users/local/dir/Building_Tile_Example")
        fused.run(udf=loaded_udf, bbox=bbox)
        ```

    Note:
        This function dynamically determines the execution path and parameters based on the inputs.
        It is designed to be flexible and support various UDF execution scenarios.
    """
    from fused._optional_deps import HAS_GEOPANDAS, HAS_MERCANTILE, HAS_SHAPELY

    if email_or_udf_or_token is not None:
        if udf is not None:
            warnings.warn(
                FusedIgnoredWarning(
                    "udf parameter is being ignored in favor of the first positional parameter."
                ),
            )
        if job_step is not None:
            warnings.warn(
                FusedIgnoredWarning(
                    "job_step parameter is being ignored in favor of the first positional parameter."
                ),
            )
        if token is not None:
            warnings.warn(
                FusedIgnoredWarning(
                    "token parameter is being ignored in favor of the first positional parameter."
                ),
            )
        if udf_email is not None:
            warnings.warn(
                FusedIgnoredWarning(
                    "udf_email parameter is being ignored in favor of the first positional parameter."
                ),
            )

        if isinstance(email_or_udf_or_token, UdfJobStepConfig):
            job_step = email_or_udf_or_token
        elif isinstance(email_or_udf_or_token, GeoPandasUdfV2):
            udf = email_or_udf_or_token
        elif isinstance(email_or_udf_or_token, UdfAccessToken):
            token = email_or_udf_or_token.token
        elif isinstance(email_or_udf_or_token, str):
            if "/" in email_or_udf_or_token:
                udf_email, udf_name = email_or_udf_or_token.split("/", maxsplit=1)
            elif "@" in email_or_udf_or_token:
                udf_email = email_or_udf_or_token
            elif _is_udf_token(email_or_udf_or_token):
                token = email_or_udf_or_token
            else:
                # This will actually be the udf name, not the user's email
                udf_email = email_or_udf_or_token
                udf_name = None
        else:
            raise TypeError(
                "Could not detect UDF from first parameter. It should be a string, UdfJobStepConfig, or BaseUdf object."
            )

    ways_of_specifying_udfs = sum([bool(x) for x in [udf, job_step, token, udf_email]])
    if ways_of_specifying_udfs == 0:
        raise ValueError("No UDF specified")
    if ways_of_specifying_udfs != 1:
        raise ValueError("UDF was specified in more than one way, which is invalid")

    local_tile_bbox: Optional["gpd.GeoDataFrame"] = None
    xyz_ignored = False
    if (
        x is not None
        and y is not None
        and z is not None
        and HAS_MERCANTILE
        and HAS_GEOPANDAS
        and HAS_SHAPELY
    ):
        import geopandas as gpd
        import mercantile
        import shapely

        tile_bounds = mercantile.bounds(x, y, z)
        local_tile_bbox = gpd.GeoDataFrame(
            {"x": [x], "y": [y], "z": [z]},
            geometry=[shapely.box(*tile_bounds)],
            crs=4326,
        )
    elif x is not None or y is not None or z is not None:
        xyz_ignored = True

    if x is not None and y is not None and z is not None:
        if type is None:
            type = "tile"
        elif type != "tile":
            warnings.warn(
                FusedIgnoredWarning(
                    "x, y, z specified but UDF type is not 'tile', so they will be ignored"
                ),
            )
    else:
        if type is None:
            type = "file"
        elif type != "file":
            raise ValueError(
                "x, y, z not specified but type is 'tile', which is an invalid configuration. You must specify x, y, and z."
            )

    if udf is not None:
        job_step = UdfJobStepConfig(udf=udf)

    parameters = {
        **kw_parameters,
        **(parameters if parameters is not None else {}),
        **{"_include_log": True},
    }

    dispatch: dict[
        tuple[
            Literal["sync", "async"],
            Literal["tile", "file"],
            Literal["saved", "token", "local_job_step"],
            Literal["realtime", "local", "batch"],
        ],
        Optional[Callable],
    ] = {
        # Saved UDF
        ("sync", "tile", "saved", "realtime"): partial(
            run_tile, udf_email, udf_name, x=x, y=y, z=z, **parameters
        ),
        ("async", "tile", "saved", "realtime"): partial(
            run_tile_async, udf_email, udf_name, x=x, y=y, z=z, **parameters
        ),
        ("sync", "file", "saved", "realtime"): partial(
            run_file, udf_email, udf_name, **parameters
        ),
        ("async", "file", "saved", "realtime"): partial(
            run_file_async, udf_email, udf_name, **parameters
        ),
        # shared UDF token
        ("sync", "tile", "token", "realtime"): partial(
            run_shared_tile, token, x=x, y=y, z=z, **parameters
        ),
        ("async", "tile", "token", "realtime"): partial(
            run_shared_tile_async, token, x=x, y=y, z=z, **parameters
        ),
        ("sync", "file", "token", "realtime"): partial(
            run_shared_file, token, **parameters
        ),
        ("async", "file", "token", "realtime"): partial(
            run_shared_file_async, token, **parameters
        ),
        # Local job step, which includes locally held code
        ("sync", "tile", "local_job_step", "realtime"): lambda: job_step.run_tile(
            x=x, y=y, z=z, **parameters
        ),
        (
            "async",
            "tile",
            "local_job_step",
            "realtime",
        ): lambda: job_step.run_tile_async(x=x, y=y, z=z, **parameters),
        ("sync", "file", "local_job_step", "realtime"): lambda: job_step.run_file(
            **parameters
        ),
        (
            "async",
            "file",
            "local_job_step",
            "realtime",
        ): lambda: job_step.run_file_async(**parameters),
        ("sync", "tile", "local_job_step", "local"): lambda: job_step.run_local(
            local_tile_bbox, **parameters
        ),
        ("async", "tile", "local_job_step", "local"): lambda: job_step.run_local(
            local_tile_bbox, **parameters
        ),
        ("sync", "file", "local_job_step", "local"): lambda: job_step.run_local(
            **parameters
        ),
        ("async", "file", "local_job_step", "local"): lambda: job_step.run_local(
            **parameters
        ),
        ("sync", "tile", "local_job_step", "batch"): None,
        ("sync", "file", "local_job_step", "batch"): lambda: job_step.set_udf(
            job_step.udf, parameters=parameters
        ).run_remote(),
    }

    udf_storage = (
        "saved"
        if udf_email is not None
        else (
            "token"
            if token is not None
            else ("local_job_step" if job_step is not None else None)
        )
    )
    if udf_storage is None:
        raise ValueError("No UDF specified")

    if engine is None:
        if udf_storage in ["token", "saved"]:
            engine = "realtime"
        else:
            engine = default_run_engine()

    if xyz_ignored:
        if x is None or y is None or z is None:
            warnings.warn(
                FusedIgnoredWarning(
                    "x, y, z arguments will be ignored because one of them is None"
                ),
            )
        elif engine == "local":
            # This warning doesn't matter on realtime because we will just put the x/y/z into the URL
            warnings.warn(
                FusedIgnoredWarning(
                    "x, y, z arguments will be ignored because the following packages were not all found: mercantile shapely geopandas"
                ),
            )

    dispatch_params = ("sync" if sync else "async", type, udf_storage, engine)

    # Ellipsis is the sentinal value for not found in the dictionary at all
    fn = dispatch.get(dispatch_params, ...)

    if fn is Ellipsis:
        if udf_storage == "token" and engine != "realtime":
            raise ValueError("UDF tokens can only be called on the realtime engine.")
        elif udf_storage == "saved" and engine != "realtime":
            raise ValueError(
                "Saved UDFs can only be called on the realtime engine. To use another engine, load the UDF locally first."
            )
        else:
            raise ValueError(
                f"Could not determine how to call with settings: {dispatch_params}"
            )
    if fn is None:
        raise ValueError(f"Call type is not yet implemented: {dispatch_params}")

    udf_eval_result = fn()

    # Nested and remote UDF calls will return UdfEvaluationResult.
    # merge the stdout/stderr from fused.run() into running environment,
    # unless _include_log=True, then return the UdfEvaluationResult object.
    if isinstance(udf_eval_result, UdfEvaluationResult):
        if udf_eval_result.stdout:
            sys.stdout.write(udf_eval_result.stdout)
        if udf_eval_result.stderr:
            sys.stderr.write(udf_eval_result.stderr)
        if udf_eval_result.error_message is not None:
            raise UdfRuntimeError(
                udf_eval_result.error_message,
                child_exception_class=udf_eval_result.exception_class,
            )
        if _include_log:
            return udf_eval_result
        else:
            return udf_eval_result.data
    return udf_eval_result
