const assetVersion = "20260619-mentor-alignment";

const layers = [
  {
    id: "sar-score",
    name: "SAR Candidate Ice Evidence",
    source: "DFSAR HH/HV/VH/VV SRI",
    focusPath: "../data/processed/demo_assets/sar_candidate_focus.png",
    rawPath: "../data/processed/derived_layers/sar_candidate_ice_evidence_score.png",
    thumbnail: "../data/processed/demo_assets/sar_candidate_focus.png",
    description:
      "Radar-derived prototype evidence score combining co-pol brightness, cross-pol enhancement, and HH/VV ratio. This ranks candidate volatile targets; it does not claim confirmed ice.",
    score: 82,
  },
  {
    id: "cpr-dop-gate",
    name: "CPR/DOP Threshold Gate",
    source: "DFSAR polarimetry readiness check",
    focusPath: "../data/processed/demo_assets/cpr_dop_threshold_focus.png",
    rawPath: "../data/processed/demo_assets/cpr_dop_threshold_focus.png",
    thumbnail: "../data/processed/demo_assets/cpr_dop_threshold_focus.png",
    description:
      "Problem Statement 8 threshold view: CPR > 1 and DOP < 0.13 are shown explicitly. Current output is a CPR/DOP-ready proxy because exact CPR/DOP needs calibrated phase/coherency-aware polarimetric products.",
    score: 72,
  },
  {
    id: "dsc-target",
    name: "Doubly Shadowed Crater Proxy",
    source: "cold-trap + shadow + terrain mask",
    focusPath: "../data/processed/demo_assets/doubly_shadowed_crater_focus.png",
    rawPath: "../data/processed/derived_layers/doubly_shadowed_crater_proxy_score.png",
    thumbnail: "../data/processed/demo_assets/doubly_shadowed_crater_focus.png",
    description:
      "DSC-1 is a Faustini-class doubly shadowed crater proxy target generated from cold-trap, shadow persistence, illumination, slope, and accessibility layers. It is a proxy until the official supplied crater AOI is received.",
    score: 84,
  },
  {
    id: "rough-filter",
    name: "Rough Terrain Rejection",
    source: "slope + accessibility + SAR/cold consistency",
    focusPath: "../data/processed/demo_assets/rough_terrain_filter_focus.png",
    rawPath: "../data/processed/derived_layers/rough_terrain_rejection_mask.png",
    thumbnail: "../data/processed/demo_assets/rough_terrain_filter_focus.png",
    description:
      "Mentor-aligned false-positive filter that rejects steep, low-access, radar-bright rough terrain before candidate ice ranking. It is a morphology proxy until registered OHRC boulder/crater extraction is complete.",
    score: 73,
  },
  {
    id: "ice-volume",
    name: "Top 5 m Ice Volume Estimate",
    source: "DSC-1 area x 5 m x ice fraction",
    focusPath: "../data/processed/demo_assets/ice_volume_estimator_focus.png",
    rawPath: "../data/processed/demo_assets/ice_volume_estimator_focus.png",
    thumbnail: "../data/processed/demo_assets/ice_volume_estimator_focus.png",
    description:
      "Scenario-based water-equivalent volume estimate for the top 5 m of regolith at the DSC-1 proxy target. It provides low, medium, and high ice-fraction cases rather than a confirmed reserve number.",
    score: 69,
  },
  {
    id: "tmc-access",
    name: "TMC-2 Landing Accessibility",
    source: "south-pole DTM-derived score",
    focusPath: "../data/processed/demo_assets/tmc2_accessibility_focus.png",
    rawPath: "../data/processed/derived_layers/tmc2_south_pole_accessibility_score.png",
    thumbnail: "../data/processed/demo_assets/tmc2_accessibility_focus.png",
    description:
      "Low-slope and moderate-relief screening layer derived from the valid south-pole TMC-2 DTM. It is intended for landing-zone and traverse triage.",
    score: 79,
  },
  {
    id: "traverse-route",
    name: "Computed Rover Traverse",
    source: "A* over accessibility + cold-trap + solar penalty",
    focusPath: "../data/processed/demo_assets/data_derived_traverse_focus.png",
    rawPath: "../data/processed/demo_assets/data_derived_traverse_focus.png",
    thumbnail: "../data/processed/demo_assets/data_derived_traverse_focus.png",
    description:
      "Data-derived A* screening route. LZ-A is selected from high-accessibility terrain, SCI-B from cold-trap/accessibility score, and the path minimizes terrain plus low-power risk within one connected valid TMC-2 island.",
    score: 81,
  },
  {
    id: "lola-validation",
    name: "NASA LOLA Validation",
    source: "LRO/LOLA PGDA 1000 m products",
    focusPath: "../data/processed/demo_assets/lola_validation_focus.png",
    rawPath: "../data/processed/derived_layers/lola_tmc_aoi_slope_1000m.png",
    thumbnail: "../data/processed/demo_assets/lola_validation_focus.png",
    description:
      "Independent NASA LRO/LOLA south-pole slope, roughness, and class products cropped to the Chandrayaan-2 TMC-2 AOI. Mean slope differs from the TMC-derived slope by only 0.96 degrees at regional scale.",
    score: 88,
  },
  {
    id: "cold-trap",
    name: "Cold-Trap Proxy",
    source: "low-sun hillshade from TMC-2 DTM",
    focusPath: "../data/processed/demo_assets/cold_trap_proxy_focus.png",
    rawPath: "../data/processed/derived_layers/cold_trap_proxy.png",
    thumbnail: "../data/processed/demo_assets/cold_trap_proxy_focus.png",
    description:
      "Prototype shadow/cold-trap score derived from eight low-sun hillshade simulations over the south-pole TMC-2 DTM. It is a screening proxy, not a validated ephemeris PSR product.",
    score: 77,
  },
  {
    id: "illumination",
    name: "Illumination Availability",
    source: "low-sun terrain simulation",
    focusPath: "../data/processed/demo_assets/illumination_proxy_focus.png",
    rawPath: "../data/processed/derived_layers/illumination_availability_proxy.png",
    thumbnail: "../data/processed/demo_assets/illumination_proxy_focus.png",
    description:
      "Low-sun illumination availability proxy for rover power and thermal planning. NASA PGDA-style illumination products are the planned external validation reference.",
    score: 70,
  },
  {
    id: "tmc-slope",
    name: "TMC-2 Slope Constraint",
    source: "ch2_tmc_ndn_20231203T0019079527",
    focusPath: "../data/processed/demo_assets/tmc2_slope_focus.png",
    rawPath: "../data/processed/derived_layers/tmc2_south_pole_slope_deg.png",
    thumbnail: "../data/processed/demo_assets/tmc2_slope_focus.png",
    description:
      "Slope layer computed from the TMC-2 DTM at a downsampled processing scale. High-slope terrain is penalized for landing and rover planning.",
    score: 74,
  },
  {
    id: "tmc-elevation",
    name: "TMC-2 Elevation Model",
    source: "10 m south-pole DTM",
    focusPath: "../data/processed/demo_assets/tmc2_elevation_focus.png",
    rawPath: "../data/processed/derived_layers/tmc2_south_pole_elevation.png",
    thumbnail: "../data/processed/demo_assets/tmc2_elevation_focus.png",
    description:
      "Digital terrain model in lunar south-pole polar stereographic projection, approximately spanning 88.65S to 81.50S.",
    score: 76,
  },
  {
    id: "tmc-ortho",
    name: "TMC-2 Optical Terrain Context",
    source: "orthographic browse",
    focusPath: "../data/processed/demo_assets/tmc2_ortho_focus.png",
    rawPath: "../data/processed/derived_layers/tmc2_south_pole_orthobrowse.png",
    thumbnail: "../data/processed/demo_assets/tmc2_ortho_focus.png",
    description:
      "Orthographic browse context from the matching TMC-2 strip. The full orthoproduct remains zipped to avoid adding roughly 2 GB of working data.",
    score: 72,
  },
  {
    id: "sar-browse",
    name: "DFSAR Radar Browse",
    source: "ch2_sar_ncls_20200913t042439405",
    focusPath: "../data/processed/demo_assets/sar_browse_focus.png",
    rawPath: "../data/processed/quicklooks/ch2_sar_ncls_20200913t042439405_b_brw_xx_fp_xx_d18_quicklook.png",
    thumbnail: "../data/processed/demo_assets/sar_browse_focus.png",
    description:
      "Calibrated full-polarimetry DFSAR browse layer used as the radar context behind candidate subsurface-ice evidence.",
    score: 78,
  },
  {
    id: "ohr-a",
    name: "OHRC Hazard Strip A",
    source: "ch2_ohr_ncp_20260103T0609041371",
    focusPath: "../data/processed/demo_assets/ohr_a_focus.png",
    rawPath: "../data/processed/quicklooks/ch2_ohr_ncp_20260103T0609041371_b_brw_d18_quicklook.png",
    thumbnail: "../data/processed/demo_assets/ohr_a_focus.png",
    description:
      "High-resolution optical browse strip for crater, boulder, and local roughness inspection near candidate landing corridors.",
    score: 68,
  },
  {
    id: "ohr-b",
    name: "OHRC Hazard Strip B",
    source: "ch2_ohr_ncp_20260103T1005176450",
    focusPath: "../data/processed/demo_assets/ohr_b_focus.png",
    rawPath: "../data/processed/quicklooks/ch2_ohr_ncp_20260103T1005176450_b_brw_d18_quicklook.png",
    thumbnail: "../data/processed/demo_assets/ohr_b_focus.png",
    description:
      "Second OHRC strip for visual comparison and local hazard explanation. Exact overlap with the TMC/DFSAR AOI still needs registration.",
    score: 66,
  },
];

