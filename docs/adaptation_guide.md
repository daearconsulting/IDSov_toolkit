# Adaptation Guide
## Tribal Data Sovereignty Toolkit

## Overview

The toolkit ships with an Oglala Lakota/Pine Ridge configuration as its
default example. This guide walks through every step of adapting it for
a different Nation. The process takes approximately 30–60 minutes.

**For Nations with existing data governance codes or policies,** contact
Daear Consulting, LLC. Integrating Nation-specific governance documents
into the toolkit configuration is a consulting engagement that goes beyond
what this guide covers.

## What "adaptation" means

Adapting the toolkit means editing one YAML file `config/nation.yaml` 
so that all sovereignty statements, provenance records, compliance
checklists, and data sharing agreement templates auto-populate with your
Nation's specific information.

Nothing in `toolkit/sovereignty.py`, `toolkit/provenance.py`,
`toolkit/governance.py`, or `toolkit/audit.py` is hard-coded to any
specific Nation. All Nation-specific information flows through the config.

## Step 1 Copy the template

```bash
cp config/nation_template.yaml config/nation.yaml
```

Open `config/nation.yaml` in a text editor. Work through each section.

## Section: `nation`

```yaml
nation:
  name:        "Navajo Nation"      # Primary Nation name
  collective:  null                 # Broader collective if applicable
  territory:   "Navajo Nation Reservation and Trust Lands"
  census_name: "Navajo Nation"      # Exact string from Census TIGER NAME field
  language:    "Diné bizaad"        # Primary language
  demonym:     "Diné"               # How members refer to themselves
```

**`census_name`** is the most technically important field and it must match
the exact string in the Census TIGER AIANNH shapefile `NAME` field.
To find the correct value, run this in a notebook:

```python
import geopandas as gpd, requests, zipfile, tempfile, io
from pathlib import Path

r = requests.get(
    "https://www2.census.gov/geo/tiger/TIGER2023/AIANNH/tl_2023_us_aiannh.zip",
    timeout=300
)
with zipfile.ZipFile(io.BytesIO(r.content)) as z:
    with tempfile.TemporaryDirectory() as tmp:
        z.extractall(tmp)
        shp = next(Path(tmp).glob("*.shp"))
        aiannh = gpd.read_file(shp)

# Search for your Nation
matches = aiannh[aiannh["NAME"].str.contains("Navajo", case=False)]
print(matches[["NAME","GEOID"]].to_string())
```

## Section: `territory`

```yaml
territory:
  bbox:
    west:  -112.0
    south:   35.0
    east:  -106.0
    north:   37.5
  centroid:
    lat: 36.5
    lon: -109.0
```

The bounding box is used for spatial data queries throughout the
analysis notebooks. Use a bbox that covers the entire territory plus
some buffer so it is easy to clip later.

To find your bbox, go to https://bboxfinder.com/ or use:

```python
# After loading your Nation's boundary:
bounds = gdf.total_bounds  # [west, south, east, north]
print(bounds)
```

## Section: `provenance`

This is the most important section. Take time to get it right as this
text appears on every data product and provenance record.

```yaml
provenance:
  treaty_name:      "1868 Treaty of Bosque Redondo"
  treaty_territory: "Diné Bikéyah (Navajo homeland)"
  treaty_status: >
    The lands of the Navajo Nation are the sovereign territory of the
    Diné people. [Continue with 2-3 sentences specific to your Nation's
    treaty status and current legal standing.]

  legal_citations:
    - "[Any relevant court case or statute]"

  subsurface_note: >
    [If relevant, note about subsurface rights, mineral rights, etc.
    Delete this field if not applicable to your analysis.]
```

**Writing the `treaty_status` field:**
This should be a statement that accurately represents your Nation's
treaty status and sovereignty claim. It should be reviewed by someone
with knowledge of your Nation's specific legal situation. The statement
in the Pine Ridge default (about the 1868 Fort Laramie Treaty) is
specific to the Oceti Sakowin; do not copy it for a different Nation.

## Section: `stewardship`

```yaml
stewardship:
  department:  "Department of Natural Resources"
  contact_url: "https://www.navajonationenvironment.org/"
  contact_note: >
    All data describing Navajo Nation lands should be reviewed by and
    shared with the Department of Natural Resources before publication.
```

The department name and contact URL appear on every sovereignty statement
and governance report. Use the Tribal department that is actually
responsible for data governance in your context; this may be Natural
Resources, Environmental Protection, GIS, THPO or a dedicated data governance
body.

## Section: `frameworks`

