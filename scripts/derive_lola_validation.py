from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image, ImageDraw, ImageFont
from rasterio.enums import Resampling
from rasterio.windows import from_bounds


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "external" / "nasa_lola_pgda"
DERIVED = ROOT / "data" / "processed" / "derived_layers"
DEMO = ROOT / "data" / "processed" / "demo_assets"
DERIVED.mkdir(parents=True, exist_ok=True)
DEMO.mkdir(parents=True, exist_ok=True)

TMC_SUMMARY = DERIVED / "tmc2_south_pole_summary.json"
TMC_SLOPE = DERIVED / "tmc2_south_pole_slope_deg.tif"
LOLA_SLOPE = RAW / "LDRM_80S_1000MPP_ADJ_SLP_100M.TIF"
LOLA_ROUGH = RAW / "LDRM_80S_1000MPP_ADJ_AVGROUGH.TIF"
LOLA_CLASS = RAW / "LDRM_80S_1000MPP_ADJ_CLASS.TIF"


def robust_uint8(arr: np.ndarray, low: float = 2, high: float = 98) -> np.ndarray:
    valid = np.isfinite(arr)
    if not valid.any():
        return np.zeros(arr.shape, dtype=np.uint8)
    lo, hi = np.nanpercentile(arr[valid], [low, high])
    if hi <= lo:
        hi = lo + 1
    scaled = np.clip((arr - lo) / (hi - lo), 0, 1)
    scaled[~valid] = 0
    return (scaled * 255).astype(np.uint8)


def colorize(gray: np.ndarray, palette: str) -> Image.Image:
    g = gray.astype("float32") / 255.0
    palettes = {
        "slope": np.array([[30, 56, 78], [52, 138, 125], [222, 190, 88], [225, 90, 69]], dtype=np.float32),
        "rough": np.array([[22, 42, 68], [48, 111, 117], [118, 164, 107], [233, 220, 147]], dtype=np.float32),
        "class": np.array([[16, 24, 32], [49, 214, 204], [242, 191, 90], [243, 108, 97]], dtype=np.float32),
    }
    stops = palettes[palette]
    scaled = g * (len(stops) - 1)
    idx = np.clip(np.floor(scaled).astype(np.int16), 0, len(stops) - 2)
    frac = scaled - idx
    rgb = stops[idx] * (1 - frac[..., None]) + stops[idx + 1] * frac[..., None]
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")


def crop_lola(path: Path, bounds: tuple[float, float, float, float], name: str, palette: str) -> tuple[np.ndarray, Path]:
    with rasterio.open(path) as src:
        window = from_bounds(*bounds, transform=src.transform).round_offsets().round_lengths()
        window = window.intersection(rasterio.windows.Window(0, 0, src.width, src.height))
        arr = src.read(1, window=window, boundless=False).astype("float32")
        profile = src.profile.copy()
        transform = src.window_transform(window)
        profile.update(width=arr.shape[1], height=arr.shape[0], transform=transform, compress="deflate")
        out_tif = DERIVED / f"{name}.tif"
        with rasterio.open(out_tif, "w", **profile) as dst:
            dst.write(arr, 1)
    png = DERIVED / f"{name}.png"
    colorize(robust_uint8(arr), palette).save(png)
    return arr, png


