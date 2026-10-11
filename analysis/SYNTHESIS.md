# Phase 3: creative uses of Lean, beyond certification

This synthesis is based on 37 repository cards in [`cards/`](cards/), each written from the repo's README and key Lean files. The 37 repos were chosen from the 87 in [Phase 1](PHASE1.md) because Lean does more than certify in them: it is used as a language, tool, referee or medium.

## 1. Primary roles

| Primary role | Repos | Count |
|---|---|--:|
| DSL host / metaprogramming | Loom, Veil, Velvet, SciLean, Verso, Alloy, LeanCopilot, Duper, Aesop, Qq, lean-auto, Plausible | 12 |
| Program | LAMR, Loogle, Strata, Eggshell, doc-gen4, REPL, import-graph | 7 |
| Certifier (software) | LNSym, Aeneas, SampCert, lean4-mlir, Iris-Lean | 5 |
| Specification / modeling | linglib, Epistemic Protocols, formal-conjectures, LeanMachines | 4 |
| Interactive / teaching | Mechanics of Proof, Natural Number Game, lean4game, ProofWidgets | 4 |
| Certifier (mathematics) | AgreeToDisagree, AppliedModelingLib | 2 |
| AI oracle / referee | Lean Eval, Comparator | 2 |
| Coordination / trust infrastructure | Lean Atlas | 1 |

Most of these repos have secondary roles too; see each card.

## 2. What the kernel actually checks

The most useful second axis is how much of a project's correctness actually rests on Lean's kernel:

