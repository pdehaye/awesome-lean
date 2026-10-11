# leanprover-community/quote4

- **Domain:** Metaprogramming infrastructure: typed expression quotations (`Q(α)`, `q(...)`, `~q(...)` matching) for writing Lean metaprograms.
- **Primary role:** `DSL-host/metaprogramming`
- **Secondary roles:** none
- **What the kernel checks:** Types only. There are no theorems (the Phase 1 count is 0). Type safety holds at elaboration time: `Quoted α` is definitionally just `Expr` (`Qq/Typ.lean`), and the claim that a value has type `α` is checked when the quotation is elaborated, not by the kernel at runtime. `Quoted.check` can re-check it in `MetaM`. `QuotedDefEq` is a `Prop` structure with an `unsafeIntro` constructor, so defeq claims are trusted assumptions.
- **Certified vs only expressed:** Nothing is proven. Lean's elaborator is used to give meta-level code more precise types.
- **Output artifact:** A library of term elaborators, macros, and a `match`/`let` extension, used by Mathlib and others (for example, iris-lean depends on it).
- **Author mode:** Human. I found no evidence of AI authorship.
- **Translation direction:** None.
- **Creative idea:** quote4 uses Lean's dependent types to type metaprograms: an object-level term of type `α` gets the meta-level type `Q(α)`, with typing rules taken from modal sequent calculus. Quotations elaborate in a context where each antiquoted variable `$a : Q(α)` is treated as an object-level `a : α`.
- **Why Lean?:** The README argues for it in terms of Lean features: `betterApp` compiles to one `betaRev` call, needs no `MetaM`, and has its implicit arguments inferred. My assessment: this needs a meta-language that is the same dependently typed language as the object language, which Lean 4 provides. Python or Dafny have no equivalent.
- **Notable techniques:**
  - `Quoted α := Expr` with coercions: `Qq/Typ.lean`.
  - Unquoting `Q(·)` types into a local context and quoting `Expr` back into code (`unquoteExpr`, `quoteExpr`, `quoteLCtx`): `Qq/Macro.lean`.
  - `~q(pattern)` matching inside `match`/`let`, instance-aware: `Qq/Match.lean`.
  - Delaborator for pretty-printing quoted terms: `Qq/Delab.lean`.
- **Heuristic check:** The Phase 1 guess was `DSL/metaprogramming + computation/examples`. I agree on the primary role. The `#eval`s in `QqTest/` are tests, not a separate role.
- **Evidence:** `README.md`, `lakefile.toml`, `Qq/Typ.lean`, `Qq/Macro.lean` (greps), `Qq/Match.lean` (header), `QqTest/` listing.
