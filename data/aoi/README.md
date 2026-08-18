# Active crater AOI contract

This folder controls which doubly shadowed crater geometry drives the validation pipeline.

## Current state

- `dsc1_proxy_registration_harness.geojson` is the current proxy AOI used for development.
- `official_crater_aoi_template.geojson` shows the expected GeoJSON shape.
- `official_crater_aoi.geojson` is intentionally absent until the supplied crater AOI is available.

## To switch to the official supplied crater

Place the mentor/ISRO supplied crater boundary at:

```text
data/aoi/official_crater_aoi.geojson
```

Expected format:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "official_supplied_doubly_shadowed_crater"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[lon, lat], [lon, lat], [lon, lat], [lon, lat]]]
      }
    }
  ]
}
```

Coordinates should be lunar longitude/latitude in decimal degrees. When this file exists, the validation scripts automatically prefer it over the proxy harness.
