# Radar CPR/DOP Readiness Note

Date: 2026-06-19

## Current Status

The dashboard implements the Problem Statement 8 radar gate explicitly:

- CPR target criterion: `CPR > 1`
- DOP target criterion: `DOP < 0.13`

Current output is a threshold-ready proxy, not exact CPR/DOP.

## What We Have

Downloaded Chandrayaan-2 DFSAR product:

`data/raw/dfsar/ch2_sar_ncls_20200913t042439405_d_fp_d18.zip`

Extracted calibrated linear-polarization intensity rasters:

- `HH`
- `HV`
- `VH`
- `VV`

Derived proxy layers:

- `data/processed/derived_layers/sar_candidate_ice_evidence_score.tif`
- `data/processed/derived_layers/sar_cross_to_co_ratio.tif`
- `data/processed/derived_layers/sar_hh_vv_ratio.tif`
- `data/processed/demo_assets/cpr_dop_threshold_focus.png`

## Why Exact CPR/DOP Is Still Pending

Exact CPR and DOP require calibrated polarimetric products with phase/coherency information or official polarimetric outputs from a DFSAR/MIDAS-style processing path. The currently extracted rasters are intensity products, which support evidence screening but not a fully defensible exact CPR/DOP claim.

## Hackathon Handling

The system therefore separates three things clearly:

- Radar evidence score: uses downloaded DFSAR intensity products.
- CPR/DOP gate: shows the required criteria and flags candidate pixels with a proxy screen.
- Scientific claim level: candidate ice evidence only, not confirmed ice.

## If Supplied Crater Data Includes Polarimetric Products

Replace the proxy gate with exact products by adding:

1. Calibrated CPR raster.
2. Calibrated DOP raster.
3. Binary threshold mask using `CPR > 1 and DOP < 0.13`.
4. Updated DSC-1 candidate score weighted by exact CPR/DOP agreement.
5. Updated volume scenarios using the exact radar-derived candidate area.

This is the highest-priority upgrade if the final hackathon data package contains the needed polarimetric terms.
