from __future__ import annotations

import warnings
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Union,
)
from urllib.parse import urlparse

from IPython import get_ipython
from IPython.core.inputsplitter import IPythonInputSplitter
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
)
from typing_extensions import Annotated

from fused_batch._cache import get_or_cache_sample
from fused_batch._formatter.formatter_job_config import (
    fused_ingestion_repr,
    fused_job_repr,
    fused_join_repr,
    fused_join_singlefile_repr,
    fused_map_repr,
    fused_udf_step_repr,
)
from fused_batch._str_utils import append_url_part, is_url
from fused_batch._udf.execute_v2 import (
    execute_against_sample,
    validate_imports_whitelist,
)
from fused_batch.warnings import (
    FusedDefaultWarning,
    FusedIgnoredWarning,
    FusedPathWarning,
    FusedTypeWarning,
)

from ...models.schema import Schema
from .._codegen import (
    create_directory_and_zip,
    extract_parameters,
    generate_meta_json,
    generate_readme,
    stringify_input,
    stringify_named_params,
    stringify_output,
    structure_params,
)
from .._inplace import _maybe_inplace
from ..api.enums import JoinType
from ..base import FusedBaseModel, UserMetadataType
from ..internal import (
    AnyDatasetInput,
    AnyDatasetOutput,
    DatasetInput,
    DatasetInputV2,
    DatasetOutputV2,
    RunResponse,
)
from ..request import WHITELISTED_INSTANCE_TYPES
from ..udf import EMPTY_UDF, AnyBaseUdf, RootAnyBaseUdf
from ..udf._eval_result import MultiUdfEvaluationResult, UdfEvaluationResult

if TYPE_CHECKING:
    import geopandas as gpd
    import pandas as pd
    import pyarrow as pa

    from ...models.coerce_dataset import CoerceableToDatasetInput
    from .. import JoinInput, JoinSingleFileInput, MapInput, Table

from fused_batch.models.udf._udf_registry import UdfRegistry

STR_IMPORTS = (
    "\n".join(
        [
            "import fused_batch",
            "from fused_batch.models.udf import Header",
            "from fused_batch.models import Schema",
        ]
    )
    + "\n\n"
)

SYSTEM_PARAMETER_NAMES = {"output", "context"}
"""Parameter names that will be provided by the Fused system"""


def _common_validate_for_overwrite(
    table_name: str,
    table_names: Sequence[str],
    overwrite: bool = False,
):
    if table_name in table_names:
        if overwrite:
            warnings.warn(
                f"Table `{table_name}` already exists and will be overwritten because `overwrite=True`.",
                FusedDefaultWarning,
            )
        else:
            raise ValueError(
                f"Table `{table_name}` already exists and cannot be written to."
            )


def _common_validate_for_run(
    *,
    output: Optional[AnyDatasetOutput],
    udf: Optional[AnyBaseUdf],
    ignore_no_udf: bool = False,
    ignore_no_output: bool = False,
    validate_imports: Optional[bool] = None,
):
    """
    Validate that the job config is ready to run
    """
    if not ignore_no_udf and not udf.code:
        raise ValueError(
            f"No UDF code is set for `{udf.name}` UDF. Set the `udf` attribute or pass `ignore_no_udf=True`."
        )
    if not ignore_no_udf and hasattr(udf, "table_schema") and udf.table_schema is None:
        raise ValueError(
            f"No UDF schema is set for `{udf.name}` UDF. Run the UDF locally with `run_local()` or pass `ignore_no_udf=True`."
        )

    if not ignore_no_output and hasattr(output, "table") and not output.table:
        raise ValueError(
            f"No `table` attribute is set on the job output configuration for `{udf.name}` UDF. Set it to write output, or pass `ignore_no_output=True`"
        )

    if not ignore_no_output and hasattr(output, "url") and not output.url:
        raise ValueError(
            f"No `url` attribute is set on the job output configuration for `{udf.name}` UDF. Set it to write output, or pass `ignore_no_output=True`"
        )

    # TODO: Check if the output table name already exists

    # Check if headers are valid
    if not ignore_no_udf and not _validate_headers_for_remote_exec(udf):
        raise ValueError(f"Headers for UDF {udf.name} cannot resolve remotely.")

    # Validate import stamements correspond to valid modules
    if udf is not None:
        validate_imports_whitelist(udf, validate_imports=validate_imports)


def _assert_udf_has_parameters(udf: AnyBaseUdf):
    assert hasattr(
        udf, "set_parameters"
    ), f"Cannot set parameters on a UDF without parameters: {type(udf)}"


