# google-deepmind/formal-conjectures: agent setup

- **Snapshot:** commit `1944481` (2026-10-12), from `repos/google-deepmind__formal-conjectures/snapshot.json`.
- **Tools targeted:** `AGENTS.md` readers (Codex and others); no tool-specific files.
- **Files:** `AGENTS.md`, short guidelines that point to `CONTRIBUTING.md`, `PROOFS.md` and `STATEMENTS.md` (not copied).
- **What agents are asked to do:** add and review formal statements of open problems; occasionally add proofs or `formal_proof` claims; add reusable definitions; write PRs.
- **Build and verification:** build only the changed scope with warnings as errors, e.g. `lake --wfail build 'FormalConjectures.ErdosProblems.«361»'`; `lake --wfail build FormalConjecturesForMathlib` for shared definitions; `lake --wfail test` for utilities. "Do not build the whole project locally for a problem-file change." There is a checklist to complete before requesting review.
- **Proof policy:** inverted: "almost every problem is `sorry`", written as `by sorry`. `FormalConjecturesForMathlib/` "must not contain `sorry`". `answer(sorry)` only for what the problem asks to determine; "A tautological term inside `answer()` is not a mathematical solution." Do not put a proposed proof of an open problem in a Lean file. Nothing on axioms or `native_decide`.
- **Lean and Mathlib guidance:** state the source faithfully: check quantifier order and scope, bounds and variants, and test empty and smallest inputs. Search Mathlib and local files with `rg`; confirm types with `#check`. Follow Mathlib naming; no global `open Classical`; omit inferable type annotations; problem files import only `FormalConjecturesUtil`. Each theorem needs one `category` and at least one AMS tag, in ascending order.
- **Skills, commands, hooks, MCP:** none.
- **Permissions and safety:** none stated beyond "the diff contains only intended files and changes".
- **Human oversight:** PRs are reviewed. Reviewer notes go in the PR, not in Lean comments. The PR should say what changed, why, and how it was checked. Nothing on labeling AI contributions.
- **Notable ideas:** a checklist for whether a statement is faithful to its source; per-module `--wfail` builds to keep the loop fast; a single plain-English style rule for docs, PRs and reviews.
- **Lean-specificity:** high: nearly every rule concerns Lean statements, `answer(sorry)`, Mathlib search and the project's Lean attributes.
- **Evidence:** `AGENTS.md`.
