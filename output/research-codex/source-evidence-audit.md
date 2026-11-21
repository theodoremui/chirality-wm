# Evidence audit of the three supplied manuscripts

Audit date: 23 October 2026. This is an independent analysis of the supplied documents, not a replication of their experiments. Page numbers refer to PDF pages. Text was extracted from every page; the original proposal's analytical figures/equations on pp. 7–8, the JEPA results figure and table on p. 6, and the URTC methods/results on pp. 2–4 were also inspected as rendered pages. Numerical claims below are attributed to the manuscripts. Their raw measurements, model checkpoints, and analysis code were not provided for independent reanalysis.

## Main finding

The sources support a carefully controlled question about preserving task-relevant information, but they provide no completed evidence that JEPA or reflection equivariance destroys useful mechanical asymmetry. The strongest foundations are their unusually candid evaluation audits: anatomical identity needs a separate test; a low-dimensional response score can improve while complete motion deteriorates; synthetic variants must inherit their source person's split; and apparently numerous gait clips may contain very few independent people or recording sources.

The original proposal already makes many of these distinctions correctly. Its main weakness is a still-unresolved machine learning contribution, spread across a large experimental program. A stronger paper would select one failure mechanism, one proposed remedy, and one decisive set of equal-information comparisons.

## 1. Original proposal: what is established

Source: [When Symmetry Hides the State: Learning Asymmetric Mechanics through Controlled Response](../../../../Downloads/hai/chirality-wm/chirality-world-models-adversarial-proposal.pdf), 19 PDF pages.

The proposal explicitly distinguishes restoration from action-conditioned prediction (p. 1); invariance from equivariance (p. 4); physical interventions from observed future commands (pp. 10–11); and identifiable measurements from information retained in a representation (p. 2). These are substantial strengths that should survive every revision.

The bilateral actuator example on pp. 6–8 is algebraically sound under its declared restriction. With left/right gains `g+b` and `g−b`, common command `a`, and differential command `u`, the forces are

`F_L = (g+b)(a+u)`, `F_R = (g−b)(a−u)`.

Therefore total force is `F_+ = 2ga+2bu`, and signed difference is `F_− = 2ba+2gu`. A total-only baseline at `u=0` cannot identify the sign of `b`; its response to a known signed input can. Individual labeled forces at baseline already identify that sign when the other required quantities are known. The original states this boundary explicitly.

The finite-contrast parity result on pp. 7–8 follows by substitution. It is an explanatory identity rather than a substantial novelty claim. The same pages correctly show that total/difference squared losses equal a rescaled bilateral squared loss, so changing coordinates creates neither information nor a new learning principle. The Gaussian sign-error expression follows from a difference with mean `4bδ` and variance `2σ²`. The original reports a Monte Carlo verification, which remains a check of a specified toy model rather than a learned-world-model result.

The persistent-context construction on p. 9 correctly holds a sampled mechanical context fixed during a rollout and updates beliefs from actual observations. The proposal also allows odd-by-odd interactions, which matter because `bu` is reflection-even. These are good implementation constraints; existing recurrent inference, Bayesian identification, and equivariant state-space models still threaten novelty.

The human datasets on pp. 12–14 answer different questions. None supplies the complete crossed mechanics-by-probe experiment. The appendix acknowledges that archives were not fully acquired and synchronized. Dataset listings should therefore be described as candidate resources, with feasibility gates, rather than ready evidence.

The chemistry discussion occupies substantial space without supplying a learning mechanism. Regardless of the separate external audit of the dated Nobel statement, removing this bridge would strengthen the machine learning argument and avoid making topical context carry scientific weight. Bilateral mechanical asymmetry is not equivalent to molecular chirality.

## 2. JEPA asymmetry paper: completed evidence and its limits

Source: [Evaluating JEPA-Inspired Motion Representations through Geometry and Gait Asymmetry](../../../../Downloads/hai/chirality-wm/jepa_asymmetry_paper.pdf), 16 PDF pages. This is the title in the supplied manuscript; the original proposal's reference to a differently named local file should be reconciled in future bibliographies.