class JobStepConfig(FusedBaseModel):
    type: Literal[
        "partition_geospatial",
        "partition_nongeospatial",
        "union",
        "udf",
        "map",
        "join",
        "join_singlefile",
    ]
    name: Optional[StrictStr] = None
    metadata: UserMetadataType = None
    """User defined metadata. Any metadata values must be JSON serializable."""
    _validate_version: bool = True
    ignore_chunk_error: bool = False
    """If `True`, continue processing even if some computations throw errors."""

    @property
    def input_metadata(self) -> AnyDatasetInput | None:
        return None

    def _validate_for_run(
        self,
        *,
        ignore_no_udf: bool = False,
        ignore_no_output: bool = False,
        validate_imports: Optional[bool] = None,
        validate_inputs: bool = True,
    ):
        has_udf = hasattr(self, "udf")
        has_output = hasattr(self, "output")
        _common_validate_for_run(
            output=self.output if has_output else None,
            udf=self.udf if has_udf else None,
            ignore_no_udf=ignore_no_udf if has_udf else True,
            ignore_no_output=ignore_no_output if has_output else True,
            validate_imports=validate_imports,
        )

    def run_remote(
        self,
        output_table: Optional[str] = ...,
        instance_type: Optional[WHITELISTED_INSTANCE_TYPES] = None,
        *,
        region: str | None = None,
        disk_size_gb: int | None = None,
        additional_env: List[str] | None = None,
        image_name: Optional[str] = None,
        ignore_no_udf: bool = False,
        ignore_no_output: bool = False,
        validate_imports: Optional[bool] = None,
        validate_inputs: bool = True,
        overwrite: Optional[bool] = None,
    ) -> RunResponse:
        """Execute this operation

        Args:
            output_table: The name of the table to write to. Defaults to None.
            instance_type: The AWS EC2 instance type to use for the job. Acceptable strings are "m5.large", "m5.xlarge", "m5.2xlarge", "m5.4xlarge", "m5.8xlarge", "m5.12xlarge", "m5.16xlarge", "r5.large", "r5.xlarge", "r5.2xlarge", "r5.4xlarge", "r5.8xlarge", "r5.12xlarge", or "r5.16xlarge". Defaults to None.
            region: The AWS region in which to run. Defaults to None.
            disk_size_gb: The disk size to specify for the job. Defaults to None.
            additional_env: Any additional environment variables to be passed into the job. Defaults to None.
            image_name: Custom image name to run. Defaults to None for default image.

            ignore_no_udf: Ignore validation errors about not specifying a UDF. Defaults to False.
            ignore_no_output: Ignore validation errors about not specifying output location. Defaults to False.
        """
        to_run = self.model_copy(deep=True)

        if output_table is Ellipsis:
            if hasattr(self, "output"):
                if not self.output.table:
                    raise ValueError("The Job requires `output_table` to be specified.")
                elif overwrite is not None:
                    to_run.output.overwrite = overwrite
        elif output_table is not None:
            to_run = to_run.set_output(
                table_or_url=output_table, overwrite=overwrite, inplace=False
            )
        else:
            ignore_no_output = True
        return to_run._run_remote(
            instance_type=instance_type,
            region=region,
            disk_size_gb=disk_size_gb,
            additional_env=additional_env,
            image_name=image_name,
            ignore_no_udf=ignore_no_udf,
            ignore_no_output=ignore_no_output,
            validate_imports=validate_imports,
            validate_inputs=validate_inputs,
        )

    def _run_remote(
        self,
        instance_type: Optional[WHITELISTED_INSTANCE_TYPES] = None,
        *,
        region: str | None = None,
        disk_size_gb: int | None = None,
        additional_env: List[str] | None = None,
        image_name: Optional[str] = None,
        ignore_no_udf: bool = False,
        ignore_no_output: bool = False,
        validate_imports: Optional[bool] = None,
        validate_inputs: bool = True,
    ) -> RunResponse:
        # TODO: if the user uses start_job, this validation will never happen
        self._validate_for_run(
            ignore_no_udf=ignore_no_udf,
            ignore_no_output=ignore_no_output,
            validate_imports=validate_imports,
            validate_inputs=validate_inputs,
        )
        config = JobConfig(steps=[self])
        return self._api.start_job(
            config,
            instance_type=instance_type,
            region=region,
            disk_size_gb=disk_size_gb,
            additional_env=additional_env,
            image_name=image_name,
        )

    def _generate_job_params(self) -> List[str]:
        # Derive parameters

        positional_parameters, named_parameters = extract_parameters(self.udf.code)
        # Replace default code params with params passed to job
        named_parameters.update(self.udf.parameters)
        # Remove positional parameters that already have values in the job
        positional_parameters = [
            positional_parameter
            for positional_parameter in positional_parameters
            if positional_parameter not in named_parameters.keys()
        ]

        if self.type == "map":
            positional_parameters[0] = stringify_input(self.input)
        elif self.type in ["join", "join_singlefile"]:
            positional_parameters[0] = stringify_input(self.input_left)
            positional_parameters[1] = stringify_input(self.input_right)
        elif self.type == "udf":
            if self.input:
                positional_parameters[0] = f"arg_list={repr(self.input)}"
        else:
            warnings.warn(
                f'Rendering of type "{self.type}" may be incomplete.', FusedTypeWarning
            )

        # After replacing the inputs, look for any parameters with no values
        # that match the reserved parameter names. These should not be included
        # in instantiating the UDF because they are provided by the system.
        positional_parameters = [
            param
            for param in positional_parameters
            if param not in SYSTEM_PARAMETER_NAMES
        ]

        _params_fn_instance = positional_parameters + stringify_named_params(
            named_parameters
        )

        output_config = []
        if hasattr(self, "output"):
            output_str = stringify_output(self.output)
            if output_str is not None:
                output_config.append(f"output_table={output_str}")

        if hasattr(self, "buffer_distance") and self.buffer_distance is not None:
            _params_fn_instance.append(f"buffer_distance={self.buffer_distance}")
        if hasattr(self, "how"):
            _params_fn_instance.append(f"join_how={repr(self.how.value)}")

        return _params_fn_instance + output_config

    def _generate_code(self, headerfile=False):
        # String: Job instantiation
        str_job_inst = f"job = {self.udf.entrypoint}({structure_params(self._generate_job_params())})"
        # String: Job execution
        str_job_exec = "job.run_local()"
        # String: UDF
        str_udf, header_cells = self.udf._generate_code(
            include_imports=False, headerfile=headerfile
        )
        # Structure cell
        src = f"""
{STR_IMPORTS}
{str_udf}
{str_job_inst}
{str_job_exec}
"""
        return src, header_cells

    def render(self, headerfile=False):
        _render(self, headerfile=headerfile)

    def export(
        self,
        path,
        how: Literal["local", "zip", "gist"] = "local",
        overwrite=False,
    ):
        _export(job=self, path=path, how=how, overwrite=overwrite)

    def set_output(
        self,
        table_or_url: Optional[str] = None,
        *,
        table: Optional[str] = None,
        url: Optional[str] = None,
        inplace: bool = False,
        overwrite: Optional[bool] = None,
    ) -> JobStepConfig:
        """Update output tables on this operation

        Args:
            table_or_url: Automatically set either `table` or `url` depending on whether this is a URL.

        Keyword Args:
            table: The name of the table to use for output. This table name must be unique. Defaults to None.
            url: If set, the URL to write the table to. Overrides `table` and `base_path`.
            inplace: If True, modify and return this object. If False, modify and return a copy. Defaults to False.
            overwrite: If True, overwrite the output dataset if it already exists. Defaults to None to not update.

        Returns:
            _description_
        """
        ret = _maybe_inplace(self, inplace)

        if not hasattr(ret, "output"):
            raise NotImplementedError("This job step does not have output")

        if table is None and url is None and table_or_url is not None:
            try:
                parsed = urlparse(table_or_url)
                if parsed.scheme:
                    url = table_or_url
            except (ValueError, TypeError, AttributeError):
                pass

            # Parsing as URL failed
            if url is None:
                table = table_or_url

        prev_project_url = (
            ret.output._project_url if hasattr(ret.output, "_project_url") else None
        )

        if (
            isinstance(ret.output, DatasetOutputV2)
            and table is not None
            and prev_project_url is not None
        ):
            # If this dataset is URL based, we can still set a table if there is a base path in the form of a project URL
            ret.output = DatasetOutputV2(
                url=append_url_part(prev_project_url, table),
                save_index=ret.output.save_index,
                sample_strategy=ret.output.sample_strategy,
                overwrite=overwrite if overwrite is not None else ret.output.overwrite,
            )
            ret.output._project_url = prev_project_url
        elif url is not None and url is not Ellipsis:
            # If a bare URL is being set, it must be done on V2
            ret.output = DatasetOutputV2(
                url=url,
                save_index=ret.output.save_index,
                sample_strategy=ret.output.sample_strategy,
                overwrite=overwrite if overwrite is not None else ret.output.overwrite,
            )
            ret.output._project_url = prev_project_url
        else:
            raise ValueError(
                "Setting a table name on an output without a project URL. Set an output URL instead."
            )

        return ret


class PartitionJobStepConfig(JobStepConfig):
    """Base class for partitioner steps (should not be instantiated directly)"""

    input: Union[List[StrictStr], StrictStr]
    """The path to the input file(s) for partitioning."""

    output: Optional[StrictStr] = None
    """Base path of the main output directory"""
    output_metadata: Optional[StrictStr] = None
    """Base path of the fused output directory"""

    partitioning_maximum_per_file: Optional[int] = 2_500_000
    """Maximum value for `partitioning_method` to use per file. If `None`, defaults to _1/10th_ of the total value of `partitioning_method`. So if the value is `None` and `partitioning_method` is `"area"`, then each file will be have no more than 1/10th the total area of all geometries.
    """

    partitioning_maximum_per_chunk: Optional[int] = 65000
    """Maximum value for `partitioning_method` to use per chunk. If `None`, defaults to _1/100th_ of the total value of `partitioning_method`. So if the value is `None` and `partitioning_method` is `"area"`, then each file will be have no more than 1/100th the total area of all geometries.
    """

    def _validate_for_run(
        self,
        *,
        ignore_no_udf: bool = False,
        ignore_no_output: bool = False,
        validate_imports: Optional[bool] = None,
        validate_inputs: bool = True,
    ):
        super()._validate_for_run(
            ignore_no_udf=ignore_no_udf,
            ignore_no_output=ignore_no_output,
            validate_imports=validate_imports,
            validate_inputs=validate_inputs,
        )

        if validate_inputs:

            def _validate_input(input: str):
                if isinstance(input, str):
                    if (
                        input.startswith("file://")
                        or input.startswith("/")
                        or input.startswith("./")
                    ):
                        warnings.warn(
                            f"Input to partition job step ({input}) is a local file reference, which will be resolved on the backend and not on your local system. If you meant to partition a local file, use `fused.upload` first and then use the remote path.",
                            FusedPathWarning,
                        )
                    elif input.startswith("fd://"):
                        warnings.warn(
                            f"Input to partition job step ({input}) is fd:// path, which may not be accepted by this version of the backend. Pass the exact S3 or GCS URL instead.",
                            FusedPathWarning,
                        )
                else:
                    warnings.warn(
                        "Input to partition job step is not a string.", FusedTypeWarning
                    )

            if isinstance(self.input, (list, tuple)):
                for input in self.input:
                    _validate_input(input)
            else:
                _validate_input(self.input)

    def _repr_html_(self) -> str:
        return fused_ingestion_repr(self)


