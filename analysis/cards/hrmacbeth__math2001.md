# hrmacbeth/math2001

- **Domain:** Undergraduate intro-to-proof course (Fordham Math 2001), companion code to the book *The Mechanics of Proof*.
- **Primary role:** `interactive/teaching`
- **Secondary roles:** `DSL-host/metaprogramming`, `certifier-math` (worked examples only)
- **What the kernel checks:** Full proofs for the worked examples and the small `Library/Theory` files; exercises and homework are `sorry` placeholders (564 sorries) for students to fill in. Homework is graded by an external autograder via `@[autograded n]`.
- **Certified vs only expressed:** Certified: elementary results (parity, divisibility, modular arithmetic, GCD) and book examples. Only expressed: exercise statements, which students prove.
- **Output artifact:** Exercise files for an editor (Gitpod/VS Code), homework sheets for autograding, a `#truth_table` widget.
- **Author mode:** Human (copyright headers by Macbeth and named contributors).
- **Translation direction:** None.
- **Creative idea:** The course reshapes Mathlib into a smaller, pedagogical proof language: strong automation (`linarith`, `simp`, `decide`, `aesop`, `tauto`) is replaced by macros that fail, and weaker purpose-built tactics (`addarith`, `numbers`, `extra`, `cancel`, `rel`) take their place.
- **Why Lean?:** Not stated in the files read. My assessment: Mathlib's tactic framework makes it cheap to build deliberately weakened variants of existing tactics; that is harder in Isabelle or Coq and impossible in Python.
- **Notable techniques:**
  - Disabling tactics by shadowing them with `fail` macros (`Library/Basic.lean`).
  - `addarith`: `linarith` restricted to given hypotheses and no rescaling (`Library/Tactic/Addarith.lean`); `numbers` built on `norm_num` core (`Library/Tactic/Numbers/Basic.lean`).
  - `math2001_init` command that sets options and erases simp/ext/instance/norm_num attributes at the start of each file (`Library/Config/Initialize.lean`).
  - `#truth_table` command that turns a propositional term into a `BExpr` and renders a widget (`Library/Tactic/TruthTable.lean`); autograded homework (`Math2001/Homework/hw6.lean`).
- **Heuristic check:** the Phase 1 guess was `certifier + DSL/metaprogramming + computation/examples + interactive`. Disagree on order: "certifier" should not lead. The proofs are teaching material and most exercises are sorried; teaching is the primary role.
- **Evidence:** `README.md`, `lakefile.lean`, `Library/Basic.lean`, `Library/Config/Initialize.lean`, `Library/Tactic/Addarith.lean`, `Library/Tactic/Rel.lean`, `Library/Tactic/TruthTable.lean`, grep of `Library/Tactic/*`, `Math2001/01_Proofs_by_Calculation/02_Proving_Equalities_in_Lean.lean`, `Math2001/Homework/hw6.lean`.