| What is checked | Repos |
|---|---|
| **Full kernel proofs** | AgreeToDisagree; AppliedModelingLib (proof files); Iris-Lean; Duper (each reconstructed proof, though not the prover itself); Comparator and Lean Eval (they replay submissions in the kernel); lean4game (players' moves); linglib's verdicts (`decide +kernel`) |
| **Kernel proofs, plus declared axioms** | Aeneas (axioms modeling parts of Rust's standard library); LeanMachines (5 axioms, one flagged as possibly unprovable, plus some `sorry`) |
| **External solvers trusted by axiom or option** | Loom (`axiom trust_smt : ∀ p, p` after an SMT "unsat"); Veil (`veil.smt.trust` is on by default); lean-auto's SMT/TPTP backends; LAMR (solver output trusted) |
| **Proofs mostly skipped** | SciLean (`sorry_proof`, over 2,000 uses); LNSym's flagship SHA-512 and AES-GCM proofs still contain `sorry` |
| **Compiler trusted instead of the kernel** | Eggshell's BLAKE3 test vectors (`native_decide`); SampCert's runtime samplers (`@[extern]` C++) |
| **Testing only** | Plausible (a passing run proves nothing); LNSym's Arm model is also tested against real hardware; Velvet's property-based tests |
| **Statements only: proofs deliberately absent** | formal-conjectures, Lean Eval challenges, Mechanics of Proof exercises |
| **Types only: Lean used as a typed language** | Verso, doc-gen4, Loogle, import-graph, REPL, Alloy, Qq, ProofWidgets |
| **Axioms standing for judgments outside Lean** | Epistemic Protocols (axioms are decisions the language model must make) |

Several projects publish their trust boundary explicitly:
- lean4-mlir has a `TRUST.md` listing float numerics, text printing, XLA/IREE and the C runtime as still trusted.
- Eggshell and Epistemic Protocols audit which axioms each proof depends on when the project builds.

## 3. Pattern catalogue

Fourteen recurring ways of using Lean beyond "prove a theorem":

1. **Statements as the deliverable.** Precise statements are published with the proofs deliberately left as `sorry`, for others to fill. Examples: open problems with status tags (formal-conjectures), prover challenges (Lean Eval), student exercises (Mechanics of Proof). formal-conjectures also uses `answer(sorry)` for problems whose answer is a value, and notes that checking such an answer needs human judgment.
2. **Lean as referee of untrusted work.** The kernel judges submissions from AI provers or players.
   - Comparator builds and replays submissions in a sandbox; Lean Eval scores only on its verdict.
   - lean4game accepts a level only with no errors or warnings.
   - REPL lets provers backtrack to numbered proof states.
   - LeanCopilot keeps only the language-model suggestions that actually check.
3. **Assumption accounting and trust ledgers.** Lean records exactly what a result rests on.
   - AgreeToDisagree finds a hypothesis the AI-written proof never used, then drops it.
   - AppliedModelingLib fingerprints reviewed statements so later AI proof work can't weaken them.
   - Lean Atlas narrows the set of statements a human must read.
   - lean4-mlir's `TRUST.md` and Eggshell's build-time axiom checks list what remains trusted.
4. **Theories as regression suites.** linglib's `Eval` records, as kernel-checked theorems, whether each linguistic theory is right, wrong or silent on recorded experimental data. A pull request that changes a verdict shows it.
5. **Definitions with two meanings, one for proofs and one for running.**
   - SampCert: probability distributions in proofs, C++ samplers at runtime, plus an export to Dafny.
   - LNSym: the Arm ISA model is both a proof target and an executable tested against hardware.
   - Veil: one `veil module` yields both a transition relation for SMT and an executable step function for a model checker.
   - Velvet: the same method can be run, tested and proven.
   - Eggshell: proofs sit on the very functions the product runs.
6. **Proofs that drive code generation.**
   - lean4-mlir derives gradients and proves them correct while generating StableHLO, so training runs exactly the code the proofs describe.
   - SciLean rewrites mathematical specifications into Float code with tactic scripts.
   - SampCert exports Dafny.
7. **Other languages embedded in Lean.**
   - Inline C (Alloy, about 200 syntax rules).
   - Documents (Verso: a document is a Lean value, and its code examples must compile).
   - A Dafny-like language (Velvet).
   - MLIR-like dialects (Strata).
   - Game scripts (lean4game).
   - Solver input formats: DIMACS, SMT-LIB and TPTP (LAMR).
8. **Verifier factories.** Loom generates a weakest-precondition engine from a chosen monad stack; angelic or demonic nondeterminism is chosen by opening a namespace. Veil and Velvet build complete verifiers as Lean libraries.
9. **Proof search as programming.** Aesop makes search strategy user-programmable through attributes. Duper turns a saturation proof search into a kernel-checkable proof. Qq gives metaprograms types (`Q(α)`).
10. **Weakening Lean for teaching.**
    - The Natural Number Game makes arithmetic `opaque`, restricts `rfl`, and keeps `rw` from closing goals.
    - Mechanics of Proof replaces `linarith`, `simp`, `decide` and similar tactics with failing macros, adds weaker purpose-built tactics, and grades homework with `@[autograded]`.
11. **Lean as orchestrator of external solvers.**
    - LAMR scripts CaDiCaL, Z3 and Vampire.
    - lean-auto translates goals to SMT/TPTP and replays proofs by reflection.
    - Strata's "meta-verifier" turns the solver queries it would send back into Lean goals.
12. **Lean as a contract or prompt language for AI agents.**
    - Epistemic Protocols gives each agent skill a Lean model; its axioms are the language model's judgments, and its theorems hold whatever it decides.
    - LeanCopilot runs the language model inside Lean as a tactic.
13. **The compiled environment as a database.**
    - Loogle searches it with Lean-term patterns.
    - import-graph computes which imports are really needed.
    - doc-gen4 builds documentation incrementally through Lake.
    - Lean Atlas splits statement-level from proof-level dependencies.
    - Aeneas collects `@[rust_fun]` attributes into an OCaml table for its extractor.
14. **Correctness by construction with dependent structures.** In LeanMachines, Event-B proof obligations are structure fields, so a model can't be built without its proofs. Iris-Lean rebuilds a Rocq-style separation-logic proof mode and tracks porting progress with `@[rocq_alias]` attributes.

## 4. Gaps and ideas (hypotheses, not findings)

These are combinations of the patterns above that none of the 37 repos does yet:

- **A shared trust-ledger format.** lean4-mlir, Eggshell, Epistemic Protocols and AppliedModelingLib each track trust in their own way. A common manifest, listing axioms, trusted solvers, `native_decide`, `extern` code and fingerprinted statements, would let a tool such as Lean Atlas or Comparator compare projects.
- **Regression suites for other empirical sciences.** linglib's verdicts-against-data design could carry over to economics (EconCSLib), physics (PhysLean) or statistics (StatsMLlib).
- **Referees outside AI benchmarks.** Comparator-style judging for legal or scientific claims, which is the direction StartClaims describes (it isn't among the analyzed repos), or for contracts and bounties.
- **Dual-meaning definitions for data and protocols.** The SampCert/Veil approach, applied to data-processing pipelines or privacy policies: the same object is proven about and executed.
- **Lean as a prompt language, more broadly.** Epistemic Protocols is the only example. Agent tool contracts, review checklists and specifications handed to AI coders are natural next targets.
- **Teaching by weakening, outside mathematics.** The Natural Number Game approach could teach programming or verification by removing automation step by step.

## 5. How Phase 1 heuristics compared

The Phase 2 readers disagreed with the Phase 1 guess at least partly on more than half of the repos (about 23 of 37, many of them minor). The recurring causes:

- **`sorry`-heavy repos read as certifiers.** formal-conjectures, Mechanics of Proof, the Natural Number Game, Lean Eval and Comparator are corpora of statements, exercises or test cases.
- **Tests counted as "computation".** In Aesop, Qq, Loogle and Aeneas, `#eval`/`#guard` are regression tests.
- **Trusted solvers are invisible to syntax.** Loom's `trust_smt`, Veil's default trust option and lean-auto's axioms look like proofs to a token count.
- **"Program" and "interactive" misfire on libraries.** ProofWidgets and Plausible have no executable, and doc-gen4 outputs a static site.
- **Velvet no longer depends on Loom.** Its domain-specific language now lives in its own repo, so Phase 1's low metaprogramming score for it was a counting artifact, not a missing dependency.

## 6. Caveats

- **Partial reading.** Each card comes from a time-boxed reading of the README and key files. Large repos (linglib, AppliedModelingLib, Strata) were sampled.
- **Authorship is the weakest field.** The clones are shallow (one commit), so human/AI authorship is mostly marked unconfirmed.
- **Selection bias.** The 37 repos are biased toward non-certifier uses by design. The 38 Phase 1 "certifier" repos (Mathlib, FLT, PFR, …) are under-represented here.
