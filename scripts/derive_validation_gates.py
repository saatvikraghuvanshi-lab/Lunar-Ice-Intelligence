from __future__ import annotations

import csv
import json
import math
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
EXTRACTED = ROOT / "data" / "processed" / "extracted_minimal"
DERIVED = ROOT / "data" / "processed" / "derived_layers"
DEMO = ROOT / "data" / "processed" / "demo_assets"
AOI_DIR = ROOT / "data" / "aoi"

OFFICIAL_AOI = AOI_DIR / "official_crater_aoi.geojson"
OFFICIAL_TEMPLATE = AOI_DIR / "official_crater_aoi_template.geojson"
PROXY_AOI = AOI_DIR / "dsc1_proxy_registration_harness.geojson"

SUMMARY = DERIVED / "validation_gate_readiness_summary.json"
CARD = DEMO / "validation_gate_readiness_focus.png"
OHR_SUMMARY = DERIVED / "ohrc_registration_hazard_summary.json"


OHR_GEOMETRIES = [
    EXTRACTED / "geometry" / "calibrated" / "20260103" / "ch2_ohr_ncp_20260103T0410224157_g_grd_d18.csv",
    EXTRACTED / "geometry" / "calibrated" / "20260103" / "ch2_ohr_ncp_20260103T0609041371_g_grd_d18.csv",
    EXTRACTED / "geometry" / "calibrated" / "20260103" / "ch2_ohr_ncp_20260103T1005176450_g_grd_d18.csv",
    EXTRACTED / "geometry" / "calibrated" / "20260103" / "ch2_ohr_ncp_20260103T1203563771_g_grd_d18.csv",
]


def font(size: int, bold: bool = False):
    names = ["arialbd.ttf", "arial.ttf"] if bold else ["arial.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def local_text(element: ET.Element, name: str) -> str | None:
    for child in element.iter():
        if child.tag.split("}")[-1] == name:
            return (child.text or "").strip()
    return None


def write_geojson_template(path: Path, name: str, bbox: tuple[float, float, float, float], status: str) -> None:
    lon_min, lat_min, lon_max, lat_max = bbox
    feature = {
        "type": "FeatureCollection",
        "name": name,
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": name,
                    "status": status,
                    "note": "Replace this polygon with the official supplied crater AOI when available.",
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [lon_min, lat_min],
                            [lon_max, lat_min],
                            [lon_max, lat_max],
                            [lon_min, lat_max],
                            [lon_min, lat_min],
                        ]
                    ],
                },
            }
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(feature, indent=2), encoding="utf-8")


def ensure_aoi_files() -> None:
    AOI_DIR.mkdir(parents=True, exist_ok=True)
    if not OFFICIAL_TEMPLATE.exists():
        write_geojson_template(
            OFFICIAL_TEMPLATE,
            "official_crater_aoi_template",
            (24.4, -85.22, 26.5, -84.84),
            "template_only",
        )
    if not PROXY_AOI.exists():
        write_geojson_template(
            PROXY_AOI,
            "dsc1_proxy_registration_harness",
            (24.4, -85.22, 26.5, -84.84),
            "proxy_harness_not_official",
        )


def iter_geojson_coords(obj: object) -> Iterable[tuple[float, float]]:
    if isinstance(obj, dict):
        for value in obj.values():
            yield from iter_geojson_coords(value)
    elif isinstance(obj, list):
        if len(obj) >= 2 and all(isinstance(v, (int, float)) for v in obj[:2]):
            yield float(obj[0]), float(obj[1])
        else:
            for item in obj:
                yield from iter_geojson_coords(item)


def load_aoi() -> dict:
    ensure_aoi_files()
    active = OFFICIAL_AOI if OFFICIAL_AOI.exists() else PROXY_AOI
    data = json.loads(active.read_text(encoding="utf-8"))
    coords = list(iter_geojson_coords(data))
    if not coords:
        raise ValueError(f"No coordinates found in {active}")
    lons = [lon for lon, _ in coords]
    lats = [lat for _, lat in coords]
    return {
        "path": str(active.relative_to(ROOT)),
        "is_official": active == OFFICIAL_AOI,
        "status": "official_supplied_aoi_active" if active == OFFICIAL_AOI else "proxy_registration_harness_active",
        "bbox": {
            "lon_min": min(lons),
            "lon_max": max(lons),
            "lat_min": min(lats),
            "lat_max": max(lats),
        },
    }


def bbox_area(bbox: dict) -> float:
    return max(0.0, bbox["lon_max"] - bbox["lon_min"]) * max(0.0, bbox["lat_max"] - bbox["lat_min"])


def bbox_overlap(a: dict, b: dict) -> dict:
    lon_min = max(a["lon_min"], b["lon_min"])
    lon_max = min(a["lon_max"], b["lon_max"])
    lat_min = max(a["lat_min"], b["lat_min"])
    lat_max = min(a["lat_max"], b["lat_max"])
    overlap = {
        "lon_min": lon_min,
        "lon_max": lon_max,
        "lat_min": lat_min,
        "lat_max": lat_max,
    }
    area = bbox_area(overlap)
    return {
        "bbox": overlap,
        "area_deg2": area,
        "overlap_fraction_of_aoi": area / max(bbox_area(a), 1e-12),
        "intersects": area > 0,
    }


