from typing import Optional, Protocol, Union

import geopandas as gpd
import pandas as pd

from fused_batch.models.schema import Schema
from fused_batch.models.udf.output import Output as OutputModel


class Output(Protocol):
    @property
    def data(self) -> Union[pd.DataFrame, gpd.GeoDataFrame, None]:
        ...

    @data.setter
    def data(self, value: Union[pd.DataFrame, gpd.GeoDataFrame, None]):
        ...

    @property
    def table_schema(self) -> Optional[Schema]:
        ...

    @table_schema.setter
    def table_schema(self, value: Optional[Schema]):
        ...


output: Output = OutputModel()
