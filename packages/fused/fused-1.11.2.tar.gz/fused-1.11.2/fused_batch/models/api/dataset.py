from __future__ import annotations

import os
import warnings
from collections import defaultdict
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Dict, List, Literal, Optional, Sequence, Set, Tuple, Union

import geopandas as gpd
import pandas as pd
import pyarrow as pa
from pydantic import (
    ConfigDict,
    Field,
    PrivateAttr,
    StrictStr,
    field_validator,
    model_validator,
)

from fused_batch._constants import DEFAULT_TABLE_NAMES
from fused_batch._formatter.formatter_dataset import (
    fused_dataset_repr,
    fused_table_repr,
)
from fused_batch._options import options as OPTIONS
from fused_batch.models._project_aware import FusedProjectAware
from fused_batch.models.api.enums import JoinType
from fused_batch.models.api.job import (
    AnyJobStepConfig,
    JoinJobStepConfig,
    JoinSinglefileJobStepConfig,
    MapJobStepConfig,
    _get_chunk,
    _get_chunk_v2,
    _get_file,
)
from fused_batch.models.base import FusedBaseModel
from fused_batch.models.internal.dataset import (
    DatasetInput,
    DatasetInputV2,
    DatasetOutput,
    DatasetOutputV2,
)
from fused_batch.models.schema import Schema
from fused_batch.models.udf.common import ChunkMetadata
from fused_batch.models.udf.udf import EMPTY_UDF, AnyBaseUdf
from fused_batch.models.urls import dataset_url_schema_validator
from fused_batch.warnings import FusedDefaultWarning, FusedRefreshingWarning

from ..request import WHITELISTED_INSTANCE_TYPES


class JobMetadata(FusedBaseModel):
    ec2_instance_type: Optional[WHITELISTED_INSTANCE_TYPES] = None
    """The EC2 instance this job is run on."""

    step_config: AnyJobStepConfig
    time_taken: Optional[float] = None
    """The time taken for the job, if known."""

    job_id: Optional[str] = None
    """The fused id for the job."""

    @property
    def job(self) -> AnyJobStepConfig:
        """The job step config that created this table."""
        return self.step_config

    @property
    def udf(self) -> Optional[AnyBaseUdf]:
        """The user-defined function that created this table."""
        if hasattr(self.step_config, "udf"):
            return self.step_config.udf

        return None

    @property
    def udf_code(self) -> Optional[str]:
        """The code string of the user-defined function that created this table."""
        udf = self.udf
        if udf is not None:
            return udf.code

        return None

    @property
    def inputs(self) -> Tuple[DatasetInput, ...]:
        """The datasets that were combined to create this table."""
        if hasattr(self.step_config, "input"):
            return (self.step_config.input,)

        if hasattr(self.step_config, "input_left") and hasattr(
            self.step_config, "input_right"
        ):
            return (self.step_config.input_left, self.step_config.input_right)

        return tuple()

    # We ignore extra keys because some keys are only useful for the backend
    model_config = ConfigDict(extra="ignore")


