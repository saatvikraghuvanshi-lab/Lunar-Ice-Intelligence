from __future__ import annotations

import heapq
import json
import math
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image, ImageDraw, ImageFont
from rasterio.enums import Resampling


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "processed" / "derived_layers"
DEMO = ROOT / "data" / "processed" / "demo_assets"
DEMO.mkdir(parents=True, exist_ok=True)

ACCESS_TIF = DERIVED / "tmc2_south_pole_accessibility_score.tif"
COLD_TIF = DERIVED / "cold_trap_proxy.tif"
ILLUM_TIF = DERIVED / "illumination_availability_proxy.tif"
ORTHO = DERIVED / "tmc2_south_pole_orthobrowse.png"
OUT_PNG = DEMO / "data_derived_traverse_focus.png"
OUT_JSON = DERIVED / "data_derived_traverse_route.json"


def normalize(arr: np.ndarray) -> np.ndarray:
    out = arr.astype("float32", copy=True)
    valid = np.isfinite(out)
    if valid.any():
        lo, hi = np.nanpercentile(out[valid], [2, 98])
        if hi <= lo:
            hi = lo + 1
        out = np.clip((out - lo) / (hi - lo), 0, 1)
    out[~valid] = np.nan
    return out


def read_small(path: Path, size: int = 520) -> tuple[np.ndarray, dict]:
    with rasterio.open(path) as src:
        scale = max(src.width / size, src.height / size, 1)
        width = int(src.width / scale)
        height = int(src.height / scale)
        arr = src.read(1, out_shape=(height, width), resampling=Resampling.bilinear).astype("float32")
        profile = {
            "width": src.width,
            "height": src.height,
            "bounds": tuple(src.bounds),
            "transform": tuple(src.transform)[:6],
            "crs": str(src.crs),
            "scale": scale,
        }
    arr[arr < -1000] = np.nan
    return arr, profile


def nearest_valid(mask: np.ndarray, y: int, x: int) -> tuple[int, int]:
    if mask[y, x]:
        return y, x
    ys, xs = np.where(mask)
    idx = np.argmin((ys - y) ** 2 + (xs - x) ** 2)
    return int(ys[idx]), int(xs[idx])


def largest_component(mask: np.ndarray) -> np.ndarray:
    h, w = mask.shape
    visited = np.zeros(mask.shape, dtype=bool)
    best: list[tuple[int, int]] = []
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    ys, xs = np.where(mask)
    for sy, sx in zip(ys, xs):
        if visited[sy, sx]:
            continue
        stack = [(int(sy), int(sx))]
        visited[sy, sx] = True
        cells: list[tuple[int, int]] = []
        while stack:
            y, x = stack.pop()
            cells.append((y, x))
            for dy, dx in neighbors:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not visited[ny, nx]:
                    visited[ny, nx] = True
                    stack.append((ny, nx))
        if len(cells) > len(best):
            best = cells
    component = np.zeros(mask.shape, dtype=bool)
    for y, x in best:
        component[y, x] = True
    return component


def pick_points(access: np.ndarray, cold: np.ndarray) -> tuple[tuple[int, int], tuple[int, int]]:
    valid = largest_component(np.isfinite(access) & np.isfinite(cold))
    h, w = access.shape
    yy = np.indices(access.shape)[0]

    # Landing zone: prioritize stable terrain in the upper reachable half.
    valid_rows = np.where(valid)[0]
    y_min, y_max = int(valid_rows.min()), int(valid_rows.max())
    upper_cut = y_min + 0.42 * (y_max - y_min)
    lower_cut = y_min + 0.54 * (y_max - y_min)
    upper = valid & (yy < upper_cut)
    if not upper.any():
        upper = valid
    landing_score = np.where(upper, access, np.nan)
    ly, lx = np.unravel_index(np.nanargmax(landing_score), access.shape)

    # Science target: prioritize cold-trap plausibility but keep rover-accessible terrain.
    lower = valid & (yy > lower_cut)
    if not lower.any():
        lower = valid
    target_score = np.where(lower, 0.68 * cold + 0.32 * access, np.nan)
    ty, tx = np.unravel_index(np.nanargmax(target_score), access.shape)

    return nearest_valid(valid, int(ly), int(lx)), nearest_valid(valid, int(ty), int(tx))


