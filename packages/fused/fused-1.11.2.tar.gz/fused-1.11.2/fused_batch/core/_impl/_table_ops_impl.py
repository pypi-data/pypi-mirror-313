import base64
from io import BytesIO
from typing import Iterable, Optional, Union

import geopandas as gpd
import geopandas.io.arrow
import pandas as pd
import pyarrow.parquet as pq
import shapely


def _normalize_url(url: str) -> str:
    if url.endswith("/"):
        return url[:-1]
    return url


def get_chunks_metadata(url: str) -> gpd.GeoDataFrame:
    """Returns a GeoDataFrame with each chunk in the table as a row.

    Args:
        url: URL of the table.
    """
    url = _normalize_url(url) + "/_sample"

    with pq.ParquetFile(url) as file:
        # do not use pq.read_metadata as it may segfault in versions >= 12 (tested on 15.0.1)
        sample_metadata = file.metadata

    if (
        b"fused:format_version" not in sample_metadata.metadata.keys()
        or sample_metadata.metadata[b"fused:format_version"] != b"5"
    ):
        raise ValueError(
            "Dataset does not have Fused metadata or it is an incompatible version."
        )

    metadata_bytes = sample_metadata.metadata[b"fused:_metadata"]
    metadata_bytes = base64.decodebytes(metadata_bytes)
    metadata_bio = BytesIO(metadata_bytes)
    chunks_df = pd.read_parquet(metadata_bio)
    return gpd.GeoDataFrame(
        chunks_df,
        geometry=chunks_df.apply(
            lambda row: shapely.box(
                xmin=row.bbox_minx,
                ymin=row.bbox_miny,
                xmax=row.bbox_maxx,
                ymax=row.bbox_maxy,
            ),
            axis=1,
        ),
    )


def get_chunk_from_table(
    url: str,
    file_id: Union[str, int, None],
    chunk_id: Optional[int],
    *,
    columns: Optional[Iterable[str]] = None,
) -> gpd.GeoDataFrame:
    """Returns a chunk from a table and chunk coordinates.

    This can be called with file_id and chunk_id from `get_chunks_metadata`.

    Args:
        url: URL of the table.
        file_id: File ID to read.
        chunk_id: Chunk ID to read.
    """
    if file_id is None:
        return gpd.read_parquet(url)
    else:
        url = _normalize_url(url) + f"/{file_id}.parquet"

    with pq.ParquetFile(url) as file:
        if chunk_id is not None:
            table = file.read_row_group(chunk_id, columns=columns)
        else:
            table = file.read(columns=columns)

        if b"geo" in table.schema.metadata:
            return geopandas.io.arrow._arrow_to_geopandas(table)
        else:
            return table.to_pandas()
