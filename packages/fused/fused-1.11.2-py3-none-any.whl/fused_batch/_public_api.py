from __future__ import annotations

import json
import os
import tempfile
import uuid
import warnings
import zipfile
from contextlib import contextmanager
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Union,
    overload,
)

import geopandas as gpd

import fused_batch
from fused_batch._global_api import get_api
from fused_batch._str_utils import detect_passing_local_file_as_str, table_to_name
from fused_batch.models._codegen import CustomJobConfig
from fused_batch.models.api import (
    Dataset,
    GeospatialPartitionJobStepConfig,
    JobConfig,
    JobStepConfig,
    JoinJobStepConfig,
    ListDetails,
    MapJobStepConfig,
    NonGeospatialPartitionJobStepConfig,
    Table,
)
from fused_batch.models.api.job import GDALOpenConfig, JoinType, RootAnyJobStepConfig
from fused_batch.models.internal import (
    DatasetInputV2,
    DatasetInputV2Table,
    DatasetInputV2Type,
    DatasetOutputV2,
    Jobs,
)
from fused_batch.models.internal.dataset import RootAnyDatasetInput
from fused_batch.models.schema import Schema
from fused_batch.models.udf import AnyBaseUdf
from fused_batch.warnings import (
    FusedDefaultWarning,
    FusedIgnoredWarning,
    FusedTypeWarning,
)

if TYPE_CHECKING:
    from xyzservices.lib import TileProvider


def _table_to_v2_table(
    table: Union[Table, str], *, read_sidecar: Union[Sequence[str], bool] = False
) -> DatasetInputV2Table:
    table_url = table.url if isinstance(table, Table) else table
    table_name = table_to_name(table_url)
    read_sidecar_bool = read_sidecar is not None and (
        read_sidecar if isinstance(read_sidecar, bool) else (table_name in read_sidecar)
    )
    return DatasetInputV2Table(
        url=table_url,
        read_sidecar_files=read_sidecar_bool,
    )


def _create_table_objs(
    tables: Iterable[Union[Table, str]],
    read_sidecar: Union[Sequence[str], bool] = False,
):
    ret = [_table_to_v2_table(t, read_sidecar=read_sidecar) for t in tables]

    if not isinstance(read_sidecar, bool):
        unapplied_sidecar_table_names: List[str] = []
        applied_sidecar_table_names = set(
            [table_to_name(t.url) for t in ret if t.read_sidecar_files is True]
        )
        for sidecar_table_name in read_sidecar:
            if sidecar_table_name not in applied_sidecar_table_names:
                unapplied_sidecar_table_names.append(sidecar_table_name)

        if unapplied_sidecar_table_names:
            warnings.warn(
                f"Some table names to read sidecars from were not applied: {unapplied_sidecar_table_names}",
                FusedIgnoredWarning,
            )

    return ret


def get_jobs(
    n: int = 5,
    *,
    skip: int = 0,
    per_request: int = 25,
    max_requests: Optional[int] = None,
) -> Jobs:
    """Get the job history.

    Args:
        n: The number of jobs to fetch. Defaults to 5.

    Keyword Args:
        skip: Where in the job history to begin. Defaults to 0, which retrieves the most recent job.
        per_request: Number of jobs per request to fetch. Defaults to 25.
        max_requests: Maximum number of requests to make. May be None to fetch all jobs. Defaults to 1.

    Returns:
        The job history.
    """
    api = get_api()
    return api.get_jobs(
        n=n, skip=skip, per_request=per_request, max_requests=max_requests
    )


def get_udfs(
    n: int = 10,
    *,
    skip: int = 0,
    per_request: int = 25,
    max_requests: Optional[int] = None,
    by: Literal["name", "id", "slug"] = "name",
    whose: Literal["self", "public"] = "self",
):
    """
    Fetches a list of UDFs.

    Args:
        n: The total number of UDFs to fetch. Defaults to 10.
        skip: The number of UDFs to skip before starting to collect the result set. Defaults to 0.
        per_request: The number of UDFs to fetch in each API request. Defaults to 25.
        max_requests: The maximum number of API requests to make.
        by: The attribute by which to sort the UDFs. Can be "name", "id", or "slug". Defaults to "name".
        whose: Specifies whose UDFs to fetch. Can be "self" for the user's own UDFs or "public" for
            UDFs available publicly. Defaults to "self".

    Returns:
        A list of UDFs.

    Examples:
        Fetch UDFs under the user account:
        ```py
        fused.get_udfs()
        ```
    """
    api = get_api()
    return api.get_udfs(
        n=n,
        skip=skip,
        per_request=per_request,
        max_requests=max_requests,
        by=by,
        whose=whose,
    )


