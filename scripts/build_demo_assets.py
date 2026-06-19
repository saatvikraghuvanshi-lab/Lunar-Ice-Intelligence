from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed" / "demo_assets"
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "sar_candidate_focus": ROOT / "data" / "processed" / "derived_layers" / "sar_candidate_ice_evidence_score.png",
    "sar_browse_focus": ROOT
    / "data"
    / "processed"
    / "quicklooks"
    / "ch2_sar_ncls_20200913t042439405_b_brw_xx_fp_xx_d18_quicklook.png",
    "tmc2_elevation_focus": ROOT / "data" / "processed" / "derived_layers" / "tmc2_south_pole_elevation.png",
    "tmc2_slope_focus": ROOT / "data" / "processed" / "derived_layers" / "tmc2_south_pole_slope_deg.png",
    "tmc2_accessibility_focus": ROOT
    / "data"
    / "processed"
    / "derived_layers"
    / "tmc2_south_pole_accessibility_score.png",
    "cold_trap_proxy_focus": ROOT / "data" / "processed" / "derived_layers" / "cold_trap_proxy.png",
    "illumination_proxy_focus": ROOT / "data" / "processed" / "derived_layers" / "illumination_availability_proxy.png",
    "tmc2_ortho_focus": ROOT / "data" / "processed" / "derived_layers" / "tmc2_south_pole_orthobrowse.png",
    "ohr_a_focus": ROOT
    / "data"
    / "processed"
    / "quicklooks"
    / "ch2_ohr_ncp_20260103T0609041371_b_brw_d18_quicklook.png",
    "ohr_b_focus": ROOT
    / "data"
    / "processed"
    / "quicklooks"
    / "ch2_ohr_ncp_20260103T1005176450_b_brw_d18_quicklook.png",
}


def find_content_bbox(img: Image.Image) -> tuple[int, int, int, int]:
    rgb = np.asarray(img.convert("RGB")).astype(np.int16)
    h, w, _ = rgb.shape
    corner = 48
    samples = np.concatenate(
        [
            rgb[:corner, :corner].reshape(-1, 3),
            rgb[:corner, -corner:].reshape(-1, 3),
            rgb[-corner:, :corner].reshape(-1, 3),
            rgb[-corner:, -corner:].reshape(-1, 3),
        ],
        axis=0,
    )
    bg = np.median(samples, axis=0)
    distance = np.sqrt(((rgb - bg) ** 2).sum(axis=2))
    brightness = rgb.mean(axis=2)
    mask = (distance > 18) & (brightness > 8)
    ys, xs = np.where(mask)
    if len(xs) == 0 or len(ys) == 0:
        return (0, 0, w, h)
    margin_x = max(24, int((xs.max() - xs.min()) * 0.08))
    margin_y = max(24, int((ys.max() - ys.min()) * 0.08))
    return (
        max(0, xs.min() - margin_x),
        max(0, ys.min() - margin_y),
        min(w, xs.max() + margin_x),
        min(h, ys.max() + margin_y),
    )


def focus_image(src: Path, dest: Path, size: tuple[int, int] = (1440, 960)) -> None:
    img = Image.open(src).convert("RGB")
    bbox = find_content_bbox(img)
    cropped = img.crop(bbox)
    cropped.thumbnail((size[0] - 120, size[1] - 120), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", size, (3, 6, 10))
    shadow = Image.new("RGBA", (cropped.width + 42, cropped.height + 42), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((20, 20, cropped.width + 20, cropped.height + 20), radius=18, fill=(0, 0, 0, 170))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    x = (size[0] - cropped.width) // 2
    y = (size[1] - cropped.height) // 2
    canvas.paste(shadow.convert("RGB"), (x - 21, y - 21))
    canvas.paste(cropped, (x, y))
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, quality=95)


def make_fusion_board() -> None:
    board = Image.new("RGB", (1600, 980), (5, 8, 12))
    draw = ImageDraw.Draw(board)
    try:
        title_font = ImageFont.truetype("arial.ttf", 34)
        label_font = ImageFont.truetype("arial.ttf", 22)
        small_font = ImageFont.truetype("arial.ttf", 17)
    except OSError:
        title_font = label_font = small_font = ImageFont.load_default()

    panels = [
        ("Radar Candidate Evidence", OUT / "sar_candidate_focus.png", (34, 94, 748, 520)),
        ("Terrain Accessibility", OUT / "tmc2_accessibility_focus.png", (818, 94, 1532, 520)),
        ("Cold-Trap Proxy", OUT / "cold_trap_proxy_focus.png", (34, 586, 748, 912)),
        ("Slope Constraint", OUT / "tmc2_slope_focus.png", (818, 586, 1532, 912)),
    ]
    draw.text((34, 26), "Lunar South Pole Evidence Fusion Board", fill=(235, 243, 245), font=title_font)
    draw.text((1050, 36), "Chandrayaan-2 DFSAR + TMC-2 + OHRC", fill=(132, 206, 196), font=small_font)
    for label, path, box in panels:
        x0, y0, x1, y1 = box
        draw.rounded_rectangle((x0 - 1, y0 - 1, x1 + 1, y1 + 1), radius=10, outline=(56, 76, 88), width=2)
        img = Image.open(path).convert("RGB")
        img.thumbnail((x1 - x0, y1 - y0 - 42), Image.Resampling.LANCZOS)
        board.paste(img, (x0 + (x1 - x0 - img.width) // 2, y0 + 16))
        draw.text((x0 + 18, y1 - 34), label, fill=(230, 238, 240), font=label_font)
    board.save(OUT / "fusion_board.png", quality=95)


def main() -> None:
    for name, src in SOURCES.items():
        focus_image(src, OUT / f"{name}.png")
        print(OUT / f"{name}.png")
    make_fusion_board()
    print(OUT / "fusion_board.png")


if __name__ == "__main__":
    main()