const fusionPath = "../data/processed/demo_assets/fusion_board.png";
const sources = [
  {
    name: "PRADAN",
    status: "used",
    url: "https://pradan.issdc.gov.in/ch2/",
    contribution: "Official DFSAR, OHRC, and TMC-2 ZIP downloads used as the raw evidence base.",
  },
  {
    name: "ISRO DFSAR 2026",
    status: "used",
    url: "https://www.isro.gov.in/Chandrayaan2_Dual_Frequency_Synthetic_Aperture_Radar.html",
    contribution: "Science anchor for radar logic: CPR > 1 and DOP < 0.13 are treated as the target validation criteria.",
  },
  {
    name: "Chandrayaan-2 Map Browse",
    status: "used",
    url: "https://chmapbrowse.issdc.gov.in",
    contribution: "AOI discovery route for south-pole payload products and visual footprint selection.",
  },
  {
    name: "ISSDC Mission Data",
    status: "used",
    url: "https://www.issdc.gov.in/chandrayaan2.html",
    contribution: "Payload and mission context for explaining why DFSAR, OHRC, and TMC-2 belong together.",
  },
  {
    name: "VEDAS OHRC Note",
    status: "used",
    url: "https://vedas.sac.gov.in/static/pdf/SIH_2024/SIH1732_CH2_PS.pdf",
    contribution: "Download workflow support for OHRC products and optical hazard-inspection framing.",
  },
  {
    name: "NASA LOLA / PDS",
    status: "used",
    url: "https://pds-geosciences.wustl.edu/missions/lro/lola.htm",
    contribution: "Independent LRO/LOLA south-pole slope, roughness, and class products now cropped to the TMC-2 AOI for external terrain validation.",
  },
  {
    name: "NASA PGDA Illumination",
    status: "used",
    url: "https://pgda.gsfc.nasa.gov/products/69",
    contribution: "Used as the validation target for a current low-sun illumination and cold-trap proxy derived from TMC-2 terrain.",
  },
  {
    name: "Problem Statement 8",
    status: "mapped",
    url: "#",
    contribution: "Requirements now mapped into dashboard layers: CPR/DOP gate, DSC-1 target proxy, rough-terrain rejection, solar-aware traverse, and top-5m volume scenarios.",
  },
  {
    name: "USGS ISIS",
    status: "roadmap",
    url: "https://isis.astrogeology.usgs.gov/",
    contribution: "Production-grade planetary image-processing route documented for PDS-style ingestion, lunar polar projection, and delivery hardening.",
  },
];

