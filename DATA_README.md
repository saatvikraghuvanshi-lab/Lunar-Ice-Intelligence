# Lunar Ice Intelligence System - Data Baseline

## Current MVP Dataset

Raw ZIP archives are kept untouched under `data/raw`.

| Instrument | File | Purpose |
| --- | --- | --- |
| DFSAR | `data/raw/dfsar/ch2_sar_ncls_20200913t042439405_d_fp_d18.zip` | Radar evidence layer for candidate subsurface ice indicators |
| OHRC | `data/raw/ohrc/ch2_ohr_ncp_20260103T0609041371_d_img_d18.zip` | High-resolution visual hazard inspection |
| OHRC | `data/raw/ohrc/ch2_ohr_ncp_20260103T1005176450_d_img_d18.zip` | Second optical strip for comparison |
| TMC-2 | `data/raw/tmc2/ch2_tmc_ndn_20231203T0019079527_d_dtm_d18.zip` | South-pole terrain model for slope and traverse-cost planning |
| TMC-2 | `data/raw/tmc2/ch2_tmc_ndn_20231203T0019079527_d_oth_d18.zip` | Matching south-pole orthorectified image context, kept zipped to save disk |
| TMC-2 | `data/raw/tmc2/ch2_tmc_ndn_20250426T0752081453_d_dtm_d18.zip` | Deprecated non-polar terrain test data |
| TMC-2 | `data/raw/tmc2/ch2_tmc_ndn_20250426T0752081453_d_oth_d18.zip` | Deprecated non-polar ortho test data |

Supporting guides are under `data/raw/docs`.

## Storage

- Raw zipped science data: about 3.86 GB.
- Minimal extracted working set plus derived products: about 3.22 GB.
- The full south-pole TMC-2 orthoproduct expands to about 1.96 GB. It is intentionally left zipped unless full-resolution texture processing is needed.

## Extracted Working Set

The minimal extracted files live under:

```text
data/processed/extracted_minimal/
```

This includes:

- Deprecated non-polar TMC-2 DTM and ortho GeoTIFFs plus labels, retained only as pipeline test data.
- Compact DFSAR SRI/GRI GeoTIFF layers plus geometry CSVs and labels.
- OHRC browse PNGs, geometry CSVs, and labels.
- Official browse PNGs for quick visual validation.

The valid south-pole TMC-2 working set lives under:

```text
data/processed/extracted_tmc2_south_pole/
```

This includes the full south-pole DTM GeoTIFF, DTM/ortho browse images, labels, and readme. The full-resolution ortho GeoTIFF remains zipped in `data/raw/tmc2`.

Generated quicklooks live under:

```text
data/processed/quicklooks/
```

Open this for a visual summary:

```text
data/processed/quicklooks/contact_sheet.png
```

## Derived Layers

Generated science/demo layers live under:

```text
data/processed/derived_layers/
```

Key outputs:

- `sar_candidate_ice_evidence_score.png`
- `sar_candidate_ice_evidence_score.tif`
- `tmc2_south_pole_elevation.png`
- `tmc2_south_pole_slope_deg.png`
- `tmc2_south_pole_accessibility_score.png`
- `tmc2_south_pole_contact_sheet.png`
- `tmc2_south_pole_summary.json`

The south-pole TMC-2 strip is in lunar polar stereographic projection and approximately spans `88.65S` to `81.50S`.

## Next Processing Steps

1. Register DFSAR radar evidence and TMC-2 terrain products into a common AOI grid.
2. Add PSR/illumination and temperature proxy layers.
3. Use OHRC geometry CSVs and browse imagery for hazard-context overlays.
4. Convert the current prototype scores into reproducible feature-based candidate ranking.
5. Add rover traverse graph search across the accessibility layer.

## Demo Entry Point

Static dashboard:

```text
demo/index.html
```

Open it in a browser to view the first evidence-board prototype.
