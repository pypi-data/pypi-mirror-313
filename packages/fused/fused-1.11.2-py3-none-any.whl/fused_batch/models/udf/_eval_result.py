from typing import Any, List, Optional, Union

import geopandas as gpd
import numpy as np
import pandas as pd
import pyarrow as pa
import xarray as xr
from pydantic import BaseModel, ConfigDict

from fused_batch._formatter.formatter_eval_result import fused_eval_result_repr
from fused_batch.models.schema import Schema
from fused_batch.models.udf import AnyBaseUdf


class UdfEvaluationResult(BaseModel):
    data: Union[
        gpd.GeoDataFrame,
        pd.DataFrame,
        pa.Table,
        xr.Dataset,
        xr.DataArray,
        np.ndarray,
        None,
    ] = None
    sidecar: Optional[bytes] = None

    udf: Optional[AnyBaseUdf] = None
    table_schema: Optional[Schema] = None

    time_taken_seconds: float

    stdout: Optional[str] = None
    stderr: Optional[str] = None
    error_message: Optional[str] = None
    error_lineno: Optional[int] = None

    def _repr_html_(self) -> str:
        return fused_eval_result_repr(self)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class MultiUdfEvaluationResult(BaseModel):
    udf_results: List[Union[UdfEvaluationResult, Any]]

    def _repr_html_(self) -> str:
        # Aggregate reprs
        result_reprs = [
            udf_result._repr_html_()
            if hasattr(udf_result, "_repr_html_")
            else repr(udf_result)
            for udf_result in self.udf_results
        ]
        return "<br><br>".join(result_reprs)

    model_config = ConfigDict(arbitrary_types_allowed=True)
