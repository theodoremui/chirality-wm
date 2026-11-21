# Independent adversarial review: version 4

**Reviewed artifact:** [v04_auditable_dynamics_and_data_contract.md](../../notes/archive/ideas-codex/v04_auditable_dynamics_and_data_contract.md).  
**Sequence:** reviewed after version 4 was saved and before version 5 was written. Independent reviewer agent substitutes for the unavailable `codex:adversarial-review` capability.

## Assessment

The exact and nonlinear conditions now make different claims for good reasons. Known nuisance parameters justify the exact diagnostic's information boundary, while the nonlinear study permits legitimate posterior updates during the delay. The timestamp contract, interval-averaged force target, commuting normalization, and snapshot controls are substantial improvements. The plan is close to an executable benchmark specification. Its main remaining weaknesses concern training fairness, the interpretation of retention, and the modest breadth of the query family.

| Dimension | Weight | Score /5 |
|---|---:|---:|
| Significance | 12% | 4.0 |
| Novelty | 18% | 2.5 |
| Conceptual/mathematical correctness | 12% | 4.5 |
| Method specificity | 12% | 4.0 |
| Identification/causal validity | 10% | 4.5 |
| Data fidelity/leakage | 10% | 5.0 |
| Experiments/baselines | 10% | 4.5 |
| Statistics/falsifiability | 8% | 4.0 |
| Feasibility | 4% | 4.0 |
| Clarity | 4% | 4.5 |
| **Weighted total** | **100%** | **80.2/100** |

**Change from version 3:** +3.2 points. **Empirical readiness:** unchanged; the benchmark, model fits, and claimed advantages remain future work. Novelty remains the limiting publication dimension despite the stronger design.

## Feedback from version 3

- **V3-1:** addressed for the present scope through snapshot and fitted-summary controls, with broader world-model claims explicitly limited.
- **V3-2:** addressed by known nuisances in the exact diagnostic and the all-observations nonlinear reference.
- **V3-3:** substantially addressed through samplewise trajectory integration, CRPS, and composite-loss terminology. The concrete training score still needs to be fixed.
- **V3-4:** substantially addressed by effect-scaled precision and a single combined primary claim. The full lock should name the comparator set and exact confidence procedure.
- **V3-5:** addressed by explicit reflection maps, normalization rules, timestamps, and interval targets.

## Required improvements

1. **V4-1 — Specify the actual gradient and scoring path (Memory, training, and coherent prediction).** Define the trajectory score, impulse CRPS estimator, weighting/normalization, number of samples, and whether training uses uninterrupted backpropagation through the diagnosis and entire delay. A candidate with a direct copy path can otherwise receive useful long-range gradients while a truncated baseline cannot. Future response targets must remain outside the recurrent input during a query rollout. Report both stored-state size and training/inference compute, including parity evaluations and Monte Carlo samples. A capped run matrix would make the twelve-week claim more credible.

2. **V4-2 — Freeze the comparator registry and selection rule (Comparators; Inference).** List which methods compete for the primary validation-selected comparator and which are privileged information references. Equation-aware identification should remain visible, but its use of the known simulator law differs from learned models. Specify how snapshot models, unrestricted recurrence, and generic gated mixtures are matched for parameter count, memory, updates, and tuning. A fixed-memory comparison and a fixed-compute comparison answer different questions; report the intended one without implying both have been guaranteed.

3. **V4-3 — Distinguish a prediction gain from a retention mechanism (Comparators; Inference).** Lower eight-second impulse error can arise from better dynamics fitting, uncertainty calibration, or easier optimization. Predeclare the recoverability curve at diagnosis end and after 1, 4, and 8 seconds using a fixed readout protocol. Compare these curves with full-history and recent-window references. State that the primary MSE contrast establishes a predictive benefit; a retention interpretation additionally needs information present at diagnosis to remain recoverable after delay, with the controls ruling out current-observation access as the explanation.

4. **V4-4 — Test a held-out temporal query, or narrow schedule language (Episode contract; Research framing).** Training and main evaluation currently use constant differential inputs from the same small set. An unseen magnitude tests amplitude extrapolation, not generalization to a new temporal schedule. Add a predeclared secondary query with an input switch or reversed pulse order, supplied at forecast origin and never used for tuning, or explicitly confine the paper to constant-query response prediction. A small temporal-composition test would strengthen the connection to world modeling without adding another large dataset.

## Remaining limitation

Even perfect execution would establish a narrow controlled memory phenomenon unless the results extend beyond these actuator equations. This is a claim boundary, not a demand to add an uncontrolled collection of experiments. The proposal should retain the option of a useful benchmark/null-result paper instead of promising an architectural breakthrough.
