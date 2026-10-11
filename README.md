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
- [Documentation](https://lean-lang.org/documentation/) - Index of the official manuals, books and tutorials.
- [Lean Language Reference](https://lean-lang.org/doc/reference/latest/) - Comprehensive reference manual for the language.
- [Lean Community](https://leanprover-community.github.io/) - Community website with installation instructions, events and Mathlib documentation.

## Getting started

- [elan](https://github.com/leanprover/elan) - Lean toolchain installer and version manager, in the spirit of rustup.
- [Lake](https://github.com/leanprover/lean4/tree/master/src/lake) - Lean's built-in build system and package manager.
- [Reservoir](https://reservoir.lean-lang.org) - Official registry of Lean packages.
- [Lean 4 Web](https://live.lean-lang.org) - Try Lean and Mathlib in the browser with no installation.

## Learning

### Books and tutorials

- [Theorem Proving in Lean 4](https://lean-lang.org/theorem_proving_in_lean4/) - The standard introduction to dependent type theory and proving in Lean.
- [Functional Programming in Lean](https://lean-lang.org/functional_programming_in_lean/) - David Thrane Christiansen's book on Lean as a general-purpose programming language.
- [Mathematics in Lean](https://leanprover-community.github.io/mathematics_in_lean/) - Hands-on introduction to formalizing mathematics with Mathlib.
- [Metaprogramming in Lean 4](https://leanprover-community.github.io/lean4-metaprogramming-book/) - Writing tactics, macros and elaborators.
- [The Mechanics of Proof](https://hrmacbeth.github.io/math2001/) - Heather Macbeth's introduction to proof writing, taught with Lean.
- [Logic and Mechanized Reasoning](https://avigad.github.io/lamr/) - Textbook on logic, SAT/SMT solving and proof assistants.
- [Type Checking in Lean 4](https://ammkrn.github.io/type_checking_in_lean4/) - Guide to Lean's kernel and type theory, aimed at writers of external checkers.

### Games

- [Lean Game Server](https://adam.math.hhu.de) - Collection of browser-based games teaching Lean and mathematics.
- [Natural Number Game](https://adam.math.hhu.de/#/g/leanprover-community/nng4) - The classic gentle introduction to proving theorems about natural numbers.

### Courses

- [Formalising Mathematics](https://b-mehta.github.io/formalising-mathematics-notes/) - Course notes from Kevin Buzzard's Imperial College course.

## Editors and tooling

- [VS Code extension](https://github.com/leanprover/vscode-lean4) - Official Lean 4 extension for Visual Studio Code, with infoview.
- [lean4-mode](https://github.com/leanprover-community/lean4-mode) - Emacs major mode for Lean 4.
- [lean.nvim](https://github.com/Julian/lean.nvim) - Neovim support for Lean 4.
- [doc-gen4](https://github.com/leanprover/doc-gen4) - Documentation generator for Lean 4 projects.
- [Verso](https://github.com/leanprover/verso) - Authoring tool for documentation, books and websites written in Lean.
- [leanblueprint](https://github.com/PatrickMassot/leanblueprint) - Plastex plugin for writing blueprints that track large formalization projects.
- [lean4web](https://github.com/leanprover-community/lean4web) - Self-hostable web editor for Lean 4.

## Search

- [Loogle](https://loogle.lean-lang.org) - Search Mathlib by name, constant and type signature patterns.
- [LeanSearch](https://leansearch.net) - Natural-language semantic search over Mathlib.
- [Moogle](https://www.moogle.ai) - Semantic search engine for Mathlib.

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
- [Sphere Packing](https://github.com/thefundamentaltheor3m/Sphere-Packing-Lean) - Formalization of Viazovska's sphere packing results.
- [Formal Conjectures](https://github.com/google-deepmind/formal_conjectures) - Google DeepMind's collection of formalized open conjectures.

## Thematic projects

- [PhysLean](https://github.com/lean-phys-community/PhysLean) - Lean Community for formalizing physics.
- [SciLean](https://github.com/lecopivo/SciLean) - Lean project for formalizing scientific computing.
- [Balancing a robot using Lean](https://www.galois.com/articles/real-time-robotics-control-in-the-lean-language) - An experiment at Galois Inc.

## Software verification

- [Cedar](https://github.com/cedar-policy/cedar-spec) - Lean formalization and proofs for AWS's Cedar authorization language.
- [Aeneas](https://github.com/AeneasVerif/aeneas) - Verification toolchain that translates Rust programs into Lean.
- [LNSym](https://github.com/leanprover/LNSym) - Symbolic simulator for Armv8 machine code.
- [SampCert](https://github.com/leanprover/SampCert) - Verified implementation of differential privacy samplers.
- [Iris-Lean](https://github.com/leanprover-community/iris-lean) - Port of the Iris separation logic framework to Lean 4.
- [Veil](https://github.com/verse-lab/veil) - Framework for verifying distributed protocols.
- [Strata](https://github.com/strata-org/Strata) - Extensible intermediate verification language framework built in Lean.

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

### Tools for AI

- [LeanDojo](https://github.com/lean-dojo/LeanDojo) - Toolkit for extracting data and interacting with Lean programmatically.
- [Lean Copilot](https://github.com/lean-dojo/LeanCopilot) - LLM-powered tactic suggestions inside Lean.
- [REPL](https://github.com/leanprover-community/repl) - JSON read-eval-print loop for driving Lean from other programs.
- [lean-lsp-mcp](https://github.com/oOo0oOo/lean-lsp-mcp) - Model Context Protocol server exposing the Lean language server to agents.

## Papers

- [The Lean 4 Theorem Prover and Programming Language](https://doi.org/10.1007/978-3-030-79876-5_37) - De Moura and Ullrich, CADE 2021.
- [The Lean Mathematical Library](https://doi.org/10.1145/3372885.3373824) - The mathlib Community, CPP 2020.

## Funding calls

- [DARPA Exponential Mathematics](https://www.darpa.mil/research/programs/expmath-exponential-mathematics) - DARPA program.
- [AI for Math Fund](https://www.renaissancephilanthropy.org/ai-for-math-fund) - Renaissance Philanthropy and XTX Markets grants for AI-assisted mathematics.

## Organizations

- [Lean FRO](https://lean-fro.org) - Lean Focused Research Organization, stewarding Lean's development ([LinkedIn](https://www.linkedin.com/company/lean-fro/)).

## Companies

- [Axiom](https://axiommath.ai) - AI for mathematics startup ([NYTimes article](https://www.nytimes.com/2026/03/12/technology/axiom-ai-code-funding.html)).
- [Harmonic](https://harmonic.fun) - Builder of Aristotle, a Lean-verified mathematical reasoning model.
- [Math Inc](https://math.inc) - Autoformalization company behind the Gauss agent.
- [hestia.ai](http://hestia.ai) - Data and AI company.

## Videos

- [Infinitude of Primes](https://www.youtube.com/watch?v=b59fpAJ8Mfs) - Scott Morrison proves in Lean that there is an infinitude of primes.
- [Formalizing the Future: Lean’s Impact on Mathematics, Programming, and AI](https://podcasts.ox.ac.uk/formalizing-future-leans-impact-mathematics-programming-and-ai) - Oxford lecture by Leo de Moura.

## Podcasts

- [Metaprogramming Your IDE in Lean 4](https://podcasts.apple.com/vn/podcast/metaprogramming-your-ide-in-lean-4-with-harry-goldstein/id1602572955?i=1000742230030) - Harry Goldstein at Software Unscripted.

## Blogs and news

- [Xena Project](https://xenaproject.wordpress.com) - Kevin Buzzard's blog on formalizing mathematics.
- [Lean Community Blog](https://leanprover-community.github.io/blog/) - Posts from the Lean community.
- [Lean links page](https://lean-lang.org/links/) - Lots of popular links and press coverage about Lean.

## Chat and social

- [Zulip](https://leanprover.zulipchat.com/) - Main discussion forum for the Lean community.
- [Twitter](https://twitter.com/leanprover) - Official Lean account.
- [Mastodon](https://functional.cafe/@leanprover) - Official Lean account.

## Other meta-resources

- [Lean Community learning resources](https://leanprover-community.github.io/learn.html) - Curated learning paths for different audiences.

## To sort

- Entropy42 - Company, link needed.
- "Lessons from Building an Auto-Active Verifier in Lean" - Link needed.
