# Resource Categories — Requirements Checker

All resources migrated from hard-coded `SKILL.md` content to `assets/requirements-checker/<category>/`.

## Load via

- `get_asset("requirements-checker", "templates", "report.md")`
- `get_asset("requirements-checker", "references", "check-criteria.md")`
- `get_asset("requirements-checker", "references", "check-criteria.md", section="1. Полнота (Completeness)")`
- `get_asset("requirements-checker", "references", "check-criteria.md", section="6. Однозначность и измеримость (Unambiguity & Measurability)")`
- `get_asset("requirements-checker", "references", "check-criteria.md", section="10. Качество открытых вопросов (Open Questions quality)")`
- `render_asset("requirements-checker", "templates", "report.md", variables={date_time, source_file, checker, criteria_version})`
- `list_assets("requirements-checker", category="...")`

## Section selectors

`section="..."` MUST be the **full heading text** as it appears in
`check-criteria.md`, including the RU/EN parenthetical, e.g.:

- `"1. Полнота (Completeness)"`
- `"6. Однозначность и измеримость (Unambiguity & Measurability)"`
- `"10. Качество открытых вопросов (Open Questions quality)"`

Partial or truncated headings are not supported.

## `render_asset` scope for `templates/report.md`

Only the header block uses `{{...}}` placeholders. The four supported keys are:

- `{{date_time}}`
- `{{source_file}}`
- `{{checker}}`
- `{{criteria_version}}`

Body fill-markers (`[list]`, `[ref]`, etc.) are filled manually and are **not**
`{{...}}` placeholders — `unresolved_placeholders(text)` will not flag them.