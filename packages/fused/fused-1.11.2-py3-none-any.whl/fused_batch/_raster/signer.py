from typing import Callable, Dict, Optional, Sequence, Union

import geopandas as gpd

from fused_batch.models.api import Dataset


def create_href_mapping(
    stac_gdf: Union[Dataset, gpd.GeoDataFrame],
    signer: Callable[[str], str],
    asset_names: Optional[Sequence[str]] = None,
) -> Dict[str, str]:
    """Create an href mapping given a STAC GeoDataFrame and a lambda signer

    Args:
        stac_gdf: A GeoDataFrame representing STAC Items
        signer: A function applied on each asset href.
        asset_names: The keys in the assets dictionary to sign. Defaults to None, in which case it signs all assets.

    Returns:
        A dict mapping from original asset hrefs to signed asset hrefs.
    """
    if isinstance(stac_gdf, Dataset):
        stac_gdf = stac_gdf.get_dataframe(file_id=None, chunk_id=None)

    assets_series = stac_gdf["assets"]

    # Note: this assumes all assets have the same names
    all_asset_names = set(assets_series[0].keys())

    if asset_names is not None:
        required_asset_names = set(asset_names).intersection(all_asset_names)
    else:
        required_asset_names = all_asset_names

    href_mapping: Dict[str, str] = {}
    for assets in assets_series:
        for required_asset_name in required_asset_names:
            href = assets[required_asset_name]["href"]
            signed_href = signer(href)
            href_mapping[href] = signed_href

    return href_mapping
