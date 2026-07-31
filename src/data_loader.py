import pystac_client
import planetary_computer
import rioxarray
import geopandas as gpd
import pandas as pd
from shapely.geometry import shape


def search_sentinel2(bbox, datetime_str, cloud_cover_lt=10):
    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace,
    )
    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime=datetime_str,
        query={"eo:cloud_cover": {"lt": cloud_cover_lt}},
    )
    return list(search.items())


def rank_by_gmw_overlap(items, gmw_union):
    rows = []
    for item in items:
        footprint = shape(item.geometry)
        rows.append({
            "id": item.id,
            "tile": item.properties.get("s2:mgrs_tile"),
            "cloud_cover": item.properties["eo:cloud_cover"],
            "overlap_deg2": footprint.intersection(gmw_union).area,
        })
    return pd.DataFrame(rows).sort_values("overlap_deg2", ascending=False).reset_index(drop=True)


def load_sentinel2_bands(item, bbox, bands):
    data = {}
    for band_id, name in bands.items():
        da = rioxarray.open_rasterio(item.assets[band_id].href)
        data[name] = da.rio.clip_box(*bbox, crs="EPSG:4326").squeeze()
    return data
