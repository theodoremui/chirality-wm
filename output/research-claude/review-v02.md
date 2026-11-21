# Review 2: *Four Ways to Lose the Hidden Side* (v02)

**Proposal:** [docs/ideas-claude/v02_four_ways_to_lose_the_hidden_side.md](../../notes/archive/ideas-claude/v02_four_ways_to_lose_the_hidden_side.md)

## Scores

| Dimension (weight) | v01 | v02 | Reason for the change |
|---|---:|---:|---|
| ICML significance (14) | 6 | 7 | The question now concerns what predictive objectives and symmetry priors keep in general, with JEPA versus reconstruction as a central comparison |
| Novelty and positioning (14) | 4 | 6 | A mechanism framework with distinct signatures, and a benchmark that switches each mechanism, go beyond assembling components; each mechanism on its own is classical |
| Technical soundness (12) | 7 | 8 | Exact linear-Gaussian reference, a defined endpoint, careful invariance statement and explicit symmetry assumptions; two gaps remain (R2, R4) |
| Research question, SMART (10) | 6 | 8 | Named endpoint, delay, thresholds and date |
| Experiments and baselines (12) | 6 | 7 | Knob per mechanism, snapshot/VariBAD/full-history baselines, refutation criteria; knobs are entangled and the JEPA arm sits in the wrong regime (R1, R6) |
| Data fidelity and leakage (8) | 7 | 8 | Reset-and-hold, cloned branches with replay checks, memory resets, parity-safe normalization |
| Statistics and falsifiability (8) | 5 | 7 | Joint decision rule, family–seed bootstrap, Holm, pilot sizing; primary contrast per mechanism still unnamed |
| Feasibility and timeline (7) | 7 | 6 | Many arms; walker harness and standing release unverified |
| Clarity, first principles (10) | 8 | 7 | Still readable, but denser, and the bracketed finding tags interrupt the prose |
| Narrative arc (5) | 6 | 6 | The mechanisms give the paper a thesis; the experiments still read as a table, not a sequence |
| **Weighted total** | **61.1** | **70.4** | |

## Strengths

- The four mechanisms turn a vague worry ("the model may discard information") into four claims that can each be false. Each has an argument, a signature and a knob.
- The exact reference is a real contribution of the design. Because commands and the lag are known, every observation is linear in $(g, b)$, so the posterior is available in closed form even with an unknown common gain.
- The query contrast is now defined operationally and computed from cloned branches, which removes the ambiguity Codex identified.
- Retention is measured three ways (fidelity slope, frozen readouts and a context-swap test), so a loss can be located in the state, the decoder or the use.
- The snapshot and VariBAD-style baselines are the right threats: if simply storing the state at the hold onset solves the task, the paper must say so.

## Critiques

**R1. The capacity knob changes availability at the same time.** E3 varies asymmetry magnitude to change the odd response's variance. Smaller $|b|$ also makes the probe less informative, so the Bayesian slope falls and the primary analysis ($\beta_{\text{Bayes}} \geq 0.8$) excludes exactly the small-asymmetry region where collapse is predicted. A cleaner knob exists. M2 is about competition for capacity, so increase the *even* predictable variance (for example by widening the range of the common gain $g$ or of the common command $a$) while holding $|b|$, the probe and therefore availability fixed. If capacity allocation is the mechanism, retention should fall as even variance rises, with no change in what the data contain. A second clean knob is the fraction of training episodes that contain probes, with test episodes always probed.

**R2. M2 does not say which targets carry parity.** All three cart observations are even. The asymmetry appears as the part of the even total force that changes sign with $u$, not as an odd observation. The reduced-rank argument works once the target is defined as the vector of responses to a query set that reflection maps to itself, such as $\{+u^*, -u^*\}$: its sum is even and its difference (the contrast) is odd. That definition should appear in the statement, together with the linear-feature assumption.

