from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
EXTRACTED = ROOT / "data" / "processed" / "extracted_minimal"
OUT = ROOT / "data" / "processed" / "quicklooks"
OUT.mkdir(parents=True, exist_ok=True)

Image.MAX_IMAGE_PIXELS = None


def robust_uint8(arr: np.ndarray) -> np.ndarray:
    arr = np.asarray(arr)
    arr = arr.astype("float32", copy=False)
    valid = np.isfinite(arr)
    if not valid.any():
        return np.zeros(arr.shape, dtype=np.uint8)
    lo, hi = np.nanpercentile(arr[valid], [2, 98])
    if hi <= lo:
        hi = lo + 1
    scaled = (arr - lo) / (hi - lo)
    return (np.clip(scaled, 0, 1) * 255).astype(np.uint8)


def save_quicklook(path: Path, max_width=1200, max_height=2200) -> Path:
    with Image.open(path) as im:
        im.draft(im.mode, (max_width, max_height))
        thumb = im.copy()
    thumb.thumbnail((max_width, max_height), Image.Resampling.BILINEAR)
    arr = np.array(thumb)
    if arr.dtype != np.uint8 or arr.ndim == 2:
        arr = robust_uint8(arr)
    out = OUT / (path.stem + "_quicklook.png")
    Image.fromarray(arr).save(out)
    return out


def make_dtm_slope_preview(dtm_preview_path: Path) -> tuple[Path, Path]:
    with Image.open(dtm_preview_path) as im:
        small = im.convert("F")
    dtm = np.array(small).astype("float32")
    dtm[~np.isfinite(dtm)] = np.nan
    dzdy, dzdx = np.gradient(dtm)
    slope = np.sqrt(dzdx * dzdx + dzdy * dzdy)
    relief_png = OUT / "tmc2_dtm_relief_quicklook.png"
    slope_png = OUT / "tmc2_dtm_slope_proxy_quicklook.png"
    Image.fromarray(robust_uint8(dtm)).save(relief_png)
    Image.fromarray(robust_uint8(slope)).save(slope_png)
    return relief_png, slope_png


def main() -> None:
    products = {
        "tmc2_dtm": next(EXTRACTED.rglob("*_d_dtm_d18.tif")),
        "tmc2_ortho": next(EXTRACTED.rglob("*_d_oth_d18.tif")),
    }
    sar_browse = sorted(EXTRACTED.rglob("ch2_sar*_b_brw*.png"))
    ohr_browse = sorted(EXTRACTED.rglob("ch2_ohr*_b_brw_d18.png"))
    tmc_browse = sorted(EXTRACTED.rglob("ch2_tmc*_b_b*t_d18.png"))

    outputs = []
    for path in tmc_browse:
        outputs.append(("tmc2_browse", save_quicklook(path)))
    for path in sar_browse:
        outputs.append(("sar_browse", save_quicklook(path)))
    for path in ohr_browse:
        outputs.append(("ohr_browse", save_quicklook(path)))

    dtm_preview = next(EXTRACTED.rglob("*_b_bdt_d18.png"))
    relief, slope = make_dtm_slope_preview(dtm_preview)
    outputs.extend([("tmc2_relief", relief), ("tmc2_slope_proxy", slope)])

    for label, path in outputs:
        print(f"{label}: {path}")


if __name__ == "__main__":
    main()