def open_table(
    path: Union[str, DatasetOutputV2],
    *,
    fetch_samples: Optional[bool] = None,
) -> Table:
    """Open a Table object given a path to the root of the table

    Args:
        path: The path to the root of the table on remote storage

    Keyword Args:
        fetch_samples: If True, fetch sample on each table when getting dataset metadata.
    Returns:
        A Table object

    Examples:
        ```py
        table = fused.open_table("s3://my_bucket/path/to/dataset/table/")
        ```
    """
    if isinstance(path, DatasetOutputV2):
        path = path.url

    api = get_api()
    return api.open_table(
        path=path,
        fetch_samples=fetch_samples,
    )


def ingest(
    input: Union[str, Sequence[str], Path, gpd.GeoDataFrame],
    output: Optional[str] = None,
    *,
    output_metadata: Optional[str] = None,
    schema: Optional[Schema] = None,
    file_suffix: Optional[str] = None,
    load_columns: Optional[Sequence[str]] = None,
    remove_cols: Optional[Sequence[str]] = None,
    explode_geometries: bool = False,
    drop_out_of_bounds: Optional[bool] = None,
    partitioning_method: Literal["area", "length", "coords", "rows"] = "rows",
    partitioning_maximum_per_file: Union[int, float, None] = None,
    partitioning_maximum_per_chunk: Union[int, float, None] = None,
    partitioning_max_width_ratio: Union[int, float] = 2,
    partitioning_max_height_ratio: Union[int, float] = 2,
    partitioning_force_utm: Literal["file", "chunk", None] = "chunk",
    partitioning_split_method: Literal["mean", "median"] = "mean",
    subdivide_method: Literal["area", None] = None,
    subdivide_start: Optional[float] = None,
    subdivide_stop: Optional[float] = None,
    split_identical_centroids: bool = True,
    target_num_chunks: int = 5000,
    lonlat_cols: Optional[Tuple[str, str]] = None,
    gdal_config: Union[GDALOpenConfig, Dict[str, Any], None] = None,
) -> GeospatialPartitionJobStepConfig:
    """Ingest a dataset into the Fused partitioned format.

    Args:
        input: A GeoPandas `GeoDataFrame` or a path to file or files on S3 to ingest. Files may be Parquet or another geo data format.
        output: Location on S3 to write the `main` table to.
        output_metadata: Location on S3 to write the `fused` table to.
        schema: Schema of the data to be ingested. This is optional and will be inferred from the data if not provided.
        file_suffix: filter which files are used for ingestion. If `input` is a directory on S3, all files under that directory will be listed and used for ingestion. If `file_suffix` is not None, it will be used to filter paths by checking the trailing characters of each filename. E.g. pass `file_suffix=".geojson"` to include only GeoJSON files inside the directory.
        load_columns: Read only this set of columns when ingesting geospatial datasets. Defaults to all columns.
        remove_cols: The named columns to drop when ingesting geospatial datasets. Defaults to not drop any columns.
        explode_geometries: Whether to unpack multipart geometries to single geometries when ingesting geospatial datasets, saving each part as its own row. Defaults to `False`.
        drop_out_of_bounds: Whether to drop geometries outside of the expected WGS84 bounds. Defaults to True.
        partitioning_method: The method to use for grouping rows into partitions. Defaults to `"rows"`.

            - `"area"`: Construct partitions where all contain a maximum total area among geometries.
            - `"length"`: Construct partitions where all contain a maximum total length among geometries.
            - `"coords"`: Construct partitions where all contain a maximum total number of coordinates among geometries.
            - `"rows"`: Construct partitions where all contain a maximum number of rows.

        partitioning_maximum_per_file: Maximum value for `partitioning_method` to use per file. If `None`, defaults to _1/10th_ of the total value of `partitioning_method`. So if the value is `None` and `partitioning_method` is `"area"`, then each file will be have no more than 1/10th the total area of all geometries. Defaults to `None`.
        partitioning_maximum_per_chunk: Maximum value for `partitioning_method` to use per chunk. If `None`, defaults to _1/100th_ of the total value of `partitioning_method`. So if the value is `None` and `partitioning_method` is `"area"`, then each file will be have no more than 1/100th the total area of all geometries. Defaults to `None`.
        partitioning_max_width_ratio: The maximum ratio of width to height of each partition to use in the ingestion process. So for example, if the value is `2`, then if the width divided by the height is greater than `2`, the box will be split in half along the horizontal axis. Defaults to `2`.
        partitioning_max_height_ratio: The maximum ratio of height to width of each partition to use in the ingestion process. So for example, if the value is `2`, then if the height divided by the width is greater than `2`, the box will be split in half along the vertical axis. Defaults to `2`.
        partitioning_force_utm: Whether to force partitioning within UTM zones. If set to `"file"`, this will ensure that the centroid of all geometries per _file_ are contained in the same UTM zone. If set to `"chunk"`, this will ensure that the centroid of all geometries per _chunk_ are contained in the same UTM zone. If set to `None`, then no UTM-based partitioning will be done. Defaults to "chunk".
        partitioning_split_method: How to split one partition into children. Defaults to `"mean"` (this may change in the future).

            - `"mean"`: Split each axis according to the mean of the centroid values.
            - `"median"`: Split each axis according to the median of the centroid values.

        subdivide_method: The method to use for subdividing large geometries into multiple rows. Currently the only option is `"area"`, where geometries will be subdivided based on their area (in WGS84 degrees).
        subdivide_start: The value above which geometries will be subdivided into smaller parts, according to `subdivide_method`.
        subdivide_stop: The value below which geometries will not be subdivided into smaller parts, according to `subdivide_method`. Recommended to be equal to subdivide_start. If `None`, geometries will be subdivided up to a recursion depth of 100 or until the subdivided geometry is rectangular.
        split_identical_centroids: If `True`, should split a partition that has
            identical centroids (such as if all geometries in the partition are the
            same) if there are more such rows than defined in "partitioning_maximum_per_file" and
            "partitioning_maximum_per_chunk".
        target_num_chunks: The target for the number of files if `partitioning_maximum_per_file` is None. Note that this number is only a _target_ and the actual number of files generated can be higher or lower than this number, depending on the spatial distribution of the data itself.
        lonlat_cols: Names of longitude, latitude columns to construct point geometries from.

            If your point columns are named `"x"` and `"y"`, then pass:

            ```py
            fused.ingest(
                ...,
                lonlat_cols=("x", "y")
            )
            ```

            This only applies to reading from Parquet files. For reading from CSV files, pass options to `gdal_config`.

        gdal_config: Configuration options to pass to GDAL for how to read these files. For all files other than Parquet files, Fused uses GDAL as a step in the ingestion process. For some inputs, like CSV files or zipped shapefiles, you may need to pass some parameters to GDAL to tell it how to open your files.

            This config is expected to be a dictionary with up to two keys:

            - `layer`: `str`. Define the layer of the input file you wish to read when the source contains multiple layers, as in GeoPackage.
            - `open_options`: `Dict[str, str]`. Pass in key-value pairs with GDAL open options. These are defined on each driver's page in the GDAL documentation. For example, the [CSV driver](https://gdal.org/drivers/vector/csv.html) defines [these open options](https://gdal.org/drivers/vector/csv.html#open-options) you can pass in.

            For example, if you're ingesting a CSV file with two columns
            `"longitude"` and `"latitude"` denoting the coordinate information, pass

            ```py
            fused.ingest(
                ...,
                gdal_config={
                    "open_options": {
                        "X_POSSIBLE_NAMES": "longitude",
                        "Y_POSSIBLE_NAMES": "latitude",
                    }
                }
            )
            ```
    Returns:

        Configuration object describing the ingestion process. Call `.execute` on this object to start a job.


    Examples:
        For example, to ingest the California Census dataset for the year 2022:
        ```py
        job = fused.ingest(
            input="https://www2.census.gov/geo/tiger/TIGER_RD18/STATE/06_CALIFORNIA/06/tl_rd22_06_bg.zip",
            output="s3://fused-sample/census/ca_bg_2022/main/",
            output_metadata="s3://fused-sample/census/ca_bg_2022/fused/",
            explode_geometries=True,
            partitioning_maximum_per_file=2000,
            partitioning_maximum_per_chunk=200,
        ).execute()
        ```
    """
    remove_cols = remove_cols if remove_cols else []
    if (
        subdivide_start is not None or subdivide_stop is not None
    ) and subdivide_method is None:
        raise ValueError(
            'subdivide_start or subdivide_stop require subdivide_method be specified (it should be "area")'
        )
    api = get_api()
    input = detect_passing_local_file_as_str(input)
    input = api._replace_df_input(input)
    return GeospatialPartitionJobStepConfig(
        input=input,
        output=output,
        output_metadata=output_metadata,
        table_schema=schema,
        file_suffix=file_suffix,
        load_columns=load_columns,
        remove_cols=remove_cols,
        explode_geometries=explode_geometries,
        drop_out_of_bounds=drop_out_of_bounds,
        lonlat_cols=lonlat_cols,
        partitioning_maximum_per_file=partitioning_maximum_per_file,
        partitioning_maximum_per_chunk=partitioning_maximum_per_chunk,
        partitioning_max_width_ratio=partitioning_max_width_ratio,
        partitioning_max_height_ratio=partitioning_max_height_ratio,
        partitioning_method=partitioning_method,
        partitioning_force_utm=partitioning_force_utm,
        partitioning_split_method=partitioning_split_method,
        subdivide_start=subdivide_start,
        subdivide_stop=subdivide_stop,
        subdivide_method=subdivide_method,
        split_identical_centroids=split_identical_centroids,
        target_num_chunks=target_num_chunks,
        gdal_config=GDALOpenConfig() if gdal_config is None else gdal_config,
    )


