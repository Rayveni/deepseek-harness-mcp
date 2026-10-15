# Check Criteria — Requirements Checker

> **Bilingual reference.** Section headings are intentionally RU/EN
> (e.g. "Полнота (Completeness)"). Within each section, the primary
> language of the checked requirements document MUST be respected;
> this reference document itself is the only file where RU/EN mix is allowed.

Reference document for the **10 checks** performed by `requirements-checker`.
Criteria version: **1.3.0**.

## 1. Полнота (Completeness)

Required sections for a full requirements spec:

- Context & Boundaries (In-Scope / Out-of-Scope)
- Stakeholders (StR-*)
- Goals & KPI (G-*, KPI-*)
- Business Requirements (**BR** — business goals at problem level)
- Stakeholder Requirements (StR)
- Functional Requirements (FR)
- Non-Functional Requirements (NFR) with metric
- Business Rules (**BRU** — operational rules; NOT the same as BR)
- Constraints (CON)
- Dependencies (DEP)
- Interfaces & Integrations (INT)
- Data Requirements (DAT)
- Acceptance Criteria (AC) — Given-When-Then
- Traceability Matrix
- MoSCoW Prioritization
- Open Questions
- Assumptions / Confirmations

An **empty section** (heading present, no content) counts as **missing**.
A **stub section** (body contains only a redirect or reference, e.g.
`(см. выше …)`, `(see above …)`, `TBD`, `TODO`) also counts as **missing**.

If any required section is missing → remark: `Missing section: [name]`.
If a section exists but is empty → remark: `Empty section: [name]`.
If a section exists but contains only a stub reference → remark:
`Stub section: [name] — contains only a reference, no content.`

## 2. Целостность ID (ID Integrity)

Rules:

- Every token matching `\b[A-Z]+-\d+\b` must be **defined exactly once**.
- Every reference to an ID must resolve to a definition.
- IDs must be unique across the document.
- IDs must belong to a known prefix: `G`, `KPI`, `BR`, `StR`, `FR`, `NFR`, `BRU`, `CON`, `ASM`, `DEP`, `INT`, `DAT`, `RISK`, `GLOSS`, `US`, `AC`, `TC`, `Q`.
- An ID must be defined in the section that **owns** its prefix (e.g. `BRU-*` in §Business Rules, not in §BR; `AC-*` in §Acceptance Criteria, not embedded inside FR/NFR; `Q-*` in §Open Questions).
- Cross-section redefinition and stub redefinition count as duplicates.

### Stub definitions

- A definition whose body is a placeholder (e.g. `[ТРЕБУЕТ ОПРЕДЕЛЕНИЯ …]`,
  `[TBD]`, `[определение отсутствует …]`) is a **stub definition**.
- A stub definition counts as **defined** for §2 ID resolution, but is
  reported as `Stub definition: [ID] at line [ref] — body is a placeholder.`
- A stub definition also appears in §6 as `Placeholder` or `Q-linked placeholder`.

### Informational IDs

- An ID that is defined and referenced only inside its own section (e.g.
  `DAT-01`, `INT-01`) may be legitimate. If the document declares it as
  informational, do not report as `Orphan ID`; report as
  `Unreferenced informational: [ID] at line [ref] — no inbound/outbound edges.`

Remark format:

- `Undefined ID: [ID] referenced at line [ref], no definition.`
- `Stub definition: [FR-02] at line [ref] — body is a placeholder.`
- `Duplicate ID: [ID] defined at line [ref A] and line [ref B] — including cross-section redefinition and stub redefinition.`
- `Misplaced definition: [ID] defined in section [X] but belongs to section [Y] (line [ref]).`
- `Orphan ID: [ID] defined at line [ref] but never referenced.`
- `Unreferenced informational: [ID] at line [ref] — no inbound/outbound edges; if intentional, mark as informational.`
- `Unknown prefix: [ID] at line [ref] — not in the allowed list.`
- `Referenced-but-missing ID: [FR-02], [AC-02], [TC-01].`