const methods = [
  {
    title: "SAR Candidate Evidence",
    inputs: ["co-pol", "cross/co", "HH/VV"],
    output: "Radar candidate score",
    formula: "0.50 brightness + 0.35 cross-pol + 0.15 ratio",
    note: "Ranks radar-bright and polarimetrically interesting pixels. It is candidate evidence only, not confirmed water ice.",
  },
  {
    title: "Terrain Accessibility",
    inputs: ["slope", "relief"],
    output: "Landing accessibility",
    formula: "0.75 low-slope + 0.25 low-relief",
    note: "Uses TMC-2 DTM slope and relative relief to screen terrain that could plausibly support landing or rover movement.",
  },
  {
    title: "Cold-Trap Proxy",
    inputs: ["shadow", "illumination"],
    output: "Cold-trap plausibility",
    formula: "0.65 shadow + 0.35 inverse illumination",
    note: "Uses eight low-sun hillshade simulations at 1.5 degree solar altitude. This needs validation against ephemeris PSR products.",
  },
  {
    title: "CPR/DOP Gate",
    inputs: ["HH/HV/VH/VV", "thresholds"],
    output: "Radar validation gate",
    formula: "CPR > 1 and DOP < 0.13 target",
    note: "Current output is threshold-ready proxy evidence because exact CPR/DOP requires calibrated phase/coherency-aware polarimetric processing.",
  },
  {
    title: "DSC-1 Proxy Mask",
    inputs: ["cold", "shadow", "slope"],
    output: "Faustini-class target",
    formula: "0.34 cold + 0.30 shadow + terrain terms",
    note: "Identifies a proxy doubly shadowed crater target until the official supplied crater AOI is received.",
  },
  {
    title: "Rough-Terrain Rejection",
    inputs: ["slope", "access", "SAR/cold"],
    output: "false-positive filter",
    formula: "0.55 slope + 0.25 low-access + 0.20 SAR/cold mismatch",
    note: "Mentor-aligned morphology proxy to avoid treating rough, radar-bright rocky terrain as candidate ice.",
  },
  {
    title: "Computed Traverse",
    inputs: ["accessibility", "cold-trap", "illumination"],
    output: "LZ-A to SCI-B route",
    formula: "A* over terrain + solar-power cost",
    note: "Finds a screening path between selected LZ-A and SCI-B while penalizing low-illumination route segments.",
  },
  {
    title: "Ice Volume Estimate",
    inputs: ["DSC area", "5 m", "ice fraction"],
    output: "water-equivalent m3",
    formula: "area * 5 m * ice_fraction",
    note: "Reports low, medium, and high scenarios to satisfy the volume requirement without claiming confirmed reserves.",
  },
];

const provenance = [
  {
    payload: "DFSAR",
    product: "ch2_sar_ncls_20200913t042439405_d_fp_d18.zip",
    date: "2020-09-13",
    role: "Radar evidence source for candidate subsurface-ice indicators.",
    status: "processed",
  },
  {
    payload: "TMC-2",
    product: "ch2_tmc_ndn_20231203T0019079527_d_dtm_d18.zip",
    date: "2023-12-03",
    role: "South-pole digital terrain model for slope, accessibility, illumination proxy, and traverse route.",
    status: "processed",
  },
  {
    payload: "TMC-2",
    product: "ch2_tmc_ndn_20231203T0019079527_d_oth_d18.zip",
    date: "2023-12-03",
    role: "Orthographic context; full raster kept zipped, browse used for visual terrain context.",
    status: "browse used",
  },
  {
    payload: "OHRC",
    product: "ch2_ohr_ncp_20260103T0609041371_d_img_d18.zip",
    date: "2026-01-03",
    role: "High-resolution optical hazard-context strip.",
    status: "context",
  },
  {
    payload: "OHRC",
    product: "ch2_ohr_ncp_20260103T1005176450_d_img_d18.zip",
    date: "2026-01-03",
    role: "Second optical hazard-context strip for comparison.",
    status: "context",
  },
  {
    payload: "DERIVED",
    product: "doubly_shadowed_crater_proxy_score + volume scenarios",
    date: "2026-06-19",
    role: "Problem Statement 8 gap-closure outputs for DSC-1 target framing and top-5m ice-volume scenarios.",
    status: "derived",
  },
  {
    payload: "DERIVED",
    product: "solar-aware A* route summary",
    date: "2026-06-19",
    role: "Traverse cost now includes accessibility, cold-trap score, and low-illumination solar-power penalty.",
    status: "derived",
  },
  {
    payload: "DERIVED",
    product: "rough_terrain_rejection_mask + morphology summary",
    date: "2026-06-19",
    role: "Mentor-aligned rough-terrain false-positive filter before candidate ice and excavation ranking.",
    status: "derived",
  },
  {
    payload: "TMC-2",
    product: "ch2_tmc_ndn_20250426T0752081453_d_dtm/oth_d18.zip",
    date: "2025-04-26",
    role: "Deprecated non-polar terrain test data retained for pipeline regression only.",
    status: "deprecated",
  },
];

