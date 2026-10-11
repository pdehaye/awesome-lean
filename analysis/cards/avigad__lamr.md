# avigad/lamr

- **Domain:** Logic and automated reasoning course (CMU 15-311): SAT, SMT, first-order provers, decision procedures.
- **Primary role:** `program`
- **Secondary roles:** `interactive/teaching`, `DSL-host/metaprogramming`, `certifier-software` (minor)
- **What the kernel checks:** Mostly computation via `#eval` (206 occurrences). Few theorems (29); the DPLL correctness specs are `admit`ted (`LAMR/Examples/using_sat_solvers/dpll.lean`). Results from CaDiCaL, Z3 and Vampire are trusted, not checked.
- **Certified vs only expressed:** Certified: small textbook proof examples (induction, equational reasoning, proof terms). `DisjointSetWithProofs` carries justifications as data (for congruence closure) and is not itself verified. Only expressed/run: formula syntax, CNF/Tseitin transformations, DPLL, unification, Fourier-Motzkin, encodings such as sudoku and magic squares.
- **Output artifact:** `#eval` output in the editor, two executables (`dpll`, `colorEncode`), and DIMACS / SMT-LIB / TPTP problem files passed to external solvers.
- **Author mode:** Human (course material; no AI markers seen).
- **Translation direction:** Out of Lean: Lean data structures are serialized to DIMACS CNF, SMT-LIB s-expressions and TPTP, and solver output is parsed back.
- **Creative idea:** Lean is used as the scripting language that drives external solvers, with embedded notations (`prop!{}`, `cnf!{}`, `fo!{}`, `sexp!{}`) for writing logic and solver input inside ordinary Lean programs.
- **Why Lean?:** Not stated directly; the README presents Lean as both programming language and theorem prover. My assessment: one language covers implementing logic algorithms, proving things about them, and writing custom syntax; Python would lose the proof side and the syntax extensions.
- **Notable techniques:**
  - `declare_syntax_cat` for propositional formulas, literals and CNF (`LAMR/Util/Propositional/Syntax.lean`).
  - S-expression DSL with a custom `generalIdent` parser and splice syntax `...{}` (`LAMR/Util/FirstOrder/Smt.lean`), used in `LAMR/Examples/using_smt_solvers/magicSquares.lean`.
  - DIMACS export and CaDiCaL invocation via `IO.Process` (`LAMR/Util/Propositional/SatSolver.lean`); DRAT proof decoding (`LAMR/Util/Propositional/DRAT.lean`; I did not see it verified).
  - TPTP export and Vampire calls (`LAMR/Util/FirstOrder/Atp.lean`, `LAMR/Examples/using_first_order_theorem_provers/aunt_agatha.lean`).
- **Heuristic check:** the Phase 1 guess was `DSL/metaprogramming + program + computation/examples + interactive`. Agree.
- **Evidence:** `README.md`, `lakefile.lean`, `LAMR/Util/Propositional/SatSolver.lean`, `Syntax.lean` (grep), `DRAT.lean`, `LAMR/Util/FirstOrder/Smt.lean`, `Atp.lean` (grep), `LAMR/Examples/using_smt_solvers/magicSquares.lean`, `LAMR/Examples/using_sat_solvers/dpll.lean`, `LAMR/Examples/using_first_order_theorem_provers/aunt_agatha.lean`, `LAMR/Util/DisjointSetWithProofs.lean` (grep).
