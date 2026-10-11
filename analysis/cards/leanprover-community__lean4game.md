# leanprover-community/lean4game

- **Domain:** Game engine and web server for browser-based Lean proof games (hosts NNG4 and others at adam.math.hhu.de).
- **Primary role:** `interactive/teaching`
- **Secondary roles:** `DSL-host/metaprogramming`, `program`, `AI-oracle/referee` (Lean is the referee of player moves, no AI involved)
- **What the kernel checks:** Player solutions. `Runner` wraps the player's tactics into a `theorem the_theorem ... := by ...` and elaborates it; a level counts as completed only if there are no errors or warnings. The engine itself proves almost nothing (1 theorem in signals).
- **Certified vs only expressed:** Certified: each player's proof of the level statement. Only expressed: game structure (worlds, levels, inventory, hints, docs), which is metadata stored in environment extensions and exported as JSON.
- **Output artifact:** Interactive UI (TypeScript frontend, not checked out here) backed by a Lean server; JSON game data in `.lake/gamedata`.
- **Author mode:** Human (no AI markers in files read).
- **Translation direction:** Out of Lean: Lean command elaborators emit JSON game data and LSP diagnostics for a web client.
- **Creative idea:** Game authoring is done entirely in Lean commands (`World`, `Level`, `Statement`, `Hint`, `NewTactic`), and hints are attached to proof states that are matched against the player's goals up to renaming of hypotheses.
- **Why Lean?:** Not stated. My assessment: the engine depends on Lean 4's user-extensible elaborators, environment extensions and LSP/RPC server; it would need rewriting for Coq or Isabelle, and Python has no proof checker.
- **Notable techniques:**
  - ~40 custom `elab ... : command` forms for the game DSL (`server/GameServer/Commands.lean`).
  - `Hint` tactic stores the abstracted goal (`abstractCtx`, `abstractMVars`) and evaluates hint text with `evalExpr` via `implemented_by` (`server/GameServer/Tactic/Hint.lean`, `Hints.lean`, `AbstractCtx.lean`).
  - Syntax-tree walk that rejects tactics/theorems not yet unlocked (`findForbiddenTactics` in `server/GameServer/Runner.lean`).
  - `@[server_rpc_method]` handlers and custom "level completed" diagnostics (`server/GameServer/RpcHandlers.lean`).
- **Heuristic check:** the Phase 1 guess was `tool-around-Lean + game/teaching + DSL/metaprogramming + program + interactive`. Agree.
- **Evidence:** `README.md`, `server/lakefile.lean`, `server/GameServer/Commands.lean`, `Tactic/Hint.lean`, `Hints.lean`, `AbstractCtx.lean`, `Runner.lean`, `RpcHandlers.lean` (grep), `SaveData.lean`, `cypress/TestGame/Game/Levels/DemoWorld/L01_HelloWorld.lean`.