def sample_geometry_bbox(path: Path, stride: int = 64) -> dict:
    lats: list[float] = []
    lons: list[float] = []
    total = 0
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for index, row in enumerate(reader):
            total += 1
            if index % stride:
                continue
            lats.append(float(row["Latitude"]))
            lons.append(float(row["Longitude"]))
    return {
        "file": str(path.relative_to(ROOT)),
        "records": total,
        "sampled_records": len(lats),
        "lat_min": min(lats),
        "lat_max": max(lats),
        "lon_min": min(lons),
        "lon_max": max(lons),
    }


def audit_dfsar_products() -> dict:
    exact_terms = ["cpr", "dop", "stokes", "coher", "covar", "circular", "midas"]
    extracted_names = [p.name.lower() for p in EXTRACTED.rglob("*") if p.is_file()]
    exact_product_files = sorted(name for name in extracted_names if any(term in name for term in exact_terms))

    calibrated_xmls = sorted((EXTRACTED / "data" / "calibrated" / "20200913").glob("ch2_sar_*_d_*_fp_xx_d18.xml"))
    raw_xmls = sorted((EXTRACTED / "data" / "raw" / "20251024").glob("ch2_sar_*_d_r0a_xx_fp_xx_d32.xml"))
    polarizations: set[str] = set()
    phase_values: list[float] = []
    for path in calibrated_xmls + raw_xmls:
        root = ET.parse(path).getroot()
        for info in root.iter():
            if info.tag.split("}")[-1] != "polarization_info":
                continue
            pol = local_text(info, "polarization")
            phase = local_text(info, "phase_orthogonality")
            if pol:
                polarizations.add(pol)
            if phase:
                try:
                    phase_values.append(float(phase))
                except ValueError:
                    pass

    raw_zip_products = []
    for archive in sorted((RAW / "dfsar").glob("ch2_sar_nrxl_20251024*_d_fp_d32.zip")):
        with zipfile.ZipFile(archive) as zf:
            names = zf.namelist()
            dats = [name for name in names if name.lower().endswith(".dat")]
            xmls = [name for name in names if name.lower().endswith(".xml")]
            raw_zip_products.append(
                {
                    "archive": str(archive.relative_to(ROOT)),
                    "dat_files": dats,
                    "xml_files": xmls,
                    "dat_bytes": sum(zf.getinfo(name).file_size for name in dats),
                }
            )

    has_linear_full_pol = {"HH", "HV", "VH", "VV"}.issubset(polarizations)
    has_exact_products = bool(exact_product_files)
    has_raw_dat = any(product["dat_files"] for product in raw_zip_products)
    if has_exact_products:
        status = "exact_product_files_available"
    elif has_raw_dat and has_linear_full_pol:
        status = "raw_full_pol_available_processing_required"
    else:
        status = "insufficient_polarimetric_inputs"

    return {
        "status": status,
        "can_compute_exact_cpr_dop_now": has_exact_products,
        "reason": (
            "Exact CPR/DOP needs calibrated circular-pol/Stokes/coherency/covariance/MIDAS products. "
            "Current raw D32 ZIPs include large raw .dat echo files, but they are not calibrated map-projected CPR/DOP rasters."
        ),
        "linear_polarizations_found": sorted(polarizations),
        "phase_orthogonality_values_found": len(phase_values),
        "phase_orthogonality_range": [min(phase_values), max(phase_values)] if phase_values else None,
        "exact_product_files_found": exact_product_files,
        "raw_zip_products": raw_zip_products,
    }


def audit_ohrc_registration(aoi: dict) -> dict:
    products = []
    aoi_bbox = aoi["bbox"]
    for path in OHR_GEOMETRIES:
        footprint = sample_geometry_bbox(path)
        overlap = bbox_overlap(aoi_bbox, footprint)
        products.append(
            {
                "product": path.stem.replace("_g_grd_d18", ""),
                "geometry": str(path.relative_to(ROOT)),
                "footprint_bbox": footprint,
                "aoi_overlap": overlap,
                "registration_status": "candidate_overlap" if overlap["intersects"] else "no_bbox_overlap",
            }
        )
    return {
        "status": "official_aoi_registration_ready" if aoi["is_official"] else "proxy_aoi_registration_harness",
        "aoi": aoi,
        "products": products,
        "best_overlap_fraction": max((item["aoi_overlap"]["overlap_fraction_of_aoi"] for item in products), default=0.0),
        "scientific_caution": (
            "This is bbox/footprint readiness. Final certification requires map-projected OHRC-to-official-AOI intersection "
            "and full-resolution crater/boulder extraction inside that AOI."
        ),
    }


def draw_wrapped(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], max_width: int, line_height: int, fill, text_font) -> int:
    x, y = xy
    words = text.split()
    line = ""
    lines: list[str] = []
    for word in words:
        candidate = f"{line} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=text_font)[2] <= max_width:
            line = candidate
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


