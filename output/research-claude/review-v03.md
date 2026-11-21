# Review 3: *Probe, Delay, Query* (v03)

**Proposal:** [docs/ideas-claude/v03_probe_delay_query_benchmark.md](../../notes/archive/ideas-claude/v03_probe_delay_query_benchmark.md)

## Scores

| Dimension (weight) | v02 (corrected) | v03 | Reason for the change |
|---|---:|---:|---|
| ICML significance (14) | 7 | 8 | A diagnostic account plus a benchmark that can locate failures in any world model, with a clean objective comparison, is a general contribution |
| Novelty and positioning (14) | 6 | 7 | Knobs that hold information fixed, a distractor phase boundary with a known spectrum, and contrast skill against an exact Bayes predictor are new as a combination; the remedy is still generic |
| Technical soundness (12) | 6 | 8 | Endpoint cannot reward amplification; propositions restricted to what they prove; JEPA prediction derived for the actual training pair |
| Research question, SMART (10) | 8 | 8 | Unchanged in form; the endpoint is now meaningful |
| Experiments and baselines (12) | 6 | 7 | Knobs and time-masked losses separate mechanisms well; remedy and baseline budgets remain unspecified |
| Data fidelity and leakage (8) | 8 | 8 | Same strong contract; distractor generation and augmentation transforms need their own rows |
| Statistics and falsifiability (8) | 7 | 7 | Joint family–seed sizing; the validity check H1 is wrongly placed in the Holm family with the mechanism tests |
| Feasibility and timeline (7) | 6 | 6 | The knob grid is large and the compute estimate is not itemized |
| Clarity, first principles (10) | 7 | 7 | Readable, but M2 is dense and the document is long |
| Narrative arc (5) | 6 | 8 | The loops give the study a clear sequence of decisions |
| **Weighted total** | **66.8** | **74.2** | |

## Strengths

- **Contrast skill is the right endpoint.** It is anchored at both ends (a symmetric body at 0 and the Bayes predictor at 1), it penalizes amplification and shrinkage alike, and a negative value has a direct reading: worse than guessing that the body is symmetric. It also connects to the zero-change result in the user's JEPA study.
- **The capacity experiment can now produce competition.** Predictable distractors with a designed spectrum give an exact phase boundary for linear predictors, which can be overlaid on results from nonlinear ones.
- **The JEPA claim is now honest.** Deriving the regression coefficient for the actual probe–response pair shows that the prediction holds only for informative probes, and the deep-linear test checks it where the theory applies.
- **Time-masked losses** make the memory experiment interpretable, and the weight-matched control rules out a pure loss-weighting explanation.
- **Proposition 4 is scoped correctly.** It covers direct heads, and rollout models are treated as an empirical question.

## Critiques

**R1. The remedy cannot be implemented from the text.** "Stochastic two-component belief, persistent slot, multiplicative fusion" names components without saying how the layers stay equivariant, how the two components are parameterized so that reflection swaps them, how gradients pass through the choice of component, or how the slot is written. A reviewer cannot judge whether the remedy is new or whether it is fairly compared.

**R2. The closest prior remedies for M1 are missing as baselines.** Lawrence et al.'s SymPE gives equivariant networks a random symmetry-breaking input; for a two-element group this is a random sign shared across both query branches, which can also represent the two-point joint distribution. Approximately equivariant networks (Wang, Walters and Yu, 2022) relax the constraint instead. Both are direct competitors to the two-component belief and must be in the baseline set.

**R3. Budgets are not matched.** Parameter counts, persistent storage, hyperparameter search size and training updates are not stated per model. Without them, a remedy win could come from extra capacity or extra tuning.

**R4. The JEPA arm is under-specified.** It is not stated what the target encoder sees, which anti-collapse regularizer is used, whether the physical readout is trained on a frozen encoder or jointly, or how many parameters the predictor has. Each of these choices can decide the JEPA-versus-reconstruction comparison.

**R5. The deep-linear experiment has no design.** The proposal promises a test that meets Littwin et al.'s assumptions but does not give the data model, the depths, or the quantity measured.

**R6. The practical consequence of contrast skill is asserted.** The text says a skill of 0.9 "attains 90% of the improvement", which is a restatement of the definition. A small decision task, such as choosing a differential command to produce a target change in force, would show what a loss of skill costs.

**R7. The hypothesis family mixes a validity check with mechanism tests.** H1 checks that the benchmark works; if it fails, nothing else is run. It should be a gate, outside the Holm family. H5 is an equivalence test and needs its own error-rate treatment.

**R8. The pipeline table is missing rows.** Distractor generation and normalization, the transformation of query-indexed targets under augmentation, and the pilot split each need an entry that says what is preserved and what guards against leakage.

