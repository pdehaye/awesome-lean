# Phase 0–1: how the awesome-lean repositories use Lean

First, automated pass over every GitHub repository linked from the README: **87 repos**, 49 of them on Reservoir, 76 containing Lean code.
The roles below are heuristic guesses from code statistics, meant to be confirmed by reading each repo in Phase 2.

## Method

- **Phase 0** (`phase0_inventory.py` → `inventory.json`): every GitHub link in the README (main or secondary link), deduplicated, with Reservoir metadata.
- **Phase 1** (`phase1_signals.py` → `signals.json`, `signals.csv`): shallow sparse clone of Lean sources and build files only, then counts on comment-stripped code:
  - **Proof ratio**: `theorem` + `lemma` as a share of all declarations (`def`, `structure`, `inductive`, `instance`, …).
  - **Meta / kLOC**: `syntax`, `macro`, `elab`, `declare_syntax_cat` and uses of `MetaM`/`TacticM`/`TermElabM`/`CommandElabM`, per 1,000 lines.
  - **IO / kLOC**: `IO` uses, plus weighted `def main` and `@[extern]`.
  - Also: `sorry`, `decide`/`native_decide`, `#eval`/`#guard`, widgets, imports, Lake executables and dependencies, share of non-Lean files.

## Heuristic roles

| Role | Rule | Repos |
|---|---|--:|
| certifier | proof ratio ≥ 0.45 | 38 |
| DSL / metaprogramming | meta ≥ 5 per kLOC, or ≥ 500 constructs in total | 31 |
| program | IO ≥ 5 per kLOC | 30 |
| computation / examples | `#eval` + `#guard` ≥ 5 per kLOC | 28 |
| interactive | uses widgets | 18 |
| spec + proof | proof ratio 0.2–0.45 | 12 |
| external tool (no Lean code) | no `.lean` files | 11 |
| tool around Lean | < 20% Lean files and < 5 kLOC | 9 |
| game / teaching | depends on `GameServer` | 2 |
| specification / modeling library | none of the above | 1 |

Repos usually get several roles; they are not exclusive.

## Calibration against 10 hand labels

| Repo | Hand label | Heuristic (final) | Match |
|---|---|---|---|
| teorth/pfr | certifier | certifier | ✓ |
| mathlib4 | certifier + tactics | certifier + DSL + interactive | ✓ |
| hawkrobe/linglib | specification / modeling | spec + proof | ✓ |
| lean-machines | specification / refinement | specification / modeling library | ✓ |
| leanprover/verso | DSL + program | DSL + program + computation + interactive | ✓ |
| nomeata/loogle | program | DSL + program + computation | ✓ |
| leanprover-community/repl | program, oracle for AI | tool around Lean + DSL + program | ✓ |
| brettkoonce/lean4-mlir | program (code generation) + certifier | certifier + program + computation | ✓ |
| leanprover-community/nng4 | interactive teaching | spec + proof + game / teaching | ✓ |
| verse-lab/velvet | DSL + certifier | certifier | partial: its DSL lives in Loom |

The first version scored 5/10. Three fixes brought it to 9/10:
- A Lake executable alone no longer counts as "program" (mathlib, PhysLean and Tau Ceti ship scripts).
- Metaprogramming also counts by absolute volume, not just density.
- Games are detected through the `GameServer` dependency.

## First observations (to verify in Phase 2)

1. **`sorry` as a way to state problems, not just a gap.**
   - The largest `sorry` counts are in formal-conjectures (4,780), ProofNet (2,403), Tao's Analysis I (1,967), Lean Eval (1,293) and PutnamBench (1,018).
   - In these repos, Lean states open problems, benchmarks and exercises precisely, and leaves the proofs for someone else.
2. **Large libraries that are mostly definitions.**
   - linglib has more definitions (43.9k) than theorems (32.3k). Strata, LNSym and Eggshell are similarly definition-heavy.
   - Lean is used there to model a domain, not mainly to prove things about it.