### Task and data

The task restores an already observed motion window from noisy 2D pose. A student receives estimated observations, while a teacher and decoder training use clean projected references. The complete window is available to a transformer; no future-state or action-conditioned forecast is evaluated (pp. 1–4). It is best described as reference-supervised restoration with JEPA-inspired objectives, not as completed self-supervised world-model evidence.

The documented split assigns people before generating edits, mirrors, views, and corruption: 112 training people, 692 motions, and 1,645 training windows; 14 different development people and 155 development windows (p. 4). All experimental follow-ups reuse those 14 development people and three fitted seeds. No locked-person confirmation was completed (pp. 9, 12, 15). Person-disjoint fitting limits direct leakage, while repeated adaptation to development results limits confirmatory interpretation.

Inputs preserve a prepared `[B,128,12,2]` coordinate layout, plus confidence, availability, and timestamps. Four-frame patches regroup the array into 384 tokens and decoding returns the same slots. However, resampling to 25 Hz, selecting windows, projecting, and making synthetic edits alter raw values and sometimes record counts. Shape preservation means retaining the declared tensor grid and anatomical indexing after preparation; it does not mean unchanged raw geometry or unchanged data distribution (pp. 2, 12–13).

Synthetic right-knee edits occur before physical mirroring and projection. The response is the change in the right-minus-left knee range of motion, using 95th minus 5th angle percentiles. It is neither a time derivative nor a direct measurement of strength. Projection need not turn a physical mirror into an exact sign reversal (pp. 2–3). Input naming errors and physical reflections are different transformations.

### Findings that should constrain new claims

| Reported result | Source | Defensible interpretation |
|---|---|---|
| Direct coordinate training improves pooled response error from 12.69° to 7.54° and waveform error from 18.57° to 12.07°. | p. 5 | Supervised restoration improves these noisy observations. It does not establish a JEPA advantage. |
| Always predicting zero response gives 5.811°, lower than all 16 neural configurations under the original pooled score. | pp. 5–7 | A trivial response baseline is essential. This says nothing by itself about whether zero can restore complete motion; it cannot. |
| Delta versus endpoint mean response gain is 0.373°, with crossed 95% interval [−1.110°, 1.760°]. | pp. 5, 14 | The relative benefit remains unresolved. |
| Core JEPA versus direct fitting under the change objective gives 0.688° [−0.640°, 1.977°]. | p. 14 | This primary comparison is uncertain and does not compare against the stronger direct-coordinate variant. |
| Auxiliary gradient magnitude at initialization is 10% of base for endpoint and approximately 0.0013% for delta. Clipping occurs on 11,999 of 12,000 updates. | pp. 6, 13 | Equal loss coefficients did not create equal initial optimization influence. This does not prove the cause of the ranking. |
| Adding the combined response/geometry penalty increases waveform error across all eight families. | pp. 6–8 | A scalar response objective can trade off against trajectory fidelity. Two simultaneously changed penalties prevent causal attribution. |
| Lower scalar weight improves delta ViTPose waveform error by 3.70°; adding dense supervision after this gives only 0.28° with an interval crossing zero. | pp. 7–8 | The evidence supports sensitivity to loss weighting more strongly than the proposed dense-target mechanism. |
| Delta has slightly lower response-error point estimates but more post hoc assignment failures than endpoint. | pp. 8–9 | Response accuracy and anatomical identity require separate measures. |

Rare failures materially affect the endpoint-versus-delta response score: about 74% of its mean difference arises from failure-cost contributions (p. 7). Yet both variants' unconditional successful-error contributions already exceed the zero-response score, so choosing a lower nonnegative failure penalty cannot rescue their pooled comparison. The paper handles this distinction carefully.

The post hoc assignment measure combines wrong, ambiguous, and nonfinite outcomes and has a different eligibility set from angle scoring. Its approximately 50% pooled failure is not an established chance baseline (pp. 8, 15). A new benchmark should retain these categories separately and define its denominator before training.

