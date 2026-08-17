const assetVersion = "20260621-zoom-refine";
const demoStateKey = "lunarIceJudgeDemoState";

const layers = [
  {
    id: "compliance-matrix",
    name: "Problem 8 Compliance Matrix",
    source: "mentor expected outcomes",
    focusPath: "../data/processed/demo_assets/problem8_compliance_matrix_focus.png",
    rawPath: "../data/processed/derived_layers/problem8_compliance_matrix_summary.json",
    thumbnail: "../data/processed/demo_assets/problem8_compliance_matrix_focus.png",
    description:
      "Judge-facing matrix mapping each required mentor workflow/outcome to current evidence, readiness status, and the exact upgrade needed to close remaining gaps.",
    score: 74,
  },
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
    id: "mentor-solution",
    name: "Mentor Expected Solution Tracker",
    source: "PS 8 mentor DOCX requirements",
    focusPath: "../data/processed/demo_assets/mentor_expected_solution_focus.png",
    rawPath: "../data/processed/demo_assets/mentor_expected_solution_focus.png",
    thumbnail: "../data/processed/demo_assets/mentor_expected_solution_focus.png",
    description:
      "Direct mapping of the mentor problem-statement workflow to current prototype outputs: PSR/DSC mapping, CPR/DOP gate, OHRC morphology, terrain safety, solar-aware traverse, and top-5m volume.",
    score: 86,
  },
  {
    id: "faustini-reference",
    name: "Faustini F2 Reference Target",
    source: "mentor DOCX target model",
    focusPath: "../data/processed/demo_assets/faustini_f2_reference_focus.png",
    rawPath: "../data/processed/demo_assets/faustini_f2_reference_focus.png",
    thumbnail: "../data/processed/demo_assets/faustini_f2_reference_focus.png",
    description:
      "Reference model from the mentor material: a Faustini permanently shadowed region, F2-style approximately 1.1 km doubly shadowed crater, lobate-rim morphology, CPR > 1, and DOP < 0.13.",
    score: 83,
  },
  {
    id: "radar-reference",
    name: "CPR/DOP Reference Comparison",
    source: "mentor thresholds + current DFSAR audit",
    focusPath: "../data/processed/demo_assets/radar_reference_comparison_focus.png",
    rawPath: "../data/processed/demo_assets/radar_reference_comparison_focus.png",
    thumbnail: "../data/processed/demo_assets/radar_reference_comparison_focus.png",
    description:
      "Shows the difference between the mentor's exact CPR/DOP validation target and the current downloaded DFSAR package, which supports audited proxy screening but not exact polarimetric products.",
    score: 80,
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
    id: "experimental-cpr-dop",
    name: "Experimental CPR/DOP Proxy",
    source: "HH/HV/VH/VV-derived screening",
    focusPath: "../data/processed/demo_assets/experimental_cpr_dop_proxy_focus.png",
    rawPath: "../data/processed/derived_layers/experimental_cpr_dop_proxy_summary.json",
    thumbnail: "../data/processed/demo_assets/experimental_cpr_dop_proxy_focus.png",
    description:
      "Algorithmic CPR-like and DOP-like proxy screen from available DFSAR-derived HH/HV/VH/VV layers. It narrows the radar-science gap visually, while exact CPR/DOP remains a calibrated polarimetry requirement.",
    score: 77,
  },
  {
    id: "validation-gates",
    name: "Validation Gate Readiness",
    source: "DFSAR CPR/DOP + AOI + OHRC audit",
    focusPath: "../data/processed/demo_assets/validation_gate_readiness_focus.png",
    rawPath: "../data/processed/derived_layers/validation_gate_readiness_summary.json",
    thumbnail: "../data/processed/demo_assets/validation_gate_readiness_focus.png",
    description:
      "Single readiness layer for the three hard gates: exact CPR/DOP computation, official supplied crater AOI replacement, and OHRC map-projected AOI registration. It is engineered to switch from proxy to exact once official products arrive.",
    score: 78,
  },
  {
    id: "dfsar-audit",
    name: "DFSAR Polarimetry Audit",
    source: "PDS4 labels + extracted DFSAR products",
    focusPath: "../data/processed/demo_assets/dfsar_polarimetry_audit_focus.png",
    rawPath: "../data/processed/demo_assets/dfsar_polarimetry_audit_focus.png",
    thumbnail: "../data/processed/demo_assets/dfsar_polarimetry_audit_focus.png",
    description:
      "Audits the current DFSAR package for exact CPR/DOP readiness. Four linear polarizations and phase-orthogonality metadata are present, but no CPR, DOP, Stokes, coherency, covariance, or circular-pol product files were found in the extracted set.",
    score: 76,
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
    source: "PDS LDEM_85S_20M polar DEM",
    focusPath: "../data/processed/demo_assets/lola_validation_focus.png",
    rawPath: "../data/processed/derived_layers/lola_85s20m_tmc_overlap_slope_deg.png",
    thumbnail: "../data/processed/demo_assets/lola_validation_focus.png",
    description:
      "Independent NASA PDS LRO/LOLA 20 m south-pole DEM cropped to the Chandrayaan-2 TMC-2 overlap. LOLA-derived mean slope differs from the TMC-derived slope by only 0.63 degrees in the overlapping validation region.",
    score: 91,
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
    id: "tmc2-202312-dtm-browse",
    name: "TMC-2 South Pole DTM Browse",
    source: "ch2_tmc_ndn_20231203T0019079527_b_bdt_d18",
    focusPath: "../data/processed/extracted_tmc2_south_pole/browse/derived/20231203/ch2_tmc_ndn_20231203T0019079527_b_bdt_d18.png",
    rawPath: "../data/processed/extracted_tmc2_south_pole/browse/derived/20231203/ch2_tmc_ndn_20231203T0019079527_b_bdt_d18.png",
    thumbnail: "../data/processed/derived_layers/tmc2_south_pole_dtm_browse.png",
    description:
      "Actual downloaded TMC-2 DTM browse product for the valid south-pole strip. Use this for visual scale/context before inspecting derived slope and accessibility layers.",
    score: 76,
  },
  {
    id: "tmc2-202312-ortho-browse",
    name: "TMC-2 South Pole Ortho Browse",
    source: "ch2_tmc_ndn_20231203T0019079527_b_bot_d18",
    focusPath: "../data/processed/extracted_tmc2_south_pole/browse/derived/20231203/ch2_tmc_ndn_20231203T0019079527_b_bot_d18.png",
    rawPath: "../data/processed/extracted_tmc2_south_pole/browse/derived/20231203/ch2_tmc_ndn_20231203T0019079527_b_bot_d18.png",
    thumbnail: "../data/processed/derived_layers/tmc2_south_pole_orthobrowse.png",
    description:
      "Actual downloaded TMC-2 orthographic browse image for the valid south-pole strip. This is the visual terrain sheet behind landing and traverse reasoning.",
    score: 78,
  },
  {
    id: "tmc2-202504-dtm-browse",
    name: "TMC-2 Non-Polar DTM Test Strip",
    source: "ch2_tmc_ndn_20250426T0752081453_b_bdt_d18",
    focusPath: "../data/processed/extracted_minimal/browse/derived/20250426/ch2_tmc_ndn_20250426T0752081453_b_bdt_d18.png",
    rawPath: "../data/processed/extracted_minimal/browse/derived/20250426/ch2_tmc_ndn_20250426T0752081453_b_bdt_d18.png",
    thumbnail: "../data/processed/quicklooks/ch2_tmc_ndn_20250426T0752081453_b_bdt_d18_quicklook.png",
    description:
      "Earlier downloaded TMC-2 DTM browse strip retained as non-polar regression/test data. It should not drive the final south-pole recommendation.",
    score: 42,
  },
  {
    id: "tmc2-202504-ortho-browse",
    name: "TMC-2 Non-Polar Ortho Test Strip",
    source: "ch2_tmc_ndn_20250426T0752081453_b_bot_d18",
    focusPath: "../data/processed/extracted_minimal/browse/derived/20250426/ch2_tmc_ndn_20250426T0752081453_b_bot_d18.png",
    rawPath: "../data/processed/extracted_minimal/browse/derived/20250426/ch2_tmc_ndn_20250426T0752081453_b_bot_d18.png",
    thumbnail: "../data/processed/quicklooks/ch2_tmc_ndn_20250426T0752081453_b_bot_d18_quicklook.png",
    description:
      "Earlier downloaded TMC-2 orthographic browse strip retained for pipeline regression and UI testing; not part of the final south-pole AOI.",
    score: 42,
  },
  {
    id: "sar-browse",
    name: "DFSAR Radar Browse",
    source: "ch2_sar_ncls_20200913t042439405",
    focusPath: "../data/processed/extracted_minimal/browse/calibrated/20200913/ch2_sar_ncls_20200913t042439405_b_brw_xx_fp_xx_d18.png",
    rawPath: "../data/processed/extracted_minimal/browse/calibrated/20200913/ch2_sar_ncls_20200913t042439405_b_brw_xx_fp_xx_d18.png",
    thumbnail: "../data/processed/quicklooks/ch2_sar_ncls_20200913t042439405_b_brw_xx_fp_xx_d18_quicklook.png",
    description:
      "Calibrated full-polarimetry DFSAR browse layer used as the radar context behind candidate subsurface-ice evidence.",
    score: 78,
  },
  {
    id: "ohr-0",
    name: "OHRC Hazard Strip 0",
    source: "ch2_ohr_ncp_20260103T0410224157",
    focusPath: "../data/processed/extracted_minimal/browse/calibrated/20260103/ch2_ohr_ncp_20260103T0410224157_b_brw_d18.png",
    rawPath: "../data/processed/extracted_minimal/browse/calibrated/20260103/ch2_ohr_ncp_20260103T0410224157_b_brw_d18.png",
    thumbnail: "../data/processed/quicklooks/ch2_ohr_ncp_20260103T0410224157_b_brw_d18_quicklook.png",
    description:
      "Additional OHRC strip from the same 2026-01-03 south-pole batch. Geometry and browse-scale crater/boulder candidates are included in the expanded footprint audit.",
    score: 69,
  },
  {
    id: "ohr-a",
    name: "OHRC Hazard Strip A",
    source: "ch2_ohr_ncp_20260103T0609041371",
    focusPath: "../data/processed/extracted_minimal/browse/calibrated/20260103/ch2_ohr_ncp_20260103T0609041371_b_brw_d18.png",
    rawPath: "../data/processed/extracted_minimal/browse/calibrated/20260103/ch2_ohr_ncp_20260103T0609041371_b_brw_d18.png",
    thumbnail: "../data/processed/quicklooks/ch2_ohr_ncp_20260103T0609041371_b_brw_d18_quicklook.png",
    description:
      "High-resolution optical browse strip for crater, boulder, and local roughness inspection near candidate landing corridors.",
    score: 68,
  },
  {
    id: "ohr-b",
    name: "OHRC Hazard Strip B",
    source: "ch2_ohr_ncp_20260103T1005176450",
    focusPath: "../data/processed/extracted_minimal/browse/calibrated/20260103/ch2_ohr_ncp_20260103T1005176450_b_brw_d18.png",
    rawPath: "../data/processed/extracted_minimal/browse/calibrated/20260103/ch2_ohr_ncp_20260103T1005176450_b_brw_d18.png",
    thumbnail: "../data/processed/quicklooks/ch2_ohr_ncp_20260103T1005176450_b_brw_d18_quicklook.png",
    description:
      "Second OHRC strip for visual comparison and local hazard explanation. Exact overlap with the TMC/DFSAR AOI still needs registration.",
    score: 66,
  },
  {
    id: "ohr-c",
    name: "OHRC Hazard Strip C",
    source: "ch2_ohr_ncp_20260103T1203563771",
    focusPath: "../data/processed/extracted_minimal/browse/calibrated/20260103/ch2_ohr_ncp_20260103T1203563771_b_brw_d18.png",
    rawPath: "../data/processed/extracted_minimal/browse/calibrated/20260103/ch2_ohr_ncp_20260103T1203563771_b_brw_d18.png",
    thumbnail: "../data/processed/quicklooks/ch2_ohr_ncp_20260103T1203563771_b_brw_d18_quicklook.png",
    description:
      "Fourth OHRC strip in the expanded hazard-context set. It improves morphology coverage while exact crater-AOI footprint registration remains pending.",
    score: 68,
  },
  {
    id: "ohr-footprint",
    name: "OHRC Footprint Registration",
    source: "OHRC per-pixel geometry CSV",
    focusPath: "../data/processed/demo_assets/ohrc_footprint_registration_focus.png",
    rawPath: "../data/processed/demo_assets/ohrc_footprint_registration_focus.png",
    thumbnail: "../data/processed/demo_assets/ohrc_footprint_registration_focus.png",
    description:
      "Footprint audit from OHRC per-pixel selenographic geometry. Four downloaded OHRC strips overlap the regional TMC-2 latitude span; exact map-projected AOI registration against the official supplied crater remains the next step.",
    score: 75,
  },
  {
    id: "ohr-hazards",
    name: "OHRC Hazard Extraction",
    source: "browse-scale crater/boulder candidates",
    focusPath: "../data/processed/demo_assets/ohrc_hazard_extraction_focus.png",
    rawPath: "../data/processed/demo_assets/ohrc_hazard_extraction_focus.png",
    thumbnail: "../data/processed/demo_assets/ohrc_hazard_extraction_focus.png",
    description:
      "Browse-scale OHRC contrast and gradient ranking marks crater/boulder candidate zones for inspection. This is not full-resolution hazard certification, but it moves OHRC beyond passive context.",
    score: 73,
  },
];

