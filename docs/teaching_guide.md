# Teaching guide

Use the fictional Example River Nation case through all seven lessons. Its
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
