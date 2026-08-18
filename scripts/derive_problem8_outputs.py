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

SAR_SCORE = DERIVED / "sar_candidate_ice_evidence_score.tif"
SAR_CROSS_CO = DERIVED / "sar_cross_to_co_ratio.tif"
SAR_HH_VV = DERIVED / "sar_hh_vv_ratio.tif"
ACCESS = DERIVED / "tmc2_south_pole_accessibility_score.tif"
SLOPE = DERIVED / "tmc2_south_pole_slope_deg.tif"
COLD = DERIVED / "cold_trap_proxy.tif"
SHADOW = DERIVED / "shadow_persistence_proxy.tif"
ILLUM = DERIVED / "illumination_availability_proxy.tif"
ORTHO = DERIVED / "tmc2_south_pole_orthobrowse.png"

DSC_TIF = DERIVED / "doubly_shadowed_crater_proxy_score.tif"
DSC_PNG = DERIVED / "doubly_shadowed_crater_proxy_score.png"
DSC_FOCUS = DEMO / "doubly_shadowed_crater_focus.png"
CPR_DOP_FOCUS = DEMO / "cpr_dop_threshold_focus.png"
VOLUME_FOCUS = DEMO / "ice_volume_estimator_focus.png"
SUMMARY = DERIVED / "problem8_gap_closure_summary.json"


def font(size: int, bold: bool = False):
    names = ["arialbd.ttf", "arial.ttf"] if bold else ["arial.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def wrap_text(text: str, draw: ImageDraw.ImageDraw, text_font: ImageFont.ImageFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        if draw.textbbox((0, 0), test, font=text_font)[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def read(path: Path) -> tuple[np.ndarray, dict]:
    with rasterio.open(path) as src:
        arr = src.read(1).astype("float32")
        profile = src.profile.copy()
    arr[arr < -1000] = np.nan
    return arr, profile


def robust_norm(arr: np.ndarray) -> np.ndarray:
    valid = np.isfinite(arr)
    out = np.zeros(arr.shape, dtype="float32")
    if valid.any():
        lo, hi = np.nanpercentile(arr[valid], [2, 98])
        if hi <= lo:
            hi = lo + 1
        out = np.clip((arr - lo) / (hi - lo), 0, 1)
    out[~valid] = np.nan
    return out


def save_tif(path: Path, arr: np.ndarray, profile: dict) -> None:
    profile = profile.copy()
    profile.update(dtype="float32", count=1, compress="deflate", nodata=np.nan)
    with rasterio.open(path, "w", **profile) as dst:
        dst.write(arr.astype("float32"), 1)


def save_png(path: Path, arr: np.ndarray) -> None:
    norm = robust_norm(arr)
    image = (np.nan_to_num(norm, nan=0) * 255).astype("uint8")
    Image.fromarray(image).save(path)


def draw_bar(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], value: float, label: str, color: tuple[int, int, int]) -> None:
    x1, y1, x2, y2 = box
    draw.rectangle(box, outline=(42, 67, 77), width=2)
    fill = int((x2 - x1) * np.clip(value, 0, 1))
    draw.rectangle((x1, y1, x1 + fill, y2), fill=color)
    draw.text((x1, y1 - 22), label, fill=(220, 236, 240), font=ImageFont.load_default())
    draw.text((x2 - 64, y1 - 22), f"{value * 100:.0f}%", fill=color, font=ImageFont.load_default())


def draw_metric_card(title: str, subtitle: str, lines: list[str], path: Path, accent=(49, 214, 204)) -> None:
    canvas = Image.new("RGB", (1440, 960), (5, 9, 13))
    draw = ImageDraw.Draw(canvas)
    title_font = font(42, bold=True)
    subtitle_font = font(24)
    body_font = font(29)
    small_font = font(22)
    draw.rectangle((34, 34, 1406, 926), outline=(45, 75, 86), width=2)
    draw.text((66, 62), title, fill=(238, 248, 249), font=title_font)
    draw.text((66, 116), subtitle, fill=accent, font=subtitle_font)
    y = 190
    for line in lines:
        wrapped = wrap_text(line, draw, body_font, 1200)
        height = max(102, 38 + len(wrapped) * 36)
        draw.rectangle((66, y, 1374, y + height), fill=(10, 18, 23), outline=(39, 61, 70), width=2)
        for index, text_line in enumerate(wrapped):
            draw.text((94, y + 24 + index * 38), text_line, fill=(218, 235, 238), font=body_font)
        y += height + 24
    draw.text((66, 888), "Scientific claim level: screening evidence only, not confirmed lunar ice.", fill=(150, 211, 205), font=small_font)
    path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(path, quality=95)


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