class GDALOpenConfig(BaseModel):
    """A class to define options for how to open files with GDAL."""

    open_options: Dict[str, str] = Field(default_factory=dict)
    """A dictionary of options passed in to GDAL for opening files."""

    layer: Optional[StrictStr] = None
    """The layer of the input file to read from."""


class GeospatialPartitionJobStepConfig(PartitionJobStepConfig):
    type: Literal["partition_geospatial"] = "partition_geospatial"

    table_schema: Optional[Schema] = None

    file_suffix: Optional[StrictStr] = None
    load_columns: Optional[List[StrictStr]] = None
    remove_cols: List[StrictStr] = Field(default_factory=list)
    explode_geometries: StrictBool = False

    drop_out_of_bounds: Optional[StrictBool] = None
    """Whether to drop points that are outside of the WGS84 valid bounds."""

    lonlat_cols: Optional[Tuple[str, str]] = None
    """Names of longitude, latitude columns to construct point geometries from.

    This currently applies only to loading Parquet files.

    If the original files are in a format such as CSV, pass the names of the longitude
    and latitude columns in the GDALOpenConfig. If you pass those to GDALOpenConfig, do
    not also pass names to lonlat_columns here.
    """

    # Partitioning options
    partitioning_max_width_ratio: Union[StrictFloat, StrictInt] = 2
    partitioning_max_height_ratio: Union[StrictFloat, StrictInt] = 2

    partitioning_method: Literal["area", "length", "coords", "rows"]
    """The method used for deciding how to group geometries."""

    partitioning_force_utm: Optional[Literal["file", "chunk"]] = None

    # TODO: switch back to median as default
    partitioning_split_method: Literal["mean", "median"]

    # Subdivide options
    subdivide_start: Optional[float] = None
    """Geometries with greater area than this (in WGS84 degrees) will be subdivided.
    Start area should be greater than or equal to stop area.
    """

    subdivide_stop: Optional[float] = None
    """This is the area that will stop continued subdivision of a geometry.
    Stop area should be less than or equal to start area. Additionally stop area cannot
    be zero, as that would cause infinite subdivision.
    """

    subdivide_method: Optional[Literal["area"]] = "area"

    split_identical_centroids: StrictBool = True
    """
    Whether to split a partition that has identical centroids (such as if all geometries
    in the partition are the same) if there are more such rows than defined in
    "partitioning_maximum_per_file" and "partitioning_maximum_per_chunk".
    """

    target_num_chunks: StrictInt = 5000
    """The target for the number of chunks if partitioning_maximum_per_file is None."""

    gdal_config: GDALOpenConfig = Field(default_factory=GDALOpenConfig)
    """Options to pass to GDAL for opening files."""

    def run_remote(
        self,
        output_table: Optional[str] = ...,
        instance_type: Optional[WHITELISTED_INSTANCE_TYPES] = None,
        *,
        region: str | None = None,
        disk_size_gb: int | None = None,
        additional_env: List[str] | None = None,
        image_name: Optional[str] = None,
        ignore_no_udf: bool = False,
        ignore_no_output: bool = False,
        validate_imports: Optional[bool] = None,
        validate_inputs: bool = True,
        overwrite: Optional[bool] = None,
    ) -> RunResponse:
        """Execute this operation

        Args:
            output_table: The name of the table to write to. Defaults to None.
            instance_type: The AWS EC2 instance type to use for the job. Acceptable strings are "m5.large", "m5.xlarge", "m5.2xlarge", "m5.4xlarge", "m5.8xlarge", "m5.12xlarge", "m5.16xlarge", "r5.large", "r5.xlarge", "r5.2xlarge", "r5.4xlarge", "r5.8xlarge", "r5.12xlarge", or "r5.16xlarge". Defaults to None.
            region: The AWS region in which to run. Defaults to None.
            disk_size_gb: The disk size to specify for the job. Defaults to None.
            additional_env: Any additional environment variables to be passed into the job. Defaults to None.
            image_name: Custom image name to run. Defaults to None for default image.

            ignore_no_udf: Ignore validation errors about not specifying a UDF. Defaults to False.
            ignore_no_output: Ignore validation errors about not specifying output location. Defaults to False.
        """
        to_run = self.model_copy(deep=True)

        if output_table is Ellipsis:
            if self.output is None and self.output_metadata is None:
                raise ValueError("The Job requires `output_table` to be specified.")
            elif overwrite is not None:
                warnings.warn(
                    "Overwrite on ingestion operation is ignored", FusedIgnoredWarning
                )
        elif output_table is not None:
            to_run = to_run.set_output(
                output=output_table, overwrite=overwrite, inplace=False
            )
        else:
            ignore_no_output = True
        return to_run._run_remote(
            instance_type=instance_type,
            region=region,
            disk_size_gb=disk_size_gb,
            additional_env=additional_env,
            image_name=image_name,
            ignore_no_udf=ignore_no_udf,
            ignore_no_output=ignore_no_output,
            validate_imports=validate_imports,
            validate_inputs=validate_inputs,
        )

    def set_output(
        self,
        output: Optional[str] = None,
        output_metadata: Optional[str] = None,
        inplace: bool = False,
        overwrite: Optional[bool] = None,
    ):
        ret = _maybe_inplace(self, inplace)

        if overwrite is not None:
            warnings.warn(
                "Overwrite on ingestion operation is ignored", FusedIgnoredWarning
            )

        if output is not None and urlparse(output).scheme:
            ret.output = output
        else:
            raise ValueError(
                "Setting an invalid output table name for `output`. Set an output URL instead."
            )

        if output_metadata is not None and urlparse(output_metadata).scheme:
            ret.output_metadata = output_metadata
        else:
            raise ValueError(
                "Setting an invalid output table name for `output_metadata`. Set an output URL instead."
            )

        return ret


class NonGeospatialPartitionJobStepConfig(PartitionJobStepConfig):
    type: Literal["partition_nongeospatial"] = "partition_nongeospatial"

    partition_col: Optional[StrictStr] = None


