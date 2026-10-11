# tydeu/lean4-alloy

- **Domain:** Foreign function interface tooling: writing C implementations of `@[extern]` Lean functions inline in `.lean` files.
- **Primary role:** `DSL-host/metaprogramming`
- **Secondary roles:** `program` (an `alloy` executable that emits C shims, plus a Lake build integration)
- **What the kernel checks:** Nothing substantive: there is one `theorem` in the whole repo. `alloy c extern def` elaborates to a `noncomputable opaque` declaration (`Alloy/C/ExternDef.lean`), so Lean only type-checks the Lean-side signature. The C body is parsed but never verified.
- **Certified vs only expressed:** Nothing is certified. C code is expressed as Lean syntax and emitted as C text.
- **Output artifact:** Generated C source files (`<mod>.alloy.c`), compiled to object files through Lake module facets, plus executables and libraries that link them.
- **Author mode:** Human. Headers credit Mac Malone (`Main.lean`, `Alloy/C/Grammar.lean`).
- **Translation direction:** Out of Lean: `Main.lean` imports a compiled module and writes its accumulated C shim (`C.getModuleShim`) to a file.
- **Creative idea:** Alloy encodes the full C grammar as Lean syntax categories (about 200 `syntax` rules), so C code parses as Lean syntax in the middle of a Lean file. Lake facets then extract, compile and link it automatically, and the language server forwards C regions to `clangd`.
- **Why Lean?:** Not stated beyond the goal of embedding FFI code "directly within Lean" (README). My assessment: it depends on Lean's extensible parser and Lake's programmable build graph. Neither has a direct counterpart in Coq or Dafny.
- **Notable techniques:**
  - C11 grammar as a Lean DSL: `Alloy/C/Grammar.lean`.
  - A command elaborator that turns `alloy c extern def` into an `opaque` plus a C function: `Alloy/C/ExternDef.lean`. `alloy c opaque_extern_type` with finalize/foreach hooks: `Alloy/C/ExternType.lean`, used in `examples/S/S.lean`.
  - Custom Lake module facets `alloy.c`, `alloy.c.o.export` and `alloy.c.o.noexport` that run the shim emitter: `lakefile.lean`.
  - LSP support that proxies to clangd (compilation database, semantic tokens): `Alloy/C/Server/Clangd.lean`, `Alloy/C/Server/`.
- **Heuristic check:** The Phase 1 guess was `DSL/metaprogramming + program + computation/examples`. I agree. The `#eval`s are FFI demos and tests.
- **Evidence:** `README.md`, `lakefile.lean`, `Main.lean`, `Alloy/C/Grammar.lean` (header), `Alloy/C/ExternDef.lean`, `Alloy/C/ExternType.lean` (greps), `Alloy/C/Server/Clangd.lean` (head), `examples/S/S.lean`.
