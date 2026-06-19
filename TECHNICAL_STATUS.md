# Technical Status - June 19, 2026

## What Is Valid Right Now

- DFSAR product `ch2_sar_ncls_20200913t042439405_d_fp_d18.zip` is usable for the lunar south-pole radar-evidence prototype.
- The extracted DFSAR SRI products contain a lunar south-pole polar stereographic CRS.
- TMC-2 pair `ch2_tmc_ndn_20231203T0019079527_d_dtm_d18.zip` and `ch2_tmc_ndn_20231203T0019079527_d_oth_d18.zip` is usable for south-pole terrain context.
- The south-pole TMC-2 DTM is in lunar polar stereographic projection and approximately spans `88.65S` to `81.50S`.
- Real SAR-derived layers have been generated in:

```text
data/processed/derived_layers/
```

Key output:

```text
sar_candidate_ice_evidence_score.tif
sar_candidate_ice_evidence_score.png
```

This score combines co-pol brightness, cross-pol response, and HH/VV ratio. It is a candidate evidence score, not confirmed ice.

South-pole terrain outputs have also been generated:

```text
tmc2_south_pole_elevation.png
tmc2_south_pole_slope_deg.png
tmc2_south_pole_accessibility_score.png
tmc2_south_pole_contact_sheet.png
```

The accessibility score combines low slope and moderate local relief. It is a prototype landing/traverse screening score, not a certified landing-site safety product.

Illumination and cold-trap proxy layers have also been generated from the TMC-2 DTM:

```text
illumination_availability_proxy.png
shadow_persistence_proxy.png
cold_trap_proxy.png
illumination_proxy_summary.json
```

These are low-sun hillshade screening proxies. They strengthen the MVP mission-planning logic, but should be validated against ephemeris-based illumination/PSR products before any scientific claim.

A rover traverse screening route has been generated:

```text
data_derived_traverse_focus.png
data_derived_traverse_route.json
```

The route is computed with A* over downsampled TMC-2 accessibility and cold-trap proxy rasters. Start and target are selected inside the largest connected valid-data component, which prevents the demo from drawing a path across no-data gaps.

NASA LRO/LOLA external validation has been added:

```text
lola_tmc_aoi_slope_1000m.png
lola_tmc_aoi_roughness_1000m.png
lola_tmc_aoi_class_1000m.png
lola_validation_focus.png
lola_external_validation_summary.json
```

Current validation result: TMC-derived mean slope `10.67 deg`, LOLA mean slope `11.63 deg`, difference `0.96 deg`. This is a strong regional sanity check because LOLA is independent and coarser than TMC-2.

## Deprecated Test Data

The older TMC-2 pair is not south-polar:

```text
ch2_tmc_ndn_20250426T0752081453_d_dtm_d18.zip
ch2_tmc_ndn_20250426T0752081453_d_oth_d18.zip
```

Raster metadata shows approximate latitude coverage:

```text
-1.53 to -28.09 degrees
```

That does not overlap the target lunar south-pole region. These files are retained only for pipeline regression testing.

## What To Build Next

1. Register valid DFSAR candidate evidence with valid TMC terrain constraints.
2. Validate the current illumination/cold-trap proxy against external PSR/illumination products.
3. Add USGS ISIS/PDS-style processing notes or command stubs for production hardening.
4. Calibrate the A* traverse route with geodetic distances, obstacle inflation, and rover dynamics.
5. Keep OHRC as visual/hazard context unless exact overlap is verified.
6. Replace prototype scores with reproducible feature-weighted candidate ranking.

## Current Demo

Static prototype:

```text
demo/index.html
```

It now includes real DFSAR-derived candidate evidence and real south-pole TMC-2 terrain layers.
