# USGS ISIS Production-Hardening Path

The current hackathon MVP uses Python/rasterio for speed and local reproducibility. For a production planetary-processing track, USGS ISIS is the right next step for PDS-style ingestion, camera/geometry handling, map projection, and calibration provenance.

## Why This Matters

Judges may ask whether the prototype can grow beyond a web demo. The answer is yes: the analysis products can be routed through a planetary image-processing stack before final map production.

## Proposed ISIS/QGIS Workflow

| Stage | ISIS/QGIS Role | MVP Equivalent |
| --- | --- | --- |
| PDS ingestion | Convert or ingest planetary products into ISIS-compatible cubes where product support exists. | Direct GeoTIFF/PNG extraction from PRADAN ZIPs. |
| Map projection | Use lunar polar stereographic map templates for consistent south-pole projection. | Rasterio reads existing polar stereographic products. |
| Terrain validation | Compare TMC-derived terrain layers against LOLA/SLDEM references. | Current LOLA PGDA validation layer. |
| Hazard mapping | Export projected layers to QGIS for footprint overlays and manual QA. | Current dashboard layer stack and quicklooks. |
| Delivery | Produce COG/GeoTIFF and PDF/PNG map products with full provenance. | Current `data/processed/derived_layers` and `demo_assets`. |

## Command Sketch

Exact ISIS commands depend on the final supported input labels and local ISIS data configuration. A production branch would test:

```bash
# Example structure only; commands must be adjusted per supported product label.
pds2isis from=<pds_product_label> to=<product>.cub
spiceinit from=<product>.cub
cam2map from=<product>.cub to=<product_polar>.cub map=lunar_south_pole.map
isis2std from=<product_polar>.cub to=<product_polar>.tif format=tiff
```

## Current Project Status

USGS ISIS is now treated as a production-hardening path, while NASA LOLA has been integrated as a real external validation source. This is the right balance for the hackathon: demonstrate actual cross-source validation now, and show a credible planetary-processing route for final deployment.
