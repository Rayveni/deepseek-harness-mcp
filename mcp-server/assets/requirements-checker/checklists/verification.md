# Operational Verification Checklist — Requirements Checker

Load and confirm every item **before finishing a check run**. This is the
operational checklist referenced from `SKILL.md` step 8.

- [ ] All **10** criteria checked and remarks listed.
- [ ] ID registry built; all IDs resolved or flagged; stub definitions listed separately.
- [ ] Stub sections and placeholders detected; Q-linked placeholders and Q-mismatches classified.
- [ ] Traceability graph checked for broken edges, orphans, goal/child mismatches, semantic gaps, and metric gaps.
- [ ] Requirement levels checked (BR vs FR vs NFR vs AC/TC).
- [ ] MoSCoW coverage checked; deferred items marked explicitly.
- [ ] AC/TC coverage checked; multi-parent AC and AC inheritance recorded.
- [ ] Term consistency, mixed-alphabet tokens, undeclared foreign terms, and canonical GLOSS forms checked.
- [ ] Q quality checked for every open question.
- [ ] No fix applied without user confirmation.
- [ ] Output language matches the source document's language.
- [ ] Relative links (`references/check-criteria.md`, `templates/report.md`) resolve via `get_asset`.
- [ ] Criteria version recorded in the report header (`1.3.0`).

For migration / skill-maintenance verification, use `checklists/migration.md`
instead of this file.