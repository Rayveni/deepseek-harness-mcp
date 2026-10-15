# Migration Verification Checklist — Requirements Checker

Use this checklist **only** when verifying the migration of this skill from
inline `SKILL.md` content to `assets/requirements-checker/<category>/`. It is
not part of a normal check run.

- [ ] All 5 categories (templates, references, checklists, examples, schemas) copied to `assets/requirements-checker/`
- [ ] `SKILL.md` rewritten to load via `get_asset` / `render_asset`
- [ ] No inline embedded resource text remains in `SKILL.md`
- [ ] Asset paths match `assets/requirements-checker/<category>/<name>`
- [ ] `unresolved_placeholders` checked after any render
- [ ] `scripts/validate.js .` exits with code 0
- [ ] Migrated skill directory: `requirements-checker_migrated/`

## Notes

- Runtime asset path is `assets/requirements-checker/<category>/<name>`.
- During migration the working directory MAY be `requirements-checker_migrated/`;
  the path above is resolved relative to the skill root.
- `checklists/verification.md` is the **operational** checklist and MUST NOT
  contain migration-only items.