def astar(cost: np.ndarray, start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]:
    h, w = cost.shape
    valid = np.isfinite(cost)
    moves = [
        (-1, 0, 1.0),
        (1, 0, 1.0),
        (0, -1, 1.0),
        (0, 1, 1.0),
        (-1, -1, math.sqrt(2)),
        (-1, 1, math.sqrt(2)),
        (1, -1, math.sqrt(2)),
        (1, 1, math.sqrt(2)),
    ]

    def heuristic(p: tuple[int, int]) -> float:
        return math.hypot(goal[0] - p[0], goal[1] - p[1])

    open_set: list[tuple[float, tuple[int, int]]] = [(heuristic(start), start)]
    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    g = {start: 0.0}
    seen = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        if current in seen:
            continue
        seen.add(current)
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return list(reversed(path))

        cy, cx = current
        for dy, dx, distance in moves:
            ny, nx = cy + dy, cx + dx
            if ny < 0 or nx < 0 or ny >= h or nx >= w or not valid[ny, nx]:
                continue
            step = distance * float(cost[ny, nx])
            tentative = g[current] + step
            neighbor = (ny, nx)
            if tentative < g.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g[neighbor] = tentative
                heapq.heappush(open_set, (tentative + heuristic(neighbor), neighbor))

    return [start, goal]


def draw_route(base_path: Path, path: list[tuple[int, int]], shape: tuple[int, int], start: tuple[int, int], goal: tuple[int, int]) -> None:
    base = Image.open(base_path).convert("RGB")
    draw = ImageDraw.Draw(base)
    w, h = base.size
    rows, cols = shape

    points = [(int(x / (cols - 1) * w), int(y / (rows - 1) * h)) for y, x in path]
    if len(points) > 1:
        draw.line(points, fill=(47, 222, 210), width=10, joint="curve")
        draw.line(points, fill=(6, 34, 38), width=4)

    def marker(pixel: tuple[int, int], label: str, color: tuple[int, int, int]) -> None:
        y, x = pixel
        px = int(x / (cols - 1) * w)
        py = int(y / (rows - 1) * h)
        draw.rectangle((px - 18, py - 18, px + 18, py + 18), outline=color, width=5)
        draw.text((px + 24, py - 20), label, fill=color, font=ImageFont.load_default())

    marker(start, "LZ-A", (242, 191, 90))
    marker(goal, "SCI-B", (243, 108, 97))

    # Crop around the computed route so the rover path and local terrain fill the dashboard panel.
    marker_points = points + [
        (int(start[1] / (cols - 1) * w), int(start[0] / (rows - 1) * h)),
        (int(goal[1] / (cols - 1) * w), int(goal[0] / (rows - 1) * h)),
    ]
    xs = [p[0] for p in marker_points]
    ys = [p[1] for p in marker_points]
    route_width = max(xs) - min(xs)
    route_height = max(ys) - min(ys)
    margin = max(150, int(max(route_width, route_height) * 1.7))
    left = max(0, min(xs) - margin)
    top = max(0, min(ys) - margin)
    right = min(w, max(xs) + margin)
    bottom = min(h, max(ys) + margin)

    crop = base.crop((left, top, right, bottom))
    canvas = Image.new("RGB", (1440, 960), (3, 6, 10))
    max_w, max_h = 1220, 780
    scale = min(max_w / crop.width, max_h / crop.height)
    crop = crop.resize((max(1, int(crop.width * scale)), max(1, int(crop.height * scale))), Image.Resampling.LANCZOS)
    x = (canvas.width - crop.width) // 2
    y = (canvas.height - crop.height) // 2
    canvas.paste(crop, (x, y))

    label = ImageDraw.Draw(canvas)
    label.rectangle((36, 34, 524, 92), fill=(5, 10, 14), outline=(55, 85, 96), width=2)
    label.text((54, 50), "Computed A* traverse: LZ-A to SCI-B", fill=(232, 246, 247), font=ImageFont.load_default())
    label.text((54, 70), "Cost surface: accessibility + cold trap + solar power penalty", fill=(133, 214, 207), font=ImageFont.load_default())
    canvas.save(OUT_PNG, quality=95)


