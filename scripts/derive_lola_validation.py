from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image, ImageDraw, ImageFont
from rasterio.enums import Resampling
from rasterio.windows import from_bounds


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "external" / "lola"
DERIVED = ROOT / "data" / "processed" / "derived_layers"
DEMO = ROOT / "data" / "processed" / "demo_assets"
DERIVED.mkdir(parents=True, exist_ok=True)
DEMO.mkdir(parents=True, exist_ok=True)

TMC_SUMMARY = DERIVED / "tmc2_south_pole_summary.json"
TMC_SLOPE = DERIVED / "tmc2_south_pole_slope_deg.tif"
LOLA_DEM = RAW / "ldem_85s_20m_float.lbl"


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
        "elevation": np.array([[16, 24, 32], [43, 94, 120], [96, 150, 130], [231, 221, 158]], dtype=np.float32),
        "slope": np.array([[30, 56, 78], [52, 138, 125], [222, 190, 88], [225, 90, 69]], dtype=np.float32),
        "rough": np.array([[22, 42, 68], [48, 111, 117], [118, 164, 107], [233, 220, 147]], dtype=np.float32),
    }
    stops = palettes[palette]
    scaled = g * (len(stops) - 1)
    idx = np.clip(np.floor(scaled).astype(np.int16), 0, len(stops) - 2)
    frac = scaled - idx
    rgb = stops[idx] * (1 - frac[..., None]) + stops[idx + 1] * frac[..., None]
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")


def save_png(arr: np.ndarray, name: str, palette: str) -> Path:
    path = DERIVED / f"{name}.png"
    colorize(robust_uint8(arr), palette).save(path)
    return path


def local_roughness(arr: np.ndarray) -> np.ndarray:
    valid = np.isfinite(arr)
    filled = np.where(valid, arr, np.nanmedian(arr[valid]) if valid.any() else 0)
    neighbors = [
        filled,
        np.roll(filled, 1, axis=0),
        np.roll(filled, -1, axis=0),
        np.roll(filled, 1, axis=1),
        np.roll(filled, -1, axis=1),
    ]
    stack = np.stack(neighbors, axis=0)
    rough = np.nanstd(stack, axis=0)
    rough[~valid] = np.nan
    return rough.astype("float32")


