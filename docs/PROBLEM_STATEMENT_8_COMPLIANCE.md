# Problem Statement 8 Compliance Review

Date: 2026-06-20

## Overall Status

Current compliance after the June 20 science-readiness pass: about 88-91%.

The project is strong as a decision-support prototype: it uses downloaded Chandrayaan-2 DFSAR, TMC-2, and OHRC files; it has radar evidence layers, terrain constraints, illumination/cold-trap proxies, LOLA validation, a rough-terrain false-positive filter, a solar-aware A* traverse, a judge demo mode, explicit scientific honesty, a Problem Statement 8 CPR/DOP gate, a DFSAR polarimetry readiness audit, OHRC footprint/hazard-readiness outputs, a DSC-1 doubly-shadowed-crater proxy target, a top-5-meter ice-volume scenario estimator, and a dashboard compliance board that maps each major requirement to evidence. The largest remaining gaps are exact CPR/DOP computation from fully calibrated polarimetric products and replacement of proxy geometry with the official supplied-crater AOI.

## What We Have Right

| Requirement | Current status | Evidence |
| --- | --- | --- |
| Use Chandrayaan-2 DFSAR | Partial/strong | DFSAR product is downloaded and processed into SAR candidate evidence layers. |
| Use Chandrayaan-2 OHRC | Partial/strong | OHRC products are downloaded; per-pixel geometry CSVs are audited; browse-scale crater/boulder hazard candidates are extracted. Exact official AOI registration is still pending. |
| South-pole terrain constraints | Strong | Valid south-pole TMC-2 DTM is processed into slope and accessibility layers. |
| Illumination/cold-trap reasoning | Partial | Low-sun hillshade proxy and cold-trap proxy exist. Needs ephemeris validation. |
| Landing site proposal | Partial/strong | LZ-A is selected as safer terrain gate with dynamic metric explanation. |
| Rover traverse | Strong prototype | A* route from LZ-A to SCI-B over accessibility and cold-trap proxy rasters. |
| Solar power constraints | Partial/strong | A* route now includes low-illumination solar-power penalty and reports low-power path percentage. |
| Doubly shadowed crater framing | Partial/strong | DSC-1 Faustini-class target proxy generated from cold-trap, shadow, illumination, slope, and accessibility layers. |
| Top 5 m volume estimate | Partial/strong | Scenario estimator reports low/medium/high water-equivalent volume from DSC-1 area x 5 m x ice fraction. |
| CPR/DOP threshold framing | Partial/strong | Dashboard shows CPR > 1 and DOP < 0.13 gate; DFSAR audit found HH/HV/VH/VV and phase-orthogonality metadata, but no exact CPR/DOP/Stokes/coherency products in the extracted set. |
| Rough terrain false-positive rejection | Partial/strong | New morphology proxy rejects steep, low-access, SAR/cold-inconsistent terrain before candidate ranking. |
| Requirement visibility | Strong | A Problem 8 Compliance Board now maps CPR/DOP, DFSAR audit, DSC-1 target, rough-terrain rejection, top-5m volume, solar-aware route, and OHRC hazard-readiness state. |
| Scientific honesty | Strong | Dashboard and terms explicitly state candidate ice, not confirmed ice; LOLA is coarse validation; OHRC overlap needs registration. |
| External validation | Strong for terrain | NASA PGDA/LRO LOLA slope comparison added; TMC mean slope 10.67 deg vs LOLA 11.63 deg. |
| Presentation clarity | Strong | Judge Demo Mode, source ledger, methodology cards, provenance cards, updated PDFs. |

## Main Gaps

| Requirement | Gap | Priority |
| --- | --- | --- |
| Doubly shadowed crater mapping | DSC-1 proxy exists, but it is not yet validated against the official supplied crater AOI or named Faustini crater geometry. | High |
| CPR and DOP computation | CPR/DOP gate and readiness audit exist, but exact CPR and DOP are not computed because no exact CPR/DOP/Stokes/coherency product files were found in the current extracted package. | Critical |
| Ice-rich vs rough terrain distinction | Rough-terrain proxy and OHRC browse-scale hazard candidates now exist; final version still needs full-resolution registered OHRC boulder/crater extraction. | Medium |
| OHRC morphology and boulder distribution | Browse-scale crater/boulder candidates exist and geometry CSVs are audited. Need exact map-projected registration to official crater AOI and full-resolution roughness metrics. | High |
| Solar power constraints in route | Low-illumination penalty exists, but still needs ephemeris-grade illumination and rover power model. | Medium |
| Top 5 m ice volume estimate | Implemented as scenarios; needs recalibration after exact radar inversion. | Medium |
| Faustini / named crater framing | UI now says Faustini-class DSC-1; exact supplied crater metadata still pending. | Medium |
| MIDAS/ENVI/QGIS workflow alignment | We use Python/rasterio and document ISIS/QGIS path, but do not show MIDAS/ENVI processing. | Medium |

## Highest Impact Additions Before Final Round

1. Replace CPR/DOP proxy with exact CPR/DOP if supplied crater data includes required polarimetric terms or official MIDAS outputs.

2. Complete OHRC registration.
   - Current state: per-pixel geometry CSVs are audited and regional latitude overlap is confirmed.
   - Next state: map-project footprints and intersect with the official crater AOI.

3. Upgrade boulder and crater morphology extraction from browse proxy to registered full-resolution OHRC.

4. Upgrade volume estimate after radar inversion.
   - Current formula is `volume = candidate_area_m2 * 5 m * ice_fraction`.
   - Add dielectric/backscatter assumptions when exact radar parameters are available.

5. Validate DSC-1 against supplied crater metadata.
   - Current DSC-1 is proxy-generated and Faustini-class.
   - Replace label/extent when official crater AOI arrives.

## Suggested Final-Round Claim

This project does not claim confirmed lunar ice. It provides an auditable screening framework that fuses Chandrayaan-2 DFSAR radar evidence, CPR/DOP threshold logic, terrain safety, illumination/cold-trap context, rough-terrain rejection, external LOLA validation, solar-aware A* traverse planning, and top-5m volume scenarios to prioritize a Faustini-class DSC-1 candidate subsurface-ice target. The next validation step is exact CPR/DOP computation and official crater AOI registration once the supplied doubly shadowed crater DFSAR product is provided.
