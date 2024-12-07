import warnings
from functools import partial
from typing import Any, Callable, Coroutine, Dict, Literal, Optional, Union, overload

import geopandas as gpd
import pandas as pd
import shapely
import xarray as xr

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

ResultType = Union[xr.Dataset, pd.DataFrame, gpd.GeoDataFrame]


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
    bbox: Union[gpd.GeoDataFrame, shapely.Geometry, None],
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
    _lat: Optional[float],
    _lng: Optional[float],
    bbox: Union[gpd.GeoDataFrame, shapely.Geometry, None],
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
    _lat: Optional[float] = None,
    _lng: Optional[float] = None,
    bbox: Union[gpd.GeoDataFrame, shapely.Geometry, None] = None,
    sync: bool = True,
    engine: Optional[Literal["realtime", "batch", "local"]] = None,
    type: Optional[Literal["tile", "file"]] = None,
    parameters: Optional[Dict[str, Any]] = None,
    **kw_parameters,
):
    """
    Executes a user-defined function (UDF) with various execution and input options.

    This function supports executing UDFs in different environments (realtime, batch, local),
    with different types of inputs (tile coordinates, geographical bounding boxes, etc.), and
    allows for both synchronous and asynchronous execution. It dynamically determines the execution
    path based on the provided parameters.

    Args:
        email_or_udf_or_token: A string that can either be an email, a UDF token, or a direct
            reference to a UDF object. It can also be a UdfJobStepConfig object for detailed
            configuration, or None to specify UDF details in other parameters.
        udf_name: The name of the UDF to execute.
        udf: A GeoPandasUdfV2 object for direct execution.
        job_step: A UdfJobStepConfig object for detailed execution configuration.
        token: A token representing a shared UDF.
        udf_email: The email associated with the UDF.
        x, y, z: Tile coordinates for tile-based UDF execution.
        _lat, _lng: Latitude and longitude for tile-based UDF execution.
        bbox: A geographical bounding box (as a GeoDataFrame or shapely Geometry) defining the area of interest.
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
    if email_or_udf_or_token is not None:
        if udf is not None:
            warnings.warn(
                "udf parameter is being ignored in favor of the first positional parameter.",
            )
        if job_step is not None:
            warnings.warn(
                "job_step parameter is being ignored in favor of the first positional parameter.",
            )
        if token is not None:
            warnings.warn(
                "token parameter is being ignored in favor of the first positional parameter.",
            )
        if udf_email is not None:
            warnings.warn(
                "udf_email parameter is being ignored in favor of the first positional parameter.",
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
            else:
                # TODO: no way to specify only UDF name
                token = email_or_udf_or_token
        else:
            raise TypeError(
                "Could not detect UDF from first parameter. It should be a string, UdfJobStepConfig, or BaseUdf object."
            )

    ways_of_specifying_udfs = sum([bool(x) for x in [udf, job_step, token, udf_email]])
    if ways_of_specifying_udfs == 0:
        raise ValueError("No UDF specified")
    if ways_of_specifying_udfs != 1:
        raise ValueError("UDF was specified in more than one way, which is invalid")

    local_tile_bbox: Optional[gpd.GeoDataFrame] = None
    if bbox is not None:
        if x is not None or y is not None or z is not None:
            warnings.warn("x, y, z arguments will be ignored in favor of bbox")
        if _lat is not None or _lng is not None:
            warnings.warn("_lat, _lng arguments will be ignored in favor of bbox")

        if (
            "x" in bbox.columns
            and "y" in bbox.columns
            and "z" in bbox.columns
            and len(bbox) == 1
        ):
            x, y, z = bbox.iloc[0][["x", "y", "z"]]
            local_tile_bbox = bbox.copy(deep=True)
        else:
            # bbox is not an x,y,z tile bounds from the Fused system, so try to find the appropriate bounds
            import mercantile

            if isinstance(bbox, gpd.GeoDataFrame):
                tile_bounds = bbox.total_bounds
            else:
                tile_bounds = shapely.bounds(bbox)

            tile = mercantile.bounding_tile(*tile_bounds)
            x, y, z = tile.x, tile.y, tile.z
            local_tile_bbox = gpd.GeoDataFrame(
                {"x": [x], "y": [y], "z": [z]}, geometry=[shapely.box(*tile_bounds)]
            )
    elif _lat is not None and _lng is not None:
        if z is None:
            raise ValueError(
                "Cannot compute x, y tile coordinates from _lat, _lng without z. You must specify z."
            )
        if x is not None or y is not None:
            warnings.warn("x and y arguments will be ignored in favor of _lat, _lng")

        import mercantile

        tile = mercantile.tile(lng=_lng, lat=_lat, zoom=z)
        tile_bounds = mercantile.bounds(tile)
        x, y, z = tile.x, tile.y, tile.z
        local_tile_bbox = gpd.GeoDataFrame(
            {"x": [x], "y": [y], "z": [z]}, geometry=[shapely.box(*tile_bounds)]
        )
    elif _lat is not None or _lng is not None:
        warnings.warn("lat, lng arguments will be ignored because one of them is None")
    elif x is not None and y is not None and z is not None:
        import mercantile

        tile_bounds = mercantile.bounds(x, y, z)
        local_tile_bbox = gpd.GeoDataFrame(
            {"x": [x], "y": [y], "z": [z]}, geometry=[shapely.box(*tile_bounds)]
        )
    elif x is not None or y is not None or z is not None:
        warnings.warn("x, y, z arguments will be ignored because one of them is None")

    if x is not None and y is not None and z is not None:
        if type is None:
            type = "tile"
        elif type != "tile":
            warnings.warn(
                "x, y, z specified but UDF type is not 'tile', so they will be ignored",
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
        ("async", "tile", "local_job_step", "realtime"): None,
        ("sync", "file", "local_job_step", "realtime"): lambda: job_step.run_file(
            **parameters
        ),
        ("async", "file", "local_job_step", "realtime"): None,
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

    return fn()
