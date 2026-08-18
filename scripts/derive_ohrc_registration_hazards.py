from __future__ import annotations

import csv
import json
import math
import xml.etree.ElementTree as ET
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
EXTRACTED = ROOT / "data" / "processed" / "extracted_minimal"
AOI_DIR = ROOT / "data" / "aoi"
TMC_XML = (
    ROOT
    / "data"
    / "processed"
    / "extracted_tmc2_south_pole"
    / "data"
    / "derived"
    / "20231203"
    / "ch2_tmc_ndn_20231203T0019079527_d_dtm_d18.xml"
)
DERIVED = ROOT / "data" / "processed" / "derived_layers"
DEMO = ROOT / "data" / "processed" / "demo_assets"
SUMMARY = DERIVED / "ohrc_registration_hazard_summary.json"
FOOTPRINT_CARD = DEMO / "ohrc_footprint_registration_focus.png"
HAZARD_CARD = DEMO / "ohrc_hazard_extraction_focus.png"
OFFICIAL_AOI = AOI_DIR / "official_crater_aoi.geojson"
PROXY_AOI = AOI_DIR / "dsc1_proxy_registration_harness.geojson"

OHR_PRODUCTS = [
    {
        "id": "OHRC-0",
        "product": "ch2_ohr_ncp_20260103T0410224157",
        "browse": EXTRACTED / "browse" / "calibrated" / "20260103" / "ch2_ohr_ncp_20260103T0410224157_b_brw_d18.png",
        "geometry": EXTRACTED / "geometry" / "calibrated" / "20260103" / "ch2_ohr_ncp_20260103T0410224157_g_grd_d18.csv",
    },
    {
        "id": "OHRC-A",
        "product": "ch2_ohr_ncp_20260103T0609041371",
        "browse": EXTRACTED / "browse" / "calibrated" / "20260103" / "ch2_ohr_ncp_20260103T0609041371_b_brw_d18.png",
        "geometry": EXTRACTED / "geometry" / "calibrated" / "20260103" / "ch2_ohr_ncp_20260103T0609041371_g_grd_d18.csv",
    },
    {
        "id": "OHRC-B",
        "product": "ch2_ohr_ncp_20260103T1005176450",
        "browse": EXTRACTED / "browse" / "calibrated" / "20260103" / "ch2_ohr_ncp_20260103T1005176450_b_brw_d18.png",
        "geometry": EXTRACTED / "geometry" / "calibrated" / "20260103" / "ch2_ohr_ncp_20260103T1005176450_g_grd_d18.csv",
    },
    {
        "id": "OHRC-C",
        "product": "ch2_ohr_ncp_20260103T1203563771",
        "browse": EXTRACTED / "browse" / "calibrated" / "20260103" / "ch2_ohr_ncp_20260103T1203563771_b_brw_d18.png",
        "geometry": EXTRACTED / "geometry" / "calibrated" / "20260103" / "ch2_ohr_ncp_20260103T1203563771_g_grd_d18.csv",
    },
]


def local_text(element: ET.Element, name: str) -> str | None:
    for child in element.iter():
        if child.tag.split("}")[-1] == name:
            return (child.text or "").strip()
    return None


def tmc_bbox() -> dict:
    root = ET.parse(TMC_XML).getroot()
    values = {}
    for name in [
        "upper_left_latitude",
        "upper_left_longitude",
        "upper_right_latitude",
        "upper_right_longitude",
        "lower_left_latitude",
        "lower_left_longitude",
        "lower_right_latitude",
        "lower_right_longitude",
    ]:
        text = local_text(root, name)
        values[name] = float(text) if text is not None else None
    lats = [values[k] for k in values if k.endswith("latitude") and values[k] is not None]
    lons = [values[k] for k in values if k.endswith("longitude") and values[k] is not None]
    return {
        "lat_min": min(lats),
        "lat_max": max(lats),
        "lon_min": min(lons),
        "lon_max": max(lons),
        "corners": values,
    }


