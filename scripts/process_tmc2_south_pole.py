from __future__ import annotations

import json
import math
import shutil
from pathlib import Path

import numpy as np
import rasterio
from affine import Affine
from PIL import Image, ImageDraw, ImageFont
from rasterio.enums import Resampling


ROOT = Path(__file__).resolve().parents[1]
EXTRACTED = ROOT / "data" / "processed" / "extracted_tmc2_south_pole"
OUT = ROOT / "data" / "processed" / "derived_layers"
OUT.mkdir(parents=True, exist_ok=True)

DTM = EXTRACTED / "data" / "derived" / "20231203" / "ch2_tmc_ndn_20231203T0019079527_d_dtm_d18.tif"
OTH_BROWSE = EXTRACTED / "browse" / "derived" / "20231203" / "ch2_tmc_ndn_20231203T0019079527_b_bot_d18.png"
DTM_BROWSE = EXTRACTED / "browse" / "derived" / "20231203" / "ch2_tmc_ndn_20231203T0019079527_b_bdt_d18.png"

MOON_RADIUS_M = 1_737_400.0


def robust_uint8(array: np.ndarray, low: float = 2, high: float = 98) -> np.ndarray:
    data = array.astype("float32", copy=False)
    valid = np.isfinite(data)
    if not valid.any():
        return np.zeros(data.shape, dtype=np.uint8)
    lo, hi = np.nanpercentile(data[valid], [low, high])
    if hi <= lo:
        hi = lo + 1
    scaled = (data - lo) / (hi - lo)
    return (np.clip(scaled, 0, 1) * 255).astype(np.uint8)


def colorize(gray: np.ndarray, palette: str) -> Image.Image:
    g = gray.astype(np.float32) / 255.0
    if palette == "terrain":
        stops = np.array(
            [
                [34, 63, 83],
                [66, 113, 116],
                [122, 154, 111],
                [190, 176, 121],
                [232, 224, 191],
            ],
            dtype=np.float32,
        )
    elif palette == "slope":
        stops = np.array(
            [
                [26, 72, 86],
                [66, 145, 120],
                [224, 188, 82],
                [210, 86, 63],
            ],
            dtype=np.float32,
        )
    else:
        stops = np.array(
            [
                [71, 45, 106],
                [35, 116, 128],
                [82, 164, 83],
                [231, 203, 88],
            ],
            dtype=np.float32,
        )
    scaled = g * (len(stops) - 1)
    idx = np.floor(scaled).astype(np.int16)
    idx = np.clip(idx, 0, len(stops) - 2)
    frac = scaled - idx
    rgb = stops[idx] * (1 - frac[..., None]) + stops[idx + 1] * frac[..., None]
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")


def write_png(name: str, arr: np.ndarray, palette: str, low: float = 2, high: float = 98) -> Path:
    path = OUT / f"{name}.png"
    colorize(robust_uint8(arr, low, high), palette).save(path)
    return path


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


def polar_bounds_to_lat_range(bounds: tuple[float, float, float, float]) -> dict[str, float]:
    xs = [bounds[0], bounds[2]]
    ys = [bounds[1], bounds[3]]
    radii = [math.hypot(x, y) for x in xs for y in ys]
    # Spherical polar stereographic approximation, enough for triage/reporting.
    angular = [2 * math.atan(r / (2 * MOON_RADIUS_M)) for r in radii]
    lats = [-90 + math.degrees(a) for a in angular]
    return {"approx_min_lat": min(lats), "approx_max_lat": max(lats)}


