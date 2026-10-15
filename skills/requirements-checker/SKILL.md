---
name: requirements-checker
description: >-
  Checks collected requirements for Completeness (including stub sections),
  Consistency, ID Integrity (including stub definitions and unreferenced
  informational IDs), Traceability Integrity (including semantic and metric
  gaps), Level Consistency, Unambiguity & Measurability (including placeholder
  tokens, Q-linked placeholders, and Q-mismatches), MoSCoW & AC/TC Coverage
  (including multi-parent AC and AC inheritance), Unified Language & Term
  Consistency (including undeclared foreign terms), and Open Questions quality
  in Russian / English. Proposes corrections; corrections applied only after
  user agreement. Triggers (en): "check requirements", "requirements review",
  "fix requirements". Triggers (ru): «проверь требования», «исправь требования»,
  «проверка полноты».
---

# Requirements Checker

Checks a collected-requirements document against **10 criteria** and produces a remark list with proposed fixes. Fixes are applied only after explicit user confirmation.

**When to use:** the user has a requirements file (e.g. `requirements.md`) and asks for verification.

**Relation to other skills:** self-contained; can optionally consume the output of `requirements-analyzer`, but does not require it.

## Process

Load all runtime resources exclusively via the assets MCP provider:

- `get_asset("requirements-checker", "references", "check-criteria.md")` — criteria reference (10 sections).
- `get_asset("requirements-checker", "references", "resource-categories.md")` — resource categories and load instructions.
- `get_asset("requirements-checker", "templates", "report.md")` — canonical report template.
- `get_asset("requirements-checker", "checklists", "verification.md")` — operational verification checklist.
- `get_asset("requirements-checker", "examples", "sample-resource.md")` — example migrated resource.
- `get_asset("requirements-checker", "schemas", "resource-types.json")` — resource types schema.

Skill-maintenance resources (not part of a normal check run) are listed under **§ Maintenance** at the end of this file.

### 1. Identify the requirements source
- Read the user-provided file (e.g. `requirements.md`).
- Note which languages are present per section (RU only / EN only / mixed).
- Note the declared primary language from the header (e.g. `Основной язык: Russian (RU)`).

### 2. Build the ID registry and traceability graph
- Collect every ID matching `\b[A-Z]+-\d+\b`: `G-*`, `KPI-*`, `BR-*`, `StR-*`, `FR-*`, `NFR-*`, `BRU-*`, `CON-*`, `ASM-*`, `DEP-*`, `INT-*`, `DAT-*`, `RISK-*`, `GLOSS-*`, `US-*`, `AC-*`, `TC-*`, `Q-*`.
- For each ID record: definition line(s), outgoing references, incoming references.
- Apply:
  - **misplaced definition**, **stub definition**, **unreferenced informational** rules (see criteria §2);
  - placeholder / Q-linked placeholder / Q-mismatch classification (see criteria §6);
  - **Q-* ownership** — `Q-*` must live in §Open Questions (see criteria §2 + §10).

### 3. Detect placeholders and stub sections
- Scan for placeholder tokens: `\[[A-ZА-Я]+\]`, `TBD`, `N/A`, `?`, `…` inside requirement bodies.
- Classify each placeholder per `get_asset("requirements-checker", "references", "check-criteria.md", section="6. Однозначность и измеримость (Unambiguity & Measurability)")`.
- Scan section bodies that contain only a reference or a redirect. Mark as **stub sections**.

### 4. Run the 10 checks
Apply criteria loaded via `get_asset("requirements-checker", "references", "check-criteria.md")` in order:

1. **Completeness (Полнота)**
2. **ID Integrity** — includes **stub definition**, **misplaced definition**, **unreferenced informational**, **duplicate ID**, **unknown prefix**, and **orphan ID** rules.
3. **Consistency (Непротиворечивость)**
4. **Traceability Integrity**
5. **Level Consistency**
6. **Unambiguity & Measurability (Однозначность и измеримость)**
7. **MoSCoW Coverage**
8. **AC/TC Coverage**
9. **Unified Language (Единый язык) & Term Consistency**
10. **Open Questions quality (Качество открытых вопросов)** — see step 5 for details.