**R3. The M2 prediction is qualitative.** "A critical magnitude that grows as the bottleneck narrows" can be made quantitative. In the linear model the threshold is where the odd block's predictable variance equals the $k$-th even eigenvalue, which can be computed from the simulator. Overlaying that predicted boundary on the measured collapse map would be the paper's most persuasive figure, and a clear failure of the prediction would also be informative.

**R4. The cost of M1 is not measured by the endpoint.** For passive histories the zero contrast that a deterministic equivariant model predicts is the correct mean, so squared-error metrics favor it. The cost appears in the predictive *distribution* and in rollouts. E2 needs a proper distributional score (CRPS or energy score; Gneiting and Raftery, 2007) and a clear statement that the deterministic model is mean-optimal but distribution-wrong.

**R5. The hold flag makes the task easier than it looks.** Every model receives a flag that marks when evidence stops. A learned gate can simply copy at the flag, which reproduces the Codex series' concern that success is close to built in. Train and test each memory model with and without the flag, and treat the flag-free result as the main one.

**R6. The JEPA arm is in the wrong regime.** Latent prediction is designed for high-dimensional inputs with unpredictable detail. On a three-channel state vector, JEPA and reconstruction will differ little, and a null result would say nothing about Littwin et al.'s prediction. Their analysis concerns features that differ in variance and in regression coefficient. The benchmark can create that regime directly: lift the observations into a higher-dimensional sensor vector and add **distractor channels** with large variance and no predictive value. Reconstruction should spend capacity on the distractors and lose the asymmetry first; latent prediction should ignore them.

**R7. Each mechanism needs one primary contrast.** E2–E5 each list several predictions. Holm adjustment requires a single named test per family. Choose one contrast per mechanism and list the rest as secondary.

**R8. The walker reference can be exact.** The proposal falls back on a learned full-history transformer as the walker's information reference, which can itself fail. With all parameters except $b$ fixed and a canonical start, the walker's probe can be simulated for each value of $b$ on a grid, which gives the likelihood of the observed history and hence a grid posterior. A simulation-based reference of this kind is exact up to the grid and the noise model.

**R9. The novelty argument is implicit.** A reviewer may say each mechanism is folklore: Curie's principle, reduced-rank regression, vanishing gradients and additive models. The paper should say plainly that the contribution is a diagnostic theory and benchmark that predicts *which* failure appears under which conditions, and that the JEPA-versus-reconstruction prediction and the quantitative capacity threshold are new empirical tests.

**R10. Thresholds need a rationale.** A retention ratio of 0.9 and a 5% next-step margin are reasonable but unexplained. State what a 10% loss of contrast means for a downstream decision, for example the error in choosing a differential command that produces a target force.

**R11. The bracketed finding tags interrupt the reading.** Move change tracking to the review and keep the proposal readable on its own.

**R12. The experiments are a table, not a line of inquiry.** The paper should show how each result decides the next question: availability first, then whether standard models fail, then which mechanism explains the failure, then whether the matching remedy fixes it, then whether the finding transfers.

## Suggestions for version 3

1. Define the benchmark formally as a set of controlled episode families with **one knob per mechanism**, choosing knobs that leave availability unchanged (even-variance spread, probe frequency in training, distractor channels, hold length, fusion type).
2. State each mechanism's assumptions explicitly, with the target parity defined through a reflection-closed query set, and give the quantitative M2 threshold.
3. Use proper distributional scores for M1.
4. Add a simulation-based grid posterior for the walker.
5. Name one primary contrast per mechanism.
6. Run memory models with and without the hold flag.
7. Organize the experiments as a sequence of loops, each with a decision.

## Codex adversarial review

Codex returned **needs-attention** with seven high and four medium findings ([raw output](codex-adversarial/codex-review-v02.txt)). Several go deeper than this review's own critiques, and two (X1, X4) correct claims that this review had accepted.