const demoSteps = [
  {
    title: "1. Problem: south-pole ice is hard to confirm",
    copy:
      "Permanently shadowed regions are scientifically valuable, but a bright pixel alone is not enough. The workflow has to combine radar evidence, terrain safety, illumination context, and route feasibility.",
    layerId: "sar-score",
    view: "fusion",
  },
  {
    title: "2. DFSAR: candidate radar evidence",
    copy:
      "Start with DFSAR-derived candidate evidence. Radar-bright and polarimetrically interesting zones are ranked as candidates, not claimed as confirmed ice.",
    layerId: "sar-score",
    view: "focus",
  },
  {
    title: "3. CPR/DOP gate: required radar criteria",
    copy:
      "The challenge explicitly names CPR > 1 and DOP < 0.13. The console now shows this gate and marks the current output as threshold-ready proxy evidence until exact polarimetric products are available.",
    layerId: "cpr-dop-gate",
    view: "focus",
  },
  {
    title: "4. Doubly shadowed crater proxy: DSC-1",
    copy:
      "A Faustini-class DSC-1 target mask combines cold-trap score, shadow persistence, low illumination, slope, and accessibility. This gives the required crater-target framing while keeping the official-AOI caveat visible.",
    layerId: "dsc-target",
    view: "focus",
  },
  {
    title: "5. Rough-terrain rejection: avoid rocky false positives",
    copy:
      "The mentor slides emphasize that radar-bright terrain can be rough rock, not ice. This filter rejects steep, low-access, SAR/cold-inconsistent regions and keeps lobate-rim morphology as a candidate cue rather than a confirmed ice claim.",
    layerId: "rough-filter",
    view: "focus",
  },
  {
    title: "6. TMC-2: terrain and slope safety",
    copy:
      "A science target is not useful if the lander or rover cannot reach it. TMC-2 DTM products provide slope, relief, and accessibility screening.",
    layerId: "tmc-access",
    view: "focus",
  },
  {
    title: "7. NASA LOLA: external terrain validation",
    copy:
      "Before trusting the terrain route, we cross-check the TMC-derived slope against independent LRO/LOLA south-pole products. The regional mean slope differs by only 0.96 degrees.",
    layerId: "lola-validation",
    view: "focus",
  },
  {
    title: "8. Cold-trap proxy: volatile plausibility",
    copy:
      "Low-sun hillshade sweeps from the TMC-2 DTM create a cold-trap proxy. This adds PSR-style plausibility while clearly marking the need for external validation.",
    layerId: "cold-trap",
    view: "focus",
  },
  {
    title: "9. Solar-aware A* traverse",
    copy:
      "The route is computed over accessibility, cold-trap, and low-illumination penalty layers inside a connected valid-data island, producing a defensible LZ-A to SCI-B screening traverse.",
    layerId: "traverse-route",
    view: "focus",
  },
  {
    title: "10. Top 5 m volume estimate",
    copy:
      "The required volume estimate is now represented as a scenario model: candidate area times 5 m depth times assumed ice fraction. It is useful for ISRU planning but not a confirmed reserve measurement.",
    layerId: "ice-volume",
    view: "focus",
  },
  {
    title: "11. Recommendation: land, traverse, excavate",
    copy:
      "The recommendation is to use LZ-A as the safer terrain gate, traverse to SCI-B/DSC-1, and treat the target as a candidate excavation/drilling zone until exact CPR/DOP and ephemeris illumination validation are complete.",
    layerId: "traverse-route",
    view: "fusion",
  },
];

