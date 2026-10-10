# Framework reference and implementation limits

The Nation determines applicable policies and frameworks. A software setting
records a choice; it does not establish adoption, consent, or authority.

| Framework | Primary reference | Toolkit treatment |
|---|---|---|
| OCAP® | https://fnigc.ca/ocap-training/ | First Nations-specific; opt in only after applicability is established |
| CARE | https://www.gida-global.org/care | Questions about benefit, authority, responsibility, and ethics |
| FAIR | https://www.go-fair.org/fair-principles/ | Metadata, identifiers, interoperability, and documented use terms |
| IEEE 2890-2025 | https://standards.ieee.org/ieee/2890/10318/ | Recommended Practice for Provenance of Indigenous Peoples' Data |
| Local Contexts | https://localcontexts.org/ | Nation-led manual review; not scored by the audit |

OCAP® is a registered trademark of the First Nations Information Governance
Centre (FNIGC). OCAP principles must not be assumed to apply to every Indigenous
Nation. Restricted data can be FAIR: A1.2 permits authentication and authorization.
Metadata disclosure also needs review where it could reveal sensitive information.

## Conceptual crosswalk, not a conformance claim

The following maps toolkit concepts, not verified IEEE clauses. The full standard
has not been assessed clause by clause for this implementation. JSON exports use
`idsov-toolkit-provenance-v2`; they are not asserted to be an IEEE or W3C serialization.

| Concept | Toolkit fields / evidence | Limitation |
|---|---|---|
| Dataset identity | record_id, dataset_name | Project IDs need uniqueness checks |
| Source lineage | data_source_url, derived_from, processing_steps | Source claims still require verification |
| Responsible people and organizations | data_steward, stewardship_dept, analyst_name | Names do not establish authority |
| Territory and applicable authority | nation_name, territory_name, treaty_status, optional treaty_reference | Nation review required; no universal treaty requirement |
| Access and handling | classification, approved_storage, version_control | Metadata records policy; it does not enforce storage access |
| Publication decision | publication_status, approval_evidence, approval_reviewer, approval_date | Evidence must be checked by an authorized reviewer |

Before making a conformance claim, review the full recommended practice, map
each applicable requirement to implementation and evidence, identify omissions,
and record the reviewer's conclusions. The question IDs prefixed IEEE are local
review prompts, not official clause identifiers.
