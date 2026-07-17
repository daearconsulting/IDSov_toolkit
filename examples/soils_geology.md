# Example: Tribal Soils and Geology Integration
## Tribal Data Sovereignty Toolkit

This example shows how `tribal_soils_geology` uses the toolkit across
its nine-notebook series. The soils and geology context adds a specific
sovereignty dimension: subsurface resources such as aquifers, mineral deposits,
and soil systems are often governed by different legal frameworks than
surface resources, yet the same OCAP® principles apply.

## The subsurface sovereignty note

The soils and geology series includes a subsurface-specific sovereignty
note in `nation.yaml` that all nine notebooks reference:

```yaml
provenance:
  subsurface_note: >
    Subsurface geological and hydrological data describing Tribal lands
    is subject to OCAP® principles. The Arikaree aquifer, the Pierre Shale,
    and the Ogallala Group are the material foundation of Lakota water 
    security and land sovereignty. Federal geological surveys conducted on 
    Pine Ridge and Rosebud describe Tribal resources. Ownership and stewardship 
    rights belong to the relevant Tribal Nations.
```

## Setup pattern (all nine notebooks)

```python
import sys
sys.path.insert(0, "/path/to/tribal-data-sovereignty-toolkit")

from toolkit.sovereignty import SovereigntyContext

ctx = SovereigntyContext.from_config("config/nation.yaml")
ctx.print_acknowledgment(source_keys=[
    "usgs_3d_model",
    "usda_ssurgo",
    "usgs_nwis_groundwater",
    "census_aiannh",
])
```

## Provenance for the 3D model (notebook 04)

The Spangler (2024) 3D geological model is the centerpiece dataset of
the series. Its provenance record reflects both technical and governance
lineage:

```python
from toolkit.provenance import ProvenanceBuilder, ProvenanceCatalog

catalog = ProvenanceCatalog("Tribal Soils and Geology for Pine Ridge 2024")

# 3D model raster horizons
for unit_name in wsd_key_horizons:
    catalog.add(
        ProvenanceBuilder(f"wsd-3d-{unit_name.lower().replace(' ','-')}")
        .for_nation(ctx)
        .for_dataset(f"WSD 3D Model {unit_name} Horizon")
        .from_source("usgs_3d_model")
        .step(f"Loaded horizon raster for {unit_name} from WSouthDakota3D.gdb")
        .step("Clipped to Pine Ridge and Rosebud combined bounding box")
        .step("Resampled to 1km resolution for visualization")
        .classify("PUBLIC")
        .note(
            f"The {unit_name} horizon is modeled at regional scale. "
            "Local variability not captured. Model uncertainty is highest "
            "on Tribal lands where well log control is sparse, a federal "
            "monitoring investment gap that Tribal-collected well logs can reduce."
        )
        .build()
    )
```

## Tribal-collected data intake framework

The three field data templates (`soil_profile_template.xlsx`,
`well_log_template.xlsx`, `field_observation_template.xlsx`) all include
a Sovereignty sheet with OCAP® language. When Tribal staff load collected
data, the sovereignty context is attached immediately:

```python
from src.loaders import load_tribal_soil_profiles

tribal_profiles = load_tribal_soil_profiles()

if not tribal_profiles.empty:
    # Attach provenance: classification is GITIGNORED for Tribal field data
    # We don't attach to the DataFrame directly (it stays local)
    # but we do create a provenance record for the catalog

    catalog.add(
        ProvenanceBuilder("tribal-soil-profiles-2024")
        .for_nation(ctx)
        .for_dataset("Tribal Soil Profile Data for Pine Ridge")
        .from_source("tribal_field_data")
        .collected_by(
            ctx.config.department,
            method="Field soil description using USDA horizon methods",
        )
        .classify("GITIGNORED")
        .note(
            "OCAP® governed. Never commit to version control. "
            "Data collected by Tribal staff fills the SSURGO sampling gap. "
            "Each Tribal profile is a control point for future soil mapping."
        )
        .build()
    )
```

