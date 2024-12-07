# TODO: This file is no longer the most recent -- use fused.core.run_* instead
# This file is only for running non-saved (code included) UDFs

import base64
import json
import time
import warnings
from io import BytesIO
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Dict, Optional, Union

import geopandas as gpd
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import requests
import xarray as xr
from loguru import logger
from PIL import Image

from fused_batch._environment import infer_display_method
from fused_batch._options import STAGING_DEFAULT_BASE_URL
from fused_batch._options import options as OPTIONS
from fused_batch._str_utils import detect_passing_local_file_as_str
from fused_batch._udf.execute_v2 import _transform_output
from fused_batch.api import FusedAPI
from fused_batch.models import AnyJobStepConfig
from fused_batch.models.udf._eval_result import UdfEvaluationResult
from fused_batch.models.udf.output import Output
from fused_batch.models.udf.udf import AnyBaseUdf
from fused_batch.warnings import FusedWarning

from ..core._impl._realtime_ops_impl import get_recursion_factor

UDF_LOCAL_SERVER_URL = "http://127.0.0.1:8000"


def _resolve_udf_server_url(client_id: Optional[str] = None) -> str:
    if client_id == "_local" or OPTIONS.realtime_client_id == "_local":
        return UDF_LOCAL_SERVER_URL

    if client_id and client_id.endswith("-staging"):
        return f"{STAGING_DEFAULT_BASE_URL}/realtime/{client_id}"

    if client_id is None:
        api = FusedAPI()
        client_id = api._automatic_realtime_client_id()

        if client_id is None:
            raise ValueError("Failed to detect realtime client ID")

    return f"{OPTIONS.base_url}/realtime/{client_id}"


def run_tile(
    x: float,
    y: float,
    z: float,
    data: Optional[
        Union[pd.DataFrame, gpd.GeoDataFrame, pa.Table, str, Path, Any]
    ] = None,
    step_config: Optional[AnyJobStepConfig] = None,
    params: Optional[Dict[str, str]] = None,
    *,
    print_time: bool = False,
    client_id: Optional[str] = None,
    dtype_out_vector: str = "parquet",
    dtype_out_raster: str = "tiff",
) -> UdfEvaluationResult:  # TODO: return png
    time_start = time.perf_counter()
    # We need to get the auth headers from the FusedAPI. Don't enable set_global_api
    # to avoid messing up the user's environment.
    api = FusedAPI(set_global_api=False)

    udf_server_url = _resolve_udf_server_url(client_id)

    assert step_config is not None
    # Apply parameters, if we want to step_config that's returned to have this,
    # overwrite step_config.
    step_config_with_params = step_config.set_udf(
        udf=step_config.udf, parameters=params
    )

    url = f"{udf_server_url}/api/v1/run/udf/tiles/{z}/{x}/{y}"

    # Headers
    recursion_factor = get_recursion_factor()
    headers = api._generate_headers({"Content-Type": "application/json"})
    headers["Fused-Recursion"] = f"{recursion_factor}"

    # Payload
    post_attr_json = {
        "data_left": data,
        "data_right": None,
        "step_config": step_config_with_params.model_dump_json(),
        "dtype_in": "json",
        "dtype_out_vector": dtype_out_vector,
        "dtype_out_raster": dtype_out_raster,
    }

    # Params
    req_params = {}

    # Make request
    start = time.time()

    r = requests.post(
        url=url,
        params=req_params,
        json=post_attr_json,
        headers=headers,
        timeout=OPTIONS.request_timeout,
    )

    end = time.time()
    if print_time:
        logger.info(f"Time in request: {end - start}")

    time_end = time.perf_counter()
    time_taken_seconds = time_end - time_start

    return _process_response(
        r, step_config=step_config_with_params, time_taken_seconds=time_taken_seconds
    )