const primaryLayerIds = [
  "compliance-matrix",
  "mentor-solution",
  "dsc-target",
  "sar-score",
  "cpr-dop-gate",
  "experimental-cpr-dop",
  "validation-gates",
  "rough-filter",
  "tmc-access",
  "cold-trap",
  "traverse-route",
  "ice-volume",
  "lola-validation",
  "ohr-hazards",
];

const productLayerIds = [
  "sar-browse",
  "ohr-0",
  "ohr-a",
  "ohr-b",
  "ohr-c",
  "tmc2-202312-dtm-browse",
  "tmc2-202312-ortho-browse",
  "tmc-elevation",
  "tmc-ortho",
  "tmc2-202504-dtm-browse",
  "tmc2-202504-ortho-browse",
];

const productLayerIdSet = new Set(productLayerIds);
const sourceProductDimensions = {
  "sar-browse": "78 x 103 browse preview",
  "ohr-0": "1200 x 10106 browse strip",
  "ohr-a": "1200 x 10107 browse strip",
  "ohr-b": "1200 x 10107 browse strip",
  "ohr-c": "1200 x 10107 browse strip",
  "tmc2-202312-dtm-browse": "1558 x 1648 browse product",
  "tmc2-202312-ortho-browse": "3117 x 3296 browse product",
  "tmc2-202504-dtm-browse": "349 x 7971 test strip",
  "tmc2-202504-ortho-browse": "699 x 15942 test strip",
};

const fusionPath = "../data/processed/demo_assets/fusion_board.png";
const candidateSites = [
  {
    id: "SCI-B",
    type: "science",
    x: 55,
    y: 72,
    label: "priority excavation target",
    iceProbability: 0.74,
    radarEvidence: 0.82,
    terrainSafety: 0.79,
    coldTrap: 0.86,
    ohrcHazard: 0.31,
    volumeRange: "21-106M m3",
    status: "Prioritize",
    narrative:
      "Best current science target: strong radar/cold-trap agreement with manageable terrain risk. Final claim still needs exact CPR/DOP and official crater AOI registration.",
  },
  {
    id: "DSC-1",
    type: "science",
    x: 47,
    y: 58,
    label: "Faustini-class DSC proxy",
    iceProbability: 0.69,
    radarEvidence: 0.76,
    terrainSafety: 0.72,
    coldTrap: 0.91,
    ohrcHazard: 0.38,
    volumeRange: "18-92M m3",
    status: "Candidate",
    narrative:
      "Primary doubly shadowed crater proxy. It is the mission-story anchor until the official supplied crater AOI replaces this working geometry.",
  },
  {
    id: "RIM-C",
    type: "validation",
    x: 38,
    y: 58,
    label: "rocky false-positive review",
    iceProbability: 0.47,
    radarEvidence: 0.71,
    terrainSafety: 0.39,
    coldTrap: 0.52,
    ohrcHazard: 0.61,
    volumeRange: "review only",
    status: "Review",
    narrative:
      "Radar-bright but risky: steeper/rougher morphology makes it a false-positive review site rather than the first excavation recommendation.",
  },
];

const landingSites = [
  {
    id: "LZ-A",
    type: "landing",
    x: 47,
    y: 24,
    label: "low slope landing gate",
    terrainSafety: 0.88,
    solarAvailability: 0.76,
    narrative: "Current safest landing gate: low slope, moderate relief, and workable power exposure.",
  },
  {
    id: "LZ-B",
    type: "landing",
    x: 33,
    y: 32,
    label: "alternate ridge landing",
    terrainSafety: 0.81,
    solarAvailability: 0.82,
    narrative: "Longer traverse but better lighting window; useful as a contingency landing site.",
  },
  {
    id: "LZ-C",
    type: "landing",
    x: 66,
    y: 29,
    label: "shorter approach, higher risk",
    terrainSafety: 0.69,
    solarAvailability: 0.63,
    narrative: "Closer to SCI-B but terrain roughness makes it secondary.",
  },
];

const routeStrategies = [
  {
    id: "route-a",
    name: "A: Ridge-safe",
    landingId: "LZ-A",
    decision: "Recommended",
    weights: { terrain: 0.52, solar: 0.28, hazard: 0.2, directness: 0.12 },
  },
  {
    id: "route-b",
    name: "B: Sunlit ridge",
    landingId: "LZ-B",
    decision: "Power backup",
    weights: { terrain: 0.32, solar: 0.48, hazard: 0.16, directness: 0.08 },
  },
  {
    id: "route-c",
    name: "C: Direct scout",
    landingId: "LZ-C",
    decision: "Short but risky",
    weights: { terrain: 0.22, solar: 0.14, hazard: 0.2, directness: 0.52 },
  },
];

