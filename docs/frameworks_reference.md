# Governance Frameworks Reference
## Tribal Data Sovereignty Toolkit

## Overview Why Four Frameworks?

A common question: why four frameworks? Isn't one enough?

Each framework addresses a different dimension of the problem:

| Framework | Core question it answers |
|---|---|
| **OCAP®** | *Who has rights over this data?* |
| **CARE** | *What are the ethical obligations of using it?* |
| **FAIR** | *How should it be technically managed?* |
| **IEEE 2890-2025** | *How do we document that we got this right?* |

A dataset can be fully FAIR while completely violating OCAP® and CARE.
FAIR says nothing about whether a community consented to their data
being collected, who owns it, or who benefits from its use.

Conversely, good intentions (CARE compliance) without technical
documentation (IEEE 2890-2025 provenance) are not enough to ensure
that sovereignty is actually exercised as data moves through systems,
institutions, and time.

The four-framework stack is the minimum coherent set.

## OCAP®: Ownership, Control, Access, Possession

**Developed by:** First Nations Information Governance Centre (FNIGC)  
**Primary context:** First Nations in Canada; widely adopted internationally  
**Reference:** https://fnigc.ca/ocap-training/

### Ownership

A community or group owns information collectively in the same way that
an individual owns their personal information, which has practical consequences 
for who may publish, share, sell, or otherwise use data.

**What ownership means in practice:**
- Tribal-collected field data is owned by the Nation, not the researcher
- Federal data collected about Tribal territory carries a moral ownership
  claim even when legal ownership is ambiguous or contested
- Publications about Tribal land and communities should credit the Nation
- Data governance agreements should explicitly assign ownership

**What ownership does not mean:**
- The Nation controls every individual's personal data
- Researchers cannot ever use data about Tribal territory
- Data ownership requires physical possession (though possession is
  important: see below)

### Control

The rights of First Nations peoples and their representative bodies to
control data collection processes in their communities. Control is the right
to participate meaningfully in decisions that affect the community.

**What control means in practice:**
- Tribal governance body approves research protocols before fieldwork
- The Nation can halt, pause, or redirect data collection
- Research questions and methods reflect community priorities
- The Nation reviews findings before external publication
- Publications require Tribal authorization

**Common failures of control:**
- Researcher obtains individual consent without community-level approval
- Findings are published before the Nation reviews them
- The Nation is consulted but not in a position to meaningfully influence
  the research

### Access

First Nations peoples must have access to data about themselves and their
communities, regardless of where that data is held. This applies to
historical data collected by federal agencies decades ago as much as
to current research.

**What access means in practice:**
- All data and findings are returned to the Nation in usable formats
- Community members can request access to data about their territory
- Technical outputs include plain-language summaries
- The Nation is not dependent on a researcher or agency to access their
  own information

**Access and classification:** Access does not mean all data should be
publicly accessible. The Nation controls who has access (Control), and
Access ensures the Nation itself always has it.

### Possession

The mechanism through which ownership can be asserted and protected.
A community cannot exercise ownership or control if they do not physically
hold a copy of the data. This is particularly important when the research
relationship ends.

**What possession means in practice:**
- The Nation holds a complete copy of all data before the project ends
- Tribal-collected data is stored on Tribal-controlled systems
- Data is gitignored and not uploaded to researcher's cloud without consent
- Governance agreements specify what happens to data after the project


## CARE: Collective Benefit, Authority to Control, Responsibility, Ethics

**Developed by:** Global Indigenous Data Alliance (GIDA)  
**Reference:** https://www.gida-global.org/care  
**Published in:** Data Science Journal (2020)

CARE was developed specifically to complement FAIR. FAIR addresses how
data should be technically managed. CARE addresses the ethical obligations
to the communities whose data is being managed.

### Collective Benefit

Data ecosystems must be designed and function in ways that enable
Indigenous peoples to derive benefit from the data. This is
specifically about benefit to the community the data describes.

**Operationalizing collective benefit:**
- Define specific community benefits before the project starts
- Ensure findings are communicated to the community in accessible form
- Create outputs that serve community decision-making
- Ask: does this analysis answer a question the community cares about?

**Failures of collective benefit:**
- Research that serves researcher career advancement without community use
- Findings published only in paywalled journals the community cannot access
- "Benefit" defined entirely by the research team without community input

### Authority to Control

Indigenous peoples' rights and interests in Indigenous data must be
recognized and their authority to control such data must be empowered.
This is ongoing governance.

**Operationalizing authority:**
- Formal data governance agreements that specify decision rights
- Mechanisms for the Nation to update, revoke, or modify data permissions
- Nation representation in research governance structures
- Regular reporting back to the Nation throughout the project

### Responsibility

Those working with Indigenous data have a responsibility to share how
data is used and to support the capacity of Indigenous peoples to govern
their own data. This includes capacity-building as a research deliverable.

**Operationalizing responsibility:**
- Document and share all analysis code and methods
- Train community members in the analytical methods used
- Ensure the Nation can reproduce and audit the analysis
- Be transparent about limitations and uncertainties

