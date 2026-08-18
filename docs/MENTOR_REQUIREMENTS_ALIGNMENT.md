# Mentor Requirements Alignment

Source: `C:\Users\saatv\Downloads\PS 8 Lunal Ice.docx`

The attached mentor document is mostly embedded slide images. The extracted slide content emphasizes that this is not just a mapping problem; it is a mission-planning problem: move from orbital observations to an actionable exploration strategy.

## Newly Extracted Mentor Details Now Reflected In The Demo

- The reference target is an F2-style, approximately 1.1 km diameter doubly shadowed crater inside the Faustini permanently shadowed region.
- The morphology cue is a lobate rim / flow-like rim appearance, presented as a candidate indicator of subsurface-ice interaction.
- The radar cue is high Circular Polarization Ratio and low Degree of Polarization, specifically `CPR > 1` and `DOP < 0.13`.
- The mission-planner question is explicit: where to land, where to drive, where to excavate, and how much ice may be available.
- The expected solution steps include PSR/DSC mapping, DFSAR CPR/DOP analysis, OHRC morphology/slope/boulder/roughness analysis, terrain-safety screening, solar-aware traverse planning, and top 0-5 m ice-volume estimation.

## Mentor/Judge Signals

| Theme | Mentor emphasis | Current project state |
| --- | --- | --- |
| Mission framing | Discover hidden lunar ice deposits and design India's future robotic exploration strategy. | Dashboard now opens with a mentor expected-solution tracker and frames LZ-A to SCI-B/DSC-1 as a landing-to-science traverse recommendation. |
| Data fusion | Use DFSAR + OHRC data. | DFSAR is processed; three raw 2025 D32 full-pol products are staged for CPR/DOP upgrade; four OHRC geometry products are audited and AOI-window crater/boulder candidates are extracted against the active proxy harness. TMC-2 is additionally used for DTM/slope/traverse. |
| Subsurface ice detection | Analyze DFSAR to compute CPR and DOP; suggested refined criteria: `CPR > 1` and `DOP < 0.13`. | CPR/DOP gate is explicit. DFSAR audit found HH/HV/VH/VV, phase metadata, and new raw full-pol products, but exact CPR/DOP still requires calibrated polarimetric processing. |
| Doubly shadowed craters | Focus on an F2-style ~1.1 km crater within Faustini permanently shadowed region. | Dashboard now includes a Faustini/F2 reference target layer and uses `DSC-1 / Faustini-class target` framing. Official supplied crater AOI is still needed for exact validation. |
| Lobate-rim morphology | Mentor slides cite a lobate-rim crater as especially promising for subsurface ice. | Rough-terrain filtering and OHRC AOI-window hazard extraction now give visible morphology evidence; exact lobate-rim AOI validation still depends on the supplied crater geometry. |
| Rough terrain false positives | Distinguish ice-rich regions from rough, rocky terrains. | Slope/accessibility, PDS LOLA 20 m DEM roughness validation, rough-terrain rejection, and OHRC browse hazard candidates are now represented. |
| Landing site | Select a feasible landing site near scientifically relevant targets. | LZ-A is shown as landing gate; route uses terrain and illumination constraints. |
| Rover traverse | Design optimal and safe traverse path considering terrain hazards and solar power constraints. | A* traverse includes accessibility, cold-trap interest, and low-illumination solar-power penalty. |
| Ice volume | Estimate subsurface ice volume within top 0-5 m. | Scenario estimator reports low/medium/high volume cases for top 5 m. |
| Expected outputs | High-probability ice regions, radar framework, landing site, rover path, quantitative ice volume. | All are represented as prototype outputs with scientific caveats. |

## Most Important Remaining Work

1. Process the new raw D32 full-pol DFSAR products into exact CPR/DOP if calibration/MIDAS workflow support is available.
2. Replace DSC-1 proxy geometry with the official Faustini/F2 supplied crater AOI.
3. Replace the proxy AOI with the official supplied crater AOI, then map-project OHRC footprints against it.
4. Upgrade AOI-window OHRC hazard candidates into full-resolution registered crater/boulder and lobate-rim extraction.
5. Add dielectric/backscatter assumptions to recalibrate top-5m volume scenarios.

## Recommended Judging Claim

Lunar Ice Intelligence is an auditable mission-planning prototype for Problem Statement 8. It screens a Faustini-class doubly shadowed crater candidate using Chandrayaan-2 DFSAR radar evidence, explicit CPR/DOP threshold logic, a DFSAR polarimetry audit, four-strip OHRC AOI-window hazard-readiness outputs, terrain and illumination constraints, NASA PDS LOLA validation, rough-terrain rejection, solar-aware A* traverse planning, and top-5m ice-volume scenarios. It does not claim confirmed ice; it ranks candidate excavation targets for follow-up once calibrated polarimetric products and official crater AOI metadata are supplied.
