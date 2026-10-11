# leanprover-community/duper

- **Domain:** Automated theorem proving: a higher-order superposition prover written in Lean that produces proofs (similar to Isabelle's Metis).
- **Primary role:** `DSL-host/metaprogramming`
- **Secondary roles:** `program` (a `duper` executable for TPTP benchmarks), `certifier-math` (proofs it produces are kernel-checked)
- **What the kernel checks:** For the `duper` tactic, the kernel checks a reconstructed proof term (`Duper/ProofReconstruction.lean`, `mkClauseProof`). The calculus code itself is not verified. About 30 files contain small `theorem`s that justify individual inference rules, e.g. `Duper/Rules/BoolSimp.lean` (`rule1Theorem`…). The TPTP executable only prints an SZS status: it declares the base logic as `axiomDecl`s and kernel-checks nothing beyond that (`Main.lean`).
- **Certified vs only expressed:** It certifies each goal it closes, by producing a proof term. It does not prove that the prover is sound or complete. In TPTP mode the output is only a verdict.
- **Output artifact:** A tactic (`duper [facts] {options}`), proof terms, and an executable that prints SZS status lines.
- **Author mode:** Human. The README names Clune, Qian and Bentkamp. I found no evidence of AI authorship.
- **Translation direction:** Into Lean: `Duper/TPTPParser/` parses TPTP problems into Lean `Expr`s.
- **Creative idea:** Duper is a complete saturation prover (clauses, unification, term orders, subsumption tries) written as ordinary Lean metaprograms. Each inference step records how to rebuild its conclusion, so a saturation run becomes a kernel-checkable Lean proof without any external solver.
- **Why Lean?:** Not stated. My assessment: writing the prover inside Lean avoids translating foreign certificates, because proof reconstruction works directly on `Expr`. The README compares it to Isabelle's Metis, and lean-auto uses it as its native backend.
- **Notable techniques:**
  - Superposition rules with per-rule proof builders (`mkSuperpositionProof`): `Duper/Rules/Superposition.lean`.
  - Proof reconstruction from the clause DAG, including Skolem handling (`PRM.matchSkolem`): `Duper/ProofReconstruction.lean`.
  - Higher-order unification procedure: `Duper/DUnif/`.
  - Monomorphization through lean-auto before saturation: `Duper/Tactic.lean` (`Auto.monoPrepInterface`).
- **Heuristic check:** The Phase 1 guess was `spec+proof + DSL/metaprogramming + (ships tooling executables)`. I partly disagree. The "proof" share is mostly helper lemmas and `DuperOnMathlib` examples. Duper is a metaprogram, not a specification.
- **Evidence:** `README.md`, `lakefile.lean`, `Main.lean`, `Duper/ProofReconstruction.lean` (head), `Duper/Tactic.lean` (grep), `Duper/Rules/Superposition.lean`, `Duper/Rules/BoolSimp.lean` (grep), `DuperOnMathlib/` listing.
