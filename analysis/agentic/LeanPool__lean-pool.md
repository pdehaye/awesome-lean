# LeanPool/lean-pool: agent setup

- **Snapshot:** commit `7761cb6` (2026-10-11), from `repos/LeanPool__lean-pool/snapshot.json`.
- **Tools targeted:** Claude Code (`CLAUDE.md`, `.claude/skills/`), `AGENTS.md` readers, GitHub Copilot code review (`.github/instructions/`).
- **Files:** `AGENTS.md` and `CLAUDE.md` are byte-identical, "a concatenation of README.md and CONTRIBUTING.md"; `review.instructions.md` (Copilot PR review rubric); two skills for Mathlib version bumps.
- **What agents are asked to do:** submit or import formalization projects; bump the whole pool to a new Lean/Mathlib release and open a PR; repair one project headlessly in CI; review PRs for "fit and significance".
- **Build and verification:** `lake exe cache get` then `lake build LeanPool.YourProject` (or `make build-project P=...`). CI runs `lake exe mk_all --check`, `lake build LeanPool`, `lake exe runLinter`, `lake exe lint-style`, and `python -m lean_pool.quality`. The bump skills require "zero errors and zero warnings" and say CI "fails on ANY `warning:` line".
- **Proof policy:** projects must be `sorry`-free, with no axioms beyond `Classical.choice`/`propext`/`Quot.sound` and no `unsafe`/`partial`. The skills also ban `native_decide`, `maxHeartbeats` increases and linter waivers. "No statement drops"; change a statement only when it no longer compiles, and then only minimally. A declaration that Mathlib has absorbed "is *still* not yours to delete".
- **Lean and Mathlib guidance:** toolchain pinned in `lean-toolchain`; Lean conventions are in `.github/CODE_QUALITY.md` (not copied). Find renames with `rg` over `.lake/packages/mathlib` and "Trust the deprecation note over a guess". Reuse Tau Ceti and Mathlib instead of vendoring them.
- **Skills, commands, hooks, MCP:**
  - `version-bump`: migrate the whole pool, using parallel agent Workflows (concurrency 2–3), a RAM watchdog and worktrees, then open a non-draft PR.
  - `version-bump-project`: CI repair of one project, CLI only ("the lean-lsp MCP is not available"), returning a structured report.
  - No hooks or MCP config.
- **Permissions and safety:** "Never change the checks or gates… If a check fails, fix the code, not the check. This applies… especially to AI agents." Content PRs may touch only `LeanPool/**/*.lean` and project YAML. Keep RAM under 24 GB; kill lean-lsp-mcp because it eats memory. No `git worktree remove --force`.
- **Human oversight:** LLM review (GPT-based) and advisory Greptile instead of mathlib-style human review; maintainers merge through a merge queue. Project cards must declare `provenance`: `human`, `AI`, or `mix`. The Copilot reviewer gives a verdict and a 1–5 code-quality score ("1 (clear AI slop)").
- **Notable ideas:** a declaration-name drop guard diffed against `main`; a structured honest-failure report ("a green report that is not green is not"); a review rubric that skips anything linters already catch.
- **Lean-specificity:** high: the skills are built around Mathlib bumps, deprecation aliases, Lean linters and axiom gates.
- **Evidence:** `AGENTS.md`, `CLAUDE.md`, `.github/instructions/review.instructions.md`, `.claude/skills/version-bump/SKILL.md`, `.claude/skills/version-bump-project/SKILL.md`.
