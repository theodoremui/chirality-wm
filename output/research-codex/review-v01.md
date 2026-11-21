# Independent adversarial review: version 1

**Reviewed artifact:** [v01_from_pose_restoration_to_mechanical_memory.md](../../notes/archive/ideas-codex/v01_from_pose_restoration_to_mechanical_memory.md).  
**Provenance:** independent reviewer agent; substitute for the unavailable `codex:adversarial-review` capability. This review was performed after version 1 was saved and before version 2 was written.

## Assessment

The revision improves focus and feasibility. Its twelve-week question is understandable, the supporting papers are represented honestly, and a simulation-first study can be executed without pretending that unmatched human records supply counterfactual interventions. The central retention experiment was already present in the original, however, so this revision currently contributes a cleaner research plan rather than a distinctive learning mechanism.

| Dimension | Weight | Score /5 |
|---|---:|---:|
| Significance | 12% | 4.0 |
| Novelty | 18% | 2.5 |
| Conceptual/mathematical correctness | 12% | 4.5 |
| Method specificity | 12% | 3.0 |
| Identification/causal validity | 10% | 4.0 |
| Data fidelity/leakage | 10% | 4.0 |
| Experiments/baselines | 10% | 3.5 |
| Statistics/falsifiability | 8% | 3.0 |
| Feasibility | 4% | 3.5 |
| Clarity | 4% | 4.5 |
| **Weighted total** | **100%** | **70.8/100** |

**Change from original:** +4.2 points, largely from sharper scope, clearer exposition, and a more credible schedule. **Empirical readiness:** unchanged; proposed experiments only. Scores assess design quality conditional on future implementation and evidence.

## Required improvements

1. **V1-1 — Separate forgetting from altered observability (Method, steps 1 and 6).** Removing a sensor after diagnosis may create an artificial missingness shift, while remaining motion can still reveal the mechanical sign. Define a history distribution in which the diagnosis is informative but subsequent observations have a known or measured information limit. Train every method on the same sensor schedule. Include a full-history estimator, a recent-window estimator, and a no-diagnostic-history control; their differences establish whether a memory challenge exists before an architecture comparison is interpreted.

2. **V1-2 — Specify the proposed intervention on learning (Method, steps 4–5; Related work).** “Add a later-response loss” could mean ordinary multistep forecasting, extra training targets, or a change in sample weights. Write an explicit risk or objective, define the memory state and the available query action, and compare with a recurrent predictor trained on the same delayed endpoints at the same horizon. Explain the narrow residual contribution after Chirality Nets, SWAP, and intervention-oriented world models. An even/odd coordinate split alone would not establish it.

3. **V1-3 — Define the prediction target and inferential population (Research question; Comparisons).** “Later physical-response error” currently covers several incompatible units and horizons. Choose one primary physical endpoint, a fixed normalization, a delay/query distribution, and a body-level paired effect. Give a practical success threshold and a pilot-based sample-size rule. Clearly separate confirmatory tests from exploratory breakdowns.

4. **V1-4 — Make uncertainty represent unresolved laterality (Method, step 4; Comparisons).** A single Gaussian mechanical context may average opposite plausible signs into a physically misleading symmetric body. Specify a distribution family capable of preserving both possibilities and use a proper predictive score alongside coverage. Test ambiguous histories and noisy diagnoses; mean error or sign accuracy alone can reward unjustified certainty. Do not claim a physical latent coordinate merely because it is named after mechanics.

5. **V1-5 — Turn the split into a reproducible intervention design (Method, step 2).** Define a body family and its generating parameters. In a continuous simulator, every newly sampled body is numerically unseen; that fact does not establish meaningful generalization. Distinguish new samples inside the training support from held-out parameter combinations and genuinely extrapolated query schedules. Keep reflection pairs, cloned states, random disturbances, and derived sensor views grouped and document the held-out supports.

## Advice for the next revision

The next useful step is an explicit experiment and an elementary functional argument showing why discarding signed history can hurt a fixed anatomical query. Such an argument should state its observability and query assumptions and should be described as a diagnostic bound rather than a new general theorem about world models. The subsequent implementation can then be judged against a precise failure condition.

**Feedback disposition:** these five issues are open at this revision; later versions should record accepted fixes or reasoned deferrals. The proposal does not yet justify a claim of improved prediction, identified human mechanics, or a novel equivariant architecture.