In most cases, leave all four frameworks enabled. If your Nation uses
Local Contexts TK Labels, set `local_contexts.enabled: true` and specify
the label type.

```yaml
frameworks:
  local_contexts:
    enabled:    true
    label_type: "TK Notice"    # TK Notice, TK Attribution Incomplete, etc.
```

Contact the Local Contexts Hub (https://localcontexts.org/) to select
the appropriate label type for your Nation's context. TK Label selection
is a governance decision and it should involve knowledge holders and
cultural leadership.

## Section: `data_classification`

The default classification schema (PUBLIC / COMMUNITY / RESTRICTED /
GITIGNORED) covers most cases. If your Nation has its own data
classification policy, replace the default tiers with your Nation's
categories:

```yaml
data_classification:
  tiers:
    - id:          "OPEN"
      label:       "Open Access"
      description: "..."
    - id:          "TRIBAL"
      label:       "Tribal Members Only"
      description: "..."
    - id:          "RESTRICTED"
      label:       "Council and Staff Only"
      description: "..."
    - id:          "SACRED"
      label:       "Ceremonial: Never Digital"
      description: "..."
```

The `id` values are used as codes throughout the toolkit. Choose short,
memorable strings. Once set and used in provenance records, changing them
requires updating all existing records.

## Step 2: Validate

```bash
python toolkit/governance.py --config config/nation.yaml --validate
```

Fix any warnings before proceeding. Common issues:

- **`nation.name is required`** you left a bracket `[...]` in the file
- **`provenance.treaty_name is required`** same
- **`At least one framework must be enabled`** check that at least
  one framework has `enabled: true`

## Step 3: Test the output

```bash
# Generate a sovereignty statement
python toolkit/governance.py --config config/nation.yaml --statement

# Generate a compliance checklist  
python toolkit/governance.py --config config/nation.yaml --checklist

# Generate a data sharing agreement template
python toolkit/governance.py --config config/nation.yaml \
    --agreement "My Research Project" \
    --output templates/data_sharing_agreement.txt
```

Review each output carefully. Does the treaty language accurately represent
your Nation's situation? Is the contact information correct? Is the
attribution language appropriate?

## Step 4: Register Nation-specific data sources

The built-in source registry covers common federal datasets. Add your
Nation's specific data sources:

```python
from toolkit.sovereignty import SovereigntyContext

ctx = SovereigntyContext.from_config("config/nation.yaml")

# Register a Nation-specific source
ctx.register_source("navajo_epa_monitoring", {
    "name":    "Navajo EPA Air and Water Monitoring Program",
    "steward": "Navajo EPA",
    "license": "Tribal — contact Navajo EPA for terms",
    "url":     "https://www.navajonationenvironment.org/",
    "note":    (
        "Data collected and owned by the Navajo Nation EPA. "
        "Use requires coordination with Navajo EPA."
    ),
})

# Now use this key in provenance records
gdf = ctx.attach_provenance(gdf, source_key="navajo_epa_monitoring")
```

## Step 5: Connect to your analysis repos

Once `nation.yaml` is configured, connect the toolkit to your analysis
repositories by adding this to their setup cells:

```python
import sys
sys.path.insert(0, "/path/to/tribal-data-sovereignty-toolkit")

from toolkit.sovereignty import SovereigntyContext
ctx = SovereigntyContext.from_config(
    "/path/to/tribal-data-sovereignty-toolkit/config/nation.yaml"
)
ctx.print_acknowledgment()
```

This replaces any individual `sovereignty.py` files in your repos with
a single canonical source. When you update `nation.yaml`, all repos
that import from the toolkit update automatically.

## What Nation-specific consulting covers

The adaptation guide above handles the generalizable configuration.
Some situations require direct consulting support:

**Integrating existing Tribal data codes:** If your Nation has enacted
data governance legislation (like the Navajo Nation Data Governance Act
or similar) or has existing data policies, the toolkit needs to be
configured to reflect those specific provisions rather than the default
OCAP® / CARE stack.

**Local Contexts TK Label selection:** Choosing the right TK Labels
requires engagement with knowledge holders and cultural leadership. 
Daear Consulting can facilitate this process and implement the labels in the toolkit.

**Custom classification schemas:** If your Nation's data classification
system differs significantly from the default four-tier schema,
particularly if it includes categories for ceremonial knowledge,
culturally sensitive locations, or other specialized content types,
the toolkit can be extended to support those.

**Training and capacity-building:** The toolkit is designed to be used
by Tribal data staff without external support. Training workshops can
accelerate adoption and ensure staff understand the governance frameworks
the toolkit implements.

**Contact:** Daear Consulting, LLC
