# <owner>/<repo>: agent setup

- **Snapshot:** commit `<short sha>` (<date>), from `repos/<owner>__<repo>/snapshot.json`.
- **Tools targeted:** which agents the files are written for (Claude Code, Codex/`AGENTS.md` readers, Copilot, Kiro, MCP clients, …).
- **Files:** the agent files, each with a few words on its role.
- **What agents are asked to do:** the kinds of work the setup expects (writing proofs, porting, refactoring, reviewing PRs, releases, CI triage, documentation…).
- **Build and verification:** how agents are told to build, test and check their work (exact commands where given).
- **Proof policy:** rules on `sorry`, `axiom`, `native_decide`, changing theorem statements, deleting or weakening results. Write "none stated" if absent.
- **Lean and Mathlib guidance:** toolchain, naming and style rules, Mathlib conventions, search tools (Loogle, `exact?`, LeanSearch…), performance advice.
- **Skills, commands, hooks, MCP:** each one with a one-line description. Write "none" if absent.
- **Permissions and safety:** allowed or forbidden tools, settings, things agents must never do.
- **Human oversight:** review process, who approves, what needs a human, how AI contributions are labeled.
- **Notable ideas:** 1–3 things other Lean projects could reuse.
- **Lean-specificity:** low / medium / high, meaning how much of the setup is specific to Lean rather than generic coding-agent advice, with one sentence of justification.
- **Evidence:** the files you actually read.
