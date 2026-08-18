# Source Audit and Competitive Upgrade Plan

This project should present sources as an evidence pipeline, not as decoration. The table below separates what is already used from what should be integrated next.

| Source | Current status | What it contributes | Evidence in workspace | Next competitive upgrade |
| --- | --- | --- | --- | --- |
| ISRO PRADAN | Used | Official Chandrayaan-2 raw data download source | `data/raw/dfsar`, `data/raw/ohrc`, `data/raw/tmc2` | Process new raw D32 full-pol SAR through calibrated polarimetric pipeline |
| ISSDC Chandrayaan-2 mission page | Used | Payload/mission context for DFSAR, OHRC, TMC-2 | `data/raw/docs/*user*guide*.pdf` | Parse metadata fields into a searchable product table |
| ISRO DFSAR 2026 subsurface-ice release | Used as science anchor | CPR > 1 and DOP < 0.13 target criteria for ice interpretation | SAR ratio/evidence layers in `data/processed/derived_layers` | Compute exact CPR/DOP if complex/full-polarimetric parameters are available |
| Chandrayaan-2 Map Browse | Used | AOI and product discovery route | South-pole TMC-2 pair `20231203T0019079527` | Add repeatable AOI search recipe and screenshots |
| VEDAS OHRC note | Used operationally | OHRC product discovery/download guidance | Four OHRC raw ZIPs, browse quicklooks, and geometry CSVs | Use OHRC geometry CSVs for exact footprint overlays |
| NASA PDS / LRO LOLA | Used for validation | Independent lunar topography, slope, and roughness reference | `LDEM_85S_20M`, `lola_validation_focus.png`, `lola_external_validation_summary.json` | Validate against ephemeris PSR/illumination and registered crater AOI |
| NASA PGDA Lunar Polar Illumination | Used as validation target | Illumination/PSR context for power and volatile preservation | `illumination_availability_proxy.png`, `shadow_persistence_proxy.png`, `cold_trap_proxy.png` | Validate proxy against ephemeris-based polar illumination products |
| Lunar South Pole Atlas, LPI | Planned presentation context | Recognizable south-pole atlas framing and PSR/slope context | Referenced in dashboard source ledger | Label candidate zones using named features/PSR context |
| USGS ISIS | Roadmap documented | Professional planetary image processing stack | `docs/USGS_ISIS_PRODUCTION_PATH.md` | Create optional ISIS/QGIS processing branch |

## What We Should Say To Judges

The MVP already uses official Chandrayaan-2 DFSAR, OHRC, and TMC-2 products downloaded from PRADAN and processed into radar-evidence, terrain-slope, landing-accessibility, and hazard-readiness layers. The latest data pass adds three raw 2025 L-band full-pol D32 DFSAR products, four OHRC strip audits, and NASA PDS `LDEM_85S_20M` terrain validation. The external NASA/LPI/USGS sources are deliberately framed as validation and production-hardening paths, not falsely claimed as ice confirmation.

## Current Prototype Formulas

| Output | Formula / Method | Scientific Caution |
| --- | --- | --- |
| SAR candidate evidence | `0.50 * co-pol brightness + 0.35 * cross/co ratio + 0.15 * HH/VV ratio` | Candidate evidence only; exact CPR/DOP validation is future work. |
| Terrain accessibility | `0.75 * low-slope score + 0.25 * local-relief score` | Screening score, not certified landing safety. |
| Cold-trap proxy | `0.65 * shadow persistence + 0.35 * inverse illumination` from low-sun hillshade sweeps | Must be validated against ephemeris-based PSR/illumination products. |
| Computed traverse | A* over `1 + ((100 - accessibility) / 18) + (cold-trap / 90)` | Needs geodetic distance calibration and rover dynamics before mission use. |

## Immediate Next Step

The strongest next technical improvement is to convert the newly downloaded raw D32 full-pol DFSAR products into calibrated polarimetric outputs for exact CPR/DOP, then intersect the four OHRC footprints with the official crater AOI.

## External Validation Result

NASA PDS LRO/LOLA `LDEM_85S_20M` was cropped to the Chandrayaan-2 TMC-2 overlap. The TMC-derived mean slope is `9.87 deg`; the LOLA-derived mean slope is `10.50 deg`; the mean difference is `0.63 deg`. The dashboard quicklook is downsampled for interactivity, but it is derived from the 20 m/pixel source DEM and gives a strong independent terrain sanity check.
