# How ProofWidgets is implemented

ProofWidgets (`leanprover-community/ProofWidgets4`) lets Lean code put interactive web UIs in the editor's infoview, the side panel that shows proof goals. It has two halves: Lean code that describes the UI and runs logic on the Lean server, and TypeScript/React code running in the infoview, which is a webview. Lean core supplies the plumbing (user widgets, RPC); ProofWidgets adds typed components, an HTML type with JSX syntax, and the patterns that make it usable.

```
 Lean file / tactic                 Lean server                     Infoview (React, in the editor)
 ─────────────────                  ───────────                     ──────────────────────────────
 #html <b>hi</b>   ──elaborates──▶  Html value (inductive)
 conv?             ──saves──────▶   "widget info" on the syntax ──▶ cursor here? load module by hash
                                    JS modules stored by hash  ◀──── importWidgetModule(hash)
                                    @[server_rpc_method] fns   ◀──── RPC call with props / selections
                                    (MetaM, Expr, goals…)      ────▶ Html / JSON back → React render
                                                               ◀──── click → LSP edit to the .lean file
```

## 1. Components: typed wrappers around JavaScript modules

The base type, in `ProofWidgets/Component/Basic.lean`:

```lean
structure Component (Props : Type) extends Widget.Module where
  «export» : String := "default"
```

A `Widget.Module` (from Lean core) is essentially **a string of JavaScript**, identified by its hash. Tagging a definition `@[widget_module]` registers it in the environment, so the infoview can later fetch it by hash. The JS can be inline:

```lean
@[widget_module]
def InteractiveCode : Component InteractiveCodeProps where
  javascript := "
    import { InteractiveCode } from '@leanprover/infoview'
    import * as React from 'react'
    export default function(props) { return React.createElement(InteractiveCode, props) }"
```

or, more often, a compiled bundle pulled in at compile time:

```lean
def HtmlDisplay : Component HtmlDisplayProps where
  javascript := include_str ".." / ".." / "widget" / "js" / "htmlDisplay.js"
```

`Props` is a Lean structure deriving `RpcEncodable`, so it serializes to JSON for the React side. The docstring admits the type boundary isn't checked: "by defining a `Component Props`… you are *asserting* that `Props` is a correct representation of `JsProps`."

## 2. `Html`: an HTML tree as a Lean value

In `ProofWidgets/Data/Html.lean`:

```lean
inductive Html where
  | element   : String → Array (String × Json) → Array Html → Html   -- <tag attrs>children</tag>
  | text      : String → Html
  | component : UInt64 → String → LazyEncodable Json → Array Html → Html  -- hash, export, props, children
```

A component node stores the **hash of the component's JavaScript**, not the code, so the tree stays small and the infoview loads each module once.

**JSX syntax in Lean** uses the [syntax-categories technique](syntax-and-elaborators.md). ProofWidgets declares `proofWidgetsJsxElement`, `proofWidgetsJsxChild`, `proofWidgetsJsxAttr` and `proofWidgetsJsxAttrVal`, plus a custom text parser (`jsxText`, which forbids `{<>}$`). A macro (`transformTag`) turns them into `Html.element` / `Html.ofComponent` calls:

```lean
return <details «open»={true}>
    <summary className="mv2 pointer">Conv 🔍</summary>
    <div className="ml1">{inner}</div>
  </details>
```

A **delaborator** in the same file prints `Html` values back as JSX, so hovers show markup instead of nested constructors.

**The React side** (`widget/src/htmlDisplay.tsx`) walks the same tree as JSON:

```ts
export type Html =
    | { element: [string, [string, any][], Html[]] }
    | { text: string }
    | { component: [string, string, any, Html[]] }
...
} else if ('component' in html) {
    const [hash, export_, props, cs] = html.component
    const mod = await importWidgetModule(rs, pos, hash)   // fetch the JS module from the Lean server
    return React.createElement(mod[export_], {...props, pos}, children)
}
```

The tree is rendered "exactly as written down in Lean", resolving components by dynamically importing their modules from the server.

## 3. Showing something: attaching widgets to syntax

A widget appears when the cursor is on a piece of syntax that carries **widget info**. The `#html` command (`Component/HtmlDisplay.lean`):

