# momonpya/eggshell

- **Domain:** Local, cross-chat memory for AI coding agents (Codex plugin, plus adapters for Claude Code, Gemini CLI and others): an evidence graph with retrieval and handoff.
- **Primary role:** `program`
- **Secondary roles:** `certifier-software`
- **What the kernel checks:** Full proofs about the production functions themselves (1167 theorems, 0 sorry). Examples: `select` returns unique, ranked, existing ids within budget (`Eggshell/SearchRank.lean`). The BLAKE3 known-answer vectors use `native_decide` (`Eggshell/Blake3.lean`), so they trust the compiler.
- **Certified vs only expressed:** Proven: selection, cache-identity, append/recovery-preserves-bytes and handoff-delivery contracts, listed in `docs/lean-boundaries.md`. Only run: embedding inference (Python/FastEmbed), file I/O and locking, and process and hook delivery. The docs state that token savings and retrieval quality are measured, not proven.
- **Output artifact:** Executables (`eggshell`, packager, test runners) and an append-only `.egg` page database.
- **Author mode:** Not determinable. Commits show a single author "Momo". There is no AGENTS.md or CLAUDE.md, and I saw no evidence either way.
- **Translation direction:** none.
- **Creative idea:** Proofs are attached directly to the executed functions of an AI-agent memory product. Build-time `run_meta` audits then check axioms and that production callers really route through the proven functions.
- **Why Lean?:** Partly stated: the engine, adapters, setup logic and package builder are written in Lean so that contracts sit on the code that runs, with Python limited to numerics (`docs/lean-boundaries.md`). Own assessment: Dafny could prove similar contracts, but Lean gives one language for proofs, the CLI and build-time meta-audits.
- **Notable techniques:**
  - Contracts on the executable definition itself, e.g. `selected_within_budget` and `selected_was_ranked` (`Eggshell/SearchRank.lean`).
  - `run_meta` audit using `collectAxioms` plus `getUsedConstants` checks that callers use the canonical, proven readers and do not bypass them (`Eggshell/ContractAudit.lean`).
  - `native_decide` known-answer tests pinning a Lean BLAKE3 implementation (`Eggshell/Blake3.lean`).
  - A C `extern_lib` for storage sync, and the Python embedding source tracked as a build input (`lakefile.lean`).
- **Heuristic check:** The Phase 1 guess was `spec+proof + program`. I mostly agree. I would order it as program first with certified components; the proofs serve the product rather than being the goal.
- **Evidence:** `README.md`, `lakefile.lean`, `docs/lean-boundaries.md`, `Eggshell/SearchRank.lean` (lines 1–235, grep), `Eggshell/ContractAudit.lean` (head), `Eggshell/Blake3.lean` (lines 218–232), `git log` (5 commits).
