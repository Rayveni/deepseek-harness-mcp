---
name: resource-migrator
description: >-
  Migrates hard-coded resource files (templates, references, checklists,
  examples, schemas) out of a Skill definition and into the `assets`
  MCP provider (`assets/<skill>/<category>/<name>`), then rewrites the
  Skill to load those resources via `get_asset`, `render_asset`,
  `list_assets`, etc. instead of embedding them inline.
  Triggers (en): "migrate resources", "extract skill resources",
  "resource migration", "assets mcp provider". Triggers (ru):
  «миграция ресурсов», «извлечь ресурсы скилла».
---

# Resource Migrator

Migrates embedded skill resources (templates, references, checklists, examples, schemas) to the assets MCP provider and rewrites the skill to load them via MCP.

**When to use:** The user asks to migrate hard-coded templates, references, checklists, examples, or schemas out of a Skill definition so they live in the `assets` MCP provider and are loaded via MCP tools.

## Resources (loaded via assets MCP provider)

All resources previously embedded in `SKILL.md` have been moved to `assets/resource-migrator/<category>/`. Load them exclusively via the MCP tool set:

- `list_skills()` — list skills in assets.
- `list_skill_categories("resource-migrator")` — categories.
- `list_assets("resource-migrator", category="...")` — files.
- `get_asset("resource-migrator", "templates", "migration-plan.md")` — full file.
- `get_asset("resource-migrator", "references", "resource-categories.md", section="Load via")` — section by heading (heading text without `#`).
- `render_asset("resource-migrator", "templates", "migration-plan.md", variables={"skillName":"resource-migrator","templatesCount":"1","referencesCount":"1","checklistsCount":"1","examplesCount":"1","schemasCount":"1"})` — render with variable substitution.
- `unresolved_placeholders(rendered_text)` — verify no leftover `{{...}}`.

### Resource map

| Resource | Asset path | Load method |
|---|---|---|
| Migration plan template (`{{placeholders}}`) | `assets/resource-migrator/templates/migration-plan.md` | `get_asset` or `render_asset` |
| Resource categories reference (5 categories) | `assets/resource-migrator/references/resource-categories.md` | `get_asset` (full or by section) |
| Verification checklist (6 items) | `assets/resource-migrator/checklists/verification.md` | `get_asset` |
| Resource types schema (JSON) | `assets/resource-migrator/schemas/resource-types.json` | `get_asset` |
| Example migrated resource | `assets/resource-migrator/examples/sample-resource.md` | `get_asset` |

### Before applying any load

Confirm unresolved placeholders: call `unresolved_placeholders(text)` after any `render_asset`. If keys remain, resolve or document them.

## Process

### 1. Identify embedded resources in the source skill
- Read the source `SKILL.md` (e.g., `resource-migrator/SKILL.md`).
- Scan for hard-coded content that should be external resources: templates with `{{...}}`, reference tables, checklist lists, example snippets, JSON schemas.

### 2. Create the assets tree
- Create `assets/<skill-name>/` subdirectories: `templates/`, `references/`, `checklists/`, `examples/`, `schemas/` (all 5 categories).
- Copy each resource file from the source skill directory to the matching `assets/` category.
- Write the migrated skill (rewritten `SKILL.md` + remaining `scripts/`) to `<skill-name>_migrated/`.

### 3. Rewrite SKILL.md to load via MCP
- Remove all embedded resource text from the body.
- Replace with references that load via `get_asset(...)` or `render_asset(...)`.
- Add a `§ Resources` section (like this one) mapping each resource to its asset path and MCP load method.
- Use the exact asset path pattern: `assets/<skill>/<category>/<name>`.

### 4. Validate the rewritten skill
- Confirm all resource files exist at their asset paths (`list_assets`).
- Confirm the body uses MCP tool calls, not inline embedded text.
- Check for unresolved placeholders (`unresolved_placeholders`).
- Ensure the skill directory structure includes `SKILL.md` plus any remaining `scripts/` (optional).
- Run `node scripts/validate.mjs .` from the skill root and confirm exit code 0.

## Quality

- Every resource is loaded exclusively via the assets MCP provider (`get_asset` / `render_asset`); no inline hard-coded resource content remains in `SKILL.md`.
- Asset paths match the pattern `assets/<skill>/<category>/<name>` for all 5 categories: `templates`, `references`, `checklists`, `examples`, `schemas`.
- Before applying any rendered template, verify `unresolved_placeholders(text)`. If keys remain, resolve them with `variables` or document them.
- The output folder is `<skill-name>_migrated/` (postfix `_migrated`).

## Assumptions

- [ASSUMPTION] Source skill has hard-coded resources in `templates/`, `references/`, `checklists/`, `examples/`, `schemas/` embedded in `SKILL.md`.
- [ASSUMPTION] Assets provider root is the workspace-local `assets/` directory (`/workspace/research/assets/`).
- [ASSUMPTION] All 5 resource categories (`templates`, `references`, `checklists`, `examples`, `schemas`) are migrated; `examples/` directory is included.
- [ASSUMPTION] `scripts/validate.mjs` exists in the source skill and is run from the skill root.