# verse-lab/veil

- **Domain:** Specifying, model-checking and proving safety of state-transition systems, mainly distributed protocols (Ivy/TLA+-style).
- **Primary role:** `DSL-host/metaprogramming`
- **Secondary roles:** `specification/modeling`, `certifier-software`, `program`, `interactive/teaching`
- **What the kernel checks:** It depends on the mode. `#check_invariants` discharges inductiveness VCs with SMT (cvc5 via lean-smt). The option `veil.smt.trust` **defaults to true** (`Veil/Base.lean`), so by default unsat results are trusted rather than reconstructed into proofs. Interactive Lean proofs are also possible. `#model_check` is explicit-state testing by computation, and the README says so explicitly. The model checker's own invariants have kernel-checked lemmas (`Veil/Core/Tools/ModelChecker/Concrete/SequentialLemmas.lean`).
- **Certified vs only expressed:** Protocol invariants are proven (solver-trusted by default). Model checking of a finite instance such as `node := Fin 4` only tests. The TLA+/Ivy examples are hand-written ports that keep the `.tla` originals alongside. I found no automatic translator.
- **Output artifact:** Verdicts (proved, counterexample traces) shown in InfoView widgets, theorems, and executable specifications.
- **Author mode:** Human (research group; heavily commented tutorial). No AI markers seen.
- **Translation direction:** Out of Lean: VCs go to SMT-LIB. Into Lean: protocols are ported by hand.
- **Creative idea:** One `veil module` declaration is elaborated twice. It becomes a two-state transition relation for SMT verification and an executable step function for a model checker that runs in the editor. The checker's search is itself written and partly proven in Lean.
- **Why Lean?:** The README says it is "foundational", with "the full power of a modern higher-order proof assistant for when automation falls short." My assessment: Ivy or TLC give push-button checking but no fallback to interactive proof. Lean adds that, plus executable specs and widgets in one tool.
- **Notable techniques:**
  - Module DSL: `type`, `relation`, `action`, `invariant`, `#gen_spec`, `#model_check`, with the frontend in `Veil/Frontend/DSL/`. A walkthrough is in `Examples/Tutorial/Ring.lean`.
  - A concurrent VC manager or server runs SMT jobs during elaboration (`Veil/Core/Tools/Verifier/Server.lean`).
  - The explicit-state model checker uses sharded hash sets and map-reduce (`Veil/Core/Tools/ModelChecker/Concrete/`), with `native_decide` side conditions in `Veil/Util/ShardedSetUInt.lean`.
  - The weakest-precondition layer comes from Loom (`lakefile.lean` requires `Loom`). A ProofWidgets/npm UI shows counterexample traces (`Veil/Core/UI/`).
- **Heuristic check:** The Phase 1 guess was `DSL/metaprogramming + program + computation/examples + interactive`. I agree, and would add `specification/modeling`. Note that by default the proofs trust SMT.
- **Evidence:** `README.md`, `lakefile.lean`, `Examples/Tutorial/Ring.lean`, `Examples/TLA/Bakery.lean`, `Veil/Base.lean` (option), `Veil/Frontend/DSL/Tactic/Core.lean`, `Veil/Core/Tools/Verifier/Server.lean`, `Veil/Core/Tools/ModelChecker/Concrete/SequentialLemmas.lean`, directory listings.
