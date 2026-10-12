# How Lean projects configure AI agents

21 of the 94 GitHub repositories in the list contain AI-agent configuration files (`CLAUDE.md`, `AGENTS.md`, skills, Copilot or Kiro instructions, MCP configs, plugin manifests). This folder has one card per repository, following [`CARD_TEMPLATE.md`](CARD_TEMPLATE.md), and a synthesis below.

The cards were written from the snapshots in [`repos/`](../../repos/README.md), whose commits are recorded in each `snapshot.json`. In `repos/`, the copied agent files carry an extra `.txt` suffix; the cards cite their original paths.

## Index

| Repository | Tools targeted | Lean-specificity | Proof policy in brief |
|---|---|---|---|
| [AeneasVerif/aeneas](AeneasVerif__aeneas.md) | Claude Code, Copilot | high | Sorry'd proofs OK, sorry'd definitions never; never turn a sorry into an axiom; banned tactics |
| [LeanPool/lean-pool](LeanPool__lean-pool.md) | Claude Code, `AGENTS.md`, Copilot review | high | No `sorry`; only the three standard axioms; never drop a declaration |
| [google-deepmind/formal-conjectures](google-deepmind__formal-conjectures.md) | `AGENTS.md` | high | `sorry` is the deliverable; statements faithful to the source |
| [lean-phys-community/PhysLean](lean-phys-community__PhysLean.md) | `AGENTS.md` | high | No `sorry`, no `axiom`, no vacuous statements |
| [leanprover/cslib](leanprover__cslib.md) | `AGENTS.md`, Lean MCP | high | None stated; `--wfail` build fails on `sorry` |
| [leanprover/lean4](leanprover__lean4.md) | Claude Code (plus a shared plugin) | high | None stated |
| [nikhgarg/AppliedModelingLib](nikhgarg__AppliedModelingLib.md) | Codex | high | No `sorry`, temporary axioms or `native_decide`; no silent weakening |
| [strata-org/Strata](strata-org__Strata.md) | Kiro, lean-lsp-mcp | high | `sorry` as scaffold; Plausible as a placeholder that finds counterexamples |
| [zengineco/gonzalgo](zengineco__gonzalgo.md) | Claude Code, Codex plugins | high | (Product skills) audit `sorryAx`, `native_decide` and axiom use in other projects |
| [TauCetiProject/TauCeti](TauCetiProject__TauCeti.md) | `AGENTS.md`, Claude Code | medium | No `sorry`; only the three standard axioms |
| [gametheoryinlean/EconCSLib](gametheoryinlean__EconCSLib.md) | `AGENTS.md` | medium | No `sorry` except `answer(sorry)` in `OpenProblem/`, enforced by a script |
| [jongwony/epistemic-protocols](jongwony__epistemic-protocols.md) | Claude Code, Codex | medium | Preflight rejects `sorry` and `native_decide`; `axiom` used on purpose for model judgments |
| [justincasher/lean-explore](justincasher__lean-explore.md) | MCP, Claude Code and Codex plugins | medium | None (a search service for other agents) |
| [NyxFoundation/lean-atlas](NyxFoundation__lean-atlas.md) | Claude Code | medium | None stated |
| [verse-lab/veil](verse-lab__veil.md) | Claude Code | medium | None stated |
| [leanprover/elan](leanprover__elan.md) | Claude Code | low | Not applicable (Rust) |
| [leanprover/lean-eval](leanprover__lean-eval.md) | `AGENTS.md` | low | No linter warnings |
| [leanprover/vscode-lean4](leanprover__vscode-lean4.md) | Claude Code | low | Not applicable (TypeScript) |
| [microsoft/SymCrypt](microsoft__SymCrypt.md) | `AGENTS.md`, Copilot | low | Covers only the C library, not the Lean proofs |
| [momonpya/eggshell](momonpya__eggshell.md) | Codex plugin | low | None (product skill for installing the tool) |
| [nomeata/loogle](nomeata__loogle.md) | Claude Code | low | None (one command for JS dependency bumps) |

**Ratings:** 9 high, 6 medium, 6 low.

**The large mathematics libraries have no agent setup:** Mathlib, FLT, PFR, Carleson and the sphere-packing project among them.

## Synthesis

### 1. Three audiences

Agent files serve different readers:
- **Agents working on the repository:** most setups.
- **Agents using the product:** the skills shipped by gonzalgo (auditing proofs), Eggshell (installing it), LeanExplore (searching Mathlib through MCP) and Epistemic Protocols' 21 packaged protocols. These are distributed as Claude Code and Codex **plugins**, often from one folder targeting both.
- **Both:** Epistemic Protocols and AppliedModelingLib.

### 2. Proof policy is a spectrum, not a rule

| Stance | Repositories |
|---|---|
| Nothing stated | The Lean FRO infrastructure repos (lean4, elan, VS Code, Loogle), Lean Atlas, Veil |
| Banned only indirectly | CSLib and Lean Eval: warnings-as-errors builds fail on `sorry` |
| Banned, with an axiom whitelist | Lean Pool and Tau Ceti allow only `propext`, `Classical.choice` and `Quot.sound`, which rules out `native_decide` |
| Banned, plus vacuity | PhysLean also forbids `True` fields, `∃ …, True` and hypotheses that assume the conclusion |
| Fine-grained | Aeneas: sorry'd proofs are acceptable during work, sorry'd definitions "NEVER"; "Agents must NEVER convert a sorry into an axiom"; axioms live in `Axioms/` with a dedicated review ("a wrong axiom is a silent lie") |
| `sorry` as a working tool | Strata writes a `sorry` skeleton first, then fills it, and recommends Plausible as a placeholder that can find counterexamples |
| `sorry` as the product | formal-conjectures (open problems); EconCSLib's `OpenProblem/` folder, enforced by a checker script |
| `axiom` as an interface | Epistemic Protocols uses axioms as declared slots for the model's own judgment |

