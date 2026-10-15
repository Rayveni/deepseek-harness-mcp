# Requirements Check Report Template

Copy this template and fill per check run. **Do not modify the source file.**

---
Check run:        {{date_time}}
Source file:      {{source_file}}
Checker:          {{checker}}
Criteria version: {{criteria_version}}
---

> `render_asset` replaces the four header keys only:
> `{{date_time}}`, `{{source_file}}`, `{{checker}}`, `{{criteria_version}}`.
> Body fill-markers below use `[list]` / `[ref]` style and are filled manually.
> `checker` is normally `requirements-checker`; `criteria_version` is `1.3.0`.

## 1. Полнота / Completeness
- Missing sections: [list]
- Empty sections:   [list]
- Stub sections:    [list]
- Proposals:        [add sections / confirm out of scope]

## 2. Целостность ID / ID Integrity
- Undefined IDs:             [list]
- Stub definitions:          [list]
- Duplicate IDs:             [list]
- Misplaced definitions:     [list]
- Orphan IDs:                [list]
- Unreferenced informational:[list]
- Unknown prefixes:          [list]
- Referenced-but-missing IDs:[list]

## 3. Непротиворечивость / Consistency
- Conflicts found: [count]
- Details:
  - Line [ref]: [section A] vs [section B] → proposal: [fix]

## 4. Целостность трассировки / Traceability Integrity
- Broken edges:        [list]
- Goal mismatches:     [list]
- Semantic gaps:       [list]
- Metric gaps:         [list]
- Missing AC:          [list]
- Missing TC:          [list]
- Orphan AC:           [list]
- Matrix mismatches:   [list]

## 5. Согласованность уровней / Level Consistency
- AC/TC embedded in wrong level: [list]
- BR at solution level:          [list]
- Invalid MoSCoW placeholders:   [list]
- Misplaced prioritization:      [list]
- Misplaced definitions:         [list]

## 6. Однозначность и измеримость / Unambiguity & Measurability
- Unambiguous issues:      [count]
- Unmeasurable issues:     [count]
- Placeholders:            [list]
- Q-linked placeholders:   [list]
- Q-mismatches:            [list]
- Details:
  - Line [ref]: [vague phrase] → proposal: [quantified version]
  - Line [ref]: [placeholder] → proposal: [concrete value or Q-XX link]

## 7. Покрытие MoSCoW / MoSCoW Coverage
- Missing MoSCoW:      [list]
- Deferred MoSCoW:     [list]
- Invalid MoSCoW:      [list]
- Misplaced MoSCoW:    [list]
- MoSCoW ref errors:   [list]

## 8. Покрытие AC/TC / AC/TC Coverage
- Missing AC:       [list]
- Missing TC:       [list]
- Non-GWT AC:       [list]
- Multi-AC TC:      [list]
- Multi-parent AC:  [list]
- AC inheritance:   [list]
- Semantic gaps:    [list]
- Metric gaps:      [list]

## 9. Единый язык и термины / Unified Language & Term Consistency
- Primary language:                [RU / EN / Mixed]
- Mixed-language sections:         [list]
- Mixed-alphabet tokens:           [list]
- Inconsistent translated terms:   [list]
- GLOSS term inconsistencies:      [list]
- Undeclared foreign terms:        [list]
- Transliteration inconsistencies: [list]

## 10. Качество открытых вопросов / Open Questions quality
- Q quality issues:                  [list]
- Items that could not be verified:  [list]
- Assumptions made during the check: [list]
- Questions for the user:            [list]

---

## Fix Proposals (apply ONLY after user confirmation)

| Line | Criterion | Remark | Proposed Fix | Status |
|------|-----------|--------|--------------|--------|
| ...  | ...       | ...    | ...          | PENDING user confirmation |

*Do not apply any row until the user confirms: "Apply fix at line X: [proposal]".*