const layerAnalytics = {
  "sar-score": {
    planTitle: "Radar-First Science Targeting",
    planSubtitle: "candidate volatile evidence",
    confidence: 74,
    confidenceLabel: "radar confidence",
    confidenceSubtitle: "candidate evidence",
    confidenceCopy:
      "This view emphasizes DFSAR-derived radar anomalies. High values should be treated as candidate volatile evidence until CPR/DOP-style validation and terrain context agree.",
    profileSubtitle: "radar response bins",
    profile: [42, 55, 63, 77, 81, 68, 59, 72, 64, 83],
    planMetrics: [
      ["Radar evidence", "0.82"],
      ["Cross-pol signal", "0.71"],
      ["Terrain gate", "0.64"],
      ["Claim level", "candidate"],
    ],
    candidates: [
      ["SCI-B", "0.82", "0.21", "0.34", "Prioritize", "good"],
      ["RIM-C", "0.71", "0.46", "0.61", "Review", "warn"],
      ["LZ-A", "0.63", "0.12", "0.18", "Landing", "good"],
    ],
    pipeline: ["HH/VV", "cross-pol", "radar score", "terrain gate", "science target"],
  },
  "cpr-dop-gate": {
    planTitle: "CPR/DOP Radar Detection Gate",
    planSubtitle: "required threshold logic",
    confidence: 72,
    confidenceLabel: "threshold readiness",
    confidenceSubtitle: "proxy, not exact",
    confidenceCopy:
      "The challenge threshold is CPR > 1 and DOP < 0.13. Current extracted rasters support CPR-like and depolarization-like proxy screening, but exact CPR/DOP needs calibrated polarimetric phase/coherency products.",
    profileSubtitle: "radar gate bins",
    profile: [27, 34, 41, 52, 68, 74, 63, 49, 38, 31],
    planMetrics: [
      ["CPR criterion", "> 1"],
      ["DOP criterion", "< 0.13"],
      ["Proxy pass pixels", "2.71%"],
      ["Status", "pending exact"],
    ],
    candidates: [
      ["CPR/DOP proxy", "0.72", "0.28", "0.42", "Gate", "warn"],
      ["SCI-B", "0.82", "0.21", "0.34", "Candidate", "good"],
      ["DSC-1", "0.84", "0.24", "0.39", "Target", "good"],
    ],
    pipeline: ["HH/HV/VH/VV", "ratio proxy", "CPR > 1 gate", "DOP < 0.13 gate", "candidate"],
  },
  "dsc-target": {
    planTitle: "Faustini-Class DSC-1 Target",
    planSubtitle: "doubly shadowed crater proxy",
    confidence: 84,
    confidenceLabel: "target confidence",
    confidenceSubtitle: "proxy target",
    confidenceCopy:
      "DSC-1 combines cold-trap score, shadow persistence, low illumination, low slope, and accessibility. It frames a Faustini-class doubly shadowed crater target until the official supplied crater AOI arrives.",
    profileSubtitle: "DSC proxy bins",
    profile: [61, 72, 84, 95, 88, 79, 67, 58, 71, 83],
    planMetrics: [
      ["Candidate area", "141.68 sq km"],
      ["Mask percentile", "top 6%"],
      ["Depth target", "top 5 m"],
      ["Claim", "proxy DSC"],
    ],
    candidates: [
      ["DSC-1", "0.84", "0.24", "0.39", "Target", "good"],
      ["SCI-B", "0.82", "0.21", "0.34", "Prioritize", "good"],
      ["LZ-A", "0.63", "0.12", "0.18", "Landing", "good"],
    ],
    pipeline: ["cold trap", "shadow", "low illum", "slope/access", "DSC-1 mask"],
  },
  "rough-filter": {
    planTitle: "Rough-Terrain False-Positive Filter",
    planSubtitle: "mentor morphology screen",
    confidence: 73,
    confidenceLabel: "screening confidence",
    confidenceSubtitle: "proxy filter",
    confidenceCopy:
      "This layer reduces the chance of calling rough, radar-bright terrain ice. It combines slope, accessibility, and SAR/cold-trap consistency, but registered OHRC boulder/crater extraction is still needed for final morphology validation.",
    profileSubtitle: "roughness rejection bins",
    profile: [16, 24, 31, 42, 58, 73, 61, 49, 36, 28],
    planMetrics: [
      ["High rough rejected", "16.0%"],
      ["Candidate retained", "12.0%"],
      ["Inputs", "slope/SAR/cold"],
      ["OHRC status", "pending"],
    ],
    candidates: [
      ["DSC-1 lobate rim", "0.78", "0.22", "0.39", "Retain", "good"],
      ["Rocky bright zone", "0.66", "0.71", "0.82", "Reject", "warn"],
      ["LZ-A corridor", "0.52", "0.14", "0.24", "Safe", "good"],
    ],
    pipeline: ["slope", "access", "SAR/cold", "rough reject", "candidate"],
  },
  "ice-volume": {
    planTitle: "Top 5 m Volume Scenario",
    planSubtitle: "ISRU estimate",
    confidence: 69,
    confidenceLabel: "estimate confidence",
    confidenceSubtitle: "scenario model",
    confidenceCopy:
      "Volume is estimated as candidate area times 5 m depth times assumed ice fraction. This satisfies the quantitative outcome as a transparent scenario model, not a confirmed reserve measurement.",
    profileSubtitle: "ice fraction scenarios",
    profile: [21, 32, 44, 57, 67, 82, 93, 78, 64, 49],
    planMetrics: [
      ["Low 3%", "21.25M m3"],
      ["Medium 8%", "56.67M m3"],
      ["High 15%", "106.26M m3"],
      ["Depth", "5 m"],
    ],
    candidates: [
      ["DSC-1 low", "0.69", "0.24", "0.39", "21.25M", "warn"],
      ["DSC-1 med", "0.76", "0.24", "0.39", "56.67M", "good"],
      ["DSC-1 high", "0.81", "0.24", "0.39", "106.26M", "good"],
    ],
    pipeline: ["DSC area", "5 m depth", "ice fraction", "uncertainty", "volume"],
  },
  "tmc-access": {
    planTitle: "Landing Safety Screening",
    planSubtitle: "terrain-first planning",
    confidence: 79,
    confidenceLabel: "terrain confidence",
    confidenceSubtitle: "DTM-derived",
    confidenceCopy:
      "This layer prioritizes low-slope, moderate-relief areas from the valid south-pole TMC-2 DTM. It is the landing-safety gate before science targeting.",
    profileSubtitle: "accessibility samples",
    profile: [64, 71, 75, 83, 78, 69, 73, 66, 81, 76],
    planMetrics: [
      ["Landing safety", "0.79"],
      ["Slope penalty", "0.21"],
      ["Relief penalty", "0.26"],
      ["Best use", "LZ filter"],
    ],
    candidates: [
      ["LZ-A", "0.63", "0.12", "0.18", "Landing", "good"],
      ["SCI-B", "0.82", "0.21", "0.34", "Prioritize", "good"],
      ["RIM-C", "0.71", "0.46", "0.61", "Review", "warn"],
    ],
    pipeline: ["TMC-2 DTM", "slope", "relief", "access score", "landing mask"],
  },
  "traverse-route": {
    planTitle: "Computed Traverse LZ-A to SCI-B",
    planSubtitle: "A* route output",
    confidence: 81,
    confidenceLabel: "route confidence",
    confidenceSubtitle: "screening route",
    confidenceCopy:
      "The route is generated with A* over accessibility, cold-trap, and low-illumination penalty rasters inside one connected valid-data island. It is a planning screen, not rover-qualified navigation.",
    profileSubtitle: "solar-aware path cost",
    profile: [21, 25, 34, 47, 56, 62, 58, 44, 31, 24],
    planMetrics: [
      ["Distance", "13.6 km"],
      ["Relative cost", "173.2"],
      ["Mean illum.", "21.49"],
      ["Low-power path", "72.7%"],
    ],
    candidates: [
      ["LZ-A to SCI-B", "0.77", "0.24", "0.34", "Route", "good"],
      ["LZ-A to RIM-C", "0.71", "0.46", "0.61", "Costly", "warn"],
      ["SCI-B local loop", "0.82", "0.29", "0.41", "Survey", "good"],
    ],
    pipeline: ["access grid", "cold trap", "solar penalty", "A* search", "route layer"],
  },
  "lola-validation": {
    planTitle: "Independent LOLA Terrain Check",
    planSubtitle: "external validation",
    confidence: 88,
    confidenceLabel: "validation confidence",
    confidenceSubtitle: "strong sanity check",
    confidenceCopy:
      "NASA LRO/LOLA 1000 m south-pole products were cropped to the TMC-2 AOI. Regional mean slope agrees within 0.96 degrees, supporting the terrain pipeline as a credible screening layer.",
    profileSubtitle: "LOLA/TMC agreement",
    profile: [82, 86, 91, 88, 84, 90, 87, 85, 89, 92],
    planMetrics: [
      ["TMC slope mean", "10.67 deg"],
      ["LOLA slope mean", "11.63 deg"],
      ["Mean delta", "0.96 deg"],
      ["Agreement", "strong"],
    ],
    candidates: [
      ["TMC AOI", "0.88", "0.11", "0.20", "Validated", "good"],
      ["LOLA slope", "0.86", "0.13", "0.24", "Reference", "good"],
      ["LOLA class", "0.72", "0.28", "0.42", "Context", "good"],
    ],
    pipeline: ["LOLA PGDA", "AOI crop", "slope compare", "roughness", "validation"],
  },
  "cold-trap": {
    planTitle: "Cold-Trap Plausibility Pass",
    planSubtitle: "shadow proxy",
    confidence: 67,
    confidenceLabel: "proxy confidence",
    confidenceSubtitle: "needs validation",
    confidenceCopy:
      "Cold-trap score comes from low-sun terrain simulations. It helps prioritize volatile-friendly terrain but must be validated against ephemeris-based illumination products.",
    profileSubtitle: "shadow persistence bins",
    profile: [72, 78, 69, 81, 84, 76, 62, 58, 66, 71],
    planMetrics: [
      ["Cold-trap proxy", "0.77"],
      ["Sun model", "1.5 deg"],
      ["Azimuth tests", "8"],
      ["Validation", "PGDA"],
    ],
    candidates: [
      ["SCI-B", "0.77", "0.21", "0.34", "Prioritize", "good"],
      ["RIM-C", "0.74", "0.46", "0.61", "Review", "warn"],
      ["LZ-A", "0.48", "0.12", "0.18", "Landing", "good"],
    ],
    pipeline: ["DTM", "hillshade", "shadow", "cold proxy", "science gate"],
  },
  illumination: {
    planTitle: "Power and Thermal Feasibility",
    planSubtitle: "illumination proxy",
    confidence: 64,
    confidenceLabel: "illumination confidence",
    confidenceSubtitle: "screening proxy",
    confidenceCopy:
      "Illumination availability is derived from low-sun hillshade sweeps. It is useful for rover power screening, but not a replacement for orbital illumination products.",
    profileSubtitle: "illumination bins",
    profile: [58, 66, 72, 69, 61, 53, 47, 55, 63, 70],
    planMetrics: [
      ["Power support", "0.70"],
      ["Shadow risk", "0.43"],
      ["Sun altitude", "1.5 deg"],
      ["Role", "rover gate"],
    ],
    candidates: [
      ["LZ-A", "0.63", "0.12", "0.18", "Power OK", "good"],
      ["SCI-B", "0.82", "0.21", "0.34", "Short stay", "warn"],
      ["RIM-C", "0.71", "0.46", "0.61", "Review", "warn"],
    ],
    pipeline: ["DTM", "sun angles", "illumination", "power gate", "route window"],
  },
  "tmc-slope": {
    planTitle: "Slope Hazard Review",
    planSubtitle: "terrain constraint",
    confidence: 76,
    confidenceLabel: "slope confidence",
    confidenceSubtitle: "DTM-derived",
    confidenceCopy:
      "Slope from TMC-2 DTM identifies terrain that should be penalized for landing and rover movement. Low slope does not guarantee boulder safety.",
    profileSubtitle: "slope-risk bins",
    profile: [22, 34, 41, 57, 66, 48, 39, 29, 36, 44],
    planMetrics: [
      ["Mean slope", "7.4 deg"],
      ["High-risk slope", "0.31"],
      ["Low-slope area", "0.74"],
      ["Role", "hazard gate"],
    ],
    candidates: [
      ["LZ-A", "0.63", "0.12", "0.18", "Landing", "good"],
      ["SCI-B", "0.82", "0.21", "0.34", "Prioritize", "good"],
      ["RIM-C", "0.71", "0.46", "0.61", "Review", "warn"],
    ],
    pipeline: ["DTM", "gradient", "slope deg", "risk map", "cost layer"],
  },
  "tmc-elevation": {
    planTitle: "Terrain Context Inspection",
    planSubtitle: "elevation model",
    confidence: 73,
    confidenceLabel: "terrain context",
    confidenceSubtitle: "polar projection",
    confidenceCopy:
      "Elevation context helps interpret crater rims, depressions, and accessible corridors. The DTM spans roughly 88.65S to 81.50S.",
    profileSubtitle: "relative elevation",
    profile: [46, 52, 61, 58, 73, 69, 55, 49, 57, 64],
    planMetrics: [
      ["Product", "TMC-2 DTM"],
      ["Pixel scale", "10 m"],
      ["Latitude span", "88.65S-81.50S"],
      ["Projection", "polar stereo"],
    ],
    candidates: [
      ["LZ-A", "0.63", "0.12", "0.18", "Landing", "good"],
      ["SCI-B", "0.82", "0.21", "0.34", "Prioritize", "good"],
      ["RIM-C", "0.71", "0.46", "0.61", "Review", "warn"],
    ],
    pipeline: ["TMC-2", "DTM", "projection", "terrain", "planning"],
  },
  "tmc-ortho": {
    planTitle: "Visual Terrain Context",
    planSubtitle: "orthographic browse",
    confidence: 66,
    confidenceLabel: "visual context",
    confidenceSubtitle: "browse layer",
    confidenceCopy:
      "The orthographic browse layer gives local terrain texture and crater context. It is not a substitute for full-resolution hazard extraction.",
    profileSubtitle: "visual texture bins",
    profile: [35, 44, 52, 63, 59, 47, 42, 51, 56, 61],
    planMetrics: [
      ["Visual context", "0.72"],
      ["Full ortho", "zipped"],
      ["Disk saved", "~2 GB"],
      ["Role", "context"],
    ],
    candidates: [
      ["LZ-A", "0.63", "0.12", "0.18", "Inspect", "good"],
      ["SCI-B", "0.82", "0.21", "0.34", "Inspect", "good"],
      ["RIM-C", "0.71", "0.46", "0.61", "Review", "warn"],
    ],
    pipeline: ["TMC-2", "ortho", "browse", "texture", "visual QA"],
  },
  "sar-browse": {
    planTitle: "Radar Context Review",
    planSubtitle: "DFSAR browse",
    confidence: 70,
    confidenceLabel: "browse confidence",
    confidenceSubtitle: "context layer",
    confidenceCopy:
      "DFSAR browse gives radar scene context. The derived SAR evidence layer should be used for ranking; this view supports visual QA.",
    profileSubtitle: "radar texture bins",
    profile: [48, 53, 59, 71, 67, 62, 55, 64, 69, 73],
    planMetrics: [
      ["Radar context", "0.78"],
      ["Payload", "DFSAR"],
      ["Polarimetry", "FP"],
      ["Role", "QA"],
    ],
    candidates: [
      ["SCI-B", "0.82", "0.21", "0.34", "Prioritize", "good"],
      ["RIM-C", "0.71", "0.46", "0.61", "Review", "warn"],
      ["LZ-A", "0.63", "0.12", "0.18", "Landing", "good"],
    ],
    pipeline: ["DFSAR", "browse", "scene QA", "compare", "derive"],
  },
  "ohr-a": {
    planTitle: "OHRC Hazard Context A",
    planSubtitle: "visual hazard",
    confidence: 58,
    confidenceLabel: "overlap confidence",
    confidenceSubtitle: "needs registration",
    confidenceCopy:
      "OHRC supports boulder/crater hazard reasoning, but exact overlap with the current TMC/DFSAR AOI still needs footprint registration.",
    profileSubtitle: "hazard texture bins",
    profile: [51, 46, 57, 63, 49, 54, 61, 58, 52, 47],
    planMetrics: [
      ["Visual hazard", "0.68"],
      ["Overlap status", "pending"],
      ["Use", "context"],
      ["Next", "footprints"],
    ],
    candidates: [
      ["LZ-A", "0.63", "0.12", "0.18", "Inspect", "good"],
      ["RIM-C", "0.71", "0.46", "0.61", "Review", "warn"],
      ["SCI-B", "0.82", "0.21", "0.34", "Inspect", "good"],
    ],
    pipeline: ["OHRC", "browse", "geometry CSV", "hazards", "overlay"],
  },
  "ohr-b": {
    planTitle: "OHRC Hazard Context B",
    planSubtitle: "visual comparison",
    confidence: 56,
    confidenceLabel: "overlap confidence",
    confidenceSubtitle: "needs registration",
    confidenceCopy:
      "Second OHRC strip is useful for comparison and presentation, but should not drive ranking until its exact footprint is registered.",
    profileSubtitle: "hazard texture bins",
    profile: [44, 52, 48, 55, 61, 57, 50, 46, 53, 59],
    planMetrics: [
      ["Visual hazard", "0.66"],
      ["Overlap status", "pending"],
      ["Use", "context"],
      ["Next", "footprints"],
    ],
    candidates: [
      ["LZ-A", "0.63", "0.12", "0.18", "Inspect", "good"],
      ["SCI-B", "0.82", "0.21", "0.34", "Inspect", "good"],
      ["RIM-C", "0.71", "0.46", "0.61", "Review", "warn"],
    ],
    pipeline: ["OHRC", "browse", "compare", "hazards", "overlay"],
  },
};

