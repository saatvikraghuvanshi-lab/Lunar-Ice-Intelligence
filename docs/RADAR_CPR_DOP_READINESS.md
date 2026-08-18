# Radar CPR/DOP Readiness Note

Date: 2026-06-20

## Current Status

The dashboard implements the Problem Statement 8 radar gate explicitly:

- CPR target criterion: `CPR > 1`
- DOP target criterion: `DOP < 0.13`

Current output is a threshold-ready proxy, not exact CPR/DOP. A DFSAR readiness audit has now been generated from the extracted PDS4 labels and product files. The new data pass adds three raw 2025 D32 full-pol products that are staged for a future calibrated CPR/DOP workflow.

## What We Have

Downloaded Chandrayaan-2 DFSAR product:

`data/raw/dfsar/ch2_sar_ncls_20200913t042439405_d_fp_d18.zip`

Additional raw full-pol products staged for CPR/DOP upgrade:

- `data/raw/dfsar/ch2_sar_nrxl_20251024t075159312_d_fp_d32.zip`
- `data/raw/dfsar/ch2_sar_nrxl_20251024t094954820_d_fp_d32.zip`
- `data/raw/dfsar/ch2_sar_nrxl_20251024t114751370_d_fp_d32.zip`

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

Readiness audit outputs:

- `scripts/audit_dfsar_polarimetry.py`
- `scripts/derive_validation_gates.py`
- `data/processed/derived_layers/dfsar_polarimetry_audit_summary.json`
- `data/processed/derived_layers/validation_gate_readiness_summary.json`
- `data/processed/demo_assets/dfsar_polarimetry_audit_focus.png`
- `data/processed/demo_assets/validation_gate_readiness_focus.png`

Audit result:

- Four linear polarizations found: `HH`, `HV`, `VH`, `VV`
- Twenty-eight phase-orthogonality metadata values found across the processed 2020 product labels and the new raw 2025 D32 labels
- Three raw 2025 L-band right-looking D32 full-pol products found, each with `HH`, `HV`, `VH`, `VV`
- Three large raw `.dat` products are present inside the ZIPs; they are upstream raw echo products, not calibrated map-projected CPR/DOP rasters
- No exact CPR, DOP, Stokes, coherency, covariance, circular-polarization, or MIDAS-style product files found in the current extracted package

## Replacement Gates Now Implemented

The repository now contains an exact-replacement harness:

- Put official crater geometry at `data/aoi/official_crater_aoi.geojson`.
- Put official/calibrated CPR and DOP outputs into the processed evidence folder when supplied.
- Re-run `scripts/derive_validation_gates.py`.

Until then, the dashboard uses `data/aoi/dsc1_proxy_registration_harness.geojson` only as a registration harness and clearly labels it as non-official.

## Why Exact CPR/DOP Is Still Pending

Exact CPR and DOP require calibrated polarimetric products with phase/coherency information or official polarimetric outputs from a DFSAR/MIDAS-style processing path. The current extracted package supports HH/HV/VH/VV evidence screening and metadata auditing, and the new raw D32 files improve readiness, but they still need calibration/processing before a defensible exact CPR/DOP claim.

## Hackathon Handling

The system therefore separates three things clearly:

- Radar evidence score: uses downloaded DFSAR intensity products.
- CPR/DOP gate: shows the required criteria and flags candidate pixels with a proxy screen.
- Scientific claim level: candidate ice evidence only, not confirmed ice.

## Next Upgrade Path

Replace the proxy gate with exact products by processing the new raw full-pol files or any supplied crater polarimetric products into:

1. Calibrated CPR raster.
2. Calibrated DOP raster.
3. Binary threshold mask using `CPR > 1 and DOP < 0.13`.
4. Updated DSC-1 candidate score weighted by exact CPR/DOP agreement.
5. Updated volume scenarios using the exact radar-derived candidate area.

This is the highest-priority upgrade if the final hackathon data package contains the needed polarimetric terms.