def ingest_nongeospatial(
    input: Union[str, Sequence[str], Path, gpd.GeoDataFrame],
    output: Optional[str] = None,
    *,
    output_metadata: Optional[str] = None,
    partition_col: Optional[str] = None,
    partitioning_maximum_per_file: int = 2_500_000,
    partitioning_maximum_per_chunk: int = 65_000,
) -> NonGeospatialPartitionJobStepConfig:
    """Ingest a dataset into the Fused partitioned format.

    Args:
        input: A GeoPandas `GeoDataFrame` or a path to file or files on S3 to ingest. Files may be Parquet or another geo data format.
        output: Location on S3 to write the `main` table to.
        output_metadata: Location on S3 to write the `fused` table to.
        partition_col: Partition along this column for nongeospatial datasets.
        partitioning_maximum_per_file: Maximum number of items to store in a single file. Defaults to 2,500,000.
        partitioning_maximum_per_chunk: Maximum number of items to store in a single file. Defaults to 65,000.

    Returns:

        Configuration object describing the ingestion process. Call `.execute` on this object to start a job.

    Examples:
        ```py
        job = fused.ingest_nongeospatial(
            input=gdf,
            output="s3://sample-bucket/file.parquet",
        ).execute()
        ```
    """
    api = get_api()
    input = detect_passing_local_file_as_str(input)
    input = api._replace_df_input(input)
    return NonGeospatialPartitionJobStepConfig(
        input=input,
        output=output,
        output_metadata=output_metadata,
        partition_col=partition_col,
        partitioning_maximum_per_file=partitioning_maximum_per_file,
        partitioning_maximum_per_chunk=partitioning_maximum_per_chunk,
    )