def make_dsc_layer() -> dict:
    cold, profile = read(COLD)
    shadow, _ = read(SHADOW)
    illum, _ = read(ILLUM)
    access, _ = read(ACCESS)
    slope, _ = read(SLOPE)

    cold_n = robust_norm(cold) * 100
    shadow_n = robust_norm(shadow) * 100
    illum_n = robust_norm(illum) * 100
    access_n = robust_norm(access) * 100
    slope_n = robust_norm(slope) * 100

    dsc = np.clip(
        0.34 * cold_n
        + 0.30 * shadow_n
        + 0.18 * (100 - illum_n)
        + 0.10 * access_n
        + 0.08 * (100 - slope_n),
        0,
        100,
    )
    dsc[~(np.isfinite(cold_n) & np.isfinite(shadow_n) & np.isfinite(illum_n))] = np.nan
    save_tif(DSC_TIF, dsc, profile)
    save_png(DSC_PNG, dsc)

    valid = np.isfinite(dsc)
    threshold = float(np.nanpercentile(dsc[valid], 94)) if valid.any() else 85.0
    mask = valid & (dsc >= threshold)
    pixel_area_m2 = abs(float(profile["transform"][0]) * float(profile["transform"][4]))
    candidate_area_m2 = float(mask.sum() * pixel_area_m2)
    depth_m = 5.0
    scenarios = {
        "low_3pct": candidate_area_m2 * depth_m * 0.03,
        "medium_8pct": candidate_area_m2 * depth_m * 0.08,
        "high_15pct": candidate_area_m2 * depth_m * 0.15,
    }

    base = Image.open(ORTHO).convert("RGB").resize((1440, 960), Image.Resampling.LANCZOS)
    overlay = Image.open(DSC_PNG).convert("L").resize((1440, 960), Image.Resampling.BILINEAR)
    color = Image.new("RGBA", (1440, 960), (53, 229, 214, 0))
    alpha = np.array(overlay)
    alpha = np.where(alpha > np.percentile(alpha[alpha > 0], 88) if (alpha > 0).any() else 255, 145, 0).astype("uint8")
    color.putalpha(Image.fromarray(alpha))
    base_rgba = base.convert("RGBA")
    base_rgba.alpha_composite(color)
    map_image = base_rgba.convert("RGB")
    crops = terrain_region_crops(map_image, 2)

    canvas = Image.new("RGB", (1440, 960), (5, 9, 13))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((34, 34, 1406, 926), outline=(45, 75, 86), width=2)
    draw.text((62, 58), "DSC-1 / Faustini-Class Candidate", fill=(244, 247, 248), font=font(46, bold=True))
    draw.text((62, 116), "Proxy doubly shadowed crater target until official AOI arrives", fill=(150, 211, 205), font=font(28))

    panels = [(64, 190, 680, 724), (724, 190, 1168, 724)]
    labels = ["candidate terrain island", "secondary overlap context"]
    for crop, box, label in zip(crops, panels, labels):
        crop = ImageEnhance.Contrast(crop).enhance(1.18)
        crop.thumbnail((box[2] - box[0] - 36, box[3] - box[1] - 72), Image.Resampling.LANCZOS)
        x = box[0] + (box[2] - box[0] - crop.width) // 2
        y = box[1] + 24
        draw.rectangle(box, fill=(0, 0, 0), outline=(45, 75, 86), width=2)
        canvas.paste(crop, (x, y))
        draw.rectangle((box[0], box[3] - 54, box[2], box[3]), fill=(4, 9, 12))
        draw.text((box[0] + 22, box[3] - 38), label, fill=(53, 229, 214), font=font(23, bold=True))

    side_x = 1198
    draw.rectangle((side_x, 190, 1374, 724), fill=(8, 17, 22), outline=(53, 229, 214), width=2)
    draw.text((side_x + 22, 226), "Score", fill=(53, 229, 214), font=font(28, bold=True))
    draw.text((side_x + 22, 272), "Top 6%", fill=(244, 247, 248), font=font(32, bold=True))
    draw.text((side_x + 22, 330), "Area", fill=(53, 229, 214), font=font(28, bold=True))
    draw.text((side_x + 22, 376), f"{candidate_area_m2 / 1_000_000:.2f}", fill=(244, 247, 248), font=font(32, bold=True))
    draw.text((side_x + 22, 414), "sq km", fill=(185, 211, 214), font=font(21))
    draw.text((side_x + 22, 478), "Depth", fill=(53, 229, 214), font=font(28, bold=True))
    draw.text((side_x + 22, 524), "0-5 m", fill=(244, 247, 248), font=font(32, bold=True))
    draw.text((side_x + 22, 590), "Claim", fill=(53, 229, 214), font=font(28, bold=True))
    draw.text((side_x + 22, 636), "proxy", fill=(255, 224, 166), font=font(30, bold=True))

    draw.rectangle((64, 772, 1374, 876), fill=(9, 18, 23), outline=(41, 66, 76), width=2)
    draw.text((92, 794), "Interpretation", fill=(242, 191, 90), font=font(28, bold=True))
    draw.text((290, 794), "Cyan marks cold + shadow candidate terrain for landing/traverse planning.", fill=(238, 248, 249), font=font(25))
    draw.text((290, 834), "It is not confirmed ice; exact AOI, CPR/DOP, and ephemeris illumination are still validation gates.", fill=(150, 211, 205), font=font(23))
    canvas.save(DSC_FOCUS, quality=95)

    return {
        "threshold_score": threshold,
        "candidate_area_m2": candidate_area_m2,
        "candidate_area_km2": candidate_area_m2 / 1_000_000,
        "volume_scenarios_m3": scenarios,
        "depth_m": depth_m,
        "outputs": {
            "dsc_tif": str(DSC_TIF.relative_to(ROOT)),
            "dsc_png": str(DSC_PNG.relative_to(ROOT)),
            "dsc_focus": str(DSC_FOCUS.relative_to(ROOT)),
        },
    }


