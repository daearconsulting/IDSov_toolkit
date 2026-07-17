# Tribal Data Sovereignty Toolkit

**Author:** Lilly Jones, PhD  
**Version:** 1.0.0  
**Frameworks:** OCAP® | CARE | FAIR | IEEE 2890-2025  
**License:** GNU Affero GPL 3.0


## Overview

The Tribal Data Sovereignty Toolkit is a generalizable framework for
implementing Indigenous data sovereignty principles in Earth data science
workflows. It provides Python modules, a teaching notebook series, and
document templates that work together to make sovereignty a built-in
feature of data pipelines.

The toolkit was developed in the context of Earth data science work and is
designed to be modular so it can be adapted for any Tribal Nation.

## Who is this for?

| Audience | Start here |
|---|---|
| Tribal data managers and natural resource staff | `templates/` then notebook 04 |
| Researchers working with Tribal data | Notebooks 00–03 |
| Students and educators | Full notebook series 00–06 |
| Hackathon and workshop participants | Notebook 05 (SEEDS Workflow) |

## Repository Structure

```
tribal-data-sovereignty-toolkit/
│
├── toolkit/                    # Python modules
│   ├── sovereignty.py          # Core — NationConfig, SovereigntyContext
│   ├── provenance.py           # IEEE 2890-2025 provenance records
│   ├── governance.py           # Statements, checklists, agreements
│   └── audit.py                # Sovereignty audit (OCAP® + CARE + FAIR + IEEE 2890)
│
├── notebooks/                  # Teaching series
│   ├── 00_orientation.ipynb    # Start here
│   ├── 01_frameworks.ipynb     # OCAP®, CARE, FAIR, IEEE 2890-2025
│   ├── 02_data_provenance.ipynb
│   ├── 03_sovereignty_audit.ipynb
│   ├── 04_collection_design.ipynb
│   ├── 05_seeds_workflow.ipynb  # Responsible Earth Data Science
│   └── 06_adaptation_guide.ipynb
│
├── templates/                  # Document toolkit (no coding required)
│   ├── data_sovereignty_statement.md
│   ├── community_consent_framework.md
│   ├── ieee_2890_compliance_checklist.xlsx
│   ├── tribal_data_catalog.xlsx
│   └── provenance_record.xlsx
│
├── config/
│   └── nation_template.yaml    # Edit this to adapt for any Nation
│
├── docs/
│   ├── quickstart.md
│   ├── frameworks_reference.md
│   └── adaptation_guide.md
│
└── examples/
    ├── water_monitoring.md
    ├── mining_twin.md
    └── soils_geology.md
```

## Quick Start

### For non-coders: use the templates directly

1. Open `templates/data_sovereignty_statement.md` and fill in the
   bracketed fields
2. Open `templates/ieee_2890_compliance_checklist.xlsx` to audit your
   dataset
3. Open `templates/tribal_data_catalog.xlsx` to catalog your data assets

No installation required.

### For Python users

```bash
# Clone the repo
git clone https://github.com/daear-consulting/tribal-data-sovereignty-toolkit
cd tribal-data-sovereignty-toolkit

# Create and activate the environment
conda env create -f environment.yml
conda activate tribal-data-sovereignty

# Install the toolkit as a package (optional but recommended)
pip install -e .

# Copy and edit the config
cp config/nation_template.yaml config/nation.yaml
# Edit nation.yaml with your Nation's information

# Validate
python toolkit/governance.py --config config/nation.yaml --validate
```

### In a notebook

```python
from toolkit.sovereignty import SovereigntyContext

ctx = SovereigntyContext.from_config("config/nation.yaml")
ctx.print_acknowledgment()

# Attach provenance to any GeoDataFrame
gdf = ctx.attach_provenance(gdf, source_key="usgs_nwis_streamflow")

# Generate citations
print(ctx.generate_citations(["usgs_nwis_streamflow", "usda_ssurgo"]))
```

## Adapting for a New Nation

The toolkit ships with an Oglala Lakota/Pine Ridge configuration as the
default example. To adapt for another Nation:

1. Copy `config/nation_template.yaml` to `config/nation.yaml`
2. Edit every field (takes approximately 20 minutes)
3. Run `python toolkit/governance.py --config config/nation.yaml --validate`
4. All notebooks, templates, and modules auto-populate from your config

See `notebooks/06_adaptation_guide.ipynb` for a complete walkthrough.

**For Nation-specific consulting assistance** such as integrating existing Tribal
data codes, Local Contexts TK Labels, or Tribal data governance policies,
contact Daear Consulting, LLC.

## The Governance Framework Stack

This toolkit implements four complementary frameworks:

| Framework | Governs | Reference |
|---|---|---|
| **OCAP®** | Ownership, Control, Access, Possession | https://fnigc.ca/ocap-training/ |
| **CARE** | Collective Benefit, Authority, Responsibility, Ethics | https://www.gida-global.org/care |
| **FAIR** | Findable, Accessible, Interoperable, Reusable | https://www.go-fair.org/fair-principles/ |
| **IEEE 2890-2025** | Provenance of Indigenous Peoples' Data | https://standards.ieee.org/ieee/2890/10318/ |

FAIR governs technical data management. CARE and OCAP® govern the ethical
obligations that FAIR alone does not address. IEEE 2890-2025 operationalizes
both into machine-readable provenance records.

## Connected Repositories

This toolkit is the canonical source for sovereignty infrastructure
used across Daear Consulting's Earth data science repos:

- **tribal_water_monitoring** - Surface water and groundwater analysis
- **he_sapa_mining_twin** - Black Hills mining history and impacts
- **tribal_soils_geology** - Soils and geology for Pine Ridge and Rosebud
- **OLC Hackathon** - Climate resiliency and digital sovereignty

## Citation

If you use this toolkit in your work, please cite:

> Jones, L. (2026). Tribal Data Sovereignty Toolkit. Daear Consulting, LLC.
> https://github.com/daear-consulting/tribal-data-sovereignty-toolkit

And acknowledge the Tribal Nations whose data and lands informed its
development:

> We are grateful for the opportunity to support Tribal data
> sovereignty in Earth data science.

## License

see LICENSE file.

The governance frameworks referenced by this toolkit (OCAP®, CARE, FAIR,
IEEE 2890-2025) are governed by their respective organizations. This
toolkit implements them but does not own or modify them.
