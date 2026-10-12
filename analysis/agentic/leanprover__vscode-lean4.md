# leanprover/vscode-lean4: agent setup

- **Snapshot:** commit `dead846` (2026-09-30), from `repos/leanprover__vscode-lean4/snapshot.json`.
- **Tools targeted:** Claude Code.
- **Files:** `.claude/CLAUDE.md`: commands and an architecture overview of the npm-workspaces/Nx monorepo.
- **What agents are asked to do:** TypeScript work on the VS Code extension, infoview, and Unicode input packages.
- **Build and verification:** `npm install`, `npm run build`, `npm run lint`, `npm run watch`, and `npm run package` for a `.vsix`. Tests (`npm run test`, with `LEAN4_TEST_FOLDER` to select a suite) need the nightly, stable and default toolchains installed through elan, but "Tests should not be run locally, only in CI".
- **Proof policy:** none stated.
- **Lean and Mathlib guidance:** none for writing Lean code. Points to the LSP 3.17 spec and to Lean's `src/Lean/Server/ProtocolOverview.lean` as the reference for the language server protocol, and explains the `LeanClient`-per-project and `lake serve` design.
- **Skills, commands, hooks, MCP:** none.
- **Permissions and safety:** only the "don't run tests locally" rule.
- **Human oversight:** none stated.
- **Notable ideas:** link agents to authoritative API references (VS Code API, manifest fields, `when` clauses, the Lean server protocol file) so they don't guess; say plainly where tests should run.
- **Lean-specificity:** low. It is generic monorepo/extension guidance, apart from the pointers to the Lean server protocol and elan toolchains.
- **Evidence:** `agent_files/.claude/CLAUDE.md`, `snapshot.json`.
