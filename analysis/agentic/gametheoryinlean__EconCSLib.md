# gametheoryinlean/EconCSLib: agent setup

- **Snapshot:** commit `b1cd89a` (2026-10-11), from `repos/gametheoryinlean__EconCSLib/snapshot.json`.
- **Tools targeted:** `AGENTS.md` readers; no tool-specific files.
- **Files:** `AGENTS.md`, an agent guide with a quick start, repository map, architecture, policies, verification commands and CI overview.
- **What agents are asked to do:** Lean library changes; knowledge-blueprint nodes written in Markdown; API-doc tooling.
- **Build and verification:** start with `git status --short --branch`. Lean: `lake exe cache get`, `lake build`, `lake build EconCSLib.Examples`, `python3 scripts/check_lean_placeholders.py EconCSLib EconCSLib.lean`. Knowledge base: a unittest, `check_knowledge_references.py`, `mdblueprint-check docs/knowledge --lean-root .`. All changes: `git diff --check`.
- **Proof policy:** no ordinary `sorry`, `admit` or `sorryAx` in production code. The exception is `EconCSLib/OpenProblem/`, where `answer(sorry)` and `:= by sorry` are allowed in the same declaration. Do not add "a deferred Lean theorem declaration merely to reserve an API"; record it as a blueprint node or issue. Do not claim a blueprint gap is proved because its prose statement exists. Nothing on axioms.
- **Lean and Mathlib guidance:** search Mathlib before adding abstractions. Prefer targeted imports over `import Mathlib`. Keep `Math/` independent of domain modules. Keep structures lean, adding finiteness or decidability assumptions only where needed. Use Mathlib naming. Write module docstrings and cite sources with labels like `[MSZ 2.18]`. Examples and OpenProblem must not be imported by `EconCSLib.lean`.
- **Skills, commands, hooks, MCP:** none.
- **Permissions and safety:** "Do not discard existing worktree changes"; no destructive Git commands unless the task needs them. Do not commit textbook PDFs, OCR content or generated sites.
- **Human oversight:** none stated beyond staged blueprint nodes that are "reviewable" before promotion. No policy on AI attribution.
- **Notable ideas:** a quarantined `OpenProblem/` folder with a placeholder checker script; a knowledge blueprint linked to Lean declarations, with separate `## References` and `## Provenance` sections; verification commands grouped by type of change.
- **Lean-specificity:** medium: the placeholder policy, import discipline and Mathlib guidance are Lean-specific, but much of the file covers the Markdown blueprint and generic Git safety.
- **Evidence:** `AGENTS.md`.