Notes:

- A reference inside a heading, table, or inline `Связь:` field counts as a reference.
- A definition may be a bullet, a heading, or a table row; detect all three.

## 3. Непротиворечивость (Consistency)

Cross-check rules:

- Each **BR** (Business Requirement) must be supported by at least one FR and one AC.
- MoSCoW MUST items must include core BR, FR, NFR and their AC (inherited, per §8).
- Numeric claims (customer count, time limits, budget) must not contradict between Context, Goals, FR, NFR.
- Constraint IDs referenced in Scope must match the Constraints section.

Contradiction format:
`Conflict: [section A] claims X; [section B] claims Y (line [ref]).`

## 4. Целостность трассировки (Traceability Integrity)

Rules:

- Every **BR** must have ≥1 outgoing FR edge and ≥1 outgoing AC edge.
- Every **FR** must have ≥1 AC.
- Every **NFR** must have ≥1 AC.
- Every **AC** must have ≥1 incoming edge from FR / NFR / BR.
- Every **TC** must have ≥1 incoming edge from an AC.
- Each traceability edge must be goal-consistent: the child’s `Цель:` must equal the parent’s ID (or the parent must be explicitly marked as multi-goal).
- Explicit traceability arrows (`→`) and inline “Связь:” fields must agree.
- **Semantic coverage:** an edge `[parent] → [child]` is valid only if the child’s **subject matter** addresses the parent’s subject matter. Formal linking alone is not enough.
- **Metric coverage:** the AC’s metric must cover the parent’s metric. If the parent declares `≤ 3 min` and the AC checks `≥ 90% taste`, that is a metric gap, not just a semantic gap.

Remark format:

- `Broken edge: [parent] → [child] (line [ref]) — [child] is undefined.`
- `Goal mismatch: [child] declares Цель: [X] but is traced to [Y] (line [ref]).`
- `Missing AC: [BR-01] has no AC.`
- `Missing TC: [AC-02] has no TC.`
- `Orphan AC: [AC-03] defined but not traced to any FR/NFR/BR.`
- `Traceability mismatch: line [ref] says [X] but matrix says [Y].`
- `Semantic gap: [AC-01] traced to [NFR-01] but addresses taste/appearance, not SanPiN (line [ref]).`
- `Metric gap: [AC-01] checks “≥ 90% taste”, but parent [FR-01] declares “50–100 шт/день” (line [ref]).`

## 5. Согласованность уровней (Level Consistency)

Rules:

- **AC** and **TC** are separate entities; they MUST NOT be embedded as fields inside BR / FR / NFR definitions.
- **BR** describe problem-level business goals; they must not encode solution details (specific equipment, specific UI).
- **FR** describe system/process behavior; they must be verifiable.
- **NFR** MUST always carry a metric (see §6).
- **CON / DEP / ASM / RISK / GLOSS / INT / DAT** are not prioritizable by MoSCoW unless the document explicitly declares otherwise.
- **US** belong to the user-story layer and must not double as FR.
- **BRU** must be defined in §Business Rules; a redirect from another section does not satisfy this.

Remark format:

- `Level mix: [BR-01] embeds AC/TC fields — move to separate AC/TC entities (line [ref]).`
- `Level mix: [NFR-01] embeds AC — extract as AC-* (line [ref]).`
- `BR at solution level: [BR-01] mentions solution artifact “[…]” (line [ref]).`
- `Invalid MoSCoW: [BRU-01] has placeholder “M/S/C/W” (line [ref]).`
- `Unprioritizable: [CON-01] carries MoSCoW but is a constraint (line [ref]).`
- `Level mix: [BRU-01] defined in §BR; move to §Business Rules (line [ref]).`

## 6. Однозначность и измеримость (Unambiguity & Measurability)

Every requirement must pass both tests:

- **Unambiguous** — no undefined terms; each actor / action / object is named.
- **Measurable** — a metric, threshold, or clear pass/fail condition is present.

### Vague words to flag (require quantification)

- RU: «быстро», «удобно», «хорошо», «достаточно», «часто», «скоро», «много», «мало», «надлежащее», «минимальные», «свежими», «свежий», «промо-акции», «простая оплата», «промышленного уровня», «потенциальные», «качественно», «вкусные», «равномерно».
- EN: "fast", "convenient", "good", "sufficient", "often", "soon", "many", "few", "proper", "minimal", "fresh", "promo", "simple payment", "industrial-level", "potential", "lower quality", "higher quality", "tasty", "evenly".

### Placeholder tokens

- Tokens matching `\[[A-ZА-Я]+\]`, `TBD`, `N/A`, `?`, `…` inside a requirement body are **blockers** for finalization, not vague words.
- Classify each placeholder:
  - **Unlinked placeholder** — placeholder not linked to any `Q-XX`.
    Remark: `Placeholder: line [ref] "[X]" — replace or link to Q-XX.`
  - **Q-linked placeholder** — placeholder linked to an open question.
    Remark: `Q-linked placeholder: line [ref] "[X]" → Q-04 (owner: …, blocking: …).`
    This is a warning for drafts and a blocker for finalization.
  - **Q-mismatch** — placeholder linked to a `Q-XX` whose subject does not
    match the placeholder context.
    Remark: `Q-mismatch: line [ref] "[X]" linked to Q-04, but Q-04 is about price.`

### Remark format

- Unmeasurable: `Unmeasurable: line [ref] "[phrase]" → propose "[quantified version]".`
- Ambiguous:    `Ambiguous: line [ref] "[phrase]" → unclear [actor|action|object]; propose "[clarification]".`
- Placeholder:  `Placeholder: line [ref] "[X]" — replace or link to Q-XX.`
- Q-linked:     `Q-linked placeholder: line [ref] "[X]" → Q-XX.`
- Q-mismatch:   `Q-mismatch: line [ref] "[X]" linked to Q-XX, but Q-XX is about [topic].`

Measurable example:   `Service time per customer ≤ 3 minutes` (NFR-02).
Unmeasurable example: `Service should be fast` → fix: `Service time per customer ≤ [X] minutes`.

## 7. Покрытие MoSCoW (MoSCoW Coverage)

Rules:

- Every prioritizable requirement (**BR, StR, FR, NFR, BRU**) must have a valid MoSCoW value: `M`, `S`, `C`, or `W`.
- Multi-value placeholders (`M/S/C/W`, `TBD`, `?`) are invalid.
- **CON / DEP / ASM / RISK / GLOSS / INT / DAT** are NOT prioritized unless the document explicitly declares they are.
- MUST items (M) must include core BR, FR, NFR, and their AC.
- The MoSCoW list must reference the canonical section where each ID is defined.
- Distinguish **Missing MoSCoW** (no priority assigned) from **Deferred MoSCoW** (explicitly marked as `TBD` / `deferred` / `post-MVP`).

Remark format:

- `Missing MoSCoW: [FR-04] has no priority (line [ref]).`
- `Deferred MoSCoW: [FR-03] = "TBD" — mark as deferred or assign a value (line [ref]).`
- `Invalid MoSCoW: [BRU-01] = "M/S/C/W" (line [ref]).`
- `Misplaced MoSCoW: [CON-01] carries priority but is a constraint (line [ref]).`
- `MoSCoW reference error: [BRU-01] listed in MoSCoW but defined in §BR, not §Business Rules (line [ref]).`

## 8. Покрытие AC/TC (AC/TC Coverage)

Rules:

- Every **FR** has ≥1 AC.
- Every **NFR** has ≥1 AC.
- Every **AC** has ≥1 TC (or is explicitly marked manual / not-testable-with-a-TC, with justification).
- Every **TC** references exactly one AC.
- AC format must be Given–When–Then (or equivalent explicit precondition / action / outcome).
- The AC must address the **same subject** as its parent (see §4 semantic coverage).
- The AC metric must cover the parent’s metric (see §4 metric coverage).