### 3. The main worry is statement integrity, not proof correctness

The kernel checks proofs; what agents can quietly damage is *what is being proven*. Each project guards this differently:
- **Lean Pool:** never drop a declaration, and change a statement only when it no longer compiles.
- **PhysLean:** no vacuous statements.
- **Aeneas:** the spec "must not be modified", and postconditions must pass a "vacuity test".
- **AppliedModelingLib:** no silent weakening, and statement fidelity checked by reviewers with no history of the authoring session.
- **formal-conjectures:** each problem stated faithfully to its source, down to quantifier order and boundary cases.

### 4. "Compiling is not proof"

Several setups say explicitly that a green build isn't enough:
- **Warnings fail the build:** `lake build --wfail`, "zero warnings".
- **Axioms are checked:** `#print axioms`, or Aeneas's `lean_verify`.
- **Bad diagnostics count:** AppliedModelingLib treats a Lean panic as a failure even when the process exits with code 0.
- **Honest reporting:** gonzalgo asks for pass rates with an explicit denominator.

### 5. Fix the code, not the check

Lean Pool, Tau Ceti, PhysLean and Aeneas forbid the usual escape hatches:
- disabling linters or adding waivers;
- raising `maxHeartbeats` or `maxRecDepth`;
- editing CI.

Tau Ceti and Lean Pool make `scripts/`, `.github/` and the lakefile human-owned.

### 6. Tactic and performance discipline

- **Aeneas:**
  - bans `omega`, `linarith`, `nlinarith` ("no exceptions"), `congr`, `all_goals` and more, and makes `agrind` the default;
  - sets budgets of under 60 s per proof, under 0.5 s per added tactic, and `maxHeartbeats` below 8M.
- **PhysLean:** keeps proofs under 50 lines, with a list of ways to split them.
- **Most projects:** build only the changed scope, because full builds are slow (Lean Pool's takes about 1.5 hours).

### 7. Interactive tooling is moving out of the repositories

- **lean-lsp-mcp** is the common interactive tool. Aeneas has a skill for it ("STOP IMMEDIATELY" if it's missing), Strata auto-approves 19 of its tools, and CSLib builds its proof loop around "the Lean MCP server". Lean Pool, on the other hand, *kills* it to save memory.
- **Shared plugins.** lean4 enables a shared `leanprover/skills` plugin rather than keeping skills in the repo, and LeanExplore ships its search service as a plugin.
- **Not captured here.** That shared tooling lives outside the snapshots, so it isn't analyzed in this folder.

### 8. Many agents at once

- **Aeneas:** fleets, verification campaigns, review gates between waves, "a full review from scratch" each time, and a hard ban on `git checkout`/`reset`/`stash`.
- **Lean Pool:** parallel agents with a RAM watchdog for Mathlib bumps.
- **AppliedModelingLib:** path leases, so several agents can share one worktree.
- **Tau Ceti:** AI rubric reviewers that can auto-merge.

### 9. Human oversight takes three forms

- **AI review replaces human review:** Tau Ceti and Lean Pool (whose Copilot review rubric includes "1 (clear AI slop)").
- **A human certifies AI work:** PhysLean requires a `Co-authored-by: Claude` trailer and certification by the human author; in Aeneas the user chooses the review mode.
- **Humans keep the irreversible actions:**
  - lean4: never merge PRs or force-push;
  - SymCrypt: "NEVER push";
  - Aeneas: "DO NOT COMMIT";
  - Loogle's command commits but doesn't push.

**Labeling AI contributions is rare.** Only PhysLean (commit trailer) and Lean Pool (a per-project `provenance` field: human, AI or mixed) do it.

### 10. Gaps and inconsistencies

- **No shared baseline.** Every project reinvents its rules on `sorry`, axioms, statement integrity and escape hatches; the same ideas recur with different wording.
- **Setups can miss the Lean part.** SymCrypt's detailed `AGENTS.md` covers only the C library, not the Lean proofs on the verified branch.
- **Agent configurations aren't tested.** Examples:
  - Aeneas: a worked example uses the banned `omega`, and two skills give `get_elem_tactic` conflicting overrides;
  - Strata: an auto-approved MCP tool name is misspelled (`loan_local_search`);
  - LeanExplore: one manifest says no authentication is needed while another requires it at install.

## Ideas for a shared Lean agent baseline

Drawn from the patterns above:
1. **A proof-policy block** covering:
   - where `sorry` is allowed;
   - an axiom whitelist, checked with `#print axioms` or `lean_verify`;
   - whether `native_decide` is allowed.
2. **Statement-integrity rules:** no dropped declarations, no silent weakening, a vacuity check, and independent review of statements before proofs.
3. **Escape hatches belong to humans:** linter options, heartbeats, CI and the lakefile.
4. **Scoped builds with warnings as errors**, plus the project's exact CI sequence.
5. **Interactive tooling:** lean-lsp-mcp usage, with a fallback when it's unavailable.
6. **Provenance:** how AI contributions are labeled.

## Limits

- **Detection relies on known path conventions** (see `AGENT_PATTERNS` in `scripts/snapshot_repos.py`). Supporting files next to skills, such as AppliedModelingLib's `references/`, aren't captured.
- **External plugins and MCP servers** referred to by a setup weren't analyzed.
- **Each card reflects one commit.** Agent setups change quickly.