class UdfJobStepConfig(JobStepConfig):
    """A job step of running a UDF."""

    type: Literal["udf"] = "udf"
    udf: AnyBaseUdf

    input: Optional[List[Any]] = None
    _validate_version: bool = True

    def set_input(
        self,
        input: Optional[List[Any]],
        inplace: bool = False,
    ) -> UdfJobStepConfig:
        """Set the input datasets on this operation

        Args:
            input: A list of JSON-serializable objects to pass as input to the UDF, or None to run once with no arguments.
            inplace: If True, modify and return this object. If False, modify and return a copy. Defaults to False.
        """
        ret = _maybe_inplace(self, inplace)
        ret.input = input

        return ret

    def set_udf(
        self,
        udf: AnyBaseUdf | dict | str,
        parameters: Optional[Dict[str, Any]] = None,
        replace_parameters: bool = False,
        inplace: bool = False,
    ) -> UdfJobStepConfig:
        """Set a user-defined function on this operation

        Args:
            udf: the representation of this UDF
            parameters: Parameters to set on the UDF. Defaults to None to not set parameters.
            replace_parameters: If True, unset any parameters not passed in parameters. Defaults to False.
            inplace: If True, modify and return this object. If False, modify and return a copy. Defaults to False.
        """
        ret = _maybe_inplace(self, inplace)
        ret.udf = RootAnyBaseUdf.model_validate(udf).root

        if parameters is not None:
            _assert_udf_has_parameters(ret.udf)
            ret.udf = ret.udf.set_parameters(
                parameters, replace_parameters=replace_parameters, inplace=False
            )

        return ret

    def run_local(
        self,
        sample: Any | None = ...,
        validate_output: bool = False,
        validate_imports: Optional[bool] = None,
        **kwargs,
    ) -> UdfEvaluationResult:
        """
        Run a UDF locally on sample data.

        Args:
            sample: The sample input to pass to the UDF. Defaults to None.
            validate_output: If True, the output of the UDF is validated and schema is updated. If False,
                the output is returned as-is. Defaults to False.
            **kwargs: Additional keyword arguments to be passed to the UDF.

        Returns:
            The output of the user-defined function (UDF) applied to the input data.

        Raises:
            Any exceptions raised by the user-defined function (UDF) during its execution.
        """
        default_sample = [] if not self.input else [self.input[0]]
        sample_list = default_sample if sample is Ellipsis else [sample]
        return execute_against_sample(
            self.udf,
            sample_list,
            validate_output=validate_output,
            validate_imports=validate_imports,
            **kwargs,
        )

    def _validate_for_run(
        self,
        *,
        ignore_no_udf: bool = False,
        ignore_no_output: bool = False,
        validate_imports: Optional[bool] = None,
        validate_inputs: bool = True,
    ):
        if not ignore_no_udf and not self.udf.code:
            raise ValueError(
                "No UDF code is set. Set the `udf` attribute or pass `ignore_no_udf=True`."
            )

        # TODO: should _common_validate_before_run be used here?

    def _repr_html_(self) -> str:
        return fused_udf_step_repr(self)

    def get_sample(
        self,
        file_id: str | int = 0,
    ) -> Any:
        if isinstance(file_id, str):
            file_id = int(file_id)
        if self.input is not None and len(self.input) >= file_id:
            return self.run_local(self.input[file_id])
        else:
            raise ValueError("No input is set.")

    def run_file(
        self,
        *,
        _client_id: Optional[str] = None,
        _include_log: bool = False,
        _dtype_out_vector: str = "parquet",
        _dtype_out_raster: str = "tiff",
        **kwargs,
    ) -> UdfEvaluationResult:
        # TODO: fix circular import error
        from fused_batch._quick.udf import run as _run_realtime

        res = _run_realtime(
            step_config=self,
            params=kwargs,
            client_id=_client_id,
            dtype_out_raster=_dtype_out_raster,
            dtype_out_vector=_dtype_out_vector,
        )
        if _include_log:
            return res
        else:
            return res.data

    # TODO: do we enforce pattern to have same args in overload, for typehints?
    def run_tile(
        self,
        *,
        x: float = None,
        y: float = None,
        z: float = None,
        _include_log: bool = False,
        _client_id: Optional[str] = None,
        _dtype_out_vector: str = "parquet",
        _dtype_out_raster: str = "tiff",
        **kwargs,
    ) -> UdfTileEvaluationResult:
        from fused_batch._quick.udf import run_tile as _run_realtime_tile

        res = _run_realtime_tile(
            step_config=self,
            x=x,
            y=y,
            z=z,
            client_id=_client_id,
            dtype_out_raster=_dtype_out_raster,
            dtype_out_vector=_dtype_out_vector,
            params=kwargs,
        )
        if _include_log:
            return res
        else:
            return res.data


class UdfTileEvaluationResult:
    pass


class MapJobStepConfig(JobStepConfig):
    type: Literal["map"] = "map"
    udf: AnyBaseUdf
    """The UDF to run on this operation."""
    input: AnyDatasetInput
    """The dataset to map over."""
    output: AnyDatasetOutput
    """How to save the map operation."""
    model_config = ConfigDict(validate_assignment=True)

    @property
    def input_metadata(self) -> AnyDatasetInput:
        """Access the input metadata."""
        return self.input

    def set_input(
        self,
        input: Optional[CoerceableToDatasetInput] = None,
        *,
        inplace: bool = False,
    ) -> MapJobStepConfig:
        """Set the input tables on this operation

        Args:
            input: Input to read.

        Keyword Args:
            inplace: If True, modify and return this object. If False, modify and return a copy. Defaults to False.
        """
        from ...models.coerce_dataset import _object_to_dataset_input

        ret = _maybe_inplace(self, inplace)

        ret.input = _object_to_dataset_input(input)

        return ret

    def set_udf(
        self,
        udf: AnyBaseUdf | dict | str,
        parameters: Optional[Dict[str, Any]] = None,
        replace_parameters: bool = False,
        inplace: bool = False,
    ) -> MapJobStepConfig:
        """Set a user-defined function on this operation

        Args:
            udf: the representation of this UDF
            parameters: Parameters to set on the UDF. Defaults to None to not set parameters.
            replace_parameters: If True, unset any parameters not passed in parameters. Defaults to False.
            inplace: If True, modify and return this object. If False, modify and return a copy. Defaults to False.
        """
        ret = _maybe_inplace(self, inplace)
        ret.udf = RootAnyBaseUdf.model_validate(udf).root

        if parameters is not None:
            _assert_udf_has_parameters(ret.udf)
            ret.udf = ret.udf.set_parameters(
                parameters, replace_parameters=replace_parameters, inplace=False
            )

        return ret

    def open_output(self, **kwargs) -> Table:
        """Opens the output of this operation

        Args:
            kwargs: Additional arguments to pass to open

        Returns:
            The Table that was generated by this operation
        """
        if isinstance(self.output, DatasetOutputV2) and self.output.url is not None:
            return self._api.open_table(self.output.url, **kwargs)
        else:
            raise ValueError("Output has unknown type or no output is set")

    def _validate_for_run(
        self,
        *,
        ignore_no_udf: bool = False,
        ignore_no_output: bool = False,
        validate_imports: Optional[bool] = None,
        validate_inputs: bool = True,
    ):
        _common_validate_for_run(
            output=self.output,
            udf=self.udf,
            ignore_no_udf=ignore_no_udf,
            ignore_no_output=ignore_no_output,
            validate_imports=validate_imports,
        )

    def get_sample(
        self,
        file_id: str | int | None = None,
        chunk_id: int | None = None,
        n_rows: int | None = None,
        use_cache: bool = True,
    ) -> MapInput:
        """Fetch a sample of this operation

        Args:
            file_id: The identifier of this file. Defaults to None.
            chunk_id: The numeric index of the chunk within the file to fetch. Defaults to None.
            n_rows: The maximum number of rows to sample. Defaults to None for all rows in the chunk.
            use_cache: If True, use a cached sample if available. Defaults to True.

        Returns:

            Sample data retrieved from the given file and chunk.
        """
        sample_coords = (file_id, chunk_id, n_rows)

        def generator():
            return self._api.sample_map(
                config=self,
                file_id=file_id,
                chunk_id=chunk_id,
                n_rows=n_rows,
            )

        if use_cache:
            return get_or_cache_sample(self, sample_coords, generator)
        else:
            return generator()

    def run_local(
        self,
        file_id: str | int | None = None,
        chunk_id: int | None = None,
        n_rows: int | None = None,
        sample: MapInput | None = None,
        validate_output: bool = True,
        validate_imports: Optional[bool] = None,
        use_cache: bool = True,
        **kwargs,
    ) -> UdfEvaluationResult:
        """
        Run a UDF locally on sample data.

        Args:
            file_id (str or int or None, optional): Identifier for the file containing the data.
                Defaults to None, in which case a file is automatically chosen.
            chunk_id (int or None, optional): Identifier for the specific chunk of data within the file.
                Defaults to None, in which case a chunk is automatically chosen.
            n_rows: The maximum number of rows to sample from the left dataset. Defaults to None for all rows in the chunk.
            sample: If sample is passed, it is used instead of retrieving a sample.
            validate_output: If True, the output of the UDF is validated and schema is updated. If False,
                the output is returned as-is. Defaults to True.
            use_cache: If True, use a cached sample if available. Defaults to True.
            **kwargs: Additional keyword arguments to be passed to the UDF.

        Returns:
            The output of the user-defined function (UDF) applied to the input data.

        Raises:
            Any exceptions raised by the user-defined function (UDF) during its execution.
        """
        sample = (
            self.get_sample(
                file_id=file_id, chunk_id=chunk_id, n_rows=n_rows, use_cache=use_cache
            )
            if sample is None
            else sample
        )

        return execute_against_sample(
            self.udf,
            sample,
            validate_output=validate_output,
            validate_imports=validate_imports,
            **kwargs,
        )

    def run_remote(
        self,
        output_table: Optional[str] = ...,
        instance_type: Optional[WHITELISTED_INSTANCE_TYPES] = None,
        *,
        region: str | None = None,
        disk_size_gb: int | None = None,
        additional_env: List[str] | None = None,
        image_name: Optional[str] = None,
        ignore_no_udf: bool = False,
        ignore_no_output: bool = False,
        validate_imports: Optional[bool] = None,
        parameters: Dict[str, Any] | None = None,
        replace_parameters: bool = False,
        overwrite: Optional[bool] = None,
    ) -> RunResponse:
        to_run = self.model_copy(deep=True)
        if parameters is not None:
            _assert_udf_has_parameters(self.udf)
            to_run = to_run.set_udf(
                self.udf.set_parameters(
                    parameters, replace_parameters=replace_parameters, inplace=False
                ),
                inplace=False,
            )
        if output_table is Ellipsis:
            if not self.output.table:
                raise ValueError("The Job requires `output_table` to be specified.")
            elif overwrite is not None:
                to_run.output.overwrite = overwrite
        elif output_table is not None:
            to_run = to_run.set_output(
                table_or_url=output_table, overwrite=overwrite, inplace=False
            )
        else:
            ignore_no_output = True
        return to_run._run_remote(
            instance_type=instance_type,
            region=region,
            disk_size_gb=disk_size_gb,
            additional_env=additional_env,
            image_name=image_name,
            ignore_no_udf=ignore_no_udf,
            ignore_no_output=ignore_no_output,
            validate_imports=validate_imports,
        )

    def _whole_file_sample(
        self,
        file_id: str | int | None = None,
        n_rows: int | None = None,
    ) -> MapInput:
        return self._api._whole_file_sample_map(
            config=self,
            file_id=file_id,
            n_rows=n_rows,
        )

    def get_output_chunk(
        self,
        file_id: str | int | None = None,
        chunk_id: int | None = None,
    ) -> Union[pa.Table, pd.DataFrame, gpd.GeoDataFrame]:
        """Fetch a sample of the output of this operation

        Args:
            file_id: The identifier of this file. Defaults to None.
            chunk_id: The numeric index of the chunk within the file to fetch. Defaults to None.

        Returns:
            Sample data retrieved from the given file and chunk.
        """
        if isinstance(self.output, DatasetOutputV2) and self.output.url:
            return _get_chunk_v2(
                url=self.output.url,
                file_id=file_id,
                chunk_id=chunk_id,
            )
        else:
            raise ValueError("Unknown output type or no output URL is set")

    def _repr_html_(self) -> str:
        return fused_map_repr(self)

    def run_realtime(
        self,
        df_left: Optional[
            Union[pd.DataFrame, gpd.GeoDataFrame, pa.Table, str, Path]
        ] = None,
        *,
        _client_id: Optional[str] = None,
        **kwargs,
    ) -> UdfEvaluationResult:
        # TODO: fix circular import error
        from fused_batch._quick.udf import run as _run_realtime

        return _run_realtime(
            df_left=df_left,
            step_config=self,
            params=kwargs,
            client_id=_client_id,
        )


