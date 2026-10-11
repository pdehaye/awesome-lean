# strata-org/Strata

- **Domain:** A program-analysis platform: extensible intermediate-representation "dialects" (a Boogie-like Core, C_Simp, B3, Laurel for Java/Python/JS, SMT-LIB, GOTO) plus verification-condition generation and backends.
- **Primary role:** `program`
- **Secondary roles:** `certifier-software`, `DSL-host/metaprogramming`, `specification/modeling`
- **What the kernel checks:** Full proofs of many transformation and semantics properties: about 3.3k theorems, for example `Strata/Transform/CallElimCorrect.lean`, `StructuredToUnstructuredCorrect.lean`, `DetToKleeneCorrect.lean`. Much test coverage is `#guard_msgs` and `#eval` (computation). The normal `verify` path trusts external SMT solvers.
- **Certified vs only expressed:** Several passes are proven to preserve semantics, against operational semantics in `Strata/DL/Imperative/`. The main verifier pipeline runs as ordinary Lean code that calls cvc5/z3. Optionally, `gen_smt_vcs` turns a program's generated VCs into Lean goals that can be closed with `grind`, as in `StrataTest/.../GenSMTVCsFuncPrecond.lean`.
- **Output artifact:** Executables (`StrataToCBMC`, `StrataCoreToGoto` writing CProver GOTO JSON, `laurelJavaGen`), verification verdicts, and theorems.
- **Author mode:** Human, industrial team. The shallow clone shows only `strata-bot` commits, and I found no AI markers, so I can't confirm further.
- **Translation direction:** Both ways. Into Lean: source languages are parsed into dialect ASTs. Out of Lean: SMT-LIB, CBMC GOTO, and generated Java code.
- **Creative idea:** Lean serves as an MLIR-like language workbench. Dialects are declared inline with `#dialect`/`#strata` blocks, as in `Examples/Lean/SQL.lean`. A "meta-verifier" reflects the same SMT queries the tool would send to a solver back into kernel-checkable Lean goals.
- **Why Lean?:** `docs/Architecture.md`: "implemented in Lean to enable both verification of its own implementation as well as … use of Lean to reason about programs written in Strata dialects." My assessment: Dafny or Python would lose the in-tree proofs about passes, and Coq would lose the performant executable tooling.
- **Notable techniques:**
  - Dialect grammars written as `op … : Cat => "syntax"` in the external StrataDDM DSL (`Strata/Languages/C_Simp/DDMTransform/Parse.lean`).
  - The `smtVCsCorrect` definition and the `gen_smt_vcs` reflection tactic (`Strata/MetaVerifier.lean`).
  - Pipeline phases with fact-set contracts (`Strata/Pipeline/PhaseContract.lean`).
  - CBMC/GOTO backend (`Strata/Backends/CBMC/`, `StrataCoreToGoto.lean`).
- **Heuristic check:** The Phase 1 guess was `spec+proof + program + computation/examples`. I agree. The large `opaque` count (1577) is probably DDM `op` declarations miscounted, not Lean `opaque`.
- **Evidence:** `README.md`, `lakefile.toml`, `docs/Architecture.md`, `Strata/MetaVerifier.lean`, `Strata/Transform/CallElimCorrect.lean` (theorem list), `Strata/Languages/C_Simp/DDMTransform/Parse.lean`, `Examples/Lean/SQL.lean`, `StrataTest/Languages/Core/Examples/GenSMTVCsFuncPrecond.lean`, `StrataCoreToGoto.lean`, directory listings.
