import numpy as np
from rasterio.features import rasterize


def resample_bands(data, resolution=20):
    return {
        name: da.rio.reproject(da.rio.crs, resolution=resolution, resampling="average")
        for name, da in data.items()
    }


def build_feature_stack(bands_20m):
    red = bands_20m["red"].values.astype(float)
    nir = bands_20m["nir"].values.astype(float)
    with np.errstate(divide="ignore", invalid="ignore"):
        ndvi = (nir - red) / (nir + red)
    return np.stack([
        bands_20m["blue"].values.astype(float),
        bands_20m["green"].values.astype(float),
        red,
        nir,
        ndvi,
    ], axis=0)


def rasterize_gmw(gmw_gdf, ref_band):
    gmw = gmw_gdf.to_crs(ref_band.rio.crs)
    return rasterize(
        shapes=((geom, 1) for geom in gmw.geometry),
        out_shape=(ref_band.shape[-2], ref_band.shape[-1]),
        transform=ref_band.rio.transform(),
        fill=0,
        dtype="uint8",
    )


def draw_balanced_sample(stack, label_mask, n_per_class=50_000, seed=42):
    X = stack.reshape(stack.shape[0], -1).T
    y = label_mask.reshape(-1)
    valid = ~np.isnan(X).any(axis=1)
    X, y = X[valid], y[valid]
    rng = np.random.default_rng(seed)
    idx = np.concatenate([
        rng.choice(np.where(y == 0)[0], n_per_class, replace=False),
        rng.choice(np.where(y == 1)[0], n_per_class, replace=False),
    ])
    return X[idx], y[idx]