class JoinJobStepConfig(JobStepConfig):
    type: Literal["join"] = "join"
    udf: AnyBaseUdf
    input_left: AnyDatasetInput
    input_right: AnyDatasetInput
    output: AnyDatasetOutput
    how: Union[JoinType, Literal["left", "inner"]] = JoinType.INNER
    buffer_distance: Optional[Union[StrictInt, StrictFloat]] = None
    model_config = ConfigDict(validate_assignment=True)

    @property
    def input_metadata(self) -> AnyDatasetInput:
        return self.input_left

    def set_input(
        self,
        input_left: Optional[CoerceableToDatasetInput] = None,
        input_right: Optional[CoerceableToDatasetInput] = None,
        *,
        inplace: bool = False,
    ) -> JoinJobStepConfig:
        """Set the input tables on this operation

        Args:
            input_left: The new left input
            input_right: The new right input

        Keyword Args:
            inplace: If True, modify and return this object. If False, modify and return a copy. Defaults to False.
        """
        from ...models.coerce_dataset import _object_to_dataset_input

        ret = _maybe_inplace(self, inplace)

        if input_left is not None:
            ret.input_left = _object_to_dataset_input(input_left)

        if input_right is not None:
            ret.input_right = _object_to_dataset_input(input_right)

        return ret

    def set_udf(
        self,
        udf: AnyBaseUdf | dict | str,
        parameters: Optional[Dict[str, Any]] = None,
        replace_parameters: bool = False,
        inplace: bool = False,
    ) -> JoinJobStepConfig:
        """Set a user-defined function on this operation

        Args:
            udf: the representation of this UDF
            parameters: Parameters to set on the UDF. Defaults to None to not set parameters.
            replace_parameters: If True, unset any parameters not passed in parameters. Defaults to False.
            inplace: If True, modify and return this object. If False, modify and return a copy. Defaults to False.
        """
        ret = _maybe_inplace(self, inplace)
        ret.udf = RootAnyBaseUdf.model_validate(udf).root

        if parameters is not None:
            _assert_udf_has_parameters(ret.udf)
            ret.udf = ret.udf.set_parameters(
                parameters, replace_parameters=replace_parameters, inplace=False
            )

        return ret

    def open_output(self, **kwargs) -> Table:
        """Opens the output of this operation

        Args:
            kwargs: Additional arguments to pass to open

        Returns:
            The Table that was generated by this operation
        """
        if isinstance(self.output, DatasetOutputV2) and self.output.url is not None:
            return self._api.open_table(self.output.url, **kwargs)
        else:
            raise ValueError("Output has unknown type or no output is set")

    def _validate_for_run(
        self,
        *,
        ignore_no_udf: bool = False,
        ignore_no_output: bool = False,
        validate_imports: Optional[bool] = None,
        validate_inputs: bool = True,
    ):
        _common_validate_for_run(
            output=self.output,
            udf=self.udf,
            ignore_no_udf=ignore_no_udf,
            ignore_no_output=ignore_no_output,
            validate_imports=validate_imports,
        )

    def get_sample(
        self,
        file_id: str | int | None = None,
        chunk_id: int | None = None,
        n_rows: int | None = None,
        use_cache: bool = True,
    ) -> JoinInput:
        """Fetch a sample of this operation

        Args:
            file_id: The identifier of this file. Defaults to None.
            chunk_id: The numeric index of the chunk within the file to fetch. Defaults to None.
            n_rows: The maximum number of rows to sample from the left dataset. Defaults to None for all rows in the chunk.
            use_cache: If True, use a cached sample if available. Defaults to True.

        Returns:

            Sample data retrieved from the given file and chunk.
        """
        sample_coords = (file_id, chunk_id, n_rows)

        def generator():
            return self._api.sample_join(
                config=self,
                file_id=file_id,
                chunk_id=chunk_id,
                n_rows=n_rows,
            )

        if use_cache:
            return get_or_cache_sample(self, sample_coords, generator)
        else:
            return generator()

    def run_local(
        self,
        file_id: str | int | None = None,
        chunk_id: int | None = None,
        n_rows: int | None = None,
        sample: JoinInput | None = None,
        validate_output: bool = True,
        validate_imports: Optional[bool] = None,
        use_cache: bool = True,
        **kwargs,
    ) -> UdfEvaluationResult:
        """
        Run a UDF locally on sample data.

        Args:
            file_id (str or int or None, optional): Identifier for the file containing the data.
                Defaults to None, in which case a file is automatically chosen.
            chunk_id (int or None, optional): Identifier for the specific chunk of data within the file.
                Defaults to None, in which case a chunk is automatically chosen.
            n_rows: The maximum number of rows to sample from the left dataset. Defaults to None for all rows in the chunk.
            sample: If sample is passed, it is used instead of retrieving a sample.
            validate_output: If True, the output of the UDF is validated and schema is updated. If False,
                the output is returned as-is. Defaults to True.
            use_cache: If True, use a cached sample if available. Defaults to True.
            **kwargs: Additional keyword arguments to be passed to the UDF.

        Returns:
            The output of the user-defined function (UDF) applied to the input data.

        Raises:
            Any exceptions raised by the user-defined function (UDF) during its execution.
        """
        sample = (
            self.get_sample(
                file_id=file_id, chunk_id=chunk_id, n_rows=n_rows, use_cache=use_cache
            )
            if sample is None
            else sample
        )

        return execute_against_sample(
            self.udf,
            sample,
            validate_output=validate_output,
            validate_imports=validate_imports,
            **kwargs,
        )

    def run_remote(
        self,
        output_table: Optional[str] = ...,
        instance_type: Optional[WHITELISTED_INSTANCE_TYPES] = None,
        *,
        region: str | None = None,
        disk_size_gb: int | None = None,
        additional_env: List[str] | None = None,
        image_name: Optional[str] = None,
        ignore_no_udf: bool = False,
        ignore_no_output: bool = False,
        validate_imports: Optional[bool] = None,
        parameters: Dict[str, Any] | None = None,
        replace_parameters: bool = False,
        overwrite: Optional[bool] = None,
    ) -> RunResponse:
        to_run = self.model_copy(deep=True)
        if parameters is not None:
            _assert_udf_has_parameters(self.udf)
            to_run = to_run.set_udf(
                self.udf.set_parameters(
                    parameters, replace_parameters=replace_parameters, inplace=False
                ),
                inplace=False,
            )
        if output_table is Ellipsis:
            if not self.output.table:
                raise ValueError("The Job requires `output_table` to be specified.")
            elif overwrite is not None:
                to_run.output.overwrite = overwrite
        elif output_table is not None:
            to_run = to_run.set_output(
                table_or_url=output_table, overwrite=overwrite, inplace=False
            )
        else:
            ignore_no_output = True
        return to_run._run_remote(
            instance_type=instance_type,
            region=region,
            disk_size_gb=disk_size_gb,
            additional_env=additional_env,
            image_name=image_name,
            ignore_no_udf=ignore_no_udf,
            ignore_no_output=ignore_no_output,
            validate_imports=validate_imports,
        )

    def get_output_chunk(
        self,
        file_id: str | int | None = None,
        chunk_id: int | None = None,
    ) -> Union[pa.Table, pd.DataFrame, gpd.GeoDataFrame]:
        """Fetch a sample of the output of this operation

        Args:
            file_id: The identifier of this file. Defaults to None.
            chunk_id: The numeric index of the chunk within the file to fetch. Defaults to None.

        Returns:
            Sample data retrieved from the given file and chunk.
        """
        if isinstance(self.output, DatasetOutputV2) and self.output.url:
            return _get_chunk_v2(
                url=self.output.url,
                file_id=file_id,
                chunk_id=chunk_id,
            )
        else:
            raise ValueError("Unknown output type or no output URL is set")

    def _repr_html_(self) -> str:
        return fused_join_repr(self)

    def run_realtime(
        self,
        df_left: Optional[
            Union[pd.DataFrame, gpd.GeoDataFrame, pa.Table, str, Path]
        ] = None,
        df_right: Optional[
            Union[pd.DataFrame, gpd.GeoDataFrame, pa.Table, str, Path]
        ] = None,
        *,
        _client_id: Optional[str] = None,
        **kwargs,
    ) -> UdfEvaluationResult:
        # TODO: fix circular import error
        from fused_batch._quick.udf import run as _run_realtime

        return _run_realtime(
            df_left=df_left,
            df_right=df_right,
            step_config=self,
            params=kwargs,
            client_id=_client_id,
        )