## The data gaps notebook (notebook 09) sovereignty synthesis

Notebook 09 synthesizes monitoring gaps across the series. The toolkit
provides the framing infrastructure:

```python
# Generate the full sovereignty statement for the series
from toolkit.governance import data_sovereignty_statement, compliance_checklist

print(data_sovereignty_statement(ctx))
```

```python
# Register soils-specific data sources
ctx.register_source("usgs_sgmc2", {
    "name":    "USGS State Geologic Map Compilation (SGMC2) for South Dakota",
    "steward": "US Geological Survey",
    "license": "Public domain",
    "url":     "https://mrdata.usgs.gov/geology/state/",
    "note":    (
        "State-scale mapping (1:500,000) does not resolve reservation-scale "
        "geologic variability. Systematic quad-scale mapping (1:24,000) has "
        "not been completed for Pine Ridge or Rosebud. This is a federal "
        "geological mapping investment gap."
    ),
})

ctx.register_source("tribal_well_logs", {
    "name":    "Tribal-Collected Well Log Data",
    "steward": ctx.config.department,
    "license": "Tribal: governed by OCAP®",
    "url":     "data/raw/ (local only: gitignored)",
    "note":    (
        "Each Tribal well log is a subsurface control point that reduces "
        "uncertainty in the Spangler (2024) 3D model on Tribal lands. "
        "Collecting and logging wells is an investment in data sovereignty."
    ),
})
```

## Gap severity scatter plot framing

The data gap assessment in notebook 09 uses the toolkit's treaty language
to frame gaps as policy findings:

```python
# After computing gap scores:
print("DATA GAP SYNTHESIS: Tribal Soils and Geology")
print()
print(ctx.config.treaty_status)
if ctx.config.subsurface_note:
    print()
    print(ctx.config.subsurface_note)
print()
print("Each gap identified in this series represents a federal investment")
print("decision on Tribal lands. The absence")
print("of monitoring data is a policy")
print("record of how federal agencies have prioritized other communities")
print("over Tribal Nations in scientific infrastructure investment.")
```

## Connecting soils/geology to water monitoring

The aquifer geology notebook (notebook 08) is the primary bridge between
the soils/geology and water monitoring series. Both repos reference the
same toolkit config and provenance registry:

```python
# In soils/geology notebook 08:
print("CONNECTION TO TRIBAL WATER MONITORING SERIES")
print()
print(
    "The Ogallala Group horizon raster from the Spangler (2024) 3D model "
    "provides the subsurface context for the aquifer analysis in "
    "tribal_water_monitoring notebook 08. Where the Ogallala is thin or "
    "absent, the White River and its tributaries have reduced baseflow."
)
print()
print("Both series implement sovereignty through the same toolkit config:")
print("  - Same treaty provenance language")
print("  - Same classification schema")
print("  - Same data source registry")
print("  - Cross-referenced provenance catalogs")
```

## Key sovereignty findings in the soils/geology series

1. **SSURGO sampling density** on Pine Ridge and Rosebud is lower than
   adjacent agricultural counties, a federal NRCS investment gap.

2. **No USGS monitoring wells** documented within Pine Ridge reservation
   boundaries, a systematic groundwater monitoring equity gap.

3. **3D model accuracy lowest on Tribal lands** the Spangler (2024)
   model's uncertainty is highest where well log control is sparsest,
   which is on Tribal territory.

4. **State geologic map resolution** (1:500,000) cannot support
   infrastructure siting or hazard assessment at the reservation scale.
   Systematic quad mapping has never been conducted on either reservation.

5. **Subsurface governance gap:** Federal geological surveys on Tribal
   territory produce data about Tribal resources (aquifers, mineral
   formations, soil systems) without a governance framework that
   recognizes Tribal ownership of those findings.
