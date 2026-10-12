# leanprover/elan: agent setup

- **Snapshot:** commit `9605b24` (2026-10-10), from `repos/leanprover__elan/snapshot.json`.
- **Tools targeted:** Claude Code ("guidance to Claude Code (claude.ai/code)").
- **Files:** `CLAUDE.md`: an `/init`-style project overview (architecture, build commands, commit and changelog rules).
- **What agents are asked to do:** Rust development on the toolchain manager (forked from rustup); writing commits and changelog entries.
- **Build and verification:** `cargo build`, `cargo build --release`, cross-compilation with `cross build --release --target <TARGET>`, and `cargo test --release --target <TARGET>`. It notes there are "No unit tests (marked `test = false`)": CI's install test (`elan-init -y`, then create and build a Lake project) is the integration check.
- **Proof policy:** none stated (the repo has no Lean files).
- **Lean and Mathlib guidance:** explains how toolchains are resolved (`ELAN_TOOLCHAIN`, overrides, `lean-toolchain`, legacy `leanpkg.toml`, default), the toolchain naming pattern `[origin/][owner/repo:]release`, nightly vs stable channels, and the rustup→elan terminology map. No Lean coding guidance.
- **Skills, commands, hooks, MCP:** none.
- **Permissions and safety:** none stated.
- **Human oversight:** commit subject `<type>: <summary>`; don't add `(#PR)` yourself; reference fixed issues in the body; no hard-wrapping. "User-facing fixes and features must add a bullet to `CHANGELOG.md` in the same commit" under `# Unreleased`.
- **Notable ideas:** require a changelog entry in the same commit, with explicit exemptions (`chore:`, test-only changes); a rustup→elan terminology map to help agents read inherited code.
- **Lean-specificity:** low. This is Rust project documentation; the Lean content is only domain knowledge about toolchain resolution.
- **Evidence:** `agent_files/CLAUDE.md`, `snapshot.json`.
