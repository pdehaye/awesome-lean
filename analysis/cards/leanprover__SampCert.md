# leanprover/SampCert

- **Domain:** Differential privacy: verified samplers (discrete Laplace/Gaussian) and DP mechanisms (pure, zCDP, approximate DP, queries such as histograms, sparse vector, bounded mean).
- **Primary role:** `certifier-software`
- **Secondary roles:** `program`, `DSL-host/metaprogramming`
- **What the kernel checks:** Full proofs over Mathlib (0 `sorry` per Phase 1; e.g. `DiscreteGaussianSample_normalizes` in `SampCert/Samplers/Gaussian/Properties.lean`). Execution goes through `@[extern]` C++ code, which the kernel does not check.
- **Certified vs only expressed:** Proven: the sampler programs produce the intended distributions, and the mechanisms satisfy their DP bounds. Only expressed or trusted: the runtime behaviour of `probPure`, `probBind`, `probUniformByte`, `probWhile` and `PMF.run`. In proofs these are functions `α → ℝ≥0∞`. At runtime they are replaced by `@[extern]` symbols from `ffi.cpp`. The Dafny output is also unverified (the printer writes `{:verify false}`).
- **Output artifact:** Theorems; a Lean executable (`test`, `check`); generated Dafny methods, which the README says are deployed in AWS Clean Rooms.
- **Author mode:** Human (Tristan, de Medeiros, per the README and git log).
- **Translation direction:** Out of Lean (SLang definitions are turned into Dafny source).
- **Creative idea:** A small probabilistic language (SLang) is given a measure-valued meaning in proofs and a C++ sampling meaning at runtime, and the same definitions are also compiled to Dafny for production.
- **Why Lean?:** The README cites heavy Mathlib use (for example the Poisson summation formula). My assessment: Dafny is the deployment target but has no library for analysis or probability. Coq/Isabelle could host the proofs but would not give the same in-language extractor and FFI route.
- **Notable techniques:**
  - A monad whose values are `α → ℝ≥0∞`, with `@[extern "prob_Bind"]` overriding it for execution (`SampCert/SLang.lean`).
  - Custom attributes `export_dafny` and `align_dafny` that walk elaborated definitions and save Dafny methods in an environment extension (`SampCert/Extractor/Export.lean`, `Align.lean`, `IRToDafny.lean`).
  - The `#print_dafny_exports` and `#print_vmc_exports` commands, which write `.dfy` files (`FastExtract.lean`, `SampCert/Extractor/VMC.lean`).
  - Lake targets that build a C++ FFI static or shared library (`lakefile.lean`).
- **Heuristic check:** The Phase 1 guess was `certifier + program`. I agree, and add the metaprogramming extractor that produces Dafny.
- **Evidence:** `README.md`, `lakefile.lean`, `SampCert/SLang.lean`, `SampCert/Extraction.lean`, `SampCert/Extractor/{Export,Align,IRToDafny,VMC}.lean`, `FastExtract.lean`, `VMC.lean`, `SampCertCheck.lean`, `Test.lean`, `SampCert/Samplers/Gaussian/Properties.lean` (grep).
