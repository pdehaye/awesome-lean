# leanprover/verso

- **Domain:** Authoring framework for documents about Lean: manuals (the Lean reference), books, blogs/websites, literate programs, docstrings.
- **Primary role:** `DSL-host/metaprogramming`
- **Secondary roles:** `program`, `interactive/teaching`
- **What the kernel checks:** for the framework, mostly nothing (a few small lemmas, e.g. `OrderedListType.all_complete` in `src/verso/Verso/Parser.lean`, Z85 size lemmas in `src/verso-util/VersoUtil/BinFiles/Z85.lean`). In documents, embedded ```` ```lean ```` blocks are elaborated as real Lean commands, so example code must typecheck and expected outputs are compared.
- **Certified vs only expressed:** proven: a few utility lemmas. Checked by elaboration: code samples inside documents. Everything else (document structure, rendering, cross-references) is just expressed and run.
- **Output artifact:** documents (HTML sites, TeX), executables (`verso`, `verso-serve`, `verso-literate`, test runner `errata-run-one`).
- **Author mode:** mainly human (David Thrane Christiansen in headers); the one checked-out commit has a `Co-authored-by: Claude` trailer, so recent work is at least partly mixed.
- **Translation direction:** out of Lean (document values to HTML/TeX).
- **Creative idea:** A document is a Lean term: a Markdown-like syntax is parsed inside a `#doc (Genre) "Title" =>` command and elaborated to a value of type `VersoDoc genre`, with "genres" packaging their own block/inline types and traversal state.
- **Why Lean?:** partly stated: documents "can make full use of the Lean metaprogramming API" and code samples are checked so text does not go stale (`README.md`, `doc/UsersGuide/Basic.lean`). Own assessment: a Scribble-style approach in Racket could host the markup, but would not elaborate Lean examples against the live environment.
- **Notable techniques:**
  - Custom `Parser`s for whole-document syntax and `#doc`/`#docs` elaborators (`src/verso/Verso/Doc/Concrete.lean`).
  - `Genre` structure with type-valued fields (`src/verso/Verso/Doc.lean`).
  - `@[code_block]`, `@[role]`, `@[directive_expander]` extension attributes, e.g. `lean` blocks that elaborate commands and highlight via SubVerso (`src/verso-manual/VersoManual/InlineLean.lean`).
  - In-house test framework using Plausible properties (`src/errata/Errata/Property.lean`).
- **Heuristic check:** the Phase 1 guess was `DSL/metaprogramming + program + computation/examples + interactive`. Agree; DSL hosting is clearly primary.
- **Evidence:** `README.md`, `lakefile.lean` (grep), `src/verso/Verso/Doc.lean` (Genre), `src/verso/Verso/Doc/Concrete.lean` (grep), `src/verso-manual/VersoManual/InlineLean.lean` (parts), `doc/UsersGuide/Basic.lean`, `src/errata/Errata.lean`, `src/errata/Errata/Property.lean`.