def main() -> None:
    access_raw, profile = read_small(ACCESS_TIF)
    cold_raw, _ = read_small(COLD_TIF, size=max(access_raw.shape))
    illum_raw, _ = read_small(ILLUM_TIF, size=max(access_raw.shape))
    if cold_raw.shape != access_raw.shape or illum_raw.shape != access_raw.shape:
        # The products are generated from the same source DTM; this is a guard if a future run differs.
        raise RuntimeError(
            f"Shape mismatch: accessibility {access_raw.shape}, cold {cold_raw.shape}, illumination {illum_raw.shape}"
        )

    access = normalize(access_raw) * 100.0
    cold = normalize(cold_raw) * 100.0
    illum = normalize(illum_raw) * 100.0
    valid = np.isfinite(access) & np.isfinite(cold) & np.isfinite(illum)
    start, goal = pick_points(access, cold)

    # Lower cost prefers accessible terrain, penalizes long low-power stretches, and tolerates cold traps near science targets.
    solar_penalty = np.clip((45.0 - illum) / 45.0, 0.0, 1.0)
    cost = 1.0 + (100.0 - access) / 18.0 + cold / 110.0 + solar_penalty * 1.45
    cost[~valid] = np.nan
    route = astar(cost, start, goal)
    draw_route(ORTHO, route, access.shape, start, goal)

    route_cost = float(sum(cost[y, x] for y, x in route if np.isfinite(cost[y, x])))
    route_illum = np.array([illum[y, x] for y, x in route if np.isfinite(illum[y, x])])
    route_access = np.array([access[y, x] for y, x in route if np.isfinite(access[y, x])])
    route_cold = np.array([cold[y, x] for y, x in route if np.isfinite(cold[y, x])])
    low_power_pct = float(np.mean(route_illum < 35.0) * 100.0) if route_illum.size else 0.0
    pixel_size_m = float((abs(profile["transform"][0]) + abs(profile["transform"][4])) / 2.0 * profile["scale"])
    route_distance_m = float(max(0, len(route) - 1) * pixel_size_m)
    summary = {
        "method": "A* route on downsampled TMC-2 accessibility, cold-trap proxy, and solar-power penalty rasters.",
        "start": {"label": "LZ-A", "row_col": start},
        "goal": {"label": "SCI-B", "row_col": goal},
        "path_pixels": len(route),
        "path_row_col": route,
        "estimated_distance_m": route_distance_m,
        "relative_cost": route_cost,
        "solar_power_metrics": {
            "mean_illumination_score": float(np.nanmean(route_illum)) if route_illum.size else None,
            "min_illumination_score": float(np.nanmin(route_illum)) if route_illum.size else None,
            "low_power_segment_pct": low_power_pct,
            "mean_accessibility_score": float(np.nanmean(route_access)) if route_access.size else None,
            "mean_cold_trap_score": float(np.nanmean(route_cold)) if route_cold.size else None,
        },
        "source_layers": [
            str(ACCESS_TIF.relative_to(ROOT)),
            str(COLD_TIF.relative_to(ROOT)),
            str(ILLUM_TIF.relative_to(ROOT)),
        ],
        "output_image": str(OUT_PNG.relative_to(ROOT)),
        "note": "This is a solar-aware screening route for demo planning. It is data-derived but still needs geodetic distance calibration, obstacle inflation, and rover dynamics before mission use.",
        "profile": profile,
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
