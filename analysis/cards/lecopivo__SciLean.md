# lecopivo/SciLean

- **Domain:** Scientific computing and machine learning: automatic differentiation, ODE solvers, n-dimensional arrays, probabilistic programming, BLAS-backed numerics.
- **Primary role:** `DSL-host/metaprogramming`
- **Secondary roles:** `program`, `specification/modeling`, `interactive/teaching`
- **What the kernel checks:** Types and program transformations. Many correctness facts are assumed. `sorry_proof` is a macro for `axiom sorryProofAxiom {P : Prop} : P` (`SciLean/Util/SorryProof.lean`), and a grep counts over 2,000 uses in `SciLean/`. The kernel checks that rewrites such as `autodiff` are well-typed equalities, relative to these axioms.
- **Certified vs only expressed:** Mostly expressed. Symbolic objects (`∇`, `limit`, `odeSolve`) state what a program should compute. Tactics then rewrite them into runnable Float code, and the approximation steps are justified by `sorry_proof` (for example `examples/HarmonicOscillator.lean`). Some algebraic and AD rule theorems are proven, but the library does not aim for end-to-end certification.
- **Output artifact:** Executables (wave equation, harmonic oscillator, MNIST, and others), a library, and ProofWidgets visualisations.
- **Author mode:** Human (Tomáš Skřivan per the git log). I found no AI markers.
- **Translation direction:** None. Lean is both the source and the target, compiled through Lean's own backend plus C/BLAS FFI.
- **Creative idea:** A program is written as a mathematical specification, such as a gradient or the exact ODE solution, and a tactic proof script compiles it into executable numerics. The `approx … by` command makes the rewrite proof the compiler.
- **Why Lean?:** The README argues that Lean "can understand mathematics", which allows code transformations guided by formal math and symbolic, noncomputable functions as first-class values. My assessment: Python/JAX gives AD but no symbolic `limit`/`integral` objects tied to a math library. Coq/Isabelle do not produce efficient native code as easily.
- **Notable techniques:**
  - The `approx` command, elaborated into a `def` whose body is the result of a tactic rewrite (`SciLean/Util/Approx/Basic.lean`, `ApproxLimit.lean`).
  - The `autodiff` tactic and conv mode, built on `lsimp` and `fun_trans` simprocs (`SciLean/Tactic/Autodiff.lean`, `SciLean/Tactic/FunTrans/`).
  - The `sorry_proof` and `sorry_data` axioms, which keep code compilable while leaving obligations open (`SciLean/Util/SorryProof.lean`).
  - The `rewrite_by` term elaborator and C FFI via `precompileModules` (`SciLean/Util/RewriteBy.lean`, `lakefile.lean`).
- **Heuristic check:** The Phase 1 guess was `spec+proof + DSL/metaprogramming + program + computation/examples + interactive`. I mostly agree. "spec+proof" overstates the proof side, because proofs are largely deferred with an axiom.
- **Evidence:** `README.md`, `lakefile.lean`, `examples/HarmonicOscillator.lean`, `SciLean/Util/SorryProof.lean`, `SciLean/Util/Approx/Basic.lean`, `SciLean/Util/RewriteBy.lean`, `SciLean/Tactic/Autodiff.lean`, directory listings of `SciLean/{AD,Tactic,Meta}`.
