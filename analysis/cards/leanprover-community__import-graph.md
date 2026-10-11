# leanprover-community/import-graph

- **Domain:** Analysis and visualisation of module import structure in Lake packages (used by Mathlib).
- **Primary role:** `program`
- **Secondary roles:** `DSL-host/metaprogramming`, `interactive/teaching`
- **What the kernel checks:** mostly nothing; a handful of small lemmas about the internal `NeedsKind`/`Needs` algebra are fully proven with `simp`/`grind` (e.g. `andThen_assoc` in `ImportGraph/Shake/Basic.lean`). Tests in `ImportGraphTest` use `#guard_msgs`.
- **Certified vs only expressed:** proven: a few algebraic properties of the dependency-kind combinator. Everything else (graph construction, unused/redundant import detection, `#find_home`) is just run; docstrings note heuristics "will *not* account for tactics and syntax" (`ImportGraph/Imports/RequiredModules.lean`).
- **Output artifact:** executables (`lake exe graph` emitting `.dot`/`.gexf`/HTML, `unused_transitive_imports`, a workspace-summary JSON emitter) and editor commands (`#redundant_imports`, `#min_imports`, `#find_home`, `#import_diff`).
- **Author mode:** human (headers: Jon Eugster, Kim Morrison, Thomas Murrills, others); no AI-agent files found.
- **Translation direction:** out of Lean (environment to Graphviz DOT / GEXF / JSON).
- **Creative idea:** It inspects the compiled `Environment` itself (constant-to-module index, transitively used constants) to compute which imports a file actually needs, and surfaces the answers as clickable infoview widgets.
- **Why Lean?:** not stated. Own assessment: the data (import DAG, constant usage, meta/private visibility) lives only in Lean's environment, so the tool must be in Lean.
- **Notable techniques:**
  - `withImportModules` + `CoreM.toIO` to load a package environment from a CLI (`MainGraph.lean`).
  - Command elaborators for import hygiene (`ImportGraph/Tools/MinImports.lean`, `ImportGraph/Tools/FindHome.lean`).
  - Bitset-encoded "needs" lattice with `grind`-proven lemmas (`ImportGraph/Shake/Basic.lean`).
  - `@[server_rpc_method]` widget resolving module names to source URIs (`ImportGraph/Widget/GoToModule.lean`).
- **Heuristic check:** the Phase 1 guess was `DSL/metaprogramming + program + computation/examples + interactive`. Agree with program/meta/interactive; "computation/examples" is just `#eval`/`#guard_msgs` test usage. It misses that a small part is actually proven.
- **Evidence:** `README.md`, `lakefile.toml`, `MainGraph.lean`, `ImportGraph/Shake/Basic.lean` (parts), `ImportGraph/Widget/GoToModule.lean` (head), `ImportGraph/Export/Gexf.lean` (head), grep over `ImportGraph/Tools/*.lean`, `ImportGraph/Imports/RequiredModules.lean`.
