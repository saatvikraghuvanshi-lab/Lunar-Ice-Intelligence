from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)

PROJECT_NAME = "Lunar Ice Intelligence System"
PROBLEM_TITLE = (
    "Detection and Characterization of Subsurface Ice in Lunar South Polar Regions "
    "Using Chandrayaan-2 Radar and Imagery Data for Landing Site and Rover Traverse Planning"
)

SOURCES = [
    (
        "ISRO Science Data Archive - Chandrayaan-2 PRADAN",
        "https://pradan.issdc.gov.in/ch2/",
    ),
    (
        "ISSDC Chandrayaan-2 mission data page",
        "https://www.issdc.gov.in/chandrayaan2.html",
    ),
    (
        "ISRO DFSAR subsurface-ice release, May 27, 2026",
        "https://www.isro.gov.in/Chandrayaan2_Dual_Frequency_Synthetic_Aperture_Radar.html",
    ),
    (
        "Chandrayaan-2 Map Browse",
        "https://chmapbrowse.issdc.gov.in",
    ),
    (
        "VEDAS note on downloading Chandrayaan-2 OHRC products",
        "https://vedas.sac.gov.in/static/pdf/SIH_2024/SIH1732_CH2_PS.pdf",
    ),
    (
        "NASA Planetary Data System Geosciences Node",
        "https://pds-geosciences.wustl.edu/",
    ),
    (
        "NASA PGDA LRO LOLA south-pole products",
        "https://pgda.gsfc.nasa.gov/products/90",
    ),
    (
        "USGS ISIS planetary image processing",
        "https://isis.astrogeology.usgs.gov/",
    ),
]

LOLA_VALIDATION = (
    "External validation now uses NASA PGDA/LRO LOLA south-pole slope, roughness, "
    "and terrain-class products cropped to the Chandrayaan-2 TMC-2 AOI. The TMC-derived "
    "mean slope is 10.67 deg, the LOLA mean slope is 11.63 deg, and the mean difference "
    "is 0.96 deg. Because LOLA is 1000 m/pixel, this is a regional sanity check, not "
    "meter-scale hazard validation."
)

ASTAR_ROUTE = (
    "The prototype route from LZ-A to SCI-B is generated with A* over downsampled "
    "TMC-2 accessibility and cold-trap proxy rasters. The route has 50 path pixels and "
    "a relative cost of 151.74. It is a screening route for judge demonstration and "
    "needs geodetic calibration, obstacle inflation, and rover dynamics before mission use."
)


def styles():
    base = getSampleStyleSheet()
    base.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=28,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#11243f"),
            spaceAfter=18,
        )
    )
    base.add(
        ParagraphStyle(
            name="CoverSub",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#3f4d63"),
            spaceAfter=20,
        )
    )
    base.add(
        ParagraphStyle(
            name="H1x",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            textColor=colors.HexColor("#16345b"),
            spaceBefore=12,
            spaceAfter=7,
        )
    )
    base.add(
        ParagraphStyle(
            name="H2x",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11.5,
            leading=15,
            textColor=colors.HexColor("#1f5f78"),
            spaceBefore=9,
            spaceAfter=5,
        )
    )
    base.add(
        ParagraphStyle(
            name="Bodyx",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.6,
            textColor=colors.HexColor("#202938"),
            spaceAfter=5,
        )
    )
    base.add(
        ParagraphStyle(
            name="Bulletx",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=13.2,
            leftIndent=14,
            firstLineIndent=-8,
            textColor=colors.HexColor("#202938"),
            spaceAfter=4,
        )
    )
    base.add(
        ParagraphStyle(
            name="Smallx",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=6.8,
            leading=8.4,
            textColor=colors.HexColor("#526173"),
            spaceAfter=1.5,
        )
    )
    base.add(
        ParagraphStyle(
            name="Cellx",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=10.5,
            textColor=colors.HexColor("#202938"),
        )
    )
    base.add(
        ParagraphStyle(
            name="CellHeadx",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10.5,
            textColor=colors.white,
        )
    )
    return base


STY = styles()


def P(text, style="Bodyx"):
    return Paragraph(text, STY[style])


def bullet(text):
    return P("- " + text, "Bulletx")