3. **Lean as a program that judges or serves.** The highest IO densities are Lean Eval, Comparator, LeanCopilot, Lean Atlas, REPL, LeanDojo and Eggshell: Lean runs as a referee, server or memory engine.
4. **Many small languages inside Lean.**
   - The highest metaprogramming densities are Alloy (C code inline), Qq, Loogle's query language, lean4game, Loom, Aesop and Duper.
   - Veil, Velvet and Strata build whole verifiers or intermediate languages as Lean libraries.
5. **Code generation from proofs.** lean4-mlir declares 211 Lake executables (one per network or experiment) whose gradients are proven, then emitted as GPU code.
6. **Verso spreading as a publishing layer.** FLT, Tao's Analysis I and Tau Ceti import Verso (FLT via VersoBlueprint), alongside the official books.
7. **Ecosystem tools outside Lean.** 11 repos contain no Lean at all: elan (Rust), Reservoir (TypeScript), LeanSearch, model releases and editor modes.

## Limits

- The signals are syntactic. A "certifier" score does not tell how deep the proofs are, and a DSL used lightly can still score high on volume.
- Repos that aggregate many projects (Lean Pool: 9.1M lines, AppliedModelingLib: 2M) are counted as single units.
- The lean4 repository mixes the compiler, the standard library and its tests, so its signals blur together.

## All repositories