class Table(FusedBaseModel, FusedProjectAware):
    url: Optional[str] = None
    """URL of the table."""

    name: Optional[str] = None
    """The name of the table."""

    table_schema: Schema
    """The Schema representing this table."""

    parent: Optional[JobMetadata] = None
    """Metadata for the job that created this table."""

    column_names: List[StrictStr]
    """The list of column names in the table."""

    num_rows: Optional[int] = None
    """The number of rows in the table."""

    num_files: Optional[int] = None
    """The number of **non-empty** files."""

    num_chunks: Optional[int] = None
    """The number of **non-empty** chunk."""

    status: Optional[str] = None
    """A status of the table."""

    sample: Optional[pd.DataFrame] = Field(None, repr=False)

    chunk_metadata: Optional[List[ChunkMetadata]] = Field(..., repr=False)
    """Descriptive information about each chunk in this table"""

    _dataset: Optional["Dataset"] = PrivateAttr(None)

    @model_validator(mode="before")
    @classmethod
    def _default_name_from_url(cls, values):
        if "url" in values and "name" not in values:
            values["name"] = values["url"].rstrip("/").rsplit("/", maxsplit=1)[1]
        return values

    @property
    def columns(self) -> List[str]:
        """The list of columns in this table"""
        return self.column_names

    @property
    def metadata_gdf(self) -> gpd.GeoDataFrame:
        """The metadata of all chunks as a GeoDataFrame"""
        if self.chunk_metadata:
            return gpd.GeoDataFrame(
                [chunk.model_dump() for chunk in self.chunk_metadata],
                geometry=[chunk.to_box() for chunk in self.chunk_metadata],
            )
        else:
            raise ValueError("No chunk metadata loaded")

    def get_chunk(
        self, file_id: str | int | None = None, chunk_id: int | None = None
    ) -> gpd.GeoDataFrame:
        """Fetch a single chunk from this table

        Args:
            file_id: The identifier of this file. Defaults to None.
            chunk_id: The numeric index of the chunk within the file to fetch. Defaults to None.

        Returns:

            A `DataFrame` retrieved from the given file, chunk, and tables.
        """
        if self._dataset:
            return self._dataset.get_chunk(
                file_id=file_id, chunk_id=chunk_id, tables=[self.name]
            )
        elif self.url:
            return _get_chunk_v2(url=self.url, file_id=file_id, chunk_id=chunk_id)

        raise NotImplementedError("self._dataset and self.url are not set")

    def get_dataframe(
        self,
        file_id: str | int | None = None,
        chunk_id: int | None = None,
        parallel_fetch: bool = True,
    ) -> gpd.GeoDataFrame:
        """Fetch multiple chunks from this table as a dataframe

        Args:
            file_id: The identifier of the file to download. If `None` is passed, all files will be chosen. Defaults to 0.
            chunk_id: The numeric index of the chunk within the file to fetch. If `None` is passed, all chunks for the given file(s) will be chosen. Defaults to 0.
            parallel_fetch: Fetch in parallel. Defaults to True.

        Raises:
            ValueError: If the function would fetch more than `max_rows` rows.

        Returns:
            A `DataFrame` with all chunks concatenated together.
        """
        if self._dataset:
            return self._dataset.get_dataframe(
                file_id=file_id,
                chunk_id=chunk_id,
                tables=[self.name],
                parallel_fetch=parallel_fetch,
            )
        elif self.url:
            # TODO: Improve this and don't use a fake dataset. This will not work
            # if e.g. the table is at the root of a volume.
            dataset_base_path = self.url.rstrip("/").rsplit("/", maxsplit=1)[0]

            if self.chunk_metadata is None:
                warnings.warn(
                    "Refreshing project because chunk metadata was not found.",
                    FusedRefreshingWarning,
                )
                self.refresh()

            dataset = Dataset(base_path=dataset_base_path, tables={self.name: self})
            return dataset.get_dataframe(
                file_id=file_id,
                chunk_id=chunk_id,
                tables=[self.name],
                parallel_fetch=parallel_fetch,
            )

        raise NotImplementedError("self._dataset and self.url are not set")

    def get_dataframe_bbox(
        self,
        minx: float,
        miny: float,
        maxx: float,
        maxy: float,
        n_rows: Optional[int] = None,
        columns: Optional[List[str]] = None,
        clip: bool = True,
        buffer: Optional[float] = None,
    ) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
        """Get a DataFrame of this Table of data in partitions matching the bounding box.

        Args:
            minx: Left coordinate of the box.
            miny: Bottom coordinate of the box.
            maxx: Right coordinate of the box.
            maxy: Top coordinate of the box.
            n_rows: If not None, up to this many rows will be returned.
            columns: If not None, only return these columns.
            clip: If True, only geometries that intersect the bounding box will be returned.
            buffer: If not None, this will be applied as the buffer for the partitions.
        """
        return self._api.download_table_bbox(
            path=self.url,
            minx=minx,
            miny=miny,
            maxx=maxx,
            maxy=maxy,
            n_rows=n_rows,
            columns=columns,
            clip=clip,
            buffer=buffer,
        )

    def join(
        self,
        other: Union[Table, str],
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
            other: The other Dataset object to join on, or a path to another dataset object.
            output_table: Where to save the output of this operation. Defaults to `None`, which will not save the output.
            udf: The user-defined function to run in the join.

        Keyword Args:
            how: The manner of doing the join. Currently  Defaults to "inner".
            left_cache_locally: Whether to cache the left dataset locally in the join. Defaults to False.
            right_cache_locally: Whether to cache the right dataset locally in the join. Defaults to False.
            buffer_distance: The size of the buffer (in meters) on the left table to use during the join. Defaults to None.

        Examples:
            ```py
            import fused

            left_table = fused.open_table("s3://bucket/path/to/table")
            other_table = fused.open_table("s3://bucket/path/to/table")
            join_config = left_table.join(other_table)
            ```

        Returns:
            An object describing the join configuration.
        """
        parsed_udf = Dataset._parse_udf(udf)

        if isinstance(other, str):
            other = self._api.open_table(
                other,
                fetch_samples=False,
            )

        input_left = DatasetInputV2.from_table_url(
            self.url,
            cache_locally=left_cache_locally,
        )
        input_right = DatasetInputV2.from_table_url(
            other.url,
            cache_locally=right_cache_locally,
        )
        output = DatasetOutputV2(url=output_table)

        join_config = JoinJobStepConfig(
            udf=parsed_udf,
            input_left=input_left,
            input_right=input_right,
            output=output,
            buffer_distance=buffer_distance,
            how=how,
        )
        return join_config

    def join_singlefile(
        self,
        other: str,
        output_table: Optional[str] = None,
        udf: Union[AnyBaseUdf, None] = None,
        *,
        left_cache_locally: bool = False,
        buffer_distance: Optional[float] = None,
    ) -> JoinJobStepConfig:
        """Construct a join config from a dataset and a Parquet file URL.

        Args:
            other: The URL to the Parquet file to join all chunks with.
            output_table: Where to save the output of this operation. Defaults to `None`, which will not save the output.
            udf: The user-defined function to run in the join

        Keyword Args:
            left_cache_locally: Whether to cache the left dataset locally in the join. Defaults to False.

        Examples:
            ```py
            left_table = fused.open_table("s3://bucket/path/to/table")
            other_file = "s3://bucket/path/to/file.parquet"
            join_config = left_table.join_singlefile(other_file)
            ```

        Returns:
            An object describing the join configuration.
        """
        parsed_udf = Dataset._parse_udf(udf)

        input_left = DatasetInputV2.from_table_url(
            self.url,
            cache_locally=left_cache_locally,
        )
        output = DatasetOutputV2(url=output_table)

        join_config = JoinSinglefileJobStepConfig(
            udf=parsed_udf,
            input_left=input_left,
            input_right=other,
            output=output,
            buffer_distance=buffer_distance,
        )
        return join_config

    def map(
        self,
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
            cache_locally: Advanced: whether to cache all the partitions locally in the map job. Defaults to False.

        Returns:
            An object describing the map configuration.
        """
        parsed_udf = Dataset._parse_udf(udf)

        dataset_input = DatasetInputV2.from_table_url(
            self.url,
            cache_locally=cache_locally,
        )
        output = DatasetOutputV2(url=output_table)

        map_config = MapJobStepConfig(
            udf=parsed_udf,
            input=dataset_input,
            output=output,
        )
        return map_config

    def _repr_html_(self) -> str:
        return fused_table_repr(self)

    def refresh(self, fetch_samples: Optional[bool] = None) -> Table:
        """Returns this table with updated metadata"""
        should_fetch_samples = False
        if fetch_samples is not None:
            should_fetch_samples = fetch_samples
        elif OPTIONS.open.fetch_samples is not None:
            should_fetch_samples = OPTIONS.open.fetch_samples

        new_table = self._api.open_table(
            path=self.url,
            fetch_samples=should_fetch_samples,
        )

        # Update self with all fields of new_table
        for key in new_table.model_dump().keys():
            value = getattr(new_table, key)
            setattr(self, key, value)

        return self

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Dataset(FusedBaseModel, FusedProjectAware):
    """A class to describe everything that exists for a dataset in an environment"""

    base_path: StrictStr
    """The path on object storage where this dataset is stored"""

    tables: Dict[StrictStr, Optional[Table]] = Field(default_factory=dict)
    """The names of one or more attribute tables in this dataset"""

    def __getattribute__(self, key):
        try:
            return super().__getattribute__(key)
        except AttributeError:
            try:
                return self.tables[key]
            # Note that we need to raise an AttributeError, **not a KeyError** so that
            # IPython's _repr_html_ works here
            except KeyError:
                raise AttributeError(
                    f"object of type {type(self).__name__} has no attribute {key}"
                ) from None

    def __dir__(self) -> List[str]:
        """Provide method name lookup and completion. Only provide 'public'
        methods.
        """
        # This enables autocompletion
        extra_attrs = set(self.tables.keys())
        normal_dir = set(dir(type(self)))
        pydantic_fields = set(self.model_fields.keys())
        return sorted(normal_dir | pydantic_fields | extra_attrs)

    @field_validator("base_path")
    @classmethod
    def validate_base_path(cls, val):
        dataset_url_schema_validator.validate_python(val)
        return val

    @field_validator("tables")
    @classmethod
    def _validate_tables(cls, v):
        for name, table in v.items():
            if table is not None:
                table.name = name
        return v

    def _add_table_up_refs(self):
        for name, table in self.tables.items():
            # name is reset here just to be safe
            if table is not None:
                table.name = name
                table._dataset = self

    def join(
        self,
        other: Union[Dataset, str],
        output_table: Optional[str] = None,
        udf: Union[AnyBaseUdf, None] = None,
        *,
        how: Union[JoinType, Literal["left", "inner"]] = "inner",
        left_tables: Sequence[str] = DEFAULT_TABLE_NAMES,
        right_tables: Sequence[str] = DEFAULT_TABLE_NAMES,
        left_cache_locally: bool = False,
        right_cache_locally: bool = False,
        buffer_distance: Optional[float] = None,
    ) -> JoinJobStepConfig:
        """Construct a join config from two datasets

        Args:
            other: The other Dataset object to join on, or a path to another dataset object.
            output_table: Where to save the output of this operation. Defaults to `None`, which will not save the output.
            udf: The user-defined function to run in the join.

        Keyword Args:
            how: The manner of doing the join. Currently  Defaults to "inner".
            left_tables: The names of the attribute tables on the left side to include in the join. Defaults to ("main",).
            right_tables: The names of the attribute tables on the left side to include in the join. Defaults to ("main",).
            left_cache_locally: Whether to cache the left dataset locally in the join. Defaults to False.
            right_cache_locally: Whether to cache the right dataset locally in the join. Defaults to False.
            buffer_distance: The size of the buffer (in meters) on the left table to use during the join. Defaults to None.

        Examples:
            ```py
            import fused

            left_table = fused.open_table("s3://bucket/path/to/table")
            other_table = fused.open_table("s3://bucket/path/to/table")
            join_config = left_table.join(other_table)
            ```

        Returns:
            An object describing the join configuration.
        """
        parsed_udf = Dataset._parse_udf(udf)

        if isinstance(other, str):
            other = self._api.open_table(other, fetch_samples=False)

        self._validate_output(output_table)

        left_tables = [table for table in left_tables if table in self.tables]
        right_tables = [table for table in right_tables if table in other.tables]
        input_left = DatasetInput(
            base_path=self.base_path,
            tables=left_tables,
            cache_locally=left_cache_locally,
        )
        input_right = DatasetInput(
            base_path=other.base_path,
            tables=right_tables,
            cache_locally=right_cache_locally,
        )
        output = DatasetOutput(table=output_table)

        join_config = JoinJobStepConfig(
            udf=parsed_udf,
            input_left=input_left,
            input_right=input_right,
            output=output,
            buffer_distance=buffer_distance,
            how=how,
        )
        return join_config

    def join_singlefile(
        self,
        other: str,
        output_table: Optional[str] = None,
        udf: Union[AnyBaseUdf, None] = None,
        *,
        left_tables: Sequence[str] = DEFAULT_TABLE_NAMES,
        left_cache_locally: bool = False,
        buffer_distance: Optional[float] = None,
    ) -> JoinJobStepConfig:
        """Construct a join config from a dataset and a Parquet file URL.

        Args:
            other: The URL to the Parquet file to join all chunks with.
            output_table: Where to save the output of this operation. Defaults to `None`, which will not save the output.
            udf: The user-defined function to run in the join

        Keyword Args:
            left_tables: The names of the attribute tables on the left side to include in the join. Defaults to ("main",).
            left_cache_locally: Whether to cache the left dataset locally in the join. Defaults to False.

        Examples:
            ```py
            import fused

            left_table = fused.open_table("s3://bucket/path/to/table")
            other_file = "s3://bucket/path/to/file.parquet"
            join_config = left_table.join_singlefile(other_file)
            ```

        Returns:
            An object describing the join configuration.
        """
        parsed_udf = Dataset._parse_udf(udf)

        self._validate_output(output_table)

        left_tables = [table for table in left_tables if table in self.tables]
        input_left = DatasetInput(
            base_path=self.base_path,
            tables=left_tables,
            cache_locally=left_cache_locally,
        )
        output = DatasetOutput(table=output_table)

        join_config = JoinSinglefileJobStepConfig(
            udf=parsed_udf,
            input_left=input_left,
            input_right=other,
            output=output,
            buffer_distance=buffer_distance,
        )
        return join_config

    def map(
        self,
        output_table: Optional[str] = None,
        udf: Union[AnyBaseUdf, None] = None,
        *,
        tables: Sequence[str] = DEFAULT_TABLE_NAMES,
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
        parsed_udf = Dataset._parse_udf(udf)

        self._validate_output(output_table)

        dataset_input = DatasetInput(
            base_path=self.base_path,
            tables=tables,
            cache_locally=cache_locally,
        )
        output = DatasetOutput(table=output_table)
        map_config = MapJobStepConfig(
            udf=parsed_udf,
            input=dataset_input,
            output=output,
        )
        return map_config

    def get_chunk(
        self,
        file_id: str | int | None = None,
        chunk_id: int | None = None,
        tables: Sequence[str] = DEFAULT_TABLE_NAMES,
    ) -> Union[pa.Table, pd.DataFrame, gpd.GeoDataFrame]:
        """Fetch a single chunk from this dataset

        Args:
            file_id: The identifier of this file. Defaults to None.
            chunk_id: The numeric index of the chunk within the file to fetch. Defaults to None.
            tables: the list of table names to fetch. Defaults to ("main",).

        Returns:

            A `DataFrame` retrieved from the given file, chunk, and tables.
        """
        return _get_chunk(
            base_path=self.base_path,
            tables=tables,
            file_id=file_id,
            chunk_id=chunk_id,
        )

    def get_dataframe(
        self,
        file_id: str | int | None = None,
        chunk_id: int | None = None,
        tables: Sequence[str] = DEFAULT_TABLE_NAMES,
        max_rows: int | None = 10_000_000,
        parallel_fetch: bool = True,
    ) -> pd.DataFrame:
        """Fetch multiple chunks from this dataset as a dataframe

        Args:
            file_id: The identifier of the file to download. If `None` is passed, all files will be chosen. Defaults to 0.
            chunk_id: The numeric index of the chunk within the file to fetch. If `None` is passed, all chunks for the given file(s) will be chosen. Defaults to 0.
            tables: the list of table names to fetch. Defaults to ("main",).
            max_rows: The maximum number of rows to fetch. If `None`, no limiting will be done. Defaults to 10_000_000.
            parallel_fetch: Fetch in parallel. Defaults to True.

        Raises:
            ValueError: If the function would fetch more than `max_rows` rows.

        Returns:
            A `DataFrame` with all chunks concatenated together.
        """
        # A mapping of file IDs to chunks that are available in this dataset
        first_table_name = tables[0]
        primary_table = self.tables[first_table_name]

        available_chunks: Dict[str, Set[int]] = defaultdict(set)
        if primary_table.chunk_metadata is not None:
            for meta in primary_table.chunk_metadata:
                available_chunks[meta.file_id].add(meta.chunk_id)
        else:
            warnings.warn(
                "Full metadata is not available, so defaulting to sequential file IDs.",
                FusedDefaultWarning,
            )
            for meta_id in range(primary_table.num_files):
                available_chunks[f"{meta_id}"] = {}

        # File ID to chunks that should be fetched
        # Note: this is not a defaultdict as I need to define the list of keys manually
        # so that I can loop over the `.keys()` below
        chunks_to_fetch: Dict[str, Set[int]] = {}

        # Initialize keys
        if file_id is not None:
            chunks_to_fetch[str(file_id)] = set()
        else:
            file_ids = available_chunks.keys()
            for file_id in file_ids:
                chunks_to_fetch[str(file_id)] = set()

        # A specific chunk is requested
        if chunk_id is not None:
            for file_id in chunks_to_fetch.keys():
                assert (
                    chunk_id in available_chunks[file_id]
                ), f"Chunk {chunk_id} does not exist for file {file_id}."
                chunks_to_fetch[file_id] = {chunk_id}

        else:
            # All chunks for the given file(s) are requested
            for file_id in chunks_to_fetch.keys():
                chunks_to_fetch[file_id] = available_chunks[file_id]

        # Check number of rows
        num_rows_to_fetch = 0
        if primary_table.chunk_metadata is not None:
            for meta in primary_table.chunk_metadata:
                file = chunks_to_fetch.get(meta.file_id, set())
                if meta.chunk_id in file:
                    num_rows_to_fetch += meta.num_rows
        else:
            num_rows_to_fetch = primary_table.num_rows

        if max_rows and num_rows_to_fetch > max_rows:
            raise ValueError(
                f"Cannot fetch {num_rows_to_fetch} given a maximum limit of {max_rows} rows. Pass a larger max_rows argument or specify fewer chunks."
            )

        chunk_dfs = []
        if parallel_fetch:
            with ThreadPoolExecutor(max_workers=OPTIONS.max_workers) as pool:
                futures: List[Future] = []
                if chunk_id is None:
                    for file_id in chunks_to_fetch.keys():
                        futures.append(
                            pool.submit(
                                _get_file,
                                base_path=self.base_path,
                                tables=tables,
                                file_id=file_id,
                            )
                        )
                    chunk_dfs = [future.result() for future in futures]
                else:
                    for file_id, chunk_ids in chunks_to_fetch.items():
                        for chunk_id in chunk_ids:
                            futures.append(
                                pool.submit(
                                    _get_chunk,
                                    base_path=self.base_path,
                                    tables=tables,
                                    file_id=file_id,
                                    chunk_id=chunk_id,
                                )
                            )
                    chunk_dfs = [future.result() for future in futures]
        else:
            if chunk_id is None:
                for file_id in chunks_to_fetch.keys():
                    file_df = _get_file(
                        base_path=self.base_path,
                        tables=tables,
                        file_id=file_id,
                    )
                    chunk_dfs.append(file_df)
            else:
                for file_id, chunk_ids in chunks_to_fetch.items():
                    for chunk_id in chunk_ids:
                        chunk_df = _get_chunk(
                            base_path=self.base_path,
                            tables=tables,
                            file_id=file_id,
                            chunk_id=chunk_id,
                        )
                        chunk_dfs.append(chunk_df)

        return pd.concat(chunk_dfs)

    def _repr_html_(self) -> str:
        return fused_dataset_repr(self)

    def _validate_output(self, output_table: Optional[str]):
        if output_table and output_table in self.tables:
            raise ValueError(
                f"Table {output_table} already exists. If you have removed it, you will need to refresh the dataset."
            )

    def delete(
        self, table_name: str, max_deletion_depth: int | Literal["unlimited"] = 2
    ) -> None:
        """Delete a table from the dataset.

        Specify a table to delete from the dataset using the provided table name.
        To prevent inadvertently deleting deeply nested objects in the object directory,
        users can specify the depth of deletion by specifying the maximum deletion depth.

        Args:
            table_name (str): The name of the table to be deleted from the dataset.
            max_deletion_depth (Optional[int], optional): The maximum depth of deletion.
                If provided, the deletion process will be performed only if there are no objects
                deeper than the specified depth. If set to "unlimited" deletion will be performed
                without any depth restrictions. Defaults to 2.

        Returns:
            None
        """
        # Construct path. Ends in `/` because it's a table.
        path = os.path.join(self.base_path, table_name, "")
        self._api.delete(path, max_deletion_depth)

    @staticmethod
    def _parse_udf(udf: Union[AnyBaseUdf, None]) -> AnyBaseUdf:
        if udf is None:
            return EMPTY_UDF
        elif isinstance(udf, AnyBaseUdf):
            return udf
        else:
            raise TypeError("Expected None or a Udf instance for `udf`.")

    model_config = ConfigDict(validate_assignment=True)
