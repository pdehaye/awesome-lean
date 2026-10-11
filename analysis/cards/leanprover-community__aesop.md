# leanprover-community/aesop

- **Domain:** Proof automation: a general-purpose, extensible proof-search tactic for Lean 4 (similar to Isabelle's `auto`).
- **Primary role:** `DSL-host/metaprogramming`
- **Secondary roles:** `certifier-math` (only indirectly: every proof it builds is a kernel-checked term in the user's development)
- **What the kernel checks:** When `aesop` succeeds, the proof term assembled from the search tree is checked by the kernel like any other proof. The tactic's own code is not verified. The `AesopTest/` files are regression tests: `example`s run through `aesop`, plus `axiom`s used as test fixtures (e.g. `AesopTest/205.lean`).
- **Certified vs only expressed:** Nothing about Aesop's search procedure is proven. It produces certified proofs for user goals. Its correctness depends only on the kernel re-checking the extracted term (`Aesop/Tree/ExtractProof.lean`).
- **Output artifact:** A tactic (`aesop`, `aesop?`), an `@[aesop]` attribute, rule-set commands, and generated tactic scripts.
- **Author mode:** Human. The copyright headers name Jannis Limperg (`Aesop/Main.lean`). I found no evidence of AI authorship.
- **Translation direction:** Out of Lean, in a narrow sense: `aesop?` turns the found proof into Lean tactic-script syntax (`Aesop/Script/`). Otherwise none.
- **Creative idea:** Aesop makes proof search a user-programmable system: rules are arbitrary tactics registered via an attribute DSL with safe/norm/unsafe phases and priorities, explored best-first over an explicit search tree inside `MetaM`.
- **Why Lean?:** Not stated directly; the README compares it to Isabelle's `auto`. My assessment: it depends on Lean's in-language metaprogramming (`TacticM`, discrimination-tree indexing, `simp_all`), so it can be written and extended in the same language and library as the proofs it serves. Mathlib's `measurability` and `continuity` are built on it (README).
- **Notable techniques:**
  - Attribute and command DSL with its own syntax categories (`Aesop.phase`, `Aesop.priority`, `Aesop.builder_name`): `Aesop/Frontend/RuleExpr.lean`, `Aesop/Frontend/Attribute.lean`, `Aesop/Frontend/Command.lean`.
  - Best-first search loop with goal/rapp limits over an AND-OR tree: `Aesop/Search/Main.lean`, `Aesop/Tree/`.
  - Generating a proof script from the search tree (unstructured to structured scripts): `Aesop/Script/UScriptToSScript.lean`, `Aesop/Search/Main.lean` (`traceScript`).
  - Profiling and statistics collection: `Aesop/Main.lean`, `Aesop/Stats/`.
- **Heuristic check:** The Phase 1 guess was `DSL/metaprogramming + computation/examples`. I agree on DSL/metaprogramming. The "examples" are tactic regression tests, not computation.
- **Evidence:** `README.md`, `lakefile.toml`, `Aesop.lean`, `Aesop/Main.lean`, `Aesop/Search/Main.lean` (definitions list), `Aesop/Frontend/*.lean` (syntax grep), `AesopTest/205.lean` (axiom grep), directory listings of `Aesop/Script`, `Aesop/Tree`.
