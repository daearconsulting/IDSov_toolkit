# Teaching guide

Use the fictional Example River Nation case through the seven core lessons and five applied labs. Its
observations, roles, and project claims do not describe an actual Nation.

| Lesson | Deliverable | Discussion check |
|---|---|---|
| 00 | Project brief | Who determines the question and benefit? |
| 01 | Applicability matrix | Can restricted data be FAIR? |
| 02 | Provenance catalog | Does public input guarantee public output? |
| 03 | Assessment and remediation | Can a score substitute for approval? |
| 04 | Collection protocol | Who controls storage, transfer, and retention? |
| 05 | Analysis and draft brief | What do missingness and geography limit? |
| 06 | Handoff manifest | What remains after technical validation? |
| 07 CARE | Action register, reuse decisions, benefit delivery plan | Who defines benefit and resolves a change of purpose? |
| 08 FAIR | Data dictionary, discovery metadata, gap report, tombstone | What makes controlled access usable and metadata safe to disclose? |
| 09 Local Contexts | Consultation worksheet, integration manifest, update log | Who can issue a Label, and how does a Notice differ? |
| 10 IEEE | Linked catalog, integrity manifest, standard review worksheet | What evidence is missing before a conformance claim? |
| 11 OCAP® | Responsibility matrix, custody inventory, revocation plan | Who controls primary data, derivatives, keys, and backups? |

## Facilitation and assessment

Begin with the proposed question. Ask learners to explain each decision before
running its cell. Use the Markdown forms for participants who do not code.
Pair technical and practitioner perspectives without assigning authority based
on technical skill. Do not ask participants to bring restricted data or reveal
cultural knowledge to complete exercises.

Assess whether learners can: identify the decision authority; distinguish a
draft from evidence; explain an analysis limitation; trace a source and derived
record; and assign unresolved work. Code execution alone is not completion.

For lesson 03, create a fictional evidence packet with a proposed benefit plan,
a draft storage policy, and an unsigned sharing request. These support partial
or no responses, not claims of actual authorization. An instructor may add a
clearly fictional signed approval to discuss scope and revocation.

Expected discussion points: restricted FAIR access is possible; derived products
need new review; an incomplete assessment has no overall score; a complete score
never overrides missing approval; the synthetic 1992 and 2024 years are excluded;
and a valid configuration is not substantive governance approval.

## Accessibility and reproducibility

Instructions and decisions are available as text. Charts label units, periods,
and source and have CSV/Markdown companions. The offline fixture avoids network
dependencies. Run each notebook independently with a fresh kernel. Set
`IDSOV_CONFIG=config/teaching_example.yaml` for repeatable classroom checks.

## Facilitating the applied labs

Allow 60–90 minutes per lab, including discussion and independent work. Run in
any order after orientation; lessons 01–04 provide useful grounding. All five
explicitly select `config/teaching_example.yaml` and run offline with standard
Python and existing toolkit dependencies. Outputs are draft teaching artifacts,
not decisions about the working Nation. Do not substitute real sensitive records
into the exercises. The labs do not change framework applicability settings.

Ask learners to edit inputs and rerun the affected cells, inspect the saved files,
and explain why a failed case failed. Retain their decision memo alongside the
artifacts. For non-coders, use exported CSV/JSON as worksheets and discuss the
same independent tasks. Add these artifacts to the lesson 06 handoff where useful.

Expected evidence of learning:

- 07: New commercial or model-training purposes remain held; each CARE action
  names a role, evidence need, and review trigger; benefit delivery is measurable.
- 08: Internal fields do not appear in discovery metadata; local identifiers and
  files are distinguished from persistent identifiers, cataloging, and deployed
  access; missing observations have an explicit treatment.
- 09: Communities issue customized Labels; researchers/institutions use Notices.
  No official Label is fabricated. Integration gaps and cached updates are tracked.
- 10: Duplicate IDs, unresolved parents, and cycles are detected; a hash is
  distinguished from source authenticity; full-standard mapping stays unassessed
  without the standard and authorized review.
- 11: First Nations applicability is explicit; community access, custody, keys,
  backups, and derivatives are addressed; planned revocation is not reported as
  verified deletion.

Assess reasoning and evidence quality rather than counting populated fields.
The functions model local teaching rules and do not implement permissions,
certify a framework, or establish an actual governance relationship.
