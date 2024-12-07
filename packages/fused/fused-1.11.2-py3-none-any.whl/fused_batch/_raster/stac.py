from __future__ import annotations

import warnings
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from itertools import zip_longest
from typing import TYPE_CHECKING, Dict, Generator, Iterable, List, Optional, Sequence

import geopandas as gpd

from fused_batch._options import options as OPTIONS

if TYPE_CHECKING:
    from pystac import Item


__all__ = ("stac_from_tiff_list", "stac_from_stac_list")


@dataclass
class IterInput:
    tiff_url: str
    id: Optional[str]
    input_datetime: Optional[datetime]


def stac_from_tiff_list(
    tiff_list: Sequence[str],
    *,
    input_datetime: Optional[Iterable[datetime]] = None,
    id: Optional[Iterable[str]] = None,
    collection: Optional[str] = None,
    asset_name: str = "asset",
    naive: bool = False,
    max_workers: Optional[int] = None,
) -> gpd.GeoDataFrame:
    """Construct a STAC GeoDataFrame from a list of GeoTIFF urls.

    Args:
        tiff_list: input paths.

    Keyword Args:
        input_datetime: datetime associated with the item. Defaults to None.
        id: id to assign to the item (default to the source basename). Defaults to None.
        collection: name of collection the item belongs to. Defaults to None.
        asset_name: asset name in the Assets object. Defaults to "asset".
        naive: When True, this function will only read geometry information for the _first_ item in the list and copy geometry information to the others. Defaults to False.

    Returns:
        a GeoDataFrame with containing the description of STAC items
    """
    from rio_stac import create_stac_item

    iterator = _iter_input(tiff_list, input_datetime=input_datetime, id=id)
    first_item = next(iterator)

    first_stac = create_stac_item(
        first_item.tiff_url,
        id=first_item.id,
        input_datetime=first_item.input_datetime,
        collection=collection,
        asset_name=asset_name,
        with_proj=True,
        with_eo=True,
    )

    if naive:
        return _infer_stac_naive(
            first_item=first_stac, iterator=iterator, asset_name=asset_name
        )

    stac_list: List[Dict] = [first_stac.to_dict()]

    def _mapper(_input_item: IterInput) -> Dict:
        return create_stac_item(
            _input_item.tiff_url,
            id=_input_item.id,
            input_datetime=_input_item.input_datetime,
            collection=collection,
            asset_name=asset_name,
            with_proj=True,
            with_eo=True,
        ).to_dict()

    max_workers = max_workers if max_workers is not None else OPTIONS.max_workers
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        stac_list.extend(pool.map(_mapper, iterator))

    return stac_from_stac_list(stac_list)


def _infer_stac_naive(
    first_item: Item, iterator: Generator[IterInput, None, None], asset_name: str
) -> gpd.GeoDataFrame:
    warnings.warn(
        "Using naive STAC generation, copying geometries from first GeoTIFF in the list."
    )

    stac_list: List[Dict] = [first_item.to_dict()]

    for _input in iterator:
        new_item = first_item.clone()
        new_item.id = _input.id or _input.tiff_url.rsplit("/")[-1]
        new_item.assets[asset_name].href = _input.tiff_url
        if _input.input_datetime:
            new_item.datetime = _input.input_datetime

        stac_list.append(new_item.to_dict())

    return stac_from_stac_list(stac_list)


def _iter_input(
    tiff_list: List[str],
    *,
    input_datetime: Optional[Iterable[datetime]] = None,
    id: Optional[Iterable[str]] = None,
) -> Generator[IterInput, None, None]:
    # Use itertools.zip_longest
    for tiff_url, _input_datetime, _id in zip_longest(
        tiff_list, input_datetime or [], id or []
    ):
        yield IterInput(tiff_url=tiff_url, id=_id, input_datetime=_input_datetime)


def stac_from_stac_list(stac_list: Sequence[Dict]) -> gpd.GeoDataFrame:
    """Construct a STAC GeoDataFrame from a list of STAC Items.

    Args:
        stac_list: input STAC Items.

    Returns:
        a GeoDataFrame with containing the description of STAC items
    """
    import stac_geoparquet

    return stac_geoparquet.to_geodataframe(stac_list)
