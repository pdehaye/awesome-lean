# verse-lab/veil: agent setup

- **Snapshot:** commit `529eb3b` (2026-10-12), from `repos/verse-lab__veil/snapshot.json`.
- **Tools targeted:** Claude Code (`.claude/CLAUDE.md`).
- **Files:** `.claude/CLAUDE.md`: a short project overview, a directory map and two notes.
- **What agents are asked to do:** implement features in the Veil library (frontend syntax, utilities, the model checker). The file notes that `Examples/` usually doesn't need checking "If your task is to implement something for Veil". It points to `README.md` for the specification syntax.
- **Build and verification:** "Whenever you've finished implementing certain feature, remember to run `lake build VeilTest` to go through all unit tests."
- **Proof policy:** none stated.
- **Lean and Mathlib guidance:** for proofs about built-in Lean definitions, "one good way is to search on [Loogle](https://loogle.lean-lang.org/)". No other guidance.
- **Skills, commands, hooks, MCP:** none.
- **Permissions and safety:** none stated.
- **Human oversight:** none stated.
- **Notable ideas:**
  - A single, specific test target (`lake build VeilTest`) to run after every feature.
  - A directory map that tells agents which folders they can skip (`Examples/`), which saves context.
- **Lean-specificity:** medium. The file is small but names a Lean build target and Loogle; the rest is a generic directory map.
- **Evidence:** `agent_files/.claude/CLAUDE.md`.