const list = document.querySelector("#layerList");
const image = document.querySelector("#mainLayer");
const description = document.querySelector("#layerDescription");
const score = document.querySelector("#scoreValue");
const title = document.querySelector("#layerTitle");
const viewButtons = document.querySelectorAll(".tool-button");
const sourceGrid = document.querySelector("#sourceGrid");
const methodGrid = document.querySelector("#methodGrid");
const provenanceRows = document.querySelector("#provenanceRows");
const judgeDemo = document.querySelector("#judgeDemo");
const startDemo = document.querySelector("#startDemo");
const prevDemo = document.querySelector("#prevDemo");
const nextDemo = document.querySelector("#nextDemo");
const demoStepTitle = document.querySelector("#demoStepTitle");
const demoStepCopy = document.querySelector("#demoStepCopy");
const demoStepCounter = document.querySelector("#demoStepCounter");
const demoProgress = document.querySelector("#demoProgress");
const planSubtitle = document.querySelector("#planSubtitle");
const planTitle = document.querySelector("#planTitle");
const planMetrics = document.querySelector("#planMetrics");
const confidenceSubtitle = document.querySelector("#confidenceSubtitle");
const confidenceRing = document.querySelector("#confidenceRing");
const confidenceValue = document.querySelector("#confidenceValue");
const confidenceLabel = document.querySelector("#confidenceLabel");
const confidenceCopy = document.querySelector("#confidenceCopy");
const profileSubtitle = document.querySelector("#profileSubtitle");
const profileChart = document.querySelector("#profileChart");
const candidateRows = document.querySelector("#candidateRows");
const pipelineSteps = document.querySelector("#pipelineSteps");