def table(rows, widths=None):
    styled = []
    for r, row in enumerate(rows):
        style = "CellHeadx" if r == 0 else "Cellx"
        styled.append([P(str(cell), style) for cell in row])
    t = Table(styled, colWidths=widths, hAlign="LEFT", repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#16345b")),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#d3dae5")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f6f8fb")]),
            ]
        )
    )
    return t


def dashboard_capabilities_table():
    return table(
        [
            ["Capability", "Current implementation", "Judge value"],
            [
                "LOLA validation",
                "Independent NASA PGDA/LRO LOLA slope, roughness, and terrain-class layers are cropped to the TMC-2 AOI.",
                "Shows that the terrain pipeline is being checked against a trusted external reference, not only self-generated layers.",
            ],
            [
                "Judge Demo Mode",
                "Seven guided steps walk through the problem, DFSAR evidence, TMC-2 safety, LOLA validation, cold-trap proxy, A* traverse, and final recommendation.",
                "Turns the dashboard into a crisp story that can be presented reliably under time pressure.",
            ],
            [
                "A* route",
                "Route from LZ-A to SCI-B is computed from accessibility and cold-trap cost layers instead of being hand drawn.",
                "Connects science target selection to operational rover planning.",
            ],
            [
                "Dynamic metrics",
                "Confidence ring, candidate ranking, traverse bars, plan label, and processing-chain text change with the selected layer.",
                "Makes the evidence stack feel alive and auditable instead of static.",
            ],
            [
                "Source ledger",
                "Every source is marked as used, validation, context, roadmap, or deprecated with a concrete contribution.",
                "Builds credibility and prevents overclaiming.",
            ],
        ],
        [1.15 * inch, 3.0 * inch, 2.45 * inch],
    )


def source_ledger_table():
    return table(
        [
            ["Source", "Status", "Contribution"],
            ["ISRO PRADAN", "Used", "Official Chandrayaan-2 DFSAR, TMC-2, and OHRC product downloads."],
            ["Chandrayaan-2 Map Browse", "Used", "AOI/product discovery and south-pole footprint selection."],
            ["DFSAR science release", "Science anchor", "CPR/DOP interpretation target; current prototype uses ratio-based candidate evidence."],
            ["TMC-2 south-pole DTM/orthobrowse", "Used", "Slope, accessibility, hillshade, cold-trap proxy, and route cost layers."],
            ["OHRC", "Context", "High-resolution visual hazard context until exact footprint registration is complete."],
            ["NASA PGDA/LRO LOLA", "Used for validation", "Independent 1000 m/pixel slope, roughness, and class sanity check."],
            ["USGS ISIS", "Roadmap", "Production-grade planetary projection/calibration path documented for later hardening."],
        ],
        [1.55 * inch, 1.15 * inch, 3.9 * inch],
    )


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#526173"))
    canvas.drawString(0.65 * inch, 0.42 * inch, PROJECT_NAME)
    canvas.drawRightString(7.62 * inch, 0.42 * inch, f"Page {doc.page}")
    canvas.restoreState()


def make_doc(filename, title, subtitle, body):
    path = OUT / filename
    doc = BaseDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=0.65 * inch,
        rightMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        title=title,
        author="Codex",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="main", frames=frame, onPage=footer)])
    story = [
        Spacer(1, 0.15 * inch),
        P(title, "CoverTitle"),
        P(subtitle, "CoverSub"),
        Spacer(1, 0.08 * inch),
    ]
    story.extend(body)
    story.append(Spacer(1, 0.08 * inch))
    story.append(P("Source Links", "H2x"))
    for label, url in SOURCES:
        story.append(P(f'<link href="{url}" color="blue">{label}</link>: {url}', "Smallx"))
    doc.build(story)
    return path


