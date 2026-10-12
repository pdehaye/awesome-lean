# leanprover/lean-eval: agent setup

- **Snapshot:** commit `38361be` (2026-10-07), from `repos/leanprover__lean-eval/snapshot.json`.
- **Tools targeted:** `AGENTS.md` readers (Codex and others).
- **Files:** `AGENTS.md`: three bullet points under "Agent Notes".
- **What agents are asked to do:** edit and add Lean files. The file doesn't name the kind of work.
- **Build and verification:** "run an appropriate build/check and clean up warning output, not just errors". No exact command is given.
- **Proof policy:** none stated.
- **Lean and Mathlib guidance:** only the linter rule: "Do not leave linter warnings behind in edited files"; warnings are "follow-up work to fix before considering a task complete".
- **Skills, commands, hooks, MCP:** none.
- **Permissions and safety:** none stated.
- **Human oversight:** none stated.
- **Notable ideas:** define "done" as free of warnings, not just free of errors. This catches Lean linter output (and `sorry` warnings), which agents tend to ignore.
- **Lean-specificity:** low. The rule mentions Lean files but is generic hygiene advice.
- **Evidence:** `agent_files/AGENTS.md`, `snapshot.json`.
