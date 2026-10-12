# lean-phys-community/PhysLean: agent setup

- **Snapshot:** commit `7639358` (2026-10-12), from `repos/lean-phys-community__PhysLean/snapshot.json`.
- **Tools targeted:** `AGENTS.md` readers, with a Claude-specific commit trailer.
- **Files:** `AGENTS.md`, rules on content, proof structure, checks, commits and PRs. It points to `AI-POLICY.md` and `docs/ReviewGuidelines.md` (not copied).
- **What agents are asked to do:** write physics lemmas and definitions in Physlib; split long proofs; write commits and PR descriptions.
- **Build and verification:** `lake exe cache get`, `lake build`, `lake exe lint_all`, `lake exe forMathlib_lint`, `./scripts/lint/required/lint-style.sh` ("commit your changes first"), `lake exe module_doc_lint`, `lake exe auxillary_script_test`. PhyslibAlpha changes have four more linters.
- **Proof policy:** "Never use the `axiom` declaration." "Never use `sorry`." No `True`-valued fields or theorems, no `∃ x, ..., True`, and no hypothesis "that assumes the conclusion". Anything depending on `sorry` or `Lean.ofReduceBool` is tagged `@[sorryful]` or `@[pseudo]`.
- **Lean and Mathlib guidance:** prefer `lemma` over `theorem` unless the result is well known. Proofs should stay under 50 lines, with a detailed list of ways to split them "by meaning" or "by structure". No trivial rewrites of Mathlib results. Module docs use a fixed heading scheme (`## i. Overview` … `## A.`). Every definition gets a docstring. Register new files in `Physlib.lean` in sorted order. `ForMathlib/` files import only from inside that folder.
- **Skills, commands, hooks, MCP:** none.
- **Permissions and safety:** never add files to `module_doc_no_lint.txt`; "fix their module documentation instead".
- **Human oversight:** "The human author must certify the code you write; the fact that it builds does not prove that what you have written is what the human author meant." Commits carry a `Co-authored-by: Claude Opus 4.8` trailer. PR descriptions list every added or removed declaration, with a "reviewer map".
- **Notable ideas:** a list of patterns that make statements vacuous (`True` fields, conclusions assumed as hypotheses); a catalogue of ways to split long proofs; a reviewer map in PRs.
- **Lean-specificity:** high: most rules are about Lean declarations, vacuous statements, proof structure and Lean linters.
- **Evidence:** `AGENTS.md`.
