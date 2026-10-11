# <owner>/<repo>

- **Domain:** what field or problem it addresses.
- **Primary role:** exactly one of: `certifier-math`, `certifier-software`, `specification/modeling`, `program`, `DSL-host/metaprogramming`, `AI-oracle/referee`, `coordination/trust-infrastructure`, `interactive/teaching`.
- **Secondary roles:** zero or more from the same list.
- **What the kernel checks:** full proofs / types only / computation via `decide` or `#eval` / tests / nothing. Give evidence.
- **Certified vs only expressed:** what is actually proven, and what Lean is only used to state, model, generate or run.
- **Output artifact:** theorems, executable, document, data, verdict, interactive UI, generated code…
- **Author mode:** human / AI / mixed, with evidence.
- **Translation direction:** into Lean (another language translated to Lean), out of Lean (Lean generating something else), or none.
- **Creative idea:** one sentence on what is unusual about how this project uses Lean.
- **Why Lean?:** what would be lost if this were written in Python, Coq/Rocq, Isabelle or Dafny. Say "not stated" if the repo doesn't argue it, then give your own assessment, labeled as such.
- **Notable techniques:** 2–4 concrete techniques, each with a file path.
- **Heuristic check:** the Phase 1 guess was `<guess>`. Agree or disagree, and why.
- **Evidence:** the files you actually read.
