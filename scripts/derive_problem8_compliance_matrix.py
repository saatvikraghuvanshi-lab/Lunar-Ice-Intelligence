from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "data" / "processed" / "demo_assets"
DERIVED = ROOT / "data" / "processed" / "derived_layers"
OUTPUT = DEMO / "problem8_compliance_matrix_focus.png"
SUMMARY = DERIVED / "problem8_compliance_matrix_summary.json"


ROWS = [
    {
        "requirement": "Map PSRs and doubly shadowed craters",
        "status": "PROXY READY",
        "score": 78,
        "evidence": "DSC-1 target from cold-trap, shadow, illumination, slope, and accessibility layers.",
        "fix": "Replace DSC-1 proxy with official supplied crater AOI when released.",
    },
    {
        "requirement": "Compute CPR > 1 and DOP < 0.13",
        "status": "MAJOR GAP",
        "score": 45,
        "evidence": "Full-pol intensity products and raw D32 candidates are present; exact CPR/DOP products are not.",
        "fix": "Run MIDAS/calibrated polarimetry or ingest supplied CPR/DOP rasters.",
    },
    {
        "requirement": "Study OHRC crater/boulder morphology",
        "status": "PARTIAL",
        "score": 68,
        "evidence": "Four OHRC strips have browse-scale candidate hazard extraction and footprint audit.",
        "fix": "Map-project OHRC strips to official AOI and extract full-resolution boulder/crater hazards.",
    },
    {
        "requirement": "Evaluate terrain safety",
        "status": "READY",
        "score": 86,
        "evidence": "TMC-2 DTM slope/accessibility, rough-terrain rejection, and LOLA independent validation.",
        "fix": "Use official crater footprint to re-score final LZ candidates.",
    },
    {
        "requirement": "Design optimal safe rover traverse",
        "status": "READY",
        "score": 82,
        "evidence": "A* route over accessibility, cold-trap, and illumination/power penalty layers.",
        "fix": "Add ephemeris-derived solar-power windows for final route scheduling.",
    },
    {
        "requirement": "Estimate top 0-5 m ice volume",
        "status": "SCENARIO READY",
        "score": 72,
        "evidence": "Area x 5 m x ice-fraction scenarios reported with low/medium/high assumptions.",
        "fix": "Tie volume to exact CPR/DOP candidate mask and dielectric/backscatter model.",
    },
]


def font(size: int, bold: bool = False):
    names = ["arialbd.ttf" if bold else "arial.ttf", "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def wrap(draw: ImageDraw.ImageDraw, text: str, max_width: int, fnt: ImageFont.ImageFont) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textbbox((0, 0), trial, font=fnt)[2] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def status_color(status: str) -> tuple[int, int, int]:
    return {
        "READY": (118, 212, 131),
        "PROXY READY": (242, 191, 90),
        "SCENARIO READY": (242, 191, 90),
        "PARTIAL": (255, 224, 166),
        "MAJOR GAP": (255, 108, 108),
    }.get(status, (150, 211, 205))


def main() -> None:
    DEMO.mkdir(parents=True, exist_ok=True)
    DERIVED.mkdir(parents=True, exist_ok=True)

    canvas = Image.new("RGB", (1600, 1100), (5, 9, 13))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((34, 34, 1566, 1066), outline=(45, 75, 86), width=2)
    draw.text((58, 58), "Problem Statement 8 Compliance Matrix", fill=(238, 248, 249), font=font(42, True))
    draw.text(
        (58, 112),
        "mentor expected solution vs current prototype status: what is solved, what is proxy-level, and what must be closed",
        fill=(150, 211, 205),
        font=font(22),
    )

    x0, y0 = 58, 170
    col = [0, 410, 590, 1010, 0]
    headers = [("Requirement", 0), ("Status", 410), ("Current evidence", 590), ("How to close", 1010)]
    draw.rectangle((x0, y0, 1542, y0 + 46), fill=(9, 18, 23), outline=(41, 66, 76), width=2)
    for label, offset in headers:
        draw.text((x0 + offset + 18, y0 + 13), label, fill=(238, 248, 249), font=font(19, True))

    row_h = 122
    for idx, row in enumerate(ROWS):
        y = y0 + 46 + idx * row_h
        bg = (7, 13, 17) if idx % 2 == 0 else (9, 18, 23)
        draw.rectangle((x0, y, 1542, y + row_h), fill=bg, outline=(30, 51, 59), width=1)
        yy = y + 18
        for line in wrap(draw, row["requirement"], 365, font(20, True)):
            draw.text((x0 + 18, yy), line, fill=(238, 248, 249), font=font(20, True))
            yy += 26

        color = status_color(row["status"])
        draw.rectangle((x0 + 428, y + 20, x0 + 562, y + 54), fill=(18, 18, 10), outline=color, width=2)
        draw.text((x0 + 440, y + 29), row["status"], fill=color, font=font(14, True))
        draw.text((x0 + 428, y + 72), f"{row['score']} / 100", fill=(255, 198, 79), font=font(25, True))

        yy = y + 16
        for line in wrap(draw, row["evidence"], 380, font(17)):
            draw.text((x0 + 608, yy), line, fill=(190, 218, 222), font=font(17))
            yy += 24

        yy = y + 16
        for line in wrap(draw, row["fix"], 430, font(17)):
            draw.text((x0 + 1028, yy), line, fill=(255, 224, 166) if row["status"] != "READY" else (181, 255, 250), font=font(17))
            yy += 24

    draw.rectangle((58, 968, 1542, 1032), fill=(12, 15, 10), outline=(92, 78, 36), width=2)
    draw.text((86, 986), "Biggest missing piece:", fill=(255, 224, 166), font=font(20, True))
    draw.text(
        (310, 986),
        "exact calibrated CPR/DOP on the official supplied doubly shadowed crater AOI.",
        fill=(238, 248, 249),
        font=font(20),
    )

    canvas.save(OUTPUT, quality=95)
    SUMMARY.write_text(json.dumps({"rows": ROWS, "image": str(OUTPUT.relative_to(ROOT))}, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT), "summary": str(SUMMARY)}, indent=2))


if __name__ == "__main__":
    main()