let selectedLayer = layers[0];
let viewMode = "focus";
let demoIndex = -1;

function currentImagePath(layer) {
  if (viewMode === "fusion") return fusionPath;
  if (viewMode === "raw") return layer.rawPath;
  return layer.focusPath;
}

function versioned(path) {
  return `${path}?v=${assetVersion}`;
}

function renderAnalytics(layer) {
  const analytics = layerAnalytics[layer.id] || layerAnalytics["sar-score"];
  planSubtitle.textContent = analytics.planSubtitle;
  planTitle.textContent = analytics.planTitle;
  planMetrics.innerHTML = analytics.planMetrics
    .map(([label, value]) => `<div><dt>${label}</dt><dd>${value}</dd></div>`)
    .join("");

  confidenceSubtitle.textContent = analytics.confidenceSubtitle;
  confidenceValue.textContent = analytics.confidence;
  confidenceLabel.textContent = analytics.confidenceLabel;
  confidenceCopy.textContent = analytics.confidenceCopy;
  confidenceRing.style.setProperty("--confidence", `${analytics.confidence}%`);

  profileSubtitle.textContent = analytics.profileSubtitle;
  profileChart.innerHTML = analytics.profile.map((value) => `<span style="height: ${value}%"></span>`).join("");

  candidateRows.innerHTML = analytics.candidates
    .map(
      ([site, evidence, slope, traverse, decision, tone]) => `
        <tr>
          <td>${site}</td>
          <td>${evidence}</td>
          <td>${slope}</td>
          <td>${traverse}</td>
          <td><span class="tag ${tone}">${decision}</span></td>
        </tr>
      `,
    )
    .join("");

  pipelineSteps.innerHTML = analytics.pipeline.map((step) => `<span>${step}</span>`).join("");
}

