# ru-normalizr: Refactoring Plan (Conservative / Behavior-Preserving)

## Baseline

Current local baseline in this workspace:

- `py -3.12 scripts/dev.py check` exits `0`
- `py -3.12 -m pytest -q` passes locally
- The worktree is already dirty in multiple code files, so this plan should assume incremental, isolated changes instead of a large all-at-once branch

This matters because the original first step, "fix the baseline", is no longer accurate. The safer starting point is to preserve the green baseline while making small, reviewable refactors.

---

## What Looks Worth Refactoring

These problems are real and worth addressing:

### 1. Repeated case-mapping data

The same `pymorphy`/`num2words` case mapping appears in multiple places:

- `ordinal_utils.py`
- `years.py`
- `numerals/ordinals.py`
- `numerals/_helpers.py`

This is low-risk to deduplicate because it is data-level duplication, not stage-level behavior.

### 2. Repeated suffix sets around ordinal/cardinal endings

There is meaningful overlap between:

- `normalizer.py: GLUED_NUMERIC_SUFFIXES`
- `numerals/_hyphen.py: ORDINAL_SUFFIXES`
- `numerals/_hyphen.py: CARDINAL_CASE_SUFFIXES`
- `years.py: YEAR_SUFFIX_TO_CASE`

These are related, but not fully interchangeable. A safe refactor should extract shared primitives without forcing one single "universal suffix table".

### 3. `normalize_ordinals()` is doing too much in one callback

`numerals/ordinals.py` currently mixes:

- suffix interpretation
- context lookup
- noun-anchor detection
- regnal-like person-name handling
- cardinal fallback behavior
- final rendering

This is a good refactor target, but it should be decomposed gradually. The right goal is testable helpers, not an arbitrary line-count target.

### 4. `_fix_glued_numbers()` is an actual hotspot

`normalizer.py::_fix_glued_numbers()`:

- runs iteratively
- calls morphology inside regex replacement
- decides multiple unrelated categories at once

This is worth profiling and simplifying, but only after lower-risk deduplication is done.

### 5. `г.` handling is spread across preprocess / years / numeral logic

The current behavior around:

- `1990 г.`
- `55 г.р.`
- `123 г.`

is distributed across multiple modules. That is a valid design concern, but centralizing it is behavior-sensitive and should only be done behind strong regression coverage.

---

## What Should Not Be Over-Unified

The biggest risk in this repo is treating "similar" logic as if it were "the same" logic.

In particular, these tables should not be merged blindly:

- `numerals/_constants.py: PREP_CASE`
- `years.py: PREPOSITIONS_TO_CASE`
- `roman_numerals.py: _REGNAL_CASE_CONTEXT`
- `numerals/ordinals.py: HEADING_CONTEXT_CASES`

They overlap lexically, but they encode different semantics by stage.

Examples:

- cardinals: `в 5 минут` -> accusative-like behavior
- years: `в 1990 году` -> locative-like behavior
- regnal names and heading ordinals have their own contextual shortcuts

So the right move is:

- document the differences clearly
- extract only truly shared subsets/helpers
- keep stage-specific policies stage-specific

Not the right move:

- one giant `PREP_CASE_*` module with forced reuse everywhere

---

## Recommended Phases

### Phase 1. Refresh the Test/Baseline Story

Goal: make the plan match reality, not old assumptions.

Steps:

1. Record the current green baseline:
   - `py -3.12 scripts/dev.py check`
   - `py -3.12 -m pytest -q`
2. Add a short "refactor guardrails" note to the plan:
   - preserve behavior unless a bugfix is intentional
   - run targeted tests after each isolated refactor
   - do not combine structural cleanup with normalization changes
3. Avoid large test-file churn up front

Why:

- Reorganizing tests before any code change creates noise and makes behavior review harder.
- This repo already has useful regression coverage in `tests/test_reported_regressions.py` and `tests/test_stages.py`.

Acceptance:

- baseline commands still pass
- no functional code changes yet

### Phase 2. Low-Risk Data Deduplication

Goal: remove the safest duplication first.

Good targets:

- shared `CASE_TO_NUM2WORDS`
- shared gender-to-`num2words` mapping
- maybe a small shared suffix helper module for clearly identical suffix groups