let generatedRoutes = [];

const layerScale = {
  default: { labelKm: 25, pixelScale: "screening view", context: "regional evidence layer" },
  "sar-score": { labelKm: 15, pixelScale: "60 m/pixel processed SAR", context: "DFSAR radar scoring strip" },
  "experimental-cpr-dop": { labelKm: 15, pixelScale: "60 m/pixel proxy grid", context: "CPR/DOP-style radar screening" },
  "cpr-dop-gate": { labelKm: 15, pixelScale: "threshold card", context: "radar validation logic" },
  "dsc-target": { labelKm: 25, pixelScale: "TMC/SAR fused proxy", context: "Faustini-class DSC target search" },
  "rough-filter": { labelKm: 25, pixelScale: "terrain morphology proxy", context: "rocky false-positive rejection" },
  "tmc-access": { labelKm: 25, pixelScale: "10 m/pixel source DTM", context: "TMC-2 landing accessibility" },
  "tmc-slope": { labelKm: 25, pixelScale: "10 m/pixel source DTM", context: "TMC-2 slope risk" },
  "tmc-elevation": { labelKm: 25, pixelScale: "10 m/pixel source DTM", context: "TMC-2 elevation model" },
  "tmc-ortho": { labelKm: 25, pixelScale: "TMC-2 orthographic browse", context: "TMC-2 visual terrain context" },
  "tmc2-202312-dtm-browse": { labelKm: 25, pixelScale: "TMC-2 DTM browse product", context: "downloaded south-pole DTM browse" },
  "tmc2-202312-ortho-browse": { labelKm: 25, pixelScale: "TMC-2 ortho browse product", context: "downloaded south-pole optical terrain browse" },
  "tmc2-202504-dtm-browse": { labelKm: 10, pixelScale: "non-polar TMC DTM test browse", context: "deprecated regression strip" },
  "tmc2-202504-ortho-browse": { labelKm: 10, pixelScale: "non-polar TMC ortho test browse", context: "deprecated regression strip" },
  "sar-browse": { labelKm: 15, pixelScale: "DFSAR browse product", context: "downloaded radar browse" },
  "cold-trap": { labelKm: 25, pixelScale: "TMC-2 hillshade proxy", context: "PSR/cold-trap screening" },
  illumination: { labelKm: 25, pixelScale: "low-sun terrain proxy", context: "rover power screening" },
  "traverse-route": { labelKm: 25, pixelScale: "A* screening route", context: "landing-to-science traverse" },
  "ice-volume": { labelKm: 25, pixelScale: "DSC-1 area scenario", context: "top 0-5 m volume model" },
  "lola-validation": { labelKm: 20, pixelScale: "20 m/pixel LOLA DEM", context: "external terrain validation" },
  "ohr-hazards": { labelKm: 2, pixelScale: "OHRC browse zoom chips", context: "optical hazard morphology" },
  "ohr-0": { labelKm: 2, pixelScale: "OHRC browse from sub-meter source", context: "optical strip inspection" },
  "ohr-a": { labelKm: 2, pixelScale: "OHRC browse from sub-meter source", context: "optical strip inspection" },
  "ohr-b": { labelKm: 2, pixelScale: "OHRC browse from sub-meter source", context: "optical strip inspection" },
  "ohr-c": { labelKm: 2, pixelScale: "OHRC browse from sub-meter source", context: "optical strip inspection" },
};

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
    contribution: "Independent LRO/LOLA LDEM_85S_20M polar DEM now cropped to the TMC-2 overlap for external terrain validation.",
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
    name: "Mentor PS 8 DOCX",
    status: "mapped",
    url: "#",
    contribution: "Embedded mentor slides now drive the mission-planner framing, Faustini/F2 target reference, lobate-rim cue, and expected solution tracker.",
  },
  {
    name: "OHRC Geometry CSVs",
    status: "used",
    url: "#",
    contribution: "Per-pixel selenographic coordinates used for footprint readiness and regional overlap audit before full AOI registration.",
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
    title: "Mentor Requirement Tracker",
    inputs: ["DOCX steps", "current layers", "status"],
    output: "judge readiness",
    formula: "required outcome -> evidence layer -> caveat",
    note: "Turns the mentor's expected workflow into a visible coverage matrix so judges can see what is implemented, what is audited, and what remains pending.",
  },
  {
    title: "Faustini/F2 Target Model",
    inputs: ["Faustini PSR", "lobate rim", "CPR/DOP"],
    output: "reference target",
    formula: "F2 cue set -> DSC-1 proxy alignment",
    note: "Uses the mentor-provided target pattern as the scientific reference while keeping the current target labeled as a proxy until official AOI data arrives.",
  },
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
    title: "DFSAR Readiness Audit",
    inputs: ["PDS4 labels", "file scan"],
    output: "CPR/DOP status",
    formula: "present terms vs required products",
    note: "Finds four linear polarizations and phase metadata, but no exact CPR/DOP/Stokes/coherency/covariance products in the current extracted package.",
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
    title: "OHRC Hazard Proxy",
    inputs: ["browse", "geometry"],
    output: "inspection candidates",
    formula: "contrast + gradient + content mask",
    note: "Moves OHRC beyond context by marking crater/boulder candidate zones while keeping full-resolution registered hazard certification pending.",
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
    payload: "MENTOR",
    product: "PS 8 Lunal Ice.docx",
    date: "2026-06-19",
    role: "Mentor/judge details extracted from embedded slides: Faustini/F2 target, lobate-rim cue, CPR/DOP thresholds, expected outputs, and mission-planner framing.",
    status: "mapped",
  },
  {
    payload: "DFSAR",
    product: "ch2_sar_ncls_20200913t042439405_d_fp_d18.zip",
    date: "2020-09-13",
    role: "Radar evidence source for candidate subsurface-ice indicators.",
    status: "processed",
  },
  {
    payload: "DFSAR",
    product: "ch2_sar_nrxl_20251024t075159312/094954820/114751370_d_fp_d32.zip",
    date: "2025-10-24",
    role: "Three newly downloaded raw L-band full-pol D32 products; labels confirm HH/HV/VH/VV and are staged for future MIDAS/CPR-DOP processing.",
    status: "metadata extracted",
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
    product: "ch2_ohr_ncp_20260103T0410224157_d_img_d18.zip",
    date: "2026-01-03",
    role: "Additional high-resolution optical strip; geometry audited and browse-scale hazard candidates extracted.",
    status: "audited",
  },
  {
    payload: "OHRC",
    product: "ch2_ohr_ncp_20260103T0609041371_d_img_d18.zip",
    date: "2026-01-03",
    role: "High-resolution optical strip; geometry audited and browse-scale hazard candidates extracted.",
    status: "audited",
  },
  {
    payload: "OHRC",
    product: "ch2_ohr_ncp_20260103T1005176450_d_img_d18.zip",
    date: "2026-01-03",
    role: "Second optical strip; geometry audited and browse-scale hazard candidates extracted.",
    status: "audited",
  },
  {
    payload: "OHRC",
    product: "ch2_ohr_ncp_20260103T1203563771_d_img_d18.zip",
    date: "2026-01-03",
    role: "Additional optical strip for expanded hazard-context coverage and footprint audit.",
    status: "audited",
  },
  {
    payload: "NASA LOLA",
    product: "ldem_85s_20m_float.img/lbl/xml",
    date: "2017-06-15",
    role: "PDS LDEM_85S_20M south-pole DEM used as independent topographic validation against TMC-2 slope behavior.",
    status: "processed",
  },
  {
    payload: "DERIVED",
    product: "dfsar_polarimetry_audit_summary + ohrc_registration_hazard_summary",
    date: "2026-06-20",
    role: "Readiness audits for exact CPR/DOP status, OHRC footprint registration, and browse-scale hazard morphology.",
    status: "derived",
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
    payload: "MODEL",
    product: "mission_planning_model_summary.json",
    date: "2026-06-20",
    role: "Generated candidate-site, route, scale, prediction-weight, and missing-input model used to drive the zoomable mission-planning dashboard.",
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
    title: "1. Rubric alignment: what is ready vs pending",
    copy:
      "Open with the compliance matrix. It shows exactly how the prototype maps to the mentor workflow, and it names the biggest remaining gap: exact CPR/DOP on the official crater AOI.",
    layerId: "compliance-matrix",
    view: "focus",
  },
  {
    title: "2. Mission problem: hidden ice to exploration plan",
    copy:
      "Start here: this is not just a map. The judge story is detection, safety, traverse, volume, and scientific honesty.",
    layerId: "mentor-solution",
    view: "focus",
  },
  {
    title: "3. Target framing: Faustini-class DSC proxy",
    copy:
      "DSC-1 is the working doubly shadowed crater proxy. We present it as a Faustini/F2-style target until the official supplied crater AOI replaces the proxy geometry.",
    layerId: "dsc-target",
    view: "focus",
  },
  {
    title: "4. DFSAR candidate evidence",
    copy:
      "Radar-bright and polarimetrically interesting zones are ranked as candidate volatile targets. This is evidence screening, not confirmed ice.",
    layerId: "sar-score",
    view: "focus",
  },
  {
    title: "5. CPR/DOP gate: the critical scientific caveat",
    copy:
      "The required final criterion is CPR > 1 and DOP < 0.13. Current files support a readiness/proxy gate; exact CPR/DOP awaits calibrated phase/coherency processing.",
    layerId: "cpr-dop-gate",
    view: "focus",
  },
  {
    title: "6. Experimental CPR/DOP-style screening",
    copy:
      "This is our best current gap-closure layer: CPR-like and DOP-like proxies from HH/HV/VH/VV-derived SAR layers. It gives a visible threshold mask but remains explicitly non-final.",
    layerId: "experimental-cpr-dop",
    view: "focus",
  },
  {
    title: "7. Validation gates: exact products and official AOI",
    copy:
      "This is the current hard-gate audit: raw full-pol DFSAR is staged, exact CPR/DOP products are still absent, the official crater AOI has not replaced the proxy, and OHRC registration is ready to intersect once that AOI arrives.",
    layerId: "validation-gates",
    view: "focus",
  },
  {
    title: "8. Reject rocky radar false positives",
    copy:
      "Radar brightness alone can be rough rock. This layer rejects steep, low-access, SAR/cold-inconsistent terrain before ranking science targets.",
    layerId: "rough-filter",
    view: "focus",
  },
  {
    title: "9. Landing safety from TMC-2 terrain",
    copy:
      "A promising crater still needs a feasible landing zone. TMC-2 slope and relief produce the accessibility screen for LZ-A style landing choices.",
    layerId: "tmc-access",
    view: "focus",
  },
  {
    title: "10. Cold-trap and solar plausibility",
    copy:
      "Low-sun terrain simulations identify cold-trap-like zones while also reminding judges that ephemeris-grade illumination validation is still required.",
    layerId: "cold-trap",
    view: "focus",
  },
  {
    title: "11. A* rover traverse",
    copy:
      "The route is computed over accessibility, science interest, and low-illumination solar penalty. This connects the safe landing zone to the candidate science target.",
    layerId: "traverse-route",
    view: "focus",
  },
  {
    title: "12. Top 5 m ice-volume scenario",
    copy:
      "This satisfies the expected volume outcome: area times 5 m depth times assumed ice fraction, reported as scenarios rather than a confirmed reserve.",
    layerId: "ice-volume",
    view: "focus",
  },
  {
    title: "13. Independent terrain validation",
    copy:
      "NASA LOLA provides external topographic validation. The TMC-2 and LOLA overlap slopes agree closely enough to support the route as a defensible screening output.",
    layerId: "lola-validation",
    view: "focus",
  },
  {
    title: "14. OHRC hazard readiness and recommendation",
    copy:
      "OHRC now contributes browse-scale crater/boulder hazard candidates. Close with the recommendation: prioritize SCI-B through LZ-A, then confirm with exact CPR/DOP and official AOI registration.",
    layerId: "ohr-hazards",
    view: "focus",
  },
];