| Repo | Section | Lean kLOC | Proof ratio | Meta / kLOC | IO / kLOC | `sorry` | Heuristic roles |
|---|---|--:|--:|--:|--:|--:|---|
| [LeanPool/lean-pool](https://github.com/LeanPool/lean-pool) | Mathematics formalization projects | 9091.1 | 0.71 | 0.1 | 0.0 | 3 | certifier + DSL/metaprogramming + interactive + (ships tooling executables) |
| [nikhgarg/AppliedModelingLib](https://github.com/nikhgarg/AppliedModelingLib) | Thematic projects | 1987.2 | 0.7 | 0.1 | 0.0 | 0 | certifier |
| [TauCetiProject/TauCeti](https://github.com/TauCetiProject/TauCeti) | Mathematics formalization projects | 1610.4 | 0.81 | 0.0 | 0.1 | 1 | certifier + (ships tooling executables) |
| [leanprover-community/mathlib4](https://github.com/leanprover-community/mathlib4) | Libraries | 1577.7 | 0.73 | 1.6 | 0.8 | 102 | certifier + DSL/metaprogramming + interactive + (ships tooling executables) |
| [leanprover/lean4](https://github.com/leanprover/lean4) | Official resources | 723.9 | 0.47 | 11.9 | 25.6 | 2383 | certifier + DSL/metaprogramming + program + computation/examples + interactive |
| [hawkrobe/linglib](https://github.com/hawkrobe/linglib) | Thematic projects | 528.9 | 0.38 | 0.0 | 0.1 | 19 | spec+proof |
| [strata-org/Strata](https://github.com/strata-org/Strata) | Software verification | 205.1 | 0.25 | 1.4 | 8.7 | 0 | spec+proof + program + computation/examples |
| [lean-phys-community/PhysLean](https://github.com/lean-phys-community/PhysLean) | Thematic projects | 175.7 | 0.72 | 0.9 | 4.9 | 16 | certifier + (ships tooling executables) |
| [brettkoonce/lean4-mlir](https://github.com/brettkoonce/lean4-mlir) | Software verification | 170.8 | 0.56 | 0.0 | 70.2 | 107 | certifier + program + computation/examples |
| [AlexKontorovich/PrimeNumberTheoremAnd](https://github.com/AlexKontorovich/PrimeNumberTheoremAnd) | Mathematics formalization projects | 144.1 | 0.92 | 0.0 | 0.0 | 231 | certifier |
| [math-inc/Sphere-Packing-Lean](https://github.com/math-inc/Sphere-Packing-Lean) | Mathematics formalization projects | 141.2 | 0.77 | 0.1 | 0.0 | 0 | certifier |
| [teorth/equational_theories](https://github.com/teorth/equational_theories) | Mathematics formalization projects | 141.0 | 0.86 | 0.5 | 0.8 | 0 | certifier + (ships tooling executables) |
| [cedar-policy/cedar-spec](https://github.com/cedar-policy/cedar-spec) | Software verification | 84.7 | 0.53 | 0.7 | 3.1 | 0 | certifier |
| [leanprover/reference-manual](https://github.com/leanprover/reference-manual) | Official resources | 76.0 | 0.14 | 3.5 | 19.7 | 151 | program + computation/examples + interactive |
| [leanprover-community/lean-liquid](https://github.com/leanprover-community/lean-liquid) | Mathematics formalization projects | 75.8 | 0.49 | 0.0 | 0.3 | 1 | certifier |
| [microsoft/SymCrypt](https://github.com/microsoft/SymCrypt) | Software verification | 75.1 | 0.56 | 0.5 | 1.6 | 0 | certifier |
| [leanprover-community/iris-lean](https://github.com/leanprover-community/iris-lean) | Software verification | 71.7 | 0.56 | 7.0 | 0.6 | 0 | certifier + DSL/metaprogramming + computation/examples + interactive |
| [google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures) | Mathematics formalization projects | 65.0 | 0.72 | 1.0 | 0.7 | 4780 | certifier + (ships tooling executables) |
| [Lean-MoDS/StatsMLlib](https://github.com/Lean-MoDS/StatsMLlib) | Thematic projects | 61.9 | 0.82 | 0.0 | 0.0 | 0 | certifier |
| [leanprover/lean-eval](https://github.com/leanprover/lean-eval) | Benchmarks and datasets | 52.6 | 0.29 | 0.2 | 269.2 | 1293 | spec+proof + program |
| [lecopivo/SciLean](https://github.com/lecopivo/SciLean) | Thematic projects | 51.4 | 0.34 | 11.5 | 19.0 | 832 | spec+proof + DSL/metaprogramming + program + computation/examples + interactive |
| [AeneasVerif/aeneas](https://github.com/AeneasVerif/aeneas) | Software verification | 48.1 | 0.34 | 13.5 | 2.7 | 24 | spec+proof + DSL/metaprogramming + computation/examples |
| [leanprover/verso](https://github.com/leanprover/verso) | Editors and tooling | 46.8 | 0.03 | 7.1 | 32.4 | 8 | DSL/metaprogramming + program + computation/examples + interactive |
| [YuanheZ/lean-stat-learning-theory](https://github.com/YuanheZ/lean-stat-learning-theory) | Mathematics formalization projects | 45.1 | 0.82 | 0.3 | 0.0 | 0 | certifier |
| [fpvandoorn/carleson](https://github.com/fpvandoorn/carleson) | Mathematics formalization projects | 41.9 | 0.85 | 0.1 | 0.0 | 6 | certifier |
| [ImperialCollegeLondon/FLT](https://github.com/ImperialCollegeLondon/FLT) | Mathematics formalization projects | 41.6 | 0.6 | 0.0 | 0.5 | 60 | certifier |
| [momonpya/eggshell](https://github.com/momonpya/eggshell) | Tools for AI | 41.2 | 0.31 | 0.0 | 82.7 | 0 | spec+proof + program |
| [verse-lab/veil](https://github.com/verse-lab/veil) | Software verification | 37.8 | 0.15 | 19.0 | 11.6 | 6 | DSL/metaprogramming + program + computation/examples + interactive |
| [teorth/analysis](https://github.com/teorth/analysis) | Mathematics formalization projects | 32.4 | 0.7 | 0.2 | 0.0 | 1967 | certifier |
| [leanprover/LNSym](https://github.com/leanprover/LNSym) | Software verification | 30.3 | 0.28 | 7.6 | 3.5 | 37 | spec+proof + DSL/metaprogramming + computation/examples + (ships tooling executables) |
| [gametheoryinlean/EconCSLib](https://github.com/gametheoryinlean/EconCSLib) | Thematic projects | 29.7 | 0.57 | 0.1 | 0.0 | 21 | certifier |
| [leanprover/fp-lean](https://github.com/leanprover/fp-lean) | Books and tutorials | 28.6 | 0.13 | 2.4 | 59.9 | 26 | program + computation/examples |
| [leanprover/cslib](https://github.com/leanprover/cslib) | Libraries | 28.0 | 0.64 | 2.0 | 0.8 | 0 | certifier + (ships tooling executables) |
| [leanprover-community/lean-auto](https://github.com/leanprover-community/lean-auto) | Libraries | 28.0 | 0.32 | 14.8 | 5.4 | 22 | spec+proof + DSL/metaprogramming + program |
| [verse-lab/velvet](https://github.com/verse-lab/velvet) | Software verification | 26.4 | 0.53 | 3.9 | 0.2 | 1 | certifier + (ships tooling executables) |
| [leanprover-community/batteries](https://github.com/leanprover-community/batteries) | Libraries | 20.7 | 0.58 | 12.1 | 5.5 | 18 | certifier + DSL/metaprogramming + program + computation/examples |
| [leanprover-community/duper](https://github.com/leanprover-community/duper) | Libraries | 18.7 | 0.23 | 27.2 | 4.4 | 40 | spec+proof + DSL/metaprogramming + (ships tooling executables) |
| [teorth/pfr](https://github.com/teorth/pfr) | Mathematics formalization projects | 18.3 | 0.88 | 0.5 | 0.3 | 6 | certifier |
| [leanprover-community/aesop](https://github.com/leanprover-community/aesop) | Libraries | 15.8 | 0.14 | 27.3 | 3.7 | 9 | DSL/metaprogramming + computation/examples |
| [leanprover/SampCert](https://github.com/leanprover/SampCert) | Software verification | 14.1 | 0.66 | 2.8 | 8.8 | 0 | certifier + program |
| [leanprover/theorem_proving_in_lean4](https://github.com/leanprover/theorem_proving_in_lean4) | Books and tutorials | 13.0 | 0.19 | 0.7 | 3.9 | 105 | computation/examples |
| [zhangir-azerbayev/ProofNet](https://github.com/zhangir-azerbayev/ProofNet) | Benchmarks and datasets | 12.3 | 1.0 | 0.0 | 0.0 | 2403 | certifier |
| [merely-true/merely-true](https://github.com/merely-true/merely-true) | Mathematics formalization projects | 9.3 | 0.82 | 0.0 | 0.0 | 0 | certifier |
| [leanprover-community/mathematics_in_lean](https://github.com/leanprover-community/mathematics_in_lean) | Books and tutorials | 8.2 | 0.46 | 0.0 | 0.0 | 340 | certifier |
| [lean-machines-central/lean-machines](https://github.com/lean-machines-central/lean-machines) | Software verification | 8.0 | 0.03 | 0.0 | 2.7 | 10 | specification/modeling library + (ships tooling executables) |
| [kbuzzard/ClassFieldTheory](https://github.com/kbuzzard/ClassFieldTheory) | Mathematics formalization projects | 7.9 | 0.57 | 0.9 | 0.0 | 80 | certifier |
| [verse-lab/loom](https://github.com/verse-lab/loom) | Software verification | 7.1 | 0.29 | 28.8 | 2.8 | 1 | spec+proof + DSL/metaprogramming + interactive |
| [trishullab/PutnamBench](https://github.com/trishullab/PutnamBench) | Benchmarks and datasets | 6.6 | 0.64 | 0.8 | 4.7 | 1018 | certifier |
| [ImperialCollegeLondon/formalising-mathematics-2024](https://github.com/ImperialCollegeLondon/formalising-mathematics-2024) | Courses | 5.9 | 0.59 | 0.0 | 0.0 | 329 | certifier |
| [hrmacbeth/math2001](https://github.com/hrmacbeth/math2001) | Books and tutorials | 5.2 | 0.65 | 15.1 | 0.2 | 564 | certifier + DSL/metaprogramming + computation/examples + interactive |
| [leanprover/doc-gen4](https://github.com/leanprover/doc-gen4) | Editors and tooling | 5.2 | 0.0 | 11.7 | 43.5 | 1 | DSL/metaprogramming + program + interactive |
| [leanprover-community/nng4](https://github.com/leanprover-community/nng4) | Games | 5.0 | 0.41 | 4.8 | 0.0 | 11 | spec+proof + game/teaching |
| [lean-forward/logical_verification_2025](https://github.com/lean-forward/logical_verification_2025) | Courses | 4.8 | 0.57 | 6.5 | 0.0 | 227 | certifier + DSL/metaprogramming + computation/examples |
| [leanprover-community/import-graph](https://github.com/leanprover-community/import-graph) | Editors and tooling | 4.1 | 0.01 | 15.6 | 25.1 | 5 | DSL/metaprogramming + program + computation/examples + interactive |
| [yangky11/miniF2F-lean4](https://github.com/yangky11/miniF2F-lean4) | Benchmarks and datasets | 3.6 | 1.0 | 0.0 | 0.0 | 488 | certifier |
| [avigad/lamr](https://github.com/avigad/lamr) | Books and tutorials | 3.6 | 0.06 | 26.5 | 45.5 | 1 | DSL/metaprogramming + program + computation/examples + interactive |
| [tydeu/lean4-alloy](https://github.com/tydeu/lean4-alloy) | Libraries | 3.3 | 0.0 | 79.1 | 52.5 | 0 | DSL/metaprogramming + program + computation/examples |
| [leanprover-community/ProofWidgets4](https://github.com/leanprover-community/ProofWidgets4) | Libraries | 3.0 | 0.0 | 21.9 | 9.1 | 0 | DSL/metaprogramming + program + interactive |
| [leanprover-community/lean4game](https://github.com/leanprover-community/lean4game) | Games | 2.4 | 0.01 | 32.5 | 6.7 | 1 | tool-around-Lean + game/teaching + DSL/metaprogramming + program + interactive |
| [NyxFoundation/lean-atlas](https://github.com/NyxFoundation/lean-atlas) | Editors and tooling | 2.4 | 0.0 | 7.2 | 105.1 | 2 | DSL/metaprogramming + program |
| [jongwony/epistemic-protocols](https://github.com/jongwony/epistemic-protocols) | Tools for AI | 2.0 | 0.74 | 4.1 | 14.3 | 2 | tool-around-Lean + certifier + program + computation/examples |
| [leanprover-community/lean4-metaprogramming-book](https://github.com/leanprover-community/lean4-metaprogramming-book) | Books and tutorials | 1.9 | 0.04 | 115.2 | 34.0 | 21 | DSL/metaprogramming + program + computation/examples |
| [leanprover-community/plausible](https://github.com/leanprover-community/plausible) | Libraries | 1.9 | 0.01 | 15.0 | 9.1 | 0 | DSL/metaprogramming + program + computation/examples |
| [leanprover-community/quote4](https://github.com/leanprover-community/quote4) | Libraries | 1.8 | 0.0 | 78.2 | 0.0 | 1 | DSL/metaprogramming + computation/examples |
| [lean-dojo/LeanCopilot](https://github.com/lean-dojo/LeanCopilot) | Tools for AI | 1.5 | 0.0 | 16.4 | 115.6 | 5 | DSL/metaprogramming + program + computation/examples |
| [leanprover/verso-templates](https://github.com/leanprover/verso-templates) | Editors and tooling | 1.4 | 0.16 | 0.7 | 95.2 | 0 | program + computation/examples |
| [nomeata/loogle](https://github.com/nomeata/loogle) | Search | 1.2 | 0.09 | 42.8 | 60.1 | 4 | DSL/metaprogramming + program + computation/examples |
| [AxiomMath/AgreeToDisagree](https://github.com/AxiomMath/AgreeToDisagree) | Thematic projects | 1.2 | 0.73 | 0.0 | 0.0 | 2 | certifier |
| [leanprover-community/repl](https://github.com/leanprover-community/repl) | Tools for AI | 1.1 | 0.07 | 20.0 | 104.5 | 8 | tool-around-Lean + DSL/metaprogramming + program |
| [leanprover/comparator](https://github.com/leanprover/comparator) | Editors and tooling | 0.8 | 0.25 | 2.5 | 145.6 | 26 | spec+proof + program |
| [lean-dojo/LeanDojo](https://github.com/lean-dojo/LeanDojo) | Tools for AI | 0.6 | 0.0 | 26.0 | 96.9 | 1 | tool-around-Lean + DSL/metaprogramming + program |
| [Julian/lean.nvim](https://github.com/Julian/lean.nvim) | Editors and tooling | 0.5 | 0.12 | 8.5 | 4.2 | 9 | tool-around-Lean + DSL/metaprogramming + computation/examples + interactive |
| [oOo0oOo/lean-lsp-mcp](https://github.com/oOo0oOo/lean-lsp-mcp) | Tools for AI | 0.1 | 0.51 | 0.0 | 0.0 | 3 | tool-around-Lean + certifier + interactive |
| [leanprover/vscode-lean4](https://github.com/leanprover/vscode-lean4) | Editors and tooling | 0.1 | 0.0 | 0.0 | 971.8 | 0 | tool-around-Lean + program + computation/examples |
| [justincasher/lean-explore](https://github.com/justincasher/lean-explore) | Search | 0.0 | 0.0 | 0.0 | 0.0 | 0 | tool-around-Lean |
| [leanprover-community/lean4web](https://github.com/leanprover-community/lean4web) | Getting started | 0.0 | 0.0 | 0.0 | 0.0 | 0 | tool-around-Lean + interactive |
| [ammkrn/type_checking_in_lean4](https://github.com/ammkrn/type_checking_in_lean4) | Books and tutorials | 0 | – | – | – | – | external tool (no Lean code) (.md:25, (none):2, .yml:1, .toml:1, .js:1) |
| [deepseek-ai/DeepSeek-Prover-V2](https://github.com/deepseek-ai/DeepSeek-Prover-V2) | Models and provers | 0 | – | – | – | – | external tool (no Lean code) (.pdf:1, (none):1, .md:1, .png:1, .zip:1) |
| [frenzymath/LeanSearch](https://github.com/frenzymath/LeanSearch) | Search | 0 | – | – | – | – | external tool (no Lean code) (.py:13, .j2:5, .txt:4, (none):3, .example:1) |
| [Goedel-LM/Goedel-Prover-V2](https://github.com/Goedel-LM/Goedel-Prover-V2) | Models and provers | 0 | – | – | – | – | external tool (no Lean code) (.png:7, .py:5, (none):3, .jsonl:3, .md:2) |
| [leanprover-community/lean4-mode](https://github.com/leanprover-community/lean4-mode) | Editors and tooling | 0 | – | – | – | – | external tool (no Lean code) (.el:10, (none):3, .yml:2, .org:2, .json:1) |
| [leanprover-community/leanprover-community.github.io](https://github.com/leanprover-community/leanprover-community.github.io) | Official resources | 0 | – | – | – | – | external tool (no Lean code) (.md:41, .jpg:32, .html:29, .png:9, .yaml:8) |
| [leanprover/elan](https://github.com/leanprover/elan) | Getting started | 0 | – | – | – | – | external tool (no Lean code) (.rs:47, .toml:6, (none):4, .md:3, .yml:2) |
| [leanprover/lean-lang.org](https://github.com/leanprover/lean-lang.org) | Official resources | 0 | – | – | – | – | external tool (no Lean code) (.html:3) |
| [leanprover/reservoir](https://github.com/leanprover/reservoir) | Getting started | 0 | – | – | – | – | external tool (no Lean code) (.vue:29, .ts:17, .py:13, .svg:7, .yml:5) |
| [MoonshotAI/Kimina-Prover-Preview](https://github.com/MoonshotAI/Kimina-Prover-Preview) | Models and provers | 0 | – | – | – | – | external tool (no Lean code) (.png:4, .py:3, .md:2, .zip:2, .pdf:1) |
| [PatrickMassot/leanblueprint](https://github.com/PatrickMassot/leanblueprint) | Editors and tooling | 0 | – | – | – | – | external tool (no Lean code) ((none):6, .tex:6, .py:5, .html:3, .md:2) |
