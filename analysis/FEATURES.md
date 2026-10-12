# Lean language features worth exploring

A shortlist of Lean 4 language features, grouped by what they let you do, with how many of the analyzed repos use each. The counts come from [`feature_scan.sh`](feature_scan.sh), a keyword search over the 74 cloned Lean repos (the lean4 compiler repo and the Lean Pool aggregate are excluded). They show *where* a feature appears, not how deeply it is used.

## A. Extending the language itself

| # | Feature | Repos | Most interesting users | Why explore it |
|---|---|--:|---|---|
| 1 | **Custom syntax categories** (`declare_syntax_cat`) | 22 | Alloy (the full C grammar), Strata (dialects), Verso, Veil, Iris-Lean | How far a foreign language can be embedded inside Lean. |
| 2 | **Macros vs elaborators** (`macro`, `elab`) | 47 / 45 | Verso (a document becomes a Lean value), Velvet (Dafny-style methods), Loogle (search queries written as Lean terms) | Macros only rewrite syntax; elaborators give new syntax a type-checked meaning. Most of the creativity sits in that difference. |
| 3 | **Delaborators / unexpanders** (control how terms are printed back) | 15 | Iris-Lean, SciLean, Aeneas | Makes an embedded language display in its own notation, not just parse. |
| 4 | **Custom attributes + environment extensions** (tags on declarations, collected across files) | 21 / 22 | Aesop rules, Aeneas `@[rust_fun]` (exported to an OCaml table), formal-conjectures `@[category]`, Mechanics of Proof `@[autograded]`, Iris-Lean `@[rocq_alias]` | Turns the library into a queryable database of metadata. |
| 5 | **Custom deriving handlers** (generate code from a type definition) | 8 write one; 64 use `deriving` | SciLean, Veil, Plausible | Code generation driven by data types. |
| 6 | **Options and `initialize` blocks** | 22 / 31 | Veil's `veil.smt.trust`, lean-auto, Duper | Behavior users can configure, including how much is trusted. |

## B. Computation and trust in the kernel

| # | Feature | Repos | Most interesting users | Why explore it |
|---|---|--:|---|---|
| 7 | **`decide +kernel` vs `native_decide`** | 11 / 17 | lean4-mlir (1,860 kernel checks) and linglib's verdicts, vs LNSym and Strata (compiled checks) | The sharpest trade-off between trusting the kernel and trusting the compiler. |
| 8 | **Proof by reflection** (`ofReduceBool`) | 8 | LNSym, PhysLean, lean-auto | Lets the kernel check a computation instead of a long proof. |
| 9 | **`axiom`, `opaque`, `#print axioms`** | 31 / 35 / 27 | lean4-mlir audits axioms about 2,000 times; the Natural Number Game makes arithmetic opaque and axiomatic to force a teaching path; Epistemic Protocols uses axioms as judgments the language model must make | Axioms used as a design tool and a trust ledger, not only as a last resort. |

## C. Programs and runtime

| # | Feature | Repos | Most interesting users | Why explore it |
|---|---|--:|---|---|
| 10 | **`@[extern]`, `@[export]`, `@[implemented_by]`, `@[csimp]`** | 13 / 3 / 21 / 6 | SampCert (proof meaning vs runtime C++), lean4-mlir, LeanCopilot (a language model running inside Lean), cedar-spec (94 exported functions callable from other languages) | One definition used in proofs, a different implementation used at runtime. |
| 11 | **`partial` / `unsafe` vs `termination_by`** | 51 / 32 / 34 | Strata (379 termination proofs), Verso and Duper (many `partial` functions) | Where projects choose plain programming over total, provable functions. |
| 12 | **Monads, transformers, custom do-notation** | 39 / 31 | Loom builds a verifier from a chosen monad stack; Functional Programming in Lean | Effects as an interface that can be verified. |
| 13 | **`Std.Do` / `mvcgen` and `Lean.Meta.Sym`** (new verification machinery in Lean's core) | 6 / 5 | Velvet, Aeneas | Very new and barely used yet: verification-condition generation built into the language. |
| 14 | **`grind`** (SMT-style automation inside Lean) | 39 | mathlib4 (6,889 uses), cslib, equational_theories, SymCrypt | Automation the kernel checks, unlike external SMT solvers that are trusted. |
| 15 | **Simprocs** (custom simplification procedures) | 11 | Aeneas (75), LNSym | Domain-specific simplification that still yields checked proofs. |

## D. Tooling, interaction and build

| # | Feature | Repos | Most interesting users | Why explore it |
|---|---|--:|---|---|
| 16 | **Widgets and server RPC** | 11 | ProofWidgets, import-graph, Verso | User interfaces written in Lean, shown in the editor. |
| 17 | **Frontend / InfoTree APIs** (driving Lean as a library) | 22 | Veil, Verso, REPL, lean4game | Lean as an engine that other programs call. |
| 18 | **`#guard_msgs`** | 34 | Strata (2,375), Iris-Lean, Aeneas, Veil | Pins down a command's exact output, so tests double as specifications. |
| 19 | **`run_meta` / `run_cmd`** | 15 | Eggshell checks its axioms at build time, Veil | Arbitrary checks that run when the project builds. |
| 20 | **Lake extensibility** (custom build targets, executables) | many* | Alloy compiles embedded C; doc-gen4 builds documentation as a build step | The build system as part of the language. |
| 21 | **Scoped notations and instances** | 45 | Loom picks angelic or demonic semantics just by opening a namespace | Switching semantics through a namespace. |
| 22 | **Typeclass search as program synthesis** (`outParam`, coercions) | 30 / 41 | Plausible builds a test from the shape of the goal; Loom derives its verifier from instances | Instance resolution doing real computation. |
| 23 | **New module system** (`public import`, `meta import`) | many* | mathlib4, Tau Ceti, linglib | Controls what each file exposes; affects compile time and trust boundaries. |

\* The search patterns for these two were too loose to give reliable counts.

## Suggested starting points

These six cover most of the creativity found in the [repo cards](cards/), and each pairs a heavy user with a contrasting one:

1. **Syntax categories + elaborators (1, 2):** how foreign languages get embedded.
2. **Attributes + environment extensions (4):** the "library as database" pattern.
3. **`@[extern]` / `@[implemented_by]` (10):** one definition for proofs, another for running.
4. **`decide +kernel` vs `native_decide` vs `axiom` (7, 9):** where trust actually sits.
5. **`Std.Do` / `mvcgen` / `Lean.Meta.Sym` (13):** brand-new machinery that hardly anyone uses yet.
6. **Widgets + Frontend APIs (16, 17):** Lean as an interactive engine.

## Deep dives

See [`features/`](features/README.md) for close readings of syntax categories and elaborators, ProofWidgets, Verso and the REPL.
