# leanprover-community/repl

- **Domain:** Machine interface to the Lean elaborator: JSON over stdin/stdout for running commands, files and individual tactics.
- **Primary role:** `program`
- **Secondary roles:** `AI-oracle/referee`, `DSL-host/metaprogramming`
- **What the kernel checks:** Whatever the user submits is elaborated normally. In tactic mode, `getProofStatus` rebuilds the finished proof term and calls `addDecl` to kernel-check it, reporting "Completed"/"Incomplete"/"Error" (`REPL/Main.lean`). The repo's own code has no proofs.
- **Certified vs only expressed:** Nothing about the REPL is proven. It runs Lean and reports messages, sorries, goals and proof status.
- **Output artifact:** Executable `repl` emitting JSON responses (environment ids, proof-state ids, messages, info-tree data), plus pickled `.olean` snapshots.
- **Author mode:** Human (Scott/Kim Morrison headers).
- **Translation direction:** none (JSON in, JSON out around Lean source).
- **Creative idea:** It exposes Lean's `Command.State` and tactic `ProofSnapshot`s as numbered, backtrackable handles, so external programs (typically ML provers; the status check says it is "Inspired by LeanDojo REPL") can branch a proof search.
- **Why Lean?:** Not stated. Own assessment: it has to be Lean because it wraps Lean's own frontend, info trees and environments directly.
- **Notable techniques:**
  - Running commands with info trees enabled to recover tactics and `sorry` goals (`REPL/Frontend.lean`, `REPL/Lean/InfoTree.lean`).
  - Snapshotting and running `CoreM`/`MetaM`/`TacticM` inside a stored proof state (`REPL/Snapshots.lean`).
  - Pickling environments and proof states to `.olean`, and replaying constants through the private `lake_environment_add` FFI export. It skips kernel checking and documents that trust boundary (`REPL/Lean/Replay.lean`, `REPL/Util/Pickle.lean`).
  - Kernel re-check of completed tactic proofs via `addDecl` (`REPL/Main.lean`, `getProofStatus`).
- **Heuristic check:** The Phase 1 guess was `tool-around-Lean + DSL/metaprogramming + program`. I agree. It is a program built on Lean metaprogramming APIs, and its main users are AI provers.
- **Evidence:** `README.md`, `lakefile.toml`, `REPL/Frontend.lean`, `REPL/Snapshots.lean` (head), `REPL/Lean/Replay.lean` (head), `REPL/Main.lean` (signatures and `getProofStatus`).
