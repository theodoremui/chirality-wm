# Independent adversarial review: version 5

**Reviewed artifact:** [v05_matched_objectives_and_defeating_baselines.md](../../docs/ideas-codex/v05_matched_objectives_and_defeating_baselines.md).  
**Sequence:** reviewed after version 5 was saved and before version 6 was written. Independent reviewer agent substitutes for the unavailable `codex:adversarial-review` capability.

## Assessment

The shared score, differentiable mixture estimator, full-delay backpropagation, comparator registry, and distinction between storage and compute make the experimental comparison substantially more credible. Canonical-reset readouts also separate stored mechanics from changing physical state. The plan now exposes the strongest simple explanations rather than leaving them as future reviewer objections. The remaining work is chiefly to remove ambiguities from the frozen protocol and to specify which system receives which fits.

| Dimension | Weight | Score /5 |
|---|---:|---:|
| Significance | 12% | 4.0 |
| Novelty | 18% | 2.5 |
| Conceptual/mathematical correctness | 12% | 4.5 |
| Method specificity | 12% | 4.5 |
| Identification/causal validity | 10% | 4.5 |
| Data fidelity/leakage | 10% | 5.0 |
| Experiments/baselines | 10% | 4.5 |
| Statistics/falsifiability | 8% | 4.0 |
| Feasibility | 4% | 4.5 |
| Clarity | 4% | 4.5 |
| **Weighted total** | **100%** | **81.8/100** |

**Change from version 4:** +1.6 points. **Empirical readiness:** unchanged; no completed model training. The incremental gain reflects implementation and resource specificity, while novelty remains conditional on future evidence.

## Feedback from version 4

- **V4-1:** substantially addressed by energy score/CRPS, independent stratified banks, full backpropagation, and compute logging.
- **V4-2:** addressed by the B1–B6 registry, validation-only selection, and clearly separated information references.
- **V4-3:** substantially addressed by the fixed canonical-reset readout and delay curve.
- **V4-4:** addressed by switched-query testing; make clear that these are held-out *forecast queries*, since diagnostic histories already contain changing commands.

## Required improvements

1. **V5-1 — Allocate the fitting budget across the exact and nonlinear conditions (Physical systems; Resources).** The 56-fit count covers seven methods with three tuning fits and five final fits, but the document does not say whether those models train on the linear system, nonlinear system, or both. A model trained only on nonlinear systems should not be interpreted as an in-distribution test on a separate linear system. Choose an explicit allocation: separate fits with their cost counted; one training population with declared condition indicators and no hidden-parameter labels; or an exact diagnostic restricted to analytical/generator verification. The retention conclusion must then match the available learned-model evidence. Specify diagnostic initial state as well as the post-diagnostic reset.

2. **V5-2 — Finish the primary inference definition (Inference).** Define the predictive point estimate used for MSE, the exact query/noise/seed averages within each family, and whether the “near-term” guardrail means a one-step forecast or the same half-second impulse at zero delay. Specify the paired bootstrap procedure, number of draws, and one-sided versus two-sided convention. Recompute nonlinear quantities such as RMSE within each bootstrap draw. State explicitly that requiring all primary conditions is an intersection-union decision, while individual exploratory contrasts do not inherit a confirmatory guarantee. A validation-selected comparator need not be the test-best comparator; keep that scope in the wording.

3. **V5-3 — Turn the resource and failure rules into a lock checklist (Resources; Data contract).** Name the finite training update budget, optimizer/learning-rate set, fresh final seeds, number of training families, and target Monte Carlo stability criterion—or specify that these values are mandatory fields filled from the pilot before the generator/test lock. If a resource cap cannot support the primary registry, stop for a documented protocol revision before confirmation rather than silently dropping difficult baselines. Prespecify how nonfinite predictions, crashed fits, and invalid simulator branches are counted; excluding failures after seeing method performance would bias the comparison.

## What still depends on results

The current architecture is deliberately modest and strongly assisted by the announced diagnostic gate. That is acceptable for a controlled experiment. It becomes an ICML learning contribution only if the results reveal a reproducible limitation, explain which baseline fails and why, and show a benefit beyond the stored-summary alternatives. A fully specified null result would support a narrower benchmark or methodological caution.
