# leanprover/doc-gen4

- **Domain:** API documentation generator for Lean 4 libraries (produces the Mathlib/Lean docs sites).
- **Primary role:** `program`
- **Secondary roles:** `DSL-host/metaprogramming`
- **What the kernel checks:** nothing. No theorems; output rendering uses `partial def` with a "TODO: Termination proof" note (`DocGen4/Output/ToHtmlFormat.lean`).
- **Certified vs only expressed:** nothing is proven. Lean is the implementation language; it loads a project's environment and pretty-prints declarations. The README notes it documents code containing `sorry` but not code that fails to compile.
- **Output artifact:** static HTML/JS documentation site, JSON, and an SQLite database of declarations and docstrings.
- **Author mode:** human (headers: Henrik Böving, Wojciech Nawrocki, Sebastian Ullrich); no AI-agent files found.
- **Translation direction:** out of Lean (Lean environment to HTML/SQLite).
- **Creative idea:** The generator is driven as Lake build facets (`lake build Lib:docs`), so documentation pages are incremental build artifacts per module, and the HTML templates are written in an in-Lean JSX syntax.
- **Why Lean?:** not stated. Own assessment: it needs Lean's environment loader, `ppExprWithInfos`, docstring and attribute data, so it has to be written in Lean.
- **Notable techniques:**
  - JSX-like syntax categories (`jsxElement`, `jsxChild`) macro-expanded to an `Html` inductive (`DocGen4/Output/ToHtmlFormat.lean`, used in `DocGen4/Output/Template.lean`).
  - Custom `module_facet`/`library_facet`/`package_facet` definitions (`docInfo`, `docs`, `srcUri`) that also shell out to git for source links (`lakefile.lean`).
  - Environment import with `importModules ... (loadExts := true)` and pretty-printing with info trees (`DocGen4/Load.lean`, `DocGen4/Process/Base.lean`).
  - SQLite storage via `leansqlite`, schema as DDL strings (`DocGen4/DB/Schema.lean`); CLI via `lean4-cli` `` `[Cli| ...] `` syntax (`Main.lean`).
- **Heuristic check:** the Phase 1 guess was `DSL/metaprogramming + program + interactive`. Partly disagree: I see no `interactive` role. The output is a static website, and the `widget` hits seem incidental. `program` should be primary.
- **Evidence:** `README.md`, `lakefile.lean`, `Main.lean` (grep), `DocGen4/Output/ToHtmlFormat.lean`, `DocGen4/Output/Template.lean`, `DocGen4/DB/Schema.lean` (grep), `DocGen4/Process/Analyze.lean` (head), `DocGen4/Load.lean` (grep).