def make_focus_asset(lola_slope_png: Path, lola_rough_png: Path, lola_class_png: Path, summary: dict) -> Path:
    canvas = Image.new("RGB", (1440, 960), (3, 6, 10))
    draw = ImageDraw.Draw(canvas)
    try:
        title_font = ImageFont.truetype("arial.ttf", 30)
        label_font = ImageFont.truetype("arial.ttf", 20)
        small_font = ImageFont.truetype("arial.ttf", 15)
    except OSError:
        title_font = label_font = small_font = ImageFont.load_default()

    draw.text((42, 34), "NASA LOLA External Validation", fill=(235, 245, 247), font=title_font)
    draw.text((42, 72), "Independent LRO/LOLA south-pole products cropped to the Chandrayaan-2 TMC-2 AOI", fill=(139, 216, 209), font=small_font)

    panels = [
        ("LOLA slope", lola_slope_png, (42, 124, 462, 604)),
        ("LOLA roughness", lola_rough_png, (510, 124, 930, 604)),
        ("LOLA class", lola_class_png, (978, 124, 1398, 604)),
    ]
    for label, path, box in panels:
        x0, y0, x1, y1 = box
        draw.rectangle((x0 - 1, y0 - 1, x1 + 1, y1 + 1), outline=(58, 88, 98), width=2)
        img = Image.open(path).convert("RGB")
        img = img.resize((x1 - x0, y1 - y0), Image.Resampling.NEAREST)
        canvas.paste(img, (x0, y0))
        draw.text((x0, y1 + 14), label, fill=(232, 240, 242), font=label_font)

    stats_box = (42, 700, 1398, 890)
    draw.rectangle(stats_box, outline=(58, 88, 98), width=2)
    lines = [
        f"AOI crop: {summary['crop_shape'][1]} x {summary['crop_shape'][0]} LOLA pixels at 1000 m/pixel",
        f"TMC slope mean: {summary['tmc_slope_mean_deg']:.2f} deg | LOLA slope mean: {summary['lola_slope_mean_deg']:.2f} deg",
        f"Slope agreement class: {summary['agreement_label']}",
        "Interpretation: LOLA is coarser than TMC-2, so agreement is used as external terrain sanity check, not pixel-perfect validation.",
    ]
    y = 722
    for line in lines:
        draw.text((64, y), line, fill=(218, 232, 235), font=label_font if y == 722 else small_font)
        y += 38

    output = DEMO / "lola_validation_focus.png"
    canvas.save(output, quality=95)
    return output


def main() -> None:
    tmc_summary = json.loads(TMC_SUMMARY.read_text(encoding="utf-8"))
    bounds = tuple(tmc_summary["source_bounds_m"])

    lola_slope, slope_png = crop_lola(LOLA_SLOPE, bounds, "lola_tmc_aoi_slope_1000m", "slope")
    lola_rough, rough_png = crop_lola(LOLA_ROUGH, bounds, "lola_tmc_aoi_roughness_1000m", "rough")
    lola_class, class_png = crop_lola(LOLA_CLASS, bounds, "lola_tmc_aoi_class_1000m", "class")

    with rasterio.open(TMC_SLOPE) as src:
        tmc = src.read(
            1,
            out_shape=(lola_slope.shape[0], lola_slope.shape[1]),
            resampling=Resampling.average,
        ).astype("float32")

    valid = np.isfinite(tmc) & np.isfinite(lola_slope)
    tmc_mean = float(np.nanmean(tmc[valid])) if valid.any() else float("nan")
    lola_mean = float(np.nanmean(lola_slope[valid])) if valid.any() else float("nan")
    diff = abs(tmc_mean - lola_mean)
    if diff <= 5:
        agreement = "strong sanity check"
    elif diff <= 12:
        agreement = "moderate sanity check"
    else:
        agreement = "needs review"

    summary = {
        "source": "NASA PGDA / LRO LOLA south-pole products",
        "source_url": "https://pgda.gsfc.nasa.gov/products/90",
        "aoi_bounds_m": bounds,
        "crop_shape": list(lola_slope.shape),
        "tmc_slope_mean_deg": tmc_mean,
        "lola_slope_mean_deg": lola_mean,
        "mean_slope_difference_deg": diff,
        "agreement_label": agreement,
        "outputs": {
            "lola_slope_png": str(slope_png.relative_to(ROOT)),
            "lola_roughness_png": str(rough_png.relative_to(ROOT)),
            "lola_class_png": str(class_png.relative_to(ROOT)),
            "focus_asset": str((DEMO / "lola_validation_focus.png").relative_to(ROOT)),
        },
        "notes": [
            "LOLA products are 1000 m/pixel, much coarser than the TMC-2 DTM-derived layers.",
            "This validates regional terrain behavior, not exact meter-scale hazards.",
        ],
    }
    focus = make_focus_asset(slope_png, rough_png, class_png, summary)
    summary["outputs"]["focus_asset"] = str(focus.relative_to(ROOT))
    out_json = DERIVED / "lola_external_validation_summary.json"
    out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
