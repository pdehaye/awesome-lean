# leanprover-community/iris-lean

- **Domain:** A Lean 4 port of Iris, a higher-order concurrent separation logic framework, including its proof mode (MoSeL), the `IProp` model, and the HeapLang example language.
- **Primary role:** `certifier-software`
- **Secondary roles:** `DSL-host/metaprogramming` (the proof mode tactics, HeapLang syntax, custom typeclass synthesis), `coordination/trust-infrastructure` (tooling that tracks the port against Iris-Rocq)
- **What the kernel checks:** Full proofs. Phase 1 counts about 5,100 theorems and 0 `sorry`. The program logic (weakest preconditions, adequacy) is proven over `IProp` (`Iris/Iris/ProgramLogic/Adequacy.lean`). `Iris/Iris/Examples/ClosedProofs.lean` shows how to get closed, pure Lean propositions out of Iris proofs.
- **Certified vs only expressed:** Certified: the algebra (CMRAs/COFEs), the BI laws, the program logic, and HeapLang's primitive laws. Only expressed: HeapLang example programs written with `hl(...)` (`Iris/Iris/Examples/HeapLang.lean`). I did not check how many of these examples come with proofs.
- **Output artifact:** A library of theorems and tactics, plus a JSON dump and HTML report of porting progress (`lake exe dumpPortingData`, `scripts/check_porting.py`).
- **Author mode:** Mixed policy, human authorship asserted. `docs/ai.md` permits AI assistance but says only humans are co-authors and asks for proofs that read like the Rocq originals.
- **Translation direction:** Into Lean, from Rocq: a manual port. Each ported declaration is tagged with `@[rocq_alias]` (`Iris/Iris/Std/RocqPorting.lean`, used in about 180 files).
- **Creative idea:** iris-lean rebuilds a Rocq-style proof environment inside Lean. It adds an embedded separation-logic proof mode with its own `i*` tactics and a Rocq-like typeclass resolution procedure. Porting progress against the upstream Rocq development is tracked by attributes in the source, which are then compiled into a report.
- **Why Lean?:** Not stated. My assessment: the project brings Iris to Lean users and to Mathlib-based constructions (`IrisMath/`). Lean's macro and elaborator system replaces Rocq's Ltac and notation machinery for MoSeL.
- **Notable techniques:**
  - About 30 proof-mode tactics (`istart`, `iapply`, `iframe`, `iloeb`, …): `Iris/Iris/ProofMode/Tactics/`.
  - Custom typeclass synthesis that tolerates mvars in input positions (`ipm_class`): `Iris/Iris/ProofMode/SynthInstance.lean`.
  - An embedded HeapLang DSL through `declare_syntax_cat hl_exp` and `hl(...)`: `Iris/Iris/HeapLang/Notation.lean`.
  - A delaborator for entailments: `Iris/Iris/ProofMode/Display.lean`.
- **Heuristic check:** The Phase 1 guess was `certifier + DSL/metaprogramming + computation/examples + interactive`. I agree on certifier plus DSL. "Interactive" fits only in the sense of a proof-mode UI. I see no meaningful computation role.
- **Evidence:** `readme.md`, `Iris/lakefile.toml`, `docs/ai.md`, `scripts/README.md`, `IrisMath/README.md`, `Iris/Iris/ProofMode/SynthInstance.lean`, `Iris/Iris/ProofMode/Tactics/*` (greps), `Iris/Iris/Examples/HeapLang.lean`, `Iris/Iris/Examples/ClosedProofs.lean`, `Iris/Iris/HeapLang/Notation.lean`, `Iris/Iris/Std/RocqPorting.lean`.