def crop_lola_dem(bounds: tuple[float, float, float, float]) -> tuple[np.ndarray, rasterio.Affine, dict]:
    with rasterio.open(LOLA_DEM) as src:
        window = from_bounds(*bounds, transform=src.transform).round_offsets().round_lengths()
        window = window.intersection(rasterio.windows.Window(0, 0, src.width, src.height))
        max_dim = 1800
        scale = max(1, int(np.ceil(max(window.width, window.height) / max_dim)))
        out_height = max(1, int(window.height // scale))
        out_width = max(1, int(window.width // scale))
        dem_km = src.read(
            1,
            window=window,
            out_shape=(out_height, out_width),
            resampling=Resampling.average,
        ).astype("float32")
        transform = src.window_transform(window) * rasterio.Affine.scale(
            window.width / out_width,
            window.height / out_height,
        )
        profile = src.profile.copy()
        profile.update(
            driver="GTiff",
            width=out_width,
            height=out_height,
            transform=transform,
            dtype="float32",
            compress="deflate",
        )

    dem_m = dem_km * 1000.0
    out_tif = DERIVED / "lola_85s20m_tmc_overlap_elevation_m.tif"
    with rasterio.open(out_tif, "w", **profile) as dst:
        dst.write(dem_m.astype("float32"), 1)
    return dem_m, transform, {"window_scale": scale, "effective_pixel_size_m": abs(transform.a)}


def slope_degrees(dem_m: np.ndarray, pixel_size_m: float) -> np.ndarray:
    gy, gx = np.gradient(dem_m, pixel_size_m, pixel_size_m)
    slope = np.degrees(np.arctan(np.sqrt(gx * gx + gy * gy))).astype("float32")
    slope[~np.isfinite(dem_m)] = np.nan
    return slope


def read_tmc_slope(bounds: tuple[float, float, float, float], shape: tuple[int, int]) -> np.ndarray:
    with rasterio.open(TMC_SLOPE) as src:
        window = from_bounds(*bounds, transform=src.transform).round_offsets().round_lengths()
        window = window.intersection(rasterio.windows.Window(0, 0, src.width, src.height))
        return src.read(1, window=window, out_shape=shape, resampling=Resampling.average).astype("float32")


def make_focus_asset(elev_png: Path, slope_png: Path, rough_png: Path, summary: dict) -> Path:
    canvas = Image.new("RGB", (1440, 960), (3, 6, 10))
    draw = ImageDraw.Draw(canvas)
    try:
        title_font = ImageFont.truetype("arial.ttf", 32)
        label_font = ImageFont.truetype("arial.ttf", 21)
        small_font = ImageFont.truetype("arial.ttf", 16)
    except OSError:
        title_font = label_font = small_font = ImageFont.load_default()

    draw.text((42, 34), "NASA LOLA 20 m External Validation", fill=(235, 245, 247), font=title_font)
    draw.text(
        (42, 76),
        "PDS LDEM_85S_20M polar DEM cropped to Chandrayaan-2 TMC-2 overlap",
        fill=(139, 216, 209),
        font=small_font,
    )

    panels = [
        ("LOLA elevation", elev_png, (42, 126, 462, 604)),
        ("LOLA-derived slope", slope_png, (510, 126, 930, 604)),
        ("LOLA local roughness", rough_png, (978, 126, 1398, 604)),
    ]
    for label, path, box in panels:
        x0, y0, x1, y1 = box
        draw.rectangle((x0 - 1, y0 - 1, x1 + 1, y1 + 1), outline=(58, 88, 98), width=2)
        img = Image.open(path).convert("RGB")
        img.thumbnail((x1 - x0, y1 - y0), Image.Resampling.NEAREST)
        px = x0 + ((x1 - x0) - img.width) // 2
        py = y0 + ((y1 - y0) - img.height) // 2
        canvas.paste(img, (px, py))
        draw.text((x0, y1 + 14), label, fill=(232, 240, 242), font=label_font)

    stats_box = (42, 700, 1398, 890)
    draw.rectangle(stats_box, outline=(58, 88, 98), width=2)
    lines = [
        f"Source product: {summary['source_product']} | source map scale: 20 m/pixel",
        f"Processed overlap: {summary['crop_shape'][1]} x {summary['crop_shape'][0]} px at ~{summary['effective_pixel_size_m']:.0f} m/pixel quicklook scale",
        f"TMC slope mean: {summary['tmc_slope_mean_deg']:.2f} deg | LOLA-derived slope mean: {summary['lola_slope_mean_deg']:.2f} deg",
        f"Slope agreement class: {summary['agreement_label']}",
        "Interpretation: independent topography validation for terrain behavior, not final meter-scale landing certification.",
    ]
    y = 722
    for index, line in enumerate(lines):
        draw.text((64, y), line, fill=(218, 232, 235), font=label_font if index == 0 else small_font)
        y += 34

    output = DEMO / "lola_validation_focus.png"
    canvas.save(output, quality=95)
    return output


def main() -> None:
    tmc_summary = json.loads(TMC_SUMMARY.read_text(encoding="utf-8"))
    tmc_bounds = tuple(tmc_summary["source_bounds_m"])

    dem_m, transform, processing = crop_lola_dem(tmc_bounds)
    lola_bounds = rasterio.transform.array_bounds(dem_m.shape[0], dem_m.shape[1], transform)
    lola_slope = slope_degrees(dem_m, processing["effective_pixel_size_m"])
    lola_rough = local_roughness(dem_m)
    tmc = read_tmc_slope(tuple(lola_bounds), lola_slope.shape)

    elev_png = save_png(dem_m, "lola_85s20m_tmc_overlap_elevation_m", "elevation")
    slope_png = save_png(lola_slope, "lola_85s20m_tmc_overlap_slope_deg", "slope")
    rough_png = save_png(lola_rough, "lola_85s20m_tmc_overlap_roughness_m", "rough")

    valid = np.isfinite(tmc) & np.isfinite(lola_slope)
    tmc_mean = float(np.nanmean(tmc[valid])) if valid.any() else float("nan")
    lola_mean = float(np.nanmean(lola_slope[valid])) if valid.any() else float("nan")
    diff = abs(tmc_mean - lola_mean)
    if diff <= 5:
        agreement = "strong independent sanity check"
    elif diff <= 12:
        agreement = "moderate independent sanity check"
    else:
        agreement = "needs AOI/projection review"

    summary = {
        "source": "NASA PDS / LRO LOLA Gridded Data Record",
        "source_url": "https://pds-geosciences.wustl.edu/lro/lro-l-lola-3-rdr-v1/lrolol_1xxx/data/lola_gdr/polar/float_img/",
        "source_product": "LDEM_85S_20M",
        "raw_label": str(LOLA_DEM.relative_to(ROOT)),
        "tmc_bounds_m": list(tmc_bounds),
        "lola_overlap_bounds_m": list(lola_bounds),
        "crop_shape": list(lola_slope.shape),
        "effective_pixel_size_m": processing["effective_pixel_size_m"],
        "tmc_slope_mean_deg": tmc_mean,
        "lola_slope_mean_deg": lola_mean,
        "mean_slope_difference_deg": diff,
        "agreement_label": agreement,
        "outputs": {
            "lola_elevation_png": str(elev_png.relative_to(ROOT)),
            "lola_slope_png": str(slope_png.relative_to(ROOT)),
            "lola_roughness_png": str(rough_png.relative_to(ROOT)),
            "focus_asset": str((DEMO / "lola_validation_focus.png").relative_to(ROOT)),
        },
        "notes": [
            "The source LOLA product is 20 m/pixel over 85S-90S.",
            "The dashboard quicklook is downsampled for interactivity, but it is derived from the 20 m PDS product.",
            "This validates terrain behavior independently; it does not replace registered OHRC hazard certification.",
        ],
    }
    focus = make_focus_asset(elev_png, slope_png, rough_png, summary)
    summary["outputs"]["focus_asset"] = str(focus.relative_to(ROOT))
    out_json = DERIVED / "lola_external_validation_summary.json"
    out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
