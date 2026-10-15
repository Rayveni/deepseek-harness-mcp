# Resource Categories Reference

The assets MCP provider (`assets/<skill>/<category>/<name>`) supports these categories for migrated skill resources:

| Category | Purpose | Example asset path |
|---|---|---|
| `templates` | Fill-in templates (`{{placeholders}}`) | `assets/resource-migrator/templates/migration-plan.md` |
| `references` | Long supporting docs, criteria, guides | `assets/resource-migrator/references/resource-categories.md` |
| `checklists` | Verification / quality checklists | `assets/resource-migrator/checklists/verification.md` |
| `examples` | Worked examples | `assets/resource-migrator/examples/sample-resource.md` |
| `schemas` | Structured data (JSON, YAML) | `assets/resource-migrator/schemas/resource-types.json` |

## Load via

Use `get_asset(skill, category, name, section=...)` to read a full file or a section by heading, and `render_asset(skill, category, name, variables={...})` to substitute `{{placeholders}}`.