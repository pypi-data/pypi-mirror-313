from typing import Any, List, Tuple

from pydantic import BaseModel, ConfigDict

from .udf.common import Chunk, ChunkData, Chunks


class BaseInput(BaseModel):
    """A base class for inputs into a UDF"""

    step_config: "AnyJobStepConfig"
    """The currently executing [`step configuration`][fused.models.api.job.AnyJobStepConfig]"""

    def as_udf_args(self) -> List[Any]:
        raise NotImplementedError()


class JoinInput(BaseInput):
    left: Chunk
    """The [`chunk`][fused.models.udf.common.Chunk] containing data used as the left side of the join.
    """

    right: Chunks
    """A list of [`chunk`][fused.models.udf.common.Chunk] objects containing data used as the right side of the join.

    Only chunks whose bounding box intersects with the left chunk will be included.
    """

    def _repr_html_(self) -> str:
        return f"""
        <h2>Left</h2>
        {self.left._repr_html_()}<br/>
        <h2>Right</h2>
        {self.right._repr_html_()}
        """

    @property
    def data(self) -> Tuple[ChunkData, ChunkData]:
        """Returns the left and right data"""
        return self.left.data, self.right.concat_data()

    def as_udf_args(self) -> List[Any]:
        return [self.left.model_copy(deep=True), self.right.model_copy(deep=True)]


class JoinSingleFileInput(BaseInput):
    left: Chunk
    """The [`chunk`][fused.models.udf.common.Chunk] containing data used as the left side of the join.
    """

    right: ChunkData
    """The data used as the right side of the join.

    This will either be a [`pandas.DataFrame`][pandas.DataFrame],
    [`geopandas.GeoDataFrame`][geopandas.GeoDataFrame], or
    [`pyarrow.Table`][pyarrow.Table], depending on the type of user-defined function in
    use.
    """

    def _repr_html_(self) -> str:
        right_html = (
            f"{self.right._repr_html_()}"
            if hasattr(self.right, "_repr_html_")
            else f"{self.right}"
        )
        return f"""
        <h2>Left</h2>
        {self.left._repr_html_()}<br/>
        <h2>Right</h2>
        {right_html}
        """

    @property
    def data(self) -> Tuple[ChunkData, ChunkData]:
        """Returns the left and right data"""
        return self.left.data, self.right

    def as_udf_args(self) -> List[Any]:
        copy = self.model_copy(deep=True)
        return [copy.left, copy.right]

    model_config = ConfigDict(arbitrary_types_allowed=True)


class MapInput(BaseInput, Chunk):
    """The [`chunk`][fused.models.udf.common.Chunk] containing data used for the map operation."""

    def as_udf_args(self) -> List[Any]:
        return [self.model_copy(deep=True)]


# Workaround for a circular model reference
from .api import AnyJobStepConfig  # noqa: E402

# The job step configs return samples (the input classes below), but the input
# classes contain copies of the job step configs! This requires using a ForwardRef
# which is then resolved afterwards. This is the resolution step, so that Pydantic
# will correctly validate the type of `step_config`, above. It must be done on each
# class individually because each class has its own field information.
BaseInput.model_rebuild()
MapInput.model_rebuild()
JoinInput.model_rebuild()
JoinSingleFileInput.model_rebuild()
