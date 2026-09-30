---
name: himouto
description: Attacks Python code with edge cases by writing Hypothesis property-based tests, running them, and reporting each bug as a minimal failing test. Use when the user asks to find bugs in, stress-test, or break Python functions, or wants property-based or edge-case tests for existing Python code.
---

# himouto

Find real bugs in Python code by writing Hypothesis property-based tests that fail against it.

## Iron rules

1. **Every finding must be a runnable failing test, never just a comment.** If you cannot make a test fail on the current code, it is not a finding.
2. **Only write test files. Never modify source files.** Not even to fix a bug you found; the failing test is the deliverable. This includes dependency files.
3. **Never weaken or delete an existing test to make it pass.** Put your tests in new files and leave existing test files untouched.

## Workflow

Copy this checklist and tick items off as you go:

```
- [ ] 1. Read the target code and find the project's test command
- [ ] 2. List properties and edge cases to try
- [ ] 3. Write Hypothesis tests
- [ ] 4. Run them and verify every failure
- [ ] 5. Report findings: minimal failing input + why it matters
```

### 1. Read the target code

Read the function, its type hints, docstring, input validation, and callers. From these, write down its contract: which inputs are valid and what it promises for them. Every later step is judged against this contract. Find the test command now (see "Running tests").

### 2. List properties and edge cases

Before writing code, list each property to test (see "Property patterns") and the inputs most likely to break it: empty, zero, negative, huge, NaN/inf, `-0.0`, unicode and whitespace, duplicates, unsorted input, `None` where the type is `Optional`.

Test at most 5 properties per function, and start with the riskiest functions (money or data math, parsing, the most branching), unless the user asks for more.

### 3. Write Hypothesis tests

- One new file per target module: `tests/test_himouto_<module>.py`. Follow the project's test layout if it differs.
- Generate only inputs the contract allows. A crash on input the function rejects by design is not a bug.
- Prefer precise strategies (`st.integers(min_value=0)`) over `assume()` or `.filter()`, which waste examples and trigger health-check errors.
- One property per test function, named after it: `test_parse_format_round_trip`.

### 4. Run and verify

Run the new file with the project's test command. For each failure:

1. **Is the failure in the target code?** An `ImportError`, a typo, or a broken strategy is a bug in your test. Fix the test; it is not a finding.
2. **Is the input valid under the contract?** If not, narrow the strategy and re-run. Narrow only when you can cite where the contract excludes the input (type hint, docstring, explicit validation). Narrowing to dodge a real failure breaks rule 3.
3. **Pin the minimal input.** Copy the shrunk `Falsifying example` from the output into `@example(...)` above `@given`. This makes the failure reproduce on any machine, without the local `.hypothesis/` database.
4. **Re-run** to confirm the pinned test fails every time.

If Hypothesis is not installed, stop and report the install command for the project's tooling. Do not edit dependency files.

If every property holds, say so and list what you tested. Never invent findings.

### 5. Report

Use the template in "Report format".

## Property patterns

- **Invariant**: a fact that holds for every input, e.g. `len(dedupe(xs)) <= len(xs)`, or the result is always in range.
- **Round-trip**: decoding an encoded value returns the original, e.g. `parse(format(x)) == x`.
- **Idempotence**: applying twice equals applying once, e.g. `normalize(normalize(s)) == normalize(s)`.
- **Boundary values**: inputs at the edges of the domain (empty, 0, max, NaN, `""`), pinned with explicit `@example`s.
- **Oracle / comparison**: the result matches a simple, obviously correct reference, e.g. `my_sort(xs) == sorted(xs)`.

## Running tests

Use the project's own test command. Detect it in this order:

1. A command documented in CI config, `Makefile`, `tox.ini`, `noxfile.py`, or the README.
2. The lock file: `uv.lock` → `uv run pytest`, `poetry.lock` → `poetry run pytest`, `pdm.lock` → `pdm run pytest`, `Pipfile.lock` → `pipenv run pytest`.
3. Fallback: `python -m pytest`. Avoid bare `pytest`, which can belong to a different environment than the project's.

Projects with `unittest`-style tests are fine: pytest runs them too.

## Report format

Sort findings by severity:

- **high**: silently wrong result, or data loss/corruption, on valid input
- **medium**: unhandled exception or crash on valid input
- **low**: inconsistent behavior on rare-but-valid input, or a misleading error

```markdown
## himouto report: <target>

Test command: `<command>` · Test file: `<path>`
Findings: <n> (high <n>, medium <n>, low <n>)

### [HIGH] <function>: <property that broke, in one line>
- Test: `<path>::<test_name>`
- Minimal failing input: `<shrunk input>`
- Expected: <what the contract promises>
- Actual: <what happened>
- Why it matters: <concrete impact on a user>

### Properties that held
- `<function>`: <property>

### Note
These tests fail until the bugs are fixed, so CI will be red. To keep CI green while a fix is pending, mark a test `@pytest.mark.xfail(strict=True)`; it will then fail loudly once the bug is fixed, as a reminder to remove the mark.
```

Leave failing tests as plain failures. Never apply `xfail` yourself; the note lets the developer choose.