const layerAnalytics = {
  "compliance-matrix": {
    planTitle: "Problem 8 Readiness Audit",
    planSubtitle: "mentor outcome compliance",
    confidence: 74,
    confidenceLabel: "overall readiness",
    confidenceSubtitle: "prototype + gaps",
    confidenceCopy:
      "This is the honest judge-facing status: terrain, traverse, LOLA validation, and scenario volume are strong; exact calibrated CPR/DOP on the official crater AOI is the major remaining scientific gap.",
    profileSubtitle: "requirement scores",
    profile: [78, 45, 68, 86, 82, 72],
    planMetrics: [
      ["Ready/strong", "2"],
      ["Proxy/scenario", "2"],
      ["Partial", "1"],
      ["Major gap", "1"],
    ],
    candidates: [
      ["Terrain + LOLA", "0.86", "0.12", "0.18", "Ready", "good"],
      ["A* traverse", "0.82", "0.18", "0.27", "Ready", "good"],
      ["CPR/DOP exact", "0.45", "0.55", "0.63", "Close", "warn"],
    ],
    pipeline: ["mentor criteria", "evidence layer", "status", "gap closure", "final pitch"],
  },
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
  "mentor-solution": {
    planTitle: "Mentor Requirements Coverage",
    planSubtitle: "PS 8 solution tracker",
    confidence: 86,
    confidenceLabel: "coverage score",
    confidenceSubtitle: "demo alignment",
    confidenceCopy:
      "The mentor DOCX asks for a mission-planning answer, not just a map. This layer tracks the exact expected steps: PSR/DSC mapping, CPR/DOP logic, OHRC morphology, safe landing, solar-aware traverse, and top-5m volume.",
    profileSubtitle: "expected output coverage",
    profile: [74, 80, 66, 88, 82, 79, 86, 72, 84, 90],
    planMetrics: [
      ["Expected steps", "6 / 6 mapped"],
      ["Ready outputs", "3"],
      ["Audited/proxy", "3"],
      ["Judge framing", "mission planner"],
    ],
    candidates: [
      ["Radar framework", "0.80", "0.18", "0.28", "Audited", "good"],
      ["Landing + route", "0.81", "0.22", "0.34", "Ready", "good"],
      ["OHRC morphology", "0.73", "0.31", "0.42", "Partial", "warn"],
    ],
    pipeline: ["mentor DOCX", "requirements", "prototype layer", "honesty status", "judge story"],
  },
  "faustini-reference": {
    planTitle: "Faustini/F2 Reference Alignment",
    planSubtitle: "official target model",
    confidence: 83,
    confidenceLabel: "framing score",
    confidenceSubtitle: "reference aligned",
    confidenceCopy:
      "The mentor material anchors the science case on a Faustini PSR F2-style crater: roughly 1.1 km diameter, doubly shadowed, lobate-rim morphology, high CPR, and low DOP. DSC-1 is framed as a proxy against that target model.",
    profileSubtitle: "reference cues covered",
    profile: [88, 78, 83, 72, 91, 86, 70, 64, 79, 84],
    planMetrics: [
      ["Reference crater", "~1.1 km"],
      ["Region", "Faustini PSR"],
      ["Morphology cue", "lobate rim"],
      ["Current AOI", "proxy"],
    ],
    candidates: [
      ["F2 reference", "0.83", "0.19", "0.33", "Model", "good"],
      ["DSC-1 proxy", "0.84", "0.24", "0.39", "Map", "good"],
      ["Official AOI", "0.00", "0.00", "1.00", "Needed", "warn"],
    ],
    pipeline: ["Faustini PSR", "F2 crater cue", "lobate rim", "CPR/DOP reference", "DSC-1 proxy"],
  },
  "radar-reference": {
    planTitle: "CPR/DOP Gap Closure",
    planSubtitle: "reference vs current package",
    confidence: 80,
    confidenceLabel: "radar readiness",
    confidenceSubtitle: "honest proxy",
    confidenceCopy:
      "This layer makes the key scientific gap transparent: the mentor target is exact CPR > 1 and DOP < 0.13; the current downloaded package contains linear-polarization intensity rasters and phase metadata, but not exact CPR/DOP products.",
    profileSubtitle: "radar requirement readiness",
    profile: [100, 100, 82, 70, 55, 42, 26, 18, 0, 0],
    planMetrics: [
      ["Required CPR", "> 1"],
      ["Required DOP", "< 0.13"],
      ["Linear pols", "4 present"],
      ["Exact product", "pending"],
    ],
    candidates: [
      ["Reference gate", "1.00", "0.13", "0.20", "Target", "good"],
      ["Current proxy", "0.72", "0.28", "0.42", "Use", "warn"],
      ["MIDAS/CPR file", "0.00", "0.00", "1.00", "Needed", "warn"],
    ],
    pipeline: ["mentor threshold", "DFSAR audit", "proxy screen", "scientific caveat", "upgrade path"],
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
      ["Proxy pass pixels", "19.41%"],
      ["Status", "pending exact"],
    ],
    candidates: [
      ["CPR/DOP proxy", "0.72", "0.28", "0.42", "Gate", "warn"],
      ["SCI-B", "0.82", "0.21", "0.34", "Candidate", "good"],
      ["DSC-1", "0.84", "0.24", "0.39", "Target", "good"],
    ],
    pipeline: ["HH/HV/VH/VV", "ratio proxy", "CPR > 1 gate", "DOP < 0.13 gate", "candidate"],
  },
  "experimental-cpr-dop": {
    planTitle: "Experimental Radar Prediction Mask",
    planSubtitle: "CPR/DOP-style proxy",
    confidence: 77,
    confidenceLabel: "proxy confidence",
    confidenceSubtitle: "not exact CPR/DOP",
    confidenceCopy:
      "This layer converts available HH/HV/VH/VV-derived products into CPR-like and DOP-like screening rasters. It is the strongest current prediction layer, but final confirmation still needs calibrated CPR/DOP on the official crater AOI.",
    profileSubtitle: "proxy threshold bins",
    profile: [19, 34, 46, 63, 71, 68, 55, 42, 28, 16],
    planMetrics: [
      ["Pass pixels", "19.41%"],
      ["Mean CPR-like", "1.16"],
      ["Mean DOP-like", "0.067"],
      ["Claim", "experimental"],
    ],
    candidates: [
      ["SCI-B", "1.16", "0.067", "0.34", "Predict", "good"],
      ["RIM-C", "1.04", "0.118", "0.61", "Review", "warn"],
      ["LZ-A", "0.72", "0.151", "0.18", "Landing", "good"],
    ],
    pipeline: ["HH/HV/VH/VV", "CPR-like proxy", "DOP-like proxy", "threshold mask", "candidate ranking"],
  },
  "validation-gates": {
    planTitle: "Hard Validation Gate Audit",
    planSubtitle: "exact replacement readiness",
    confidence: 78,
    confidenceLabel: "readiness score",
    confidenceSubtitle: "proxy gates active",
    confidenceCopy:
      "This layer tracks the three remaining hard gates: exact CPR/DOP rasters are not present yet, the official supplied crater AOI has not replaced the proxy harness, and OHRC registration is ready at footprint level but not final hazard certification.",
    profileSubtitle: "gate readiness",
    profile: [100, 100, 78, 64, 44, 0, 100, 100, 72, 38],
    planMetrics: [
      ["Raw D32 packages", "3"],
      ["Phase metadata", "28 values"],
      ["Official AOI", "not supplied"],
      ["OHRC overlap", "proxy-ready"],
    ],
    candidates: [
      ["Exact CPR/DOP", "0.78", "0.00", "1.00", "Pending", "warn"],
      ["Official AOI", "0.00", "0.00", "1.00", "Needed", "warn"],
      ["OHRC footprint", "1.00", "0.20", "0.32", "Ready", "good"],
    ],
    pipeline: ["raw D32 scan", "exact file check", "AOI gate", "OHRC overlap", "replace proxy"],
  },
  "dfsar-audit": {
    planTitle: "DFSAR Polarimetry Readiness",
    planSubtitle: "metadata audit",
    confidence: 76,
    confidenceLabel: "audit confidence",
    confidenceSubtitle: "exact products missing",
    confidenceCopy:
      "The downloaded DFSAR set is stronger now: the processed 2020 product provides calibrated HH/HV/VH/VV evidence and the three new 2025 D32 files are raw L-band full-pol candidates. Exact CPR/DOP still needs calibration or official MIDAS-style outputs.",
    profileSubtitle: "product readiness",
    profile: [100, 100, 100, 100, 64, 38, 0, 0, 0, 0],
    planMetrics: [
      ["Polarizations", "4"],
      ["Phase terms", "16"],
      ["Raw D32 full-pol", "3"],
      ["Exact CPR/DOP files", "0"],
    ],
    candidates: [
      ["HH/HV/VH/VV", "1.00", "0.00", "0.10", "Present", "good"],
      ["phase metadata", "0.76", "0.00", "0.20", "Present", "good"],
      ["CPR/DOP product", "0.00", "0.00", "1.00", "Pending", "warn"],
    ],
    pipeline: ["PDS4 labels", "polarization scan", "phase audit", "missing products", "honest gate"],
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
  "ohr-footprint": {
    planTitle: "OHRC Footprint Registration Audit",
    planSubtitle: "geometry-ready",
    confidence: 71,
    confidenceLabel: "registration readiness",
    confidenceSubtitle: "regional overlap",
    confidenceCopy:
      "Four OHRC geometry CSVs contain per-pixel selenographic coordinates and overlap the TMC-2 south-pole latitude span. Exact crater-AOI registration still needs map-projected footprint intersection against the official supplied crater.",
    profileSubtitle: "footprint readiness",
    profile: [82, 86, 88, 91, 72, 54, 38, 31, 24, 18],
    planMetrics: [
      ["OHRC strips", "4"],
      ["Geometry records", "489,808"],
      ["Latitude overlap", "yes"],
      ["AOI status", "pending"],
    ],
    candidates: [
      ["OHRC-0", "0.72", "0.18", "0.41", "Register", "warn"],
      ["OHRC-A", "0.71", "0.18", "0.41", "Register", "warn"],
      ["OHRC-B", "0.70", "0.18", "0.42", "Register", "warn"],
      ["OHRC-C", "0.72", "0.18", "0.42", "Register", "warn"],
    ],
    pipeline: ["geometry CSV", "lat/lon bounds", "TMC span", "regional overlap", "AOI pending"],
  },
  "ohr-hazards": {
    planTitle: "OHRC Hazard Candidate Extraction",
    planSubtitle: "browse-scale morphology",
    confidence: 73,
    confidenceLabel: "hazard proxy",
    confidenceSubtitle: "needs full-res AOI",
    confidenceCopy:
      "Contrast and gradient ranking marks crater/boulder candidate zones on the OHRC browse strips. It is a useful inspection layer, but final landing-hazard certification needs full-resolution registered OHRC footprints.",
    profileSubtitle: "candidate clusters",
    profile: [58, 66, 74, 82, 77, 64, 71, 69, 55, 48],
    planMetrics: [
      ["OHRC-0 hazards", "12"],
      ["OHRC-A hazards", "12"],
      ["OHRC-B hazards", "11"],
      ["OHRC-C hazards", "11"],
    ],
    candidates: [
      ["OHRC-0 strip", "0.74", "0.27", "0.39", "Inspect", "good"],
      ["OHRC-A strip", "0.73", "0.28", "0.39", "Inspect", "good"],
      ["OHRC-B strip", "0.71", "0.31", "0.42", "Inspect", "good"],
      ["OHRC-C strip", "0.72", "0.29", "0.41", "Inspect", "good"],
    ],
    pipeline: ["OHRC browse", "content crop", "contrast/gradient", "candidate marks", "hazard proxy"],
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
    planTitle: "Generated Rover Traverse Planner",
    planSubtitle: "A* route output",
    confidence: 81,
    confidenceLabel: "route confidence",
    confidenceSubtitle: "screening route",
    confidenceCopy:
      "The route is generated with A* over accessibility, cold-trap, and low-illumination penalty rasters inside one connected valid-data island. It is a planning screen, not rover-qualified navigation.",
    profileSubtitle: "solar-aware path cost",
    profile: [21, 25, 34, 47, 56, 62, 58, 44, 31, 24],
    planMetrics: [
      ["Planner", "A* generated"],
      ["Inputs", "terrain + solar + hazard"],
      ["Route options", "3 strategies"],
      ["Updates", "target/landing changes"],
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
    confidence: 91,
    confidenceLabel: "validation confidence",
    confidenceSubtitle: "strong sanity check",
    confidenceCopy:
      "NASA PDS LRO/LOLA LDEM_85S_20M was cropped to the TMC-2 overlap and converted into elevation, slope, and roughness quicklooks. Mean slope agrees within 0.63 degrees, supporting the terrain pipeline as a credible screening layer.",
    profileSubtitle: "LOLA/TMC agreement",
    profile: [82, 86, 91, 88, 84, 90, 87, 85, 89, 92],
    planMetrics: [
      ["TMC slope mean", "9.87 deg"],
      ["LOLA slope mean", "10.50 deg"],
      ["Mean delta", "0.63 deg"],
      ["Agreement", "strong"],
    ],
    candidates: [
      ["TMC AOI", "0.88", "0.11", "0.20", "Validated", "good"],
      ["LOLA slope", "0.91", "0.10", "0.18", "Reference", "good"],
      ["LOLA roughness", "0.78", "0.24", "0.34", "Context", "good"],
    ],
    pipeline: ["PDS LDEM", "AOI crop", "slope derive", "roughness", "validation"],
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
      ["Validation", "ephemeris pending"],
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
const productLayerList = document.querySelector("#productLayerList");
const mapFrame = document.querySelector("#mapFrame");
const mapCanvas = document.querySelector("#mapCanvas");
const image = document.querySelector("#mainLayer");
const routeOverlay = document.querySelector("#routeOverlay");
const candidateOverlay = document.querySelector("#candidateOverlay");
const zoomIn = document.querySelector("#zoomIn");
const zoomOut = document.querySelector("#zoomOut");
const resetView = document.querySelector("#resetView");
const zoomLabel = document.querySelector("#zoomLabel");
const scaleLabel = document.querySelector("#scaleLabel");
const viewportReadout = document.querySelector("#viewportReadout");
const description = document.querySelector("#layerDescription");
const score = document.querySelector("#scoreValue");
const title = document.querySelector("#layerTitle");
const viewButtons = document.querySelectorAll(".tool-button[data-view]");
const openFullLayer = document.querySelector("#openFullLayer");
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
const candidateButtons = document.querySelector("#candidateButtons");
const routeButtons = document.querySelector("#routeButtons");
const plannerMetrics = document.querySelector("#plannerMetrics");
const plannerNarrative = document.querySelector("#plannerNarrative");
const pageTabs = document.querySelectorAll(".page-tab");
const detailPages = document.querySelectorAll(".detail-page");

let selectedLayer = layers[0];
let viewMode = "focus";
let demoIndex = -1;
let activeDetailPage = "mission";
let selectedCandidateId = "SCI-B";
let selectedRouteId = "route-a";
let viewport = { scale: 1, x: 0, y: 0 };
let canvasFit = { width: 1, height: 1, availableWidth: 1, availableHeight: 1, baseX: 18, baseY: 18, mode: "fit" };
let dragging = false;
let dragStart = { x: 0, y: 0, viewportX: 0, viewportY: 0 };

function saveDemoState() {
  const state = JSON.stringify({
    demoIndex,
    layerId: selectedLayer.id,
    viewMode,
    detailPage: activeDetailPage,
    selectedCandidateId,
    selectedRouteId,
  });
  try {
    localStorage.setItem(demoStateKey, state);
    sessionStorage.setItem(demoStateKey, state);
  } catch {
    // Storage can be unavailable in some embedded/browser privacy modes.
  }
}

function readDemoState() {
  try {
    return JSON.parse(localStorage.getItem(demoStateKey) || sessionStorage.getItem(demoStateKey) || "null");
  } catch {
    return null;
  }
}

function requestedPage() {
  const params = new URLSearchParams(window.location.search);
  const page = params.get("page");
  return ["mission", "requirements", "details", "walkthrough"].includes(page) ? page : null;
}

function requestedLayer() {
  const params = new URLSearchParams(window.location.search);
  const layer = params.get("layer");
  return layer && layers.some((item) => item.id === layer) ? layer : null;
}

function currentImagePath(layer) {
  if (productLayerIdSet.has(layer.id)) return viewMode === "raw" ? layer.rawPath : layer.focusPath;
  if (viewMode === "fusion") return fusionPath;
  if (viewMode === "raw") return layer.rawPath;
  return layer.focusPath;
}

function versioned(path) {
  return `${path}?v=${assetVersion}`;
}

function layerScaleInfo(layer = selectedLayer) {
  return layerScale[layer.id] || layerScale.default;
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function clampViewport() {
  const scaledWidth = canvasFit.width * viewport.scale;
  const scaledHeight = canvasFit.height * viewport.scale;
  const minX = scaledWidth > canvasFit.availableWidth ? canvasFit.availableWidth - scaledWidth : 0;
  const minY = scaledHeight > canvasFit.availableHeight ? canvasFit.availableHeight - scaledHeight : 0;
  viewport.x = scaledWidth > canvasFit.availableWidth ? clamp(viewport.x, minX, 0) : 0;
  viewport.y = scaledHeight > canvasFit.availableHeight ? clamp(viewport.y, minY, 0) : 0;
}

function renderViewport() {
  clampViewport();
  mapCanvas.style.transform = `translate(${canvasFit.baseX + viewport.x}px, ${canvasFit.baseY + viewport.y}px) scale(${viewport.scale})`;
  zoomLabel.textContent = `${viewport.scale.toFixed(1)}x`;
  const scale = layerScaleInfo();
  const visibleKm = scale.labelKm / viewport.scale;
  scaleLabel.textContent = `${visibleKm >= 1 ? visibleKm.toFixed(visibleKm >= 10 ? 0 : 1) : (visibleKm * 1000).toFixed(0)} ${visibleKm >= 1 ? "km" : "m"}`;
  viewportReadout.textContent = `${scale.context} | ${scale.pixelScale} | ${canvasFit.mode} | pan ${Math.round(viewport.x)}, ${Math.round(viewport.y)}`;
}

function updateCanvasFit() {
  if (!image.naturalWidth || !image.naturalHeight) return;
  const padding = 36;
  const availableWidth = Math.max(1, mapFrame.clientWidth - padding);
  const availableHeight = Math.max(1, mapFrame.clientHeight - padding);
  const frameRatio = availableWidth / availableHeight;
  const imageRatio = image.naturalWidth / image.naturalHeight;
  const tallSourceProduct = productLayerIdSet.has(selectedLayer.id) && image.naturalHeight > image.naturalWidth * 1.8;
  const width = tallSourceProduct ? availableWidth : imageRatio > frameRatio ? availableWidth : availableHeight * imageRatio;
  const height = tallSourceProduct ? availableWidth / imageRatio : imageRatio > frameRatio ? availableWidth / imageRatio : availableHeight;
  const baseX = tallSourceProduct ? 18 : 18 + (availableWidth - width) / 2;
  const baseY = tallSourceProduct ? 18 : 18 + (availableHeight - height) / 2;
  canvasFit = { width, height, availableWidth, availableHeight, baseX, baseY, mode: tallSourceProduct ? "fit-width raster" : "fit-frame raster" };
  mapCanvas.style.width = `${width}px`;
  mapCanvas.style.height = `${height}px`;
  renderViewport();
}

function resetViewport() {
  viewport = { scale: 1, x: 0, y: 0 };
  renderViewport();
}

function zoomViewport(multiplier, clientX = null, clientY = null) {
  const nextScale = Math.max(1, Math.min(12, viewport.scale * multiplier));
  if (nextScale === viewport.scale) return;
  const rect = mapFrame.getBoundingClientRect();
  const pointerX = (clientX ?? rect.left + rect.width / 2) - rect.left - canvasFit.baseX;
  const pointerY = (clientY ?? rect.top + rect.height / 2) - rect.top - canvasFit.baseY;
  const imageX = (pointerX - viewport.x) / viewport.scale;
  const imageY = (pointerY - viewport.y) / viewport.scale;
  viewport.scale = nextScale;
  viewport.x = pointerX - imageX * nextScale;
  viewport.y = pointerY - imageY * nextScale;
  renderViewport();
}

function markerLayersFor(layer) {
  return layer.id === "traverse-route" && viewMode !== "fusion" ? [...landingSites, ...candidateSites] : [];
}

function routeOverlayAllowed(layer) {
  return layer.id === "traverse-route" && viewMode !== "fusion";
}

function selectedCandidate() {
  return candidateSites.find((site) => site.id === selectedCandidateId) || candidateSites[0];
}

function selectedRoute() {
  return generatedRoutes.find((route) => route.id === selectedRouteId) || generatedRoutes[0] || generateRoute(routeStrategies[0], selectedCandidate());
}

function markerIsActive(marker) {
  return marker.id === selectedCandidateId || marker.id === selectedRoute().landingId;
}

function gaussian(x, y, cx, cy, spread) {
  const dx = x - cx;
  const dy = y - cy;
  return Math.exp(-(dx * dx + dy * dy) / (2 * spread * spread));
}

function clamp01(value) {
  return Math.max(0, Math.min(1, value));
}

function syntheticTerrainCost(x, y) {
  const ridgeRisk = gaussian(x, y, 46, 54, 10) * 0.55;
  const craterRisk = gaussian(x, y, 37, 58, 7) * 0.7 + gaussian(x, y, 59, 68, 6) * 0.48;
  const rimRelief = Math.abs(Math.sin((x + y) * 0.12)) * 0.18;
  return clamp01(0.18 + ridgeRisk + craterRisk + rimRelief);
}

function syntheticSolarPenalty(x, y) {
  const shadowBasin = gaussian(x, y, 52, 71, 13) * 0.62;
  const southDarkening = Math.max(0, y - 54) / 70;
  const ridgeLight = gaussian(x, y, 34, 31, 10) * 0.28;
  return clamp01(0.2 + shadowBasin + southDarkening - ridgeLight);
}

function syntheticHazardCost(x, y) {
  return clamp01(
    gaussian(x, y, 39, 58, 6) * 0.72 +
      gaussian(x, y, 58, 73, 5) * 0.55 +
      gaussian(x, y, 65, 42, 8) * 0.44 +
      0.12,
  );
}

function routeCellCost(x, y, strategy, target) {
  const terrain = syntheticTerrainCost(x, y);
  const solar = syntheticSolarPenalty(x, y);
  const hazard = syntheticHazardCost(x, y);
  const targetPull = Math.hypot(x - target.x, y - target.y) / 100;
  return (
    1 +
    terrain * strategy.weights.terrain * 7 +
    solar * strategy.weights.solar * 6 +
    hazard * strategy.weights.hazard * 8 +
    targetPull * strategy.weights.directness * 4
  );
}

function toGrid(point, size) {
  return {
    x: Math.max(0, Math.min(size - 1, Math.round((point.x / 100) * (size - 1)))),
    y: Math.max(0, Math.min(size - 1, Math.round((point.y / 100) * (size - 1)))),
  };
}

function toPercent(point, size) {
  return [(point.x / (size - 1)) * 100, (point.y / (size - 1)) * 100];
}

function gridKey(x, y) {
  return `${x},${y}`;
}

function simplifyPath(points) {
  if (points.length <= 14) return points;
  const step = Math.ceil(points.length / 14);
  const simplified = points.filter((_, index) => index % step === 0);
  const last = points[points.length - 1];
  if (simplified[simplified.length - 1] !== last) simplified.push(last);
  return simplified;
}

function generateRoute(strategy, target = selectedCandidate()) {
  const size = 52;
  const landing = landingSites.find((site) => site.id === strategy.landingId) || landingSites[0];
  const start = toGrid(landing, size);
  const goal = toGrid(target, size);
  const startKey = gridKey(start.x, start.y);
  const goalKey = gridKey(goal.x, goal.y);
  const open = [{ ...start, key: startKey, f: 0 }];
  const cameFrom = new Map();
  const gScore = new Map([[startKey, 0]]);
  const closed = new Set();
  const directions = [
    [1, 0, 1],
    [-1, 0, 1],
    [0, 1, 1],
    [0, -1, 1],
    [1, 1, 1.414],
    [-1, 1, 1.414],
    [1, -1, 1.414],
    [-1, -1, 1.414],
  ];

  while (open.length) {
    open.sort((a, b) => a.f - b.f);
    const current = open.shift();
    if (!current || closed.has(current.key)) continue;
    if (current.key === goalKey) break;
    closed.add(current.key);

    for (const [dx, dy, distance] of directions) {
      const nx = current.x + dx;
      const ny = current.y + dy;
      if (nx < 0 || ny < 0 || nx >= size || ny >= size) continue;
      const key = gridKey(nx, ny);
      if (closed.has(key)) continue;
      const [px, py] = toPercent({ x: nx, y: ny }, size);
      const tentative = (gScore.get(current.key) || 0) + routeCellCost(px, py, strategy, target) * distance;
      if (tentative >= (gScore.get(key) ?? Infinity)) continue;
      cameFrom.set(key, current.key);
      gScore.set(key, tentative);
      const heuristic = Math.hypot(nx - goal.x, ny - goal.y);
      open.push({ x: nx, y: ny, key, f: tentative + heuristic });
    }
  }

  const path = [];
  let key = goalKey;
  if (!cameFrom.has(key)) {
    path.push([landing.x, landing.y], [target.x, target.y]);
  } else {
    while (key) {
      const [x, y] = key.split(",").map(Number);
      path.push(toPercent({ x, y }, size));
      if (key === startKey) break;
      key = cameFrom.get(key);
    }
    path.reverse();
  }

  const points = simplifyPath(path);
  const samples = points.map(([x, y]) => ({
    terrain: syntheticTerrainCost(x, y),
    solar: 1 - syntheticSolarPenalty(x, y),
    hazard: syntheticHazardCost(x, y),
  }));
  const average = (field) => samples.reduce((sum, sample) => sum + sample[field], 0) / samples.length;
  const distanceKm =
    points.reduce((sum, point, index) => {
      if (index === 0) return 0;
      const previous = points[index - 1];
      return sum + Math.hypot(point[0] - previous[0], point[1] - previous[1]) * 0.42;
    }, 0) || Math.hypot(landing.x - target.x, landing.y - target.y) * 0.42;
  const terrainRisk = average("terrain");
  const hazardRisk = average("hazard");
  const solarExposure = average("solar");

  return {
    ...strategy,
    targetId: target.id,
    points,
    distanceKm,
    cost: clamp01(0.18 + terrainRisk * 0.32 + hazardRisk * 0.28 + (1 - solarExposure) * 0.22 + distanceKm / 120),
    solarExposure,
    hazardRisk,
    terrainRisk,
  };
}

function recomputeRoutes() {
  const target = selectedCandidate();
  generatedRoutes = routeStrategies.map((strategy) => generateRoute(strategy, target));
}

function routePointString(route) {
  return route.points.map(([x, y]) => `${x.toFixed(2)},${y.toFixed(2)}`).join(" ");
}

function renderRouteOverlay(layer) {
  if (!routeOverlayAllowed(layer)) {
    routeOverlay.innerHTML = "";
    return;
  }

  routeOverlay.innerHTML = generatedRoutes
    .map(
      (route) => `
        <polyline
          class="route-line ${route.id === selectedRouteId ? "active" : ""}"
          points="${routePointString(route)}"
          vector-effect="non-scaling-stroke"
        />
      `,
    )
    .join("");
}

function renderMarkers(layer) {
  const markers = markerLayersFor(layer);
  candidateOverlay.innerHTML = markers
    .map(
      (marker) => `
        <button class="candidate-marker ${marker.type} ${markerIsActive(marker) ? "active" : ""}" data-marker-id="${marker.id}" type="button" style="left:${marker.x}%; top:${marker.y}%">
          <strong>${marker.id}</strong>
          <span>${marker.label}</span>
        </button>
      `,
    )
    .join("");

  candidateOverlay.querySelectorAll(".candidate-marker").forEach((markerButton) => {
    markerButton.addEventListener("pointerdown", (event) => event.stopPropagation());
    markerButton.addEventListener("click", (event) => {
      event.stopPropagation();
      const markerId = markerButton.dataset.markerId;
      if (candidateSites.some((site) => site.id === markerId)) {
        selectedCandidateId = markerId;
      }
      if (landingSites.some((site) => site.id === markerId)) {
        const routeForLanding = generatedRoutes.find((route) => route.landingId === markerId);
        if (routeForLanding) selectedRouteId = routeForLanding.id;
      }
      renderPlanner();
      renderMarkers(selectedLayer);
      renderRouteOverlay(selectedLayer);
      saveDemoState();
    });
  });
}

function productAnalytics(layer) {
  const isSouthPole = layer.id.includes("202312") || layer.id.startsWith("ohr") || layer.id === "sar-browse";
  const isOhrc = layer.id.startsWith("ohr-");
  const isTmc = layer.id.startsWith("tmc2-") || layer.id === "tmc-elevation" || layer.id === "tmc-ortho";
  const isSar = layer.id === "sar-browse";
  const role = isSar ? "radar scene QA" : isOhrc ? "optical hazard inspection" : "terrain context QA";
  const confidence = isSouthPole ? Math.max(58, Math.min(78, layer.score)) : 42;
  const pipeline = isSar
    ? ["DFSAR browse", "scene inspect", "compare SAR score", "CPR/DOP caveat", "science QA"]
    : isOhrc
      ? ["OHRC browse", "zoom inspect", "crater/boulder cues", "footprint pending", "hazard QA"]
      : ["TMC-2 browse", "terrain inspect", "DTM/ortho compare", "slope context", "route QA"];

  return {
    planTitle: layer.name,
    planSubtitle: role,
    confidence,
    confidenceLabel: "source utility",
    confidenceSubtitle: isSouthPole ? "usable evidence context" : "test strip only",
    confidenceCopy: `${layer.name} is an actual downloaded source product. Use zoom/pan to inspect texture, craters, shadows, terrain continuity, and visual plausibility before trusting derived model layers. ${isSouthPole ? "It supports the south-pole mission story, but still needs exact AOI/coregistration for final certification." : "It is retained as a non-polar regression strip and should not drive the final recommendation."}`,
    profileSubtitle: isOhrc ? "visual hazard cues" : isSar ? "radar browse bins" : "terrain browse bins",
    profile: isOhrc ? [52, 61, 74, 68, 57, 63, 71, 59, 66, 73] : isSar ? [31, 42, 58, 76, 69, 54, 43, 61, 72, 64] : [44, 53, 66, 72, 61, 47, 58, 69, 75, 63],
    planMetrics: [
      ["Product role", role],
      ["Image size", sourceProductDimensions[layer.id] || "source browse"],
      ["Source file", layer.source],
      ["Inspection", "zoom/pan"],
      ["Use level", isSouthPole ? "mission evidence" : "regression only"],
    ],
    candidates: [
      ["Visual QA", "1.00", "0.00", "0.00", "Inspect", "good"],
      ["Model link", isSouthPole ? "0.72" : "0.20", "0.18", "0.32", isSouthPole ? "Use" : "Do not use", isSouthPole ? "good" : "warn"],
      ["Certification", "0.00", "0.00", "1.00", "Needs AOI", "warn"],
    ],
    pipeline,
  };
}

function renderAnalytics(layer) {
  const analytics = layerAnalytics[layer.id] || productAnalytics(layer);
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

function formatPercent(value) {
  return `${Math.round(value * 100)}%`;
}

function renderPlanner() {
  recomputeRoutes();
  const candidate = selectedCandidate();
  const route = selectedRoute();
  const landing = landingSites.find((site) => site.id === route.landingId) || landingSites[0];

  candidateButtons.innerHTML = candidateSites
    .map(
      (site) => `
        <button type="button" class="${site.id === selectedCandidateId ? "active" : ""}" data-candidate-id="${site.id}">
          <b>${site.id}</b>
          <span>${formatPercent(site.iceProbability)} ice-likelihood</span>
        </button>
      `,
    )
    .join("");

  routeButtons.innerHTML = generatedRoutes
    .map(
      (option) => `
        <button type="button" class="${option.id === selectedRouteId ? "active" : ""}" data-route-id="${option.id}">
          <b>${option.name}</b>
          <span>${option.distanceKm.toFixed(1)} km | cost ${option.cost.toFixed(2)}</span>
        </button>
      `,
    )
    .join("");

  plannerMetrics.innerHTML = [
    ["Planner", "A* generated"],
    ["Selected target", candidate.id],
    ["Ice likelihood", formatPercent(candidate.iceProbability)],
    ["Radar evidence", formatPercent(candidate.radarEvidence)],
    ["Cold-trap score", formatPercent(candidate.coldTrap)],
    ["OHRC hazard risk", formatPercent(candidate.ohrcHazard)],
    ["Top 0-5 m volume", candidate.volumeRange],
    ["Landing option", landing.id],
    ["Traverse", `${route.distanceKm.toFixed(1)} km, cost ${route.cost.toFixed(2)}`],
    ["Path vertices", `${route.points.length} generated`],
    ["Solar exposure", formatPercent(route.solarExposure)],
    ["Route hazard", formatPercent(route.hazardRisk)],
  ]
    .map(([label, value]) => `<div><dt>${label}</dt><dd>${value}</dd></div>`)
    .join("");

  plannerNarrative.textContent = `${candidate.narrative} Route ${route.name} is recomputed toward ${candidate.id} from ${landing.id}: ${landing.narrative} Current decision: ${route.decision}.`;

  candidateButtons.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      selectedCandidateId = button.dataset.candidateId;
      renderPlanner();
      renderMarkers(selectedLayer);
      renderRouteOverlay(selectedLayer);
      saveDemoState();
    });
  });

  routeButtons.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      selectedRouteId = button.dataset.routeId;
      renderPlanner();
      renderMarkers(selectedLayer);
      renderRouteOverlay(selectedLayer);
      saveDemoState();
    });
  });
}

