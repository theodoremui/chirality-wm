# Independent adversarial review: supplied proposal

**Reviewed source:** `chirality-world-models-adversarial-proposal.pdf`, 12 October 2026, 19 pages.  
**Review date:** 23 October 2026.  
**Provenance:** independent reviewer agent acting as a transparent substitute for the unavailable `codex:adversarial-review` capability. This is a research-design judgment, not a conference acceptance prediction.

## Assessment

The proposal has a credible measurement argument and unusually careful boundaries around causal identification. It distinguishes observation ambiguity from representation loss, correctly separates invariant from equivariant modeling, recognizes that response-coordinate losses may only reweight existing targets, and gives future-command leakage appropriate attention. Its principal weakness is the absence of a sharply specified learning contribution beyond established context inference and recurrent prediction. The extensive chemistry discussion and many prospective human datasets disperse attention without resolving that weakness.

| Dimension | Weight | Score /5 | Reason |
|---|---:|---:|---|
| Significance | 12% | 4.0 | Physical response prediction is an important test of learned representations. |
| Novelty | 18% | 2.0 | Equivariant recurrence, persistent context, and response supervision already have strong precedents. |
| Conceptual/mathematical correctness | 12% | 4.5 | Reflection rules, finite contrasts, and observation restrictions are carefully qualified. |
| Method specificity | 12% | 3.0 | The objective and backbone leave decisive implementation choices open. |
| Identification/causal validity | 10% | 4.0 | Matched branches and prospective-input rules are strong; realistic identifiability remains unverified. |
| Data fidelity/leakage | 10% | 4.0 | Most major leakage routes are identified, but archives and transformations have not been validated. |
| Experiments/baselines | 10% | 3.5 | Baseline categories are sensible; the matrix lacks a single decisive comparison. |
| Statistics/falsifiability | 8% | 3.0 | Clustered inference is recognized; primary estimand, sample size, and success threshold remain open. |
| Feasibility | 4% | 2.0 | Simulator escalation and four human studies create a large acquisition and analysis burden. |
| Clarity | 4% | 3.0 | Definitions are good; the long analogy and dataset catalog obscure the central experiment. |
| **Weighted total** | **100%** | **66.6/100** | Sum of weight × score / 5. |

**Empirical readiness:** analytical toy check only. There are no completed neural training or human prediction results. The supporting pose-restoration results cannot fill that gap.

## Prioritized revisions

1. **O1 — State a learning claim that could fail against a strong ordinary memory model (§§5–6).** Persistent context and later response prediction already appear in the original design. Specify what changes in optimization or memory, what information remains available, and why the change should matter at a fixed capacity and training horizon. Make the ordinary context estimator the primary comparator.
2. **O2 — Choose one confirmatory experiment (§6).** Begin with a reproducible delayed-response benchmark, a validated identification estimator, and one physical outcome. Move the four human datasets to a conditional external-validation plan. Archive acquisition should not determine whether the principal hypothesis can be tested.
3. **O3 — Fix the estimand before experiments (§6.3).** Name the physical response, horizon, delay distribution, population of bodies, minimum useful improvement, and unit of inference. Specify seed treatment and a sample-size rule before locked evaluation.
4. **O4 — Make the narrative proportionate to the evidence (§§2, 8).** Remove the chemistry exposition from the main argument; the direct mechanics example already explains why total response can reveal signed parameters. Preserve the sound parity derivation as a diagnostic, without treating an elementary identity as the primary theoretical contribution.

**Publication boundary:** a worthwhile simulation benchmark is plausible. A compelling ICML methods paper still requires an observed, reproducible retention gap and a remedy that exceeds matched optimization and context baselines.
