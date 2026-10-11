# leanprover/LNSym

- **Domain:** A formal Armv8 AArch64 ISA model and symbolic simulation for proving machine-code programs correct, aimed at cryptographic kernels (SHA-512, AES-GCM from AWS-LC).
- **Primary role:** `certifier-software`
- **Secondary roles:** `specification/modeling`, `DSL-host/metaprogramming`, `program`
- **What the kernel checks:** Full proofs for small programs (`Proofs/Popcount32.lean`, `Proofs/Experiments/Abs` using `bv_decide`, which leaves `.lrat` certificates). The headline SHA-512 and AES-GCM proofs still contain `sorry` (`Proofs/SHA512/SHA512Loop.lean`, `SHA512BlockSym.lean`, `Proofs/AES-GCM/GCMGmultV8Sym.lean`). Benchmarks can run with `debug.skipKernelTC true`.
- **Certified vs only expressed:** Properties of small programs and the simulation lemmas are certified. The ISA semantics is only *validated* by co-simulation against real hardware. The crypto end-to-end results are incomplete.
- **Output artifact:** Theorems, plus an `lnsym` executable that runs random conformance tests of the Lean ISA model against an Arm machine.
- **Author mode:** Human (Amazon and Lean FRO authors in headers). Development stopped in December 2024 according to the last commit.
- **Translation direction:** Into Lean: machine code is embedded as `(address, 32-bit opcode)` lists via `def_program`, and ELF binaries are loaded through ELFSage.
- **Creative idea:** The same Lean ISA model is both a proof object and an executable that is co-simulated: the Lean binary spawns native Arm instructions and compares register states. Custom symbolic-execution tactics (`sym_n`, `sym_block`) step through binaries inside proofs.
- **Why Lean?:** Not stated. My assessment: one artifact serves as a fast executable model for conformance testing, as a proof target, and as the host for custom tactics plus `bv_decide`. In ACL2 this was possible but untyped; Coq/Isabelle would need extraction.
- **Notable techniques:**
  - Co-simulation harness using `IO.Process` to call `Arm/Insts/Cosim/armsimulate` (`Arm/Cosim.lean`, `Main.lean`).
  - Symbolic-simulation tactics `sym_n` and `explode_step` (`Tactics/Sym.lean`), `sym_block` (`Tactics/SymBlock.lean`), and `#genProgramInfo` (`Tactics/StepThms.lean`).
  - The `prune_updates` and `cse` tactics simplify large state terms (`Tactics/PruneUpdates.lean`, `Tactics/CSE.lean`).
  - Generic partial-correctness framework (`Correctness/Correctness.lean`).
- **Heuristic check:** The Phase 1 guess was `spec+proof + DSL/metaprogramming + computation/examples + (ships tooling executables)`. I agree. Note that the flagship proofs are unfinished (37 `sorry`).
- **Evidence:** `README.md`, `lakefile.lean`, `Main.lean`, `Arm/Cosim.lean`, `Proofs/Popcount32.lean`, `Proofs/SHA512/SHA512Loop.lean`, `Proofs/SHA512/SHA512BlockSym.lean`, `Proofs/AES-GCM/GCMGmultV8Sym.lean`, `Benchmarks/SHA512_50_noKernel_noLint.lean`, `Specs/SHA512.lean`, tactic grep, directory listings.
