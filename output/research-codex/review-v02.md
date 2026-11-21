# Independent adversarial review: version 2

**Reviewed artifact:** [v02_observability_before_memory.md](../../notes/archive/ideas-codex/v02_observability_before_memory.md).  
**Sequence:** reviewed after version 2 was saved and before version 3 was written. Independent reviewer agent substitutes for the unavailable `codex:adversarial-review` capability.

## Assessment

The reset construction is a substantial improvement. It gives the memory claim a known observation law, retains the same sensors, and distinguishes a controlled diagnostic task from continuous dynamics. The half-second impulse has a concrete physical interpretation, and the elementary risk calculation is stated at an appropriate level. The principal unresolved issue is the actual treatment contrast: delayed query rehearsal and recurrence trained on the same delayed endpoints currently appear to optimize the same conditional likelihood. A method comparison cannot be interpreted until their difference is explicit.

| Dimension | Weight | Score /5 |
|---|---:|---:|
| Significance | 12% | 4.0 |
| Novelty | 18% | 2.5 |
| Conceptual/mathematical correctness | 12% | 4.5 |
| Method specificity | 12% | 3.5 |
| Identification/causal validity | 10% | 4.5 |
| Data fidelity/leakage | 10% | 4.5 |
| Experiments/baselines | 10% | 4.0 |
| Statistics/falsifiability | 8% | 3.5 |
| Feasibility | 4% | 4.0 |
| Clarity | 4% | 4.5 |
| **Weighted total** | **100%** | **76.2/100** |

**Change from version 1:** +5.4 points. **Empirical readiness:** unchanged; all neural-model comparisons remain proposed. The improvement reflects a better identified experiment, not evidence that the candidate works.

## Feedback from version 1

- **V1-1:** substantially addressed by the reset construction, shared sensor schedule, and full-history/recent-window controls. Its continuous-dynamics limitation is acknowledged.
- **V1-2:** partly addressed by an explicit query likelihood, but the candidate and matched baseline still need distinguishable implementations.
- **V1-3:** partly addressed through the impulse endpoint and practical thresholds; the inferential decision rule remains incomplete.
- **V1-4:** substantially addressed by a mixture and proper predictive scoring; the actual equivariant update remains unspecified.
- **V1-5:** substantially addressed through parameter support and family grouping; final pilot lock details remain necessary.

## Required improvements

1. **V2-1 — Define a nondegenerate treatment contrast (Learning intervention; Comparisons).** The stated rehearsal objective and an ordinary recurrent model given the same origins, schedules, targets, weights, and unroll length may be identical. Provide a compact algorithm or comparison table specifying every actual difference. If the method is persistent probabilistic context with reflection-consistent updates, make that the candidate and use the same query loss everywhere. If only origin sampling or loss weights change, name that intervention accurately and include its matched reweighting control. Rebranding standard multistep likelihood cannot support novelty.

2. **V2-2 — Specify the belief update and how it obeys reflection (Learning intervention).** Two Gaussian components do not by themselves yield an equivariant posterior or persistent information. Define what is stored, how an observation updates it, which parameters are fixed during a rollout, and how mixture weights, means, and covariance transform. A compact architectural specification is enough. Include a generic context model with the same dimension and mixture family so a gain cannot be attributed merely to having two modes or extra capacity.

3. **V2-3 — Make the confirmation rule executable (Research question; Comparisons).** State whether the required 5% improvement is a point-estimate threshold or a confidence-bound threshold, define the near-term noninferiority comparison, and handle an almost-zero comparator error. Give a numerical precision target and a capped pilot-based sample-size formula, or a locked fixed sample size justified by the pilot. Comparator selection must use validation only. Confidence intervals conditional on five fitted seeds cannot imply reliability across arbitrary future training runs; keep that distinction visible.

4. **V2-4 — Decide what broader evidence the paper requires (Schedule; Related work).** The cart task is solved by a low-dimensional sufficient statistic and known equations. It can validate the diagnostic and expose avoidable forgetting, but by itself gives limited evidence about representation learning in richer world models. Require one compact nonlinear or contact system for a general methods claim, with a predeclared fallback to a diagnostic/benchmark contribution if the cart alone succeeds. Retain a twelve-week scope by dropping human acquisition and adaptive probe learning, rather than treating external breadth as guaranteed.

5. **V2-5 — Audit why the memory is useful without giving the readout extra information (Comparisons).** A frozen readout should receive exactly the stored state and announced query, be fit on training families, tune on validation families, and be evaluated on the lockbox. Compare it with the same-capacity readout of a recent observation window and with a full-history reference. Check multiple delays and neutral noise levels; reset-specific episode timing or a separate sign label must not silently enter the predictor. This prevents decoder fitting, proxy labels, or clock cues from becoming an alternative explanation for a purported retention gap.

## Next revision

The most valuable next revision would freeze the candidate's memory update and a small comparison matrix. The mechanics example and causal data contract are already strong enough to support that decision. Avoid adding new terminology or loss components until the exact effect of each one can be isolated.
