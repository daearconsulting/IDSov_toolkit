# Tribal Data Sovereignty Toolkit

**Author:** Lilly Jones, PhD                         
**Version:** 1.2.0                                     
**Frameworks:** OCAP® | CARE | FAIR | IEEE 2890-2025                             
**License:** GNU Affero GPL 3.0

> [![DOI](https://zenodo.org/badge/1282454716.svg)](https://doi.org/10.5281/zenodo.21405018)

## Overview

The Tribal Data Sovereignty Toolkit is a generalizable framework for
supporting Nation-defined data governance decisions in Earth data science
workflows. It provides Python modules, a teaching notebook series, and
document templates that work together to make sovereignty a built-in
feature of data pipelines.

The toolkit was developed in the context of Earth data science work and is
designed to be modular so it can be adapted for any Tribal Nation.

## Who is this for?

| Audience | Start here |
|---|---|
| Tribal data managers and natural resource staff | [`Forms/`](Forms/) then [notebook 04](Notebooks/04_collection_design.ipynb) |
| Researchers working with Tribal data | [Notebooks 00–03](Notebooks/) |
| Students and educators | [Full notebook series 00–06](Notebooks/) |
| Hackathon and workshop participants | [Notebook 05 (SEEDS Workflow)](Notebooks/05_seeds_workflow.ipynb) |

## Repository Structure

```
IDSov_toolkit/
│
├── toolkit/                    # Python modules
│   ├── sovereignty.py          # Core with NationConfig, SovereigntyContext
│   ├── provenance.py           # IEEE 2890-2025 provenance records
│   ├── governance.py           # Statements, checklists, agreements
│   └── audit.py                # Sovereignty audit (OCAP® + CARE + FAIR + IEEE 2890)
│
├── Notebooks/                  # Teaching series
│   ├── 00_orientation.ipynb    # Start here
│   ├── 01_frameworks.ipynb     # OCAP®, CARE, FAIR, IEEE 2890-2025
│   ├── 02_data_provenance.ipynb
│   ├── 03_sovereignty_audit.ipynb
│   ├── 04_collection_design.ipynb
│   ├── 05_seeds_workflow.ipynb  # Responsible Earth Data Science
│   └── 06_adaptation_guide.ipynb
│
├── Forms/                      # Document toolkit (no coding required)
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

> [!IMPORTANT]
> Do not commit restricted, confidential, culturally sensitive, or otherwise
> non-public Tribal data to Git, example outputs, or public notebooks. Follow
> the relevant Nation's governance rules and approved storage requirements.

### For non-coders: use the templates directly

1. Open `Forms/data_sovereignty_statement.md` and fill in the
   bracketed fields
2. Open `Forms/ieee_2890_compliance_checklist.xlsx` (legacy filename; self-assessment) to review your
   dataset
3. Open `Forms/tribal_data_catalog.xlsx` to catalog your data assets

No installation required.

### For Python users

```bash
# Clone the repo
git clone https://github.com/daearconsulting/IDSov_toolkit.git
cd IDSov_toolkit

# Create and activate the environment
conda env create -f environment.yml
conda activate tribal-data-sovereignty

# Install the toolkit as a package (optional but recommended)
pip install -e .

# For a working project, copy and complete the blank config
cp config/nation_template.yaml config/nation.yaml
# Resolve placeholders and document Nation-selected policies before validation

# Validate
python -m toolkit.governance --config config/nation.yaml --validate
```

### In a notebook

```python
from toolkit.sovereignty import SovereigntyContext

ctx = SovereigntyContext.from_config("config/nation.yaml")
ctx.print_acknowledgment()

# Attach provenance to any GeoDataFrame
gdf = ctx.attach_provenance(gdf, source_key="usgs_nwis_streamflow", classification="PUBLIC")

# Generate citations
print(ctx.generate_citations(["usgs_nwis_streamflow", "usda_ssurgo"]))
```

## Adapting for a New Nation

The toolkit ships with a clearly fictional Example River Nation teaching configuration and a separate blank working template. To adapt for another Nation:

1. Copy `config/nation_template.yaml` to `config/nation.yaml`
2. Resolve placeholders and document Nation-selected policies (configuration entry time excludes governance review)
3. Run `python -m toolkit.governance --config config/nation.yaml --validate`
4. Notebooks load your config through the shared loader; regenerate and review outputs and complete standalone forms separately

See the [adaptation guide notebook](Notebooks/06_adaptation_guide.ipynb) for a
complete walkthrough, or begin with the [quickstart](docs/quickstart.md).

## Testing

Install the development dependencies and run the unit tests:

```bash
pip install -e ".[dev]"
pytest
```

To execute the notebooks covered by continuous integration:

```bash
pytest --nbmake Notebooks/00_orientation.ipynb Notebooks/01_frameworks.ipynb \
  Notebooks/02_data_provenance.ipynb Notebooks/03_sovereignty_audit.ipynb \
  Notebooks/04_collection_design.ipynb Notebooks/05_seeds_workflow.ipynb \
  Notebooks/06_adaptation_guide.ipynb
```

**For Nation-specific consulting assistance** such as integrating existing Tribal
data codes, Local Contexts TK Labels, or Tribal data governance policies,
contact Daear Consulting, LLC.

## The Governance Framework Stack

This toolkit supports complementary frameworks. A Nation determines which are
applicable and may replace or extend them with its own policies. In particular,
OCAP® was developed for First Nations in Canada and must not be assumed to apply
outside that context.

| Framework | Governs | Reference |
|---|---|---|
| **OCAP®** | Ownership, Control, Access, Possession | https://fnigc.ca/ocap-training/ |
| **CARE** | Collective Benefit, Authority, Responsibility, Ethics | https://www.gida-global.org/care |
| **FAIR** | Findable, Accessible, Interoperable, Reusable | https://www.go-fair.org/fair-principles/ |
| **IEEE 2890-2025** | Provenance of Indigenous Peoples' Data | https://standards.ieee.org/ieee/2890/10318/ |

FAIR addresses technical data management, including restricted access. CARE and, where applicable, OCAP® address governance concerns that FAIR alone does not cover. The toolkit provides its own provenance schema; IEEE conformance has not been established.

## Connected Repositories

This toolkit is the canonical source for sovereignty infrastructure
used across Daear Consulting's Earth data science repos.

## Citation

If you use this toolkit in your work, please cite:

> Jones, L. (2026). Tribal Data Sovereignty Toolkit. Daear Consulting, LLC.
> https://github.com/daearconsulting/IDSov_toolkit

Machine-readable citation metadata is available in [`citation.cff`](citation.cff).

And acknowledge the Tribal Nations whose data and lands informed its
development:

> We are grateful for the opportunity to support Tribal data
> sovereignty in Earth data science.

## License

See the [GNU Affero General Public License v3.0](LICENSE).

The governance frameworks referenced by this toolkit (OCAP®, CARE, FAIR,
IEEE 2890-2025) are governed by their respective organizations. This
toolkit provides review prompts informed by them and does not claim certification.

## Revised teaching workflow

Each lesson produces a draft artifact and includes objectives, a decision exercise,
an independent task, and a completion checklist. See [the teaching guide](docs/teaching_guide.md).
The shared case is fictional, and lesson 05 uses synthetic observations offline by
default. No approval, engagement, or return of findings is implied by execution.

The audit withholds overall scores for incomplete assessments, records evidence
per question, honors framework selection, and separates research/sharing approvals
from indicative scores. It never certifies compliance or grants release permission.

Access classification, approved storage, version control, and publication status
are separate fields. Migrate the old GITIGNORED tier using the
[adaptation guide](docs/adaptation_guide.md). A treaty is optional where inapplicable.

Load order: explicit path, IDSOV_CONFIG, config/nation.yaml, fictional teaching example.
The blank template intentionally fails validation until completed. Configuration
entry time is separate from governance review and authorization.

The existing whitepaper is a separately maintained document and may describe an
earlier release. Current behavior is documented in these guides and tested code.
