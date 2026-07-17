# Example: He Sapa Mining Twin Integration
## Tribal Data Sovereignty Toolkit

This example shows how `he_sapa_mining_twin` uses the toolkit for the
Black Hills mining history analysis. The mining twin has a distinctive
sovereignty challenge: it describes extractive industry activity on
unceded Lakota territory, which requires careful framing throughout.

## The territorial provenance challenge

He Sapa (the Black Hills) presents the clearest case of the distinction
between legal title and moral sovereignty. The Black Hills were taken in 
violation of the 1868 Fort Laramie Treaty. The U.S. Supreme Court confirmed 
this in *United States v. Sioux Nation* (1980). The Sioux Nations declined 
monetary compensation, maintaining that the land was never legally transferred.

The toolkit's treaty provenance language for He Sapa work:

```yaml
# In nation.yaml for He Sapa-specific analysis:
provenance:
  treaty_name:      "1868 Fort Laramie Treaty"
  treaty_territory: "He Sapa (Black Hills): unceded Lakota territory"
  treaty_status: >
    He Sapa (the Black Hills) remain the unceded territory of the Lakota
    people under the 1868 Fort Laramie Treaty. The Black Hills were taken
    by the United States in violation of that treaty. The U.S. Supreme
    Court confirmed this in United States v. Sioux Nation of Indians,
    448 U.S. 371 (1980). The Sioux Nations have declined financial
    compensation, maintaining that the land was never legally transferred.
    USGS mineral data describing He Sapa describes Lakota resources.
  legal_citations:
    - "United States v. Sioux Nation of Indians, 448 U.S. 371 (1980)"
    - "1868 Fort Laramie Treaty, Article II"
```

## Setup pattern

```python
import sys
sys.path.insert(0, "/path/to/tribal-data-sovereignty-toolkit")

from toolkit.sovereignty import SovereigntyContext

ctx = SovereigntyContext.from_config("config/nation.yaml")
ctx.print_acknowledgment(source_keys=["usgs_mrds", "census_aiannh"])
```

## Attaching provenance to mine data

```python
from toolkit.provenance import ProvenanceBuilder, ProvenanceCatalog

catalog = ProvenanceCatalog("He Sapa Mining Twin")

# MRDS mine data
catalog.add(
    ProvenanceBuilder("mrds-black-hills-2024")
    .for_nation(ctx)
    .for_dataset("USGS MRDS Mine Locations for the Black Hills")
    .from_source("usgs_mrds")
    .step("Queried USGS MRDS WFS endpoint (GML format)")
    .step("Parsed GML with ElementTree; extracted coordinates from gml:coordinates")
    .step("Classified by commodity group (gold, silver, other metals, etc.)")
    .step("Spatially joined to HUC8 watershed boundaries")
    .classify("PUBLIC")
    .note(
        "USGS MRDS documents extractive industry activity on unceded "
        "Lakota territory. The presence of 1,719+ mine records in He Sapa "
        "reflects the history of the 1877 Act of Congress that took the "
        "Black Hills in violation of the 1868 Fort Laramie Treaty. "
        "This data describes Lakota resources extracted without consent."
    )
    .build()
)

catalog.save("outputs/provenance_catalog_hesapa.json")
```

## The sovereignty framing for mining data

Mining data on unceded territory requires an explicit sovereignty frame
that goes beyond the standard "federal data collected on Tribal lands"
language. The He Sapa mining twin notebooks use this pattern:

```python
# In notebook 01 (Mine Gazetteer), after loading MRDS data:
print(ctx.generate_citations(["usgs_mrds"]))
print()
print("TERRITORIAL NOTE")
print(ctx.config.treaty_status)
print()
print(
    f"The {len(mines):,} mine records in this dataset describe extractive "
    "industry activity on Lakota territory. This includes gold mines "
    "established during and after the 1874 Custer Expedition, an "
    "illegal incursion into treaty-protected land that precipitated the "
    "Black Hills War and the 1877 Act of Congress taking He Sapa."
)
```

## The interactive demo map sovereignty considerations

The He Sapa demo map (`outputs/he_sapa_mining_twin_demo.html`) includes
a territorial acknowledgment panel in the map interface itself:

```python
# In the folium map construction:
acknowledgment_html = f"""
<div style="background:#1a1a2e;color:white;padding:12px;border-radius:6px;
            font-family:sans-serif;font-size:11px;max-width:300px;">
  <b style="color:#4FC3F7;">He Sapa Black Hills</b><br>
  <hr style="border-color:#4FC3F7;margin:6px 0;">
  Unceded Lakota Territory<br>
  1868 Fort Laramie Treaty<br><br>
  {ctx.config.treaty_status[:200]}...<br><br>
  <small style="color:#aaa;">
    {ctx.config.legal_citations[0] if ctx.config.legal_citations else ""}
  </small>
</div>
"""
folium.Marker(
    [44.0, -103.5],
    popup=folium.Popup(acknowledgment_html, max_width=320),
    icon=folium.DivIcon(html='<div style="color:#4FC3F7;font-size:12px;">⚑</div>'),
    tooltip="Territorial Acknowledgment"
).add_to(m)
```

## Mine count per watershed as a sovereignty finding

The HUC8 watershed analysis in notebook 02 produces the key finding:
mine density by watershed. The sovereignty framing:

```python
# After computing mine_counts per watershed:
print("MINE DENSITY BY WATERSHED for He Sapa")
print(ctx.config.treaty_status)
print()
print("NOTE: These mines extracted resources from Lakota territory.")
print("The watershed with highest mine density (10120109) includes")
print("the central Black Hills where gold extraction was most intensive.")
print()
print("This analysis does not constitute an endorsement of past or")
print("present extractive activity on Lakota territory.")
```

## Key sovereignty findings in the mining twin

1. **1,719+ USGS MRDS records** document extractive industry on unceded
   Lakota territory, a dataset describing Lakota resource loss.

2. **MRDS coverage gaps:** The federal mine database may undercount
   historical small-scale mining; it does not document the full extent
   of resource extraction.

3. **No Tribal royalty data:** Federal records do not document whether
   or how Tribal Nations were compensated for resource extraction on
   treaty territory.

4. **The data frame matters:** Presenting mine data as neutral geographic
   information without the treaty context obscures the history the data
   encodes. The toolkit's provenance and acknowledgment infrastructure
   ensures that context is always present.
