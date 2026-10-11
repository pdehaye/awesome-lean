# nikhgarg/AppliedModelingLib

- **Domain:** Economics & Computation and applied modelling: matching, auctions, fair division, recommender systems and others. It formalises about 40 research papers (lakefile default targets), with a shared library.
- **Primary role:** `certifier-math`
- **Secondary roles:** `coordination/trust-infrastructure`, `specification/modeling`
- **What the kernel checks:** Full proofs of each paper's `Spec` statements. Phase 1 counts 0 `sorry`; `docs/VALIDATION_MODEL.md` says a paper is "Lean-closed" only when its dependency closure has no `sorryAx`. Lean explicitly does not judge whether a `Spec` faithfully translates the paper; that is left to human review and LLM-as-judge passes.
- **Certified vs only expressed:** Proven: each `PaperInterface.lean` `Spec` is matched by an endpoint theorem in `ProofInterface.lean` (for example Gale–Shapley Theorem 1). Only expressed: the match between paper and Lean, which is recorded as review receipts, an obligation ledger and digests outside the kernel.
- **Output artifact:** Theorems, per-paper validation reports, dependency DAGs, and JSON audit data for a review dashboard.
- **Author mode:** AI-written, with human review. The README says "an LLM writes Lean code, Lean checks … and both humans and LLM-as-judge" verify the translation.
- **Translation direction:** Into Lean (papers to Lean).
- **Creative idea:** Each paper is split into a short human-review file of transparent `Spec : Prop` definitions and a separate proof file. Lean-side tools fingerprint the specs so that AI proof work cannot quietly weaken a statement after review.
- **Why Lean?:** Implied: Mathlib and CSLib, plus kernel checking of AI-written proofs. My assessment: kernel checking is what makes large-scale LLM authorship trustworthy, and Python could not provide that.
- **Notable techniques:**
  - The `PaperInterface.lean` / `ProofInterface.lean` split (`papers/GS62CollegeAdmissions/`).
  - A command that walks the post-elaboration declaration graph and collects axiom closures for JSON closeout (`AppliedModelingLib/Audit/DeclarationGraph.lean`).
  - Signature and manifest hashing via a helper invoked inside Lean (`scripts/lean_signature_manifest_helper.lean`).
  - A three-question validation model: Lean, human, LLM audit (`docs/VALIDATION_MODEL.md`).
- **Heuristic check:** The Phase 1 guess was `certifier`. I agree on the primary role, but it misses the large trust and audit infrastructure built around AI authorship.
- **Evidence:** `README.md`, `lakefile.toml`, `docs/VALIDATION_MODEL.md`, `papers/GS62CollegeAdmissions/PaperInterface.lean`, `papers/GS62CollegeAdmissions/ProofInterface.lean`, `AppliedModelingLib/Audit/DeclarationGraph.lean`, `scripts/lean_signature_manifest_helper.lean` (headers). Sampled one paper of about 83 folders.
