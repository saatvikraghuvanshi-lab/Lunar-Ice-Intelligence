# Problem Statement 8 Compliance Review

Date: 2026-06-27

## Overall Status

Current compliance after the June 27 validation/limitations pass: about 92-94% as a decision-support prototype, with the same critical scientific caveat: exact calibrated CPR/DOP and the official supplied crater AOI are still required before any confirmed-ice claim.

The project is strong as a decision-support prototype: it uses downloaded Chandrayaan-2 DFSAR, TMC-2, and OHRC files; it has radar evidence layers, terrain constraints, illumination/cold-trap proxies, LOLA validation, a rough-terrain false-positive filter, a solar-aware A* traverse, a judge demo mode, explicit scientific honesty, a Problem Statement 8 CPR/DOP gate, a DFSAR polarimetry readiness audit, OHRC AOI-window hazard-readiness outputs, a DSC-1 doubly-shadowed-crater proxy target, a top-5-meter ice-volume scenario estimator, and dashboard pages that map each major requirement to evidence. The latest validation pass keeps three raw 2025 D32 full-pol DFSAR products staged, expands OHRC audit coverage to four strips, uses NASA PDS `LDEM_85S_20M`, adds a validation-gate harness for exact CPR/DOP and official AOI replacement, and now crops OHRC hazard candidates inside the active AOI window. The largest remaining gaps are exact CPR/DOP computation from calibrated polarimetric processing and replacement of proxy geometry with the official supplied-crater AOI.

## What We Have Right

| Requirement | Current status | Evidence |
| --- | --- | --- |
| Use Chandrayaan-2 DFSAR | Partial/strong | Processed 2020 DFSAR product is used for SAR evidence; three raw 2025 D32 full-pol products are staged for exact CPR/DOP processing. |
| Use Chandrayaan-2 OHRC | Partial/strong | Four OHRC products are downloaded; per-pixel geometry CSVs are audited; AOI-window crater/boulder hazard candidates are extracted against the active proxy harness. Exact official AOI certification is still pending. |
| South-pole terrain constraints | Strong | Valid south-pole TMC-2 DTM is processed into slope and accessibility layers. |
| Illumination/cold-trap reasoning | Partial | Low-sun hillshade proxy and cold-trap proxy exist. Needs ephemeris validation. |
| Landing site proposal | Partial/strong | LZ-A is selected as safer terrain gate with dynamic metric explanation. |
| Rover traverse | Strong prototype | A* route from LZ-A to SCI-B over accessibility and cold-trap proxy rasters. |
| Solar power constraints | Partial/strong | A* route now includes low-illumination solar-power penalty and reports low-power path percentage. |
| Doubly shadowed crater framing | Partial/strong | DSC-1 Faustini-class target proxy generated from cold-trap, shadow, illumination, slope, and accessibility layers. |
| Faustini/F2 mentor reference | Strong presentation / pending AOI | Dashboard now shows the mentor's F2-style ~1.1 km Faustini PSR reference model and separates it from the current DSC-1 proxy. |
| Lobate-rim morphology cue | Partial/strong | Lobate-rim cue is explicitly represented in the new reference layer and rough-terrain filter, but exact lobate-rim extraction still depends on official AOI registration. |
| Top 5 m volume estimate | Partial/strong | Scenario estimator reports low/medium/high water-equivalent volume from DSC-1 area x 5 m x ice fraction. |
| CPR/DOP threshold framing | Partial/strong | Dashboard shows CPR > 1 and DOP < 0.13 gate; DFSAR audit found HH/HV/VH/VV, phase-orthogonality metadata, and three raw full-pol D32 products, but exact CPR/DOP is not yet generated. |
| Validation gate readiness | Strong | `scripts/derive_validation_gates.py` checks raw D32 ZIP contents, exact CPR/DOP product presence, active AOI status, and OHRC footprint overlap against the active AOI. |
| Rough terrain false-positive rejection | Partial/strong | New morphology proxy rejects steep, low-access, SAR/cold-inconsistent terrain before candidate ranking. |
| Requirement visibility | Strong | A mentor expected-solution tracker and Problem 8 Compliance Board now map CPR/DOP, DFSAR audit, DSC-1 target, rough-terrain rejection, top-5m volume, solar-aware route, and OHRC hazard-readiness state. |
| Scientific honesty | Strong | Dashboard and docs explicitly state candidate ice, not confirmed ice; exact CPR/DOP is pending; LOLA validates terrain behavior but does not certify landing hazards; OHRC AOI-window hazards are not final landing certification. |
| External validation | Strong for terrain | NASA PDS `LDEM_85S_20M` slope comparison added; TMC mean slope 9.87 deg vs LOLA-derived 10.50 deg over the overlap. |
| Presentation clarity | Strong | Judge Demo Mode, source ledger, methodology cards, provenance cards, updated PDFs. |