function selectLayer(layer) {
  selectedLayer = layer;
  image.src = versioned(currentImagePath(layer));
  image.alt = viewMode === "fusion" ? "Lunar south pole evidence fusion board" : layer.name;
  title.textContent = viewMode === "fusion" ? "Evidence Fusion Board" : layer.name;
  description.textContent = `${layer.name}: ${layer.description} Source: ${layer.source}.`;
  score.textContent = layer.score;
  renderAnalytics(layer);

  document.querySelectorAll(".layer-btn").forEach((button) => {
    button.classList.toggle("active", button.dataset.layerId === layer.id);
  });
}

function setViewMode(mode) {
  viewMode = mode;
  viewButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.view === mode);
  });
  selectLayer(selectedLayer);
}

function layerById(id) {
  return layers.find((layer) => layer.id === id) || layers[0];
}

function renderDemoState() {
  const active = demoIndex >= 0;
  judgeDemo.classList.toggle("active", active);
  prevDemo.disabled = !active || demoIndex === 0;
  nextDemo.disabled = !active || demoIndex === demoSteps.length - 1;
  startDemo.textContent = active ? "Restart Demo" : "Start Demo";
  demoStepCounter.textContent = active ? `${demoIndex + 1} / ${demoSteps.length}` : `0 / ${demoSteps.length}`;

  if (active) {
    const step = demoSteps[demoIndex];
    demoStepTitle.textContent = step.title;
    demoStepCopy.textContent = step.copy;
  } else {
    demoStepTitle.textContent = "Guided finalist walkthrough";
    demoStepCopy.textContent =
      "Step through the mission story from uncertainty to a ranked landing-and-traverse recommendation.";
  }

  [...demoProgress.children].forEach((button, index) => {
    button.classList.toggle("active", active && index <= demoIndex);
  });
}

function goToDemoStep(index) {
  demoIndex = Math.max(0, Math.min(index, demoSteps.length - 1));
  const step = demoSteps[demoIndex];
  viewMode = step.view;
  viewButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.view === viewMode);
  });
  selectLayer(layerById(step.layerId));
  renderDemoState();
}

layers.forEach((layer) => {
  const button = document.createElement("button");
  button.className = "layer-btn";
  button.type = "button";
  button.dataset.layerId = layer.id;
  button.innerHTML = `
    <img src="${versioned(layer.thumbnail)}" alt="" />
    <span><strong>${layer.name}</strong><span>${layer.source}</span></span>
    <b>${layer.score}</b>
  `;
  button.addEventListener("click", () => selectLayer(layer));
  list.appendChild(button);
});

viewButtons.forEach((button) => {
  button.addEventListener("click", () => setViewMode(button.dataset.view));
});

demoSteps.forEach((_, index) => {
  const dot = document.createElement("button");
  dot.type = "button";
  dot.setAttribute("aria-label", `Go to demo step ${index + 1}`);
  dot.addEventListener("click", () => goToDemoStep(index));
  demoProgress.appendChild(dot);
});

startDemo.addEventListener("click", () => goToDemoStep(0));
prevDemo.addEventListener("click", () => goToDemoStep(demoIndex <= 0 ? 0 : demoIndex - 1));
nextDemo.addEventListener("click", () => goToDemoStep(demoIndex < 0 ? 0 : demoIndex + 1));

sources.forEach((source) => {
  const card = document.createElement("article");
  card.className = "source-card";
  card.innerHTML = `
    <span class="source-status ${source.status}">${source.status}</span>
    <h3>${source.name}</h3>
    <p>${source.contribution}</p>
    <a href="${source.url}" target="_blank" rel="noreferrer">Open source</a>
  `;
  sourceGrid.appendChild(card);
});

methods.forEach((method) => {
  const item = document.createElement("article");
  item.className = "method-item";
  item.innerHTML = `
    <div class="method-head">
      <h3>${method.title}</h3>
      <span>${method.output}</span>
    </div>
    <div class="method-flow">
      ${method.inputs.map((input) => `<b>${input}</b>`).join("")}
      <strong>${method.formula}</strong>
    </div>
    <p>${method.note}</p>
  `;
  methodGrid.appendChild(item);
});

provenanceRows.innerHTML = provenance
  .map(
    (row) => `
      <article class="provenance-item">
        <div class="provenance-main">
          <span class="payload-chip">${row.payload}</span>
          <div>
            <h3>${row.product}</h3>
            <p>${row.role}</p>
          </div>
        </div>
        <div class="provenance-meta">
          <span>${row.date}</span>
          <span class="tag ${row.status === "deprecated" ? "warn" : "good"}">${row.status}</span>
        </div>
      </article>
    `,
  )
  .join("");

selectLayer(layers[0]);
renderDemoState();