function selectLayer(layer) {
  selectedLayer = layer;
  if (productLayerIdSet.has(layer.id) && viewMode === "fusion") {
    viewMode = "focus";
    viewButtons.forEach((button) => {
      button.classList.toggle("active", button.dataset.view === viewMode);
    });
  }
  const selectedImagePath = versioned(currentImagePath(layer));
  image.src = selectedImagePath;
  image.classList.toggle(
    "pixel-layer",
    viewMode === "raw" || productLayerIdSet.has(layer.id),
  );
  const isProduct = productLayerIdSet.has(layer.id);
  image.alt = viewMode === "fusion" && !isProduct ? "Lunar south pole evidence fusion board" : layer.name;
  title.textContent = viewMode === "fusion" && !isProduct ? "Evidence Fusion Board" : layer.name;
  description.textContent = isProduct
    ? `${layer.name}: ${layer.description} Source: ${layer.source}. Inspection mode: fit-width source image. Pan/zoom the photograph; no planner route is overlaid until footprint registration supports it.`
    : `${layer.name}: ${layer.description} Source: ${layer.source}. Planner state: target ${selectedCandidateId}, traverse ${selectedRoute().name}. Click candidate markers or route options to re-plan.`;
  score.textContent = layer.score;
  renderAnalytics(layer);
  renderPlanner();
  renderRouteOverlay(layer);
  renderMarkers(layer);
  if (image.complete && image.naturalWidth) {
    updateCanvasFit();
  }
  resetViewport();

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
  saveDemoState();
}

