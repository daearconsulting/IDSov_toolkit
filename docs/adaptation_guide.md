# Adaptation guide

1. Copy `config/nation_template.yaml` to `config/nation.yaml`. The template is
   intentionally incomplete. Keep the fictional teaching files separate.
2. Resolve identity, territory, designated steward, policy/authority, attribution,
   framework applicability, access tiers, and handling fields with the Nation.
   A treaty citation is optional where not applicable.
3. Select applicable frameworks. OCAP is opt-in, not universally applicable.
   Document selections in `Forms/framework_applicability.md`.
4. For live NOAA work, set state code, division IDs, start year, and a reviewed
   spatial rationale. Verify the chosen geography against source metadata.
5. Run `python -m toolkit.governance --config config/nation.yaml --validate`.
   Validation checks structure and placeholders, not substantive approval.
6. Review generated statements, records, and agreements. Record evidence,
   reviewer, and date in `Forms/evidence_and_approvals.md`.
7. Complete `Forms/stewardship_handoff.md` and assign remaining work.

All notebooks use `toolkit.teaching.load_context`: explicit path > `IDSOV_CONFIG`
> `config/nation.yaml` > `config/teaching_example.yaml`. Invalid selected files
fail instead of silently switching Nations. Relative explicit paths resolve
against the repository root. The fallback is always visibly fictional.

Twenty to thirty minutes may suffice for entering previously agreed configuration
values. Governance review and authorization have their own timelines. Nation
staff can lead adaptation; consulting or technical assistance is optional.

## Changing access tiers

Use access tiers that match Nation policy and update lesson `.classify("PUBLIC")`
and `classification="PUBLIC"` inputs to an appropriate configured tier. Unsupported
tiers fail validation. `GITIGNORED` is no longer an access tier. Migrate it to a
Nation-selected sensitivity tier plus explicit approved storage and version-control
rules. Existing configs containing that tier raise a migration error.

Source registration is in-memory. Put project-specific `register_source` calls in
shared project setup and execute them for each new context. Do not assume YAML
edits rewrite existing outputs; regenerate and review them.

## Safe adaptation check

`config/teaching_second_nation.yaml` changes identity, territory, framework selection,
and live-data division configuration without any real Nation claims. Tests verify
that these values propagate. Offline synthetic divisions remain fixture identifiers
and are deliberately independent of real geography.
