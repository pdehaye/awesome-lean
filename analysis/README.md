# How the awesome-lean repositories use Lean

An analysis of the repositories linked from the [list](../README.md): where Lean is used to certify things, and where it is used as a language, tool, referee or medium.

| Step | Output | What it contains |
|---|---|---|
| Phase 0 | [`inventory.json`](inventory.json) | Every GitHub repo linked from the list (87), with Reservoir metadata. Script: [`phase0_inventory.py`](phase0_inventory.py). |
| Phase 1 | [`PHASE1.md`](PHASE1.md), [`signals.csv`](signals.csv) | Code statistics per repo and heuristic role guesses, checked against 10 hand labels. Script: [`phase1_signals.py`](phase1_signals.py). |
| Phase 2 | [`cards/`](cards/) | 37 repo cards following [`CARD_TEMPLATE.md`](CARD_TEMPLATE.md): roles, what the kernel checks, the creative idea, why Lean. |
| Phase 3 | [`SYNTHESIS.md`](SYNTHESIS.md) | Role table, trust breakdown, 14 patterns of creative use, open ideas. |
| Features | [`FEATURES.md`](FEATURES.md) | 23 Lean language features worth exploring, with usage counts. Script: [`feature_scan.sh`](feature_scan.sh). |
| Deep dives | [`features/`](features/README.md) | How syntax categories and elaborators, ProofWidgets, Verso and the REPL work, with code from the repos. |

To reproduce Phase 1: `python3 phase0_inventory.py && python3 phase1_signals.py <clone-dir>`. The repos are cloned sparsely (Lean sources and build files only).
