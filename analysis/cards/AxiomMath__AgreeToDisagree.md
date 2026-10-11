# AxiomMath/AgreeToDisagree

- **Domain:** Epistemic game theory: Aumann's agreement theorem and a p-belief variant, formalised to make its hidden assumptions explicit ("assumption accounting").
- **Primary role:** `certifier-math`
- **Secondary roles:** `AI-oracle/referee`
- **What the kernel checks:** Full proofs in `AgreeToDisagree/` and `output/`, which form the built library (`lakefile.toml` globs). The only 2 `sorry` are in `input/`, the problem statements given to the prover, and `input/` is not built.
- **Certified vs only expressed:** Proven: `agreeToDisagree`, an n-agent version `agreeToDisagree'`, and `agreeToDisagree_beliefs` (posteriors that are a p-common belief differ by at most `2(1-p)`). Each proof is relative to explicit hypotheses: measurable partitions with positive-measure cells, and (in the hand-cleaned version) separate priors `μ₁ μ₂` plus an explicit agreement hypothesis `h'` that replaces the implicit common prior.
- **Output artifact:** Theorems, plus the prover's input/output pair kept as a record.
- **Author mode:** Mixed. The README says `output/` is AxiomProver's output and `AgreeToDisagree/` is the "final hand-cleaned formalisation".
- **Translation direction:** Into Lean (a paper theorem into Lean statements).
- **Creative idea:** Lean is used to account for assumptions, not only to confirm a result. For example, the AI proof's signature keeps the hypothesis `_hP₁₂` unused, which shows that hypothesis is unnecessary. The human version drops it and turns the common-prior assumption into an explicit hypothesis.
- **Why Lean?:** Not stated. My assessment: the Mathlib measure theory (`Setoid.IsPartition`, `countable_meas_pos_of_disjoint_iUnion`) and AxiomProver's Lean target are the practical reasons.
- **Notable techniques:**
  - Partitions as `Subtype Setoid.IsPartition` with the refinement lattice from Mathlib (`AgreeToDisagree/AgreeToDisagree.lean`).
  - Deriving countability from positive-measure cells, which removes the measurable-join hypothesis (`Partition.countable_of_measure_pos`, same file).
  - Keeping the `input/` (sorry stubs) to `output/` (AI proofs) to cleaned layout as a provenance trail (`input/AgreeToDisagree.lean`, `output/AgreeToDisagree.lean`).
- **Heuristic check:** The Phase 1 guess was `certifier`. I agree, and add the AI-referee aspect: Lean checks AxiomProver's output.
- **Evidence:** `README.md`, `lakefile.toml`, `input/AgreeToDisagree.lean`, `input/AgreeToDisagreeBeliefs.lean` (statement), `output/AgreeToDisagree.lean` (signature), `AgreeToDisagree/AgreeToDisagree.lean`.
