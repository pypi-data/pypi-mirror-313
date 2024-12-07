from __future__ import annotations

import warnings
from enum import Enum
from typing import Dict, List, Literal, Optional, Union
from urllib.parse import urlparse

from pydantic import BaseModel, Field, RootModel, StrictBool, StrictStr, field_validator
from typing_extensions import Annotated

from fused_batch._constants import DEFAULT_TABLE_NAMES
from fused_batch._str_utils import append_url_part
from fused_batch.warnings import FusedDeprecationWarning

from .._project_aware import FusedProjectAware
from ..base import FusedBaseModel
from ..urls import dataset_url_schema_validator


class DatasetInputBase(FusedBaseModel):
    type: Literal[None, "v2"]


class DatasetInput(DatasetInputBase):
    """(Deprecated) A class to describe a dataset to be used in a join or map operation"""

    type: Literal[None] = None

    base_path: StrictStr
    """The base path of the input dataset."""
    tables: List[StrictStr] = Field(default_factory=lambda: list(DEFAULT_TABLE_NAMES))
    """The list of table names to fetch in the operation."""

    cache_locally: StrictBool = False
    """Whether to cache all files from the input locally."""

    read_sidecar_files: Optional[Dict[StrictStr, StrictBool]] = None
    """Whether to read sidecar files from the input as part of the operation."""

    first_n: Optional[int] = None
    """Process only the first N files of the dataset. This is for debugging and benchmarking purposes.

    Note that this can produce output tables that are missing files.
    """

    file_sort_field: Optional[str] = None
    """When processing files, use this field on the metadata table to sort the files"""

    @field_validator("base_path")
    @classmethod
    def validate_base_path(cls, val):
        dataset_url_schema_validator.validate_python(val)
        return val

    def __init__(self, **data):
        super().__init__(**data)
        warnings.warn("DatasetInput class is deprecated", FusedDeprecationWarning)


class DatasetInputType(str, Enum):
    V2 = "v2"
    """Zip or Union operation"""


class DatasetInputV2Type(str, Enum):
    ZIP = "zip"
    """Append column-wise within partitions"""
    UNION = "union"
    """Append partitions"""


class DatasetInputV2Table(BaseModel):
    url: StrictStr
    read_sidecar_files: Optional[StrictBool] = None
    cache_locally: StrictBool = False

    @field_validator("url")
    @classmethod
    def validate_base_path(cls, val):
        dataset_url_schema_validator.validate_python(val)
        return val


class DatasetInputV2(DatasetInputBase, FusedProjectAware):
    type: Literal["v2"] = "v2"

    operation: DatasetInputV2Type

    tables: List[DatasetInputV2Table]
    # TODO: columns: Any = None
    # TODO: rename columns
    # TODO: Move buffer_distance here

    first_n: Optional[int] = None
    """Process only the first N files of the dataset. This is for debugging and benchmarking purposes.

    Note that this can produce output tables that are missing files."""
    file_sort_field: Optional[str] = None
    """When processing files, use this field on the metadata table to sort the files"""

    @classmethod
    def from_table_url(cls, url: str, *, cache_locally: bool = False) -> DatasetInputV2:
        """Create a DatasetInputV2 that reads a single table from a URL."""
        return cls(
            # The specific operation isn't important, ZIP is just a convenient default.
            operation=DatasetInputV2Type.ZIP,
            tables=[DatasetInputV2Table(url=url, cache_locally=cache_locally)],
        )


AnyDatasetInput = Annotated[
    Union[
        DatasetInput,
        DatasetInputV2,
    ],
    Field(..., discriminator="type"),
]


class RootAnyDatasetInput(RootModel[AnyDatasetInput]):
    pass


class SampleStrategy(str, Enum):
    """How to generate output samples"""

    EMPTY = "empty"
    """Do not generate a sample"""
    FIRST_CHUNK = "first_chunk"
    """The sample is from the first chunk"""
    GEO = "geo"
    """Geographically sample"""


class DatasetOutputType(str, Enum):
    V2 = "v2"
    """Save as a table to a URL"""


class DatasetOutputBase(BaseModel):
    type: Literal[None, "v2"]

    save_index: Optional[StrictBool] = None
    """Whether to override saving the output index."""

    sample_strategy: Optional[SampleStrategy] = None
    """How to generate output samples, or None for the default."""

    overwrite: bool = False
    """Whether the API should overwrite the output dataset if it already exists."""

    def from_str(
        s: Optional[str], project_url: Optional[str] = None
    ) -> AnyDatasetOutput:
        try:
            parsed = urlparse(s)
            if parsed.scheme:
                output = DatasetOutputV2(url=s)
                output._project_url = project_url
                return output
        except (ValueError, TypeError, AttributeError):
            pass

        if project_url is not None:
            url = append_url_part(project_url, s) if s is not None else None
            output = DatasetOutputV2(url=url)
            output._project_url = project_url
            return output

        if s is None:
            return DatasetOutputV2()

        # Parsing as URL failed
        return DatasetOutput(table=s)


class DatasetOutput(DatasetOutputBase):
    """(Deprecated) Output that writes a table to a dataset"""

    type: Literal[None] = None
    base_path: Optional[StrictStr] = None
    table: Optional[StrictStr] = None

    def __init__(self, **data):
        super().__init__(**data)
        warnings.warn("DatasetOutput class is deprecated", FusedDeprecationWarning)


class DatasetOutputV2(DatasetOutputBase, FusedProjectAware):
    """Output that writes a table to a URL"""

    type: Literal["v2"] = "v2"

    url: Optional[StrictStr] = None
    """Table URL to write to"""

    def to_v1(self) -> DatasetOutput:
        """Converts this output object to a DatasetOutput (V1)"""
        if self.url is None:
            return DatasetOutput(
                base_path=None,
                table=None,
                save_index=self.save_index,
                sample_strategy=self.sample_strategy,
            )

        base_path, table = self.url.rstrip("/").rsplit("/", maxsplit=1)
        return DatasetOutput(
            base_path=base_path,
            table=table,
            save_index=self.save_index,
            sample_strategy=self.sample_strategy,
            overwrite=self.overwrite,
        )

    @property
    def table(self) -> Optional[str]:
        """Returns the table name for this output"""
        if self.url:
            return self.url.rstrip("/").rsplit("/", maxsplit=1)[1]
        return None


AnyDatasetOutput = Annotated[
    Union[
        DatasetOutput,
        DatasetOutputV2,
    ],
    Field(..., discriminator="type"),
]
