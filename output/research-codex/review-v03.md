# Independent adversarial review: version 3

**Reviewed artifact:** [v03_a_parity_consistent_belief_that_can_remain_uncertain.md](../../notes/archive/ideas-codex/v03_a_parity_consistent_belief_that_can_remain_uncertain.md).  
**Sequence:** reviewed after version 3 was saved and before version 4 was written. Independent reviewer agent substitutes for the unavailable `codex:adversarial-review` capability.

## Assessment

Version 3 makes the training intervention assessable: all models receive delayed supervision, while the candidate changes when stored context can update. The parity construction and sign-mixture formulas also make the architecture more concrete. The tradeoff is now visible. A diagnostic flag identifies the interval to remember, and copying its summary may solve the task with conventional memory. The paper should test that simple explanation directly. In addition, sign-independent observations conditional on fixed nuisance parameters need not be uninformative after uncertainty about those parameters is integrated out.

| Dimension | Weight | Score /5 |
|---|---:|---:|
| Significance | 12% | 4.0 |
| Novelty | 18% | 2.5 |
| Conceptual/mathematical correctness | 12% | 4.0 |
| Method specificity | 12% | 4.0 |
| Identification/causal validity | 10% | 4.5 |
| Data fidelity/leakage | 10% | 4.5 |
| Experiments/baselines | 10% | 4.0 |
| Statistics/falsifiability | 8% | 4.0 |
| Feasibility | 4% | 4.0 |
| Clarity | 4% | 4.5 |
| **Weighted total** | **100%** | **77.0/100** |

**Change from version 2:** +0.8 points. Method and statistical specificity improve, while a newly exposed nuisance-uncertainty issue limits the mathematical score. **Empirical readiness:** unchanged; no model-training evidence exists.

## Feedback from version 2

- **V2-1:** addressed: delayed supervision is shared and no longer presented as intrinsically novel.
- **V2-2:** substantially addressed: memory size, update gate, parity construction, and mixture law are stated. Predictive marginalization remains open.
- **V2-3:** partly addressed: confidence-bound decisions and a capped sample rule are supplied, but precision must be tied to the small target effect.
- **V2-4:** partly addressed: nonlinear actuators are required for a broader claim, but shared static saturation remains close to the analytical identification problem.
- **V2-5:** addressed in the planned frozen-readout protocol, with training and query access restricted appropriately.

## Required improvements

1. **V3-1 — Test the simplest gate-based explanation (Candidate; Comparisons; Intended contribution).** The episode flag tells the model when evidence arrives, after which the candidate simply preserves a summary. Add a 128-value baseline that copies the final diagnostic encoder state and uses the same query decoder, plus a compact fitted-parameter summary when identification permits it. Compare the candidate with these controls before claiming a learned retention mechanism. Shared saturation adds nonlinear identification but little structural diversity; a result confined to the cart family should be described as a diagnostic memory result. A broader world-model method claim needs a structurally different dynamics setting or correspondingly narrower language.

2. **V3-2 — Separate conditional sign invariance from absence of posterior information (Physical experiment; Candidate).** Neutral observations are independent of the sign for matched fixed `g, τ, α`, but they can refine those nuisance parameters. If diagnosis couples sign or magnitude with nuisance uncertainty, later neutral measurements can legitimately change the mechanical belief. State the exact conditional-independence claim and test an all-observations Bayesian reference. Either make nuisance parameters known in the exact memory diagnostic and vary them as a separate stress test, or explicitly acknowledge the gate as an approximate inductive bias that may discard useful evidence. Do not infer Bayesian sufficiency from paired-sign equality alone.

3. **V3-3 — Make the trajectory and impulse distributions agree (Candidate; Statistical decisions).** Specify whether impulse comes from integration of predicted force trajectories or a separate head. A separate head can improve the primary metric without preserving physically coherent trajectories. Define the predictive sampling law, including temporal noise, and use integrated samples for the impulse. If a tractable impulse density is unavailable, a proper sample-based score such as CRPS is preferable to an unspecified log likelihood. The sum of trajectory and derived-impulse scores is a weighted composite objective; it should not be described as an exact joint likelihood for independent observations.

4. **V3-4 — Plan precision around the actual effect and lock multiplicity (Statistical decisions).** The absolute precision target `0.0005 (N·s)²` can exceed the 5% improvement margin by a large factor when comparator MSE is small. Use pilot comparator risk and paired variance to set precision as a declared fraction of the target effect, while retaining the sample cap and an underpowered fallback. State which linear/nonlinear claims, guardrail, and architecture contrasts are confirmatory and how their error rates are controlled. Keep comparator selection on validation data.

5. **V3-5 — Preserve the declared reflection through preprocessing (Shape and splits).** Training-derived normalization must commute with the reflection: odd channels need zero centering or an explicitly transformed center, and paired channels need compatible scales. Define the action, flag, force, and stored-state reflection maps, then verify involution and the decoder's transformed predictions numerically. Freeze time-index conventions for the 50-step target and its integral; recording a shape alone does not specify whether endpoint samples are included. These checks are especially useful because the claimed architectural guarantee can be broken outside the network.

## Next revision

Version 4 should emphasize the exact observation and preprocessing contract. It can keep the architecture modest while making its claimed scope honest. The largest remaining publication risk is novelty: transparent tests of simple baselines are more valuable than adding another mechanism before the current gate is understood.
