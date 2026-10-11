# leanprover-community/nng4

- **Domain:** Introductory proof teaching: Peano arithmetic on a home-made natural number type (the Natural Number Game).
- **Primary role:** `interactive/teaching`
- **Secondary roles:** `DSL-host/metaprogramming`, `certifier-math` (minor)
- **What the kernel checks:** Full proofs of each level's `Statement` (the reference solution at build time, the player's at play time), but relative to axioms: `MyNat.add`, `mul`, `pow` are `opaque` with `add_zero`/`add_succ` etc. declared as `axiom`s.
- **Certified vs only expressed:** Certified: textbook facts (`zero_add`, `add_comm`, ...) relative to the declared axioms. Nothing new about mathematics; the point is the player's experience. An `xyzzy` cheat tactic uses its own axiom.
- **Output artifact:** A playable game (levels, hints, inventory) served by lean4game; `.po` translation files.
- **Author mode:** Human (ported from the Lean 3 game; no AI markers seen).
- **Translation direction:** None (the content was ported from Lean 3).
- **Creative idea:** The game weakens and reshapes standard Lean on purpose (opaque, axiomatized addition; `rfl` restricted to reducible transparency; `rw` that does not close goals by `rfl`) so that the kernel enforces the intended teaching path instead of letting automation skip it.
- **Why Lean?:** Not stated beyond using the lean4game engine. My assessment: it needs Lean 4's ability to redefine core tactics in user code; Python cannot check the proofs at all.
- **Notable techniques:**
  - `opaque add` plus `axiom add_zero`/`add_succ` instead of a recursive definition (`Game/MyNat/Addition.lean`).
  - Redefined `rw` and `rfl` tactics (`Game/Tactic/Rw.lean`, `Game/Tactic/Rfl.lean`).
  - `decide` macro preceded by a custom simp set `MyNat_decide` that unfolds numerals (`Game/Tactic/Decide.lean`, `Game/Tactic/LabelAttr.lean`).
  - Levels written in the lean4game DSL with goal-dependent `Hint`s (`Game/Levels/Addition/L01zero_add.lean`); lakefile picks a local or remote GameServer via `#eval` (`lakefile.lean`).
- **Heuristic check:** the Phase 1 guess was `spec+proof + game/teaching`. Partly disagree: the proofs are teaching material resting on axiomatized arithmetic, so "spec+proof" overstates it; teaching is the primary role.
- **Evidence:** `README.md`, `lakefile.lean`, `Game/MyNat/Definition.lean`, `Game/MyNat/Addition.lean`, `Game/Tactic/Xyzzy.lean`, `Rw.lean`, `Rfl.lean`, `Decide.lean`, `LabelAttr.lean`, `Game/Levels/Addition/L01zero_add.lean`, grep of axioms/elabs under `Game/`.
