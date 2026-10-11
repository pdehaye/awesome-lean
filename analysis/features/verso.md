# How Verso is implemented

Verso (`leanprover/verso`) is Lean's documentation authoring system: books, manuals, blogs and websites written *in Lean files*. Its central idea is that a document is a Lean value, built by Lean's own elaborator, so code examples are elaborated for real and documents can be extended with ordinary Lean code. The official books (Theorem Proving in Lean 4, Functional Programming in Lean), the Lean reference manual, and projects such as FLT, Tao's Analysis I and Tau Ceti use it.

```
 .lean file                          elaboration (Lean compiler)               output program
 ──────────                          ───────────────────────────               ──────────────
 #doc (Manual) "Title" =>      ──▶   command parser swapped for Verso's   ──▶  Part Manual (a Lean value)
 Markdown-like text                  block parser; blocks → Doc AST            genre's main: traverse,
 ```lean … ``` code blocks     ──▶   code elaborated + highlighted (SubVerso)   resolve cross-refs,
 {role}`…`, :::directive       ──▶   expanders found by attribute               emit HTML / TeX
```

## 1. Genres: one framework, many kinds of document

Every document is written in a **genre** (`src/verso/Verso/Doc.lean`):

```lean
public structure Genre : Type 1 where
  PartMetadata : Type      -- metadata per section (author, date, cross-reference id…)
  Block : Type             -- extra block-level elements the genre adds
  Inline : Type            -- extra inline elements the genre adds
  TraverseContext : Type   -- read-only data for the traversal pass
  TraverseState : Type     -- mutable state for the traversal pass
```

The core document types are parameterized by the genre. `Manual`, `Blog`, `Tutorial` and the literate-programming genres each fill in these types, and each provides a `main` function that traverses the document and generates output. A genre with no extensions is `Genre.none := ⟨Empty, Empty, Empty, Unit, Unit⟩`.

**The document model lives in Lean core.** Verso's inline type is an alias for core's:

```lean
public abbrev Inline (genre : Genre) :=
  Lean.Doc.Inline genre.Inline
```

and `#doc` opens `Lean.Doc.Syntax`. The document AST and its syntax are thus shared with Lean itself. The docstrings in Verso's own sources are written in Verso markup (`{name}`…``, `{lean}`…``), which shows the two meeting.

## 2. Two ways to write a document

**As a term.** `#doc (Genre) "Title" => …` can be a term whose value is the whole document (`Verso/Doc/Concrete.lean`):

```lean
elab "#doc" "(" genre:term ")" title:str "=>" text:completeDocument eoi : term => do
  findGenreTm genre
  let endPos := (← getFileMap).source.rawEndPos
  let doc ← elabDoc genre title text.raw.getArgs endPos
  Term.elabTerm (← `( ($(doc) : VersoDoc $genre))) none
```

**As a command that takes over the rest of the file.** This is the most unusual trick. The command form of `#doc` **replaces Lean's command parser** with a Verso block parser, so everything after it in the file is read as document text, one top-level block at a time:

```lean
elab_rules : command
  | `(command|#doc ( $genreSyntax:term ) $title:str =>%$tok) => ... do
  elabCommand <| ← `(open scoped Lean.Doc.Syntax)
  startDoc genreSyntax title
  -- Sets up basic incremental evaluation of documents by replacing Lean's command-by-command parser
  -- with a top-level-block parser.
  modifyEnv fun env => originalCatParserExt.setState env (categoryParserFnExtension.getState env)
  replaceCategoryParser `command versoBlockCommandFn
```

`replaceCategoryParser` edits `categoryParserFnExtension`, the environment extension where Lean stores the parser for each syntax category. Since each block is now a "command", Lean's normal incremental processing applies: editing one paragraph re-elaborates only from there on, as with code. One complication is handled explicitly: Lean's command parser skips comments, but in a document `--` may be ordinary text, so Verso tracks the last parsed position itself (`lastVersoEndPosExt`).

## 3. Extensions by attribute

Documents can contain roles (`{lean}`fib``), directives (`:::fragment`), custom code blocks and more. Each kind has its own attribute, all created with `mkDocExpanderAttribute` (`Verso/Doc/Elab/Monad.lean`):

| Attribute | What it implements |
|---|---|
| `inline_expander` | Inline elements of a given name |
| `block_expander` | Block elements of a given name |
| `role_expander` | Roles such as `{lean}`…`` |
| `code_block_expander` | Fenced code blocks such as ```` ```lean ```` |
| `directive_expander` | `:::` directives |
| `part_command` | Side effects on the document's structure |
| `block_command_expander` | Block-level commands |

An extension is just a Lean function tagged with the right attribute, for example `@[code_block_expander module]` and `@[role_expander anchor]` in `Verso/Code/External.lean`, which display code taken from other files. Any library can add new document features without touching Verso.

## 4. Code blocks are elaborated for real

The `lean` code block of the Manual genre (`verso-manual/VersoManual/InlineLean.lean`) runs the code through Lean's frontend in the document's own environment:

```lean
meta def lean : CodeBlockExpanderOf LeanBlockConfig
  | config, str => elabCommands config str toHighlightedLeanBlock
```

`elabCommands` does the following:
- It turns off asynchronous elaboration, "so that info trees and messages are available when highlighting syntax".
- It elaborates declarations as public, so that later code blocks can refer to them.
- It loops `Parser.parseCommand` then `Command.elabCommandTopLevel` over the block's text, collecting info trees per command.
- It highlights the result with SubVerso (`Highlighted`), carrying the hovers and types from those info trees into the output.

So a book's examples are checked by the build: if a Lean update breaks an example, the book stops compiling. Each code block is also registered as a "point of interest" for the editor's outline view.

## 5. From document value to output

`#doc` produces a `VersoDoc genre`, described as "a not-fully-evaluated document" that becomes a `Part` through `VersoDoc.toPart`. Document-wide data is gathered in `DocReconstruction`: highlighted code deduplicated in a shared table (`highlightDeduplication`), link targets and footnotes, looked up when blocks are built.

Output is produced by an ordinary Lean program. Each document is compiled into an executable: the lakefile declares `lean_exe usersguide`, `lean_exe demosite` and others, and a genre's `main` (e.g. `manualMain` in `VersoManual.lean`) traverses the document, resolves cross-references and writes HTML or TeX. HTML and TeX are themselves written with embedded syntax: `Verso/Output/Html.lean` and `Verso/Output/TeX.lean` declare syntax categories (`html`, `attrib`, `tex`, …) so output templates can be written as markup inside Lean.

The repository also ships search (`verso-search`), a local server (`verso-serve`), literate-programming tools (`verso-literate`), and `VersoBlueprint`, which FLT uses for its project blueprint.

## Lean features it exercises

| Feature (from [`FEATURES.md`](../FEATURES.md)) | Where it shows up |
|---|---|
| Syntax categories + elaborators (1, 2) | The document grammar; `#doc` as a term and as a command; HTML/TeX syntax |
| Custom attributes + environment extensions (4) | The seven expander attributes; `lastVersoEndPosExt` |
| Replacing a category's parser | `#doc` swaps the `command` parser via `categoryParserFnExtension` |
| Frontend / InfoTree APIs (17) | Code blocks parsed and elaborated with Lean's frontend; info trees used for highlighting |
| Lake extensibility (20) | One executable per document; search and server tools |

**The design in one line:** a document is a Lean program, so it gets Lean's type checking, incremental elaboration, editor support and extensibility, and its code examples cannot silently go stale.

## See also

- [Syntax categories and elaborators](syntax-and-elaborators.md): Verso is strategy 5 there.
- [The Verso card](../cards/leanprover__verso.md) from Phase 2.
