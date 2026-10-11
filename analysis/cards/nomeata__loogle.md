# nomeata/loogle

- **Domain:** Search engine for declarations in Lean/Mathlib environments (CLI, web backend, Zulip bot, `#find` command).
- **Primary role:** `program`
- **Secondary roles:** `DSL-host/metaprogramming`
- **What the kernel checks:** nothing of substance. The ~13 `theorem`s and 4 `sorry`s in `Tests.lean` are search fixtures (e.g. `my_true_eq_true`), checked only via `#guard_msgs` output comparison.
- **Certified vs only expressed:** nothing about loogle itself is proven. Lean is the implementation language and the runtime: queries are elaborated as Lean terms and matched against `ConstantInfo` types with `MetaM` unification.
- **Output artifact:** executable (`loogle` CLI, JSON output) plus a `#find` command; search results.
- **Author mode:** human (Joachim Breitner, Mario Carneiro in headers); no AI-agent files found.
- **Translation direction:** none.
- **Creative idea:** A search engine whose query language *is* Lean term syntax: patterns like `(List.replicate (_ + _) _ = _)` are elaborated with metavariables and matched up to reducible defeq against every constant in an imported environment.
- **Why Lean?:** not stated. Own assessment: the tool must load `.olean` environments and reuse Lean's elaborator and unifier, so it can only be written in Lean (or against Lean's internals).
- **Notable techniques:**
  - Term-pattern matching via `AbstractMVarsResult` and `withReducible` unification; suffix trie over names for string fragments (`Loogle/Find.lean`, `Loogle/Trie.lean`).
  - On-disk index cache written with `saveModuleData`/`readModuleData` and `unsafeCast` ("pickling", vendored from Batteries) (`Loogle/Pickle.lean`, `Loogle/Cache.lean`).
  - `@[builtin_term_parser]` for the `⊢ T` turnstile query syntax, made visible via `precompileModules := true` (`Loogle/Parsers.lean`, `lakefile.lean` comments).
  - Optional seccomp sandboxing through FFI (`@[extern "loogle_seccomp"]`) toggled by a custom `#ifEnv` command elaborator (`Seccomp.lean`, `Loogle.lean` around `Seccomp.enable`).
- **Heuristic check:** the Phase 1 guess was `DSL/metaprogramming + program + computation/examples`. Mostly agree, but `program` is primary: metaprogramming is the means, a search service is the product. "computation/examples" reflects `#guard_msgs` tests, not computation-as-proof.
- **Evidence:** `README.md`, `lakefile.lean`, `Seccomp.lean`, `LoogleMain.lean`, `Loogle.lean` (grep), `Loogle/Find.lean` (skim), `Loogle/Pickle.lean`, `Loogle/Parsers.lean` (grep), `Tests.lean` (grep).