def map(
    dataset: Union[str, Dataset, Table],
    output_table: Optional[str] = None,
    udf: Union[AnyBaseUdf, None] = None,
    *,
    cache_locally: bool = False,
) -> MapJobStepConfig:
    """Construct a `map` config from this Table

    Args:
        output_table: Where to save the output of this operation. Defaults to `None`, which will not save the output.
        udf: A user-defined function to run in this map. Defaults to None.

    Keyword Args:
        tables: The attribute tables to include in the map reduce. Defaults to ("main",).
        cache_locally: Advanced: whether to cache all the partitions locally in the map job. Defaults to False.

    Returns:
        An object describing the map configuration.
    """
    api = get_api()
    if isinstance(dataset, str):
        dataset = api.open_table(dataset, fetch_samples=False)

    return dataset.map(
        output_table=output_table,
        udf=udf,
        cache_locally=cache_locally,
    )


def join(
    dataset: Union[str, Dataset, Table],
    other: Union[str, Dataset, Table],
    output_table: Optional[str] = None,
    udf: Union[AnyBaseUdf, None] = None,
    *,
    how: Union[JoinType, Literal["left", "inner"]] = "inner",
    left_cache_locally: bool = False,
    right_cache_locally: bool = False,
    buffer_distance: Optional[float] = None,
) -> JoinJobStepConfig:
    """Construct a join config from two tables

    Args:
        other: The other Dataset object to join on
        output_table: Where to save the output of this operation. Defaults to `None`, which will not save the output.
        udf: The user-defined function to run in the join

    Keyword Args:
        how: The manner of doing the join. Currently  Defaults to "inner".
        left_cache_locally: Whether to cache the left dataset locally in the join. Defaults to False.
        right_cache_locally: Whether to cache the right dataset locally in the join. Defaults to False.
        buffer_distance: The size of the buffer (in meters) on the left table to use during the join. Defaults to None.

    Returns:
        An object describing the join configuration.

    Examples:
        ```py
        import fused

        left_table = fused.open_table("s3://bucket/path/to/table")
        other_table = fused.open_table("s3://bucket/path/to/table")
        join_config = fused.join(left_table, other_table)
        ```


    """
    api = get_api()

    if isinstance(dataset, str):
        dataset = api.open_table(dataset, fetch_samples=False)

    if isinstance(other, str):
        other = api.open_table(other, fetch_samples=False)

    return dataset.join(
        other=other,
        output_table=output_table,
        udf=udf,
        how=how,
        left_cache_locally=left_cache_locally,
        right_cache_locally=right_cache_locally,
        buffer_distance=buffer_distance,
    )