def sample_geometry(path: Path, stride: int = 64) -> dict:
    table = np.genfromtxt(path, delimiter=",", names=True, dtype=None, encoding=None)
    sampled = table[::stride]
    lats = sampled["Latitude"]
    lons = sampled["Longitude"]
    pixels = sampled["Pixel"]
    scans = sampled["Scan"]
    return {
        "records": int(table.shape[0]),
        "sampled_records": len(lats),
        "lat_min": float(np.min(lats)),
        "lat_max": float(np.max(lats)),
        "lon_min": float(np.min(lons)),
        "lon_max": float(np.max(lons)),
        "pixel_min": int(np.min(pixels)),
        "pixel_max": int(np.max(pixels)),
        "scan_min": int(np.min(scans)),
        "scan_max": int(np.max(scans)),
    }


def ranges_overlap(a_min: float, a_max: float, b_min: float, b_max: float) -> bool:
    return max(a_min, b_min) <= min(a_max, b_max)


def iter_geojson_coords(obj: object):
    if isinstance(obj, dict):
        for value in obj.values():
            yield from iter_geojson_coords(value)
    elif isinstance(obj, list):
        if len(obj) >= 2 and all(isinstance(value, (int, float)) for value in obj[:2]):
            yield float(obj[0]), float(obj[1])
        else:
            for item in obj:
                yield from iter_geojson_coords(item)


def load_active_aoi() -> dict:
    active = OFFICIAL_AOI if OFFICIAL_AOI.exists() else PROXY_AOI
    data = json.loads(active.read_text(encoding="utf-8"))
    coords = list(iter_geojson_coords(data))
    if not coords:
        raise ValueError(f"No AOI coordinates found in {active}")
    lons = [lon for lon, _ in coords]
    lats = [lat for _, lat in coords]
    return {
        "path": str(active.relative_to(ROOT)),
        "is_official": active == OFFICIAL_AOI,
        "status": "official_supplied_aoi_active" if active == OFFICIAL_AOI else "proxy_aoi_active",
        "bbox": {
            "lon_min": min(lons),
            "lon_max": max(lons),
            "lat_min": min(lats),
            "lat_max": max(lats),
        },
    }