def run(
    df_left: Optional[
        Union[pd.DataFrame, gpd.GeoDataFrame, pa.Table, str, Path, Any]
    ] = None,
    df_right: Optional[
        Union[pd.DataFrame, gpd.GeoDataFrame, pa.Table, str, Path]
    ] = None,
    step_config: Optional[AnyJobStepConfig] = None,
    params: Optional[Dict[str, str]] = None,
    *,
    print_time: bool = False,
    read_options: Optional[Dict] = None,
    client_id: Optional[str] = None,
    dtype_out_vector: str = "parquet",
    dtype_out_raster: str = "tiff",
) -> pd.DataFrame:
    """Run a UDF over a DataFrame.

    Args:
        df_left: Input DataFrame, or path to a local Parquet file.
        df_right: Input DataFrame, or path to a local Parquet file.
        step_config: AnyJobStepConfig.
        params: Additional parameters to pass to the UDF. Must be JSON serializable.

    Keyword Args:
        print_time: If True, print the amount of time taken in the request.
        read_options: If not None, options for reading `df` that will be passed to GeoPandas.
    """
    # TODO: This function is too complicated

    time_start = time.perf_counter()
    # We need to get the auth headers from the FusedAPI. Don't enable set_global_api
    # to avoid messing up the user's environment.
    api = FusedAPI(set_global_api=False)

    udf_server_url = _resolve_udf_server_url(client_id)

    assert step_config is not None
    # Apply parameters, if we want to step_config that's returned to have this,
    # overwrite step_config.
    step_config_with_params = step_config.set_udf(
        udf=step_config.udf, parameters=params
    )

    # Note: Custom UDF uses the json POST attribute.
    url = f"{udf_server_url}/api/v1/run/udf"

    # This is the body for when step_config_with_params.type == "udf".
    body = {
        "data_left": df_left,
        "step_config": step_config_with_params.model_dump_json(),
        "dtype_in": "json",
        "dtype_out_vector": dtype_out_vector,
        "dtype_out_raster": dtype_out_raster,
    }

    # TODO: This is not really supported
    if step_config_with_params.type != "udf":
        # Infer dtype_in from df_left. Ensure df_right, if present, is same type.
        if df_left is not None:
            data_left, dtype_in_left = _serialize_input(df_left, read_options)
            body["data_left"] = data_left
            body["dtype_in"] = dtype_in_left

        if df_right is not None:
            body["data_right"], dtype_in_right = _serialize_input(
                df_right, read_options
            )
            assert (
                dtype_in_left == dtype_in_right
            ), "Left and right must be same type. Fused currently supports 'GeoDataFrame' and 'geojson'."

    method = "POST"
    post_attr_json = body

    recursion_factor = get_recursion_factor()
    post_attr_headers = api._generate_headers({"Content-Type": "application/json"})
    post_attr_headers["Fused-Recursion"] = f"{recursion_factor}"

    req_params = {}

    # Make request
    start = time.time()

    r = requests.request(
        method=method,
        url=url,
        params=req_params,
        json=post_attr_json,
        headers=post_attr_headers,
        timeout=OPTIONS.request_timeout,
    )
    end = time.time()
    if print_time:
        logger.info(f"Time in request: {end - start}")

    time_end = time.perf_counter()
    time_taken_seconds = time_end - time_start

    return _process_response(
        r, step_config=step_config_with_params, time_taken_seconds=time_taken_seconds
    )


def _serialize_input(df: Union[str, pd.DataFrame, dict], read_options=None):
    if isinstance(df, pd.DataFrame):
        return (
            base64.encodebytes(_serialize_df(df, read_options).getvalue()).decode(
                "utf-8"
            ),
            "parquet",
        )
    elif isinstance(df, str):
        return json.loads(df), "geojson"
    elif isinstance(df, dict):
        return df, "geojson"


def _serialize_df(df: pd.DataFrame, read_options: Optional[Dict] = None):
    df = detect_passing_local_file_as_str(df)
    if isinstance(df, Path):
        read_options = {} if read_options is None else read_options
        if df.suffix == ".parquet":
            df = gpd.read_parquet(df, **read_options)
        else:
            df = gpd.read_file(df, **read_options)
    assert not isinstance(
        df, str
    ), f"A string input was passed but a file with that name could not be found: {df}"

    buf = BytesIO()
    if isinstance(df, pd.DataFrame):
        df.to_parquet(buf)
    elif isinstance(df, pa.Table):
        pq.write_table(df, buf)
    else:
        assert False, f"Unexpected type for df: {type(df)}"
    return buf


