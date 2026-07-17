# Quickstart Guide
## Tribal Data Sovereignty Toolkit

## Choose your path

### I don't write code, I just need governance documents

No installation required. Go straight to `templates/`:

| Template | Use it for |
|---|---|
| `data_sovereignty_statement.md` | Any report, publication, or data package |
| `community_consent_framework.md` | Starting a new data collection program |
| `ieee_2890_compliance_checklist.xlsx` | Auditing an existing dataset before publication |
| `tribal_data_catalog.xlsx` | Maintaining an inventory of your Nation's data assets |
| `provenance_record.xlsx` | Documenting a single dataset's governance history |

Fill in the bracketed fields. That's it.

### I'm a researcher working with Tribal data

**- Read notebook 01 (Frameworks).** Understand what OCAP®, CARE,
FAIR, and IEEE 2890-2025 require of you before you touch any data.

**- Fill out `templates/community_consent_framework.md`** before
data collection begins. Get it reviewed by the Tribal department.

**- Set up the toolkit in Python:**

```bash
git clone https://github.com/daear-consulting/tribal-data-sovereignty-toolkit
cd tribal-data-sovereignty-toolkit

conda env create -f environment.yml
conda activate tribal-data-sovereignty

cp config/nation_template.yaml config/nation.yaml
# Edit nation.yaml (takes about 20 minutes)
```

**- Add sovereignty to your notebooks:**

```python
from toolkit.sovereignty import SovereigntyContext

ctx = SovereigntyContext.from_config("config/nation.yaml")
ctx.print_acknowledgment()   # call at the top of every notebook
```

**- Attach provenance to every output:**

```python
# After loading a GeoDataFrame from a federal source
gdf = ctx.attach_provenance(gdf, source_key="usgs_nwis_streamflow")

# Before sharing any output
print(ctx.generate_citations(["usgs_nwis_streamflow", "usda_ssurgo"]))
```

**- Audit before publication:**

```python
from toolkit.audit import SovereigntyAudit
audit = SovereigntyAudit("My Dataset Name")
# respond to questions, then:
print(audit.report())
```

### I'm teaching a course or running a hackathon

Work through the notebooks in order:

```
00_orientation.ipynb        ← 15 min  what is this and who is it for
01_frameworks.ipynb         ← 45 min  OCAP®, CARE, FAIR, IEEE 2890-2025
02_data_provenance.ipynb    ← 60 min  building and attaching provenance records
03_sovereignty_audit.ipynb  ← 60 min  auditing a dataset
04_collection_design.ipynb  ← 45 min  sovereignty-first field data design
05_seeds_workflow.ipynb      ← 90 min full SEEDS cycle with live climate data
06_adaptation_guide.ipynb   ← 30 min  adapting for a new Nation
```

Notebook 05 (SEEDS Workflow) is the standalone teaching notebook 
it runs a complete Earth data science analysis of Pine Ridge drought
data while weaving sovereignty checks into every step. It is suitable
for hackathons and workshops without requiring the other notebooks first.

## Validating your config

After editing `config/nation.yaml`:

```bash
python toolkit/governance.py --config config/nation.yaml --validate
```

If validation passes, generate a sovereignty statement:

```bash
python toolkit/governance.py --config config/nation.yaml --statement
```

Or a compliance checklist:

```bash
python toolkit/governance.py --config config/nation.yaml --checklist
```

## The three-line minimum

If you do nothing else, at least do this in every notebook that touches
Indigenous data:

```python
from toolkit.sovereignty import SovereigntyContext
ctx = SovereigntyContext.from_config("config/nation.yaml")
ctx.print_acknowledgment()
```

This tells everyone who opens the notebook whose land the data describes, 
what treaty governs that land, and what frameworks
apply. That is the minimum floor of responsible practice.

## Getting help

**Technical questions:** Open an issue on GitHub.

**Nation-specific configuration assistance:** Contact Daear Consulting, LLC.
Nation-specific work such as integrating Tribal data codes, Local Contexts TK
Labels, custom governance schemas is a consulting engagement.

**Framework questions:**
- OCAP®: https://fnigc.ca/ocap-training/
- CARE: https://www.gida-global.org/care
- FAIR: https://www.go-fair.org/fair-principles/
- IEEE 2890-2025: https://standards.ieee.org/ieee/2890/10318/