def job(
    input: Union[
        str,
        Dict,
        JobStepConfig,
        JobConfig,
        Sequence[Union[Dict, JobStepConfig, JobConfig]],
    ],
    content_type: Optional[str] = None,
    ignore_chunk_error: bool = False,
) -> JobConfig:
    """Construct a JobConfig

    Args:
        input: A object or list of objects describing job steps.
        content_type: How to interpret `input` when it is a string. E.g. "json" for JSON or "fused_job_id" for a Fused Job ID.

    Returns:
        A combined job config.
    """
    if isinstance(input, str):
        if content_type is None:
            if _is_valid_uuid(input):
                content_type = "fused_job_id"
            else:
                warnings.warn(
                    'content_type is not set, assuming "json"', FusedDefaultWarning
                )
                content_type = "json"
        if content_type == "fused_job_id":
            api = get_api()
            return api.get_job_config(input)
        if content_type == "json":
            return JobConfig(
                steps=[RootAnyJobStepConfig.model_validate_json(input).root]
            )
        else:
            assert (
                False
            ), f"Unknown content type: {content_type}. Should be one of `json` or `fused_job_id`."
    elif isinstance(input, dict):
        return JobConfig(steps=[RootAnyJobStepConfig.model_validate(input).root])
    elif isinstance(input, JobStepConfig):
        config = JobConfig(steps=[input])
    elif isinstance(input, JobConfig):
        return job(input.model_copy(deep=True).steps)
    else:
        # Assumed to be sequence
        steps: List[JobStepConfig] = []
        for input_step in input:
            if isinstance(input_step, dict):
                step = RootAnyJobStepConfig.model_validate(input_step).root
                steps.append(step)
            elif isinstance(input_step, JobStepConfig):
                steps.append(input_step.model_copy(deep=True))
            elif isinstance(input_step, JobConfig):
                steps.extend(input_step.model_copy(deep=True).steps)
            else:
                assert False, "expected dict or JobStepConfig"

        config = JobConfig(steps=steps, ignore_chunk_error=ignore_chunk_error)

    return config


def _whoami():
    """
    Returns information on the currently logged in user
    """
    api = get_api()
    return api._whoami()


def plot(
    gdf: gpd.GeoDataFrame,
    source: Union[str, "TileProvider", Ellipsis] = ...,
    **geopandas_kwargs: Dict[str, Any],
):
    """
    Plot a GeoDataFrame on a map using contextily to add basemap

    Args:
        gdf: A GeoPandas `GeoDataFrame` to plot.
        source : Basemap to use. Accepts an xyzservices.TileProvider object or str.
            [Optional. Default: CartoDB DarkMatterNoLabels]
            The tile source: web tile provider, a valid input for a query of a
            :class:`xyzservices.TileProvider` by a name from ``xyzservices.providers`` or
            path to local file.
        **geopandas_kwargs: Additional keyword arguments to pass to `gdf.plot`.
    """
    import contextily as cx

    if source is Ellipsis:
        source = cx.providers.CartoDB.DarkMatterNoLabels

    ax = gdf.plot(**geopandas_kwargs)
    if hasattr(gdf, "crs") and gdf.crs is not None:
        crs = gdf.crs.to_string()
    else:
        crs = "WGS84"
        warnings.warn("CRS not specified, defaulting to WGS84", FusedDefaultWarning)
    return cx.add_basemap(ax, crs=crs, source=source)


