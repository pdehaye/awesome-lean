# zengineco/gonzalgo: agent setup

- **Snapshot:** commit `dd04e84` (2026-10-03), from `repos/zengineco__gonzalgo/snapshot.json`.
- **Tools targeted:** skill-capable agents through plugin manifests for Claude Code (`.claude-plugin/plugin.json`), Codex (`.codex-plugin/`) and `.agents/plugins/marketplace.json` (seen in the tree, not captured).
- **Files:** two `SKILL.md` files, both for agents *using* the product (the `gonzalgo` Python package) on someone else's Lean project. Nothing configures agents working on this repository. `lean-axiom-provenance`: what a Lean project rests on (`sorry`, `native_decide`, axioms) and why. `lean-generated-proof-audit`: checking whether machine-generated proofs really prove their theorems.
- **What agents are asked to do:** audit Lean repos and prover/LLM output; trace axiom dependencies; set up CI gates; report benchmark pass rates honestly.
- **Build and verification:** `pip install gonzalgo`; `gonzalgo lean-files ./scripts`; `lake build`; `lake env lean -D maxErrors=4000 scripts/Split.lean`; then `gonzalgo check <dump>`, which is "not optional" because `ConstantInfo.value?` returns `none` for theorems without `allowOpaque := true`. Queries: `trust` (`--fail-on-trust` for CI), `why`, `eligible`, `impact`, `profile`.
- **Proof policy:** the skills judge other people's proofs rather than write them. Flag every theorem reaching `sorryAx` upstream, `native_decide` results (`Lean.ofReduceBool`), and axioms beyond `propext`, `Quot.sound`, `Classical.choice`. "Verify the declaration you are claiming is in the environment" (Lean issue #8212). Do not call a proof wrong for using choice.
- **Lean and Mathlib guidance:** split choice dependence by statement vs. proof; `set_option maxErrors` in a file is ignored; name the Lean/Mathlib version behind any figure (here 4.32.1). Points to `axiom-audit` and `is-my-lean-proof-vacuous` for related checks.
- **Skills, commands, hooks, MCP:** the two skills; no hooks or MCP.
- **Permissions and safety:** none stated; both skills say the tool "proves nothing and checks no proofs itself".
- **Human oversight:** none stated. Reporting rules guard against overclaiming: give corpus size, how many entered the environment, how many carry `sorryAx`, and the denominator; never a corrected rate you did not compute.
- **Notable ideas:** three outcomes of a failed proof (typed `sorry`, admitted elaboration failure, never entered); a "What not to say" list; a kernel-trust profile (`kernel-trust.json`) for declaring what a project rests on.
- **Lean-specificity:** high: both skills are about Lean's kernel, axioms, `sorryAx` and elaboration behaviour.
- **Evidence:** `skills/lean-axiom-provenance/SKILL.md`, `skills/lean-generated-proof-audit/SKILL.md`; `tree.txt` for context.