function layerById(id) {
  return layers.find((layer) => layer.id === id) || layers[0];
}

function isPrimaryLayer(id) {
  return primaryLayerIds.includes(id) || productLayerIds.includes(id);
}

function renderDemoState() {
  const active = demoIndex >= 0;
  judgeDemo.classList.toggle("demo-running", active);
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
  const safeIndex = Number.isFinite(index) ? index : 0;
  demoIndex = Math.max(0, Math.min(safeIndex, demoSteps.length - 1));
  const step = demoSteps[demoIndex];
  viewMode = step.view;
  viewButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.view === viewMode);
  });
  selectLayer(layerById(step.layerId));
  renderDemoState();
  saveDemoState();
}

function setDetailPage(page) {
  activeDetailPage = page;
  pageTabs.forEach((tab) => {
    tab.classList.toggle("active", tab.dataset.pageTarget === page);
  });
  detailPages.forEach((section) => {
    section.classList.toggle("active", section.dataset.page === page);
  });
  const url = new URL(window.location.href);
  url.searchParams.set("page", page);
  window.history.replaceState({}, "", url);
  saveDemoState();
}

const primaryLayers = primaryLayerIds.map(layerById);

primaryLayers.forEach((layer) => {
  const button = document.createElement("button");
  button.className = "layer-btn";
  button.type = "button";
  button.dataset.layerId = layer.id;
  button.innerHTML = `
    <img src="${versioned(layer.thumbnail)}" alt="" />
    <span><strong>${layer.name}</strong><span>${layer.source}</span></span>
    <b>${layer.score}</b>
  `;
  button.addEventListener("click", () => {
    selectLayer(layer);
    saveDemoState();
  });
  list.appendChild(button);
});

