# nomeata/loogle: agent setup

- **Snapshot:** commit `9f11169` (2026-07-09), from `repos/nomeata__loogle/snapshot.json`.
- **Tools targeted:** Claude Code (a custom slash command).
- **Files:** `.claude/commands/bump-js-deps.md`: a maintenance command for the web frontend.
- **What agents are asked to do:** update the CDN-hosted JS/CSS library versions embedded in `server.py`'s HTML.
- **Build and verification:** no build or test step. The integrity check is to recompute SRI `sha384-…` hashes with a given `curl | python3 hashlib` one-liner, and to keep esm.sh `modulepreload` hrefs and `import` statements consistent.
- **Proof policy:** none stated.
- **Lean and Mathlib guidance:** none.
- **Skills, commands, hooks, MCP:** `/bump-js-deps`: find CDN URLs, check the latest npm versions, update URLs and SRI hashes, report, commit.
- **Permissions and safety:** "Commit the changes (but do not push)."
- **Human oversight:** a human pushes. The agent reports "what was updated and what was already at the latest version".
- **Notable ideas:** narrow, repeatable chores written as commands with a commit-but-don't-push boundary; computing SRI hashes in a reproducible way.
- **Lean-specificity:** low. The only agent file is about web dependency hygiene, not the Lean search engine itself.
- **Evidence:** `agent_files/.claude/commands/bump-js-deps.md`, `snapshot.json`.
