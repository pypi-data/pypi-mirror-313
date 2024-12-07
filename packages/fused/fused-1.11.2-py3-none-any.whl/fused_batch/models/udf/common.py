from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

import geopandas as gpd
import pandas as pd
import pyarrow as pa
import shapely
from pydantic import BaseModel, ConfigDict, RootModel, StrictStr

if TYPE_CHECKING:
    from pydantic.typing import ReprArgs


class ChunkMetadata(BaseModel):
    file_id: str
    """The identifier of the file that contains this chunk."""

    chunk_id: int
    """The identifier of this chunk inside the file."""

    bbox_minx: float
    """The west-most coordinate of this bounding box."""

    bbox_miny: float
    """The southern-most coordinate of this bounding box."""

    bbox_maxx: float
    """The east-most coordinate of this bounding box."""

    bbox_maxy: float
    """The northern-most coordinate of this bounding box."""

    sum_area: float
    """The sum of all area of all geometries in this chunk.

    !!! note

        Area is currently computed in the WGS84 coordinate system, so it should only be used as a heuristic.
    """

    sum_length: float
    """The sum of all lengths of all geometries in this chunk.

    !!! note

        Length is currently computed in the WGS84 coordinate system, so it should only be used as a heuristic.
    """

    # These are set to optional with a None default because older datasets might not
    # have utm area/length defined
    sum_area_utm: Optional[float] = None
    """The sum of all geometries' area in UTM"""

    sum_length_utm: Optional[float] = None
    """The sum of all geometries' length in UTM"""

    num_coords: int
    """The sum of the number of coordinates among all geometries in this chunk.
    """

    num_rows: int
    """The number of rows in this chunk"""

    def to_box(self) -> shapely.Polygon:
        """Returns a Shapely polygon representing the bounding box of this chunk"""
        return shapely.box(
            xmin=self.bbox_minx,
            ymin=self.bbox_miny,
            xmax=self.bbox_maxx,
            ymax=self.bbox_maxy,
        )


class SidecarDict:
    def __init__(self, wrapped_dict: Dict[StrictStr, bytes]):
        self.wrapped_dict = wrapped_dict

    def __repr__(self) -> str:
        sidecar_details = ", ".join(
            [f"{key}: {len(val)}" for key, val in self.wrapped_dict.items()]
        )
        return f"SidecarDict({sidecar_details})"


def _wrap_sidecar_dict(to_wrap: Dict[StrictStr, bytes]) -> SidecarDict:
    if to_wrap is not None:
        return SidecarDict(to_wrap)
    else:
        return to_wrap


ChunkData = Union[pa.Table, pd.DataFrame, gpd.GeoDataFrame]


class Chunk(BaseModel):
    data: ChunkData
    """The data object contained within this chunk.

    This will either be a [`pandas.DataFrame`][pandas.DataFrame],
    [`geopandas.GeoDataFrame`][geopandas.GeoDataFrame], or
    [`pyarrow.Table`][pyarrow.Table], depending on the type of user-defined function in
    use.
    """

    metadata: ChunkMetadata
    """The [ChunkMetadata][fused.models.udf.common.ChunkMetadata] describing this chunk."""

    sidecar: Optional[Dict[StrictStr, bytes]] = None

    def _repr_html_(self) -> str:
        data_repr = (
            f"{self.data._repr_html_()}"
            if hasattr(self.data, "_repr_html_")
            else f"{self.data}"
        )
        return f"""
        {data_repr}<br/>
        Metadata: <code>{self.metadata}</code><br/>
        {f'Has sidecar <code>[{", ".join(self.sidecar.keys())}]</code>' if self.sidecar else ''}
        """

    def __repr_args__(self) -> "ReprArgs":
        args = super().__repr_args__()

        def _transform_chunk_repr(
            arg: Tuple[Optional[str], Any]
        ) -> Tuple[Optional[str], Any]:
            if arg[0] == "sidecar" and arg[1] is not None:
                # Wrap the sidecar dict in order to avoid dumping a bunch of bytes as output
                # TODO: It would be nice if this were the type of the field
                return (arg[0], _wrap_sidecar_dict(arg[1]))
            else:
                return arg

        return [_transform_chunk_repr(arg) for arg in args]

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Chunks(RootModel[List[Chunk]]):
    def _repr_html_(self) -> str:
        text = "<ul>"
        for chunk_idx, chunk in enumerate(self):
            text += f"<li><h3>{chunk_idx}</h3>{chunk._repr_html_()}</li>"
        text += "</ul>"
        return text

    @property
    def data(self) -> ChunkData:
        return self.concat_data()

    def concat_data(self, **kwargs) -> ChunkData:
        if len(self.root) == 0:
            # TODO: If this could be a different type -- pa.Table, for example -- that needs
            # to be passed in to Chunks.from_list.
            return pd.DataFrame()

        first = self.root[0].data
        if isinstance(first, pd.DataFrame):
            assert all(isinstance(chunk.data, pd.DataFrame) for chunk in self.root)
            return pd.concat([chunk.data for chunk in self.root], **kwargs)
        else:
            return pa.concat_tables([chunk.data for chunk in self.root], **kwargs)

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)

    @classmethod
    def from_list(cls, chunks: List[Chunk]) -> "Chunks":
        return cls(root=chunks)
