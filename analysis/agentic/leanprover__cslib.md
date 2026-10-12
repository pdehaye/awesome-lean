# leanprover/cslib: agent setup

- **Snapshot:** commit `4b88bca` (2026-10-11), from `repos/leanprover__cslib/snapshot.json`.
- **Tools targeted:** `AGENTS.md` readers, plus any agent with a "Lean MCP server" available (none is configured in the repo).
- **Files:** `AGENTS.md`: repository overview, MCP-first workflow, validation commands, critical requirements, style.
- **What agents are asked to do:** formalize CS theory in Lean (proof development, new modules, tests), write PRs.
- **Build and verification:** iterate with MCP diagnostics ("Wait for elaboration to finish"); keep Lake for checkpoints. Full CI sequence before committing: `lake build --wfail --iofail`, `lake exe mk_all --check`, `lake test`, `lake lint`, `lake exe lint-style`. New files need `lake exe mk_all`; `lake exe shake Cslib` minimizes imports.
- **Proof policy:** none stated (no rules on `sorry` or axioms; the `--wfail` build implicitly fails on `sorry` warnings).
- **Lean and Mathlib guidance:** "Use the Lean MCP server first" for goals, hover and theorem search; don't repeatedly run `lake build` or `lake env lean` when MCP can answer. Every module must import `Cslib.Init`. Follow the Mathlib code style, `CODESTYLE.md` and `CONTRIBUTING.md`; use domain-specific variable names (`State`, `μ`); "golfing is welcome if proofs remain clear"; reuse existing typeclasses; use `module` with `public import`.
- **Skills, commands, hooks, MCP:** none in the repo. The Lean MCP server is assumed to be provided by the session.
- **Permissions and safety:** if MCP is unavailable, "briefly report the limitation"; "Do not silently skip checking for MCP availability". Run commands from the repo root.
- **Human oversight:** PR titles `type(scope): description`; copyright header with year and authors. No AI-labeling or review rules.
- **Notable ideas:** an MCP-first proof loop with explicit "reserve Lake for …" rules to cut slow rebuilds; one ordered CI validation sequence ("do not run both redundantly"); a step-by-step "creating a new module" recipe.
- **Lean-specificity:** high. Nearly every section concerns Lake, Mathlib style, Lean MCP tooling or library import structure.
- **Evidence:** `agent_files/AGENTS.md`, `snapshot.json`.
