# TauCetiProject/TauCeti: agent setup

- **Snapshot:** commit `997f205` (2026-10-12), from `repos/TauCetiProject__TauCeti/snapshot.json`.
- **Tools targeted:** `AGENTS.md` readers; Claude Code through `.claude/CLAUDE.md`, whose copied content is just `../AGENTS.md` (probably a symlink).
- **Files:** `AGENTS.md`, the contract for agents in this "AI-owned code repo"; `.claude/CLAUDE.md`, a pointer to it.
- **What agents are asked to do:** add mathematics that advances a target in the separate TauCetiRoadmap repo; refactor, simplify proofs and document existing code ("always in scope"); answer AI review findings; make forward-only Mathlib/toolchain bumps.
- **Build and verification:** no commands given. "`main` is always green"; CI builds against pinned Mathlib and enforces the Mathlib linter set.
- **Proof policy:** no `sorry`; no axioms beyond `propext`, `Classical.choice`, `Quot.sound` ("so no `native_decide`"); no `meta import`; no `maxHeartbeats` overrides. "Do not try to disable these." No backwards compatibility: when code moves, delete obsolete names, with no aliases or `deprecated` shims.
- **Lean and Mathlib guidance:** Mathlib's lakefile `rev` must stay `master`; the exact commit lives in `lake-manifest.json`. Lean meta code is human-owned and goes in `scripts/`, so `TauCeti/` holds "mathematics, not metaprogramming". No naming or search-tool advice.
- **Skills, commands, hooks, MCP:** none in the repo. `tauceti-review` and `/review` belong to the external review pipeline.
- **Permissions and safety:** `scripts/`, `.github/` and the lakefile are human-owned; pins may move only forward (checked by `bump-guard`). Never open PRs or issues in TauCetiRoadmap. "Never delete a PR's human-owned changes to get it past the build gate." "Do not `--admin`-merge AI-authored PRs."
- **Human oversight:** AI review agents judge each PR against rubrics in TauCetiReview and post `approve` / `request_changes` / `block`. A PR that changes only `TauCeti/` (or makes a forward-only bump) merges automatically once all rubrics approve and CI is green. Anything touching human-owned paths needs a human. Roadmap changes need a human. Each PR states `Roadmap: <Area>` or `Roadmap: none`.
- **Notable ideas:** a roadmap that gates new mathematics but not refactors; a rule for contradictory review findings ("Contest one of the threads, link the conflicting one, and quote its wording"); path-based auto-merge eligibility.
- **Lean-specificity:** medium: the rules about axioms, `meta import`, Mathlib pins and declaration shims are Lean-specific, but most of the file is about governance and the review pipeline.
- **Evidence:** `AGENTS.md`, `.claude/CLAUDE.md`.
