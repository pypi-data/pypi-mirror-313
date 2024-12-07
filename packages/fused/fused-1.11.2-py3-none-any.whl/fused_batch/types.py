from typing import TypeVar

import geopandas as gpd
import mercantile
import shapely

TileXYZ = TypeVar("TileXYZ", bound=mercantile.Tile)
TileGDF = TypeVar("TileGDF", bound=gpd.GeoDataFrame)
Bbox = TypeVar("Bbox", bound=shapely.geometry.polygon.Polygon)