def prd_body():
    return [
        P("1. Product Vision", "H1x"),
        P(
            "Build a decision-support platform that fuses Chandrayaan-2 DFSAR radar, OHRC/TMC-2 imagery, terrain, illumination, and scientific priors to identify candidate subsurface ice zones in lunar south-polar permanently shadowed regions and convert them into actionable landing-site and rover-traverse recommendations."
        ),
        P("2. Success Definition", "H1x"),
        bullet("A judge can select a lunar south-pole area and immediately see ice-likelihood, terrain hazards, landing safety, and traverse feasibility."),
        bullet("The system explains every recommendation using visible evidence layers rather than presenting a black-box score."),
        bullet("A demo can run on preprocessed public sample data even if live PRADAN downloads are not available during judging."),
        P("3. Users", "H1x"),
        table(
            [
                ["User", "Primary Need", "Product Response"],
                ["Mission planner", "Shortlist safe and useful landing zones", "Ranked sites with safety, science value, and resource-potential scores"],
                ["Planetary scientist", "Inspect evidence for possible subsurface ice", "Layer-by-layer radar, morphology, slope, shadow, and confidence views"],
                ["Rover operations team", "Plan traverses that avoid hazards", "Cost-aware path planning with slope, illumination, communication, and science targets"],
                ["Hackathon judge", "Understand value quickly", "Interactive dashboard, explanation panel, and downloadable mission brief"],
            ],
            [1.2 * inch, 2.0 * inch, 3.4 * inch],
        ),
        P("4. Core Features", "H1x"),
        table(
            [
                ["Feature", "MVP Scope", "Stretch Scope"],
                ["AOI explorer", "South-pole dashboard with DFSAR, TMC-2, OHRC context, LOLA validation, cold-trap, and route layers", "Draw custom AOI and fetch matching PDS products"],
                ["Ice likelihood", "Evidence-weighted candidate score using radar ratios, cold-trap proxy, and terrain context", "Bayesian uncertainty and calibration against published candidate craters"],
                ["Landing suitability", "TMC-2 slope/accessibility with LOLA regional sanity check", "Multi-objective optimization for several mission profiles"],
                ["Rover traverse", "Computed A* path from LZ-A to SCI-B over accessibility and cold-trap cost grids", "Energy-aware route with communication and thermal constraints"],
                ["Explainability", "Dynamic metrics and processing-chain text update with the selected layer", "Counterfactual comparison between candidate sites"],
                ["Judge Demo Mode", "Guided seven-step story from problem to recommendation", "Branching demo paths for science, engineering, and product judges"],
                ["Reports", "PDF/HTML mission brief for selected site", "Versioned science audit package"],
            ],
            [1.35 * inch, 2.55 * inch, 2.7 * inch],
        ),
        P("5. Current Dashboard Capability", "H1x"),
        dashboard_capabilities_table(),
        P("6. MVP Workflow", "H1x"),
        bullet("Load the curated lunar south-pole AOI assembled from official Chandrayaan-2 DFSAR, TMC-2, and OHRC files."),
        bullet("Normalize and render derived layers: SAR candidate evidence, terrain slope/accessibility, illumination/shadow proxies, cold-trap proxy, LOLA validation, and route focus image."),
        bullet("Use Judge Demo Mode to step through problem, evidence, validation, traverse, and final site recommendation."),
        bullet("Compute candidate scores and dynamic metrics that change as the layer stack changes."),
        bullet("Generate a rover traverse from landing point LZ-A to high-interest science target SCI-B."),
        bullet("Produce explanation panels, source ledger, and mission-planning PDF report."),
        P("7. Scoring Model", "H1x"),
        P(
            "The MVP is framed as an evidence-weighted decision system, not a claim of confirmed ice. The current SAR candidate evidence score combines co-pol brightness, cross/co ratio, and HH/VV ratio. Terrain accessibility combines low-slope and local-relief behavior from TMC-2. The cold-trap proxy combines shadow persistence and inverse illumination from low-sun hillshade sweeps. ISRO's 2026 DFSAR release highlights CPR > 1 with DOP < 0.13 as a refined criterion for volumetric scattering potentially associated with subsurface ice; exact CPR/DOP computation remains a validation upgrade."
        ),
        P("8. Validation and Scientific Honesty", "H1x"),
        P(LOLA_VALIDATION),
        P(ASTAR_ROUTE),
        bullet("Use candidate, evidence-consistent, or prioritized target language unless a claim is externally validated."),
        bullet("Separate raw evidence, derived proxy, validation layer, and operational recommendation in the UI."),
        P("9. Source-to-Evidence Ledger", "H1x"),
        source_ledger_table(),
        P("10. Acceptance Criteria", "H1x"),
        bullet("Map renders in under 5 seconds for preprocessed demo AOIs."),
        bullet("Each candidate site has a reproducible score breakdown and source-layer thumbnails."),
        bullet("Judge Demo Mode completes the problem-to-recommendation story without requiring live portal access."),
        bullet("Dynamic metric panels update when switching between DFSAR, TMC-2, LOLA, cold-trap, and traverse layers."),
        bullet("Traverse avoids cells above configured slope/hazard thresholds."),
        bullet("All public data sources and preprocessing assumptions are cited in the UI and report."),
        bullet("No output uses the phrase confirmed ice unless backed by external labeled truth; use likely, candidate, or evidence-consistent."),
        P("11. Risks", "H1x"),
        table(
            [
                ["Risk", "Impact", "Mitigation"],
                ["Limited labeled ground truth", "Model validation is difficult", "Use physics-informed scoring, published craters, uncertainty, and transparent assumptions"],
                ["Large PDS products", "Downloads and preprocessing may be slow", "Curate small AOI bundles and cache COG/Zarr-ready derivatives"],
                ["Radar false positives from rough terrain", "Misleading ice score", "Combine DOP, CPR, morphology, slope, and multi-frequency consistency"],
                ["LOLA resolution mismatch", "External validation can be overinterpreted", "Clearly call it a regional sanity check, not pixel-level hazard proof"],
                ["Hackathon time pressure", "Overbuilt backend", "Ship a strong preprocessed demo first, live ingestion second"],
            ],
            [1.45 * inch, 1.75 * inch, 3.4 * inch],
        ),
    ]


