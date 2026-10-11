# verse-lab/velvet

- **Domain:** Dafny-style deductive verification of imperative programs embedded in Lean.
- **Primary role:** `DSL-host/metaprogramming`
- **Secondary roles:** `certifier-software`
- **What the kernel checks:** Full proofs. `prove_correct` produces a `<name>.spec` theorem. VCs are discharged by `velvet_vcgen … with finish` (grind-based, `Velvet/Core/VCGen/Frontend.lean`) or by hand (`Velvet/Examples/Sqrt.lean`). I found no SMT trust axiom. `#derive_tester_for` also runs contracts as executable checkers (`#eval increment.check …`, `docs/doc.md`).
- **Certified vs only expressed:** About 50 LeetCode-style programs (`CaseStudies/LeetProof/`), a segment tree, graph code and examples are proven against their pre/postconditions. The semantics (`WPPartial` in `Velvet/Core/Partial/Defs.lean`) is an axiomatised class, so partial correctness is relative to those axioms. Testing only checks concrete inputs.
- **Output artifact:** A Lean library and DSL. The proofs yield theorems, and programs compile and run. A stub `velvet` executable (`Main.lean`) only prints a greeting.
- **Author mode:** Mostly human. Headers name Lean FRO authors (Sebastian Graf, Vladimir Gladshtein) in `Velvet/Core/VCGen/Solve.lean`. Every LeetProof file follows one template ("Program description", `precondition`/`postcondition`), which hints at a benchmark pipeline, possibly machine-assisted. That is unconfirmed: I found no AI markers.
- **Translation direction:** None.
- **Creative idea:** A Dafny-like `method … requires … ensures … do` language is built entirely from Lean syntax extensions. Its VC generator is built on Lean core's own `Std.Internal.Do` / `mvcgen` and `Lean.Meta.Sym` machinery, so the same code is executable, testable and provable.
- **Why Lean?:** The README argues for "multi-modal" use: compile, execute, property-test and prove in one environment, with Mathlib available. My assessment: Dafny can't fall back to interactive proof or Mathlib, and Coq/Isabelle lack Lean's `do`-notation extension points.
- **Notable techniques:**
  - The `method` command syntax is in `Velvet/Frontend/SyntaxDecls.lean` and is elaborated in `Velvet/Frontend/Method.lean`, including `partial_fixpoint` motives for `method rec`.
  - `while`/`for` with named invariants are high-priority `doElem` syntax (`Velvet/Core/Loop/Elaboration.lean`).
  - The VCGen worklist uses Sym-simp (`Velvet/Core/VCGen/Solve.lean`).
  - Testers are derived from contracts via Decidable heuristics (`Velvet/Frontend/Testing.lean`, `Velvet/Core/DecidableHeuristics.lean`).
- **Heuristic check:** The Phase 1 guess was `certifier`. I disagree in part: the core is about 7k lines of elaborators and VCGen (DSL host), and the case studies are the certifier part. Velvet does **not** depend on Loom. `lakefile.toml` requires only `plausible`. Loom survives only as the source of one adapted file (`DecidableHeuristics.lean`: "Adapted from Loom's CaseStudies/TestingUtil.lean").
- **Evidence:** `README.md`, `lakefile.toml`, `lake-manifest.json`, `Main.lean`, `docs/doc.md` (headings), `Velvet/Frontend/{SyntaxDecls,Method,Testing}.lean`, `Velvet/Core/VCGen/Solve.lean`, `Velvet/Examples/Sqrt.lean`, `CaseStudies/LeetProof/MoveZeroes.lean`, `CaseStudies/README.md` (fetched).