| # | Severity | Finding | Disposition in v03 |
|---|---|---|---|
| X1 | high | The retention ratio rewards amplification: a model predicting 1.2 × the Bayesian mean scores $\rho = 1.2$ with worse error; zero slope can also mean uncorrelated nonzero predictions | **Fixed.** The primary endpoint becomes the *contrast skill* $S = (R_0 - R_{\text{model}})/(R_0 - R_{\text{Bayes}})$, a squared-error skill score relative to the symmetric predictor and the Bayes predictor. Amplification lowers $S$; $S \le 1$ in expectation. The slope is kept as a calibration diagnostic |
| X2 | high | Squared-error training penalizes two-cluster predictions; passive histories have no sign information, so $\rho$ is undefined there | **Fixed.** Models are trained with proper scores (energy score over the joint pair of query branches, plus next-step likelihood); paired branches share one latent-body draw; passive histories are scored on the joint distribution, never with retention measures |
| X3 | high | Shrinking $\lvert b\rvert$ weakens evidence; the cart's query targets have rank ≤ 2, so widths ≥ 2 create no competition | **Fixed.** $\lvert b\rvert$ is never the capacity knob. Capacity competition comes from *predictable distractor channels with a known spectrum* that are part of the prediction target, with widths 1 and 2 tested explicitly; every cell reports Bayes-normalized risk |
| X4 | high | The JEPA ordering does not follow from Littwin et al.: the input-to-target regression coefficient $s t \mathrm{Var}(b)/(s^2\mathrm{Var}(b) + \sigma^2)$ vanishes as asymmetry shrinks | **Fixed.** The coefficients are derived for the actual training pairs. The ordering is claimed only in the high-SNR regime, where the coefficient approaches $t/s$ independent of $\lvert b\rvert$; a controlled deep-linear experiment matches Littwin et al.'s assumptions; the nonlinear JEPA comparison is stated as an empirical hypothesis |
| X5 | high | Next-step loss during the query already rewards retention, so E4 does not remove memory supervision | **Fixed.** Losses are written with temporal masks (probe, hold, teacher-forced query steps, open-loop query). The no-delayed-signal arm trains on probe and hold only; a query-weight-matched control is added; the zero-gradient claim is restricted to hold losses |
| X6 | high | The additive-decoder result does not cover rollouts, where a nonlinear transition can create the interaction | **Fixed.** Proposition 4 is restated for a direct response head on a frozen origin state; rollout models compare generic concatenation with explicit multiplicative fusion as an empirical question of how easily the interaction is learned |
| X7 | high | The walker has no defined endpoint or exact denominator | **Fixed.** Walker endpoint: contrast in total vertical ground impulse, normalized by body weight × horizon, for a mirrored pair of open-loop query sequences; the denominator is the simulation-grid posterior; the learned transformer is reported as a comparison only |
| X8 | medium | Reflect-inputs-keep-targets equals correct augmentation in the cart because all targets are even | **Fixed.** The negative control is an invariant history encoder with an unreflected query; transformations of trajectory and query-indexed targets are defined explicitly |
| X9 | medium | A two-second recent window at short holds includes the probe or the washout | **Fixed.** The recent window is one second, starts after a one-second washout, and is evaluated at holds of two seconds or more |
| X10 | medium | Flipping the odd block of a mirrored equivariant state is algebraic, not causal | **Fixed.** Interventions are defined per representation class with matched command and noise pairs, sham swaps and nuisance swaps, validated by readouts |
| X11 | medium | Seed variance sets a precision floor that more test families cannot remove | **Fixed.** The pilot estimates family and seed variance separately; seeds and families are sized jointly, with an insufficient-precision outcome |

**Revised score after Codex.** Findings X1, X3 and X4 show that the soundness score of 8 was too generous: the primary endpoint could reward a wrong model, the capacity experiment could not produce competition, and one theoretical prediction was misattributed. A corrected score for v02 is soundness 6 and experiments 6, which lowers the total to **66.8**. The scorecard uses the corrected value.