def arch_body():
    return [
        P("1. Guiding Architecture", "H1x"),
        P(
            "Use a thin interactive web app over a reproducible geospatial processing pipeline. The demo should not depend on live heavy downloads. Preprocess selected Chandrayaan-2 products into cloud-optimized rasters and compact metadata tables, then serve them through APIs optimized for fast visualization and scoring."
        ),
        P("2. System Components", "H1x"),
        table(
            [
                ["Layer", "Recommended Tech", "Reason"],
                ["Frontend", "Next.js or Vite React, TypeScript, MapLibre GL, deck.gl", "Fast hackathon UI, strong map layer control, good visual polish"],
                ["API", "FastAPI, Pydantic, Uvicorn", "Python-native geospatial/ML integration and quick schema validation"],
                ["Processing", "Python, rasterio, rioxarray, xarray, numpy, scikit-image, scikit-learn", "Best ecosystem for PDS/geospatial raster transforms"],
                ["Path planning", "networkx or custom grid A*", "Simple, explainable route generation over terrain-cost grids"],
                ["Storage", "PostgreSQL + PostGIS, object storage/local files for COG/Zarr", "Spatial queries in DB, heavy rasters outside DB"],
                ["ML/Scoring", "scikit-learn baseline, PyTorch optional", "Start explainable; add deep learning only if data and time allow"],
                ["Reports", "ReportLab or WeasyPrint", "Generate site-selection PDFs from scored outputs"],
            ],
            [1.25 * inch, 2.5 * inch, 2.85 * inch],
        ),
        P("3. Data Pipeline", "H1x"),
        bullet("Ingest: download PDS4 products from PRADAN/CH2 Map Browse and store raw archives unchanged."),
        bullet("Parse: read PDS labels, extract raster arrays, geometry, instrument metadata, acquisition time, and projection info."),
        bullet("Calibrate/derive: generate radar-ratio evidence, roughness proxy, slope, accessibility, illumination/shadow proxy, cold-trap proxy, and crater context layers where possible."),
        bullet("Normalize: reproject to lunar south-pole stereographic grid and resample to common resolution buckets."),
        bullet("Tile: export visualization layers as Cloud Optimized GeoTIFFs or MBTiles for fast dashboard rendering."),
        bullet("Validate: crop NASA PGDA/LRO LOLA products to the TMC-2 AOI and compare regional slope behavior."),
        bullet("Score: calculate pixel and candidate-site scores, dynamic dashboard metrics, and candidate rankings."),
        bullet("Route: run A* over accessibility and cold-trap cost layers to connect landing and science points."),
        P("4. Processing Architecture", "H1x"),
        table(
            [
                ["Stage", "Inputs", "Outputs"],
                ["Raw archive", "PDS IMG/XML/LBL files, product manifests", "Immutable raw product registry"],
                ["Geometric processing", "SPICE kernels, product footprints, camera/SAR metadata", "Projected raster stack"],
                ["Feature extraction", "DFSAR, OHRC, TMC-2 DEM/imagery", "Radar evidence, slope, accessibility, morphology, illumination and cold-trap proxies"],
                ["External validation", "NASA PGDA/LRO LOLA slope, roughness, class products", "Regional sanity-check metrics and validation focus layer"],
                ["Decision scoring", "Feature rasters and site constraints", "Ice evidence confidence, landing safety, traverse cost"],
                ["Route planning", "Accessibility and cold-trap proxy rasters", "A* path, relative cost, route evidence notes"],
                ["Presentation", "Scores, layers, paths, explanations", "Dynamic dashboard, Judge Demo Mode, mission brief PDF"],
            ],
            [1.35 * inch, 2.4 * inch, 2.85 * inch],
        ),
        P("5. Current Demo Architecture", "H1x"),
        dashboard_capabilities_table(),
        P("6. A* Traverse and Validation Notes", "H1x"),
        P(ASTAR_ROUTE),
        P(LOLA_VALIDATION),
        P("7. Deployment for Hackathon", "H1x"),
        bullet("Local-first demo: Docker Compose with frontend, API, PostGIS, and mounted data directory."),
        bullet("Preprocessed sample AOIs shipped in repository or external Drive link to avoid live download failures."),
        bullet("Optional cloud demo: Render/Fly.io for API and Vercel for frontend; use hosted tile files if size permits."),
        bullet("Keep a fully offline demo mode because mission-data portals and networks may be unreliable during presentation."),
        P("8. Development Standards", "H1x"),
        bullet("Every raster derivative must record source product ID, processing version, projection, resolution, and checksum."),
        bullet("APIs must return confidence and explanation metadata with every recommendation."),
        bullet("The UI must separate evidence, inference, and mission recommendation to avoid overclaiming."),
        bullet("Use configuration files for mission weights so judges can see how priorities change the landing recommendation."),
        P("9. Source-to-Evidence Ledger", "H1x"),
        source_ledger_table(),
    ]