const productLayers = productLayerIds.map(layerById);

productLayers.forEach((layer) => {
  const button = document.createElement("button");
  button.className = "layer-btn product-layer-btn";
  button.type = "button";
  button.dataset.layerId = layer.id;
  button.innerHTML = `
    <img src="${versioned(layer.thumbnail)}" alt="" />
    <span><strong>${layer.name}</strong><span>${layer.source}</span></span>
    <b>${layer.score}</b>
  `;
  button.addEventListener("click", () => {
    viewMode = "focus";
    viewButtons.forEach((viewButton) => {
      viewButton.classList.toggle("active", viewButton.dataset.view === viewMode);
    });
    selectLayer(layer);
    saveDemoState();
  });
  productLayerList.appendChild(button);
});

viewButtons.forEach((button) => {
  button.addEventListener("click", () => setViewMode(button.dataset.view));
});

zoomIn.addEventListener("click", () => zoomViewport(1.35));
zoomOut.addEventListener("click", () => zoomViewport(1 / 1.35));
resetView.addEventListener("click", resetViewport);
image.addEventListener("load", () => {
  updateCanvasFit();
  resetViewport();
});
window.addEventListener("resize", updateCanvasFit);

mapFrame.addEventListener(
  "wheel",
  (event) => {
    event.preventDefault();
    zoomViewport(event.deltaY < 0 ? 1.18 : 1 / 1.18, event.clientX, event.clientY);
  },
  { passive: false },
);

