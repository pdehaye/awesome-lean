# How the Lean REPL is implemented

The REPL (`leanprover-community/repl`) turns Lean into a service that other programs drive through JSON on stdin and stdout. It is the main bridge between Lean and AI provers: a prover sends Lean code or a tactic, gets back messages and goals, and can go back to any earlier state to try something else. The whole tool is about 1,500 lines of Lean, because it reuses Lean's own frontend instead of reimplementing anything.

```
 external program (e.g. an AI prover)              REPL process (Lean)
 ────────────────────────────────────              ───────────────────
 {"cmd": "def f := 2"}                  ───────▶   parse + elaborate with Lean's frontend
                                        ◀───────   {"env": 0, "messages": [...], "sorries": [...]}
 {"cmd": "example : f = 2 := by sorry", "env": 0}  run in snapshot 0, find the sorry
                                        ◀───────   {"env": 1, "sorries": [{"proofState": 0, "goal": "⊢ f = 2"}]}
 {"tactic": "rfl", "proofState": 0}     ───────▶   run the tactic in proof snapshot 0
                                        ◀───────   {"proofState": 1, "goals": []}
 {"tactic": "simp", "proofState": 0}    ───────▶   same starting point: a different branch
```

## 1. The protocol: numbered snapshots you can return to

Two kinds of requests (`README.md`):

- **Command mode:** `{"cmd": "...", "env": n}` runs complete commands (declarations) in environment `n`, or in a fresh environment if `env` is omitted.
- **Tactic mode:** `{"tactic": "...", "proofState": n}` runs one tactic in proof state `n`.

Every response returns a new number. Because old numbers stay valid, **backtracking is free**: "You can backtrack simply by using earlier values for `env`." A prover can explore a search tree by branching from any earlier state, which is exactly what tree-search provers need.

The server keeps these snapshots in its state (`REPL/Main.lean`):

```lean
structure State where
  /-- Environment snapshots after complete declarations. -/
  cmdStates : Array CommandSnapshot := #[]
  /-- Proof states after individual tactics. -/
  proofStates : Array ProofSnapshot := #[]
```

## 2. Reusing Lean's frontend

The REPL doesn't parse or elaborate anything itself. `REPL/Frontend.lean` wraps Lean's own `IO.processCommands`, turning on info trees (the data structure the editor uses for hovers and goals):

```lean
def processCommandsWithInfoTrees
    (inputCtx : Parser.InputContext) (parserState : Parser.ModuleParserState)
    (commandState : Command.State) : IO (Command.State × List Message × List InfoTree) := do
  let commandState := { commandState with infoState.enabled := true }
  let s ← IO.processCommands inputCtx parserState commandState <&> Frontend.State.commandState
  pure (s, s.messages.toList, s.infoState.trees.toList)
```

For a fresh environment, `processInput` first parses and processes the `import` header, then the rest of the input. For an existing environment, it continues from the saved `Command.State`. Running a command in environment `n` just means resuming Lean's frontend from snapshot `n`.

## 3. Snapshots: freezing the elaborator's state

A **proof state** is a bundle of the states of all the monads involved in elaborating a tactic proof (`REPL/Snapshots.lean`):

```lean
structure ProofSnapshot where
  ...
  termState     : Term.State
  termContext   : Term.Context
  tacticState   : Tactic.State
  tacticContext : Tactic.Context
  rootGoals     : List MVarId
```

Running a tactic means parsing a string and evaluating it inside that frozen state, which yields a new snapshot:

```lean
def runString (p : ProofSnapshot) (t : String) : IO ProofSnapshot := ...
def runSyntax (p : ProofSnapshot) (t : Syntax) : IO ProofSnapshot :=
  Prod.snd <$> p.runTacticM (evalTactic t)
```

Lean's state is purely functional, so an old snapshot is never modified, and returning to it is just reusing a value.

## 4. Finding entry points: `sorry` as a hole to fill

Tactic mode starts from a `sorry`. After running a command, the REPL searches the info trees for `sorry` nodes (`REPL/Lean/InfoTree.lean`):

```lean
def sorries (t : InfoTree) : List (ContextInfo × SorryType × Position × Position) :=
  (t.findSorryTacticNodes.map fun ⟨i, ctx⟩ =>
    ({ ctx with mctx := i.mctxBefore, ... }, .tactic i.goalsBefore.head!, stxRange ctx.fileMap i.stx)) ++
  (t.findSorryTermNodes.map fun ⟨i, ctx⟩ =>
    (ctx, .term i.lctx i.expectedType?, stxRange ctx.fileMap i.stx))
```

Each `sorry`, in tactic or term position, becomes a numbered `ProofSnapshot` with its goal. The same info trees also feed `allTactics` mode, which reports every tactic in a file with the goals before it, a common way to extract training data.

This is the [Phase 3 pattern](../SYNTHESIS.md) "statements as the deliverable" in machine form: a `sorry` marks a precise hole, and the REPL hands it to whoever can fill it.

## 5. Pickling: saving states to disk

Environments and proof states can be written to `.olean` files and loaded in another session, possibly on another machine (`REPL/Util/Pickle.lean`):

```lean
/-- By abusing `saveModuleData` and `readModuleData` we can pickle and unpickle objects to disk. -/
def pickle {α : Type} (path : FilePath) (x : α) (key : Name := by exact decl_name%) : IO Unit :=
  saveModuleData path key (unsafe unsafeCast x)
```

This reuses the machinery Lean uses for compiled modules, via `unsafeCast`, and loads data into a compacted memory region that has to be freed by hand.

Restoring an environment needs constants put back without re-checking them. `REPL/Lean/Replay.lean` uses a private Lean export from Lake (`lake_environment_add`) and states its trust model explicitly:

> `replayToElabEnv` bypasses kernel type-checking. The REPL produces and consumes its own pickles, so the constants being replayed have already been checked by the kernel once. **Pickles are trusted artifacts; this is not a verifier boundary.** A malicious or corrupt `.olean` could install unchecked constants directly into the environment.

That's why judging untrusted AI submissions is left to a separate tool, [Comparator](../cards/leanprover__comparator.md), which sandboxes builds and replays proofs in the kernel.

## Lean features it exercises

| Feature (from [`FEATURES.md`](../FEATURES.md)) | Where it shows up |
|---|---|
| Frontend / InfoTree APIs (17) | `IO.processCommands`, info trees for sorries, goals and tactics |
| Monads and their states (12) | `ProofSnapshot` bundles `Term`, `Tactic`, `Meta` and `Core` states |
| `unsafe` code (11) | Pickling via `unsafeCast`, `unpickle` |
| Trust boundaries (9) | Replay bypasses the kernel, with the trust model documented |

**The design in one line:** Lean's elaborator state is an immutable value, so the REPL just numbers these values and lets clients resume from any of them, which turns proof search into ordinary tree search.

## Limits stated in the repo

- Tactic mode is labeled experimental, and a completed proof state can't yet be written back into the original command to produce a new environment.
- Restoring a pickled environment restores constants but not environment-extension entries, so scoped notations and attributes may be missing.
- Replay depends on a private, unstable Lean export, which may break with future Lean releases.
