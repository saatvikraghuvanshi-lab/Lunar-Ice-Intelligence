# Data Manifest

This repository intentionally does not track raw Chandrayaan-2 archives, extracted GeoTIFF rasters, local virtual environments, or build caches.

## Local Raw Data Layout

Place downloaded source products in:

| Payload | Local folder | Notes |
| --- | --- | --- |
| Chandrayaan-2 DFSAR | `data/raw/dfsar/` | Full-polarization radar product for candidate ice evidence. |
| Chandrayaan-2 TMC-2 | `data/raw/tmc2/` | DTM and orthographic products for slope, accessibility, and traverse. |
| Chandrayaan-2 OHRC | `data/raw/ohrc/` | High-resolution hazard context; footprint registration remains pending. |
| NASA LRO/LOLA / PDS validation | `data/raw/external/` | Coarse independent terrain sanity check. |

## Current Local Products Used

| Payload | Product | Role |
| --- | --- | --- |
| DFSAR | `ch2_sar_ncls_20200913t042439405_d_fp_d18.zip` | SAR candidate evidence and CPR/DOP threshold-readiness proxy. |
| TMC-2 | `ch2_tmc_ndn_20231203T0019079527_d_dtm_d18.zip` | South-pole DTM for slope, illumination proxy, accessibility, and A* route. |
| TMC-2 | `ch2_tmc_ndn_20231203T0019079527_d_oth_d18.zip` | Orthographic context. |
| OHRC | `ch2_ohr_ncp_20260103T0609041371_d_img_d18.zip` | High-resolution context strip. |
| OHRC | `ch2_ohr_ncp_20260103T1005176450_d_img_d18.zip` | High-resolution context strip. |

## Git-Tracked Derived Demo Assets

Small PNG/JSON artifacts under `data/processed/demo_assets/` and selected `data/processed/derived_layers/*.png|*.json` are tracked so the dashboard can run without committing multi-GB source products.

## Scientific Caveat

The current DFSAR-derived CPR/DOP gate is threshold-ready but not exact CPR/DOP. Exact CPR/DOP requires calibrated polarimetric phase/coherency products or official MIDAS-style outputs.