def _process_response(
    r: requests.Response,
    step_config: AnyJobStepConfig,
    time_taken_seconds: float,
) -> UdfEvaluationResult:
    result_content: Optional[bytes] = None
    output_df: Optional[pd.DataFrame] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    error_message: Optional[str] = None
    error_lineno: Optional[int] = None

    try:
        if r.status_code != 200 and r.status_code != 422:
            raise ValueError(r.text)
        result_content = r.content
        # x-fused-metadata holds LogHandler as JSON, which contains stdout/stderr.
        _fused_metadata = r.headers.get("x-fused-metadata")
        fused_metadata = json.loads(_fused_metadata) if _fused_metadata else {}

        # Extract stdout/stderr.
        stdout = fused_metadata.get("stdout")
        stderr = fused_metadata.get("stderr")

        # Extract udf.
        udf: Optional[AnyBaseUdf] = None
        if step_config is not None:
            udf = step_config.udf

        # Extract error line, if exists.
        error_lineno = fused_metadata.get("lineno")

        if r.status_code == 200:
            # If the UDF returned None.
            if len(result_content) == 0:
                return UdfEvaluationResult(
                    data=None,
                    udf=udf,
                    time_taken_seconds=time_taken_seconds,
                    stdout=stdout,
                    stderr=stderr,
                    error_message=error_message,
                    error_lineno=error_lineno,
                )

            # Else, process response output.
            res_buf = BytesIO(result_content)

            if r.headers["content-type"] == "image/png":
                display_method = infer_display_method(None, None)
                if display_method.show_widget:
                    from IPython.display import Image as IPythonImage
                    from IPython.display import display

                    display(IPythonImage(data=r.content, format="png"))

                image = Image.open(BytesIO(r.content))
                width, height = image.size
                if len(image.getbands()) == 1:
                    image_data = list(image.getdata())
                    image_data = [
                        image_data[i : i + width]
                        for i in range(0, len(image_data), width)
                    ]
                    data_array = xr.DataArray(image_data, dims=["y", "x"])
                else:
                    image_data = []
                    for band in range(len(image.getbands())):
                        band_data = list(image.getdata(band=band))
                        band_data = [
                            band_data[i : i + width]
                            for i in range(0, len(band_data), width)
                        ]
                        image_data.append(band_data)
                    data_array = xr.DataArray(image_data, dims=["band", "y", "x"])

                # Create the dataset with image, latitude, and longitude data
                dataset = xr.Dataset({"image": data_array})

                return UdfEvaluationResult(
                    data=dataset,
                    udf=udf,
                    time_taken_seconds=time_taken_seconds,
                    stdout=stdout,
                    stderr=stderr,
                    error_message=error_message,
                    error_lineno=error_lineno,
                )
            elif r.headers["content-type"] == "image/tiff":
                # TODO: Automatically display tiff?
                import rioxarray

                with NamedTemporaryFile(prefix="udf_result", suffix=".tiff") as ntmp:
                    with open(ntmp.name, "wb") as f:
                        f.write(r.content)
                    rda = rioxarray.open_rasterio(
                        ntmp.name,
                        masked=True,
                    )
                    dataset = xr.Dataset({"image": rda})

                    return UdfEvaluationResult(
                        data=dataset,
                        udf=udf,
                        time_taken_seconds=time_taken_seconds,
                        stdout=stdout,
                        stderr=stderr,
                        error_message=error_message,
                        error_lineno=error_lineno,
                    )
            else:  # assume parquet
                m = pq.read_metadata(res_buf)
                if b"geo" in m.metadata:
                    try:
                        output_df = gpd.read_parquet(res_buf)
                    except ValueError as e:
                        warnings.warn(
                            f"Result has geo metadata but could not be loaded in GeoPandas: {e}",
                            FusedWarning,
                        )
                if output_df is None:
                    output_df = pd.read_parquet(res_buf)

                if "fused_index" not in output_df.columns:
                    # TODO: Hack since the backend no longer responds with fused_index
                    output_df["fused_index"] = list(range(len(output_df)))

                new_output = _transform_output(
                    output=Output(data=output_df, skip_fused_index_validation=True)
                )

                new_output.validate_data_with_schema()

                if hasattr(udf, "table_schema") and udf.table_schema is None:
                    udf.table_schema = new_output.table_schema  # TODO: ?
                return UdfEvaluationResult(
                    data=new_output.data,
                    sidecar=new_output.sidecar_output,
                    udf=udf,
                    table_schema=new_output.table_schema,
                    time_taken_seconds=time_taken_seconds,
                    stdout=stdout,
                    stderr=stderr,
                    error_message=error_message,
                    error_lineno=error_lineno,
                )
        else:
            if "errormsg" in fused_metadata and fused_metadata["errormsg"]:
                error_message = f"The UDF returned the following error for chunk {fused_metadata['chunkinfo']} in line {fused_metadata.get('lineno')}:\n{fused_metadata['errormsg']}"
            elif "exception" in fused_metadata and fused_metadata["exception"]:
                error_message = fused_metadata["exception"]
            else:
                # No error message was returned, e.g. due to deserialization error
                try:
                    # Look for a "detail" field in the response payload
                    details_obj = json.loads(r.text)
                    error_message = details_obj["detail"]
                except:  # noqa: E722
                    error_message = r.text

            return UdfEvaluationResult(
                data=None,
                udf=udf,
                time_taken_seconds=time_taken_seconds,
                stdout=stdout,
                stderr=stderr,
                error_message=error_message,
                error_lineno=error_lineno,
            )
    except:  # noqa: E722
        r.raise_for_status()
        raise
