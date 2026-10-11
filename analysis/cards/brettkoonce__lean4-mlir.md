# brettkoonce/lean4-mlir

- **Domain:** Deep learning: neural networks are specified in Lean, compiled to StableHLO/MLIR, and trained on GPUs through XLA/PJRT or IREE. This is the companion code for a book.
- **Primary role:** `certifier-software`
- **Secondary roles:** `program`, `specification/modeling`, `interactive/teaching`
- **What the kernel checks:** Full proofs over ℝ. Each layer's backward pass is the Jacobian-transpose of its forward (Mathlib `fderiv`), composed up to whole-network VJPs, with no project axioms per `TRUST.md`. The rendered MLIR text is tied to denoted `SHlo` nodes (`LeanMlir/Proofs/Codegen/MlpRender.lean`). Phase 1 also counts many `decide`/`guard` uses and 107 `sorry`.
- **Certified vs only expressed:** Proven: the VJP identities and that each emitted SGD update node denotes the certified step. Trusted (stated in `TRUST.md`): ℝ→Float32 numerics, per-op text printing, the XLA/IREE compilers, and the C runtime in `ffi/`. Cross-checked only, not proven: agreement with a JAX reference. The accuracy numbers are measured.
- **Output artifact:** Generated MLIR files (`verified_mlir/`), about 200 training executables, theorems, and a leanblueprint book.
- **Author mode:** Mixed. The commits are by the human author with `Co-Authored-By: Claude Opus 5.5` trailers (git log).
- **Translation direction:** Out of Lean (Lean `NetSpec` to StableHLO text).
- **Creative idea:** The gradients are derived and proven in Lean at code-generation time, and the GPU trains on exactly the MLIR bytes those proofs describe. Lean replaces the autograd library.
- **Why Lean?:** Partly stated: the README says there is "no Python at run time and no autograd library" and that the gradients are "machine-checked over the reals". My assessment: Mathlib's `fderiv` and the ability to run Lean as a code generator in the same language are what Python/JAX and Dafny lack.
- **Notable techniques:**
  - An `SHlo` AST with a denotation and a `pretty` printer, so the train-step text is assembled from proven nodes (`LeanMlir/Proofs/Codegen/MlpRender.lean`, `RenderKit.lean`).
  - An MLIR code generator of about 8.5k lines from `NetSpec` (`LeanMlir/MlirCodegen.lean`, `LeanMlir/Spec.lean`).
  - `@[extern]` runtime entry points for PJRT/IREE (`LeanMlir/IreeRuntime.lean`, `F32Array.lean`).
  - An axiom audit plus a `comparator` re-check of the headline theorems (`TRUST.md`, `tests/comparator/`).
- **Heuristic check:** The Phase 1 guess was `certifier + program + computation/examples`. I agree. I would add that much of the program side is code generation out of Lean.
- **Evidence:** `README.md`, `TRUST.md` (fetched), `LeanMlir/Spec.lean`, `LeanMlir/Proofs/Codegen/MlpRender.lean`, `LeanMlir/MlirCodegen.lean` (def list), directory listings, git log.
