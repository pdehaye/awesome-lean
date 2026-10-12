# justincasher/lean-explore: agent setup

- **Snapshot:** commit `17b9d6c` (2026-09-28), from `repos/justincasher__lean-explore/snapshot.json`.
- **Tools targeted:** MCP clients, packaged as a plugin. `tree.txt` also lists `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`, and `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` under `plugins/lean-explore/`, so the plugin targets Claude Code and Codex. Those manifests weren't captured.
- **Files:** `plugins/lean-explore/.mcp.json`: declares one HTTP MCP server.
- **What agents are asked to do:** none stated. The repo provides a tool for other projects' agents to use, not instructions for agents working in this repo.
- **Build and verification:** none stated.
- **Proof policy:** none stated.
- **Lean and Mathlib guidance:** none stated in the captured file. The server is LeanExplore, a search service for Lean declarations.
- **Skills, commands, hooks, MCP:** MCP server `lean-explore`, `"type": "http"`, `"url": "https://www.leanexplore.com/mcp"` (a hosted server, so nothing is installed locally). No skills, commands or hooks.
- **Permissions and safety:** none stated.
- **Human oversight:** none stated.
- **Notable ideas:**
  - Ship a Lean search engine as an installable agent plugin, through a hosted MCP endpoint, for both the Claude and Codex plugin marketplaces.
- **Lean-specificity:** medium. The setup is a single generic MCP declaration, but the service it points to exists only to search Lean libraries.
- **Evidence:** `agent_files/plugins/lean-explore/.mcp.json`; `tree.txt` for the plugin manifests.
