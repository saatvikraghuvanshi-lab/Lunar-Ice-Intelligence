# Data Manifest

This repository intentionally does not track raw Chandrayaan-2 archives, extracted GeoTIFF rasters, local virtual environments, or build caches.

## Local Raw Data Layout

Place downloaded source products in:

| Payload | Local folder | Notes |
| --- | --- | --- |
| Chandrayaan-2 DFSAR | `data/raw/dfsar/` | Full-polarization radar product for candidate ice evidence. |
| Chandrayaan-2 TMC-2 | `data/raw/tmc2/` | DTM and orthographic products for slope, accessibility, and traverse. |
| Chandrayaan-2 OHRC | `data/raw/ohrc/` | High-resolution hazard context; footprint registration harness is active pending official AOI. |
| NASA LRO/LOLA / PDS validation | `data/raw/external/lola/` | Independent south-pole terrain sanity check. |

## Current Local Products Used

| Payload | Product | Role |
| --- | --- | --- |
| DFSAR | `ch2_sar_ncls_20200913t042439405_d_fp_d18.zip` | SAR candidate evidence and CPR/DOP threshold-readiness proxy. |
| DFSAR | `ch2_sar_nrxl_20251024t075159312_d_fp_d32.zip` | Raw L-band full-pol D32 candidate for future CPR/DOP processing. |
| DFSAR | `ch2_sar_nrxl_20251024t094954820_d_fp_d32.zip` | Raw L-band full-pol D32 candidate for adjacent coverage. |
| DFSAR | `ch2_sar_nrxl_20251024t114751370_d_fp_d32.zip` | Raw L-band full-pol D32 candidate for adjacent coverage. |
| TMC-2 | `ch2_tmc_ndn_20231203T0019079527_d_dtm_d18.zip` | South-pole DTM for slope, illumination proxy, accessibility, and A* route. |
| TMC-2 | `ch2_tmc_ndn_20231203T0019079527_d_oth_d18.zip` | Orthographic context. |
| OHRC | `ch2_ohr_ncp_20260103T0410224157_d_img_d18.zip` | High-resolution context strip; geometry audited. |
| OHRC | `ch2_ohr_ncp_20260103T0609041371_d_img_d18.zip` | High-resolution context strip. |
| OHRC | `ch2_ohr_ncp_20260103T1005176450_d_img_d18.zip` | High-resolution context strip. |
| OHRC | `ch2_ohr_ncp_20260103T1203563771_d_img_d18.zip` | High-resolution context strip; geometry audited. |
| NASA LOLA | `ldem_85s_20m_float.img/.lbl/.xml` | PDS LDEM_85S_20M polar DEM for independent TMC terrain validation. |

## Git-Tracked Derived Demo Assets

Small PNG/JSON artifacts under `data/processed/demo_assets/` and selected `data/processed/derived_layers/*.png|*.json` are tracked so the dashboard can run without committing multi-GB source products.

## AOI Replacement Harness

| File | Role |
| --- | --- |
| `data/aoi/dsc1_proxy_registration_harness.geojson` | Current proxy AOI used only to exercise OHRC footprint registration logic. |
| `data/aoi/official_crater_aoi_template.geojson` | Template showing where the supplied crater polygon should go. |
| `data/aoi/official_crater_aoi.geojson` | Not present yet. Add the official supplied crater AOI here to replace the proxy harness. |
| `data/processed/derived_layers/validation_gate_readiness_summary.json` | Machine-readable status for exact CPR/DOP, active AOI, and OHRC registration readiness. |

## Scientific Caveat

The current DFSAR-derived CPR/DOP gate is threshold-ready but not exact CPR/DOP. Exact CPR/DOP requires calibrated polarimetric phase/coherency products or official MIDAS-style outputs. Three raw 2025 D32 full-pol `.dat` products are now staged as candidates for that next processing step, but they are raw echo products rather than finished CPR/DOP rasters.
