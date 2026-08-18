from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


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
    "ohr_0_focus": ROOT
    / "data"
    / "processed"
    / "quicklooks"
    / "ch2_ohr_ncp_20260103T0410224157_b_brw_d18_quicklook.png",
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
    "ohr_c_focus": ROOT
    / "data"
    / "processed"
    / "quicklooks"
    / "ch2_ohr_ncp_20260103T1203563771_b_brw_d18_quicklook.png",
}


def font(size: int, bold: bool = False):
    names = ["arialbd.ttf", "arial.ttf"] if bold else ["arial.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


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


def make_ohr_focus(src: Path, dest: Path, label: str, size: tuple[int, int] = (1440, 960)) -> None:
    img = Image.open(src).convert("RGB")
    bbox = find_content_bbox(img)
    content = img.crop(bbox)
    # OHRC browse strips are very tall and narrow. Show a representative
    # enlarged section instead of shrinking the whole strip into a speck.
    section_h = min(content.height, max(1400, int(content.height * 0.28)))
    y0 = max(0, int(content.height * 0.34) - section_h // 2)
    section = content.crop((0, y0, content.width, min(content.height, y0 + section_h)))
    section = ImageEnhance.Contrast(section).enhance(1.25)
    section.thumbnail((410, 680), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", size, (3, 6, 10))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((42, 42, 1398, 918), outline=(45, 75, 86), width=2)
    draw.text((72, 70), f"{label} - Enlarged OHRC Hazard Context", fill=(238, 248, 249), font=font(36, bold=True))
    draw.text((72, 118), "Representative crop from the downloaded 0.25 m-class OHRC browse strip", fill=(150, 211, 205), font=font(23))

    x = 160
    y = 185
    draw.rectangle((x - 24, y - 24, x + section.width + 24, y + section.height + 24), fill=(7, 13, 17), outline=(53, 229, 214), width=3)
    canvas.paste(section, (x, y))

    panel_x = 700
    draw.rectangle((panel_x, 210, 1330, 740), fill=(8, 17, 22), outline=(45, 75, 86), width=2)
    draw.text((panel_x + 30, 246), "What this layer is for", fill=(53, 229, 214), font=font(30, bold=True))
    bullets = [
        "Visual inspection of crater rims, boulder-like spots, and rough local texture.",
        "Used as hazard context before accepting a landing or rover traverse corridor.",
        "Not yet a registered AOI proof; final overlap needs map-projected footprint intersection.",
    ]
    yy = 310
    for bullet in bullets:
        draw.text((panel_x + 34, yy), "-", fill=(242, 191, 90), font=font(27))
        words = bullet.split()
        line = ""
        lines = []
        for word in words:
            test = f"{line} {word}".strip()
            if draw.textbbox((0, 0), test, font=font(24))[2] <= 540:
                line = test
            else:
                lines.append(line)
                line = word
        lines.append(line)
        for line in lines:
            draw.text((panel_x + 68, yy), line, fill=(222, 236, 240), font=font(24))
            yy += 32
        yy += 22
    draw.rectangle((panel_x, 780, 1330, 850), fill=(18, 18, 10), outline=(92, 78, 36), width=2)
    draw.text((panel_x + 26, 802), "Dashboard claim: OHRC context + hazard proxy, not final certification.", fill=(255, 224, 166), font=font(21))
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, quality=95)


def make_sar_browse_focus(src: Path, dest: Path, size: tuple[int, int] = (1440, 960)) -> None:
    img = Image.open(src).convert("RGB")
    bbox = find_content_bbox(img)
    content = img.crop(bbox)
    # The DFSAR browse is a low-resolution quicklook. Use nearest-neighbor
    # enlargement so it reads as a pixel QA layer instead of a blurred photo.
    content = ImageEnhance.Contrast(content).enhance(1.45)
    target_h = 560
    scale = max(1, target_h // max(1, content.height))
    enlarged = content.resize((content.width * scale, content.height * scale), Image.Resampling.NEAREST)
    enlarged.thumbnail((470, 690), Image.Resampling.NEAREST)

    canvas = Image.new("RGB", size, (3, 6, 10))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((42, 42, 1398, 918), outline=(45, 75, 86), width=2)
    draw.text((72, 70), "DFSAR Radar Browse Context", fill=(238, 248, 249), font=font(44, bold=True))
    draw.text((72, 124), "Low-resolution quicklook for scene QA; evidence ranking uses derived SAR layers", fill=(150, 211, 205), font=font(28))

    x = 150
    y = 210
    draw.rectangle((x - 30, y - 30, x + enlarged.width + 30, y + enlarged.height + 30), fill=(0, 0, 0), outline=(53, 229, 214), width=3)
    canvas.paste(enlarged, (x, y))
    draw_wrapped(
        draw,
        f"Browse quicklook enlarged {scale}x; crisp pixels show source limits.",
        (x, y + enlarged.height + 32),
        420,
        27,
        (255, 224, 166),
        font(22),
    )

    panel_x = 700
    draw.rectangle((panel_x, 214, 1330, 740), fill=(8, 17, 22), outline=(45, 75, 86), width=2)
    draw.text((panel_x + 30, 250), "How to use this view", fill=(53, 229, 214), font=font(34, bold=True))
    bullets = [
        "Use for visual QA and payload context only.",
        "Do not rank candidate ice from this low-resolution browse image.",
        "Use SAR Candidate Evidence, CPR/DOP Gate, and DFSAR Audit for science logic.",
    ]
    yy = 320
    for bullet in bullets:
        draw.text((panel_x + 34, yy), "-", fill=(242, 191, 90), font=font(31))
        yy = draw_wrapped(draw, bullet, (panel_x + 72, yy), 500, 37, (222, 236, 240), font(29)) + 24
    draw.rectangle((panel_x, 770, 1330, 870), fill=(18, 18, 10), outline=(92, 78, 36), width=2)
    draw_wrapped(
        draw,
        "Judge-safe claim: browse confirms scene context; derived DFSAR products drive evidence.",
        (panel_x + 26, 790),
        560,
        30,
        (255, 224, 166),
        font(24),
    )
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


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    max_width: int,
    line_height: int,
    fill: tuple[int, int, int],
    text_font,
) -> int:
    x, y = xy
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        test = f"{line} {word}".strip()
        if draw.textbbox((0, 0), test, font=text_font)[2] <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    for line in lines:
        draw.text((x, y), line, fill=fill, font=text_font)
        y += line_height
    return y


def make_faustini_reference() -> None:
    canvas = Image.new("RGB", (1440, 960), (4, 7, 10))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((42, 42, 1398, 918), outline=(45, 75, 86), width=2)
    draw.text((70, 72), "Faustini / F2 Reference Target", fill=(238, 248, 249), font=font(48, bold=True))
    draw.text(
        (70, 124),
        "Mentor framing for the official doubly shadowed crater objective",
        fill=(150, 211, 205),
        font=font(28),
    )

    # Left: crater/PSR schematic.
    draw.ellipse((112, 230, 532, 650), fill=(24, 28, 30), outline=(130, 144, 150), width=3)
    draw.ellipse((212, 320, 430, 538), fill=(0, 0, 0), outline=(84, 92, 96), width=2)
    draw.arc((212, 320, 430, 538), start=238, end=42, fill=(239, 239, 230), width=20)
    draw.arc((212, 320, 430, 538), start=80, end=190, fill=(125, 130, 130), width=9)
    draw.line((430, 370, 696, 232), fill=(242, 191, 90), width=5)
    draw.line((430, 486, 696, 628), fill=(242, 191, 90), width=5)
    draw.rectangle((690, 206, 1248, 656), fill=(8, 16, 20), outline=(242, 191, 90), width=2)
    draw.text((724, 238), "Reference crater pattern", fill=(255, 224, 166), font=font(36, bold=True))
    ref_rows = [
        ("Location", "Faustini permanently shadowed region"),
        ("Target", "F2-style ~1.1 km doubly shadowed crater"),
        ("Morphology", "lobate rim / flow-like rim appearance"),
        ("Radar cue", "high CPR (> 1) and low DOP (< 0.13)"),
        ("Mission use", "landing-to-excavation planning target"),
    ]
    yy = 300
    for label, value in ref_rows:
        draw.text((724, yy), label.upper(), fill=(83, 229, 218), font=font(21, bold=True))
        yy = draw_wrapped(draw, value, (862, yy - 4), 330, 31, (230, 240, 242), font(25))
        yy += 16

    draw.text((132, 680), "Current dashboard target", fill=(83, 229, 218), font=font(34, bold=True))
    current = (
        "DSC-1 is a Faustini-class proxy until the supplied crater AOI arrives. "
        "The app keeps the exact CPR/DOP and OHRC registration caveats visible instead of overclaiming confirmation."
    )
    draw_wrapped(draw, current, (132, 728), 1120, 38, (226, 238, 241), font(29))
    draw.rectangle((132, 826, 1254, 884), fill=(18, 18, 10), outline=(92, 78, 36), width=2)
    draw_wrapped(
        draw,
        "Judge takeaway: matches the mentor target model while separating reference evidence from current proxy evidence.",
        (158, 842),
        1050,
        25,
        (255, 224, 166),
        font(20),
    )
    canvas.save(OUT / "faustini_f2_reference_focus.png", quality=95)


def make_expected_solution_matrix() -> None:
    canvas = Image.new("RGB", (1440, 960), (4, 7, 10))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((42, 42, 1398, 918), outline=(45, 75, 86), width=2)
    draw.text((70, 62), "Mentor Expected Solution Tracker", fill=(238, 248, 249), font=font(48, bold=True))
    draw.text((70, 122), "Problem-statement steps mapped to prototype outputs", fill=(150, 211, 205), font=font(30))

    rows = [
        ("1", "Map PSR and doubly shadowed craters", "Cold-trap + shadow proxy, DSC-1/Faustini-class target", "proxy"),
        ("2", "Compute CPR/DOP and apply CPR > 1, DOP < 0.13", "Threshold gate + DFSAR audit; exact products pending", "audited"),
        ("3", "Study morphology, slopes, boulders, roughness with OHRC", "OHRC footprint audit + browse-scale crater/boulder candidates", "partial"),
        ("4", "Evaluate terrain safety and proximity to ice-bearing regions", "TMC-2 slope/accessibility + LOLA validation + candidate ranking", "ready"),
        ("5", "Design optimal safe path with solar constraints", "Solar-aware A* route from LZ-A to SCI-B/DSC-1", "ready"),
        ("6", "Estimate top 5 m ice concentration and volume", "Low/medium/high water-equivalent scenarios with caveats", "ready"),
    ]
    colors = {
        "ready": (118, 212, 131),
        "partial": (242, 191, 90),
        "audited": (242, 191, 90),
        "proxy": (49, 214, 204),
    }
    y = 190
    for num, requirement, output, status in rows:
        draw.rectangle((78, y, 1362, y + 92), fill=(8, 16, 20), outline=(38, 58, 68), width=2)
        draw.ellipse((104, y + 22, 154, y + 72), fill=(16, 34, 39), outline=colors[status], width=2)
        draw.text((120, y + 31), num, fill=(238, 248, 249), font=font(26, bold=True))
        draw.text((180, y + 16), requirement, fill=(238, 248, 249), font=font(31, bold=True))
        draw_wrapped(draw, output, (180, y + 56), 780, 30, (170, 206, 213), font(24))
        draw.rectangle((1118, y + 29, 1286, y + 65), fill=(12, 24, 27), outline=colors[status], width=2)
        draw.text((1140, y + 34), status.upper(), fill=colors[status], font=font(23, bold=True))
        y += 106
    draw.text((82, 842), "Mission-planner answer", fill=(83, 229, 218), font=font(30, bold=True))
    draw_wrapped(
        draw,
        "Where to land, where to drive, where to excavate, and how much ice may be available are shown as auditable prototype outputs.",
        (392, 842),
        820,
        31,
        (226, 238, 241),
        font(26),
    )
    canvas.save(OUT / "mentor_expected_solution_focus.png", quality=95)


def make_radar_reference_comparison() -> None:
    canvas = Image.new("RGB", (1440, 960), (4, 7, 10))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((42, 42, 1398, 918), outline=(45, 75, 86), width=2)
    draw.text((70, 66), "CPR/DOP Reference vs Current DFSAR Package", fill=(238, 248, 249), font=font(44, bold=True))
    draw.text((70, 122), "Exact polarimetric validation target vs audited proxy evidence", fill=(150, 211, 205), font=font(30))

    draw.rectangle((94, 188, 650, 768), fill=(8, 16, 20), outline=(45, 75, 86), width=2)
    draw.text((128, 224), "Reference detection", fill=(255, 224, 166), font=font(36, bold=True))
    ref = [
        "Circular Polarization Ratio: CPR > 1",
        "Degree of Polarization: DOP < 0.13",
        "F2-style crater: ~1.1 km diameter",
        "Interpretation: candidate subsurface ice only after rough-terrain filtering",
    ]
    yy = 288
    for item in ref:
        draw.text((132, yy), "+", fill=(83, 229, 218), font=font(30, bold=True))
        yy = draw_wrapped(draw, item, (174, yy), 400, 36, (230, 240, 242), font(29)) + 14

    draw.rectangle((790, 188, 1346, 768), fill=(8, 16, 20), outline=(45, 75, 86), width=2)
    draw.text((824, 224), "Current evidence state", fill=(83, 229, 218), font=font(36, bold=True))
    current = [
        "HH, HV, VH, VV intensity rasters present",
        "16 phase-orthogonality metadata values present",
        "No exact CPR/DOP/Stokes/coherency/covariance products found",
        "Dashboard keeps threshold gate visible and labels output as proxy",
    ]
    yy = 288
    for item in current:
        draw.text((828, yy), "+", fill=(242, 191, 90), font=font(30, bold=True))
        yy = draw_wrapped(draw, item, (870, yy), 390, 36, (230, 240, 242), font(29)) + 14

    draw.line((692, 240, 746, 240), fill=(83, 229, 218), width=4)
    draw.polygon([(746, 240), (724, 228), (724, 252)], fill=(83, 229, 218))
    draw.text((632, 286), "honest", fill=(242, 191, 90), font=font(27, bold=True))
    draw.text((606, 324), "gap closure", fill=(242, 191, 90), font=font(27, bold=True))
    draw.rectangle((108, 818, 1330, 884), fill=(18, 18, 10), outline=(92, 78, 36), width=2)
    draw_wrapped(
        draw,
        "Upgrade path: drop in official CPR/DOP or MIDAS outputs; the same threshold gate becomes an exact validation layer.",
        (136, 836),
        1140,
        26,
        (255, 224, 166),
        font(21),
    )
    canvas.save(OUT / "radar_reference_comparison_focus.png", quality=95)


def main() -> None:
    for name, src in SOURCES.items():
        if name == "sar_browse_focus":
            make_sar_browse_focus(src, OUT / f"{name}.png")
        elif name == "ohr_0_focus":
            make_ohr_focus(src, OUT / f"{name}.png", "OHRC-0")
        elif name == "ohr_a_focus":
            make_ohr_focus(src, OUT / f"{name}.png", "OHRC-A")
        elif name == "ohr_b_focus":
            make_ohr_focus(src, OUT / f"{name}.png", "OHRC-B")
        elif name == "ohr_c_focus":
            make_ohr_focus(src, OUT / f"{name}.png", "OHRC-C")
        else:
            focus_image(src, OUT / f"{name}.png")
        print(OUT / f"{name}.png")
    make_fusion_board()
    print(OUT / "fusion_board.png")
    make_faustini_reference()
    make_expected_solution_matrix()
    make_radar_reference_comparison()
    print(OUT / "faustini_f2_reference_focus.png")
    print(OUT / "mentor_expected_solution_focus.png")
    print(OUT / "radar_reference_comparison_focus.png")


if __name__ == "__main__":
    main()