def make_contact_sheet(items: list[tuple[str, Path]], output: Path) -> None:
    thumb_w, thumb_h = 520, 320
    pad = 24
    label_h = 42
    sheet = Image.new("RGB", (thumb_w * 2 + pad * 3, (thumb_h + label_h) * 2 + pad * 3), (245, 247, 250))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    for index, (label, path) in enumerate(items):
        img = Image.open(path).convert("RGB")
        img.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = pad + (index % 2) * (thumb_w + pad)
        y = pad + (index // 2) * (thumb_h + label_h + pad)
        frame = Image.new("RGB", (thumb_w, thumb_h), (16, 24, 32))
        frame.paste(img, ((thumb_w - img.width) // 2, (thumb_h - img.height) // 2))
        sheet.paste(frame, (x, y))
        draw.text((x, y + thumb_h + 10), label, fill=(20, 32, 44), font=font)
    sheet.save(output)


def main() -> None:
    with rasterio.open(DTM) as src:
        scale = max(src.width / 4096, src.height / 4096, 1)
        out_w = int(src.width / scale)
        out_h = int(src.height / scale)
        elevation = src.read(1, out_shape=(out_h, out_w), resampling=Resampling.bilinear).astype("float32")
        profile = src.profile.copy()
        transform = src.transform * Affine.scale(src.width / out_w, src.height / out_h)
        bounds = tuple(src.bounds)
        pixel_size_m = abs(transform.a)
        crs = str(src.crs)

    elevation[elevation <= -32000] = np.nan
    grad_y, grad_x = np.gradient(elevation, pixel_size_m, pixel_size_m)
    slope_deg = np.degrees(np.arctan(np.sqrt(grad_x**2 + grad_y**2)))

    slope_score = 1.0 - np.clip(slope_deg / 15.0, 0, 1)
    relief = np.abs(elevation - np.nanmedian(elevation))
    relief_score = 1.0 - np.clip(relief / np.nanpercentile(relief, 95), 0, 1)
    accessibility = np.clip((0.75 * slope_score + 0.25 * relief_score) * 100, 0, 100)

    outputs = {
        "tmc2_south_pole_elevation": write_png("tmc2_south_pole_elevation", elevation, "terrain"),
        "tmc2_south_pole_slope_deg": write_png("tmc2_south_pole_slope_deg", slope_deg, "slope", 0, 95),
        "tmc2_south_pole_accessibility_score": write_png(
            "tmc2_south_pole_accessibility_score", accessibility, "score", 5, 99
        ),
    }
    outputs["tmc2_south_pole_slope_deg_tif"] = write_tif("tmc2_south_pole_slope_deg", slope_deg, profile, transform)
    outputs["tmc2_south_pole_accessibility_score_tif"] = write_tif(
        "tmc2_south_pole_accessibility_score", accessibility, profile, transform
    )

    if OTH_BROWSE.exists():
        orth_out = OUT / "tmc2_south_pole_orthobrowse.png"
        shutil.copyfile(OTH_BROWSE, orth_out)
        outputs["tmc2_south_pole_orthobrowse"] = orth_out
    if DTM_BROWSE.exists():
        dtm_browse_out = OUT / "tmc2_south_pole_dtm_browse.png"
        shutil.copyfile(DTM_BROWSE, dtm_browse_out)
        outputs["tmc2_south_pole_dtm_browse"] = dtm_browse_out

    contact = OUT / "tmc2_south_pole_contact_sheet.png"
    make_contact_sheet(
        [
            ("TMC-2 Orthographic Browse", outputs.get("tmc2_south_pole_orthobrowse", outputs["tmc2_south_pole_elevation"])),
            ("DTM Elevation", outputs["tmc2_south_pole_elevation"]),
            ("Slope From DTM", outputs["tmc2_south_pole_slope_deg"]),
            ("Landing Accessibility", outputs["tmc2_south_pole_accessibility_score"]),
        ],
        contact,
    )
    outputs["tmc2_south_pole_contact_sheet"] = contact

    lat_range = polar_bounds_to_lat_range(bounds)
    summary = {
        "source": str(DTM.relative_to(ROOT)),
        "crs": crs,
        "source_bounds_m": bounds,
        "approx_latitude_range_deg": lat_range,
        "downsampled_shape": [int(out_h), int(out_w)],
        "pixel_size_m_at_processing_scale": pixel_size_m,
        "products": {key: str(value.relative_to(ROOT)) for key, value in outputs.items()},
        "notes": [
            "TMC-2 DTM is used for terrain feasibility layers.",
            "Accessibility is a prototype score based on low slope and moderate local relief; it is not a certified landing-site safety product.",
            "Full OTH raster remains zipped to save roughly 2 GB of disk space; browse image is enough for demo context.",
        ],
    }
    summary_path = OUT / "tmc2_south_pole_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