mapFrame.addEventListener("dblclick", (event) => {
  zoomViewport(1.8, event.clientX, event.clientY);
});

mapFrame.addEventListener("pointerdown", (event) => {
  dragging = true;
  mapFrame.classList.add("dragging");
  mapFrame.setPointerCapture(event.pointerId);
  dragStart = { x: event.clientX, y: event.clientY, viewportX: viewport.x, viewportY: viewport.y };
});

mapFrame.addEventListener("pointermove", (event) => {
  if (!dragging) return;
  viewport.x = dragStart.viewportX + event.clientX - dragStart.x;
  viewport.y = dragStart.viewportY + event.clientY - dragStart.y;
  renderViewport();
});

function endDrag(event) {
  if (!dragging) return;
  dragging = false;
  mapFrame.classList.remove("dragging");
  if (event.pointerId !== undefined) {
    try {
      mapFrame.releasePointerCapture(event.pointerId);
    } catch {
      // Pointer capture may already be released if the pointer leaves the browser surface.
    }
  }
}

mapFrame.addEventListener("pointerup", endDrag);
mapFrame.addEventListener("pointercancel", endDrag);

demoSteps.forEach((_, index) => {
  const dot = document.createElement("button");
  dot.type = "button";
  dot.setAttribute("aria-label", `Go to demo step ${index + 1}`);
  dot.addEventListener("click", () => goToDemoStep(index));
  demoProgress.appendChild(dot);
});
demoProgress.style.gridTemplateColumns = `repeat(${demoSteps.length}, minmax(0, 1fr))`;

startDemo.addEventListener("click", () => goToDemoStep(0));
prevDemo.addEventListener("click", () => goToDemoStep(demoIndex <= 0 ? 0 : demoIndex - 1));
nextDemo.addEventListener("click", () => goToDemoStep(demoIndex < 0 ? 0 : demoIndex + 1));
openFullLayer.addEventListener("click", () => {
  window.open(versioned(currentImagePath(selectedLayer)), "_blank", "noopener,noreferrer");
});

pageTabs.forEach((tab) => {
  tab.addEventListener("click", () => setDetailPage(tab.dataset.pageTarget));
});

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

const restoredState = readDemoState();
activeDetailPage = requestedPage() || restoredState?.detailPage || "mission";

if (restoredState?.viewMode) {
  viewMode = restoredState.viewMode;
}

if (candidateSites.some((site) => site.id === restoredState?.selectedCandidateId)) {
  selectedCandidateId = restoredState.selectedCandidateId;
}

if (routeStrategies.some((route) => route.id === restoredState?.selectedRouteId)) {
  selectedRouteId = restoredState.selectedRouteId;
}

recomputeRoutes();

const restoredLayer = requestedLayer()
  ? layerById(requestedLayer())
  : restoredState?.layerId && isPrimaryLayer(restoredState.layerId)
    ? layerById(restoredState.layerId)
    : layerById(primaryLayerIds[0]);
selectLayer(restoredLayer);
setDetailPage(activeDetailPage);

if (Number.isInteger(restoredState?.demoIndex) && restoredState.demoIndex >= 0) {
  goToDemoStep(restoredState.demoIndex);
} else {
  renderDemoState();
}
