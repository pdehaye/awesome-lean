# Feature deep dives

Close readings of how specific Lean language features are used, with code quoted from the repositories. They follow up on the [feature shortlist](../FEATURES.md).

| Deep dive | Shortlist features | What it shows |
|---|---|---|
| [Syntax categories and elaborators](syntax-and-elaborators.md) | 1, 2 | Eight strategies for embedding other languages in Lean: LAMR, Alloy, Velvet, Veil, Verso, Strata, lean4game, Loogle |
| [ProofWidgets](proofwidgets.md) | 1–4, 10, 16, 17, 20 | Interactive UIs in the infoview: typed JavaScript components, an `Html` type with JSX syntax, server-side RPC, widgets that edit the proof script |
| [Verso](verso.md) | 1, 2, 4, 17, 20 | Documents as Lean values: genres, a `#doc` command that replaces Lean's command parser, extensions by attribute, code blocks elaborated for real |
| [REPL](repl.md) | 9, 11, 12, 17 | Lean as a JSON service for AI provers: numbered elaborator snapshots, `sorry` as entry points, pickling and its trust model |
