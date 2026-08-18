# Lunar Ice Intelligence

Mission-planning prototype for **Problem Statement 8: Detection and Characterization of Subsurface Ice in Lunar South Polar Regions Using Chandrayaan-2 Radar and Imagery Data for Landing Site and Rover Traverse Planning**.

The system fuses Chandrayaan-2 DFSAR radar evidence, TMC-2 terrain products, OHRC footprint/hazard-readiness outputs, illumination/cold-trap proxies, NASA LOLA validation, rough-terrain rejection, solar-aware A* routing, top-5m ice-volume scenarios, and mentor-DOCX requirements from the Problem Statement 8 briefing.

**Live demo: https://lunar-ice-intelligence.onrender.com/**

## Current Scientific Claim

This project does **not** claim confirmed lunar water ice.

It provides an auditable screening and mission-planning workflow for ranking candidate subsurface-ice targets in a Faustini-class doubly shadowed crater setting.

The dashboard now explicitly tracks the mentor's Faustini/F2-style reference target: a ~1.1 km doubly shadowed crater in Faustini PSR with lobate-rim morphology, high CPR, and low DOP as the reference pattern.

## What The Demo Shows

- CPR/DOP threshold gate: `CPR > 1` and `DOP < 0.13` are explicit.
- Validation Gate Readiness layer for the three hard blockers: exact CPR/DOP, official supplied crater AOI, and OHRC map-projected registration.
- Mentor expected-solution tracker for PSR/DSC mapping, CPR/DOP, OHRC morphology, terrain safety, solar-aware traverse, and top 0-5 m volume.
- Faustini/F2 reference model and lobate-rim morphology cue.
- DFSAR polarimetry audit: four calibrated linear polarizations and phase metadata are present; three raw 2025 D32 full-pol products are staged for the CPR/DOP upgrade; exact CPR/DOP products are not yet generated.
- Active AOI harness: `data/aoi/dsc1_proxy_registration_harness.geojson` is used only until `data/aoi/official_crater_aoi.geojson` is supplied.
- DSC-1 / Faustini-class doubly shadowed crater proxy target.
- OHRC footprint audit and browse-scale crater/boulder hazard candidates across four 2026-01-03 strips.
- Rough-terrain false-positive rejection before candidate ranking.
- TMC-2 slope/accessibility terrain safety.
- NASA PDS LRO/LOLA LDEM_85S_20M external terrain validation.
- Cold-trap and illumination proxy.
- Solar-aware A* traverse from LZ-A to SCI-B/DSC-1.
- Top 5 m volume scenarios: 3%, 8%, and 15% assumed ice fraction.
- Limitations and scientific honesty panel.

## Live Deployment

The app is live at **https://lunar-ice-intelligence.onrender.com/**, hosted on **Render** from the `web/` directory (build command `npm install && npm run build`). The Next.js auth shell and the same-origin evidence dashboard are served together, so the whole system is one URL.

Notes:

- Render's **free tier spins the instance down after inactivity** — the first request after idle can take ~50 seconds to wake up.
- If `DATABASE_URL` is not set on Render, auth uses the JSON user store (`web/.local/users.json`), which is **ephemeral** on Render's disk: accounts and sessions reset whenever the instance restarts or redeploys. To get persistent accounts, set `DATABASE_URL` to a hosted Postgres (Neon/Supabase), then run `cd web && npx prisma db push` once.
- Build gotcha: Render installs with `NODE_ENV=production`, which omits devDependencies. Tailwind's PostCSS plugin and the TypeScript toolchain therefore live in `dependencies` (see `web/package.json`), not devDependencies.

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

The evidence console requires a signed-in session. Login/signup are rate-limited per IP, sessions are revocable via logout, and security headers (CSP, HSTS in production, frame/referrer/permissions policies) are applied in `web/next.config.ts`.

## Alternative Host: Vercel

Render is the current host; the app is also Vercel-ready if you prefer it there. The Next.js app lives in `web/`, and the evidence dashboard ships inside it (`web/public/demo/`), so **one Vercel deploy hosts everything** — no separate static server, no `localhost` dependencies. The Next.js app lives in `web/`, and the evidence dashboard ships inside it (`web/public/demo/`), so **one Vercel deploy hosts everything** — no separate static server, no `localhost` dependencies.

1. Push the repo to GitHub.
2. In Vercel, **Add New Project → Import** the repo, and set **Root Directory** to `web` (the Next.js project).
3. Create a free PostgreSQL database: **Vercel Postgres** (easiest — one free database on the Hobby plan, created in Vercel's Storage tab, env vars auto-injected) or **Supabase / Neon** (free tiers) and copy its connection string.
4. Make sure `DATABASE_URL` is set in Vercel project settings → **Environment Variables** (Vercel Postgres adds it automatically). This is **required** — without it, the app falls back to a local JSON user store, which does not persist on serverless.
5. Push the schema once: `cd web && npx prisma db push` with `DATABASE_URL` set to the same connection string.
6. **Deploy.**

Local development needs no database: `npm run dev` uses the JSON store in `web/.local/users.json` (gitignored). The Prisma path activates only when `DATABASE_URL` starts with `postgres`.

## Data Policy

Raw Chandrayaan-2 archives, extracted GeoTIFF rasters, virtual environments, and build caches are intentionally not tracked in GitHub.

See [data/DATA_MANIFEST.md](data/DATA_MANIFEST.md) for the local raw-data layout and required products.

## Key Documents

- [Problem Statement 8 Compliance](docs/PROBLEM_STATEMENT_8_COMPLIANCE.md)
- [Mentor Requirements Alignment](docs/MENTOR_REQUIREMENTS_ALIGNMENT.md)
- [Radar CPR/DOP Readiness](docs/RADAR_CPR_DOP_READINESS.md)
- [Limitations and Scientific Honesty](docs/LIMITATIONS_AND_SCIENTIFIC_HONESTY.md)
- [Data Manifest](data/DATA_MANIFEST.md)
- [Runbook](RUNBOOK.md)
- [Source Audit](SOURCE_AUDIT.md)

## Remaining High-Priority Work

1. Process the new raw D32 full-pol DFSAR products through a calibrated polarimetric/MIDAS path and replace the CPR/DOP proxy with exact CPR and DOP.
2. Replace DSC-1 proxy with the official supplied crater AOI at `data/aoi/official_crater_aoi.geojson`.
3. Run `scripts/derive_validation_gates.py` after the official AOI or exact CPR/DOP outputs are added.
4. Map-project OHRC footprints against the official AOI and upgrade browse-scale hazard candidates to full-resolution registered extraction.
5. Add exact lobate-rim and boulder/crater segmentation after registered OHRC AOI overlap is available.
6. Recalibrate ice-volume scenarios after exact radar inversion.
