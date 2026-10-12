# momonpya/eggshell: agent setup

- **Snapshot:** commit `5187316` (2026-10-10), from `repos/momonpya__eggshell/snapshot.json`.
- **Tools targeted:** Codex. The skill ships inside a Codex plugin (`plugins/eggshell/.codex-plugin/`, `hooks/hooks.json`); it says ordinary ChatGPT Chat cannot run it.
- **Files:** `plugins/eggshell/skills/eggshell/SKILL.md`, a skill for agents *using* the product: installing, inspecting and troubleshooting Eggshell, a local cross-chat memory for Codex. Nothing configures agents working on the repository itself (no `AGENTS.md`/`CLAUDE.md`). The tree shows the tool is written in Lean (`Eggshell/PluginHooks.lean`, `lakefile.lean`), but the skill never mentions Lean.
- **What agents are asked to do:** set up the plugin, migrate older installs, verify hooks, run memory controls (`!egg doctor`, `!egg graph`, `!egg keep`, `!egg off`…), diagnose missing context.
- **Build and verification:** check first with `sh <plugin-root>/scripts/setup.sh --check --project <path>`, install with the same script without `--check`. Verification means a real two-chat test: "Installation alone does not prove that a handoff was received."
- **Proof policy:** none stated.
- **Lean and Mathlib guidance:** none stated.
- **Skills, commands, hooks, MCP:** one skill (`eggshell`); the plugin's automatic Codex hooks record and retrieve memory; `!egg` shell controls. No MCP.
- **Permissions and safety:** setup downloads a runtime, Python packages and MiniLM only "once setup is authorized". "A checksum mismatch must stop setup; do not bypass verification." Never bypass `/hooks` trust checks; remove only `eggshell@eggshell`, "not unrelated plugins"; do not publish work-file contents without authorization; inspecting memory must not change settings.
- **Human oversight:** the user reviews and enables hooks through `/hooks`. No contribution policy.
- **Notable ideas:** a read-only `--check` mode before any install; treat recalled outcomes as evidence and "distinguish reused findings from new checks and explicitly unverified facts".
- **Lean-specificity:** low: the only agent file is an operations guide for a memory plugin; Lean is just the implementation language.
- **Evidence:** `plugins/eggshell/skills/eggshell/SKILL.md`; `tree.txt` for context.
