# lean-machines-central/lean-machines

- **Domain:** Formal modeling and stepwise refinement of stateful systems, inspired by Event-B.
- **Primary role:** `specification/modeling`
- **Secondary roles:** `certifier-software`
- **What the kernel checks:** Proof obligations as structure fields: an `OrdinaryEvent` cannot be built without a `safety` proof that the action preserves the machine invariant; refined events need `strengthening` and `simulation` proofs. The library also proves some framework lemmas (23 theorems), relies on 5 axioms, and has unfinished `sorry`s in the non-deterministic event algebra.
- **Certified vs only expressed:** Certified (by users of the framework): invariant preservation, guard strengthening, simulation, convergence of their models. The framework itself only defines the shapes; some extensionality facts are assumed as axioms (`_Action_ext_ax`, flagged in a comment as possibly unprovable) and parts of `NonDet/Algebra/Convergent.lean` are `sorry`.
- **Output artifact:** A library for writing machine models; the `lean-machines` executable only prints a version string (`Main.lean`).
- **Author mode:** Human (comments such as "don't know how to finish this", no AI markers seen).
- **Translation direction:** None (README: not compatible with Event-B/Rodin; a translator is "under consideration").
- **Creative idea:** Event-B's proof obligations become fields of dependent structures, so correctness-by-construction is enforced by the type checker, and events are also given Functor/Monad/Category/Arrow instances so they can be combined like functional programs.
- **Why Lean?:** Stated partly: refinement "in the context of a functional programming environment" (README). My assessment: dependent types let proof obligations live inside the data, which Rodin keeps as separate side conditions; Dafny or Python could not express the categorical event algebra this way.
- **Notable techniques:**
  - `class Machine` with `invariant`, and `_EventPO`/`OrdinaryEvent` bundling the safety obligation (`LeanMachines/Event/Basic.lean`, `LeanMachines/Event/Ordinary.lean`).
  - `class Refinement` and `_REventPO` with `strengthening`/`simulation` fields (`LeanMachines/Refinement/Relational/Basic.lean`); functional and strong refinement variants under `Refinement/Functional`, `Refinement/Strong`.
  - Lawful Functor/Applicative/Monad/Category/Arrow instances for events (`LeanMachines/Event/Algebra/Basic.lean`).
  - Catalogue of event kinds and their obligations (`docs/EventZoo.md`).
- **Heuristic check:** the Phase 1 guess was `specification/modeling library + (ships tooling executables)`. Agree on the role; the "tooling executable" is only a version printer.
- **Evidence:** `README.md`, `lakefile.lean`, `Main.lean`, `docs/EventZoo.md` (start), `LeanMachines/Event/Basic.lean`, `LeanMachines/Event/Ordinary.lean`, `LeanMachines/Refinement/Relational/Basic.lean`, grep of axioms/sorry/instances across `LeanMachines/`.
