# leanprover/lean-eval

- **Domain:** Benchmarking automated (and human) formal mathematics: a catalog of research-level problem statements scored by comparator.
- **Primary role:** `AI-oracle/referee`
- **Secondary roles:** `specification/modeling`, `program`, `coordination/trust-infrastructure`
- **What the kernel checks:** Types only for the trusted statements: problems are `@[eval_problem]` theorems/defs with `sorry` bodies (e.g. `generated/sturm/Challenge.lean`). A submitted proof is checked later by the external comparator pipeline (Lean kernel plus the nanoda kernel), not inside this repo.
- **Certified vs only expressed:** Nothing mathematical is proven here. Lean states the problems (Mathlib/TauCeti statements), and the Lean tooling generates per-problem workspaces and runs the scoring.
- **Output artifact:** Generated comparator workspaces (`Challenge.lean`, `Solution.lean` bridge, `Submission.lean`, config), plus a verdict per submission and a leaderboard.
- **Author mode:** Mixed. Statements are written by humans (manifest `submitter` field); solvers can be humans or models. `docs/overhaul-completion-plan.md` mentions "headless-agent submission" and self-reported model/human-involvement fields.
- **Translation direction:** none (Lean generates Lean workspaces).
- **Creative idea:** A Lean attribute plus Lean metaprograms turn sorry'd theorem statements into isolated, sandboxed "fill the hole" workspaces whose only scoring is a kernel-backed comparator verdict.
- **Why Lean?:** Not stated. Own assessment: the benchmark depends on Mathlib for statements and on Lean's exportable kernel terms, so comparator can check statement identity and axioms exactly; a Python harness could not compare statements semantically.
- **Notable techniques:**
  - Reading elaborated terms to count lambda binders over `sorryAx`, so the generated `Solution.lean` delegates with the right arguments (`EvalTools/ExtractTheorem.lean`, `signatureExplicitParameters`).
  - Computing same-module dependencies from elaborated terms to split `ChallengeDeps` from hole-dependent helpers (`EvalTools/ExtractTheorem.lean`).
  - The per-workspace `lake test` driver is written in Lean. It strips workspace paths from the search path and refuses tool overrides inside the workspace (`templates/WorkspaceTest.lean`, copied into `generated/*/WorkspaceTest.lean`, `trustedTool`).
  - CLI with manifest validation and import-coverage checks (`EvalTools/Main.lean`, `EvalTools/ValidateManifest.lean`).
- **Heuristic check:** The Phase 1 guess was `spec+proof + program`. I partly disagree. The theorem count (1491) is high, but most are sorry'd challenge statements (sorry=1293, many duplicated across `generated/`). This is statement authoring plus referee tooling, not proof.
- **Evidence:** `README.md`, `lakefile.toml`, `EvalTools/Markers.lean`, `EvalTools/ExtractTheorem.lean`, `generated/sturm/WorkspaceTest.lean` (head), `generated/sturm/Challenge.lean`, `generated/sturm/Solution.lean`, `docs/overhaul-completion-plan.md` (grep), `LeanEval/ProgramVerification/*` (grep).