### Ethics

Indigenous peoples' rights and wellbeing should be the primary concern
at all stages of the data lifecycle from design, generation, analysis, and
dissemination. Ethics is an ongoing orientation.

**Operationalizing ethics:**
- Consider potential harms before publishing any finding
- Review maps for sensitive location disclosure
- Ask whether the analysis could be used in ways that harm the community
- Document ethical considerations alongside technical methods


## FAIR: Findable, Accessible, Interoperable, Reusable

**Developed by:** GO FAIR Initiative  
**Reference:** https://www.go-fair.org/fair-principles/  
**Published in:** Scientific Data (2016)

FAIR governs technical data management. It emerged from scientific data
infrastructure concerns and addresses how to make data usable across
institutions and over time. FAIR applies to the data that is meant to
be shared while OCAP® and CARE determine what should be shared.

### Findable

Data and metadata should be easy to find for both humans and computers.

**Key elements:**
- Persistent identifier (DOI, accession number)
- Rich metadata registered in a searchable resource
- Metadata includes the identifier for the data

**For Indigenous data:** Metadata should include territorial and treaty
provenance. A dataset described only by its technical characteristics
(geographic extent, date range) without identifying whose land it
describes is not adequately documented.

### Accessible

Once found, data should be accessible through standardized, open protocols.
Importantly: "accessible" does not mean "publicly open." Authentication
and authorization are permitted but what matters is that the protocol is
standard and the access conditions are clearly defined.

**For Indigenous data:** Some data should be accessible only to Tribal
members or authorized partners. This is FAIR-compliant as long as the
access conditions are clearly documented and the mechanism is standard.

### Interoperable

Data should use standardized formats and vocabularies so it can be
integrated with other data and processed by standard tools.

**Primary elements:**
- Use established file formats (GeoJSON, CSV, NetCDF, GDB)
- Use controlled vocabularies and ontologies where applicable
- Include qualified references to other data

### Reusable

Data should be well-described enough that it can be replicated and
combined in different settings.

**Primary elements:**
- Clear, accessible license
- Rich provenance documentation
- Meets domain-relevant community standards

**For Indigenous data:** The license should reflect OCAP® and CARE
constraints. A standard open license (CC0, CC-BY) may be appropriate
for public data but is insufficient for data with governance obligations.
The license should specify what additional permissions are required.

## IEEE 2890-2025

**Full title:** IEEE 2890-2025 Recommended Practice for Provenance of
Indigenous Peoples' Data  
**Status:** Active standard (approved 2025)  
**Reference:** https://standards.ieee.org/ieee/2890/10318/

### What it is

IEEE 2890-2025 is the first international technical standard specifically
for Indigenous data. It establishes that provenance records for Indigenous
data must document not only technical lineage (the standard W3C PROV
elements with entity, agent, activity) but also governance lineage.

### Governance lineage requirements

IEEE 2890-2025 requires that provenance records for Indigenous data include:

- **Nation identification**: which Indigenous Nation's territory or
  people does the data describe?
- **Territorial citation**: what is the specific territory, treaty
  basis, and treaty status?
- **Stewardship identification**: which Tribal governance body or
  department is responsible for stewarding this data?
- **Governance framework documentation**: which frameworks apply
  (OCAP®, CARE, FAIR, Local Contexts, etc.)?
- **Classification**: what is the data classification tier?

### Why it matters

Without IEEE 2890-2025, provenance records for Indigenous data look the
same as provenance records for any other data. They document technical
lineage but carry no information about governance obligations. Data can
be copied, processed, and republished without any indication that it
describes Indigenous territory or carries sovereignty obligations.

IEEE 2890-2025 makes governance machine-readable and it can be processed
by data systems, searched, and enforced programmatically.

### Implementation in this toolkit

The `toolkit/provenance.py` module implements IEEE 2890-2025 through
the `ProvenanceRecord` dataclass and `ProvenanceBuilder` fluent interface.
Every provenance record produced by the toolkit includes all required
governance lineage fields alongside the technical provenance fields.

## Framework Relationships

```
OCAP®          ──── Who has rights?
                          │
                          
CARE           ──── What are the obligations?
                          │
                          
FAIR           ──── How is it technically managed?
                          │
                          
IEEE 2890-2025 ──── How do we document it?
```

These frameworks address different layers of the same problem. 
A complete governance approach requires all four.

## A Note on Local Contexts

[Local Contexts](https://localcontexts.org/) provides Traditional Knowledge
(TK) Labels and Notices that complement OCAP® and CARE by communicating
cultural protocols around specific types of knowledge such as seasonal knowledge,
sacred knowledge, gender-restricted knowledge, and others.

Local Contexts is supported in this toolkit through the `local_contexts`
flag in `nation_template.yaml`. It is disabled by default because TK
Label selection is Nation-specific and requires engagement with the Local
Contexts Hub. Nations interested in TK Labels should contact Local Contexts
directly (https://localcontexts.org) and then contact Daear Consulting for toolkit integration support.
