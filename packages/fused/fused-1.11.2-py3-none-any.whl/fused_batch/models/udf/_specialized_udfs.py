import warnings
from pathlib import Path
from typing import Any, BinaryIO, Iterable, Literal, Optional, Union, overload

from fused_batch.models.api.job import (
    JoinJobStepConfig,
    JoinSinglefileJobStepConfig,
    JoinType,
    MapJobStepConfig,
    UdfJobStepConfig,
)
from fused_batch.models.internal import DatasetOutputBase
from fused_batch.warnings import FusedUdfWarning

from ..coerce_dataset import CoerceableToDatasetInput, _object_to_dataset_input
from .base_udf import UdfType
from .udf import GeoPandasUdfV2


class GeoPandasUdfV2Callable(GeoPandasUdfV2):
    type: Literal[UdfType.GEOPANDAS_V2] = UdfType.GEOPANDAS_V2
    """This class is returned from `@fused_batch.udf` and represents
    a UDF that can be instantiated into a job."""

    def to_file(self, where: Union[str, Path, BinaryIO], *, overwrite: bool = False):
        """Write the UDF to disk or the specified file-like object.

        The UDF will be written as a Zip file.

        Args:
            where: A path to a file or a file-like object.

        Keyword Args:
            overwrite: If true, overwriting is allowed.
        """
        job = self()
        job.export(where, how="zip", overwrite=overwrite)

    def to_directory(self, where: Union[str, Path], *, overwrite: bool = False):
        """Write the UDF to disk as a directory (folder).

        Args:
            where: A path to a directory.

        Keyword Args:
            overwrite: If true, overwriting is allowed.
        """
        job = self()
        job.export(where, how="local", overwrite=overwrite)

    def to_gist(self, where: Optional[str] = None, *, overwrite: bool = False):
        """Write the UDF to Github as a Gist.

        Args:
            gist_id: Optionally, a Gist ID to overwrite.

        Keyword Args:
            overwrite: If true, overwriting is allowed.
        """
        job = self()
        job.export(where, how="gist", overwrite=overwrite)

    # This is a subclass of GeoPandasUdfV2 so that the job classes can reference
    # GeoPandasUdfV2 without issues. This class is then installed over the
    # GeoPandasUdfV2 type code so that loaded objects get the __call__ methods.

    # List of data input is passed - run that
    @overload
    def __call__(
        self,
        dataset: None = None,
        right: None = None,
        *,
        arg_list: Iterable[Any],
        output_table: Optional[str] = None,
        buffer_distance: Optional[float] = None,
        join_is_singlefile: Optional[bool] = None,
        join_how: Union[JoinType, Literal["left", "inner"]] = JoinType.INNER,
        **kwargs
    ) -> UdfJobStepConfig:
        ...

    # Nothing is passed - run the UDF once
    @overload
    def __call__(
        self,
        dataset: None = None,
        right: None = None,
        *,
        arg_list: None = None,
        output_table: Optional[str] = None,
        buffer_distance: Optional[float] = None,
        join_is_singlefile: Optional[bool] = None,
        join_how: Union[JoinType, Literal["left", "inner"]] = JoinType.INNER,
        **kwargs
    ) -> UdfJobStepConfig:
        ...

    @overload
    def __call__(
        self,
        dataset: CoerceableToDatasetInput,
        right: None = None,
        *,
        arg_list: None = None,
        output_table: Optional[str] = None,
        buffer_distance: Optional[float] = None,
        join_is_singlefile: Optional[bool] = None,
        join_how: Union[JoinType, Literal["left", "inner"]] = JoinType.INNER,
        **kwargs
    ) -> MapJobStepConfig:
        ...

    @overload
    def __call__(
        self,
        dataset: CoerceableToDatasetInput,
        right: str,
        *,
        arg_list: None = None,
        output_table: Optional[str] = None,
        buffer_distance: Optional[float] = None,
        join_how: Union[JoinType, Literal["left", "inner"]] = JoinType.INNER,
        join_is_singlefile: Literal[True],
        **kwargs
    ) -> JoinSinglefileJobStepConfig:
        ...

    # None for join_is_singlefile will get typed as JoinJobStepConfig,
    # which is probably fine. (single file is expected to be rare/unusual.)
    # Specify join_is_singlefile explicitly if that's an issue.
    @overload
    def __call__(
        self,
        dataset: CoerceableToDatasetInput,
        right: CoerceableToDatasetInput,
        *,
        arg_list: None = None,
        output_table: Optional[str] = None,
        buffer_distance: Optional[float] = None,
        join_is_singlefile: Optional[Literal[False]] = None,
        join_how: Union[JoinType, Literal["left", "inner"]] = JoinType.INNER,
        **kwargs
    ) -> JoinJobStepConfig:
        ...

    def __call__(
        self,
        dataset: Optional[CoerceableToDatasetInput] = None,
        right: Optional[CoerceableToDatasetInput] = None,
        *,
        arg_list: Optional[Iterable[Any]] = None,
        output_table: Optional[str] = None,
        buffer_distance: Optional[float] = None,
        join_is_singlefile: Optional[bool] = None,
        join_how: Union[JoinType, Literal["left", "inner"]] = JoinType.INNER,
        **kwargs
    ) -> Union[
        UdfJobStepConfig,
        MapJobStepConfig,
        JoinJobStepConfig,
        JoinSinglefileJobStepConfig,
    ]:
        """Create a job from this UDF.

        Args:
            dataset: The dataset to run the UDF on.
            right: The right dataset to join with. If None, no join is performed and only `dataset` is processed. If this is a URL to a single Parquet file, a singlefile join is created. Defaults to None.
            arg_list: A list of records to pass in to the UDF as input. This option is mutually exclusive with `dataset` and `right`.
            output_table: The name of the table to write output columns on `dataset`.
            buffer_distance: For join jobs, the buffer around `dataset` partitions to perform.
            join_is_singlefile: If not None, whether a join operation should be performed in `singlefile` mode, i.e. all partitions join with a single Parquet file. Defaults to None, which indicates autodetect.
        """

        any_datasets_passed = dataset is not None or right is not None
        any_data_passed = arg_list is not None
        if any_datasets_passed and any_data_passed:
            warnings.warn(
                "`dataset` and `arg_list` are mutually exclusive options, `dataset` will be ignored.",
                FusedUdfWarning,
            )

        passed_dataset = dataset
        dataset = (
            _object_to_dataset_input(dataset, allow_none=True)
            if any_datasets_passed
            else None
        )
        if dataset is None:
            # Detect that this is actually some sort of regular data input, not a dataset.
            any_datasets_passed = False

        with_params = self.model_copy()
        # TODO: Consider using with_parameters here, and validating that "context" and other reserved parameter names are not being passed.
        new_parameters = {**kwargs}
        if new_parameters:
            with_params.parameters = new_parameters

        project_url = dataset._project_url if hasattr(dataset, "_project_url") else None

        output = DatasetOutputBase.from_str(output_table, project_url=project_url)

        if any_data_passed or not any_datasets_passed:
            if arg_list is not None and not len(arg_list):
                warnings.warn(
                    "An empty `arg_list` was passed in, no calls to the UDF will be made.",
                    FusedUdfWarning,
                )
            if passed_dataset is not None:
                arg_list = (
                    [passed_dataset, *arg_list]
                    if arg_list is not None
                    else [passed_dataset]
                )

            return UdfJobStepConfig(
                udf=with_params,
                input=arg_list,
                output=output,
            )
        elif right is None:
            assert dataset is not None
            return MapJobStepConfig(
                input=dataset,
                udf=with_params,
                output=output,
            )
        elif (
            isinstance(right, str) and right.endswith(".parquet")
        ) or join_is_singlefile is True:
            assert dataset is not None
            return JoinSinglefileJobStepConfig(
                input_left=dataset,
                input_right=right,
                udf=with_params,
                output=output,
                buffer_distance=buffer_distance,
            )
        else:
            assert dataset is not None
            right = _object_to_dataset_input(right)
            return JoinJobStepConfig(
                input_left=dataset,
                input_right=right,
                udf=with_params,
                output=output,
                buffer_distance=buffer_distance,
                how=join_how,
            )