**R9. The knob grid is not costed.** Eleven knobs crossed with objectives and seeds can multiply into thousands of fits. The proposal needs an explicit experiment inventory: which knobs are crossed and which are varied one at a time around a base configuration, how many fits that requires, and what is cut first.

**R10. The prose is becoming dense.** M2 now contains a proposition, a phase boundary, a numerical example and a derivation of the JEPA coefficient in one section. Readers outside the subfield will need a short plain-language summary before each formal statement.

## Suggestions for version 4

1. Specify the remedy completely: parity-split layers, gated nonlinearity, the two-component belief built by evaluating one network on the evidence and its reflection, an additive evidence slot with a learned gate, exact expectation over components, and a multiplicative head.
2. Add SymPE-style and approximately equivariant baselines, and match parameters, storage, updates and tuning budget.
3. Specify the JEPA arm completely, with frozen and joint readouts.
4. Design the deep-linear experiment.
5. Add a decision task that shows what a loss of contrast skill costs.
6. Move H1 out of the Holm family and treat it as a gate.

## Codex adversarial review

Codex returned **needs-attention** with seven high and three medium findings ([raw output](codex-adversarial/codex-review-v03.txt)). This review had judged v03 technically sound; several findings show otherwise. The most consequential is X2, a scoring rule under which a perfect probabilistic model would have failed the success criterion.

| # | Severity | Finding | Disposition in v04 |
|---|---|---|---|
| X1 | high | M1 confounds latent stochasticity with output-family expressiveness: a deterministic latent with a mixture head can produce the same two modes; the passive law under a continuous prior is not two points | **Fixed.** M1 is restated as a requirement on the family *and persistence* of the predictive distribution. A deterministic-latent joint-mixture baseline (B4m) is added; per-step versus persistent draws separate the designs; the passive law is described correctly, with the two-point case kept as an illustration |
| X2 | high | Scoring one sampled contrast doubles an exact sampler's risk, so a correct model could reach only $S = 0.75$ | **Fixed.** The point prediction is the predictive mean over $N$ samples, each shared across branches; $N$ is locked by a Monte Carlo accuracy rule; the appendix gives the $(1 + 1/N)R_{\text{Bayes}}$ result |
| X3 | high | The capacity boundary needs a statistic from which $\mathbb E[b \mid H]$ is linearly recoverable; raw channels have zero covariance with $b$ under a random probe sign; nonlinear losses differ | **Fixed.** The linear experiment uses an explicit balanced-probe statistic $\sum_t d(t)F_{+,t}$, squared error and a closed-form $C$; nonlinear results are separate empirical experiments |
| X4 | high | An unchanged asymmetry coefficient does not imply the JEPA ordering; predictable distractors also have high coefficients | **Fixed.** All features' variances, cross-covariances and coefficients are derived; distractors below, equal to and above the asymmetry's coefficient; the ordering prediction is restricted to low-coefficient distractors |
| X5 | high | Hold observations can refine $g$ and so change the posterior of $b$; chance recent-window accuracy does not prove fixed information | **Fixed.** An information audit reports Bayes risk across holds and the posterior coupling of $g$ and $b$; the primary memory condition fixes $g$; gate G requires constant Bayes risk across holds |
| X6 | high | Removing all query losses also leaves the response head untrained | **Fixed.** Every memory arm trains a response readout on the frozen origin state with stopped gradients; H4 is scored on these readouts |
| X7 | high | H5 is a construction check; an additive head scores zero by design | **Fixed.** M4's primary test is sample efficiency of multiplicative fusion versus concatenation in the baseline architecture at matched recoverability; the additive head is an implementation control |
| X8 | high | Failing to reject is treated as ruling a mechanism out | **Fixed.** Three outcomes (supported, excluded by an equivalence test against a meaningful effect, inconclusive), with meaningful effects and precision targets for every endpoint, including the gate |
| X9 | medium | The calibration slope labels the Bayes predictor as shrunk | **Fixed.** Attenuation is measured by regressing $\hat r$ on the Bayes mean; calibration by regressing $r$ on $\hat r$ with an intercept |
| X10 | medium | A spectral-radius bound does not give $\|A^n\| \le c\,r^n$ | **Fixed.** Proposition 3 assumes an operator-norm contraction, gives the Jordan-block counterexample, and the experiments measure Jacobian norms |

**Revised score after Codex.** X1–X5 and X7 show that four of the five mechanism tests could not have identified their mechanisms as designed, and X2 would have misjudged a correct model. Soundness drops from 8 to 6, experiments from 7 to 6, and statistics from 7 to 6, giving a corrected total of **69.8**. The scorecard uses the corrected value.
