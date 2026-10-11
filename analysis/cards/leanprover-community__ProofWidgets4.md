# leanprover-community/ProofWidgets4

- **Domain:** User-interface components for the Lean infoview: visualisations, custom goal displays, point-and-click proof editing.
- **Primary role:** `interactive/teaching`
- **Secondary roles:** `DSL-host/metaprogramming`
- **What the kernel checks:** nothing about the library itself. Demos state some theorems but use `axiom test_sorry` as a placeholder (`ProofWidgets/Demos/SelectInsertConv.lean`, `ProofWidgets/Demos/Euclidean.lean`).
- **Certified vs only expressed:** nothing is proven. The `Component` docstring says that defining one means "*asserting* that `Props` is a correct representation of `JsProps`". The Lean/JS interface is trusted, not checked (`ProofWidgets/Component/Basic.lean`).
- **Output artifact:** interactive UI (React components in the VS Code infoview), driven by Lean RPC methods.
- **Author mode:** human (Wojciech Nawrocki, E.W. Ayers, Patrick Massot and others in headers); no AI-agent files found.
- **Translation direction:** out of Lean (Lean `Html`/`Expr` values to JSON props rendered by JavaScript).
- **Creative idea:** "Delaborating into HTML": `ExprPresenter`s turn a goal's `Expr` into interactive HTML that keeps references back to the term, and widgets can edit the proof script (e.g. a `conv?` tactic that writes `conv => enter [...]` from a selected subterm).
- **Why Lean?:** not stated. Own assessment: the components need live access to the elaborator state (goals, `MetaM`, expression positions) over the Lean server's RPC, which only Lean offers in this form. Coq/Isabelle have their own UI extension models, but they are not shared with this one.
- **Notable techniques:**
  - `Component Props` = `Widget.Module` with JS embedded via `include_str` and `@[widget_module]` (`ProofWidgets/Component/Basic.lean`, `ProofWidgets/Component/Recharts.lean`).
  - Scoped JSX syntax categories elaborating to `Html` (`ProofWidgets/Data/Html.lean`), with `#html` display command (`ProofWidgets/Component/HtmlDisplay.lean`).
  - `@[expr_presenter]` attribute plus `evalConstCheck` through an `implemented_by` opaque (`ProofWidgets/Presentation/Expr.lean`).
  - Lakefile targets that run `npm` to build TypeScript before the Lean modules (`lakefile.lean`).
- **Heuristic check:** the Phase 1 guess was `DSL/metaprogramming + program + interactive`. Partly disagree: `interactive` should be primary, and `program` does not fit. It is a library with no `lean_exe`.
- **Evidence:** `README.md`, `lakefile.lean` (grep), `ProofWidgets/Component/Basic.lean`, `ProofWidgets/Presentation/Expr.lean`, `ProofWidgets/Data/Html.lean` (grep), `ProofWidgets/Component/Recharts.lean` (grep), `ProofWidgets/Demos/SelectInsertConv.lean` (head).
