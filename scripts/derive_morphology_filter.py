from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image, ImageDraw, ImageEnhance, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "processed" / "derived_layers"
DEMO = ROOT / "data" / "processed" / "demo_assets"
DEMO.mkdir(parents=True, exist_ok=True)

SLOPE = DERIVED / "tmc2_south_pole_slope_deg.tif"
ACCESS = DERIVED / "tmc2_south_pole_accessibility_score.tif"
SAR_SCORE = DERIVED / "sar_candidate_ice_evidence_score.tif"
COLD = DERIVED / "cold_trap_proxy.tif"
ORTHO = DERIVED / "tmc2_south_pole_orthobrowse.png"

ROUGH_PNG = DERIVED / "rough_terrain_rejection_mask.png"
FOCUS = DEMO / "rough_terrain_filter_focus.png"
SUMMARY = DERIVED / "morphology_filter_summary.json"


def font(size: int, bold: bool = False):
    names = ["arialbd.ttf", "arial.ttf"] if bold else ["arial.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def read(path: Path) -> np.ndarray:
    with rasterio.open(path) as src:
        arr = src.read(1).astype("float32")
    arr[arr < -1000] = np.nan
    return arr


def norm(arr: np.ndarray) -> np.ndarray:
    valid = np.isfinite(arr)
    out = np.zeros(arr.shape, dtype="float32")
    if valid.any():
        lo, hi = np.nanpercentile(arr[valid], [2, 98])
        if hi <= lo:
            hi = lo + 1.0
        out = np.clip((arr - lo) / (hi - lo), 0, 1)
    out[~valid] = np.nan
    return out


def match_shape(arr: np.ndarray, shape: tuple[int, int]) -> np.ndarray:
    n = norm(arr)
    if arr.shape == shape:
        return n
    image = Image.fromarray((np.nan_to_num(n, nan=0) * 255).astype("uint8"))
    image = image.resize((shape[1], shape[0]), Image.Resampling.BILINEAR)
    return np.array(image).astype("float32") / 255.0


def save_png(path: Path, arr: np.ndarray) -> None:
    image = (np.nan_to_num(norm(arr), nan=0) * 255).astype("uint8")
    Image.fromarray(image).save(path)


def terrain_region_crops(img: Image.Image, count: int = 2) -> list[Image.Image]:
    gray = np.asarray(img.convert("L"))
    mask = gray > 18
    try:
        from scipy import ndimage

        labels, total = ndimage.label(mask)
        regions = []
        for label_id in range(1, total + 1):
            ys, xs = np.where(labels == label_id)
            if len(xs) < 500:
                continue
            x1, x2 = xs.min(), xs.max()
            y1, y2 = ys.min(), ys.max()
            area = (x2 - x1 + 1) * (y2 - y1 + 1)
            regions.append((area, x1, y1, x2, y2))
        regions.sort(reverse=True)
        boxes = [(x1, y1, x2 + 1, y2 + 1) for _, x1, y1, x2, y2 in regions[:count]]
    except Exception:
        boxes = [(0, 0, img.width // 2, img.height // 2), (img.width // 2, img.height // 2, img.width, img.height)]
    return [img.crop(box) for box in boxes]


def main() -> None:
    slope = read(SLOPE)
    access = read(ACCESS)
    sar = read(SAR_SCORE)
    cold = read(COLD)

    slope_n = norm(slope)
    access_n = norm(access)
    sar_n = match_shape(sar, slope.shape)
    cold_n = match_shape(cold, slope.shape)

    rough_risk = np.clip(0.55 * slope_n + 0.25 * (1.0 - access_n) + 0.20 * np.abs(sar_n - cold_n), 0, 1)
    candidate_consistency = np.clip(0.45 * sar_n + 0.35 * cold_n + 0.20 * access_n - 0.35 * rough_risk, 0, 1)
    rough_risk[~(np.isfinite(slope_n) & np.isfinite(access_n))] = np.nan
    candidate_consistency[~np.isfinite(rough_risk)] = np.nan

    save_png(ROUGH_PNG, rough_risk * 100)

    base = Image.open(ORTHO).convert("RGB").resize((1440, 960), Image.Resampling.LANCZOS)
    rough = Image.open(ROUGH_PNG).convert("L").resize((1440, 960), Image.Resampling.BILINEAR)
    rough_arr = np.array(rough)
    overlay = Image.new("RGBA", (1440, 960), (255, 93, 93, 0))
    rough_threshold = np.percentile(rough_arr[rough_arr > 0], 84) if (rough_arr > 0).any() else 255
    alpha = np.where(rough_arr > rough_threshold, 130, 0).astype("uint8")
    overlay.putalpha(Image.fromarray(alpha))
    map_canvas = base.convert("RGBA")
    map_canvas.alpha_composite(overlay)
    map_image = map_canvas.convert("RGB")
    crops = terrain_region_crops(map_image, 2)

    out = Image.new("RGB", (1440, 960), (5, 9, 13))
    draw = ImageDraw.Draw(out)
    draw.rectangle((34, 34, 1406, 926), outline=(45, 75, 86), width=2)
    draw.text((62, 58), "Rough-Terrain False-Positive Filter", fill=(244, 247, 248), font=font(44, bold=True))
    draw.text((62, 114), "Reject radar-bright rough terrain before ice-volume ranking", fill=(255, 180, 180), font=font(28))

    panels = [(64, 190, 682, 724), (724, 190, 1168, 724)]
    labels = ["review/reject terrain island", "candidate corridor context"]
    for crop, box, label in zip(crops, panels, labels):
        crop = ImageEnhance.Contrast(crop).enhance(1.18)
        crop.thumbnail((box[2] - box[0] - 36, box[3] - box[1] - 72), Image.Resampling.LANCZOS)
        x = box[0] + (box[2] - box[0] - crop.width) // 2
        y = box[1] + 24
        draw.rectangle(box, fill=(0, 0, 0), outline=(45, 75, 86), width=2)
        out.paste(crop, (x, y))
        draw.rectangle((box[0], box[3] - 54, box[2], box[3]), fill=(4, 9, 12))
        draw.text((box[0] + 22, box[3] - 38), label, fill=(255, 180, 180), font=font(23, bold=True))

    side_x = 1198
    draw.rectangle((side_x, 190, 1374, 724), fill=(8, 17, 22), outline=(242, 191, 90), width=2)
    draw.text((side_x + 22, 226), "Mentor", fill=(242, 191, 90), font=font(28, bold=True))
    draw.text((side_x + 22, 272), "check", fill=(244, 247, 248), font=font(30, bold=True))
    draw.text((side_x + 22, 340), "Slope", fill=(150, 211, 205), font=font(24, bold=True))
    draw.text((side_x + 22, 382), "Access", fill=(150, 211, 205), font=font(24, bold=True))
    draw.text((side_x + 22, 424), "SAR/cold", fill=(150, 211, 205), font=font(24, bold=True))
    draw.text((side_x + 22, 466), "mismatch", fill=(150, 211, 205), font=font(24, bold=True))
    draw.text((side_x + 22, 546), "Goal", fill=(242, 191, 90), font=font(28, bold=True))
    draw.text((side_x + 22, 592), "avoid", fill=(244, 247, 248), font=font(28, bold=True))
    draw.text((side_x + 22, 628), "false ice", fill=(244, 247, 248), font=font(28, bold=True))

    draw.rectangle((64, 772, 1374, 876), fill=(9, 18, 23), outline=(41, 66, 76), width=2)
    draw.text((92, 794), "Interpretation", fill=(242, 191, 90), font=font(28, bold=True))
    draw.text((290, 794), "Red overlay marks terrain that should be rejected or reviewed before selecting ice targets.", fill=(238, 248, 249), font=font(25))
    draw.text((290, 834), "It helps distinguish radar-bright rough rock from plausible volatile-bearing terrain.", fill=(150, 211, 205), font=font(23))
    out.save(FOCUS, quality=95)

    valid = np.isfinite(rough_risk)
    high_rough = rough_risk > np.nanpercentile(rough_risk[valid], 84)
    high_candidate = candidate_consistency > np.nanpercentile(candidate_consistency[np.isfinite(candidate_consistency)], 88)
    summary = {
        "framing": "Prototype morphology/roughness screen for rejecting rough-terrain radar false positives.",
        "inputs": [
            str(SLOPE.relative_to(ROOT)),
            str(ACCESS.relative_to(ROOT)),
            str(SAR_SCORE.relative_to(ROOT)),
            str(COLD.relative_to(ROOT)),
        ],
        "formula": "0.55*slope + 0.25*(1-accessibility) + 0.20*abs(SAR-cold_trap)",
        "high_rough_pixel_pct": float(high_rough.sum() / valid.sum() * 100) if valid.any() else 0.0,
        "candidate_after_rejection_pct": float(high_candidate.sum() / valid.sum() * 100) if valid.any() else 0.0,
        "outputs": {
            "rough_png": str(ROUGH_PNG.relative_to(ROOT)),
            "focus": str(FOCUS.relative_to(ROOT)),
        },
        "caution": "This is a terrain-morphology proxy. Registered OHRC boulder/crater extraction is still required for final hazard certification.",
    }
    SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