def make_cpr_dop_summary() -> dict:
    score, _ = read(SAR_SCORE)
    cross_co, _ = read(SAR_CROSS_CO)
    hh_vv, _ = read(SAR_HH_VV)
    valid = np.isfinite(score) & np.isfinite(cross_co) & np.isfinite(hh_vv)
    cpr_proxy = robust_norm(cross_co) * 1.45
    dop_risk_proxy = 1.0 - robust_norm(np.abs(hh_vv - 1.0))
    candidate = valid & (cpr_proxy > 1.0) & (dop_risk_proxy > 0.87)
    summary = {
        "status": "CPR/DOP-ready proxy, not exact CPR/DOP",
        "why_not_exact": "Current extracted DFSAR rasters are intensity products. Exact CPR/DOP needs calibrated polarimetric products with required phase/coherency terms or official MIDAS-style outputs.",
        "thresholds_from_problem": {"cpr": "> 1", "dop": "< 0.13"},
        "proxy_candidate_pixel_pct": float(candidate.sum() / valid.sum() * 100.0) if valid.any() else 0.0,
        "mean_cpr_proxy_in_candidates": float(np.nanmean(cpr_proxy[candidate])) if candidate.any() else None,
        "mean_dop_risk_proxy_in_candidates": float(np.nanmean(1.0 - dop_risk_proxy[candidate])) if candidate.any() else None,
    }
    draw_metric_card(
        "CPR / DOP Detection Gate",
        "Problem threshold shown explicitly; exact computation pending calibrated polarimetry",
        [
            "Target criteria: CPR > 1 and DOP < 0.13 for refined ice-candidate screening.",
            f"Current proxy screen: {summary['proxy_candidate_pixel_pct']:.2f}% of valid SAR pixels pass CPR-like and depolarization-like gates.",
            "Scientific status: candidate evidence only; exact CPR/DOP requires phase/coherency-aware DFSAR processing.",
            "Next step: replace proxy gate with MIDAS/official polarimetric CPR and DOP outputs when supplied crater data arrives.",
        ],
        CPR_DOP_FOCUS,
        accent=(255, 224, 166),
    )
    summary["output_image"] = str(CPR_DOP_FOCUS.relative_to(ROOT))
    return summary


def make_volume_card(dsc: dict) -> dict:
    scenarios = dsc["volume_scenarios_m3"]
    area_km2 = dsc["candidate_area_km2"]
    lines = [
        f"Candidate DSC-1 area: {area_km2:.2f} sq km from the top-scoring cold/shadow terrain mask.",
        "Depth assumption: top 5 m of regolith, matching the problem statement requirement.",
        f"Low scenario, 3% ice fraction: {scenarios['low_3pct'] / 1_000_000:.3f} million cubic m water-equivalent ice.",
        f"Medium scenario, 8% ice fraction: {scenarios['medium_8pct'] / 1_000_000:.3f} million cubic m water-equivalent ice.",
        f"High scenario, 15% ice fraction: {scenarios['high_15pct'] / 1_000_000:.3f} million cubic m water-equivalent ice.",
    ]
    draw_metric_card(
        "Top 5 m Subsurface Ice Volume Estimator",
        "Scenario estimate, not a confirmed reserve measurement",
        lines,
        VOLUME_FOCUS,
        accent=(53, 229, 214),
    )
    return {"output_image": str(VOLUME_FOCUS.relative_to(ROOT)), "assumption": "area * 5 m * ice_fraction"}


def main() -> None:
    dsc = make_dsc_layer()
    cpr_dop = make_cpr_dop_summary()
    volume = make_volume_card(dsc)
    summary = {
        "framing": "Problem Statement 8 gap closure outputs for Faustini-class doubly shadowed crater screening.",
        "doubly_shadowed_crater_proxy": dsc,
        "cpr_dop_gate": cpr_dop,
        "volume_estimator": volume,
        "scientific_caution": [
            "DSC-1 is a proxy target until the official supplied crater AOI is received.",
            "CPR/DOP output is a threshold-ready proxy, not exact CPR/DOP.",
            "Volume estimate is scenario-based and must be recalibrated after exact radar inversion.",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
