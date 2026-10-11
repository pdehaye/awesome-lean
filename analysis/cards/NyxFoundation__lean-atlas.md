# NyxFoundation/lean-atlas

- **Domain:** Reviewing large (often AI-generated) formalizations for semantic faithfulness, through dependency-graph visualization.
- **Primary role:** `coordination/trust-infrastructure`
- **Secondary roles:** `DSL-host/metaprogramming`, `program`
- **What the kernel checks:** Nothing of its own (0 theorems). It reads the already-checked environment of a target project.
- **Certified vs only expressed:** Nothing is proven. Lean is used to annotate declarations (confidence, progress, main theorem) and to compute dependency graphs from elaborated constants.
- **Output artifact:** JSON graph data (`lake exe atlas graph-data`), served to a Next.js viewer, plus a "review cone" of nodes that humans should check.
- **Author mode:** Human-authored tool, aimed at human-AI collaborative formalization (README subtitle and "semantic hallucination" motivation).
- **Translation direction:** Out of Lean (environment to JSON/DOT for a web UI).
- **Creative idea:** It splits dependencies into type-level versus proof-level edges and prunes proof-level ones ("Lean Compass"). What remains is the small set of definitions and statements a human must read to trust that the main theorems mean what they should, given that the kernel already vouches for the proofs.
- **Why Lean?:** Stated indirectly: the type checker guarantees logical correctness but not intent, so review effort should go only where semantics can change. Own assessment: the edge classification needs exact access to `ConstantInfo.type` versus `value`, which only Lean's own environment gives faithfully.
- **Notable techniques:**
  - Edge classification via `ci.type.getUsedConstantsAsSet` versus value constants (`LeanAtlas/Deps/Core.lean`).
  - Compass traversal that excludes `theoremValue*` edges (`LeanAtlas/Compass/Main.lean`, `isCompassEdge`).
  - Custom attributes stored in persistent environment extensions (`LeanAtlas/Metadata/Attribute/Meta.lean`, `Confidence.lean`, `ProofProgress.lean`).
  - Linters that warn when review attributes are missing, scoped by a registered option (`LeanAtlas/Metadata/Linter.lean`).
- **Heuristic check:** The Phase 1 guess was `DSL/metaprogramming + program`. I partly disagree. The metaprogramming is real, but the purpose is review and trust infrastructure for AI-produced proofs, so I put it as primary.
- **Evidence:** `README.md`, `lakefile.toml`, `LeanAtlas/Metadata/Attribute/Meta.lean`, `LeanAtlas/Metadata/Linter.lean`, `LeanAtlas/Deps/Core.lean` (grep), `LeanAtlas/GraphData/Core.lean` (grep), `LeanAtlas/Compass/Main.lean`, `LeanAtlas/CLI/Serve.lean` (grep).
