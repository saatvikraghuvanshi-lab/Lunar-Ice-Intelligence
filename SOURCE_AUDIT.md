# Source Audit and Competitive Upgrade Plan

This project should present sources as an evidence pipeline, not as decoration. The table below separates what is already used from what should be integrated next.

| Source | Current status | What it contributes | Evidence in workspace | Next competitive upgrade |
| --- | --- | --- | --- | --- |
| ISRO PRADAN | Used | Official Chandrayaan-2 raw data download source | `data/raw/dfsar`, `data/raw/ohrc`, `data/raw/tmc2` | Add product IDs and timestamps to every UI layer card |
| ISSDC Chandrayaan-2 mission page | Used | Payload/mission context for DFSAR, OHRC, TMC-2 | `data/raw/docs/*user*guide*.pdf` | Parse metadata fields into a searchable product table |
| ISRO DFSAR 2026 subsurface-ice release | Used as science anchor | CPR > 1 and DOP < 0.13 target criteria for ice interpretation | SAR ratio/evidence layers in `data/processed/derived_layers` | Compute exact CPR/DOP if complex/full-polarimetric parameters are available |
| Chandrayaan-2 Map Browse | Used | AOI and product discovery route | South-pole TMC-2 pair `20231203T0019079527` | Add repeatable AOI search recipe and screenshots |
| VEDAS OHRC note | Used operationally | OHRC product discovery/download guidance | OHRC raw ZIPs and browse quicklooks | Use OHRC geometry CSVs for exact footprint overlays |
| NASA PDS / LRO LOLA | Used for validation | Independent lunar topography, slope, roughness, and class reference | `lola_validation_focus.png`, `lola_external_validation_summary.json` | Add higher-resolution LOLA/SLDEM validation when storage budget permits |
| NASA PGDA Lunar Polar Illumination | Used as validation target | Illumination/PSR context for power and volatile preservation | `illumination_availability_proxy.png`, `shadow_persistence_proxy.png`, `cold_trap_proxy.png` | Validate proxy against ephemeris-based polar illumination products |
| Lunar South Pole Atlas, LPI | Planned presentation context | Recognizable south-pole atlas framing and PSR/slope context | Referenced in dashboard source ledger | Label candidate zones using named features/PSR context |
| USGS ISIS | Roadmap documented | Professional planetary image processing stack | `docs/USGS_ISIS_PRODUCTION_PATH.md` | Create optional ISIS/QGIS processing branch |

## What We Should Say To Judges

The MVP already uses official Chandrayaan-2 DFSAR, OHRC, and TMC-2 products downloaded from PRADAN and processed into radar-evidence, terrain-slope, and landing-accessibility layers. The external NASA/LPI/USGS sources are deliberately framed as validation and production-hardening paths, not falsely claimed as fully integrated data.

## Current Prototype Formulas

| Output | Formula / Method | Scientific Caution |
| --- | --- | --- |
| SAR candidate evidence | `0.50 * co-pol brightness + 0.35 * cross/co ratio + 0.15 * HH/VV ratio` | Candidate evidence only; exact CPR/DOP validation is future work. |
| Terrain accessibility | `0.75 * low-slope score + 0.25 * local-relief score` | Screening score, not certified landing safety. |
| Cold-trap proxy | `0.65 * shadow persistence + 0.35 * inverse illumination` from low-sun hillshade sweeps | Must be validated against ephemeris-based PSR/illumination products. |
| Computed traverse | A* over `1 + ((100 - accessibility) / 18) + (cold-trap / 90)` | Needs geodetic distance calibration and rover dynamics before mission use. |

## Immediate Next Step

The strongest next technical improvement is to validate the current illumination/cold-trap proxy against a trusted ephemeris-based product, because candidate ice is only persuasive if radar evidence is balanced against permanently shadowed terrain, slope safety, and rover power/thermal constraints.

## External Validation Result

NASA LRO/LOLA 1000 m south-pole products from PGDA were cropped to the Chandrayaan-2 TMC-2 AOI. The TMC-derived mean slope is `10.67 deg`; the LOLA mean slope is `11.63 deg`; the mean difference is `0.96 deg`. Because LOLA is much coarser than TMC-2, this is a regional sanity check rather than pixel-perfect validation, but it is strong evidence that the terrain pipeline is behaving credibly.