The paper's three principal intervals cross zero. Later analyses and repeated development use do not provide independent replications. Its available material lacks the complete reconstructed poses and checkpoints needed to repeat the pipeline (p. 15).

### Consequences for a new world-model study

Preserve the anatomical and data-provenance checks, zero-response and direct-fitting controls, and participant-level aggregation. Do not reuse the numerical gains as evidence that response objectives work. Compare auxiliary losses with both equal weights and matched initial gradient influence, then log their later gradient norms, clipping, and convergence. Change one factor at a time. Use an independent confirmation set after design choices are frozen.

## 3. URTC draft: useful feasibility work with decisive source leakage

Source: [Learning Monocular Gait Representations through Neurologically Informed World Models](../../../../Downloads/hai/chirality-wm/jepa-writeups/URTC%20Paper%20Draft%202026%20%286%29.pdf), 5 PDF pages.

The cohort contains 96 sequences from 18 source videos: 12 normal sequences from one video, nine Parkinson's sequences from two, 12 stroke sequences from three, 16 cerebral-palsy sequences from two, and 47 myopathic sequences from ten (p. 2, Table I). Some videos can contribute multiple categories, so these per-class video counts should not be added to infer a new total.

The pipeline extracts 33 MediaPipe landmarks, centers on the pelvis, scales by a sequence-level median body width, and resizes sequences to 64 frames. It masks 60% of eligible tokens among ten selected bilateral landmarks; the target encoder sees the complete sequence. Normal-only pretraining uses the 12 clips from one video. The frozen encoder supplies a pooled 384-dimensional vector to a Random Forest (pp. 2–3).

On the saved 47/21 sequence split, S-JEPA reaches 61.9% accuracy and 61.3% macro F1; the saved handcrafted reference reaches 76.2% and 72.8% (pp. 3–4). All nine test videos also occur in classifier training, and three test sequences share the pretraining source video. On the full 96-sequence split, all 16 test videos also occur in training, with four test sequences sharing the pretraining source video (p. 4). None of these results estimates unseen-video or unseen-person performance.

The reference is a saved whole-pipeline result, not a clean representation ablation. The documented earlier feature pipeline omits bounding-box crops, assumes a fixed 30 Hz rate, contains 22 all-zero features, and uses wrist indices in logic intended for ankles (p. 3). Its superior point estimate neither validates those choices nor settles whether handcrafted features are generally better.

The missingness-only control's lower accuracy than S-JEPA does not establish that embeddings avoid shortcuts. It bounds one fitted control under one representation of missingness; stronger models could exploit missingness or source artifacts differently. The paper's conclusion that missingness does not explain the embedding score should be softened to “this control does not reproduce the embedding score.”

Temporal resizing removes information about original duration unless timestamps or duration are retained. Sequence-level normalization and internal-gap interpolation can also access future samples relative to a forecasting origin. These operations may be acceptable for completed-window classification but must be redesigned for prospective dynamics. The mean/std pooling across bilateral tokens deserves a side-sensitive readout control: pooling can discard information, although positional embeddings mean that loss of laterality cannot be assumed without testing it.

The neurologically selected mask has no matched random/full-body/motion-aware/contralateral ablation. Normal-only training and literature-guided anatomy are plausible inductive biases, but this source does not establish their benefit. It also contains no physical commands, no synchronized force supervision, and no calibrated mechanical-strength labels. Use it to motivate leakage audits and pose-observation uncertainty, not as an intervention benchmark.

## 4. Independent grade of the original proposal

This score evaluates the current research plan's readiness to become a compelling ICML study. It is neither an acceptance probability nor a grade of completed experiments. Each dimension receives 0–10; weighted points equal weight × score / 10. Unverified external references are left to the literature audit rather than silently treated as valid or invalid.