```lean
syntax (name := htmlCmd) "#html " term : command

@[command_elab htmlCmd]
def elabHtmlCmd : CommandElab := fun
  | stx@`(#html $t:term) => do
    let ht ← (← liftTermElabM <| evalCommandMHtml <| ← ``(HtmlEval.eval $t))
    liftCoreM <| Widget.savePanelWidgetInfo
      (hash HtmlDisplayPanel.javascript)
      (return json% { html: $(← rpcEncode ht) })
      stx
```

- **The term can be a computation.** `#html` accepts a pure `Html` or a metaprogram returning one (e.g. `CommandElabM Html`). It evaluates the term at elaboration time with `evalTerm`, using the `unsafe` + `@[implemented_by]` trick (`evalCommandMHtmlUnsafe`).
- **Any tactic can attach a panel** by calling `savePanelWidgetInfo` with a component hash, props and a syntax range; that's how `conv?` works below.

## 4. Logic runs on the server: RPC and references

Functions marked `@[server_rpc_method]` run in the Lean server, with full access to `MetaM`, the environment and the goals:

```lean
@[server_rpc_method]
def ppExprTagged : InteractiveExprProps → Server.RequestM (Server.RequestTask Widget.CodeWithInfos)
  | ⟨ref⟩ => Server.RequestM.asTask <| ref.val.runMetaM Widget.ppExprTagged
```

The props hold a `Server.WithRpcRef ExprWithCtx`: a **reference** to a Lean object kept on the server, not a serialized copy. Expressions with their local context never cross into JavaScript; the browser holds handles and asks Lean to act on them. `InteractiveExpr` uses this to pretty-print lazily, only when an expression is actually shown.

**Writing components in Lean.** `mk_rpc_widget%` (`Component/OfRpcMethod.lean`) is an elaborator that turns an RPC method `Props → RequestM (RequestTask Html)` into a `Component Props`, so UI logic can live entirely in Lean. The docstring lists the limits: such components must be pure (no React state of their own), and can't pass closures, such as click handlers written in Lean, to children.

## 5. Closing the loop: select in the goal, edit the source

The `conv?` demo (`Demos/SelectInsertConv.lean`) combines all of this:

```lean
elab stx:"conv?" : tactic => do
  let some replaceRange := (← getFileMap).lspRangeOfStx? stx | return
  Widget.savePanelWidgetInfo ConvSelectionPanel.javascriptHash
    (pure $ json% { replaceRange: $(replaceRange) }) stx
```

1. The tactic records where `conv?` sits in the file and attaches a panel widget there.
2. In the goal display, the user shift-clicks a subterm; the infoview passes the selected locations to the panel's props.
3. `ConvSelectionPanel.rpc` runs on the server: it finds the goal, computes a path to the selected subterm in `MetaM` (`insertEnter`), and returns `Html` containing a `MakeEditLink` component.
4. `MakeEditLink` (`Component/MakeEditLink.lean`) carries an LSP `TextDocumentEdit`. Clicking it **rewrites the .lean file**, replacing `conv?` with `conv => enter [...]`.

A widget becomes a proof-authoring tool: the user points at the goal, Lean computes the right tactic, and the editor writes it into the source.

## 6. Expression presenters: delaborators that output HTML

`Presentation/Expr.lean` adds a custom attribute:

```lean
initialize exprPresenters : TagAttribute ← registerTagAttribute `expr_presenter
```

A function tagged `@[expr_presenter]` is "similar to a delaborator but outputs HTML trees instead of syntax." The server method `getExprPresentations` lists every presenter that applies to a selected expression, so the user can switch views, for example from a formula to a diagram (`Demos/ExprPresentation.lean`). Registration by attribute makes the set extensible from any library.

## 7. Building: Lake drives npm

`lakefile.lean` declares the TypeScript sources (`widget/src/*.tsx`), `package.json`, `rollup.config.js` and `tsconfig.json` as build inputs, runs `npm install` and rollup when they change, and writes bundles to `widget/js/`. The Lean files `include_str` those bundles, so editing a `.tsx` file triggers a Lean rebuild of the components that embed it. The demos show the range this enables: Penrose diagrams, Graphviz, force-directed graphs, Recharts plots, an interactive SVG, a Rubik's cube, red-black trees and Venn diagrams.

## Lean features it exercises

| Feature (from [`FEATURES.md`](../FEATURES.md)) | Where it shows up |
|---|---|
| Syntax categories + macros (1, 2) | The JSX syntax for `Html` |
| Delaborators (3) | `Html` printed back as JSX |
| Custom attributes (4) | `@[widget_module]`, `@[server_rpc_method]`, `@[expr_presenter]` |
| `@[implemented_by]` + `unsafe` (10) | Evaluating `#html` terms at elaboration time |
| Widgets and server RPC (16) | Server references (`WithRpcRef`), lazy pretty-printing, `mk_rpc_widget%` |
| Frontend / language-server integration (17) | Selections in the goal display, LSP edits to the file |
| Lake extensibility (20) | npm and rollup driven from the lakefile |

**The design in one line:** Lean owns the meaning (types, goals, expressions, edits), JavaScript only renders, and the two talk through typed props, server-side references and RPC.
