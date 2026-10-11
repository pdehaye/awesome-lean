# jongwony/epistemic-protocols

- **Domain:** Human–AI collaboration protocols, packaged as Claude Code/Codex plugins (`/inquire`, `/elicit`, `/bound`, and others) that bring key decisions back to the user.
- **Primary role:** `specification/modeling`
- **Secondary roles:** `certifier-software`, `DSL-host/metaprogramming`
- **What the kernel checks:** Full proofs of small "guarantee" theorems about each protocol contract (for example `settled_not_ai` and `held_only_by_person` in `lean/EpistemicProtocols/Aitesis/Theorems.lean`). The contracts declare the model's judgments as `axiom`s. A Lean audit checks that proofs depend only on `propext`, `Classical.choice`, `Quot.sound` plus those declared judgments.
- **Certified vs only expressed:** Proven: structural properties of the contract model, for example that only person-origin turns can settle or dismiss an entry. Only expressed: the protocol behaviour itself. Each SKILL.md contains a Lean block that an LLM reads as instructions. Its `axiom`s are, in the block's words, judgments "yours to make" as "the model it is written for". Whether the LLM follows the block is not checked.
- **Output artifact:** Agent skills (prompts with Lean contracts embedded), theorems, and a JSON audit report (`lake lint`).
- **Author mode:** Mixed or AI-heavy. Commits carry `Co-Authored-By: Claude Opus 5.5` and mention codex review (git log).
- **Translation direction:** Into Lean. Lean blocks are extracted from SKILL.md into `lean/.contract/` by a Node script (`lakefile.toml` comment).
- **Creative idea:** Lean is the prompt language. The LLM is cast as the logical "model" of the contract's axioms, and the theorems state what holds whatever judgments the model makes.
- **Why Lean?:** Not stated beyond "core Lean 4 and elaborates as written". My assessment: a typed, checkable notation is more precise than prose, and plain Lean with no Mathlib keeps it light. Python could not give the elaboration check.
- **Notable techniques:**
  - A shared GROUND module (turn origins, `Cite`, `Occ`) that must appear verbatim in every SKILL.md block (`lean/EpistemicProtocols/Ground.lean`).
  - An audit that reads the elaborated environment and uses `Lean.collectAxioms` (`lean/Audit/Check.lean`, `lean/Audit/Main.lean`).
  - Fixtures that break each audit rule as tests (`lean/Tests/Fixture/{Good,Bad,Foreign,Unwired}`).
  - `warningAsError = true` across the build (`lakefile.toml`).
- **Heuristic check:** The Phase 1 guess was `tool-around-Lean + certifier + program + computation/examples`. I disagree. The core use is Lean as a specification and prompt language for agents, with small proofs about that model.
- **Evidence:** `README.md`, `lakefile.toml`, `lean/EpistemicProtocols/Ground.lean`, `lean/EpistemicProtocols/Aitesis/Theorems.lean`, `lean/Audit/Check.lean`, `lean/Audit/Main.lean`, `aitesis/skills/inquire/SKILL.md` (fetched), git log.
