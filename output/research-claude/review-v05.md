# Review 5: *A Leakage-Proof Pipeline and a Preregistered Analysis* (v05)

**Proposal:** [docs/ideas-claude/v05_leakage_proof_pipeline_and_preregistered_analysis.md](../../notes/archive/ideas-claude/v05_leakage_proof_pipeline_and_preregistered_analysis.md)

## Scores

| Dimension (weight) | v04 (corrected) | v05 | Reason for the change |
|---|---:|---:|---|
| ICML significance (14) | 8 | 8 | Unchanged; both tiers remain simulated and low-dimensional |
| Novelty and positioning (14) | 7 | 7 | The model's novelty is now honestly narrowed to a combination, since input-conditioned SymPE already gives evidence-dependent sign weights; the diagnostic account and benchmark carry the contribution |
| Technical soundness (12) | 6 | 8 | All eleven v04 Codex findings resolved, including the controller error and the normalization that would have cancelled the capacity knob |
| Research question, SMART (10) | 8 | 8 | Unchanged |
| Experiments and baselines (12) | 7 | 8 | Input-conditioned SymPE, autoregressive mixtures and a flag-free snapshot; M1 classes defined |
| Data fidelity and leakage (8) | 8 | 10 | Every array, the reflection operator per tier, six automated checks, and a per-step independent unit |
| Statistics and falsifiability (8) | 7 | 9 | Registered plan, paired two-way bootstrap, ordered decision table, walker replication family, locked test, deviation policy |
| Feasibility and timeline (7) | 6 | 7 | Costed inventory under a cap with a cut order |
| Clarity, first principles (10) | 6 | 7 | The words–formal–test structure makes each mechanism readable |
| Narrative arc (5) | 8 | 8 | Unchanged |
| **Weighted total** | **70.8** | **79.3** | |

## Strengths

- **The data contract is now the strongest part of the proposal.** Shapes, channel parities and the reflection operator are written down for both tiers, and six automated checks turn the leakage rules into tests that fail loudly. The hidden-parameter store, which training code cannot read, closes a route that most simulation studies leave open.
- **Each step names its independent unit,** so it is visible that windows, branches, noise replicates and reflected copies never inflate the sample.
- **The analysis plan is registrable.** Estimators, bootstrap construction, multiplicity, the walker replication rule and the locked-test procedure are specified well enough for a third party to check them.
- **Meaningful effects have reasons.** The conversion from contrast skill to control error, and the quarter-gap rule for energy scores, mean the effect sizes come from the problem and not from convenience.
- **Figure 1** shows the whole pipeline on one page, with what each stage preserves and guards against.

## Critiques

**R1. External validity is the main remaining weakness.** Both tiers are simulated, proprioceptive and low-dimensional. ICML reviewers working on world models will ask whether anything changes when observations are images, which is the regime where JEPA-style models are used and where the capacity mechanism should matter most. They will also ask whether the account says anything about real movement.

**R2. The user's own data and encoders are not used.** The JEPA asymmetry study built paired synthetic knee edits on AMASS motion with person-level splits, trained JEPA-style encoders, and kept a locked confirmation cohort that was never evaluated. That cohort is an uncontaminated test set for one question this proposal can ask: do those trained encoders keep the sign and size of a knee edit in a way a readout can recover, and does contrast skill explain the zero-change result? Using it would connect the new study to real motion at almost no data cost.

**R3. The walker has no nuisance uncertainty.** All walker parameters except $b$ are fixed, which makes the walker tier easier than the cart's even-spread condition. A second unknown parameter, such as a common leg-gain scale on a two-dimensional grid, would keep the grid posterior exact while restoring the competition that M2 depends on.

**R4. The walker's model set is not named.** The inventory says five models are run on the walker, but not which five.

**R5. The paper's claim under each outcome is implicit.** Loop decisions say what to do next, but the proposal does not say what the paper will claim, and under which title, if the signed belief wins, if a snapshot matches it, or if every standard model already succeeds. Writing this down in advance protects against reframing the results after they are seen.

