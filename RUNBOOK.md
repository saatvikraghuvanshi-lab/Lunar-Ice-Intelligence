# Runbook

## 1. Local Environment

Create and use the local geospatial environment:

```powershell
& "C:\Users\saatv\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-geospatial.txt
```

## 2. Regenerate PDF Planning Docs

```powershell
.\.venv\Scripts\python.exe scripts\generate_lunar_ice_docs.py
```

Outputs:

```text
output/pdf/
```

## 3. Extract Minimal Working Data

The minimal extraction has already been done. To rebuild the original quicklooks:

```powershell
.\.venv\Scripts\python.exe scripts\preprocess_lunar_data.py
```

Outputs:

```text
data/processed/quicklooks/
```

## 4. Derive SAR Evidence Layers

```powershell
.\.venv\Scripts\python.exe scripts\derive_sar_evidence.py
```

Outputs:

```text
data/processed/derived_layers/
```

Most important current layer:

```text
data/processed/derived_layers/sar_candidate_ice_evidence_score.png
data/processed/derived_layers/sar_candidate_ice_evidence_score.tif
```

## 5. Derive South-Pole TMC-2 Terrain Layers

```powershell
.\.venv\Scripts\python.exe scripts\process_tmc2_south_pole.py
```

Outputs:

```text
data/processed/derived_layers/tmc2_south_pole_elevation.png
data/processed/derived_layers/tmc2_south_pole_slope_deg.png
data/processed/derived_layers/tmc2_south_pole_accessibility_score.png
data/processed/derived_layers/tmc2_south_pole_contact_sheet.png
```

The full south-pole OTH GeoTIFF is intentionally left zipped to save about 2 GB.

## 6. Derive Illumination and Cold-Trap Proxies

```powershell
.\.venv\Scripts\python.exe scripts\derive_illumination_proxy.py
```

Outputs:

```text
data/processed/derived_layers/illumination_availability_proxy.png
data/processed/derived_layers/shadow_persistence_proxy.png
data/processed/derived_layers/cold_trap_proxy.png
```

These are low-sun hillshade screening proxies derived from the TMC-2 DTM. They are not substitutes for validated ephemeris-based PSR or illumination products, but they make the MVP mission-planning story stronger.

## 7. Derive Rover Traverse Route

```powershell
.\.venv\Scripts\python.exe scripts\derive_traverse_route.py
```

Outputs:

```text
data/processed/demo_assets/data_derived_traverse_focus.png
data/processed/derived_layers/data_derived_traverse_route.json
```

The route is an A* screening path over the TMC-2 accessibility and cold-trap proxy rasters. It is constrained to one connected valid-data terrain island so it does not pretend the rover can cross no-data gaps.

## 8. Derive NASA LOLA External Validation

```powershell
.\.venv\Scripts\python.exe scripts\derive_lola_validation.py
```

Outputs:

```text
data/processed/demo_assets/lola_validation_focus.png
data/processed/derived_layers/lola_external_validation_summary.json
```

This crops NASA LRO/LOLA south-pole slope, roughness, and class products to the Chandrayaan-2 TMC-2 AOI. Current result: TMC-derived mean slope `10.67 deg`, LOLA mean slope `11.63 deg`, mean difference `0.96 deg`, which is a strong regional sanity check.

## 9. Build Demo-Focused Assets

```powershell
.\.venv\Scripts\python.exe scripts\build_demo_assets.py
```

Outputs:

```text
data/processed/demo_assets/
```

These are cropped, presentation-focused images generated from the real processed layers. They keep the raw science products unchanged while making the dashboard readable on a projector or laptop screen.

## 10. Open Demo

Open this file in a browser:

```text
demo/index.html
```

When using the local server:

```powershell
.\.venv\Scripts\python.exe -m http.server 8765 -d .
```

Then open:

```text
http://localhost:8765/demo/index.html
```

## 11. Judge Demo Mode

Use the `Start Demo` button at the top of the dashboard for the live judging flow. It walks through:

1. Problem framing: south-pole ice is hard to confirm.
2. DFSAR candidate radar evidence.
3. TMC-2 terrain/slope safety.
4. NASA LOLA external terrain validation.
5. Cold-trap proxy for volatile plausibility.
6. A* traverse from landing zone to science target.
7. Recommendation: prioritize `SCI-B` via `LZ-A` while keeping the claim at candidate level.

This mode is the fastest way to present the prototype in a 2-3 minute judge slot.

## 12. Data Notes

The valid TMC-2 DTM/ortho pair is:

```text
ch2_tmc_ndn_20231203T0019079527_d_dtm_d18.zip
ch2_tmc_ndn_20231203T0019079527_d_oth_d18.zip
```

The older `20250426T0752081453` TMC-2 pair is non-polar and should be treated only as pipeline test data.