class JoinSinglefileJobStepConfig(JobStepConfig):
    type: Literal["join_singlefile"] = "join_singlefile"
    udf: AnyBaseUdf
    input_left: AnyDatasetInput
    input_right: StrictStr
    output: AnyDatasetOutput
    experimental_read_once: Optional[StrictBool] = None
    experimental_read_udf: Optional[AnyBaseUdf] = None

    @property
    def input_metadata(self) -> AnyDatasetInput:
        return self.input_left

    model_config = ConfigDict(validate_assignment=True)

    def set_input(
        self,
        input_left: Optional[CoerceableToDatasetInput] = None,
        input_right: Optional[str] = None,
        *,
        inplace: bool = False,
    ) -> JoinSinglefileJobStepConfig:
        """Set the input tables on this operation

        All arguments except for input_right apply to the left dataset.

        Args:
            input_left: URL of the left table to read.
            input_right: URL of the right dataset file. Defaults to None for no update.

        Keyword Args:
            inplace: If True, modify and return this object. If False, modify and return a copy. Defaults to False.
        """
        from ...models.coerce_dataset import _object_to_dataset_input

        ret = _maybe_inplace(self, inplace)

        if input_left is not None:
            ret.input_left = _object_to_dataset_input(input_left)

        if input_right is not None:
            ret.input_right = input_right

        return ret

    def set_udf(
        self,
        udf: AnyBaseUdf | dict | str,
        parameters: Optional[Dict[str, Any]] = None,
        replace_parameters: bool = False,
        inplace: bool = False,
    ) -> JoinSinglefileJobStepConfig:
        """Set a user-defined function on this operation

        Args:
            udf: the representation of this UDF
            parameters: Parameters to set on the UDF. Defaults to None to not set parameters.
            replace_parameters: If True, unset any parameters not passed in parameters. Defaults to False.
            inplace: If True, modify and return this object. If False, modify and return a copy. Defaults to False.
        """
        ret = _maybe_inplace(self, inplace)
        ret.udf = RootAnyBaseUdf.model_validate(udf).root

        if parameters is not None:
            _assert_udf_has_parameters(ret.udf)
            ret.udf = ret.udf.set_parameters(
                parameters, replace_parameters=replace_parameters, inplace=False
            )

        return ret

    def open_output(self, **kwargs) -> Table:
        """Opens the output of this operation

        Args:
            kwargs: Additional arguments to pass to open

        Returns:
            The Table that was generated by this operation
        """
        if isinstance(self.output, DatasetOutputV2) and self.output.url is not None:
            return self._api.open_table(self.output.url, **kwargs)
        else:
            raise ValueError("Output has unknown type or no output is set")

    def _validate_for_run(
        self,
        *,
        ignore_no_udf: bool = False,
        ignore_no_output: bool = False,
        validate_imports: Optional[bool] = None,
        validate_inputs: bool = True,
    ):
        _common_validate_for_run(
            output=self.output,
            udf=self.udf,
            ignore_no_udf=ignore_no_udf,
            ignore_no_output=ignore_no_output,
            validate_imports=validate_imports,
        )

    def get_sample(
        self,
        file_id: str | int | None = None,
        chunk_id: int | None = None,
        n_rows: int | None = None,
        use_cache: bool = True,
    ) -> JoinSingleFileInput:
        """Fetch a sample of this operation

        Args:
            file_id: The identifier of this file. Defaults to None.
            chunk_id: The numeric index of the chunk within the file to fetch. Defaults to None.
            n_rows: The maximum number of rows to sample from the left dataset. Defaults to None for all rows in the chunk.
            use_cache: If True, use a cached sample if available. Defaults to True.

        Returns:

            Sample data retrieved from the given file and chunk.
        """
        sample_coords = (file_id, chunk_id, n_rows)

        def generator():
            return self._api.sample_single_file_join(
                config=self,
                file_id=file_id,
                chunk_id=chunk_id,
                n_rows=n_rows,
            )

        if use_cache:
            return get_or_cache_sample(self, sample_coords, generator)
        else:
            return generator()

    def run_local(
        self,
        file_id: str | int | None = None,
        chunk_id: int | None = None,
        n_rows: int | None = None,
        sample: JoinSingleFileInput | None = None,
        validate_output: bool = True,
        validate_imports: Optional[bool] = None,
        use_cache: bool = True,
        **kwargs,
    ) -> UdfEvaluationResult:
        """
        Run a UDF locally on sample data.

        Args:
            file_id (str or int or None, optional): Identifier for the file containing the data.
                Defaults to None, in which case a file is automatically chosen.
            chunk_id (int or None, optional): Identifier for the specific chunk of data within the file.
                Defaults to None, in which case a chunk is automatically chosen.
            n_rows: The maximum number of rows to sample from the left dataset. Defaults to None for all rows in the chunk.
            sample: If sample is passed, it is used instead of retrieving a sample.
            validate_output: If True, the output of the UDF is validated and schema is updated. If False,
                the output is returned as-is. Defaults to True.
            use_cache: If True, use a cached sample if available. Defaults to True.
            **kwargs: Additional keyword arguments to be passed to the UDF.

        Returns:
            The output of the user-defined function (UDF) applied to the input data.

        Raises:
            Any exceptions raised by the user-defined function (UDF) during its execution.
        """
        sample = (
            self.get_sample(
                file_id=file_id, chunk_id=chunk_id, n_rows=n_rows, use_cache=use_cache
            )
            if sample is None
            else sample
        )

        return execute_against_sample(
            self.udf,
            sample,
            validate_output=validate_output,
            validate_imports=validate_imports,
            **kwargs,
        )

    def run_remote(
        self,
        output_table: Optional[str] = ...,
        instance_type: Optional[WHITELISTED_INSTANCE_TYPES] = None,
        *,
        region: str | None = None,
        disk_size_gb: int | None = None,
        additional_env: List[str] | None = None,
        image_name: Optional[str] = None,
        ignore_no_udf: bool = False,
        ignore_no_output: bool = False,
        parameters: Dict[str, Any] | None = None,
        replace_parameters: bool = False,
        overwrite: Optional[bool] = None,
        validate_imports: Optional[bool] = None,
    ) -> RunResponse:
        to_run = self.model_copy(deep=True)
        if parameters is not None:
            _assert_udf_has_parameters(self.udf)
            to_run = to_run.set_udf(
                self.udf.set_parameters(
                    parameters, replace_parameters=replace_parameters, inplace=False
                ),
                inplace=False,
            )
        if output_table is Ellipsis:
            if not self.output.table:
                raise ValueError("The Job requires `output_table` to be specified.")
            elif overwrite is not None:
                to_run.output.overwrite = overwrite
        elif output_table is not None:
            to_run = to_run.set_output(
                table_or_url=output_table, overwrite=overwrite, inplace=False
            )
        else:
            ignore_no_output = True
        return to_run._run_remote(
            instance_type=instance_type,
            region=region,
            disk_size_gb=disk_size_gb,
            additional_env=additional_env,
            image_name=image_name,
            ignore_no_udf=ignore_no_udf,
            ignore_no_output=ignore_no_output,
            validate_imports=validate_imports,
        )

    def get_output_chunk(
        self,
        file_id: str | int | None = None,
        chunk_id: int | None = None,
    ) -> Union[pa.Table, pd.DataFrame, gpd.GeoDataFrame]:
        """Fetch a sample of the output of this operation

        Args:
            file_id: The identifier of this file. Defaults to None.
            chunk_id: The numeric index of the chunk within the file to fetch. Defaults to None.

        Returns:
            Sample data retrieved from the given file and chunk.
        """
        if isinstance(self.output, DatasetOutputV2) and self.output.url:
            return _get_chunk_v2(
                url=self.output.url,
                file_id=file_id,
                chunk_id=chunk_id,
            )
        else:
            raise ValueError("Unknown output type or no output URL is set")

    def _repr_html_(self) -> str:
        return fused_join_singlefile_repr(self)


