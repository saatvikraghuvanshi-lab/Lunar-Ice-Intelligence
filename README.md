# Lunar Ice Intelligence

Mission-planning prototype for **Problem Statement 8: Detection and Characterization of Subsurface Ice in Lunar South Polar Regions Using Chandrayaan-2 Radar and Imagery Data for Landing Site and Rover Traverse Planning**.

The system fuses Chandrayaan-2 DFSAR radar evidence, TMC-2 terrain products, OHRC context, illumination/cold-trap proxies, NASA LOLA validation, rough-terrain rejection, solar-aware A* routing, and top-5m ice-volume scenarios.

## Current Scientific Claim

This project does **not** claim confirmed lunar water ice.

It provides an auditable screening and mission-planning workflow for ranking candidate subsurface-ice targets in a Faustini-class doubly shadowed crater setting.

## What The Demo Shows

- CPR/DOP threshold gate: `CPR > 1` and `DOP < 0.13` are explicit.
- DSC-1 / Faustini-class doubly shadowed crater proxy target.
- Rough-terrain false-positive rejection before candidate ranking.
- TMC-2 slope/accessibility terrain safety.
- NASA LRO/LOLA coarse validation.
- Cold-trap and illumination proxy.
- Solar-aware A* traverse from LZ-A to SCI-B/DSC-1.
- Top 5 m volume scenarios: 3%, 8%, and 15% assumed ice fraction.
- Limitations and scientific honesty panel.

## Run Locally

Static evidence dashboard:

```powershell
python -m http.server 8765
```

Open:

```text
http://localhost:8765/demo/index.html
```

Next.js auth/product shell:

```powershell
cd web
npm install
npm run dev
```

Open:

```text
http://127.0.0.1:3001/signup
```

Temporary hackathon behavior: sign-in can route directly to the evidence dashboard without credentials.

## Data Policy

Raw Chandrayaan-2 archives, extracted GeoTIFF rasters, virtual environments, and build caches are intentionally not tracked in GitHub.

See [data/DATA_MANIFEST.md](data/DATA_MANIFEST.md) for the local raw-data layout and required products.

## Key Documents

- [Problem Statement 8 Compliance](docs/PROBLEM_STATEMENT_8_COMPLIANCE.md)
- [Mentor Requirements Alignment](docs/MENTOR_REQUIREMENTS_ALIGNMENT.md)
- [Radar CPR/DOP Readiness](docs/RADAR_CPR_DOP_READINESS.md)
- [Data Manifest](data/DATA_MANIFEST.md)
- [Runbook](RUNBOOK.md)
- [Source Audit](SOURCE_AUDIT.md)

## Remaining High-Priority Work

1. Replace CPR/DOP proxy with exact CPR and DOP if supplied DFSAR crater data includes required polarimetric terms or MIDAS outputs.
2. Register OHRC footprints against DFSAR/TMC-2 AOI.
3. Add OHRC boulder/crater morphology extraction after registration.
4. Recalibrate ice-volume scenarios after exact radar inversion.
5. Use official supplied crater AOI to replace the current DSC-1 proxy geometry.