def schema_body():
    return [
        P("1. Data Acquisition Strategy", "H1x"),
        P(
            "Primary Chandrayaan-2 data should be obtained from ISRO's Planetary Data System archive through ISSDC PRADAN and Chandrayaan-2 Map Browse. ISSDC states that Chandrayaan-2 data from CLASS, CHACE-2, XSM, IIRS, TMC-2, OHRC, DFRS, and DFSAR are processed by level definitions and provided in PDS standards for archival and dissemination."
        ),
        table(
            [
                ["Need", "Instrument/Product", "Where to Get It", "Use in Project"],
                ["Radar evidence for subsurface ice", "Chandrayaan-2 DFSAR L/S-band SAR, full or hybrid polarimetry", "PRADAN: https://pradan.issdc.gov.in/ch2/ and CH2 Map Browse", "CPR, DOP, scattering behavior, radar feature stack"],
                ["Landing hazard imagery", "OHRC calibrated products", "CH2 Map Browse: select South Pole projection and CH2_OHR_Calibrated_Product", "Boulder/crater proxy, morphology, landing-site visual context"],
                ["Terrain and DEM", "TMC-2 stereo/DEM products where available", "PRADAN/CH2 Map Browse", "Slope, roughness, route cost, landing safety"],
                ["Hydration/mineral context", "IIRS hyperspectral products", "PRADAN", "Optional 3-micron hydration/mineral evidence layer"],
                ["Geometry/navigation", "SPICE kernels and footprints", "PRADAN/ISSDC", "Co-registration, illumination geometry, product provenance"],
                ["Auxiliary validation", "LRO LOLA slope/roughness/class products", "NASA PGDA/PDS", "Independent regional sanity check for TMC-2 terrain behavior"],
                ["Production hardening", "USGS ISIS and PDS validation workflows", "USGS ISIS documentation", "Future projection/calibration audit trail"],
            ],
            [1.05 * inch, 1.35 * inch, 2.0 * inch, 2.2 * inch],
        ),
        P("2. Practical Download Steps", "H1x"),
        bullet("Create/login to PRADAN if required: https://pradan.issdc.gov.in/ch2/."),
        bullet("Open Chandrayaan-2 Map Browse at https://chmapbrowse.issdc.gov.in."),
        bullet("Set map projection to South Pole for lunar south-polar AOIs."),
        bullet("Use instrument footprint filters: DFSAR/SAR products for radar, CH2_OHR_Calibrated_Product for OHRC, and TMC-2 products for terrain context."),
        bullet("Select footprints over target PSRs, inspect product metadata, and download PDS products."),
        bullet("If browser download limits or timeouts occur, use PRADAN bulk download guidance and keep a local manifest of product IDs."),
        P("3. Current Downloaded Product Set", "H1x"),
        table(
            [
                ["Payload", "Product", "Role"],
                ["DFSAR", "ch2_sar_ncls_20200913t042439405_d_fp_d18.zip", "Radar evidence source for candidate subsurface-ice indicators."],
                ["TMC-2", "ch2_tmc_ndn_20231203T0019079527_d_dtm_d18.zip", "South-pole digital terrain model for slope, accessibility, illumination proxy, and traverse route."],
                ["TMC-2", "ch2_tmc_ndn_20231203T0019079527_d_oth_d18.zip", "Orthographic context layer; browse used for visual terrain context."],
                ["OHRC", "ch2_ohr_ncp_20260103T0609041371_d_img_d18.zip", "High-resolution optical hazard-context strip."],
                ["OHRC", "ch2_ohr_ncp_20260103T1005176450_d_img_d18.zip", "Second optical hazard-context strip for comparison."],
                ["NASA LOLA", "PGDA LDRM_80S_1000MPP_ADJ_* products", "Independent slope, roughness, and terrain-class validation crop."],
            ],
            [0.95 * inch, 2.75 * inch, 2.9 * inch],
        ),
        P("4. Candidate API Endpoints", "H1x"),
        table(
            [
                ["Method", "Path", "Purpose", "Key Response"],
                ["GET", "/api/aoi", "List demo AOIs", "AOI id, bounds, centroid, available layers"],
                ["POST", "/api/aoi", "Create custom AOI", "AOI id and ingest status"],
                ["GET", "/api/layers/{aoi_id}", "List raster/vector layers", "Tile URLs, legends, resolution, source products"],
                ["POST", "/api/score/ice", "Run or fetch ice-likelihood scoring", "Raster summary, candidate targets, confidence"],
                ["GET", "/api/metrics/{layer_id}", "Fetch dynamic metrics for a selected dashboard layer", "Confidence, status label, candidate table, profile bars, processing chain"],
                ["GET", "/api/validation/lola/{aoi_id}", "Return external LOLA comparison", "TMC mean slope, LOLA mean slope, mean difference, caveats"],
                ["POST", "/api/score/landing", "Rank landing ellipses", "Safety/resource/science score breakdown"],
                ["POST", "/api/traverse", "Plan route from site to targets", "Path geometry, distance, cost, hazard events"],
                ["GET", "/api/demo/judge-mode", "Return guided demo sequence", "Step titles, target layer ids, narration, UI focus areas"],
                ["GET", "/api/products/{product_id}", "Product provenance", "Instrument, acquisition, processing, checksum"],
                ["POST", "/api/reports/mission-brief", "Generate PDF report", "Report URL and status"],
            ],
            [0.65 * inch, 1.5 * inch, 2.15 * inch, 2.3 * inch],
        ),
        P("5. API Object Sketch", "H1x"),
        P(
            "<b>IceScoreRequest</b>: aoi_id, layer_set_id, model_version, weights, thresholds, min_confidence. "
            "<b>IceCandidate</b>: id, geometry, score, confidence, area_m2, evidence: {cpr, dop, psr, morphology, roughness}, source_product_ids. "
            "<b>TraverseRequest</b>: aoi_id, start_site_id, target_ids, max_slope_deg, avoid_psr_mode, energy_budget_wh, science_weight. "
            "<b>LayerMetric</b>: dynamic metrics object with layer_id, plan_label, confidence, confidence_status, profile_bars, candidate_rows, processing_steps. "
            "<b>ValidationResult</b>: validation_id, source, compared_layer_ids, metrics_json, caveats."
        ),
        P("6. Database Schema", "H1x"),
        table(
            [
                ["Table", "Core Fields", "Purpose"],
                ["raw_products", "id, instrument, product_id, url, acquisition_time, level, footprint_geom, checksum, local_path", "Immutable data provenance"],
                ["aoi", "id, name, bounds_geom, centroid, notes, created_at", "Study regions and demo areas"],
                ["raster_layers", "id, aoi_id, product_id, layer_type, uri, crs, resolution_m, min_val, max_val, processing_version", "COG/Zarr-derived map layers"],
                ["feature_stats", "id, aoi_id, layer_id, geom, mean, p05, p50, p95, nodata_pct", "AOI and candidate summaries"],
                ["validation_results", "id, aoi_id, source_name, source_url, compared_layer_ids, metrics_json, caveats, created_at", "External validation such as LOLA vs TMC-2 slope sanity checks"],
                ["layer_metrics", "id, layer_id, plan_label, confidence, status, bars_json, candidate_rows_json, processing_steps_json", "Dynamic dashboard metric payloads"],
                ["ice_candidates", "id, aoi_id, geom, score, confidence, method, evidence_json, product_ids, created_at", "Ranked ice-likelihood targets"],
                ["landing_sites", "id, aoi_id, geom, safety_score, science_score, resource_score, total_score, constraints_json", "Candidate landing zones"],
                ["traverse_paths", "id, aoi_id, landing_site_id, target_id, geom, distance_m, total_cost, hazard_events_json", "Rover routes"],
                ["demo_steps", "id, order_index, title, target_layer_id, narration, metric_focus_json", "Judge Demo Mode story sequence"],
                ["reports", "id, aoi_id, type, uri, generated_at, config_json", "Generated mission briefs"],
            ],
            [1.15 * inch, 3.15 * inch, 2.3 * inch],
        ),
        P("7. Current Evidence and LOLA Validation", "H1x"),
        P(LOLA_VALIDATION),
        P(ASTAR_ROUTE),
        P("8. Source-to-Evidence Ledger", "H1x"),
        source_ledger_table(),
        P("9. Spatial Indexing and Storage", "H1x"),
        bullet("Use PostGIS geometry columns for AOIs, footprints, candidate regions, landing ellipses, and traverses."),
        bullet("Store large rasters as files, not database blobs; keep URIs and metadata in PostgreSQL."),
        bullet("Use ST_Intersects for product discovery by AOI and GIST indexes on all geometry fields."),
        bullet("Use product checksums and processing_version to make every score reproducible."),
    ]