def delete(
    path: str,
    max_deletion_depth: Union[int, Literal["unlimited"]] = 2,
) -> bool:
    """Delete the files at the path.

    Args:
        path: Directory or file to delete, like `fd://my-old-table/`
        max_deletion_depth: If set (defaults to 2), the maximum depth the operation will recurse to.
                            This option is to help avoid accidentally deleting more data that intended.
                            Pass `"unlimited"` for unlimited.


    Examples:
        ```python
        fused.delete("fd://bucket-name/deprecated_table/")
        ```
    """
    api = get_api()
    return api.delete(path, max_deletion_depth=max_deletion_depth)


@overload
def list(path: str, *, details: Literal[False] = False) -> List[str]:
    ...


@overload
def list(path: str, *, details: Literal[True]) -> List[ListDetails]:
    ...


def list(path: str, *, details: bool = False):
    """List the files at the path.

    Args:
        path: Parent directory URL, like `fd://bucket-name/`

    Keyword Args:
        details: If True, return additional metadata about each record.

    Returns:
        A list of paths as URLs, or as metadata objects.

    Examples:
        ```python
        fused.list("fd://bucket-name/")
        ```
    """
    api = get_api()
    return api.list(path, details=details)


def get(path: str) -> bytes:
    """Download the contents at the path to memory.

    Args:
        path: URL to a file, like `fd://bucket-name/file.parquet`

    Returns:
        bytes of the file

    Examples:
        ```python
        fused.get("fd://bucket-name/file.parquet")
        ```
    """
    api = get_api()
    return api.get(path)


def download(path: str, local_path: Union[str, Path]) -> None:
    """Download the contents at the path to disk.

    Args:
        path: URL to a file, like `fd://bucket-name/file.parquet`
        local_path: Path to a local file.
    """
    api = get_api()
    api.download(path, local_path=local_path)


def upload(local_path: Union[str, Path, bytes, BinaryIO], remote_path: str) -> None:
    """Upload local file to S3.

    Args:
        local_path: Either a path to a local file (`str`, `Path`) or the contents to upload.
                    Any string will be treated as a Path, if you wish to upload the contents of
                    the string, first encode it: `s.encode("utf-8")`
        remote_path: URL to upload to, like `fd://new-file.txt`

    Examples:
        To upload a local json file to your Fused-managed S3 bucket:
        ```py
        fused.upload("my_file.json", "fd://my_bucket/my_file.json")
        ```
    """
    api = get_api()
    if isinstance(local_path, str):
        # We assume any string being passed in is a path, rather than the contents
        # to upload.
        local_path = Path(local_path)
        if not local_path.exists():
            warnings.warn(
                '`local_path` is being treated as a path but it does not exist. If you wish to upload the contents of the string, encode it to bytes first with `.encode("utf-8")',
                FusedTypeWarning,
            )
    if isinstance(local_path, Path):
        local_path = local_path.read_bytes()
    api.upload(path=remote_path, data=local_path)


def sign_url(path: str) -> str:
    """Create a signed URL to access the path.

    This function may not check that the file represented by the path exists.

    Args:
        path: URL to a file, like `fd://bucket-name/file.parquet`

    Returns:
        HTTPS URL to access the file using signed access.

    Examples:
        ```python
        fused.sign_url("fd://bucket-name/table_directory/file.parquet")
        ```
    """
    api = get_api()
    return api.sign_url(path)


def sign_url_prefix(path: str) -> Dict[str, str]:
    """Create signed URLs to access all blobs under the path.

    Args:
        path: URL to a prefix, like `fd://bucket-name/some_directory/`

    Returns:
        Dictionary mapping from blob store key to signed HTTPS URL.

    Examples:
        ```python
        fused.sign_url_prefix("fd://bucket-name/table_directory/")
        ```
    """
    api = get_api()
    return api.sign_url_prefix(path)