## Main Gaps

| Requirement | Gap | Priority |
| --- | --- | --- |
| Doubly shadowed crater mapping | DSC-1 proxy exists, and a proxy AOI harness now exercises registration logic, but it is not yet validated against the official supplied crater AOI or named Faustini crater geometry. | High |
| CPR and DOP computation | CPR/DOP gate and readiness audit exist, and raw D32 full-pol `.dat` products are confirmed inside the ZIPs, but exact CPR and DOP still require calibrated polarimetric/MIDAS processing or supplied output rasters. | Critical |
| Ice-rich vs rough terrain distinction | Rough-terrain proxy and OHRC browse-scale hazard candidates now exist; final version still needs full-resolution registered OHRC boulder/crater extraction. | Medium |
| OHRC morphology and boulder distribution | AOI-window crater/boulder candidates exist from four OHRC geometry CSVs. Need official AOI replacement, exact map projection, and full-resolution roughness metrics. | High |
| Solar power constraints in route | Low-illumination penalty exists, but still needs ephemeris-grade illumination and rover power model. | Medium |
| Top 5 m ice volume estimate | Implemented as scenarios; needs recalibration after exact radar inversion. | Medium |
| Faustini / named crater framing | UI now shows the Faustini/F2 reference target; exact supplied crater metadata still pending. | Medium |
| MIDAS/ENVI/QGIS workflow alignment | We use Python/rasterio and document ISIS/QGIS path, but do not show MIDAS/ENVI processing. | Medium |

## Highest Impact Additions Before Final Round

1. Process the new raw D32 full-pol DFSAR products into exact CPR/DOP if the required calibration path or MIDAS workflow is available.

2. Complete OHRC certification.
   - Current state: per-pixel geometry CSVs are audited and active-AOI browse windows are used for crater/boulder hazard extraction.
   - Next state: replace the proxy harness with the official crater AOI, then map-project full-resolution OHRC footprints and intersect hazards with that official geometry.

3. Upgrade boulder and crater morphology extraction from browse proxy to registered full-resolution OHRC.

4. Upgrade volume estimate after radar inversion.
   - Current formula is `volume = candidate_area_m2 * 5 m * ice_fraction`.
   - Add dielectric/backscatter assumptions when exact radar parameters are available.

5. Validate DSC-1 against supplied crater metadata.
   - Current DSC-1 is proxy-generated and Faustini/F2-aligned.
   - Replace label/extent when official crater AOI arrives.
   - Add exact lobate-rim segmentation once registered OHRC footprint/AOI overlap is available.

## Suggested Final-Round Claim

This project does not claim confirmed lunar ice. It provides an auditable screening framework that fuses Chandrayaan-2 DFSAR radar evidence, CPR/DOP threshold logic, terrain safety, illumination/cold-trap context, rough-terrain rejection, NASA PDS LOLA validation, OHRC AOI-window hazard extraction, solar-aware A* traverse planning, and top-5m volume scenarios to prioritize a Faustini-class DSC-1 candidate subsurface-ice target. The next validation step is exact CPR/DOP computation and official crater AOI replacement once the supplied doubly shadowed crater geometry is provided.