**R6. The abstract is too procedural.** It now spends a third of its length on the data contract. The user asked for a strategic abstract that states the question, the idea and why the answer matters, without the mechanics of the study.

**R7. Compute risk is concentrated in the walker.** About 100 of the 265 GPU-hours go to the walker, which also has the largest feasibility risk (upright release, contact extraction). The plan should state what the paper reports if the walker gate fails in week 2.

## Suggestions for version 6

1. Add a pixel variant of the walker (rendered frames) for the objective comparison, gated on compute.
2. Add a re-analysis of the user's JEPA pose encoders on the study's untouched locked confirmation cohort.
3. Add a second unknown parameter to the walker on a two-dimensional exact grid.
4. Name the walker model set.
5. Write an outcome-to-claim table, including titles.
6. Rewrite the abstract to be strategic.
7. State the fallback if the walker gate fails.

## Codex adversarial review

Codex returned **needs-attention** with five high and seven medium findings ([raw output](codex-adversarial/codex-review-v05.txt)). The physical leak in X1 was a regression introduced when the reset was described; X5 rests on a simulation Codex ran during the review.

| # | Severity | Finding | Disposition in v06 |
|---|---|---|---|
| X1 | high | The reset restored position only; the activation difference decays as $d(0)e^{-t/\tau}$, so residual force still carried $b$ | **Fixed.** Full physical reset including both activations; gate check that bodies differing only in $b$ give identical hold records under identical noise; query impulse derived from the reset |
| X2 | high | DreamerV3 (categorical latents) and SWAP (stochastic latents) were mislabeled as unimodal | **Fixed.** Faithful stochastic versions of both; deterministic and Gaussian heads become controlled ablations within one backbone; whether a model's rollouts are bimodal is measured rather than assumed |
| X3 | high | With one fixed query, a decoder can output $C \pm K\hat b$ and never form a product | **Fixed.** Query amplitude and shape vary, with held-out combinations used only in testing; the fixed-pair linear decoder is a shortcut control |
| X4 | high | H3n at one width cannot separate capacity from harder optimization | **Fixed.** H3n is a variance × width interaction with a width-64 ample-capacity control and convergence diagnostics |
| X5 | high | Five-seed percentile intervals excluded a true zero 16% of the time in Codex's simulation | **Fixed.** Seeds are the units of inference, with a paired $t$ interval over 10 seeds; coverage and family-wise error are validated by simulation from pilot variance components before registration; decision intervals are Bonferroni-simultaneous |
| X6 | medium | Parity normalization divides by zero when the branch sum is constant | **Fixed.** Fixed physical scales, tested on the known-$g$ noise-free condition |
| X7 | medium | Beating a Gaussian shows non-Gaussianity, not bimodality | **Fixed.** Body distribution frozen with $\lvert b\rvert$ bounded away from zero, Gaussian optimized under the energy score, a flexible unimodal control, and reported mode separation |
| X8 | medium | Passive histories with odd distractors or noisy walker channels are not reflection-fixed | **Fixed.** Proposition 1 is restricted to reflection-fixed inputs; other passive inputs are tested for calibration and distributional symmetry |
| X9 | medium | Converging the posterior mean certifies nothing on symmetric histories | **Fixed.** References are converged on predictive means, second moments, Bayes risks and reference scores, with ESS and repeatability checks |
| X10 | medium | Time-to-threshold is undefined when the threshold is never reached | **Fixed.** Mean skill over a registered training-size grid |
| X11 | medium | The skill-to-control conversion does not hold across bodies | **Fixed.** $\delta_S$ is calibrated in the pilot against dial-a-force cost, and every model uses the Bayes reference's moment-based decision rule |
| X12 | medium | The walker inventory undercounted fits | **Fixed.** Every model–condition–tuning–seed combination counted, with pilot and coverage simulation included; total 356 GPU-hours under a 400 cap |

**Revised score after Codex.** X1 and X6 are errors in the design itself, so soundness falls from 8 to 6. X2–X4 weaken the experiments (8 to 6), X5 the statistics (9 to 7), and X12 the feasibility (7 to 6). The corrected total is **72.2**. The scorecard uses the corrected value.