### Multi-parent AC

- If an AC is traced to more than one parent, require explicit justification
  (shared metric, shared acceptance scenario). Otherwise split it.

### AC inheritance

- AC inherit the MoSCoW priority of their parent.
- Do not require MoSCoW on AC directly; verify consistency instead.
- If the parent has no MoSCoW, mark the AC as `AC inheritance: [AC-01] has no parent priority`.

Remark format:

- `Missing AC: [FR-03] has no AC (line [ref]).`
- `Missing AC: [NFR-01] has no AC (line [ref]).`
- `Missing TC: [AC-02] has no TC (line [ref]).`
- `Non-GWT AC: [AC-03] “…” → propose Given/When/Then (line [ref]).`
- `Multi-AC TC: [TC-01] references [AC-01] and [AC-02]; split (line [ref]).`
- `Multi-parent AC: [AC-01] traced to [BR-01], [FR-01], [NFR-01] — split or justify (line [ref]).`
- `AC inheritance: [AC-01] inherits M from [FR-01]; no direct MoSCoW needed.`
- `Semantic gap: [AC-01] does not address [NFR-01] subject (line [ref]).`
- `Metric gap: [AC-01] metric “≥ 90% taste” does not cover parent [FR-01] metric “50–100 шт/день” (line [ref]).`

## 9. Единый язык и термины (Unified Language & Term Consistency)

Rules:

- The document must declare its primary language (Russian or English) in a header note.
- Each section must use the same language; mixed-language sections must be explicitly marked as bilingual.
- Translated terms (e.g. `KPI` vs `КПЭ`, `stakeholder` vs `заинтересованная сторона`) must be consistent; flag inconsistent translations.
- Mixed-alphabet tokens inside a single word (e.g. `Потentialные`, `卫生`) are language issues.
- GLOSS terms must be used consistently with their definitions; synonyms that contradict the glossary must be flagged.
- If the source interview was Russian but the spec is English — confirm with the user; do not assume the translation is final.
- **Undeclared foreign terms:** if a primary language is declared, every non-primary-language token must be either:
  - a registered term in GLOSS, OR
  - explicitly marked as a business term (e.g. `ROI`, `KPI` in a glossary or a footnote).
- **Canonical form:** if a term has multiple transliterations (`SanPiN` / `СанПиН` / `санитарные нормы`), the canonical form must be registered in GLOSS and used everywhere.

Flag format:

- `Language: [section] uses [language A] but references terms from [language B] (line [ref]); confirm intended language.`
- `Language: line [ref] "Потentialные" mixes alphabets; propose "Потенциальные".`
- `Language: line [ref] "卫生" is neither RU nor EN; propose "санитарные нормы".`
- `Term: [GLOSS-01] defines “Чебурек” but line [ref] uses “чебуреок”; unify.`
- `Undeclared foreign term: line [ref] "ROI" — add to GLOSS or mark as business term.`
- `Transliteration: line [ref] "санитарные нормы" — canonical form is "SanPiN" (GLOSS-04).`

## 10. Качество открытых вопросов (Open Questions quality)

Each `Q-XX` must have:

- owner / ответственный;
- blocking artifact / блокирует;
- status (`open` / `in progress` / `closed`);
- date (opened / updated).

If a `Q-XX` has no explicit `status`, treat it as `open`.

Ownership: `Q-*` must be defined in the §Open Questions section; a definition
elsewhere is a `Misplaced definition` (see §2).

Remark format:

- `Q quality: [Q-01] missing status (line [ref]).`
- `Q quality: [Q-02] missing date (line [ref]).`
- `Q quality: [Q-03] blocking artifact not specified (line [ref]).`
- `Q quality: [Q-04] owner not specified (line [ref]).`