Recommended scope:

- keep `ordinal_utils.py` in place for now unless a compatibility shim is added
- update imports only where duplication is exact
- do not force years/regnal/heading case tables into one abstraction yet

Acceptance:

- all tests pass
- duplicated exact case maps are reduced to one source of truth
- no output changes

### Phase 3. Extract Helpers From `normalize_ordinals()`

Goal: make ordinal logic reviewable and independently testable.

Extract helpers such as:

- find first noun on the right
- find likely person-name anchor on the left
- normalize default suffix interpretation
- render cardinal-vs-ordinal output from a resolved decision

Recommended shape:

- keep `normalize_ordinals()` as an orchestrator
- move helper logic only after adding or confirming focused tests for the affected behavior
- avoid changing policy while extracting helpers

Non-goal:

- shrinking the function to a specific number of lines

Acceptance:

- ordinal/regression tests still pass
- helper-level tests can be added for the extracted logic
- behavior remains unchanged

### Phase 4. Profile and Tame `_fix_glued_numbers()`

Goal: reduce risk and cost in the preprocess pipeline hotspot.

Steps:

1. Measure how often the iterative loop needs more than one pass
2. Separate easy classifications from morphology-dependent ones
3. Short-circuit known cases first:
   - suffixes
   - units
   - prepositions
4. Leave morphology only for ambiguous leftovers

Important:

- this should be driven by profiling and regression examples, not aesthetics
- if multiple passes are genuinely needed, document why and keep them

Acceptance:

- tests pass
- morphology calls are reduced or at least better localized
- no unintended changes in glued-number behavior

### Phase 5. Evaluate `г.` Centralization as a Separate Bugfix Track

Goal: reduce contradictory handling without destabilizing the pipeline.

This should happen only after the earlier refactors are merged and stable.

Recommended approach:

1. Inventory current expected behavior with explicit tests for:
   - year abbreviations
   - birth-year abbreviations
   - gram/mass contexts
2. Introduce one classifier/helper only if it clearly replaces duplicated decisions
3. Keep preprocess canonicalization separate from semantic classification

Important:

- this is not a "cleanup" task
- this is a behavior-sensitive normalization change area

Acceptance:

- explicit `г.` coverage is stronger than before
- no regressions in year or measurement handling

### Phase 6. Optional Internal Cleanup

Possible follow-ups after the main risk areas are stable:

- move compound adjective stems to a better internal constants location
- remove dead code / unused imports
- improve inline comments where stage-specific behavior is non-obvious

This phase should stay internal-only unless a user-visible bug is being fixed.

---

## Things I Would Remove From the Older Plan

These ideas are not wrong, but they are not good default refactor goals here:

- "Fix `dev.py check` first" because it already passes
- large test-file reorganization before code changes
- forcing all preposition tables into one central module
- moving `ordinal_utils.py` without a compatibility plan
- adding new public config like `extra_compound_stems` before there is a real user need
- using function length alone as a success metric
- updating `CHANGELOG.md` for purely internal refactors

---

## Suggested Execution Order

1. Keep baseline green and documented.
2. Deduplicate exact shared mappings only.
3. Extract ordinal helpers without changing policy.
4. Profile and simplify `_fix_glued_numbers()` conservatively.
5. Treat `г.` centralization as its own behavior-sensitive project.
6. Do final cleanup only after the core logic settles.

This order better matches the repository guidance:

- smallest correct fix
- no unnecessary refactors during bugfix work
- preserve public behavior
- add or keep tests close to behavior-sensitive changes

---

## Done Criteria

The refactor is successful when:

- exact duplicated case maps are centralized
- ordinal logic is easier to test and review
- `_fix_glued_numbers()` is better understood and less opaque
- stage-specific semantics remain stage-specific
- the full validation flow still passes
- no changelog entry is added unless behavior changes intentionally

---

## Practical Validation Flow

For each isolated refactor:

1. run targeted tests for the touched area
2. run `py -3.12 -m pytest -q`
3. if the change touches packaging or broad pipeline wiring, run `py -3.12 scripts/dev.py check`

For behavior-sensitive phases (`normalize_ordinals`, `_fix_glued_numbers`, `г.` handling), add before/after sample assertions when practical instead of relying on structural confidence alone.
