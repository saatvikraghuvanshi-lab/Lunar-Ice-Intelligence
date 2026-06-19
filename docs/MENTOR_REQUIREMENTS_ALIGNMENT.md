# Mentor Requirements Alignment

Source: `C:\Users\saatv\Downloads\PS 8 Lunal Ice.docx`

The attached mentor document is mostly embedded slide images. The extracted slide content emphasizes that this is not just a mapping problem; it is a mission-planning problem.

## Mentor/Judge Signals

| Theme | Mentor emphasis | Current project state |
| --- | --- | --- |
| Mission framing | Discover hidden lunar ice deposits and design India's future robotic exploration strategy. | Dashboard now frames LZ-A to SCI-B/DSC-1 as a landing-to-science traverse recommendation. |
| Data fusion | Use DFSAR + OHRC data. | DFSAR is processed; OHRC geometry is audited and browse-scale crater/boulder candidates are extracted. TMC-2 is additionally used for DTM/slope/traverse. |
| Subsurface ice detection | Analyze DFSAR to compute CPR and DOP; suggested refined criteria: `CPR > 1` and `DOP < 0.13`. | CPR/DOP gate is explicit. DFSAR audit found HH/HV/VH/VV and phase metadata, but exact CPR/DOP products were not found in the extracted package, so the system marks this as threshold-ready proxy evidence. |
| Doubly shadowed craters | Focus on doubly shadowed craters within Faustini permanently shadowed region. | Dashboard now uses `DSC-1 / Faustini-class target` framing. Official supplied crater AOI is still needed for exact validation. |
| Lobate-rim morphology | Mentor slides cite a lobate-rim crater as especially promising for subsurface ice. | Rough-terrain filtering and OHRC browse-scale hazard extraction now give visible morphology evidence; exact lobate-rim AOI validation still depends on the supplied crater geometry. |
| Rough terrain false positives | Distinguish ice-rich regions from rough, rocky terrains. | Slope/accessibility, LOLA roughness validation, rough-terrain rejection, and OHRC browse hazard candidates are now represented. |
| Landing site | Select a feasible landing site near scientifically relevant targets. | LZ-A is shown as landing gate; route uses terrain and illumination constraints. |
| Rover traverse | Design optimal and safe traverse path considering terrain hazards and solar power constraints. | A* traverse includes accessibility, cold-trap interest, and low-illumination solar-power penalty. |
| Ice volume | Estimate subsurface ice volume within top 0-5 m. | Scenario estimator reports low/medium/high volume cases for top 5 m. |
| Expected outputs | High-probability ice regions, radar framework, landing site, rover path, quantitative ice volume. | All are represented as prototype outputs with scientific caveats. |

## Most Important Remaining Work

1. Replace CPR/DOP proxy with exact products if supplied crater data includes CPR/DOP, Stokes, coherency, covariance, circular-pol, or official MIDAS outputs.
2. Replace DSC-1 proxy geometry with the official supplied crater AOI.
3. Map-project OHRC footprints and intersect them with the official AOI.
4. Upgrade browse-scale OHRC hazard candidates into full-resolution registered crater/boulder extraction.
5. Add dielectric/backscatter assumptions to recalibrate top-5m volume scenarios.

## Recommended Judging Claim

Lunar Ice Intelligence is an auditable mission-planning prototype for Problem Statement 8. It screens a Faustini-class doubly shadowed crater candidate using Chandrayaan-2 DFSAR radar evidence, explicit CPR/DOP threshold logic, a DFSAR polarimetry audit, OHRC footprint/hazard-readiness outputs, terrain and illumination constraints, LOLA validation, rough-terrain rejection, solar-aware A* traverse planning, and top-5m ice-volume scenarios. It does not claim confirmed ice; it ranks candidate excavation targets for follow-up once calibrated polarimetric products and official crater AOI metadata are supplied.
