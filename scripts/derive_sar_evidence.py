from pathlib import Path

import numpy as np
import rasterio
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
EXTRACTED = ROOT / "data" / "processed" / "extracted_minimal"
OUT = ROOT / "data" / "processed" / "derived_layers"
OUT.mkdir(parents=True, exist_ok=True)


def robust_uint8(array: np.ndarray, low=2, high=98) -> np.ndarray:
    data = array.astype("float32", copy=False)
    valid = np.isfinite(data)
    if not valid.any():
        return np.zeros(data.shape, dtype=np.uint8)
    lo, hi = np.nanpercentile(data[valid], [low, high])
    if hi <= lo:
        hi = lo + 1
    scaled = (data - lo) / (hi - lo)
    return (np.clip(scaled, 0, 1) * 255).astype(np.uint8)


def read(path: Path) -> tuple[np.ndarray, dict]:
    with rasterio.open(path) as src:
        arr = src.read(1).astype("float32")
        profile = src.profile.copy()
    arr[arr <= 0] = np.nan
    return arr, profile


def write_png(name: str, arr: np.ndarray) -> Path:
    path = OUT / f"{name}.png"
    Image.fromarray(robust_uint8(arr)).save(path)
    return path


def write_tif(name: str, arr: np.ndarray, profile: dict) -> Path:
    profile = profile.copy()
    profile.update(dtype="float32", count=1, compress="deflate", nodata=np.nan)
    path = OUT / f"{name}.tif"
    with rasterio.open(path, "w", **profile) as dst:
        dst.write(arr.astype("float32"), 1)
    return path


def main() -> None:
    sri_dir = EXTRACTED / "data" / "calibrated" / "20200913"
    # Prefer S-band product if present, otherwise first matching set.
    prefix = "ch2_sar_ncxs_20200913t042439405_d_sri_xx_fp"
    hh, profile = read(sri_dir / f"{prefix}_hh_d18.tif")
    hv, _ = read(sri_dir / f"{prefix}_hv_d18.tif")
    vh, _ = read(sri_dir / f"{prefix}_vh_d18.tif")
    vv, _ = read(sri_dir / f"{prefix}_vv_d18.tif")

    co_pol_mean = (hh + vv) / 2.0
    cross_pol_mean = (hv + vh) / 2.0
    cross_to_co_ratio = cross_pol_mean / (co_pol_mean + 1e-6)
    hh_vv_ratio = hh / (vv + 1e-6)

    # Transparent prototype score: bright co-pol response plus enhanced cross-pol ratio.
    bright = robust_uint8(co_pol_mean).astype("float32") / 255.0
    cross = robust_uint8(cross_to_co_ratio).astype("float32") / 255.0
    ratio = robust_uint8(hh_vv_ratio).astype("float32") / 255.0
    candidate_score = (0.50 * bright + 0.35 * cross + 0.15 * ratio) * 100.0

    products = {
        "sar_co_pol_mean": co_pol_mean,
        "sar_cross_pol_mean": cross_pol_mean,
        "sar_cross_to_co_ratio": cross_to_co_ratio,
        "sar_hh_vv_ratio": hh_vv_ratio,
        "sar_candidate_ice_evidence_score": candidate_score,
    }
    for name, arr in products.items():
        print(write_tif(name, arr, profile))
        print(write_png(name, arr))

    summary = {
        "crs": str(profile.get("crs")),
        "width": profile["width"],
        "height": profile["height"],
        "transform": tuple(profile["transform"])[:6],
        "note": "Prototype evidence score only. It highlights radar-bright and cross-pol-enhanced pixels; it is not confirmed ice.",
    }
    (OUT / "sar_evidence_summary.json").write_text(str(summary), encoding="utf-8")
    print(OUT / "sar_evidence_summary.json")


if __name__ == "__main__":
    main()
