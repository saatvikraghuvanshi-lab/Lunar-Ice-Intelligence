from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "processed" / "derived_layers"
DEMO = ROOT / "data" / "processed" / "demo_assets"

SAR_SCORE = DERIVED / "sar_candidate_ice_evidence_score.png"
CROSS_CO = DERIVED / "sar_cross_to_co_ratio.png"
HH_VV = DERIVED / "sar_hh_vv_ratio.png"
CO_POL = DERIVED / "sar_co_pol_mean.png"

CPR_PROXY_PNG = DERIVED / "experimental_cpr_like_proxy.png"
DOP_PROXY_PNG = DERIVED / "experimental_dop_like_proxy.png"
MASK_PNG = DERIVED / "experimental_cpr_dop_candidate_mask.png"
FOCUS = DEMO / "experimental_cpr_dop_proxy_focus.png"
SUMMARY = DERIVED / "experimental_cpr_dop_proxy_summary.json"


def font(size: int, bold: bool = False):
    names = ["arialbd.ttf" if bold else "arial.ttf", "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def read_gray(path: Path) -> np.ndarray:
    arr = np.asarray(Image.open(path).convert("L")).astype("float32") / 255.0
    return arr


def colorize(arr: np.ndarray, palette: str = "radar", valid: np.ndarray | None = None) -> Image.Image:
    arr = np.clip(arr, 0, 1)
    if valid is None:
        valid = np.ones(arr.shape, dtype=bool)
    if palette == "mask":
        rgb = np.zeros((*arr.shape, 3), dtype=np.uint8)
        rgb[..., 0] = np.where(arr > 0.5, 255, 8)
        rgb[..., 1] = np.where(arr > 0.5, 206, 18)
        rgb[..., 2] = np.where(arr > 0.5, 79, 22)
        rgb[~valid] = (0, 0, 0)
        return Image.fromarray(rgb)
    if palette == "dop":
        rgb = np.zeros((*arr.shape, 3), dtype=np.uint8)
        rgb[..., 0] = (40 + arr * 215).astype(np.uint8)
        rgb[..., 1] = (220 - arr * 160).astype(np.uint8)
        rgb[..., 2] = (255 - arr * 215).astype(np.uint8)
        rgb[~valid] = (0, 0, 0)
        return Image.fromarray(rgb)
    rgb = np.zeros((*arr.shape, 3), dtype=np.uint8)
    rgb[..., 0] = (arr * 255).astype(np.uint8)
    rgb[..., 1] = np.clip(70 + arr * 150, 0, 255).astype(np.uint8)
    rgb[..., 2] = np.clip(210 - arr * 160, 0, 255).astype(np.uint8)
    rgb[~valid] = (0, 0, 0)
    return Image.fromarray(rgb)


def fit_image(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    out = Image.new("RGB", size, (0, 0, 0))
    img = img.convert("RGB")
    img.thumbnail(size, Image.Resampling.LANCZOS)
    out.paste(img, ((size[0] - img.width) // 2, (size[1] - img.height) // 2))
    return out


def main() -> None:
    DEMO.mkdir(parents=True, exist_ok=True)
    DERIVED.mkdir(parents=True, exist_ok=True)

    score = read_gray(SAR_SCORE)
    cross = read_gray(CROSS_CO)
    hhvv = read_gray(HH_VV)
    copol = read_gray(CO_POL)

    # This is an explainable screening approximation, not a physics-exact CPR/DOP inversion.
    cpr_like = np.clip(1.65 * (0.52 * cross + 0.33 * score + 0.15 * copol), 0, 1.65)
    linear_balance = 1.0 - np.clip(np.abs(hhvv - 0.5) * 2.0, 0, 1)
    depol_strength = np.clip(0.65 * cross + 0.35 * linear_balance, 0, 1)
    dop_like = np.clip(0.22 * (1.0 - depol_strength), 0, 0.22)

    candidate = (cpr_like > 1.0) & (dop_like < 0.13) & (score > 0.58)
    valid = score > 0.03
    candidate_pct = float(candidate.sum() / max(1, valid.sum()) * 100.0)

    Image.fromarray((np.clip(cpr_like / 1.65, 0, 1) * 255).astype(np.uint8)).save(CPR_PROXY_PNG)
    Image.fromarray((np.clip(dop_like / 0.22, 0, 1) * 255).astype(np.uint8)).save(DOP_PROXY_PNG)
    Image.fromarray(np.where(candidate, 255, 0).astype(np.uint8)).save(MASK_PNG)

    canvas = Image.new("RGB", (1600, 1100), (5, 9, 13))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((34, 34, 1566, 1066), outline=(45, 75, 86), width=2)
    draw.text((58, 58), "Experimental CPR/DOP Proxy Screening", fill=(238, 248, 249), font=font(42, True))
    draw.text(
        (58, 112),
        "uses available HH/HV/VH/VV-derived layers to mimic the required CPR > 1 and DOP < 0.13 gate; not exact calibrated polarimetry",
        fill=(150, 211, 205),
        font=font(22),
    )

    panels = [
        ("CPR-like proxy", colorize(cpr_like / 1.65, "radar", valid), (58, 178, 512, 678), "higher = more circular/depolarized-style evidence"),
        ("DOP-like proxy", colorize(dop_like / 0.22, "dop", valid), (572, 178, 1026, 678), "lower = more depolarized-style response"),
        ("Threshold pass mask", colorize(candidate.astype("float32"), "mask", valid), (1086, 178, 1540, 678), "yellow = CPR-like > 1, DOP-like < 0.13, radar score gate"),
    ]
    for title, img, box, caption in panels:
        draw.rectangle(box, outline=(45, 75, 86), width=2)
        fitted = fit_image(img, (box[2] - box[0] - 34, box[3] - box[1] - 104))
        canvas.paste(fitted, (box[0] + 17, box[1] + 22))
        draw.rectangle((box[0], box[3] - 72, box[2], box[3]), fill=(4, 9, 12))
        draw.text((box[0] + 18, box[3] - 58), title, fill=(238, 248, 249), font=font(21, True))
        draw.text((box[0] + 18, box[3] - 30), caption, fill=(150, 211, 205), font=font(15))

    draw.rectangle((58, 724, 1540, 926), fill=(9, 18, 23), outline=(41, 66, 76), width=2)
    draw.text((86, 746), "What this adds", fill=(53, 229, 214), font=font(27, True))
    bullets = [
        f"Candidate pass rate: {candidate_pct:.2f}% of valid SAR-screened pixels pass the experimental gate.",
        f"Mean CPR-like value in pass mask: {float(np.mean(cpr_like[candidate])) if candidate.any() else 0:.2f}; target threshold shown as > 1.",
        f"Mean DOP-like value in pass mask: {float(np.mean(dop_like[candidate])) if candidate.any() else 0:.3f}; target threshold shown as < 0.13.",
        "This narrows the gap visually and algorithmically, but the pitch must still say exact CPR/DOP needs calibrated polarimetric processing.",
    ]
    y = 790
    for bullet in bullets:
        draw.text((92, y), f"- {bullet}", fill=(238, 248, 249), font=font(19))
        y += 32

    draw.rectangle((58, 950, 1540, 1032), fill=(18, 12, 10), outline=(255, 108, 108), width=2)
    draw.text((86, 974), "Scientific honesty:", fill=(255, 166, 166), font=font(23, True))
    draw.text(
        (310, 974),
        "Experimental proxy only. Final acceptance requires official/MIDAS CPR + DOP rasters on the supplied crater AOI.",
        fill=(255, 224, 166),
        font=font(20),
    )

    canvas.save(FOCUS, quality=95)
    summary = {
        "status": "experimental proxy, not exact CPR/DOP",
        "inputs": {
            "sar_score": str(SAR_SCORE.relative_to(ROOT)),
            "cross_to_co_ratio": str(CROSS_CO.relative_to(ROOT)),
            "hh_vv_ratio": str(HH_VV.relative_to(ROOT)),
            "co_pol_mean": str(CO_POL.relative_to(ROOT)),
        },
        "formulas": {
            "cpr_like": "1.65 * (0.52 * cross_to_co_norm + 0.33 * sar_score_norm + 0.15 * co_pol_norm)",
            "dop_like": "0.22 * (1 - (0.65 * cross_to_co_norm + 0.35 * linear_balance_proxy))",
            "candidate_mask": "cpr_like > 1.0 AND dop_like < 0.13 AND sar_score_norm > 0.58",
        },
        "metrics": {
            "candidate_pixel_pct": candidate_pct,
            "mean_cpr_like_in_candidates": float(np.mean(cpr_like[candidate])) if candidate.any() else None,
            "mean_dop_like_in_candidates": float(np.mean(dop_like[candidate])) if candidate.any() else None,
        },
        "outputs": {
            "cpr_like_png": str(CPR_PROXY_PNG.relative_to(ROOT)),
            "dop_like_png": str(DOP_PROXY_PNG.relative_to(ROOT)),
            "candidate_mask_png": str(MASK_PNG.relative_to(ROOT)),
            "focus_card": str(FOCUS.relative_to(ROOT)),
        },
        "required_for_exact": [
            "official supplied doubly shadowed crater AOI",
            "calibrated polarimetric CPR raster",
            "calibrated polarimetric DOP raster",
            "or MIDAS/official processor output with phase/coherency-aware products",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