### 5. Criterion 10 — Open Questions quality (detail)
This step expands item 10 of step 4; it is not a separate 11th check.

For every `Q-XX` verify: owner; blocking artifact; status (`open` / `in progress` / `closed`); date (opened / updated). Report missing fields as `Q quality` remarks per `get_asset("requirements-checker", "references", "check-criteria.md", section="10. Качество открытых вопросов (Open Questions quality)")`.

### 6. Generate remarks list (no writes yet)
- Produce a structured list: criterion, line reference, remark, proposed fix.
- Use the format from `get_asset("requirements-checker", "templates", "report.md")`.
- **Do not apply fixes.** Show the list as a chat message, or write it to a temporary proposal file only if the user pre-authorized the path.

### 7. Request confirmation before applying fixes
- For each proposed correction, ask the user: *"Apply fix for [criterion] at [line]: [proposal]? (yes / no / suggest alternative)"*.
- Apply **only after** an explicit positive confirmation.

### 8. Verification checklist (before finishing)
Load `get_asset("requirements-checker", "checklists", "verification.md")` and confirm every item. The checklist content is not duplicated here; treat the asset as the single source of truth.

For migration / skill-maintenance runs, use `get_asset("requirements-checker", "checklists", "migration.md")` instead (see § Maintenance).

## § Resources

All runtime resources are loaded exclusively via the assets MCP provider (`get_asset` / `render_asset`). No inline hard-coded resource content remains in this `SKILL.md`.

| Resource | Asset path | Load method |
|---|---|---|
| Check criteria reference (10 sections, v1.3.0) | `assets/requirements-checker/references/check-criteria.md` | `get_asset` (full file or by `section="..."`) |
| Resource categories reference | `assets/requirements-checker/references/resource-categories.md` | `get_asset` |
| Report template | `assets/requirements-checker/templates/report.md` | `get_asset`, or `render_asset` with header variables |
| Operational verification checklist | `assets/requirements-checker/checklists/verification.md` | `get_asset` |
| Example migrated resource | `assets/requirements-checker/examples/sample-resource.md` | `get_asset` |
| Resource types schema (JSON) | `assets/requirements-checker/schemas/resource-types.json` | `get_asset` |

Asset path pattern: `assets/requirements-checker/<category>/<name>` for all 5 categories: `templates`, `references`, `checklists`, `examples`, `schemas`.

`templates/report.md` uses `{{...}}` **only in the header block** for `render_asset` (keys: `{{date_time}}`, `{{source_file}}`, `{{checker}}`, `{{criteria_version}}`). Body fill-markers use `[list]`-style text and are filled manually. Before applying any `render_asset` result, call `unresolved_placeholders(text)` to confirm no leftover `{{...}}` keys remain.

## § Maintenance

Skill-maintenance resources are **not** loaded during a normal check run.

| Resource | Asset path | Load method |
|---|---|---|
| Migration verification checklist | `assets/requirements-checker/checklists/migration.md` | `get_asset` |

Use `checklists/migration.md` only when verifying the migration of this skill from inline `SKILL.md` content to `assets/requirements-checker/<category>/`.

## Quality

- Every remark references the exact line / file section.
- Every proposed fix is a concrete edit, not a vague suggestion.
- No file is modified without explicit user agreement.
- Before publishing changes to this skill, run: `node scripts/validate.js .`

## Assumptions

- [ASSUMPTION] Default source-document language is Russian; if the source is English, output switches accordingly.
- [ASSUMPTION] `templates/report.md` is the canonical report shape; deviations must be justified in the report itself.
- [ASSUMPTION] If the source mixes RU/EN without marking a section bilingual, it is treated as a language issue, not as a deliberate choice.
- [ASSUMPTION] Placeholders `[X]`, `[Y]`, `[N]` are blockers only if the document is intended for finalization; in a draft they are reported as `Placeholder` or `Q-linked placeholder` remarks, not as hard failures.
- [ASSUMPTION] Semantic coverage of a parent by a child is judged by subject matter keywords; metric coverage is judged by numeric thresholds and units.
- [ASSUMPTION] AC inherit the MoSCoW priority of their parent; direct MoSCoW on AC is not required.
- [ASSUMPTION] A `Q-XX` without an explicit `status` is treated as `open`.