| Dimension | Weight | Score | Weighted points | Main reason |
|---|---:|---:|---:|---|
| Significance and relevance to ML | 12 | 9 | 10.8 | Predictive sufficiency under intervention is broadly relevant beyond gait. |
| Specificity and testability of question | 12 | 7 | 8.4 | Three sound hypotheses, but no single locked endpoint, effect threshold, or time-bound decision. |
| Novelty relative to established methods | 16 | 4 | 6.4 | Equivariance, persistent context, response weighting, and identification are established; their new scientific payoff remains to be shown. |
| Mathematical and methodological soundness | 14 | 7 | 9.8 | Correct toy analysis and transformation cautions; the learned bottleneck and mechanism remain underspecified. |
| Experimental discrimination and baselines | 12 | 7 | 8.4 | Strong baseline intentions, but too many systems and unresolved implementation/equal-budget details. |
| Data integrity and leakage controls | 8 | 8 | 6.4 | Excellent prospective-input cautions; exact tensor contracts and acquired datasets remain incomplete. |
| Statistical inference and falsifiability | 8 | 7 | 5.6 | Appropriate independent units and falsification; power, primary contrasts, multiplicity and lockbox rules need operational definitions. |
| Feasibility and scope discipline | 6 | 5 | 3.0 | Multiple simulators, four human datasets, and optional adaptive probing overextend a first paper. |
| Clarity and narrative economy | 6 | 6 | 3.6 | Careful prose, but lengthy chemistry framing and dataset catalog obscure the central learning claim. |
| Evidence maturity and reproducibility | 6 | 3 | 1.8 | Only the toy check is completed; no demonstrated representation gap or learned remedy. |
| **Total** | **100** | | **64.2 / 100** | **Promising research direction; a focused diagnostic study is needed.** |

## 5. Priority recommendations

1. **Demonstrate the information-retention gap before designing a remedy.** Under identical causal histories, test a well-tuned direct predictor or conventional identifier against the learned state. If histories themselves do not distinguish the relevant futures, no representation objective can fix the problem. If a standard recurrent model already succeeds, report the boundary or change the hypothesized failure mechanism.
2. **Make the contribution about predictive sufficiency under a resource constraint.** State what must be predicted, which future input family is in scope, how much history or interaction is allowed, and why a compressed state fails. “Preserves asymmetry” alone can mean anything from sign classification to complete physical prediction.
3. **Keep one controlled bilateral simulator as the core study.** Use the toy as an implementation check and one complex environment as external stress testing. Treat at most one human archive as a gated secondary analysis, with its narrower claims explicit.
4. **Define the entire information contract at each stage.** Maintain immutable raw records, split independent source families before derived windows, keep timestamps/anatomical slots/masks aligned, compute normalization from training data or available past only, and supply identical action information to every model. Show the prepared input/output tensor shapes in the pipeline figure.
5. **Separate physical reflection, observation corruption, and parameter interventions.** Transform actions, forces, controller/environment state, and anatomical labels when testing equivariance. A reflected recording is neither a new person nor an independently observed counterfactual.
6. **Use paired evaluation without counting replicas as people.** Aggregate windows/branches within independently sampled bodies or participants, average or separately report training seeds, and freeze the primary contrast before opening a confirmation set. Report failure rates alongside errors on a fixed eligible population.
7. **Make method selection conditional on diagnostics.** A response auxiliary deserves adoption only if its advantage survives simple loss rescaling, direct history regression, a conventional context estimator, and equal capacity/optimization comparisons. A two-stream architecture must permit odd-by-odd interactions; a single unimodal posterior must not be forced to express unresolved sign ambiguity as certainty.
8. **Turn the schedule into decision gates.** Reserve an early phase for simulator reflection/clone tests and identifiability checks, a middle phase for diagnostic and matched baselines, and a final phase for locked confirmation. State in advance which negative outcomes eliminate each proposed novelty claim.

The central editorial choice is to retain the sources' honesty while reducing their accumulated machinery. An ICML-facing paper needs a learning phenomenon that other researchers can test and reuse, supported by a protocol that makes its alternative explanations difficult to sustain.
