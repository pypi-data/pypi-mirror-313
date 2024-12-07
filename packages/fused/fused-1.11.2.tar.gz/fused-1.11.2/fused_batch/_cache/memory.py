from typing import Any, Callable, Dict, Optional, Tuple, TypeVar, Union

from pydantic import BaseModel

from fused_batch._options import options as OPTIONS

SAMPLE_KEY_FIELDS = frozenset(("input", "input_left", "input_right", "buffer_distance"))
_sample_cache: Dict[Tuple[str, Optional[str], Optional[int], Optional[int]], Any] = {}

SampleType = TypeVar("SampleType")


def size() -> int:
    return len(_sample_cache)


def clear() -> None:
    """Clear the cache contents"""
    _sample_cache.clear()


def get_or_cache_sample(
    job_config: BaseModel,
    sample_coords: Tuple[Union[str, int, None], Optional[int], Optional[int]],
    generator: Callable[[], SampleType],
) -> SampleType:
    if not OPTIONS.cache.enable:
        return generator()

    job_json = job_config.json(include=SAMPLE_KEY_FIELDS)

    if sample_coords is not None:
        # Ensure the file ID is a string
        file_id = (
            str(sample_coords[0]) if sample_coords[0] is not None else sample_coords[0]
        )
        key = (job_json, file_id, sample_coords[1], sample_coords[2])
    else:
        key = (job_json, None, None, None)

    if key in _sample_cache:
        return _sample_cache[key]
    else:
        sample = generator()
        # TODO: Support a maximum size of the cache
        # TODO: Support an on disk cache instead of in memory
        _sample_cache[key] = sample
        return sample
