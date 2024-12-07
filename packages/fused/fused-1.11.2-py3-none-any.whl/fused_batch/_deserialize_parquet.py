from io import BytesIO
from typing import Union

import geopandas as gpd
import pandas as pd


def parquet_to_df(b: bytes) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
    try:
        return gpd.read_parquet(BytesIO(b))
    except:  # noqa: E722
        return pd.read_parquet(BytesIO(b))
