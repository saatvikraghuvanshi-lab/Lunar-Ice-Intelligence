# Mentor Requirements Alignment

Source: `C:\Users\saatv\Downloads\PS 8 Lunal Ice.docx`

The attached mentor document is mostly embedded slide images. The extracted slide content emphasizes that this is not just a mapping problem; it is a mission-planning problem.

## Mentor/Judge Signals

| Theme | Mentor emphasis | Current project state |
| --- | --- | --- |
| Mission framing | Discover hidden lunar ice deposits and design India's future robotic exploration strategy. | Dashboard now frames LZ-A to SCI-B/DSC-1 as a landing-to-science traverse recommendation. |
| Data fusion | Use DFSAR + OHRC data. | DFSAR is processed; OHRC is retained as context until footprint registration is complete. TMC-2 is additionally used for DTM/slope/traverse. |
| Subsurface ice detection | Analyze DFSAR to compute CPR and DOP; suggested refined criteria: `CPR > 1` and `DOP < 0.13`. | CPR/DOP gate is explicit. Exact CPR/DOP is pending because current extracted rasters are intensity-only, so the system marks this as threshold-ready proxy evidence. |
| Doubly shadowed craters | Focus on doubly shadowed craters within Faustini permanently shadowed region. | Dashboard now uses `DSC-1 / Faustini-class target` framing. Official supplied crater AOI is still needed for exact validation. |
| Lobate-rim morphology | Mentor slides cite a lobate-rim crater as especially promising for subsurface ice. | Needs stronger UI representation. Add a morphology/roughness false-positive filter and call out lobate-rim evidence. |
| Rough terrain false positives | Distinguish ice-rich regions from rough, rocky terrains. | Slope/accessibility and LOLA roughness validation exist. Needs clearer "rough terrain rejection" layer in the dashboard. |
| Landing site | Select a feasible landing site near scientifically relevant targets. | LZ-A is shown as landing gate; route uses terrain and illumination constraints. |
| Rover traverse | Design optimal and safe traverse path considering terrain hazards and solar power constraints. | A* traverse includes accessibility, cold-trap interest, and low-illumination solar-power penalty. |
| Ice volume | Estimate subsurface ice volume within top 0-5 m. | Scenario estimator reports low/medium/high volume cases for top 5 m. |
| Expected outputs | High-probability ice regions, radar framework, landing site, rover path, quantitative ice volume. | All are represented as prototype outputs with scientific caveats. |

## Most Important Remaining Work

1. Add a visible rough-terrain / morphology false-positive filter.
2. Strengthen Faustini / lobate-rim crater framing in the first viewport and Judge Demo Mode.
3. Keep CPR/DOP honest: threshold-ready proxy now, exact when supplied crater data includes required polarimetric products.
4. Add drill/excavation wording to the recommendation, not only "science target."
5. Keep OHRC as pending registration until footprint overlap is proven.

## Recommended Judging Claim

Lunar Ice Intelligence is an auditable mission-planning prototype for Problem Statement 8. It screens a Faustini-class doubly shadowed crater candidate using Chandrayaan-2 DFSAR radar evidence, explicit CPR/DOP threshold logic, terrain and illumination constraints, LOLA validation, rough-terrain rejection, solar-aware A* traverse planning, and top-5m ice-volume scenarios. It does not claim confirmed ice; it ranks candidate excavation targets for follow-up once calibrated polarimetric products and official crater AOI metadata are supplied.