def aoi_pixel_window(path: Path, aoi_bbox: dict, image_size: tuple[int, int]) -> dict | None:
    table = np.genfromtxt(path, delimiter=",", names=True, dtype=None, encoding=None)
    mask = (
        (table["Longitude"] >= aoi_bbox["lon_min"])
        & (table["Longitude"] <= aoi_bbox["lon_max"])
        & (table["Latitude"] >= aoi_bbox["lat_min"])
        & (table["Latitude"] <= aoi_bbox["lat_max"])
    )
    if not np.any(mask):
        return None
    pixels = table["Pixel"][mask]
    scans = table["Scan"][mask]
    all_pixels = table["Pixel"]
    all_scans = table["Scan"]

    width, height = image_size
    pixel_min = int(np.min(all_pixels))
    pixel_max = int(np.max(all_pixels))
    scan_min = int(np.min(all_scans))
    scan_max = int(np.max(all_scans))
    pixel_scale = (width - 1) / max(1, pixel_max - pixel_min)
    scan_scale = (height - 1) / max(1, scan_max - scan_min)
    scaled_pixels = (pixels - pixel_min) * pixel_scale
    scaled_scans = (scans - scan_min) * scan_scale
    margin_x = max(40, int((float(np.max(scaled_pixels)) - float(np.min(scaled_pixels)) + 1) * 0.2))
    margin_y = max(80, int((float(np.max(scaled_scans)) - float(np.min(scaled_scans)) + 1) * 0.12))
    x1 = max(0, int(np.min(scaled_pixels)) - margin_x)
    x2 = min(width, int(np.max(scaled_pixels)) + margin_x)
    y1 = max(0, int(np.min(scaled_scans)) - margin_y)
    y2 = min(height, int(np.max(scaled_scans)) + margin_y)
    if x2 <= x1:
        x2 = min(width, x1 + max(80, width // 8))
    if y2 <= y1:
        y2 = min(height, y1 + max(160, height // 12))
    return {
        "pixel_window": [x1, y1, x2, y2],
        "matched_geometry_samples": int(mask.sum()),
        "window_fraction_of_browse": ((x2 - x1) * (y2 - y1)) / max(1, width * height),
        "geometry_to_browse_scale": {
            "pixel_scale": pixel_scale,
            "scan_scale": scan_scale,
            "geometry_pixel_max": pixel_max,
            "geometry_scan_max": scan_max,
        },
    }


def normalize_gray(img: Image.Image) -> np.ndarray:
    gray = np.asarray(img.convert("L")).astype("float32")
    lo, hi = np.percentile(gray, [2, 98])
    if hi <= lo:
        hi = lo + 1
    return np.clip((gray - lo) / (hi - lo), 0, 1)


def gradient_score(arr: np.ndarray) -> np.ndarray:
    gx = np.zeros_like(arr)
    gy = np.zeros_like(arr)
    gx[:, 1:-1] = arr[:, 2:] - arr[:, :-2]
    gy[1:-1, :] = arr[2:, :] - arr[:-2, :]
    grad = np.sqrt(gx * gx + gy * gy)
    lo, hi = np.percentile(grad, [80, 99.5])
    if hi <= lo:
        hi = lo + 1
    return np.clip((grad - lo) / (hi - lo), 0, 1)


def connected_components(mask: np.ndarray, limit: int = 24) -> list[dict]:
    visited = np.zeros(mask.shape, dtype=bool)
    h, w = mask.shape
    comps: list[dict] = []
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            if not mask[y, x] or visited[y, x]:
                continue
            q = deque([(x, y)])
            visited[y, x] = True
            xs: list[int] = []
            ys: list[int] = []
            while q:
                cx, cy = q.popleft()
                xs.append(cx)
                ys.append(cy)
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if 0 <= nx < w and 0 <= ny < h and mask[ny, nx] and not visited[ny, nx]:
                        visited[ny, nx] = True
                        q.append((nx, ny))
            area = len(xs)
            if 35 <= area <= 900:
                width = max(xs) - min(xs) + 1
                height = max(ys) - min(ys) + 1
                compact = area / max(1, width * height)
                if compact > 0.18:
                    comps.append(
                        {
                            "x": float(np.mean(xs)),
                            "y": float(np.mean(ys)),
                            "bbox": [min(xs), min(ys), max(xs), max(ys)],
                            "area_px": area,
                            "compactness": compact,
                        }
                    )
    comps.sort(key=lambda item: item["area_px"], reverse=True)
    return comps[:limit]


def content_bbox(arr: np.ndarray) -> tuple[int, int, int, int]:
    mask = arr > max(0.03, float(np.percentile(arr, 68)) * 0.18)
    ys, xs = np.where(mask)
    if len(xs) == 0 or len(ys) == 0:
        return (0, 0, arr.shape[1], arr.shape[0])
    margin_x = max(8, int((xs.max() - xs.min()) * 0.04))
    margin_y = max(8, int((ys.max() - ys.min()) * 0.04))
    return (
        max(0, int(xs.min()) - margin_x),
        max(0, int(ys.min()) - margin_y),
        min(arr.shape[1], int(xs.max()) + margin_x),
        min(arr.shape[0], int(ys.max()) + margin_y),
    )


def hazard_candidates(img: Image.Image, source_window: list[int] | None = None) -> list[dict]:
    offset_x = 0
    offset_y = 0
    if source_window:
        x1, y1, x2, y2 = source_window
        img = img.crop((x1, y1, x2, y2))
        offset_x = x1
        offset_y = y1
    small = img.convert("L")
    small.thumbnail((720, 720), Image.Resampling.LANCZOS)
    arr = normalize_gray(small)
    grad = gradient_score(arr)
    x1, y1, x2, y2 = content_bbox(arr)
    tile = 34
    candidates: list[dict] = []
    for y in range(y1, max(y1 + 1, y2 - tile), tile // 2):
        for x in range(x1, max(x1 + 1, x2 - tile), tile // 2):
            patch = arr[y : y + tile, x : x + tile]
            edge = grad[y : y + tile, x : x + tile]
            if patch.size == 0:
                continue
            brightness = float(patch.mean())
            if brightness < 0.05:
                continue
            local_contrast = float(np.percentile(patch, 92) - np.percentile(patch, 8))
            edge_energy = float(edge.mean())
            dark_core = float(1.0 - np.percentile(patch, 20))
            score = 0.50 * local_contrast + 0.35 * edge_energy + 0.15 * dark_core
            candidates.append(
                {
                    "x": x + tile / 2,
                    "y": y + tile / 2,
                    "bbox": [x, y, x + tile, y + tile],
                    "area_px": int(tile * tile),
                    "compactness": float(local_contrast),
                    "score": score,
                }
            )
    candidates.sort(key=lambda item: item["score"], reverse=True)

    selected: list[dict] = []
    for candidate in candidates:
        if all(abs(candidate["x"] - prev["x"]) > tile * 1.2 or abs(candidate["y"] - prev["y"]) > tile * 1.2 for prev in selected):
            selected.append(candidate)
        if len(selected) >= 24:
            break

    scale_x = img.width / small.width
    scale_y = img.height / small.height
    for comp in selected:
        comp["x"] = comp["x"] * scale_x + offset_x
        comp["y"] = comp["y"] * scale_y + offset_y
        bx1, by1, bx2, by2 = comp["bbox"]
        comp["bbox"] = [
            bx1 * scale_x + offset_x,
            by1 * scale_y + offset_y,
            bx2 * scale_x + offset_x,
            by2 * scale_y + offset_y,
        ]
    return selected


def font(size: int):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def make_footprint_card(products: list[dict], tmc: dict) -> None:
    canvas = Image.new("RGB", (1440, 960), (5, 9, 13))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((34, 34, 1406, 926), outline=(45, 75, 86), width=2)
    draw.text((58, 54), "OHRC Footprint Registration Audit", fill=(238, 248, 249), font=font(42))
    draw.text((58, 108), "zoomed view of downloaded OHRC geometry CSV footprints", fill=(150, 211, 205), font=font(25))

    all_lats = []
    all_lons = []
    for product in products:
        fp = product["footprint"]
        all_lats.extend([fp["lat_min"], fp["lat_max"]])
        all_lons.extend([fp["lon_min"], fp["lon_max"]])
    lon_pad = 0.8
    lat_pad = 0.35
    lon_min = min(all_lons) - lon_pad
    lon_max = max(all_lons) + lon_pad
    lat_min = min(all_lats) - lat_pad
    lat_max = max(all_lats) + lat_pad

    plot = (70, 180, 1005, 710)
    draw.rectangle(plot, fill=(7, 14, 18), outline=(41, 66, 76), width=2)

    def map_xy(lon: float, lat: float) -> tuple[int, int]:
        x = plot[0] + int(((lon - lon_min) / (lon_max - lon_min)) * (plot[2] - plot[0]))
        y = plot[3] - int(((lat - lat_min) / (lat_max - lat_min)) * (plot[3] - plot[1]))
        return x, y

    for step in range(5):
        lat = lat_min + step * (lat_max - lat_min) / 4
        _, y = map_xy(lon_min, lat)
        draw.line((plot[0], y, plot[2], y), fill=(18, 36, 43), width=1)
        draw.text((plot[0] + 10, y - 22), f"{abs(lat):.2f}S", fill=(111, 158, 168), font=font(18))
    for step in range(5):
        lon = lon_min + step * (lon_max - lon_min) / 4
        x, _ = map_xy(lon, lat_min)
        draw.line((x, plot[1], x, plot[3]), fill=(18, 36, 43), width=1)
        draw.text((x - 26, plot[3] + 14), f"{lon:.1f}E", fill=(111, 158, 168), font=font(18))

    colors = [(53, 229, 214), (242, 191, 90), (156, 208, 116), (238, 112, 102)]
    label_offsets = [(18, 18), (18, 58), (18, 98), (18, 138)]
    for index, (product, color) in enumerate(zip(products, colors)):
        bbox = product["footprint"]
        x1, y1 = map_xy(bbox["lon_min"], bbox["lat_max"])
        x2, y2 = map_xy(bbox["lon_max"], bbox["lat_min"])
        draw.rectangle((min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)), outline=color, width=4)
        lx = min(x1, x2) + label_offsets[index][0]
        ly = min(y1, y2) + label_offsets[index][1]
        draw.rectangle((lx - 8, ly - 4, lx + 150, ly + 34), fill=(4, 9, 12), outline=color, width=2)
        draw.text((lx, ly), product["id"], fill=color, font=font(24))

    side_x = 1040
    draw.rectangle((side_x, 180, 1370, 710), fill=(8, 17, 22), outline=(45, 75, 86), width=2)
    draw.text((side_x + 26, 214), "How to read this", fill=(53, 229, 214), font=font(28))
    notes = [
        "Each box is a downloaded OHRC strip footprint derived from its geometry CSV.",
        "All four strips sit inside the TMC-2 south-pole latitude range.",
        "This proves geometry readiness, not final official crater AOI registration.",
    ]
    yy = 270
    for note in notes:
        words = note.split()
        line = ""
        for word in words:
            test = f"{line} {word}".strip()
            if draw.textbbox((0, 0), test, font=font(21))[2] <= 250:
                line = test
            else:
                draw.text((side_x + 30, yy), line, fill=(222, 236, 240), font=font(21))
                yy += 30
                line = word
        draw.text((side_x + 30, yy), line, fill=(222, 236, 240), font=font(21))
        yy += 48
    draw.rectangle((side_x + 26, 604, side_x + 304, 670), fill=(18, 18, 10), outline=(92, 78, 36), width=2)
    draw.text((side_x + 44, 622), "Next: map-project and intersect", fill=(255, 224, 166), font=font(18))
    draw.text((side_x + 44, 646), "with official supplied crater AOI.", fill=(255, 224, 166), font=font(18))

    y = 742
    for product in products:
        overlap = "regional overlap" if product["tmc_lat_overlap"] else "outside TMC latitude span"
        draw.rectangle((58, y, 1382, y + 42), fill=(9, 18, 23), outline=(41, 66, 76), width=1)
        draw.text((82, y + 8), product["id"], fill=(53, 229, 214), font=font(20))
        draw.text((190, y + 8), product["product"], fill=(238, 248, 249), font=font(18))
        draw.text((720, y + 9), f"Lat {product['footprint']['lat_min']:.3f} to {product['footprint']['lat_max']:.3f} | {overlap}", fill=(185, 211, 214), font=font(17))
        y += 48
    canvas.save(FOOTPRINT_CARD, quality=95)


def make_hazard_card(products: list[dict], aoi: dict) -> None:
    canvas = Image.new("RGB", (1600, 1100), (5, 9, 13))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((34, 34, 1566, 1066), outline=(45, 75, 86), width=2)
    draw.text((58, 58), "OHRC AOI-Registered Hazard Extraction", fill=(238, 248, 249), font=font(42))
    draw.text((58, 112), f"candidate crater/boulder zones inside the active AOI window ({aoi['status']})", fill=(150, 211, 205), font=font(23))
    panels = [
        (58, 164, 772, 524),
        (828, 164, 1542, 524),
        (58, 552, 772, 912),
        (828, 552, 1542, 912),
    ]

    def paste_contained(src: Image.Image, target: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        x1, y1, x2, y2 = target
        fitted = ImageOps.contain(src, (x2 - x1, y2 - y1), Image.Resampling.BICUBIC)
        px = x1 + ((x2 - x1) - fitted.width) // 2
        py = y1 + ((y2 - y1) - fitted.height) // 2
        canvas.paste(fitted, (px, py))
        return (px, py, px + fitted.width, py + fitted.height)

    for product, box in zip(products, panels):
        source = Image.open(product["browse_path"]).convert("RGB")
        image_box = (box[0] + 24, box[1] + 22, box[2] - 24, box[3] - 76)
        picks = [0, 1] if len(product["hazards"]) > 1 else [0] if product["hazards"] else []
        tile_gap = 24
        tile_w = (image_box[2] - image_box[0] - tile_gap) // 2
        tile_h = image_box[3] - image_box[1]
        panel_draw = ImageDraw.Draw(canvas)
        for tile_index, hazard_index in enumerate(picks):
            candidate = product["hazards"][hazard_index]
            crop_w = min(source.width, 820)
            crop_h = min(source.height, 1280)
            x1 = max(0, min(source.width - crop_w, int(candidate["x"] - crop_w // 2)))
            y1 = max(0, min(source.height - crop_h, int(candidate["y"] - crop_h // 2)))
            crop_box = (x1, y1, x1 + crop_w, y1 + crop_h)
            crop = source.crop(crop_box)
            crop = ImageEnhance.Contrast(crop).enhance(1.62)
            crop = ImageEnhance.Sharpness(crop).enhance(1.35)
            x = image_box[0] + tile_index * (tile_w + tile_gap)
            y = image_box[1]
            placed = paste_contained(crop, (x, y, x + tile_w, y + tile_h))
            px1, py1, px2, py2 = placed
            cx = px1 + (candidate["x"] - crop_box[0]) * ((px2 - px1) / max(1, crop_w))
            cy = py1 + (candidate["y"] - crop_box[1]) * ((py2 - py1) / max(1, crop_h))
            radius = 20 + min(34, math.sqrt(candidate["area_px"]) * 1.05)
            color = (242, 191, 90) if hazard_index < 6 else (53, 229, 214)
            panel_draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=color, width=3)
            label = "top hazard review" if hazard_index == 0 else "secondary review"
            panel_draw.rectangle((x + 10, y + 10, x + 214, y + 42), fill=(4, 9, 12), outline=color, width=1)
            panel_draw.text((x + 18, y + 17), label, fill=color, font=font(16))
        if not picks:
            draw.text((image_box[0] + 22, image_box[1] + 118), "No AOI-window hazards detected", fill=(255, 224, 166), font=font(24))
        draw.rectangle(box, outline=(45, 75, 86), width=2)
        draw.rectangle((box[0], box[3] - 52, box[2], box[3]), fill=(4, 9, 12))
        window_note = f"{product['aoi_window']['matched_geometry_samples']} AOI samples" if product["aoi_window"] else "no AOI pixel window"
        draw.text((box[0] + 18, box[3] - 38), f"{product['id']} | AOI hazard chips | {len(product['hazards'])} candidates | {window_note}", fill=(238, 248, 249), font=font(20))

    draw.rectangle((58, 948, 1542, 1032), fill=(9, 18, 23), outline=(41, 66, 76), width=2)
    draw.text((86, 972), "Interpretation", fill=(242, 191, 90), font=font(24))
    draw.ellipse((284, 976, 318, 1010), outline=(242, 191, 90), width=3)
    draw.text((334, 976), "top review", fill=(255, 224, 166), font=font(20))
    draw.ellipse((502, 976, 536, 1010), outline=(53, 229, 214), width=3)
    draw.text((552, 976), "secondary review", fill=(181, 255, 250), font=font(20))
    draw.text((760, 970), "Use this to reject visually risky landing/traverse corridors.", fill=(238, 248, 249), font=font(20))
    draw.text((760, 1000), "Final certification still needs the official crater AOI if this run is using the proxy harness.", fill=(255, 224, 166), font=font(20))
    canvas.save(HAZARD_CARD, quality=95)


def main() -> None:
    DERIVED.mkdir(parents=True, exist_ok=True)
    DEMO.mkdir(parents=True, exist_ok=True)
    tmc = tmc_bbox()
    aoi = load_active_aoi()
    products = []
    for spec in OHR_PRODUCTS:
        footprint = sample_geometry(spec["geometry"])
        img = Image.open(spec["browse"])
        window = aoi_pixel_window(spec["geometry"], aoi["bbox"], img.size)
        hazards = hazard_candidates(img, window["pixel_window"] if window else None)
        products.append(
            {
                "id": spec["id"],
                "product": spec["product"],
                "browse_path": str(spec["browse"].relative_to(ROOT)),
                "geometry_path": str(spec["geometry"].relative_to(ROOT)),
                "image_size": list(img.size),
                "footprint": footprint,
                "aoi_window": window,
                "tmc_lat_overlap": ranges_overlap(footprint["lat_min"], footprint["lat_max"], tmc["lat_min"], tmc["lat_max"]),
                "tmc_lon_overlap_note": "Longitude comparison near lunar poles is projection-sensitive; exact overlap should use map-projected footprints.",
                "hazards": hazards,
            }
        )

    make_footprint_card(products, tmc)
    make_hazard_card(products, aoi)
    summary = {
        "status": "OHRC footprint and AOI-window hazard audit generated",
        "scientific_caution": (
            "This is not final OHRC hazard certification. It uses geometry CSV samples to crop active-AOI windows and produces browse-scale "
            "crater/boulder candidates inside those windows. The next upgrade is full map projection and official crater AOI replacement."
        ),
        "active_aoi": aoi,
        "tmc2_south_pole_bbox": tmc,
        "products": products,
        "outputs": {
            "footprint_card": str(FOOTPRINT_CARD.relative_to(ROOT)),
            "hazard_card": str(HAZARD_CARD.relative_to(ROOT)),
        },
    }
    SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