def library_body():
    return [
        P("1. Target Library Philosophy", "H1x"),
        P(
            "Favor mature geospatial and planetary-science tools over custom parsing. The system should be explainable and reproducible, so start with deterministic feature engineering and only add deep learning when data volume and labels justify it."
        ),
        P("2. Core Python Libraries", "H1x"),
        table(
            [
                ["Library", "Use", "Priority"],
                ["pds4_tools", "Read PDS4 labels and arrays from Chandrayaan-2 products", "Must have"],
                ["rasterio / rioxarray", "Raster IO, reprojection, clipping, metadata", "Must have"],
                ["xarray / dask", "Large raster stacks and chunked computations", "High"],
                ["numpy / pandas", "Numerical and tabular processing", "Must have"],
                ["geopandas / shapely / pyproj", "Vector geometry, CRS transforms, spatial operations", "Must have"],
                ["scikit-image", "Crater/boulder/texture features, morphology, filtering", "High"],
                ["scikit-learn", "Baseline scoring, calibration, feature importance", "High"],
                ["networkx", "Graph route planning and critical path analysis", "Medium"],
                ["pytorch", "Optional CNN/UNet feature extraction if labeled data is available", "Stretch"],
                ["matplotlib / plotly", "Diagnostics and scientific plots", "High"],
                ["reportlab", "Generate updated PRD, architecture, API/schema, and target-library PDFs", "High"],
            ],
            [1.35 * inch, 3.85 * inch, 1.4 * inch],
        ),
        P("3. Planetary and Geospatial Toolchain", "H1x"),
        table(
            [
                ["Tool", "Use", "Notes"],
                ["USGS ISIS", "Planetary image calibration, projection, SPICE-aware processing", "Best serious choice for planetary raster workflows"],
                ["NASA Ames Stereo Pipeline", "Stereo DEM generation/refinement from imagery", "Useful for OHRC/TMC-2 terrain products"],
                ["GDAL", "COG conversion, warping, tiling, raster utilities", "Required under most Python geospatial stacks"],
                ["QGIS", "Manual QA, map design, layer inspection", "Excellent for demo validation and screenshots"],
                ["PostGIS", "Spatial database and product discovery queries", "Recommended backend store"],
                ["MapLibre GL", "Frontend map rendering", "Open-source map visualization"],
                ["deck.gl", "High-performance raster/vector overlays", "Good for heatmaps and path overlays"],
                ["NASA PGDA / PDS", "External terrain and illumination reference datasets", "Used for current LOLA validation and future PSR checks"],
            ],
            [1.45 * inch, 3.45 * inch, 1.7 * inch],
        ),
        P("4. Frontend Libraries", "H1x"),
        bullet("React + TypeScript for the dashboard."),
        bullet("MapLibre GL for map canvas, layer toggles, bounds, and custom tile sources."),
        bullet("deck.gl for candidate heatmaps, path overlays, hover picking, and layer blending."),
        bullet("TanStack Query for API state and caching."),
        bullet("Zustand or Redux Toolkit for map-layer state if the UI grows."),
        bullet("Recharts or Plotly.js for evidence charts and score decomposition."),
        bullet("Guided-tour component or a small state-machine hook for Judge Demo Mode sequencing."),
        P("5. Current Demo Feature Dependencies", "H1x"),
        table(
            [
                ["Feature", "Current dependency path", "Future library path"],
                ["Dynamic metrics", "Static JSON/JS objects generated from processed layer summaries", "FastAPI layer metrics endpoint backed by PostGIS tables"],
                ["A* traverse", "Python-derived route JSON and rendered focus PNG", "networkx/custom A* service using COG/Zarr cost grids"],
                ["LOLA validation", "Downloaded PGDA GeoTIFFs cropped with rasterio", "Reusable validation job with provenance and tolerance thresholds"],
                ["Judge Demo Mode", "Frontend step state that switches layers and narration", "Persisted demo_steps table plus downloadable presenter script"],
                ["Source ledger", "Dashboard and PDF tables from audited source status", "Product registry with checksum, source URL, and processing version"],
            ],
            [1.35 * inch, 2.7 * inch, 2.55 * inch],
        ),
        P(LOLA_VALIDATION),
        P(ASTAR_ROUTE),
        P("6. Backend and API Libraries", "H1x"),
        bullet("FastAPI and Pydantic for typed request/response contracts."),
        bullet("SQLAlchemy or SQLModel with GeoAlchemy2 for PostGIS tables."),
        bullet("Celery/RQ or FastAPI BackgroundTasks for heavier preprocessing jobs."),
        bullet("Uvicorn for local development and Docker Compose deployment."),
        bullet("ReportLab or WeasyPrint for mission brief PDF generation."),
        P("7. Recommended MVP Stack", "H1x"),
        table(
            [
                ["Part", "Pick for Hackathon"],
                ["Frontend", "Vite React + TypeScript + MapLibre GL + deck.gl"],
                ["Backend", "FastAPI + Pydantic + SQLModel"],
                ["Database", "PostgreSQL + PostGIS"],
                ["Raster storage", "Local data directory with Cloud Optimized GeoTIFFs"],
                ["Processing", "Python scripts using pds4_tools, rasterio, geopandas, scikit-image, scikit-learn"],
                ["Route planning", "Grid A* with networkx or a small custom implementation"],
                ["Validation", "NASA PGDA/LRO LOLA crop plus caveated regional comparison"],
                ["Demo data", "Preprocessed AOI bundle downloaded from PRADAN/CH2 Map Browse and NASA PGDA"],
            ],
            [1.8 * inch, 4.8 * inch],
        ),
        P("8. Source-to-Evidence Ledger", "H1x"),
        source_ledger_table(),
        P("9. What Not to Overbuild", "H1x"),
        bullet("Do not start with a large deep-learning model unless you already have labels and compute."),
        bullet("Do not store full rasters in PostgreSQL; store files and metadata separately."),
        bullet("Do not depend on live portal downloads during the final demo."),
        bullet("Do not claim definitive ice detection; present transparent evidence and uncertainty."),
    ]


def main():
    docs = [
        (
            "01_PRD_Lunar_Ice_Intelligence_System.pdf",
            "Product Requirements Document",
            PROBLEM_TITLE,
            prd_body(),
        ),
        (
            "02_Architecture_Tech_Stack_Guidelines.pdf",
            "Architecture and Tech Stack Guidelines",
            PROBLEM_TITLE,
            arch_body(),
        ),
        (
            "03_API_Database_Schemas_and_Data_Acquisition.pdf",
            "API, Database Schemas, and Data Acquisition",
            PROBLEM_TITLE,
            schema_body(),
        ),
        (
            "04_Target_Library_Document.pdf",
            "Target Library Document",
            PROBLEM_TITLE,
            library_body(),
        ),
    ]
    for filename, title, subtitle, body in docs:
        path = make_doc(filename, title, subtitle, body)
        print(path)


if __name__ == "__main__":
    main()
