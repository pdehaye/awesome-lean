# lean-dojo/LeanCopilot

- **Domain:** LLM-assisted theorem proving inside Lean: tactic suggestion, proof search and premise selection.
- **Primary role:** `DSL-host/metaprogramming`
- **Secondary roles:** `AI-oracle/referee`, `program`
- **What the kernel checks:** Nothing of the repo's own (0 theorems). In user proofs, LLM-suggested tactics are run by the elaborator before they are shown (`hint` with `checkTactics`), and an accepted proof goes through normal kernel checking.
- **Certified vs only expressed:** Nothing about the tool is proven. Lean hosts the tactics, runs model inference through FFI, and filters model output by executing it.
- **Output artifact:** Tactics (`suggest_tactics`, `search_proof`, `select_premises`) and "Try this" suggestions in the editor, plus a model-download executable.
- **Author mode:** Human-written tooling whose runtime output is AI-generated tactic text.
- **Translation direction:** none. Goals are pretty-printed to text for the model, and model text is parsed back as `tactic` syntax.
- **Creative idea:** Native LLM inference (CTranslate2 via `@[extern]`) runs inside the Lean process as a tactic. Each generated string is parsed and executed against the goal, and only the ones that actually work are kept.
- **Why Lean?:** The README's case is that LLMs are used "natively in Lean" in the proof workflow. Own assessment: a Python wrapper (LeanDojo-style) would sit outside the editor. Hosting the model in Lean puts suggestions in the infoview and lets aesop use them as a rule.
- **Notable techniques:**
  - `@[extern]` opaque bindings to a C++ CTranslate2 wrapper for generate/encode/retrieve (`LeanCopilot/Models/FFI.lean`), with Lake targets that build or download `libctranslate2` (`lakefile.lean`).
  - Parse-and-run filtering of suggestions with `runParserCategory` and `evalTactic` inside `observing?`, keeping a goal-closing one (`LeanCopilot/Frontend.lean`, `hint`).
  - LLM as an aesop rule: `search_proof` expands to `aesop? (add 100% tacGen)` (`LeanCopilot/LlmAesop.lean`).
  - External models via JSON over `curl` to a local server (`LeanCopilot/Models/External.lean`).
- **Heuristic check:** The Phase 1 guess was `DSL/metaprogramming + program + computation/examples`. I agree. The `#eval` examples are model-API demos, not computations being certified.
- **Evidence:** `README.md`, `lakefile.lean` (grep of targets), `LeanCopilot/Tactics.lean`, `LeanCopilot/LlmAesop.lean`, `LeanCopilot/Frontend.lean`, `LeanCopilot/Models/FFI.lean`, `LeanCopilot/Models/External.lean`.
