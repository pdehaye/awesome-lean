# verse-lab/loom

- **Domain:** Building program verifiers. It is a framework for deriving weakest-precondition (WP) verifiers for monadic, possibly nondeterministic imperative code.
- **Primary role:** `DSL-host/metaprogramming`
- **Secondary roles:** `certifier-software`, `specification/modeling`
- **What the kernel checks:** Full proofs of the framework's metatheory: monad-algebra laws, WP rules, and the theorem that extraction refines WP (`ExtractNonDet.extract_refines_wp`). The kernel also checks VCs closed by `aesop`/`auto`. But `loom_smt` closes goals with `axiom trust_smt : ∀ p, p` once Z3/CVC5 says unsat (`Loom/SMT.lean`), and `loom_solve_async` admits goals with `sorry` (`CaseStudies/Tactic.lean`).
- **Certified vs only expressed:** The WP calculus and its soundness are certified. Example programs in Cashmere (a toy bank-balance language) are proven correct by `prove_correct … by loom_solve`. Any goal discharged through `loom_smt` rests on trusting the solver.
- **Output artifact:** A Lean library (verifier-building toolkit) plus example theorems. Programs are also runnable via `#eval` (`Cashmere.lean`).
- **Author mode:** Human (academic group, paper artifact: the README cites paper sections). I saw no AI markers.
- **Translation direction:** None. Programs are written directly as Lean `do`-code with new syntax.
- **Creative idea:** Uses Lean's `do`-notation as the base of a "verifier factory": you pick a monad-transformer stack, and typeclass instances (Monad Transformer Algebras) produce the WP generator, with angelic or demonic nondeterminism selected by an `open` of a namespace.
- **Why Lean?:** Not stated. My assessment: the design depends on shallow embedding in an executable monad, typeclass resolution and user-extensible syntax and elaborators. Dafny has no such extensibility, and Coq/Isabelle programs can't be run as directly.
- **Notable techniques:**
  - `MAlgOrdered`/`MAlgLift` typeclasses give WP for transformer stacks (`Loom/MonadAlgebras/Defs.lean`).
  - The `#derive_lifted_wp` and `#gen_spec` commands generate WP lemmas through metaprogramming (`Loom/Meta.lean`).
  - `while … invariant … decreasing` and `let x :| p` are added as `doElem` syntax (`CaseStudies/Macro.lean`). Cashmere's `bdef`/`prove_correct` commands are defined in `CaseStudies/Cashmere/Syntax_Cashmere.lean`.
  - An SMT bridge sends queries through lean-auto and retries with the other solver on `unknown` (`Loom/SMT.lean`).
- **Heuristic check:** The Phase 1 guess was `spec+proof + DSL/metaprogramming + interactive`. I agree with the DSL emphasis. "Interactive" is minor: ProofWidgets is only imported in `CaseStudies/Tactic.lean`. Velvet no longer lives here; the README still describes `CaseStudies/Velvet`, but those files are absent and the last commit says Velvet moved to its own repo.
- **Evidence:** `README.md`, `lakefile.lean`, `Loom/MonadAlgebras/Defs.lean`, `Loom/Meta.lean`, `Loom/SMT.lean`, `Loom/MonadAlgebras/NonDetT/Extract.lean`, `CaseStudies/Macro.lean`, `CaseStudies/Tactic.lean`, `CaseStudies/Cashmere/Cashmere.lean`, file listing.
