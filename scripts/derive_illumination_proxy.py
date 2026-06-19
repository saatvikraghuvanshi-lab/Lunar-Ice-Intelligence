from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import rasterio
from affine import Affine
from PIL import Image
from rasterio.enums import Resampling


ROOT = Path(__file__).resolve().parents[1]
DTM = (
    ROOT
    / "data"
    / "processed"
    / "extracted_tmc2_south_pole"
    / "data"
    / "derived"
    / "20231203"
    / "ch2_tmc_ndn_20231203T0019079527_d_dtm_d18.tif"
)
OUT = ROOT / "data" / "processed" / "derived_layers"
OUT.mkdir(parents=True, exist_ok=True)


def robust_uint8(array: np.ndarray, low: float = 2, high: float = 98) -> np.ndarray:
    valid = np.isfinite(array)
    if not valid.any():
        return np.zeros(array.shape, dtype=np.uint8)
    lo, hi = np.nanpercentile(array[valid], [low, high])
    if hi <= lo:
        hi = lo + 1
    scaled = np.clip((array - lo) / (hi - lo), 0, 1)
    scaled[~valid] = 0
    return (scaled * 255).astype(np.uint8)


def colorize_score(arr: np.ndarray, invert: bool = False) -> Image.Image:
    v = arr.astype("float32")
    if invert:
        v = 100 - v
    g = np.clip(v / 100, 0, 1)
    stops = np.array(
        [
            [29, 39, 65],
            [42, 92, 105],
            [80, 151, 115],
            [219, 187, 90],
            [246, 238, 183],
        ],
        dtype=np.float32,
    )
    scaled = g * (len(stops) - 1)
    idx = np.floor(scaled).astype(np.int16)
    idx = np.clip(idx, 0, len(stops) - 2)
    frac = scaled - idx
    rgb = stops[idx] * (1 - frac[..., None]) + stops[idx + 1] * frac[..., None]
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")


def write_tif(name: str, arr: np.ndarray, profile: dict, transform: Affine) -> Path:
    path = OUT / f"{name}.tif"
    profile = profile.copy()
    profile.update(
        width=arr.shape[1],
        height=arr.shape[0],
        transform=transform,
        dtype="float32",
        count=1,
        compress="deflate",
        nodata=np.nan,
    )
    with rasterio.open(path, "w", **profile) as dst:
        dst.write(arr.astype("float32"), 1)
    return path


def hillshade(elevation: np.ndarray, pixel_size_m: float, azimuth_deg: float, altitude_deg: float) -> np.ndarray:
    dy, dx = np.gradient(elevation, pixel_size_m, pixel_size_m)
    slope = np.arctan(np.sqrt(dx * dx + dy * dy))
    aspect = np.arctan2(-dx, dy)
    az = math.radians(azimuth_deg)
    alt = math.radians(altitude_deg)
    shade = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect)
    return np.clip(shade, 0, 1)


def main() -> None:
    with rasterio.open(DTM) as src:
        scale = max(src.width / 4096, src.height / 4096, 1)
        out_w = int(src.width / scale)
        out_h = int(src.height / scale)
        elevation = src.read(1, out_shape=(out_h, out_w), resampling=Resampling.bilinear).astype("float32")
        profile = src.profile.copy()
        transform = src.transform * Affine.scale(src.width / out_w, src.height / out_h)
        pixel_size_m = abs(transform.a)

    elevation[elevation <= -32000] = np.nan
    filled = elevation.copy()
    filled[~np.isfinite(filled)] = np.nanmedian(filled)

    # Near-polar sun elevations are low; multiple azimuths approximate seasonal/diurnal grazing illumination.
    azimuths = [0, 45, 90, 135, 180, 225, 270, 315]
    shades = np.stack([hillshade(filled, pixel_size_m, az, 1.5) for az in azimuths], axis=0)
    illumination = np.nanmean(shades, axis=0) * 100.0
    shadow_persistence = (1.0 - np.nanmax(shades, axis=0)) * 100.0
    cold_trap_proxy = np.clip(0.65 * shadow_persistence + 0.35 * (100 - illumination), 0, 100)

    mask = np.isfinite(elevation)
    for arr in (illumination, shadow_persistence, cold_trap_proxy):
        arr[~mask] = np.nan

    outputs = {
        "illumination_availability_proxy": illumination,
        "shadow_persistence_proxy": shadow_persistence,
        "cold_trap_proxy": cold_trap_proxy,
    }
    products = {}
    for name, arr in outputs.items():
        png = OUT / f"{name}.png"
        if name == "illumination_availability_proxy":
            colorize_score(arr).save(png)
        else:
            colorize_score(arr, invert=False).save(png)
        tif = write_tif(name, arr, profile, transform)
        products[name] = {"png": str(png.relative_to(ROOT)), "tif": str(tif.relative_to(ROOT))}

    summary = {
        "source": str(DTM.relative_to(ROOT)),
        "method": "Prototype low-sun hillshade proxy using eight azimuths at 1.5 degree solar altitude.",
        "products": products,
        "note": "This is an illumination/shadow proxy for hackathon screening, not a substitute for validated ephemeris-based PSR products.",
    }
    (OUT / "illumination_proxy_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
