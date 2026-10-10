# Soils and geology governance exercise

This is a teaching workflow, not a finding about any Nation. Define the project
question and designated authority using `Forms/project_brief.md`.

1. Verify SSURGO and geological data retrieval success, query bounds, time coverage, filters,
   pagination, and source metadata. Save the exact query and retrieval date.
2. Distinguish an empty or failed response from absence of observations. A
   successful empty query alone does not establish a monitoring or investment gap.
3. Evaluate spatial coverage against the question. Compare like-for-like areas,
   periods, variables, and denominators before making a disparity claim.
4. Document uncertainty, source limitations, and alternative explanations.
   A policy or investment conclusion needs additional evidence and community review.
5. Create provenance with explicit access classification, approved storage,
   version-control rules, and pending publication status. Review derived products
   even when inputs are public.
6. Use `SovereigntyAudit(..., frameworks=ctx.config.active_frameworks)` and record
   evidence for each answer. Scores do not establish approval.
7. Return a draft in an accessible format and record actual review and receipt
   evidence before claiming the return is complete.

## Diagnostic record

| Item | Record |
|---|---|
| Retrieval status | [success / failure / partial] |
| Query and source | [Exact request and metadata] |
| Returned coverage | [Spatial, temporal, variables, missingness] |
| Comparison design | [Comparable period and denominator] |
| Claim supported | [Observation only until evidence supports more] |
| Alternative explanations | [Filters, retrieval problems, coverage limits] |
| Reviewer / date / evidence | [Complete] |

Use lesson 05 for a fully offline analysis with coverage diagnostics. For an
actual project, replace the synthetic source and obtain the applicable review.