AnyJobStepConfig = Annotated[
    Union[
        MapJobStepConfig,
        JoinJobStepConfig,
        JoinSinglefileJobStepConfig,
        UdfJobStepConfig,
        GeospatialPartitionJobStepConfig,
        NonGeospatialPartitionJobStepConfig,
    ],
    Field(..., discriminator="type"),
]


class RootAnyJobStepConfig(RootModel[AnyJobStepConfig]):
    pass


class JobConfig(FusedBaseModel):
    name: Optional[StrictStr] = None
    """The name of the job."""

    steps: List[AnyJobStepConfig]
    """The individual steps to run in sequence in the job."""

    metadata: UserMetadataType = None
    """User defined metadata. Any metadata values must be JSON serializable."""
    _validate_version: bool = True

    @property
    def udfs(self) -> UdfRegistry:
        udf_dict = {}
        for step in self.steps:
            udf_dict[step.udf.name] = step.udf
        return UdfRegistry(udf_dict)

    def _validate_for_run(
        self,
        *,
        ignore_no_udf: bool = False,
        ignore_no_output: bool = False,
        validate_imports: Optional[bool] = None,
        validate_inputs: bool = True,
    ):
        for step in self.steps:
            step._validate_for_run(
                ignore_no_udf=ignore_no_udf,
                ignore_no_output=ignore_no_output,
                validate_imports=validate_imports,
                validate_inputs=validate_inputs,
            )

    def run_remote(
        self,
        instance_type: Optional[WHITELISTED_INSTANCE_TYPES] = None,
        *,
        region: str | None = None,
        disk_size_gb: int | None = None,
        additional_env: List[str] | None = None,
        image_name: Optional[str] = None,
        ignore_no_udf: bool = False,
        ignore_no_output: bool = False,
        validate_imports: Optional[bool] = None,
        validate_inputs: bool = True,
        **kwargs,
    ) -> RunResponse:
        """Execute an operation

        Keyword Args:
            region: The AWS region in which to run. Defaults to None.
            instance_type: The AWS EC2 instance type to use for the job. Acceptable strings are "m5.large", "m5.xlarge", "m5.2xlarge", "m5.4xlarge", "m5.8xlarge", "m5.12xlarge", "m5.16xlarge", "r5.large", "r5.xlarge", "r5.2xlarge", "r5.4xlarge", "r5.8xlarge", "r5.12xlarge", or "r5.16xlarge". Defaults to None.
            disk_size_gb: The disk size to specify for the job. Defaults to None.
            additional_env: Any additional environment variables to be passed into the job, each in the form KEY=value. Defaults to None.
            image_name: Custom image name to run. Defaults to None for default image.
        """
        assert self._api is not None

        # Operate on a copy because step parameters might change.
        ret = _maybe_inplace(self, inplace=False)

        # TODO: if the user uses start_job, this validation will never happen
        ret._validate_for_run(
            ignore_no_udf=ignore_no_udf,
            ignore_no_output=ignore_no_output,
            validate_imports=validate_imports,
            validate_inputs=validate_inputs,
        )

        for step in ret.steps:
            if hasattr(step, "udf"):
                filtered_kwargs = {
                    k: v for k, v in kwargs.items() if k in step.udf._parameter_list
                }

                step.udf.parameters.update(filtered_kwargs)

        return ret._api.start_job(
            config=self,
            instance_type=instance_type,
            region=region,
            disk_size_gb=disk_size_gb,
            additional_env=additional_env,
            image_name=image_name,
        )

    def _to_job_step_config(self) -> JobStepConfig:
        if len(self.steps) > 1:
            warnings.warn(
                "input has more than one job step, taking the first",
                FusedDefaultWarning,
            )
        assert len(self.steps) > 0, "Input should have a job step defined"
        return self.steps[0]

    def _repr_html_(self) -> str:
        return fused_job_repr(self)

    def export(
        self,
        path,
        how: Literal["local", "zip"] = "local",
        overwrite=False,
    ):
        _export(job=self, path=path, how=how, overwrite=overwrite)

    def _generate_code(self, headerfile=False):
        udfs = {}
        header_cells_list = []
        jobs = []
        job_names = []
        for step in self.steps:
            str_udf, header_cells = step.udf._generate_code(
                include_imports=False, headerfile=headerfile
            )
            udfs[step.udf.name] = str_udf
            header_cells_list.extend(header_cells)
            # TODO: catch overlapping names
            # String: job instantiation
            job_names.append(f"job_{step.udf.name}")
            jobs.append(
                f"job_{step.udf.name} = {step.udf.name}({structure_params(step._generate_job_params())})"
            )

        # String: Job steps
        str_udfs = "\n\n".join(udfs.values())
        str_job = "\n".join(jobs)
        if len(job_names) == 1:
            str_multijob = f"job = fused_batch.experimental.job({job_names[0]})"
        else:
            str_multijob = (
                f"job = fused_batch.experimental.job([{', '.join(job_names)}])"
            )
        # String: Job execution
        str_job_exec = "job.run_local()"
        # Structure cell
        src = f"""
{STR_IMPORTS}
{str_udfs}\n
{str_job}
{str_multijob}
{str_job_exec}
"""
        return src, set(header_cells_list)

    def run_local(
        self,
        validate_output: bool = ...,
        validate_imports: Optional[bool] = None,
        *args,
        **kwargs,
    ) -> MultiUdfEvaluationResult:
        # For each step, run the JobStepConfig with run_local
        runs = []
        for step in self.steps:
            filtered_kwargs = {
                k: v for k, v in kwargs.items() if k in step.udf._parameter_list
            }

            # Unless validate_output is set, use default
            if validate_output is Ellipsis:
                _step = step.run_local(
                    validate_imports=validate_imports, *args, **filtered_kwargs
                )
            else:
                _step = step.run_local(
                    validate_output=validate_output,
                    validate_imports=validate_imports,
                    *args,
                    **filtered_kwargs,
                )
            runs.append(_step)
        return MultiUdfEvaluationResult(udf_results=[run for run in runs])

    def render(self, headerfile=False):
        _render(self, headerfile=headerfile)

    def get_sample(self):
        raise NotImplementedError(
            "Cannot get sample of a job. Please call get_sample on a job step. For example: `job.steps[0].get_sample()`"
        )