def zip_tables(
    tables: Iterable[Union[Table, str]],
    *,
    read_sidecar: Union[Sequence[str], bool] = False,
) -> DatasetInputV2:
    """Create a job input that zips the columns of tables together. This takes the partitions from all the listed tables and combines them (as new columns) into a single DataFrame per chunk.

    Args:
        tables: The tables to zip together

    Keyword Args:
        read_sidecar: Whether to read sidecar information, either a sequence of table names (i.e. the last part of the table path) to read it from or a boolean which will be applied to all tables (default False).
    """
    return DatasetInputV2(
        tables=_create_table_objs(tables=tables, read_sidecar=read_sidecar),
        operation=DatasetInputV2Type.ZIP,
    )


def union_tables(
    tables: Iterable[Union[Table, str]],
    *,
    read_sidecar: Union[Sequence[str], bool] = False,
) -> DatasetInputV2:
    """Create a job input that unions the partitions of tables together. This takes the partitions from all the listed tables (which should have the same schema) and runs the operation over each partition.

    Args:
        tables: The tables to union together

    Keyword Args:
        read_sidecar: Whether to read sidecar information, either a sequence of table names (i.e. the last part of the table path) to read it from or a boolean which will be applied to all tables (default False).
    """
    return DatasetInputV2(
        tables=_create_table_objs(tables=tables, read_sidecar=read_sidecar),
        operation=DatasetInputV2Type.UNION,
    )


def load_job(path: Union[str, Path, BinaryIO]):
    @contextmanager
    def change_directory(path):
        if isinstance(path, (str, Path)):
            path_obj = Path(path)
        else:
            path_obj = path
        # Store the current working directory
        old_directory = os.getcwd()

        try:
            if not isinstance(path_obj, Path) or path_obj.is_file():
                # If .zip, create a temporary directory for zip.
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Extract the contents of the zip file.
                    with zipfile.ZipFile(path, "r") as zip_ref:
                        zip_ref.extractall(temp_dir)

                    os.chdir(temp_dir)
                    yield temp_dir

            else:
                os.chdir(path)
                yield
        finally:
            # Revert back to the original directory.
            os.chdir(old_directory)

    with change_directory(path):
        # Open and read the JSON file
        with Path("meta.json").open("r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

        # Validate the asset JSON and apply necessary migrations
        validated_job = CustomJobConfig(**data["job_config"])

        jobs = []
        for step in validated_job.steps:
            local_headers = [
                header["module_name"] + ".py" for header in step["udf"]["headers"]
            ]

            # TODO: Add type hint "List[DatasetInputBase]"
            # TODO: Switch to DatasetInputBase.parse_obj below
            input_params = []
            arg_list: Optional[Any] = None
            join_is_singlefile: Optional[bool] = None
            buffer_distance: Optional[float] = None
            join_how: Optional[str] = None
            if step["type"] == "join":
                input_params = [
                    RootAnyDatasetInput.model_validate(step["input_left"]).root,
                    RootAnyDatasetInput.model_validate(step["input_right"]).root,
                ]
                buffer_distance = step.get("buffer_distance")
                join_how = step.get("how")
            elif step["type"] == "map":
                input_params = [RootAnyDatasetInput.model_validate(step["input"]).root]
            elif step["type"] == "join_singlefile":
                input_params = [
                    RootAnyDatasetInput.model_validate(step["input_left"]).root,
                    step["input_right"],
                ]
                join_is_singlefile = True
            elif step["type"] == "udf":
                arg_list = step.get("input")
            udf_registry = fused_batch.experimental.load_udf(
                udf_paths=[step["udf"]["source"]], header_paths=local_headers
            )
            # TODO: Note this may misdetect if you try to read more than one UDF with the same entrypoint name
            detected_udf_name = (
                step["udf"]["name"]
                if step["udf"]["name"] in udf_registry
                else step["udf"]["entrypoint"]
            )
            # Materialize job with input parameters
            # Note this code is expected to not reload the output of the job
            job = udf_registry[detected_udf_name](
                *input_params,
                **step["udf"]["parameters"],
                buffer_distance=buffer_distance,
                join_is_singlefile=join_is_singlefile,
                **({"join_how": join_how} if join_how is not None else {}),
                arg_list=arg_list,
            )

            job.udf.metadata = step["udf"].get("metadata")
            job.metadata = step.get("metadata")

            # Materialize job and append
            jobs.append(job)

        job = fused_batch.experimental.job(jobs)
        job.metadata = (
            validated_job.metadata
        )  # TODO: job.export does not write this metadata

    assert isinstance(job, JobConfig)

    return job


def _is_valid_uuid(s: str) -> bool:
    try:
        uuid.UUID(s)
        return True
    except ValueError:
        return False
