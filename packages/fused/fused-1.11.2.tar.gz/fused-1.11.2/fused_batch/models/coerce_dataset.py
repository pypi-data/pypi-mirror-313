from typing import Optional, Union

from .api.dataset import Dataset, Table
from .internal.dataset import (
    AnyDatasetInput,
    AnyDatasetOutput,
    DatasetInput,
    DatasetInputBase,
    DatasetInputV2,
    DatasetOutputBase,
    DatasetOutputV2,
)
from .urls import DatasetUrl

CoerceableToDatasetInput = Union[str, AnyDatasetInput, Dataset, Table, DatasetUrl]

CoerceableToDatasetOutput = Union[str, AnyDatasetOutput]

CoerceableToDataset = Union[str, DatasetInput, Dataset, DatasetUrl]


def _object_to_dataset_input(
    dataset: CoerceableToDatasetInput, *, allow_none: bool = False
) -> Optional[AnyDatasetInput]:
    if isinstance(dataset, Dataset):
        return DatasetInput(base_path=dataset.base_path)
    elif isinstance(dataset, Table):
        input = DatasetInputV2.from_table_url(url=dataset.url)
        input._project_url = (
            dataset._project_url if hasattr(dataset, "_project_url") else None
        )
        return input
    elif isinstance(dataset, str):
        return DatasetInputV2.from_table_url(url=dataset)
    elif isinstance(dataset, DatasetInputBase):
        return dataset
    else:
        if allow_none:
            return None
        assert False, f"Unknown type for dataset input: {type(dataset)}"


def _object_to_dataset_output(
    dataset: Optional[CoerceableToDatasetOutput],
) -> AnyDatasetOutput:
    if dataset is None:
        return DatasetOutputV2()
    elif isinstance(dataset, str):
        return DatasetOutputV2(url=dataset)
    elif isinstance(dataset, DatasetOutputBase):
        return dataset
    else:
        assert False, f"Unknown type for dataset output: {type(dataset)}"
