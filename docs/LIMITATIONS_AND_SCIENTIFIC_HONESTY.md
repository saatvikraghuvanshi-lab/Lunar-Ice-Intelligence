# Limitations and Scientific Honesty

Date: 2026-06-27

This project is a mission-planning and candidate-screening prototype. It does not claim confirmed lunar water ice. The strongest current claim is that the system ranks evidence-consistent excavation candidates and shows exactly which validation gates must close before a scientific confirmation claim is defensible.

## Current Claim Level

| Output | Current claim | Do not claim |
| --- | --- | --- |
| SCI-B / DSC-1 candidate | High-priority candidate subsurface-ice target for follow-up | Confirmed water ice |
| CPR/DOP gate | Required `CPR > 1` and `DOP < 0.13` logic is implemented as an explicit validation gate | Exact calibrated CPR/DOP has been computed |
| Experimental CPR/DOP proxy | HH/HV/VH/VV-derived screening proxy that narrows radar candidates | MIDAS-grade or mission-grade polarimetry |
| Official crater AOI | Proxy registration harness is active and ready to be replaced | Official supplied crater geometry is already integrated |
| OHRC hazards | AOI-window browse-scale crater/boulder candidates are extracted from four OHRC geometry products | Full-resolution certified landing hazard map |
| LOLA validation | Independent terrain sanity check using NASA PDS LDEM_85S_20M | Meter-scale landing safety certification |
| Cold-trap / illumination | Low-sun hillshade proxy for volatile plausibility and rover power risk | Ephemeris-grade PSR/illumination solution |
| Top 0-5 m ice volume | Scenario estimate from area, 5 m depth, and assumed ice fraction | Measured resource reserve |
| Rover traverse | A* planning recommendation over screening layers | Executable rover command path |

## Three Hard Validation Gates

1. **Exact CPR/DOP**

   The dashboard currently shows the required scientific thresholds and an experimental proxy mask. Exact CPR/DOP remains pending because the available D32 products are raw full-pol `.dat` echo products, not calibrated map-projected CPR/DOP rasters. A defensible final claim needs official/MIDAS-style CPR and DOP products, or a validated calibration workflow that produces them.

2. **Official supplied crater AOI**

   The active AOI is `data/aoi/dsc1_proxy_registration_harness.geojson`. It exists so the pipeline, UI, and OHRC registration logic can be tested end-to-end. When the mentor/ISRO supplied crater boundary is available, place it at `data/aoi/official_crater_aoi.geojson`; the validation scripts automatically prefer it.

3. **OHRC full-resolution hazard certification**

   The current OHRC upgrade uses geometry CSVs to crop AOI-window hazard candidates from four downloaded OHRC strips. This is much stronger than generic visual context, but it is still browse-scale. Final landing certification needs map-projected full-resolution OHRC extraction inside the official crater AOI, with crater/boulder/lobate-rim metrics.

## Why These Limitations Help The Pitch

- They prevent the team from overstating evidence as confirmed ice.
- They show the judges that the system is designed for scientific replacement: proxy outputs can be swapped for exact products without changing the architecture.
- They make the final recommendation credible: land at LZ-A, prioritize SCI-B/DSC-1, and use the A* route as a planning concept while exact polarimetry and official AOI validation close.

## Presenter Script

> We are not claiming confirmed lunar ice. We are showing an auditable pipeline that moves from Chandrayaan-2 orbital evidence to a mission-planning recommendation. The hard validation gates are exact CPR/DOP, official crater AOI replacement, and full-resolution OHRC hazard certification. Until those close, our output is a ranked candidate excavation strategy, not a discovery claim.

