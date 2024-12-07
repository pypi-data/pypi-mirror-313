from __future__ import annotations

import warnings
from pathlib import Path
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Sequence,
    Set,
    TextIO,
    Tuple,
    Union,
)

import geopandas as gpd
from pydantic import BaseModel, StrictBool, StrictStr

import fused_batch._public_api
from fused_batch._formatter.formatter_project import fused_project_repr
from fused_batch._global_api import get_api
from fused_batch._options import options as OPTIONS
from fused_batch._str_utils import append_url_part, table_to_name
from fused_batch.models.api import (
    Dataset,
    GeospatialPartitionJobStepConfig,
    JoinJobStepConfig,
    MapJobStepConfig,
    NonGeospatialPartitionJobStepConfig,
    Table,
)
from fused_batch.models.api.job import GDALOpenConfig, JoinType
from fused_batch.models.internal.dataset import (
    DatasetInputV2,
    DatasetInputV2Table,
    DatasetInputV2Type,
    DatasetOutputV2,
)
from fused_batch.models.schema import Schema
from fused_batch.models.udf import AnyBaseUdf
from fused_batch.models.urls import DatasetUrl
from fused_batch.warnings import (
    FusedIgnoredWarning,
    FusedPathWarning,
    FusedRefreshingWarning,
)