def _get_chunk(
    *,
    base_path: str,
    tables: Sequence[str],
    file_id: Optional[Union[str, int]] = None,
    chunk_id: Optional[int] = None,
    n_rows: Optional[int] = None,
) -> Union[pa.Table, pd.DataFrame, gpd.GeoDataFrame]:
    # TODO: Consider optimizing for the Docker case
    if len(tables) == 1:
        return _get_chunk_v2(
            url=append_url_part(base_path, tables[0]),
            file_id=file_id,
            chunk_id=chunk_id,
            n_rows=n_rows,
        )
    dataset_input = DatasetInput(
        base_path=base_path,
        tables=tables,
    )
    map_config = MapJobStepConfig(
        input=dataset_input,
        output=DatasetOutputV2(),
        udf=EMPTY_UDF,
    )
    map_input = map_config.get_sample(file_id=file_id, chunk_id=chunk_id, n_rows=n_rows)
    return map_input.data


def _get_chunk_v2(
    *,
    url: str,
    file_id: Optional[Union[str, int]] = None,
    chunk_id: Optional[int] = None,
    n_rows: Optional[int] = None,
) -> Union[pa.Table, pd.DataFrame, gpd.GeoDataFrame]:
    # TODO: Consider optimizing for the Docker case
    dataset_input = DatasetInputV2.from_table_url(url)
    map_config = MapJobStepConfig(
        input=dataset_input,
        output=DatasetOutputV2(),
        udf=EMPTY_UDF,
    )
    map_input = map_config.get_sample(file_id=file_id, chunk_id=chunk_id, n_rows=n_rows)
    return map_input.data


def _get_file(
    *,
    base_path: str,
    tables: Sequence[str],
    file_id: Optional[Union[str, int]] = None,
    n_rows: Optional[int] = None,
) -> Union[pa.Table, pd.DataFrame, gpd.GeoDataFrame]:
    # TODO: Consider optimizing for the Docker case
    if len(tables) == 1:
        return _get_file_v2(
            url=append_url_part(base_path, tables[0]),
            file_id=file_id,
            n_rows=n_rows,
        )
    dataset_input = DatasetInput(
        base_path=base_path,
        tables=tables,
    )
    map_config = MapJobStepConfig(
        input=dataset_input,
        output=DatasetOutputV2(),
        udf=EMPTY_UDF,
    )
    map_input = map_config._whole_file_sample(file_id=file_id, n_rows=n_rows)
    return map_input.data


def _get_file_v2(
    *,
    url: str,
    file_id: Optional[Union[str, int]] = None,
    n_rows: Optional[int] = None,
) -> Union[pa.Table, pd.DataFrame, gpd.GeoDataFrame]:
    # TODO: Consider optimizing for the Docker case
    dataset_input = DatasetInputV2.from_table_url(url)
    map_config = MapJobStepConfig(
        input=dataset_input,
        output=DatasetOutputV2(),
        udf=EMPTY_UDF,
    )
    map_input = map_config._whole_file_sample(file_id=file_id, n_rows=n_rows)
    return map_input.data


def _validate_headers_for_remote_exec(udf: AnyBaseUdf) -> bool:
    """If unresolved headers reference local files, returns False."""

    for header in udf.headers:
        # If header is a string that is not a remote path.
        if isinstance(header, str) and not is_url(header):
            warnings.warn(f"Header {header} cannot resolve remotely.")
            return False

    return True


def _export(job, path, how, overwrite=False):
    # Validate `how`
    if how not in ("gist", "local", "zip"):
        raise ValueError("`how` must be one of 'local', or 'zip'")
    # Handle single step jobs
    if isinstance(job, JobStepConfig):
        job = JobConfig(steps=[job])

    files = {
        "meta.json": generate_meta_json(job),
        # "multijob.py": obj._generate_code(headerfile=True),
        "README.md": generate_readme(job),
    }

    # Files: UDFs & Headers
    for step in job.steps:
        for header in step.udf.headers:
            # Don't raise warning if header names overlap, since they're shared.
            header_filename = header.module_name + ".py"
            if header_filename not in files:
                src = header.source_code
                files[header_filename] = src
        # Raise warning if UDF names overlap.
        udf_filename = f"udf_{step.udf.name}.py"
        if udf_filename not in files:
            files[udf_filename] = STR_IMPORTS + step.udf.code
        else:
            warnings.warn(
                f"Duplicate UDF name {step.udf.name}. Skipping.",
                FusedDefaultWarning,
            )

    # Export
    create_directory_and_zip(path=path, how=how, files=files, overwrite=overwrite)


def _render(job, headerfile=False):
    def create_new_cell(contents):
        """Similar to ipython.set_next_input but allows multiple cells to be created at once."""
        from IPython.core.getipython import get_ipython

        shell = get_ipython()

        payload = dict(
            source="set_next_input",
            text=contents,
            replace=False,
        )
        shell.payload_manager.write_payload(payload, single=False)

    # Get the current IPython instance.
    ipython = get_ipython()
    if ipython is None:
        raise RuntimeError("This function can only be used in a Jupyter Notebook.")

    # Create an instance of IPythonInputSplitter.
    splitter = IPythonInputSplitter()

    # Generate code string and split into lines.
    src_udf, header_cells = job._generate_code(headerfile=headerfile)
    lines = src_udf.strip().split("\n")

    # Set the content of the subsequent cell with.
    create_new_cell(splitter.transform_cell("\n".join(lines)))

    # Headers
    if headerfile:
        for header in header_cells:
            create_new_cell(header)
