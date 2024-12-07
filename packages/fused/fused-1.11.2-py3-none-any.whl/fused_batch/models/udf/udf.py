from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Literal, Optional, Sequence, Union

from pydantic import Field, PrivateAttr, RootModel
from typing_extensions import Annotated

from fused_batch.models.schema import Schema
from fused_batch.models.udf.base_udf import BaseUdf, UdfType

from .._inplace import _maybe_inplace


class JoinType(str, Enum):
    LEFT = "left"
    INNER = "inner"


class GeoPandasUdfV2(BaseUdf):
    """A user-defined function that operates on [`geopandas.GeoDataFrame`s][geopandas.GeoDataFrame]."""

    type: Literal[UdfType.GEOPANDAS_V2] = UdfType.GEOPANDAS_V2
    table_schema: Optional[Schema] = None
    """The [`Schema`][fused.models.Schema] describing the output of this UDF.
    """

    entrypoint: str
    """Name of the function within the code to invoke."""

    parameters: Dict[str, Any] = Field(default_factory=dict)
    """Parameters to pass into the entrypoint."""

    _parameter_list: Optional[Sequence[str]] = PrivateAttr(None)
    original_headers: Optional[str] = None

    _nested_callable = PrivateAttr(None)  # TODO : Find out type

    def set_parameters(
        self,
        parameters: Dict[str, Any],
        replace_parameters: bool = False,
        inplace: bool = False,
    ) -> "GeoPandasUdfV2":
        """Set the parameters on this UDF.

        Args:
            parameters: The new parameters dictionary.
            replace_parameters: If True, unset any parameters not in the parameters argument. Defaults to False.
            inplace: If True, modify this object. If False, return a new object. Defaults to True.
        """
        ret = _maybe_inplace(self, inplace)
        new_parameters = (
            parameters
            if replace_parameters
            else {
                **ret.parameters,
                **parameters,
            }
        )
        ret.parameters = new_parameters
        return ret

    def eval_schema(self, inplace: bool = False) -> "GeoPandasUdfV2":
        """Reload the schema saved in the code of the UDF.

        Note that this will evaluate the UDF function.

        Args:
            inplace: If True, update this UDF object. Otherwise return a new UDF object (default).
        """
        from fused_batch._udf.execute_v2 import execute_for_decorator

        new_udf = execute_for_decorator(self)
        assert isinstance(
            new_udf, GeoPandasUdfV2
        ), f"UDF has unexpected type: {type(new_udf)}"
        ret = _maybe_inplace(self, inplace)
        ret.table_schema = new_udf.table_schema
        ret._parameter_list = new_udf._parameter_list
        return ret

    def run_local(
        self,
        sample: Any | None = ...,
        *,
        inplace: bool = False,
        validate_output: bool = False,
        validate_imports: Optional[bool] = None,
        **kwargs,
    ) -> "UdfEvaluationResult":  # ruff: noqa: F821
        """Evaluate this UDF against a sample.

        Args:
            sample: Sample (from `get_sample`) to execute against.
            inplace: If True, update this UDF object with schema information. (default)
        """
        from fused_batch._udf.execute_v2 import execute_against_sample
        from fused_batch.models.udf._eval_result import (  # ruff: noqa: F401
            UdfEvaluationResult,
        )

        ret = _maybe_inplace(self, inplace)
        sample_list = [] if sample is Ellipsis else [sample]
        return execute_against_sample(
            udf=ret,
            input=sample_list,
            validate_output=validate_output,
            validate_imports=validate_imports,
            **kwargs,
        )


EMPTY_UDF = GeoPandasUdfV2(
    name="EMPTY_UDF", code="", entrypoint="", table_schema=Schema(fields=[])
)

AnyBaseUdf = Annotated[GeoPandasUdfV2, Field(..., discriminator="type")]


class RootAnyBaseUdf(RootModel[AnyBaseUdf]):
    pass
