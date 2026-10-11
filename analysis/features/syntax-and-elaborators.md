# Syntax categories and elaborators: how other languages get embedded in Lean

Features 1 and 2 of the [shortlist](../FEATURES.md). Code excerpts are quoted from the repositories, with the file paths given.

## The core idea

Lean's parser can be extended from inside Lean itself. New grammar rules are ordinary declarations: they live in a library, are imported like functions, and take effect in the files that import them. Three tools work together:

| Tool | What it does | What it can see |
|---|---|---|
| `declare_syntax_cat` + `syntax` | Adds a new grammar category with its own rules, precedences and tokens | Only text |
| `macro` / `macro_rules` | Rewrites new syntax into existing syntax | Only syntax: no types, no environment |
| `elab` / `elab_rules` | Turns syntax directly into Lean terms or declarations, as a program running inside the compiler | Types, the whole environment, error reporting; can generate declarations and side artifacts |

The repositories combine these in different ways. Below are eight strategies, from the lightest to the most radical.

## 1. A notation for data (LAMR): macros building a data structure

LAMR (Avigad's *Logic and Mechanized Reasoning*) gives propositional formulas their own grammar, then uses macros to turn them into an ordinary Lean data type (`avigad/lamr`, `LAMR/Util/Propositional/Syntax.lean`):

```lean
declare_syntax_cat propform
syntax "prop!{" propform "}"  : term          -- entry point from Lean
syntax:35 propform:36 " ∧ " propform:35 : propform
syntax:20 propform:21 " → " propform:20 : propform
syntax:max "¬ " propform:40             : propform

macro_rules
  | `(prop!{$p ∧ $q})  => `(PropForm.conj prop!{$p} prop!{$q})
  | `(prop!{$p → $q})  => `(PropForm.impl prop!{$p} prop!{$q})
```

Used as: `#eval prop!{(p1 ∧ p2) ∨ (q1 ∧ q2)}.toCnfForm.toString`.

This is a **deep embedding**: the formula becomes a value of type `PropForm` that Lean code can inspect, normalize to CNF, or print in DIMACS for a SAT solver.

**Weakness of macros:** they aren't checked by types until someone uses them. The same file contains

```lean
  | `(prop!{⊤})        => `(ProfForm.tr)    -- typo: should be PropForm.tr
```

which goes unnoticed because nothing in the repo writes `prop!{⊤}`. An elaborator would have caught it at once.

## 2. A whole foreign grammar (Alloy): C inside Lean files

Alloy declares the full C grammar as Lean syntax categories (`cExpr`, `cTypeSpec`, `cDirectDeclarator`, …; about 200 rules in `Alloy/C/Grammar.lean`). Usage (`examples/my_add/MyAdd.lean`):

```lean
alloy c include <lean/lean.h>

alloy c extern def myAdd (x y : UInt32) : UInt32 := {
  return x + y;
}
```

The elaborator (`Alloy/C/ExternDef.lean`) does two things with this one command:

```lean
elab_rules : command
| `(externDecl| ... alloy c extern ... def $id $bs* : $ty := $stmts*) => do
  -- 1. declare a Lean function with no body, implemented externally
  let cmd ← `(... noncomputable opaque $id $[$bs]* : $ty)
  elabCommand cmd
  -- 2. record the C body so Lake can compile and link it
  elabExternImpl exTk sym? ⟨id.raw[0]⟩ bvs ty (packBody stmts)
```

One piece of syntax yields a Lean declaration plus a generated C file, which the build system compiles automatically. The editor forwards the C regions to `clangd`, so C gets C tooling inside a Lean file.

## 3. A surface language on top of Lean's own programs (Velvet): Dafny style

Velvet defines `method … requires … ensures … do` (`verse-lab/velvet`, `CaseStudies/DataStructures/PriorityQueue.lean`):

```lean
method siftDown ... (input : Array α) (start : Nat)
  returns (result : Array α) in Id
  requires bounded: start < input.size
  ensures heap: HeapFrom result start
  ensures elements: result.Perm input
do
  let mut data := input
  let mut hole := start
  while has_left: 2 * hole + 1 < data.size
    invariant elements: data.Perm input
    decreasing remaining: data.size - hole
  ...
```

This is a **shallow embedding**. The method body is an ordinary Lean `do` program, so it runs as is. `requires`, `ensures` and `invariant` become named propositions that feed a verification-condition generator built on Lean's `Std.Internal.Do` machinery.

A small trick (`Velvet/Core/Specs.lean`): `assert` maps to a function that does nothing at runtime but carries a proposition the verifier can see:

```lean
/-- A runtime no-op that introduces an assertion into verification conditions. -/
public def assertGadget ... (_assertion : Pred) : m PUnit := pure ⟨⟩
```

The same code is executable, testable and provable, because the new syntax compiles down to ordinary Lean.

## 4. One declaration, several artifacts (Veil): a protocol modeling language

```lean
veil module FieldNamedNone₂
type value
individual none : value
relation r (n : value) (m : value)
#gen_state
action foo {
  none := *       -- nondeterministic assignment
  r := *
}
end FieldNamedNone₂
```

(`verse-lab/veil`, `VeilTest/FieldNamedNone.lean`; grammar in `Veil/Frontend/DSL/Module/Syntax.lean`, with categories such as `stateComponentKind`, `procedureKind` and `propertyKind`.)

Keywords like `individual`, `relation`, `action` and `:= *` come from the modeling languages Ivy and TLA+, not from Lean. `#gen_state` *generates* the state structure. From one module, Veil's elaborators produce a transition relation for SMT verification and an executable step function for an in-editor model checker.

## 5. Documents as programs (Verso)

```lean
#doc (Manual) "Next Steps" =>

Here is a Lean code block:

​```lean
def fib : Nat → Nat
  | 0 => 0
  | 1 => 1
  | n + 2 => fib (n + 1) + fib n
​```

The function {lean}`fib` computes Fibonacci numbers.
```

(`leanprover/verso-templates`, `slides/Slides.lean`.) The Markdown-like text is parsed by Verso's grammar and elaborated into a Lean value of type `VersoDoc genre`. The embedded `lean` blocks are elaborated for real, so a book's code examples can't silently go stale. See the [Verso deep dive](verso.md).

## 6. Getting out of Lean's lexer entirely (Strata): grammars written as data

```lean
#dialect
dialect ArithPrograms;
type num;
fn add_expr (a : num, b : num) : num => @[prec(25), leftassoc] a "+" b;
op assert (label : Label, c : bool) : Command => "assert " label c ";\n";
#end

private def testEnv :=
#strata
program ArithPrograms;
init x : num := 0;
assert [test]: (x == 0);
#end
```

(`strata-org/Strata`, `StrataTest/DL/Imperative/DDMDefinition.lean`.)

The C-style `//` comments in these files show that the text between `#dialect` and `#end` isn't Lean syntax. Strata reads grammars written as data, with precedence and associativity as attributes, and then parses programs in those dialects. The mechanism lives in Strata's `StrataDDM` dependency, which wasn't inspected here, so this part is inferred from how the files look. New languages can be defined without writing Lean metaprograms.

## 7. Teaching scripts (lean4game): a language for game authors

```lean
World "Addition"
Level 1
Title "zero_add"
Introduction "In this level we're going to prove that $0+n=n$ ..."

Statement zero_add (n : ℕ) : 0 + n = n := by
  Hint "You can start a proof by induction on `n` by typing:
  `induction n with d hd`."
  induction n with d hd
  · Hint (hidden := true) "try rewriting `add_zero`."
    rw [add_zero]
    rfl
```

(`leanprover-community/nng4`, `Game/Levels/Addition/L01zero_add.lean`.)

`World`, `Level`, `Introduction` and `Statement` are new commands. `Hint` sits inside the proof, and the elaborator records the proof state at that point. When a player reaches a matching state, even with differently named variables (`{hd}` is filled in), the hint appears. The author's model proof becomes a map of hints.

## 8. A query language that is Lean syntax (Loogle)

Loogle adds no grammar. It reuses Lean's term syntax with blanks (`_`) as a search language: `(List.replicate (_ + _) _ = _)` is elaborated as a pattern and matched against every definition in the library.

## What separates these approaches

| Question | Lighter end | Heavier end |
|---|---|---|
| Macro or elaborator? | Macros (LAMR): quick, but no type checking, so the typo above survives | Elaborators (Alloy, Velvet, Veil): type-directed errors shown at the right place in the foreign syntax |
| Deep or shallow embedding? | Deep (LAMR, Strata): the embedded program can be analyzed, transformed and printed | Shallow (Velvet): the program runs directly, and Lean's proof tools apply directly |
| What comes out? | One Lean term | Declarations plus side artifacts: C files (Alloy), generated state and executables (Veil), HTML/TeX (Verso) |
| Whose lexer? | Lean's tokens and comments | Its own (Strata's `#dialect … #end` blocks) |
| Editor support | Comes free from Lean's syntax trees: hovers, go-to-definition | Forwarded to another tool (Alloy sends C to `clangd`) |

## Worth exploring further

1. **Printing back (delaborators).** Iris-Lean, SciLean and [ProofWidgets](proofwidgets.md) make embedded terms display in their own notation, not as raw Lean.
2. **Error quality.** How Velvet and Veil report a failed `ensures` or `invariant` at the right line of the user's code.
3. **Precedence and ambiguity.** How Alloy fits C's grammar into Lean's precedence-based parser, and where it compromises.
4. **Grammars as data versus grammar as code.** Strata's approach avoids metaprograms; its tradeoffs are worth a closer look in `StrataDDM`.
5. **A small experiment.** Build a tiny language twice, once with macros and once with an elaborator, to compare error messages and type safety.
