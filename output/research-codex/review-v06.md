# Independent adversarial review: version 6

**Reviewed artifact:** [v06_locked_inference_and_generality_gates.md](../../docs/ideas-codex/v06_locked_inference_and_generality_gates.md).  
**Sequence:** reviewed after version 6 was saved and before version 7 was written. Independent reviewer agent substitutes for the unavailable `codex:adversarial-review` capability.

## Assessment

The mixed-regime family design resolves the fitting-budget ambiguity, and the inference procedure now defines the actual point predictions, averaging, bootstrap, and guardrails. Failure accounting is appropriately conservative. The conditional walker replication provides a concrete path beyond the cart without promising evidence that has not been acquired. The final revision should close three implementation/interpretation gaps and explain the closest prior work more precisely, rather than expand the experiment list further.

| Dimension | Weight | Score /5 |
|---|---:|---:|
| Significance | 12% | 4.0 |
| Novelty | 18% | 2.5 |
| Conceptual/mathematical correctness | 12% | 4.5 |
| Method specificity | 12% | 4.5 |
| Identification/causal validity | 10% | 4.5 |
| Data fidelity/leakage | 10% | 5.0 |
| Experiments/baselines | 10% | 4.5 |
| Statistics/falsifiability | 8% | 4.5 |
| Feasibility | 4% | 4.5 |
| Clarity | 4% | 4.5 |
| **Weighted total** | **100%** | **82.6/100** |

**Change from version 5:** +0.8 points. **Empirical readiness:** unchanged; proposed training and validation only. This is a stronger executable design, not evidence of superiority or an estimate of acceptance probability.

## Feedback from version 5

- **V5-1:** addressed through a shared mixed-regime training population, disclosed regime flag, grouped companions, and explicit initial states.
- **V5-2:** addressed through the predictive mean, fixed within-family aggregation, delay-zero guardrail, paired bootstrap, and intersection-union rule.
- **V5-3:** addressed through optimizer/update locks, fresh final seeds, mandatory manifest fields, compute gates, and explicit treatment of failures.

## Final-revision corrections

1. **V6-1 — Reset learned memory between independent histories (Episode contract; Candidate).** The physical reset deliberately preserves memory *within* an episode. State equally clearly that memory and context priors restart between signs, regimes, noise replicas, and independent episodes. Linear and nonlinear companions share a family for splitting but must not share online inferred context. Each query branch should start from a copy of the same query-origin memory, with no update from another branch's target or simulated response. This prevents the new paired-regime design from accidentally transferring identifying information across records.

2. **V6-2 — Make the walker modification relative to the official actuator and distinguish custom observations (Generality gate).** The official XML uses knee motor gear 50, so define the alteration as `50 × (1±b)` or an equivalent multiplicative actuator gain, rather than an ambiguous absolute gain of `1±b`. The official observation function provides orientations, height, and velocities; the proposed generalized-coordinate/foot-force arrays are custom benchmark measurements. Specify ground-on-foot vertical contact-force extraction, coordinate/sign checks, and interval averaging, then verify the stated dimensions against the pinned model. The 40 Hz control rate and six motors are supported by the [official task](https://raw.githubusercontent.com/google-deepmind/dm_control/main/dm_control/suite/walker.py) and [XML](https://raw.githubusercontent.com/google-deepmind/dm_control/main/dm_control/suite/walker.xml).

3. **V6-3 — Distinguish moving codes from lost information (Evidence for retention).** A common frozen readout can fail when useful information changes its orientation in latent space across time. Add matched delay-specific readouts, or a small readout conditioned on the declared delay, alongside the common readout. Fit and tune them on the same training/validation partitions and disclose their extra parameters. If delay-specific decoding succeeds, describe a changing code rather than erasure. This refines my earlier recommendation for a common readout: that control improves comparability but is insufficient alone. [Compact but Moving](https://arxiv.org/abs/2609.21787) directly motivates this distinction by studying transported intervention-relevant directions in recurrent states.

4. **V6-4 — Explain the nearest-work distinction in ordinary language (Relation to prior work).** Replace the list-like final citation paragraph with a few specific comparisons. Chirality Nets/SWAP establish symmetry-consistent recurrence; context-adaptation work already uses history to infer hidden embodiment; ConDA's [Identifiable World Models](https://arxiv.org/abs/2610.07028) concerns recoverable coordinates and intervention responses; Compact but Moving examines changing intervention-relevant geometry. State what the present observation/reset diagnostic adds and retain the admission that gated copying is a conventional ingredient. This will make the final proposal easier to assess without increasing scope.

## Final claim boundary

The strongest defensible planned contribution is an auditable experiment separating information availability, representation geometry, and delayed predictive use. A new general-purpose memory method is not established by the design alone. If stored summaries or ordinary context already match the candidate, that result should determine the paper's central claim.
