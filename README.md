<p align="center">
  <img src="assets/logo.png" width="160" alt="himouto logo" />
</p>

<h1 align="center">himouto</h1>

<p align="center">
  Gives your AI agent a bratty little sister who tries the inputs you didn't think of<br/>
  and shows off everything she broke.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/status-v0.1%20in%20progress-orange.svg" alt="Status: v0.1 in progress">
  <img src="https://img.shields.io/badge/python-3.11%2B-blue.svg" alt="Python 3.11+">
</p>

---

himouto is a Claude Code skill (packaged as a plugin) that attacks Python code with edge cases and Hypothesis property-based tests. A code reviewer reads your code and says it *might* break. himouto runs it and proves it *does*, with a failing test you can keep. It only writes tests and never edits your source.

- **Punchline:** A reviewer says it might break. She proves it breaks.
- **Metaphor:** She doesn't create bugs. She finds the ones already there — like jumping on a sofa whose leg is already cracked. Better now than when guests arrive (production).
- **Pairs with [ponytail](https://github.com/DietrichGebert/ponytail):** ponytail makes your agent write less code. himouto makes sure the code that's left doesn't break.

> **Status:** v0.1, in progress. Nothing below has been measured yet — no accuracy, no bug counts, no benchmarks. Anything not built is marked *planned*.

## Problem

- AI agents write code that looks right but breaks on inputs nobody tried (empty, negative, boundary, rounding, huge values).
- Example-based tests check the cases the author already thought of.
- Property-based testing finds the rest, but writing properties/specs is the #1 barrier to using it in practice (16 of 30 participants in [Goldstein et al., "Property-Based Testing in Practice"](https://andrewhead.info/assets/pdf/pbt-in-practice.pdf)).

## How it works (v0.1)

Rules:
1. Every finding is a runnable failing test, never just a comment.
2. It only writes test files. It never modifies source.
3. It never weakens or deletes existing tests.

Workflow:
1. Read the target code.
2. List properties and edge cases to try.
3. Write Hypothesis tests.
4. Run them.
5. For each failure, report the minimal failing input (via Hypothesis shrinking) and why it matters to a user, sorted by severity.

Property patterns it uses: invariants, round-trip, idempotence, boundary values, oracle/comparison.

**Who it's for:** Python developers using Claude Code who want an agent that attacks their code with weird inputs before users do. Built first for the author's own projects ("scratch your own itch"). Not a code reviewer, not an auto-fixer, not a replacement for pytest.

## Repo layout (current)

```
himouto/
├── demo/                        # sample code to try the skill on
├── tests/                       # project tests
├── pyproject.toml, uv.lock      # dev environment (uv)
└── .python-version              # Python 3.11
```

The plugin manifest (`.claude-plugin/plugin.json`) and skill definition (`skills/himouto/SKILL.md`) are v0.1 drafts: they pass `claude plugin validate --strict` but have not been tried on real code yet.

## Quickstart (current, for development)

Dev environment:

```bash
uv sync --locked
uv run pytest
```

Try the plugin locally with Claude Code (official dev flow, once the manifest lands):

```bash
claude plugin validate .
claude --plugin-dir .
```

Once installed, skills are invoked with the plugin prefix, e.g. `/himouto:<skill>`.

Marketplace install is **planned**, not available yet. The skill itself doesn't assume `uv` — it runs whatever test command the target project uses.

## Roadmap

| Version | What |
|---|---|
| v0.1 | Core skill: attack code with Hypothesis, write failing tests, never edit source ← **current** |
| v0.2 | Dogfood on real personal projects; log every case where it can't tell a bug from intended behavior |
| v0.3 | Ask the human when unsure (max 3 multiple-choice questions, each with the counterexample). Answers saved to `.himouto/contracts.md` and turned into permanent property tests |
| v0.4 | Measure v0.1 vs v0.3 on seeded-bug demos (recall, false positives, cost), including a demo with no bugs |
| v0.5 | Hook that blocks weakening her tests; optional persona; professional output in CI |

**The idea behind v0.3 (main differentiator):** existing tools find bugs from what code *declares* (docstrings, comments). Business rules like "fee must never be negative" usually live only in people's heads. himouto plans to ask, then lock the answer in as a test — building an executable spec of rules nobody wrote down.

A bratty little-sister voice when running locally, with an automatic professional tone in CI (`CI=true`) and an off switch, is also planned (v0.5) — not implemented in v0.1.

## Related work

- [agentic-pbt](https://github.com/mmaaz-git/agentic-pbt) (`/hypo`): agent that writes property-based tests for libraries from documented behavior. himouto targets business code and undocumented rules instead.
- Trail of Bits' property-based testing skill.
- [Hypothesis](https://hypothesis.readthedocs.io/), which does the actual input generation and shrinking.
- [ponytail](https://github.com/DietrichGebert/ponytail), the companion idea.

## Limitations

- Early and unmeasured. No benchmarks yet.
- Python + Hypothesis only.
- LLM-written properties can be tautological (always pass). Validating properties with mutation testing is planned, not done.
- Hypothesis is randomized; seeds/settings are needed to avoid flaky runs.
- It can report behavior that is actually intended. Asking the user (v0.3) is meant to address this.

## License

[MIT](LICENSE)
