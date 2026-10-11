# leanprover/comparator

- **Domain:** Trustworthy judging of untrusted Lean proofs (built for the AIMO LLM competitions, per the README acknowledgement).
- **Primary role:** `AI-oracle/referee`
- **Secondary roles:** `coordination/trust-infrastructure`, `program`
- **What the kernel checks:** The solution environment is replayed into the Lean kernel in-process (`Main.lean`, `runBuiltinKernel` using `Kernel.Environment.replay`), and optionally into external kernels such as nanoda. Statement equality and the axiom allow-list are checked by comparator's own Lean code over exported terms.
- **Certified vs only expressed:** Comparator certifies other people's proofs: the statement matches the challenge, only permitted axioms are used, and the kernel accepts the proof. Its own code is not verified. The theorems in `tests/projects/` are adversarial fixtures, not results.
- **Output artifact:** A pass/fail verdict (executable `comparator` driven by a JSON config).
- **Author mode:** Human (Henrik Böving / Lean FRO headers). The software is designed to judge AI-produced solutions.
- **Translation direction:** none. It reads lean4export's text export, not oleans.
- **Creative idea:** Lean is used as the judge's implementation language. It builds and exports both sides in a landrun sandbox, compares `ConstantInfo`s structurally, and never mmaps adversarial oleans.
- **Why Lean?:** The README argues the trust model (sandboxing, no olean loading, optional second kernel) rather than the language. Own assessment: writing it in Lean lets comparator reuse Lean's own `ConstantInfo`/`Expr` types and kernel replay, so no reimplementation can drift from the checker.
- **Notable techniques:**
  - A worklist walk over constants used in each statement that requires equal `ConstantInfo` in both environments. Hole names are exempt from value equality (`Comparator/Compare.lean`).
  - Definition holes: name, type, universes and safety must match (`definitionHoleMatches`, `Comparator/Compare.lean`).
  - Transitive axiom audit (`Comparator/Axioms.lean`).
  - landrun argument builder and external-kernel invocation with a nanoda-style config (`Main.lean`).
  - Regression fixtures for known attacks, e.g. a redefined structure behind a raw `Expr.proj` elaborator (`tests/projects/proj_trick/`).
- **Heuristic check:** The Phase 1 guess was `spec+proof + program`. I disagree. The 42 "theorems" are Challenge/Solution test fixtures. The repo is a referee program.
- **Evidence:** `README.md`, `lakefile.toml`, `Main.lean`, `Comparator/Compare.lean`, `Comparator/Axioms.lean` (head), `tests/projects/proj_trick/{Challenge,Solution}.lean`.
