# Example: Tribal Water Monitoring Integration
## Tribal Data Sovereignty Toolkit

This example shows how `tribal_water_monitoring` uses the toolkit for
sovereignty-compliant water data analysis. It covers the patterns used
in all six analysis notebooks in that series.

## Setup pattern (used in every notebook)

```python
import sys
sys.path.insert(0, "/path/to/tribal-data-sovereignty-toolkit")

from toolkit.sovereignty import SovereigntyContext

ctx = SovereigntyContext.from_config("config/nation.yaml")
ctx.print_acknowledgment(source_keys=[
    "usgs_nwis_streamflow",
    "noaa_pdsi",
    "census_aiannh",
])
```

## Attaching provenance to streamflow data

After loading streamflow data from USGS NWIS:

```python
# flow_df is a DataFrame with columns: site_no, datetime, flow_cfs, station
# Convert to GeoDataFrame using gauge locations
import geopandas as gpd

flow_gdf = gpd.GeoDataFrame(
    flow_df,
    geometry=gpd.points_from_xy(gauge_lons, gauge_lats),
    crs="EPSG:4326"
)

# Attach IEEE 2890-2025 provenance
flow_gdf = ctx.attach_provenance(
    flow_gdf,
    source_key     = "usgs_nwis_streamflow",
    classification = "PUBLIC",
    additional     = {
        "analysis_period": f"{FLOW_START_YEAR}-{FLOW_END_YEAR}",
        "gauge_count":     str(flow_df["site_no"].nunique()),
        "parameter":       "Mean daily discharge (00060)",
    }
)
```

Every exported file now carries its sovereignty metadata in the column
headers, meeting IEEE 2890-2025 requirements.

## Building a project provenance catalog

```python
from toolkit.provenance import ProvenanceBuilder, ProvenanceCatalog

catalog = ProvenanceCatalog("Tribal Water Monitoring for Pine Ridge 2024")

# Streamflow data
catalog.add(
    ProvenanceBuilder("nwis-streamflow-2024")
    .for_nation(ctx)
    .for_dataset("White River Streamflow")
    .from_source("usgs_nwis_streamflow")
    .step("Queried USGS NWIS daily values API for 15 gauges")
    .step("Parsed RDB format, extracted parameter 00060 (discharge)")
    .step("Computed baseflow separation (Lyne-Hollick digital filter)")
    .step("Classified drought stage: Normal/Watch/Emergency")
    .step("Computed annual 7-day minimum flow (7Q)")
    .classify("PUBLIC")
    .note(
        "Gauge coverage on Pine Ridge and Rosebud is sparse "
        "for >18,000 km². Monitoring gaps are a federal infrastructure "
        "equity finding. Tribal-collected well data fills this gap."
    )
    .build()
)

# PDSI drought index
catalog.add(
    ProvenanceBuilder("noaa-pdsi-2024")
    .for_nation(ctx)
    .for_dataset("NOAA PDSI Pine Ridge Climate Divisions 7-8")
    .from_source("noaa_pdsi")
    .step("Downloaded NOAA climdiv-pdsidv file")
    .step("Filtered to SD (state 39), divisions 7 and 8")
    .step("Averaged across both divisions for single Pine Ridge series")
    .step("Classified: Normal/Mild/Moderate/Severe/Extreme drought")
    .classify("PUBLIC")
    .note(
        "PDSI computed from weather stations, many outside reservation. "
        "Station density on Tribal lands is lower than surrounding counties. "
        "Index accuracy is reduced for reservation-specific conditions."
    )
    .build()
)

catalog.save("outputs/provenance_catalog.json")
```

## Sovereignty audit before publication

```python
from toolkit.audit import SovereigntyAudit

audit = SovereigntyAudit("Tribal Water Monitoring Analysis for Pine Ridge 2024")

audit.respond_all({
    "OCAP-O1": ("yes",     "MOU signed with Pine Ridge Natural Resources Dept"),
    "OCAP-O2": ("partial", "MOU covers data sharing; publication rights in progress"),
    "OCAP-C1": ("yes",     "Tribal Council approved watershed monitoring program"),
    "OCAP-C2": ("yes",     ""),
    "OCAP-A1": ("yes",     "Data returned to NRD quarterly"),
    "OCAP-A2": ("partial", "Technical report complete; plain language summary pending"),
    "OCAP-P1": ("yes",     "NRD holds copy on Tribal server"),
    "OCAP-P2": ("yes",     ""),
    "CARE-C1": ("yes",     "Drought early warning system for water managers"),
    "CARE-C2": ("partial", "Water managers consulted; broader community next"),
    "CARE-A1": ("yes",     ""),
    "CARE-A2": ("no",      "No formal mechanism to revoke permissions yet"),
    "CARE-R1": ("yes",     ""),
    "CARE-R2": ("yes",     "Data sharing agreement in place"),
    "CARE-E1": ("yes",     "No sensitive locations in gauge dataset"),
    "CARE-E2": ("partial", "Ethics documented for project; post-project unclear"),
    "FAIR-F1": ("no",      "DOI pending Zenodo upload"),
    "FAIR-F2": ("yes",     ""),
    "FAIR-A1": ("yes",     ""),
    "FAIR-I1": ("yes",     "GeoJSON, CSV, Parquet with standard USGS field names"),
    "FAIR-R1": ("yes",     "CC0 for public data; Tribal data gitignored"),
    "FAIR-R2": ("yes",     "IEEE 2890-2025 provenance catalog attached"),
    "IEEE-1":  ("yes",     "Treaty provenance on every output"),
    "IEEE-2":  ("yes",     "NRD identified as steward"),
    "IEEE-3":  ("yes",     "Processing steps documented in provenance catalog"),
    "IEEE-4":  ("partial", "Derived datasets link to source; chain incomplete for some"),
    "IEEE-5":  ("yes",     "Classification attached to every output file"),
})

print(audit.report())
audit.save("outputs/sovereignty_audit_water_monitoring.txt")
```

## Monitoring gap finding 

The water monitoring series consistently surfaces monitoring gaps on
Tribal lands. The toolkit provides the framing for presenting these
gaps as policy findings rather than data errors:

```python
# In notebook 08 (aquifer geology), after loading USGS well sites:
wells_pr = load_usgs_well_sites(PINE_RIDGE_BBOX)

if wells_pr.empty:
    print("MONITORING GAP FINDING")
    print(ctx.config.treaty_status)
    print()
    print(
        "No USGS groundwater monitoring wells documented within Pine Ridge "
        "Reservation boundaries. This is not a geological uncertainty, it "
        "is a federal investment gap with a documented history. "
        "Tribal-collected well logs fill this gap: see data/templates/"
    )
```

The sovereignty framing: "federal investment gap" rather than "data
unavailable" is consistent across all notebooks and is grounded in
the treaty provenance language in `nation.yaml`.


## Sovereignty findings across the series

The water monitoring series produces five findings that require the
sovereignty framing:

1. **Streamflow monitoring:** 15 gauges for 18,000+ km² of Tribal
   territory is insufficient for drought early warning.

2. **Groundwater monitoring:** USGS well density on Pine Ridge is a
   fraction of that in adjacent agricultural counties.

3. **Water quality:** Public WQP monitoring is sparse; gaps are a
   federal infrastructure equity issue.

4. **PDSI accuracy:** The drought index is computed from stations
   concentrated outside reservation boundaries.

5. **Aquifer characterization:** The Spangler (2024) 3D model's accuracy
   is lowest on Tribal lands due to sparse well log control.

Each of these findings is framed in notebook 09 (Data Gaps and Sovereignty)
using the treaty provenance language from the toolkit config.
