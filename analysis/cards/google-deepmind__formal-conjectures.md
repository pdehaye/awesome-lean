# google-deepmind/formal-conjectures

- **Domain:** Formal statements of open (and solved) mathematical conjectures from Erdős problems, OEIS, Wikipedia, MathOverflow, arXiv, Hilbert/Millennium problems, and other sources.
- **Primary role:** `specification/modeling`
- **Secondary roles:** `AI-oracle/referee`, `certifier-math`, `DSL-host/metaprogramming`
- **What the kernel checks:** Mostly types only. Statements elaborate against Mathlib and are closed with `sorry`; the lakefile sets `warn.sorry = false` (about 4,780 `sorry`). Some `variants`, test and API lemmas carry full proofs (for example `erdos_1.variants.weaker` in `FormalConjectures/ErdosProblems/1.lean`).
- **Certified vs only expressed:** Mostly expressed: the main theorems state conjectures. Attributes record their epistemic status: `@[category research open/solved]` and `@[formal_proof using … at "link"]`, the latter pointing to proofs elsewhere (Erdős 1 links to an external Lean disproof). Answers to "determine X" questions are written as `answer(sorry)`, which the repository says needs human judgment to fill, not Lean alone.
- **Output artifact:** A versioned benchmark (`bench-vN` tags), a statement-metadata extractor, and docs.
- **Author mode:** Human contributors with review. The README plans to use AlphaProof to flag misformalisations. I did not check how many contributions are AI-generated.
- **Translation direction:** Into Lean (informal conjectures to Lean statements).
- **Creative idea:** `sorry` is the deliverable: each open problem is an unfilled hole tagged with its status, so that provers (human or AI) can be scored on filling it.
- **Why Lean?:** Implied by Mathlib coverage and the target audience of automated provers. My assessment: Mathlib's breadth is the deciding factor, and no other system has a comparable library.
- **Notable techniques:**
  - An `answer( )` elaborator with three modes (`always_true`, `postpone`, `with_auxiliary`), selected by an option (`FormalConjecturesUtil/Answer.lean`).
  - `category`, `formal_proof` (including `conditional … assuming`) and `AMS` attributes (`FormalConjecturesUtil/Attributes/Basic.lean`).
  - Custom linters requiring a category, AMS tag, LaTeX docstrings and other conventions (`FormalConjecturesUtil/Linters/`, `lakefile.toml`).
  - `extract_names`, which reads `.olean` files and emits statement metadata (`scripts/extract_names.lean`).
- **Heuristic check:** The Phase 1 guess was `certifier + (ships tooling executables)`. I disagree. The main theorems are deliberately unproven; this is a specification corpus and benchmark, not certification.
- **Evidence:** `README.md`, `lakefile.toml`, `FormalConjecturesUtil/Answer.lean`, `FormalConjecturesUtil/Attributes/Basic.lean`, `FormalConjectures/ErdosProblems/1.lean`, `scripts/extract_names.lean`, `FormalConjectures/OEIS/109671.lean` (grep).