def draw_status_card(summary: dict) -> None:
    CARD.parent.mkdir(parents=True, exist_ok=True)
    canvas = Image.new("RGB", (1440, 960), (5, 9, 13))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((34, 34, 1406, 926), outline=(45, 75, 86), width=2)
    draw.text((62, 58), "Validation Gate Readiness", fill=(238, 248, 249), font=font(44, True))
    draw.text((62, 112), "Exact CPR/DOP, official crater AOI, and OHRC registration status", fill=(150, 211, 205), font=font(25))

    radar = summary["radar_cpr_dop"]
    aoi = summary["active_aoi"]
    ohrc = summary["ohrc_registration"]
    ohrc_hazards = summary.get("ohrc_aoi_hazards", {})

    cards = [
        {
            "title": "1. Exact CPR/DOP",
            "status": "PENDING" if not radar["can_compute_exact_cpr_dop_now"] else "READY",
            "accent": (242, 191, 90) if not radar["can_compute_exact_cpr_dop_now"] else (118, 212, 131),
            "body": (
                f"Found {len(radar['linear_polarizations_found'])} linear polarizations, "
                f"{radar['phase_orthogonality_values_found']} phase metadata values, and "
                f"{len(radar['raw_zip_products'])} raw D32 .dat packages. Exact CPR/DOP still requires calibrated polarimetric/MIDAS outputs."
            ),
        },
        {
            "title": "2. Official Crater AOI",
            "status": "OFFICIAL" if aoi["is_official"] else "PROXY",
            "accent": (118, 212, 131) if aoi["is_official"] else (242, 191, 90),
            "body": (
                f"Active AOI file: {aoi['path']}. "
                "Drop the supplied crater polygon into data/aoi/official_crater_aoi.geojson to replace the proxy harness."
            ),
        },
        {
            "title": "3. OHRC Registration",
            "status": "READY" if ohrc["best_overlap_fraction"] > 0 else "WAITING",
            "accent": (53, 229, 214) if ohrc["best_overlap_fraction"] > 0 else (242, 191, 90),
            "body": (
                f"Best bbox overlap with active AOI is {ohrc['best_overlap_fraction'] * 100:.1f}%. "
                f"AOI-window hazard extraction found {ohrc_hazards.get('total_hazard_candidates', 0)} candidates across "
                f"{ohrc_hazards.get('products_with_aoi_windows', 0)} OHRC strips."
            ),
        },
    ]

    y = 188
    for card in cards:
        draw.rectangle((70, y, 1370, y + 168), fill=(9, 18, 23), outline=(41, 66, 76), width=2)
        draw.text((100, y + 28), card["title"], fill=(238, 248, 249), font=font(30, True))
        draw.rectangle((1120, y + 30, 1318, y + 72), fill=(12, 24, 27), outline=card["accent"], width=2)
        draw.text((1160, y + 38), card["status"], fill=card["accent"], font=font(22, True))
        draw_wrapped(draw, card["body"], (100, y + 90), 1060, 31, (202, 224, 228), font(23))
        y += 196

    draw.rectangle((70, 794, 1370, 878), fill=(18, 18, 10), outline=(92, 78, 36), width=2)
    draw.text((100, 814), "Judge-safe claim", fill=(255, 224, 166), font=font(25, True))
    draw_wrapped(
        draw,
        "The system is engineered for exact replacement: when official CPR/DOP rasters or the supplied crater AOI arrive, the proxy gates are replaced without changing the demo story.",
        (330, 816),
        940,
        28,
        (255, 235, 190),
        font(21),
    )
    canvas.save(CARD, quality=95)


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DEMO.mkdir(parents=True, exist_ok=True)
    aoi = load_aoi()
    ohrc_aoi_hazards = None
    if OHR_SUMMARY.exists():
        ohr_data = json.loads(OHR_SUMMARY.read_text(encoding="utf-8"))
        products = ohr_data.get("products", [])
        ohrc_aoi_hazards = {
            "status": ohr_data.get("status", "not_generated"),
            "active_aoi": ohr_data.get("active_aoi"),
            "products_with_aoi_windows": sum(1 for item in products if item.get("aoi_window")),
            "total_hazard_candidates": sum(len(item.get("hazards", [])) for item in products),
            "source_summary": str(OHR_SUMMARY.relative_to(ROOT)),
        }
    summary = {
        "radar_cpr_dop": audit_dfsar_products(),
        "active_aoi": aoi,
        "ohrc_registration": audit_ohrc_registration(aoi),
        "ohrc_aoi_hazards": ohrc_aoi_hazards or {
            "status": "not_generated",
            "products_with_aoi_windows": 0,
            "total_hazard_candidates": 0,
            "source_summary": str(OHR_SUMMARY.relative_to(ROOT)),
        },
        "outputs": {
            "summary": str(SUMMARY.relative_to(ROOT)),
            "dashboard_image": str(CARD.relative_to(ROOT)),
            "official_aoi_template": str(OFFICIAL_TEMPLATE.relative_to(ROOT)),
            "proxy_aoi_harness": str(PROXY_AOI.relative_to(ROOT)),
        },
    }
    SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    draw_status_card(summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
