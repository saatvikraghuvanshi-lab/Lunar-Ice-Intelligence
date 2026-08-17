from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
EXTRACTED = ROOT / "data" / "processed" / "extracted_minimal"
DERIVED = ROOT / "data" / "processed" / "derived_layers"
DEMO = ROOT / "data" / "processed" / "demo_assets"
SUMMARY = DERIVED / "dfsar_polarimetry_audit_summary.json"
CARD = DEMO / "dfsar_polarimetry_audit_focus.png"


def text_of(element: ET.Element, local_name: str) -> str | None:
    for child in element.iter():
        if child.tag.split("}")[-1] == local_name:
            return (child.text or "").strip()
    return None


def read_xml(path: Path) -> dict:
    root = ET.parse(path).getroot()
    product = {
        "file": str(path.relative_to(ROOT)),
        "title": text_of(root, "title"),
        "start": text_of(root, "start_date_time"),
        "stop": text_of(root, "stop_date_time"),
        "num_polarizations": text_of(root, "num_polarizations"),
        "polarizations": [],
        "phase_orthogonality": [],
    }

    for info in root.iter():
        if info.tag.split("}")[-1] != "polarization_info":
            continue
        pol = text_of(info, "polarization")
        phase = text_of(info, "phase_orthogonality")
        if pol:
            product["polarizations"].append(pol)
        if phase:
            try:
                product["phase_orthogonality"].append(float(phase))
            except ValueError:
                product["phase_orthogonality"].append(phase)
    return product


def infer_product_files() -> list[str]:
    files = [p.name.lower() for p in EXTRACTED.rglob("*") if p.is_file()]
    signals = [
        name
        for name in files
        if any(token in name for token in ["cpr", "dop", "stokes", "coher", "covar", "complex", "s4"])
    ]
    return sorted(signals)


def make_card(summary: dict) -> None:
    DEMO.mkdir(parents=True, exist_ok=True)
    canvas = Image.new("RGB", (1440, 960), (5, 9, 13))
    draw = ImageDraw.Draw(canvas)
    try:
        title_font = ImageFont.truetype("arial.ttf", 36)
        head_font = ImageFont.truetype("arial.ttf", 24)
        body_font = ImageFont.truetype("arial.ttf", 21)
        mono_font = ImageFont.truetype("consola.ttf", 20)
    except OSError:
        title_font = head_font = body_font = mono_font = ImageFont.load_default()

    draw.rectangle((34, 34, 1406, 926), outline=(45, 75, 86), width=2)
    draw.text((58, 58), "DFSAR Polarimetry Audit", fill=(238, 248, 249), font=title_font)
    draw.text((58, 104), "what is ready now vs. what exact CPR/DOP still needs", fill=(255, 224, 166), font=body_font)

    cards = [
        ("Available", f"{summary['available_polarizations']} linear-pol intensity rasters: HH, HV, VH, VV"),
        ("Metadata", f"{summary['phase_terms_found']} phase-orthogonality values found in PDS4 labels"),
        ("Missing", "No CPR/DOP/Stokes/coherency/covariance product files found in current extracted set"),
        ("Decision", "Keep CPR/DOP gate visible, but label it threshold-ready until official polarimetric outputs arrive"),
    ]
    y = 172
    for label, value in cards:
        draw.rectangle((58, y, 1382, y + 116), fill=(9, 18, 23), outline=(41, 66, 76), width=2)
        draw.text((82, y + 22), label, fill=(53, 229, 214), font=head_font)
        draw.text((82, y + 62), value, fill=(222, 236, 240), font=body_font)
        y += 142

    draw.rectangle((58, 746, 1382, 884), fill=(18, 18, 10), outline=(92, 78, 36), width=2)
    draw.text((82, 772), "Problem threshold target", fill=(255, 224, 166), font=head_font)
    draw.text((82, 816), "CPR > 1 AND DOP < 0.13", fill=(255, 240, 177), font=mono_font)
    draw.text((470, 816), "exact computation pending calibrated phase/coherency-aware products", fill=(185, 211, 214), font=body_font)
    canvas.save(CARD, quality=95)


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    xmls = sorted((EXTRACTED / "data" / "calibrated" / "20200913").glob("ch2_sar_*_d_*_fp_xx_d18.xml"))
    products = [read_xml(path) for path in xmls]
    polarizations = sorted({pol for product in products for pol in product["polarizations"]})
    phase_values = [phase for product in products for phase in product["phase_orthogonality"]]
    exact_files = infer_product_files()

    summary = {
        "status": "threshold-ready audit complete; exact CPR/DOP not computed from current files",
        "available_polarizations": len(polarizations),
        "polarizations": polarizations,
        "phase_terms_found": len(phase_values),
        "phase_orthogonality_range": [min(phase_values), max(phase_values)] if phase_values else None,
        "exact_cpr_dop_product_files_found": exact_files,
        "current_limitation": (
            "The extracted DFSAR rasters support HH/HV/VH/VV intensity-ratio proxy screening. "
            "Exact CPR and DOP should be generated from calibrated circular-pol, Stokes, coherency, covariance, "
            "or official MIDAS-style polarimetric outputs when supplied."
        ),
        "products": products,
        "dashboard_image": str(CARD.relative_to(ROOT)),
    }
    SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    make_card(summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
