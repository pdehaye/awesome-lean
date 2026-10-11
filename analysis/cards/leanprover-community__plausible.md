# leanprover-community/plausible

- **Domain:** QuickCheck-style property-based testing for Lean propositions, used as a tactic.
- **Primary role:** `DSL-host/metaprogramming`
- **Secondary roles:** `certifier-software`
- **What the kernel checks:** tests, not proofs. The `plausible` tactic runs random tests and, if none fails, calls `admitGoal` ("behaves like `admit`", `Plausible/Tactic.lean`). The goal stays unproven (sorry).
- **Certified vs only expressed:** `TestResult.failure` carries a term of type `¬ p`, built from `Decidable` instances and combined through `Testable` instances, so a reported counterexample comes with a refutation by construction (`Plausible/Testable.lean`). But it runs via `unsafe evalExpr`, so the kernel does not re-check it. Success is only "no counterexample found".
- **Output artifact:** verdict (counterexample message or silent admit); a library of generators and shrinkers.
- **Author mode:** human (Simon Hudon, Kim Morrison, Ernest Ng in headers; ported from mathlib3); no AI-agent files found.
- **Translation direction:** none.
- **Creative idea:** Testing that lives inside the proof assistant: a goal is reverted into a `Prop`, and typeclass resolution assembles a `Testable` instance from its structure. Typed results mean a counterexample is itself a refutation of `p`.
- **Why Lean?:** not stated. Own assessment: same idea as Isabelle's Quickcheck/Nitpick and Coq's QuickChick. Lean's version gains direct tactic integration and `deriving Arbitrary`. Python's Hypothesis cannot test statements written as `Prop`s.
- **Notable techniques:**
  - `Testable p` class with instance-driven decomposition of `∀`, `→`, `∧`, `∃` (`Plausible/Testable.lean`).
  - `mk_decorations` tactic used as an auto-param to annotate the proposition with variable names (`Plausible/Testable.lean`, `Decorations`).
  - Deriving handlers for `Arbitrary` (fuel-based) and `Shrinkable` on inductive types (`Plausible/DeriveArbitrary.lean`, `Plausible/DeriveShrinkable.lean`).
  - Tactic that builds `Testable.check` as an `Expr`, evaluates it, then admits the goal (`Plausible/Tactic.lean`).
- **Heuristic check:** the Phase 1 guess was `DSL/metaprogramming + program + computation/examples`. Mostly agree on metaprogramming. Disagree with `program`: there is no executable, and it is a tactic library. "computation" is right in spirit, since the checks are evaluated tests rather than kernel `decide`.
- **Evidence:** `README.md`, `lakefile.toml`, `Plausible/Tactic.lean`, `Plausible/Testable.lean` (parts), `Plausible/DeriveArbitrary.lean` (head).