class Project(BaseModel):
    """A project represents a collection of tables or directories of files in blob storage.

    Tables and folders under this project may be accessed with attribute or subscript operator.
    For example, all of the following will have the same result:

    ```py
    project.tables['my_table_name']

    project.my_table_name

    project['my_table_name']
    ```
    """

    root_base_path: DatasetUrl
    """The base path of the overall project."""
    base_path: DatasetUrl
    """The base path of the project folder, which tables in it are relative to. This may be different
    than `root_base_path` if this Project instance is a folder (sub-project) of an overall project."""

    tables: Dict[StrictStr, Table]
    """Tables in this project."""
    folders: Dict[StrictStr, Project]
    """Project folders in this project."""
    virtual_folders: List[StrictStr]
    """Project folders in this project that have not been materialized.

    Accessing one of these through `project[virtual_folder_name]` will result in automatic
    loading of that folder to a `Project` instance.
    """

    # The following are settings that were used to open the project and the user shouldn't
    # need to change. Modifying them after opening a project will only take effect in case
    # of `refresh()`.
    fetch_table_metadata: Optional[StrictBool] = None
    fetch_minimal_table_metadata: Optional[StrictBool] = None
    fetch_samples: Optional[StrictBool] = None

    def _getitem_internal(self, key: str) -> Union[Project, Table, None]:
        if key in self.tables:
            # If a table and a folder are both specified, the table takes precedence
            return self.tables[key]
        elif key in self.folders:
            return self.folders[key]
        elif key in self.virtual_folders:
            return self._materialize_virtual_folder(key)
        else:
            # TODO: Allow specifying random paths
            return None

    def __getitem__(self, key: str) -> Union[Project, Table]:
        ret = self._getitem_internal(key)
        if ret is None:
            if OPTIONS.open.auto_refresh_project and not key.startswith("_"):
                # Do not do the refresh for keys that start with _ because IPython
                # will probe a number of attributes (such as the _ipython_canary...
                # attribute) when rendering an object. This will make the repr take a
                # very long time.
                warnings.warn(
                    f"Refreshing project because key {key} was not found",
                    FusedRefreshingWarning,
                )
                self.refresh()

                # Try again:
                ret = self._getitem_internal(key)

            if ret is None:
                # Check again because ret may have been modified by auto_refresh_project,
                # above.
                raise KeyError(f"Key {key} not found")
        return ret

    def __getattribute__(self, key) -> Union[Project, Table]:
        try:
            return super().__getattribute__(key)
        except AttributeError:
            try:
                return self[key]
            # Note that we need to raise an AttributeError, **not a KeyError** so that
            # IPython's _repr_html_ works here
            except KeyError:
                raise AttributeError(
                    f"object of type {type(self).__name__} has no attribute {key}"
                ) from None

    def _repr_html_(self):
        return fused_project_repr(self)

    def __dir__(self) -> List[str]:
        # Provide method name lookup and completion. Only provide 'public'
        # methods.
        # This enables autocompletion
        # Pydantic methods to remove in __dir__
        PYDANTIC_METHODS = {
            "Config",
            "construct",
            "copy",
            "from_orm",
            "json",
            "parse_file",
            "parse_obj",
            "schema",
            "schema_json",
            "update_forward_refs",
            "validate",
        }
        EXTRA_METHODS = {
            "fetch_table_metadata",
            "fetch_minimal_table_metadata",
            "fetch_samples",
        }

        extra_attrs = set(self.tables.keys()) | set(
            self.folders.keys() | set(self.virtual_folders)
        )
        normal_dir = {
            name
            for name in dir(type(self))
            if (
                not name.startswith("_")
                and name not in PYDANTIC_METHODS
                and name not in EXTRA_METHODS
            )
        }
        pydantic_fields = set(self.model_fields.keys())
        return sorted(normal_dir | pydantic_fields | extra_attrs)

    def _ipython_key_completions_(self) -> List[str]:
        # https://ipython.readthedocs.io/en/stable/config/integrating.html#tab-completion
        return sorted(
            set(self.tables.keys())
            | set(self.folders.keys() | set(self.virtual_folders))
        )

    def _materialize_all_virtual_folders(self) -> Iterable[Project]:
        to_materialize = [*self.virtual_folders]
        for key in to_materialize:
            yield self._materialize_virtual_folder(key)

    def _materialize_virtual_folder(self, folder_name: str) -> Project:
        self.virtual_folders.remove(folder_name)
        new_folder = open_project(
            append_url_part(self.base_path, folder_name),
            _fetch_minimal_table_metadata=self.fetch_minimal_table_metadata,
            fetch_table_metadata=self.fetch_table_metadata,
            fetch_samples=self.fetch_samples,
        )
        self.folders[folder_name] = new_folder
        return new_folder

    def tree(self, file: TextIO = None) -> None:
        """Print a tree representation of this project.

        Args:
            file: File-like object to write to. Defaults to `None` for `sys.stdout`.
        """

        def _print_tree(project: Project, indent: int):
            prefix = ("|   " * (indent - 1)) + "|-- "
            for name in project.tables.keys():
                print(f"{prefix}{name}", file=file)
            for name, folder in project.folders.items():
                print(f"{prefix}{name}", file=file)
                _print_tree(folder, indent + 1)
            for name, folder in project.virtual_folders:
                print(f"{prefix}{name} (virtual)", file=file)

        print(self.base_path, file=file)
        _print_tree(self, 1)

    def refresh(
        self,
        *,
        fetch_table_metadata: Optional[bool] = None,
        fetch_samples: Optional[bool] = None,
        _fetch_minimal_table_metadata: Optional[bool] = None,
    ) -> Project:
        """Returns this project with updated metadata

        Keyword args, if specified, will change how the project loads metadata. This can be used to reload a project
        with metadata, after it is initially loaded without metadata.

        Keyword Args:
            fetch_table_metadata: If True, fetch metadata on each table.
            fetch_samples: If True, fetch sample on each table.
        """
        if fetch_table_metadata is not None:
            self.fetch_table_metadata = fetch_table_metadata
        if fetch_samples is not None:
            self.fetch_samples = fetch_samples
        if _fetch_minimal_table_metadata is not None:
            self.fetch_minimal_table_metadata = _fetch_minimal_table_metadata

        new_self = open_project(
            self.base_path,
            _fetch_minimal_table_metadata=self.fetch_minimal_table_metadata,
            fetch_table_metadata=self.fetch_table_metadata,
            fetch_samples=self.fetch_samples,
        )
        self.tables = new_self.tables
        self.folders = new_self.folders
        self.virtual_folders = new_self.virtual_folders
        return self

    def path(self, path: str) -> str:
        """Returns the path to an item under this project."""
        return append_url_part(self.base_path, path)

    def project(self, path: str) -> Project:
        """Open a subproject of this project."""
        if path in self.folders:
            return self.folders[path]
        elif path in self.virtual_folders:
            return self._materialize_virtual_folder(path)
        else:
            return Project(
                base_path=self.path(path),
                tables={},
                folders={},
                fetch_minimal_table_metadata=self.fetch_minimal_table_metadata,
                fetch_table_metadata=self.fetch_table_metadata,
                fetch_samples=self.fetch_samples,
            )

    def open_table(
        self,
        path: Union[str, DatasetOutputV2],
        *,
        fetch_samples: Optional[bool] = None,
    ) -> Table:
        """Open a Table object given a path to the root of the table

        Args:
            path: The path to the root of the table on remote storage

        Keyword Args:
            fetch_samples: If True, fetch sample on each table when getting dataset metadata.

        Example:

            table = project.open_table("path/to/dataset/table/")

        Returns:
            A Table object
        """
        if isinstance(path, str):
            path = self.path(path)
        elif isinstance(path, DatasetOutputV2):
            path = path.url

        return fused_batch._public_api.open_table(
            path=path,
            fetch_samples=fetch_samples,
        )

    def ingest(
        self,
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
            target_num_chunks: The target for the number of chunks if `partitioning_maximum_per_file` is None. Note that this number is only a _target_ and the actual number of files and chunks generated can be higher or lower than this number, depending on the spatial distribution of the data itself.
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
        # TODO: Support input being resolved
        project_output = self.path(output) if output else None
        project_output_metadata = (
            self.path(output_metadata) if output_metadata else None
        )
        return fused_batch._public_api.ingest(
            input=input,
            output=project_output,
            output_metadata=project_output_metadata,
            schema=schema,
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
            gdal_config=gdal_config,
        )

    def ingest_nongeospatial(
        self,
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
        project_output = self.path(output) if output else None
        project_output_metadata = (
            self.path(output_metadata) if output_metadata else None
        )
        return fused_batch._public_api.ingest_nongeospatial(
            input=input,
            output=project_output,
            output_metadata=project_output_metadata,
            partition_col=partition_col,
            partitioning_maximum_per_file=partitioning_maximum_per_file,
            partitioning_maximum_per_chunk=partitioning_maximum_per_chunk,
        )

    def map(
        self,
        dataset: Union[str, Dataset, Table],
        output_table: Optional[str] = None,
        udf: Union[AnyBaseUdf, None] = None,
        *,
        cache_locally: bool = False,
    ) -> MapJobStepConfig:
        """Construct a `map` config from this Dataset

        Args:
            output_table: Where to save the output of this operation. Defaults to `None`, which will not save the output.
            udf: A user-defined function to run in this map. Defaults to None.

        Keyword Args:
            tables: The attribute tables to include in the map reduce. Defaults to ("main",).
            cache_locally: Advanced: whether to cache all the partitions locally in the map job. Defaults to False.

        Returns:
            An object describing the map configuration.
        """
        if isinstance(dataset, str):
            dataset = self.open_table(
                dataset,
                fetch_samples=False,
            )

        return dataset.map(
            output_table=output_table,
            udf=udf,
            cache_locally=cache_locally,
        )

    def join(
        self,
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
        """Construct a join config from two datasets

        Args:
            other: The other Dataset object to join on
            output_table: Where to save the output of this operation. Defaults to `None`, which will not save the output.
            udf: The user-defined function to run in the join

        Keyword Args:
            how: The manner of doing the join. Currently  Defaults to "inner".
            left_tables: The names of the attribute tables on the left side to include in the join.
            right_tables: The names of the attribute tables on the left side to include in the join.
            left_cache_locally: Whether to cache the left dataset locally in the join. Defaults to False.
            right_cache_locally: Whether to cache the right dataset locally in the join. Defaults to False.
            buffer_distance: The size of the buffer (in meters) on the left table to use during the join. Defaults to None.

        Examples:
            ```py
            import fused

            left_dataset = fused.open("s3://bucket/path/to/dataset")
            other_dataset = fused.open("s3://bucket/path/to/dataset")
            join_config = left_dataset.join(other_dataset)
            ```

        Returns:
            An object describing the join configuration.
        """
        if isinstance(dataset, str):
            dataset = self.open_table(dataset, fetch_samples=False)

        if isinstance(other, str):
            other = self.open_table(other, fetch_samples=False)

        return dataset.join(
            other=other,
            output_table=output_table,
            udf=udf,
            how=how,
            left_cache_locally=left_cache_locally,
            right_cache_locally=right_cache_locally,
            buffer_distance=buffer_distance,
        )

    def delete(
        self,
        path: str,
        max_deletion_depth: Union[int, Literal["unlimited"]] = 2,
    ) -> bool:
        """Delete the files at the path.

        Args:
            path: Directory or file to delete, like `my-old-table/`
            max_deletion_depth: If set (defaults to 2), the maximum depth the operation will recurse to.
                                This option is to help avoid accidentally deleting more data that intended.
                                Pass `"unlimited"` for unlimited.
        """
        project_path = self.path(path) if path is not None else self.base_path
        return fused_batch._public_api.delete(
            project_path, max_deletion_depth=max_deletion_depth
        )

    def list(self, path: Optional[str] = None) -> List[str]:
        """List the files at the path.

        Args:
            path: Parent directory, like `table_name`. Defaults to None to list the root of the project.

        Returns:
            A list of paths as URLs
        """
        project_path = self.path(path) if path is not None else self.base_path
        return fused_batch._public_api.list(project_path)

    def get(self, path: str) -> bytes:
        """Download the contents at the path to memory.

        Args:
            path: Path to a file, like `table_name/file.parquet`

        Returns:
            bytes of the file
        """
        project_path = self.path(path)
        return fused_batch._public_api.get(project_path)

    def download(self, path: str, local_path: Union[str, Path]) -> None:
        """Download the contents at the path to disk.

        Args:
            path: Path to a file, like `table_name/file.parquet`
            local_path: Path to a local file.
        """
        project_path = self.path(path)
        return fused_batch._public_api.download(project_path, local_path=local_path)

    def sign_url(self, path: str) -> str:
        """Create a signed URL to access the path.

        This function may not check that the file represented by the path exists.

        Args:
            path: Path to a file, like `table_name/file.parquet`

        Returns:
            HTTPS URL to access the file using signed access.
        """
        project_path = self.path(path)
        return fused_batch._public_api.sign_url(project_path)

    def sign_url_prefix(self, path: str) -> Dict[str, str]:
        """Create signed URLs to access all blobs under the path.

        Args:
            path: Path to a prefix, like `table_name/`

        Returns:
            Dictionary mapping from blob store key to signed HTTPS URL.
        """
        project_path = self.path(path)
        return fused_batch._public_api.sign_url_prefix(project_path)

    def _table_to_v2_table(
        self,
        table: Union[Table, str],
        *,
        read_sidecar: Union[Sequence[str], bool] = False,
    ) -> DatasetInputV2Table:
        table_url = table.url if isinstance(table, Table) else self.path(table)
        table_name = table_to_name(table_url)
        read_sidecar_bool = read_sidecar is not None and (
            read_sidecar
            if isinstance(read_sidecar, bool)
            else (table_name in read_sidecar)
        )
        return DatasetInputV2Table(
            url=table_url,
            read_sidecar_files=read_sidecar_bool,
        )

    def _create_table_objs(
        self,
        tables: Iterable[Union[Table, str]],
        read_sidecar: Union[Sequence[str], bool] = False,
    ):
        ret = [self._table_to_v2_table(t, read_sidecar=read_sidecar) for t in tables]

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

    def sel(
        self,
        tables: Union[Iterable[Union[Table, str]], Table, str, None] = None,
        *,
        read_sidecar: Union[Sequence[str], bool] = False,
        how: Optional[Union[str, DatasetInputV2Type]] = None,
        **kwargs,
    ) -> DatasetInputV2:
        """Create a job input that zips or unions tables together

        Args:
            tables: The names of tables to include in the input, e.g. `["table_0", "table_1", "table_5"]`.

        Keyword Args:
            read_sidecar: Whether to read sidecar information, either a sequence of table names (i.e. the last part
                          of the table path) to read it from or a boolean which will be applied to all tables (default False).
            how: The operation used to combine multiple input tables. This may be either `"zip"` or `"union"`.
                 By default this will be `"zip"` when `tables` is specified, `"union"` otherwise. This corresponds
                 with `fused.zip_tables` and `fused.union_tables` respectively.
        """
        default_how = DatasetInputV2Type.ZIP

        if len(kwargs) > 1 or (len(kwargs) == 1 and tables is not None):
            raise ValueError(
                "Too many keyword arguments passed in to fused.sel. There should only be a single `partition_name=values` argument."
            )

        if len(kwargs) == 0 and tables is None:
            raise ValueError(
                "No tables selected. Pass `tables=values` or `partition_name=values`."
            )

        if len(kwargs) == 1:
            default_how = DatasetInputV2Type.UNION

            assert tables is None
            kv_name = next(iter(kwargs.keys()))
            if isinstance(kwargs[kv_name], str):
                tables = [f"{kv_name}={kwargs[kv_name]}"]
            else:
                tables = [f"{kv_name}={kv_value}" for kv_value in kwargs[kv_name]]
        elif isinstance(tables, str) or isinstance(tables, Table):
            tables = [tables]

        if how is None:
            how = default_how

        if isinstance(how, str):
            how = DatasetInputV2Type(how)

        input = DatasetInputV2(
            tables=self._create_table_objs(tables=tables, read_sidecar=read_sidecar),
            operation=how,
        )
        input._project_url = self.root_base_path
        return input

    def isel(
        self,
        tables: Union[Iterable[int], int],
        *,
        read_sidecar: Union[Sequence[bool], bool] = False,
        how: Optional[Union[str, DatasetInputV2Type]] = None,
    ) -> DatasetInputV2:
        """Create a job input that zips or unions tables together, by their integer index. Tables
        are implicitly ordered by name.

        Args:
            tables: The index of tables to include in the input, e.g. `[0, 1, 5]`.

        Keyword Args:
            read_sidecar: Whether to read sidecar information, either a sequence of table names (i.e. the last part
                          of the table path) to read it from or a boolean which will be applied to all tables (default False).
            how: The operation used to combine multiple input tables. This may be either `"zip"` or `"union"`.
                 This corresponds with `fused.zip_tables` and `fused.union_tables` respectively. Defaults to `"zip"`.
        """
        default_how = DatasetInputV2Type.ZIP

        if how is None:
            how = default_how

        if isinstance(how, str):
            how = DatasetInputV2Type(how)

        table_names = sorted(self.tables.keys())
        read_sidecar = (
            ([read_sidecar] * len(table_names))
            if isinstance(read_sidecar, bool)
            else read_sidecar
        )

        input = DatasetInputV2(
            tables=self._create_table_objs(tables=tables, read_sidecar=read_sidecar),
            operation=how,
        )
        input._project_url = self.root_base_path
        return input


def open_project(
    path: str,
    *,
    lazy: bool = False,
    fetch_table_metadata: Optional[bool] = None,
    fetch_samples: Optional[bool] = None,
    _fetch_minimal_table_metadata: Optional[bool] = None,
    _max_depth: Optional[int] = 1,
    _eager: bool = False,
) -> Project:
    """Open a project folder.

    Args:
        path: Path to the project folder, e.g. `"s3://bucket-name/project-name/"`
        lazy: If True, no metadata about the project is loaded.
        fetch_table_metadata: This is passed on to the `Table` open calls.
        fetch_samples: This is passed on to the `Table` open calls.
        _fetch_minimal_table_metadata: If True and fetch_table_metadata is also True,
                                       a reduced set of Table metadata will be fetched.
        _max_depth: Maximum depth of folders to load.
        _eager: If True, recursive calls will be made to materialize all virtual
                folders that `max_depth` would otherwise cause.
    """
    if lazy:
        return Project(base_path=path, tables=[], folders=[])

    # TODO: Other values are not supported because the code for adding virtual folders
    # needs to be improved for it. Both where the virtual folders are added in the tree
    # and how to imlpement "eager" DFS mode.
    assert _max_depth is None or _max_depth == 1, "max_depth may only be None or 1"

    api = get_api()
    folder = api.open_folder(
        path=path,
        fetch_minimal_table_metadata=_fetch_minimal_table_metadata,
        fetch_table_metadata=fetch_table_metadata,
        fetch_samples=fetch_samples,
        max_depth=_max_depth,
    )

    all_tables = folder.tables

    # Create a prefix tree for the project
    project_tree: Dict[str, Any] = {}
    resolved_path = path if folder.base_path is None else folder.base_path

    for table in sorted(all_tables, key=lambda ds: ds.url):
        table_path = table.url
        if table_path.startswith(resolved_path):
            table_path = table_path[len(resolved_path) :]
            path_parts = table_path.strip("/").split("/")

            curr_tree_node = project_tree
            do_not_set = False
            for path_part in path_parts[:-1]:
                if path_part not in curr_tree_node:
                    curr_tree_node[path_part] = {}
                elif isinstance(curr_tree_node[path_part], Table):
                    # Note: if there is both a dataset and a folder,
                    # it will be shadowed by the dataset
                    warnings.warn(
                        f"Table {table.url} is nested within another table",
                        FusedPathWarning,
                    )
                    do_not_set = True
                    break
                curr_tree_node = curr_tree_node[path_part]

            if not do_not_set:
                curr_tree_node[path_parts[-1]] = table
        else:
            warnings.warn(f"Table path {table_path} is invalid", FusedPathWarning)

    # In "eager" mode, the frontend does DFS to materialize folders. This reduces the
    # pressure of each backend call (hopefully to within a reasonable timeout) while
    # allowing the frontend to get the whole data.
    def _recursive_eager_materialize(pr: Project):
        # note that non-virtual folders are not recursed into, so this also requires
        # max_depth=1.
        for folder in pr._materialize_all_virtual_folders():
            _recursive_eager_materialize(folder)

    # Convert the prefix tree into a tree of Project objects
    def _recursive_create_project(
        base_path: str, tree, additional_folders: Optional[Sequence[str]] = None
    ):
        tables: Dict[str, Table] = {}
        folders: Dict[str, Project] = {}
        all_names: Set[str] = set()
        for key, val in tree.items():
            all_names.add(key)
            if isinstance(val, Table):
                tables[key] = val
                val._project_url = path
            else:
                folders[key] = _recursive_create_project(f"{base_path}/{key}", val)
        # Any folder that hasn't been added as something else means there was
        # another object there that we could materialize.
        virtual_folders = (
            [key for key in additional_folders if key not in all_names]
            if additional_folders
            else []
        )
        ret = Project(
            root_base_path=path,
            base_path=base_path,
            tables=tables,
            folders=folders,
            virtual_folders=virtual_folders,
            fetch_minimal_table_metadata=_fetch_minimal_table_metadata,
            fetch_table_metadata=fetch_table_metadata,
            fetch_samples=fetch_samples,
        )
        if _eager:
            _recursive_eager_materialize(ret)
        return ret

    return _recursive_create_project(path, project_tree, folder.folders)
