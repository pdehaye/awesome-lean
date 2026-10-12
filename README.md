# Awesome Lean [![Awesome](https://awesome.re/badge-flat.svg)](https://awesome.re)

[Lean homepage](https://lean-lang.org)

> A collaborative list of awesome Lean resources. Feel free to contribute!

Lean is a functional programming language that makes it easy to write correct and maintainable code. You can also use Lean as an interactive theorem prover.

## Contents

- [Official resources](#official-resources)
- [Getting started](#getting-started)
- [Learning](#learning)
  - [Books and tutorials](#books-and-tutorials)
  - [Games](#games)
  - [Courses](#courses)
- [Editors and tooling](#editors-and-tooling)
- [Search](#search)
- [Libraries](#libraries)
- [Mathematics formalization projects](#mathematics-formalization-projects)
- [Thematic projects](#thematic-projects)
- [Software verification](#software-verification)
- [AI and machine learning](#ai-and-machine-learning)
  - [Models and provers](#models-and-provers)
  - [Benchmarks and datasets](#benchmarks-and-datasets)
  - [Tools for AI](#tools-for-ai)
- [Papers](#papers)
- [Funding calls](#funding-calls)
- [Organizations](#organizations)
- [Companies](#companies)
- [Videos](#videos)
- [Podcasts](#podcasts)
- [Blogs and news](#blogs-and-news)
- [Chat and social](#chat-and-social)
- [Other meta-resources](#other-meta-resources)
- [To sort](#to-sort)

## Official resources

- [Lean 4 repository](https://github.com/leanprover/lean4) - Source code of the Lean 4 compiler, elaborator and standard library.
- [Documentation](https://lean-lang.org/learn/) - Index of the official manuals, books and tutorials ([GitHub](https://github.com/leanprover/lean-lang.org)).
- [Lean Language Reference](https://lean-lang.org/doc/reference/latest/) - Comprehensive reference manual for the language ([GitHub](https://github.com/leanprover/reference-manual)).
- [Lean Community](https://leanprover-community.github.io/) - Community website with installation instructions, events and Mathlib documentation ([GitHub](https://github.com/leanprover-community/leanprover-community.github.io)).

## Getting started

- [elan](https://github.com/leanprover/elan) - Lean toolchain installer and version manager, in the spirit of rustup.
- [Lake](https://github.com/leanprover/lean4/tree/master/src/lake) - Lean's built-in build system and package manager.
- [Reservoir](https://reservoir.lean-lang.org) - Official registry of Lean packages ([GitHub](https://github.com/leanprover/reservoir)).
- [Lean 4 Web](https://live.lean-lang.org) - Try Lean and Mathlib in the browser with no installation ([GitHub](https://github.com/leanprover-community/lean4web)).

## Learning

### Books and tutorials

- [Theorem Proving in Lean 4](https://lean-lang.org/theorem_proving_in_lean4/) - The standard introduction to dependent type theory and proving in Lean ([GitHub](https://github.com/leanprover/theorem_proving_in_lean4)).
- [Functional Programming in Lean](https://lean-lang.org/functional_programming_in_lean/) - David Thrane Christiansen's book on Lean as a general-purpose programming language ([GitHub](https://github.com/leanprover/fp-lean)).
- [Mathematics in Lean](https://leanprover-community.github.io/mathematics_in_lean/) - Hands-on introduction to formalizing mathematics with Mathlib ([GitHub](https://github.com/leanprover-community/mathematics_in_lean)).
- [Metaprogramming in Lean 4](https://leanprover-community.github.io/lean4-metaprogramming-book/) - Writing tactics, macros and elaborators ([GitHub](https://github.com/leanprover-community/lean4-metaprogramming-book)).
- [The Mechanics of Proof](https://hrmacbeth.github.io/math2001/) - Heather Macbeth's introduction to proof writing, taught with Lean ([GitHub](https://github.com/hrmacbeth/math2001)).
- [Logic and Mechanized Reasoning](https://avigad.github.io/lamr/) - Textbook on logic, SAT/SMT solving and proof assistants ([GitHub](https://github.com/avigad/lamr)).
- [Type Checking in Lean 4](https://ammkrn.github.io/type_checking_in_lean4/) - Guide to Lean's kernel and type theory, aimed at writers of external checkers ([GitHub](https://github.com/ammkrn/type_checking_in_lean4)).

### Games

- [Lean Game Server](https://adam.math.hhu.de) - Collection of browser-based games teaching Lean and mathematics ([GitHub](https://github.com/leanprover-community/lean4game)).
- [Natural Number Game](https://adam.math.hhu.de/#/g/leanprover-community/nng4) - The classic gentle introduction to proving theorems about natural numbers ([GitHub](https://github.com/leanprover-community/nng4)).

### Courses

- [Formalising Mathematics](https://b-mehta.github.io/formalising-mathematics-notes/) - Course notes from Kevin Buzzard's Imperial College course ([GitHub](https://github.com/ImperialCollegeLondon/formalising-mathematics-2024)).
- [The Hitchhiker's Guide to Logical Verification](https://github.com/lean-forward/logical_verification_2025) - Course on interactive theorem proving and program semantics in Lean 4.

## Editors and tooling

- [VS Code extension](https://github.com/leanprover/vscode-lean4) - Official Lean 4 extension for Visual Studio Code, with infoview.
- [lean4-mode](https://github.com/leanprover-community/lean4-mode) - Emacs major mode for Lean 4.
- [lean.nvim](https://github.com/Julian/lean.nvim) - Neovim support for Lean 4.
- [doc-gen4](https://github.com/leanprover/doc-gen4) - Documentation generator for Lean 4 projects.
- [Verso](https://verso.lean-lang.org/) - Authoring tool for documentation, books and websites written in Lean ([GitHub](https://github.com/leanprover/verso)).
- [Verso templates](https://github.com/leanprover/verso-templates) - Ready-to-copy starter projects for Verso textbooks, blogs and websites, with a setup script.
- [leanblueprint](https://github.com/PatrickMassot/leanblueprint) - Plastex plugin for writing blueprints that track large formalization projects.
- [lean4web](https://github.com/leanprover-community/lean4web) - Self-hostable web editor for Lean 4.
- [Comparator](https://github.com/leanprover/comparator) - Sandboxed, trustworthy judge that independently re-checks Lean proofs against a challenge statement.
- [Lean Atlas](https://github.com/NyxFoundation/lean-atlas) - Interactive dependency-graph viewer that narrows down what humans must review in AI-assisted formalizations.
- [import-graph](https://github.com/leanprover-community/import-graph) - Tool to visualize and analyze the import structure of Lean projects.
- [LeanArchitect](https://github.com/hanwenzhu/LeanArchitect) - Generates blueprint data directly from `@[blueprint]`-tagged Lean declarations.
- [Leaff](https://github.com/alexjbest/leaff) - Diff tool summarizing the differences between two versions of a Lean environment, fast enough for Mathlib.
- [lean4checker](https://github.com/leanprover/lean4checker) - Replays a module's environment to confirm every declaration is accepted by the kernel.
- [gonzalgo](https://github.com/zengineco/gonzalgo) - Declaration graph keeping statement and proof dependencies apart, showing where a library spends its axioms.
- [jixia](https://github.com/frenzymath/jixia) - Static analysis tool extracting source-level declaration data, for IDEs and machine learning.
- [leaner](https://github.com/SrGaabriel/leaner) - Linter, formatter and whole-program dead code eliminator.

## Search

- [Loogle](https://loogle.lean-lang.org) - Search Mathlib by name, constant and type signature patterns ([GitHub](https://github.com/nomeata/loogle)).
- [LeanSearch](https://leansearch.net) - Natural-language semantic search over Mathlib ([GitHub](https://github.com/frenzymath/LeanSearch)).
- [LeanExplore](https://www.leanexplore.com) - Semantic search engine for Lean 4 declarations across Mathlib and other packages ([GitHub](https://github.com/justincasher/lean-explore)).

## Libraries

- [Mathlib](https://github.com/leanprover-community/mathlib4) - The community's unified library of formalized mathematics ([docs](https://leanprover-community.github.io/mathlib4_docs/)).
- [Batteries](https://github.com/leanprover-community/batteries) - Extended standard library of data structures and tactics.
- [Aesop](https://github.com/leanprover-community/aesop) - White-box automation tactic for proof search.
- [Duper](https://github.com/leanprover-community/duper) - Superposition-based automatic theorem prover tactic.
- [lean-auto](https://github.com/leanprover-community/lean-auto) - Interface between Lean and external automated theorem provers.
- [Plausible](https://github.com/leanprover-community/plausible) - Property-based testing framework.
- [ProofWidgets](https://github.com/leanprover-community/ProofWidgets4) - Interactive user-interface widgets in the infoview.
- [Qq](https://github.com/leanprover-community/quote4) - Type-safe expression quotations for metaprogramming.
- [Alloy](https://github.com/tydeu/lean4-alloy) - Write C FFI code inline in Lean.
- [CSLib](https://www.cslib.io/) - Computer Science Library ([GitHub](https://github.com/leanprover/cslib)).

## Mathematics formalization projects

- [Fermat's Last Theorem](https://github.com/ImperialCollegeLondon/FLT) - Kevin Buzzard's project to formalize a proof of FLT.
- [Liquid Tensor Experiment](https://github.com/leanprover-community/lean-liquid) - Formalization of a key theorem of Clausen and Scholze, completed in 2022.
- [Polynomial Freiman-Ruzsa](https://github.com/teorth/pfr) - Formalization of the PFR conjecture proof, led by Terence Tao.
- [Equational Theories Project](https://github.com/teorth/equational_theories) - Large-scale collaborative exploration of implications between magma laws.
- [Analysis I](https://github.com/teorth/analysis) - Lean companion to Terence Tao's Analysis I textbook.
- [Carleson](https://github.com/fpvandoorn/carleson) - Formalization of a generalized Carleson theorem.
- [Prime Number Theorem And...](https://github.com/AlexKontorovich/PrimeNumberTheoremAnd) - Formalizing the prime number theorem and related analytic number theory.
- [Sphere Packing](https://github.com/math-inc/Sphere-Packing-Lean) - Completed formalization of Viazovska's sphere packing optimality in dimensions 8 and 24.
- [Statistical Learning Theory](https://github.com/YuanheZ/lean-stat-learning-theory) - Sorry-free Lean 4 library for statistical learning theory, built with human-AI collaboration.
- [Class Field Theory](https://github.com/kbuzzard/ClassFieldTheory) - Kevin Buzzard's project to formalize class field theory.
- [Formal Conjectures](https://github.com/google-deepmind/formal-conjectures) - Google DeepMind's collection of formalized open conjectures.
- [Tau Ceti](https://github.com/TauCetiProject/TauCeti) - Library of formal mathematics written by AI contributors under human-directed roadmaps, incubated by the Lean FRO and the Mathlib Initiative.
- [merely-true](https://github.com/merely-true/merely-true) - Permissive, CI-gated repository of AI-generated mathematics with no manual review.
- [Lean Pool](https://github.com/LeanPool/lean-pool) - Curated collection of formalization projects outside Mathlib's scope, checked by linters and LLM review.

## Thematic projects

- [PhysLean](https://github.com/lean-phys-community/PhysLean) - Lean Community for formalizing physics.
- [SciLean](https://github.com/lecopivo/SciLean) - Lean project for formalizing scientific computing.
- [EconCSLib](https://github.com/gametheoryinlean/EconCSLib) - Library and knowledge base for computational economics: games, social choice, fair division, matching and mechanism design.
- [AppliedModelingLib](https://github.com/nikhgarg/AppliedModelingLib) - AI-assisted workflow for formalizing economics and computation research papers, formerly also named EconCSLib ([paper](https://arxiv.org/abs/2606.13306)).
- [EconLib](https://fortune.com/2026/06/01/axiom-math-econlib-antitrust-economic-theory-verified/) - Axiom Math's formally verified library of economic theory, starting with Aumann's agreement theorem ([GitHub](https://github.com/AxiomMath/AgreeToDisagree)).
- [StatsMLlib](https://github.com/Lean-MoDS/StatsMLlib) - Sorry-free library for probability, high-dimensional statistics, empirical processes and learning theory ([Lean-MoDS](https://github.com/Lean-MoDS)).
- [linglib](https://github.com/hawkrobe/linglib) - Library for formal linguistics across semantics, syntax, pragmatics, morphology and phonology.
- [Balancing a robot using Lean](https://www.galois.com/articles/real-time-robotics-control-in-the-lean-language) - An experiment at Galois Inc.

## Software verification

- [Cedar](https://github.com/cedar-policy/cedar-spec) - Lean formalization and proofs for AWS's Cedar authorization language.
- [Aeneas](https://github.com/AeneasVerif/aeneas) - Verification toolchain that translates Rust programs into Lean.
- [LNSym](https://github.com/leanprover/LNSym) - Symbolic simulator for Armv8 machine code.
- [SampCert](https://github.com/leanprover/SampCert) - Verified implementation of differential privacy samplers.
- [Iris-Lean](https://github.com/leanprover-community/iris-lean) - Port of the Iris separation logic framework to Lean 4.
- [Veil](https://github.com/verse-lab/veil) - Framework for verifying distributed protocols.
- [Velvet](https://github.com/verse-lab/velvet) - Dafny-style verifier for imperative programs that mixes SMT automation with interactive Lean proofs.
- [Loom](https://github.com/verse-lab/loom) - Framework for building foundational multi-modal program verifiers in Lean.
- [Verified SymCrypt](https://www.microsoft.com/en-us/research/blog/verifying-rust-cryptography-in-symcrypt-from-standards-to-code/) - Microsoft Research verifies Rust cryptography in SymCrypt with Aeneas and Lean ([GitHub](https://github.com/microsoft/SymCrypt/tree/feature/verifiedcrypto)).
- [Strata](https://github.com/strata-org/Strata) - Extensible intermediate verification language framework built in Lean.
- [LeanMachines](https://github.com/lean-machines-central/lean-machines) - Event-B inspired framework for modeling and stepwise refinement of stateful systems.
- [lean4-mlir](https://github.com/brettkoonce/lean4-mlir) - Neural networks specified in Lean with machine-checked gradients, compiled through MLIR to GPU ([book](https://lean.brettkoonce.com/blueprint/)).

## AI and machine learning

### Models and provers

- [Leanstral](https://mistral.ai/news/leanstral) - Vibe coding model built by Mistral.ai.
- [AlphaProof](https://deepmind.google/discover/blog/ai-solves-imo-problems-at-silver-medal-level/) - Google DeepMind's reinforcement-learning prover that reached IMO silver-medal level in Lean.
- [DeepSeek-Prover-V2](https://github.com/deepseek-ai/DeepSeek-Prover-V2) - Open-weight theorem proving model for Lean 4.
- [Kimina-Prover](https://github.com/MoonshotAI/Kimina-Prover-Preview) - Open reasoning-based prover for Lean 4.
- [Goedel-Prover-V2](https://github.com/Goedel-LM/Goedel-Prover-V2) - Open-source automated theorem prover for Lean 4.

### Benchmarks and datasets

- [miniF2F (Lean 4)](https://github.com/yangky11/miniF2F-lean4) - Olympiad-level formal problem benchmark.
- [PutnamBench](https://github.com/trishullab/PutnamBench) - Benchmark of Putnam competition problems.
- [ProofNet](https://github.com/zhangir-azerbayev/ProofNet) - Benchmark for autoformalization and proving of undergraduate mathematics.
- [Lean Eval](https://lean-lang.org/eval/) - Lean FRO's public leaderboard of hard formalization problems, judged by Comparator ([problems](https://github.com/leanprover/lean-eval)).

### Tools for AI

- [LeanDojo](https://github.com/lean-dojo/LeanDojo) - Toolkit for extracting data and interacting with Lean programmatically.
- [Lean Copilot](https://github.com/lean-dojo/LeanCopilot) - LLM-powered tactic suggestions inside Lean.
- [REPL](https://github.com/leanprover-community/repl) - JSON read-eval-print loop for driving Lean from other programs.
- [lean-lsp-mcp](https://github.com/oOo0oOo/lean-lsp-mcp) - Model Context Protocol server exposing the Lean language server to agents.
- [Eggshell](https://github.com/momonpya/eggshell) - Local memory that lets AI agents reuse prior work across chats, with a core and contracts written in Lean.
- [Epistemic Protocols](https://github.com/jongwony/epistemic-protocols) - Human-AI collaboration protocols whose contracts are modeled and checked in Lean.
- [lint-llm-proofs](https://github.com/jessealama/lint-llm-proofs) - Linters with automatic fixes for patterns typical of LLM-generated proofs.

## Papers

- [The Lean 4 Theorem Prover and Programming Language](https://doi.org/10.1007/978-3-030-79876-5_37) - De Moura and Ullrich, CADE 2021 ([GitHub](https://github.com/leanprover/lean4)).
- [The Lean Mathematical Library](https://doi.org/10.1145/3372885.3373824) - The mathlib Community, CPP 2020 ([GitHub](https://github.com/leanprover-community/mathlib4)).
- [Velvet: A Foundational Multi-Modal Verifier for Imperative Programs in Lean](https://ilyasergey.net/assets/pdf/papers/velvet-cav26.pdf) - CAV 2026 distinguished paper ([GitHub](https://github.com/verse-lab/velvet)).
- [Lessons from Building an Auto-Active Verifier in Lean](https://popl26.sigplan.org/details/dafny-2026-papers/14/Lessons-from-Building-an-Auto-Active-Verifier-in-Lean) - Experience report on building Veil, Dafny 2026 workshop at POPL ([GitHub](https://github.com/verse-lab/veil)).
- [Lean Atlas](https://arxiv.org/abs/2604.16347) - Integrated proof environment for scalable human-AI collaborative formalization ([GitHub](https://github.com/NyxFoundation/lean-atlas)).

## Funding calls

- [DARPA Exponential Mathematics](https://www.darpa.mil/research/programs/expmath-exponential-mathematics) - DARPA program.
- [AI for Math Fund](https://www.renaissancephilanthropy.org/ai-for-math-fund) - Renaissance Philanthropy and XTX Markets grants for AI-assisted mathematics.

## Organizations

- [Lean FRO](https://lean-lang.org/fro/) - Lean Focused Research Organization, stewarding Lean's development ([LinkedIn](https://www.linkedin.com/company/lean-fro/), [roadmap](https://lean-lang.org/fro/roadmap/), [GitHub](https://github.com/leanprover)).

## Companies

- [Axiom](https://axiommath.ai) - AI for mathematics startup ([NYTimes article](https://www.nytimes.com/2026/03/12/technology/axiom-ai-code-funding.html), [GitHub](https://github.com/AxiomMath)).
- [Harmonic](https://harmonic.fun) - Builder of Aristotle, a Lean-verified mathematical reasoning model.
- [Math Inc](https://math.inc) - Autoformalization company behind the Gauss agent ([GitHub](https://github.com/math-inc)).
- [hestia.ai](https://hestia.ai) - Data and AI company.
- [StartClaims](https://startclaims.eu) - Formally verified claims calculation, using Lean to make evidence and reasoning checkable.

## Videos

- [Infinitude of Primes](https://www.youtube.com/watch?v=b59fpAJ8Mfs) - Scott Morrison proves in Lean that there is an infinitude of primes.
- [Formalizing the Future: Lean’s Impact on Mathematics, Programming, and AI](https://podcasts.ox.ac.uk/formalizing-future-leans-impact-mathematics-programming-and-ai) - Oxford lecture by Leo de Moura.
- [Lean FRO channel](https://www.youtube.com/@leanfro) - Talks and updates from the Lean Focused Research Organization.
- [leanprover community channel](https://www.youtube.com/@leanprovercommunity5485) - Recordings of community talks, workshops and demos.
- [Terence Tao](https://www.youtube.com/@TerenceTao27) - Screencasts of Terence Tao formalizing mathematics in Lean, often with AI tools.

## Podcasts

- [Metaprogramming Your IDE in Lean 4](https://podcasts.apple.com/vn/podcast/metaprogramming-your-ide-in-lean-4-with-harry-goldstein/id1602572955?i=1000742230030) - Harry Goldstein at Software Unscripted.
- [Z3 and Lean, the Spiritual Journey](https://www.typetheoryforall.com/episodes/z3-and-lean-the-spiritual-journey) - Leo de Moura on Type Theory Forall.
- [Why Harmonic Thinks AI Is About to Change Math](https://www.sequoiacap.com/podcast/training-data-harmonic/) - Vlad Tenev and Tudor Achim on Sequoia's Training Data.

## Blogs and news

- [Xena Project](https://xenaproject.wordpress.com) - Kevin Buzzard's blog on formalizing mathematics.
- [Leo de Moura's blog](https://leodemoura.github.io/blog/) - Writing by Lean's creator.
- [Lean Community Blog](https://leanprover-community.github.io/blog/) - Posts from the Lean community.
- [Lean links page](https://lean-lang.org/links/) - Lots of popular links and press coverage about Lean.

## Chat and social

- [Zulip](https://leanprover.zulipchat.com/) - Main discussion forum for the Lean community.
- [X (Twitter)](https://x.com/leanprover) - Official Lean account.
- [Mastodon](https://functional.cafe/@leanprover) - Official Lean account.

## Other meta-resources

- [Lean Community learning resources](https://leanprover-community.github.io/learn.html) - Curated learning paths for different audiences.
- [Lean Community events](https://leanprover-community.github.io/events.html) - Upcoming and past workshops, conferences and schools.
- [Mathlib overview](https://leanprover-community.github.io/mathlib-overview.html) - Map of the mathematics currently covered by Mathlib.

## To sort

- Entropy42 - Company, link needed.
