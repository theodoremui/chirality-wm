# Review 1: *What a Probe Reveals* (v01)

**Proposal:** [docs/ideas-claude/v01_what_a_probe_reveals.md](../../docs/ideas-claude/v01_what_a_probe_reveals.md)
**Rubric:** [scoring-rubric.md](scoring-rubric.md)

## Scores

| Dimension (weight) | Score | Change from Codex v07 | Reason |
|---|---:|---:|---|
| ICML significance (14) | 6 | +1 | Motivation now runs through world models and the spread of symmetry priors in robot learning, though the question remains about one toy parameter |
| Novelty and positioning (14) | 4 | 0 | The model combines equivariant recurrence, persistent context and a response loss, all of which exist |
| Technical soundness (12) | 7 | −1 | Mostly correct; the invariance example is imprecise and the role of the two-sided belief is asserted, not derived |
| Research question, SMART (10) | 6 | −1 | Time-bound and specific; "more accurately" has no threshold and "several seconds" no value |
| Experiments and baselines (12) | 6 | −1 | Good reference set (Bayesian filter, oracle, deterministic equivariant model); no experiment varies the factors that would explain a retention failure |
| Data fidelity and leakage (8) | 7 | −2 | Family-level split with mirror twins and parity-safe normalization; missing memory resets, branch handling, controller provenance |
| Statistics and falsifiability (8) | 5 | −3 | Paired bootstrap over families with seeds; no primary decision rule, sample size or multiplicity plan |
| Feasibility and timeline (7) | 7 | +1 | Two tiers and a 13-week plan are realistic |
| Clarity, first principles (10) | 8 | +5 | Concepts are built up from one example; the prose is readable by a non-specialist |
| Narrative arc (5) | 6 | +3 | Clear motivation, but the study is a single comparison without a line of inquiry |
| **Weighted total** | **61.1** | **+1.2** | |

Version 1 trades some of the Codex protocol's rigor for a large gain in readability and motivation. The total barely moves because the scientific core is still a single comparison between a proposed architecture and baselines, with no account of why the baselines would fail.

## Strengths

- The three-question frame (availability, retention, use) is now the spine of the proposal, and the exact Bayesian filter gives availability a concrete answer.
- The two-motor example is introduced before any abstraction, and each later concept refers back to it.
- Removing the chemistry section and the four human datasets frees space for the learning question without losing anything the study can test.
- The note that the query command sequence is fixed before the query window starts closes the feedback-leakage route the original proposal warned about.
- The persistent context is sampled once per imagined trajectory, which prevents the imagined body from changing its stronger side mid-rollout.

## Critiques

**R1. There is no theory of why retention would fail.** H2 predicts that a standard recurrent world model "loses the sign information as the delay grows". Nothing in the proposal says why. If the baseline happens to retain the information, the study ends with a null result and no explanation; if it does not, the study cannot say which design choice caused the loss. An ICML paper needs candidate mechanisms that make different predictions.

**R2. The reason for the two-sided belief is not stated.** The proposal introduces a mixture with one component per side but does not explain what goes wrong without it. The underlying fact is Curie's principle for equivariant functions: a deterministic equivariant model given a mirror-symmetric input must return a mirror-symmetric output (Smidt, Geiger and Miller, 2021; Kaba and Ravanbakhsh, 2023). A passive cart history is mirror-symmetric, so a deterministic equivariant model must predict zero signed response, and its imagined rollouts all describe an average body that does not exist. A stochastic equivariant model avoids this by placing equal probability on two asymmetric outcomes (Lawrence et al., ICLR 2025). This should be stated and tested, because it is the clearest formal reason the proposed model differs from the SWAP-style baseline.

**R3. The invariance example is imprecise.** Section 3 says an invariant model "would give the same internal state for a left-stronger and a right-stronger body". Invariance equates the states for a history and its mirror image, which reflects both the body and the probe. The correct consequence is that an invariant model gives the same prediction for a fixed later query on two mirror-twin bodies whose probes were also mirrored, even though their true responses have opposite signs.

**R4. The primary metric mixes availability with retention.** Error in the signed response is affected by sensor noise and probe strength as well as by memory. A model can score poorly because the data were weak. The natural correction is to compare each model with the Bayesian filter given the same history, for example through the ratio of their predicted signed responses. A second gap is that the metric cannot detect the failure the user's JEPA study suggests: predictions that shrink toward zero asymmetry. A regression slope of predicted on true signed response, where 1 means faithful and 0 means collapse to symmetric predictions, would expose shrinkage directly.

**R5. JEPA is described but not studied.** The user's prior work and the most active current debate about world models both concern latent prediction versus reconstruction. Littwin et al. (NeurIPS 2024) show that in deep linear networks JEPA objectives favor features with large regression coefficients, whereas reconstruction favors features with large variance. A signed asymmetry is a textbook example of a small-variance, highly predictive feature. Comparing objectives on the same episodes would make the paper relevant well beyond bilateral bodies.

**R6. The research question lacks a decision threshold.** "More accurately" and "several seconds" should be replaced with a named metric, the delay at which it is measured, and the size of difference that counts as success.

**R7. The experiment varies delay but not the factors that would explain a failure.** If retention fails, the next question is whether it fails because the asymmetry is small, because probes are rare in training, because the latent state is too narrow, or because the decoder cannot combine context with the command. None of these is varied.

**R8. The role of mirror augmentation is unclear.** Augmenting with reflected episodes and their reflected labels makes an unconstrained model approximately equivariant. It is a useful baseline, but the proposal should say what it is expected to show. A deliberately wrong augmentation, which reflects inputs but keeps the original labels, would make the model invariant and could serve as a negative control.

**R9. Leakage routes remain.** The proposal does not say that recurrent memory is reset between independent episodes, how branches generated from one saved state are kept together, or on which bodies the walker's nominal controller is designed. A controller tuned on test bodies would leak their mechanics into the data.

**R10. Statistical plan is incomplete.** There is no fixed primary endpoint, no rule for declaring success, no sample-size reasoning for the number of test families, and no adjustment for the several comparisons implied by H2 and H3.

**R11. The walker's observation restriction is unspecified.** If both knee angles are observed during walking, an asymmetric knee gain will produce a visible limp and the sign of $b$ may be available without any probe. The availability question has to be asked again for the walker, and the proposal needs an empirical reference for it because no exact Bayesian filter exists there.

## Suggestions for version 2

1. **Name the mechanisms.** State a small set of distinct ways a predictive model can lose the asymmetry, each with a short formal argument and a measurable signature. Candidates: the symmetry constraint (Curie's principle), capacity allocation under squared-error training, the absence of any training signal for retention during an uninformative delay, and decoders that cannot combine odd context with an odd command.
2. **Adopt an oracle-normalized retention measure and a shrinkage measure.** Report the fidelity slope of predicted against true signed response and its ratio to the Bayesian filter's slope.
3. **Compare training objectives.** Add reconstruction-based, latent-prediction (JEPA-style) and response-trained world models.
4. **Give each mechanism a knob.** Vary asymmetry magnitude, probe frequency, latent width and decoder fusion alongside delay.
5. **Make the research question measurable** with explicit thresholds and the delay at which they apply.
6. **Clarify the augmentation controls** and add the invariant negative control.

## Codex adversarial review

Codex (`codex:adversarial-review`, raw output in [codex-adversarial/codex-review-v01.txt](codex-adversarial/codex-review-v01.txt)) returned **needs-attention** with seven high and three medium findings. Codex also ran a short simulation showing that, for $m = 1$, $k = 2$, $c = 0.4$ and $\tau = 0.1$, the cart's position and velocity still depend measurably on $b$ eight seconds after the probe. Activation washout alone therefore does not hide the asymmetry.

| # | Severity | Finding | Disposition in v02 |
|---|---|---|---|
| X1 | high | Activation washout does not remove asymmetry from position and velocity, so recent motion can reveal $b$ | **Fixed.** The delay becomes a *reset-and-hold* phase: a fixture returns the cart to a canonical rest state and holds it, while the model's memory is kept. A free-delay condition is kept as a labeled secondary condition with recent-window references |
| X2 | high | The "exact" Bayesian reference ignores randomized $g$, $\tau$, $m$ | **Fixed.** Core condition: $\tau$, $m$, $k$, $c$ known and fixed; $g$ and $b$ unknown. Because commands are known, every observation is linear in $(g, b)$, so the posterior is available in closed form. Unknown-$\tau$, unknown-$m$ condition uses a Rao–Blackwellized reference with reported convergence. References given true nuisances are labeled privileged |
| X3 | high | The signed-response estimand is undefined | **Fixed.** Defined as the *query contrast*: half the difference between responses to $+u^*$ and $-u^*$ from the same cloned origin state, for the model and for the simulator |
| X4 | high | Prediction error cannot establish information loss or use | **Fixed.** Frozen-state readouts at probe end and at each delay (common and delay-specific, fit on training families), interpreted as usable information for the tested readout class, plus a context-swap test for use |
| X5 | high | The walker may reveal asymmetry continuously | **Fixed.** Walker episodes use a harnessed probe and a harnessed hold with zero commands, then an open-loop released query from a canonical pose. A walking condition with a fixed policy is kept as a labeled continuous-evidence condition |
| X6 | high | Baselines cannot isolate the contribution; no stored-summary or full-history model | **Fixed.** Added a snapshot baseline, a full-history transformer and a VariBAD-style belief model; the remedy is factored into separate ablations |
| X7 | high | No decision rule, margins or seed treatment | **Fixed (outline).** v02 states the primary endpoint, success threshold, noninferiority margin, crossed family–seed bootstrap and failed-fit rule; v05 will freeze the full analysis plan |
| X8 | medium | H2 is not tested because every model gets query loss | **Fixed.** Next-step-only arms test M3; query-supervised arms test the remedies; full backpropagation through the episode is specified |
| X9 | medium | Output invariance confused with latent collapse; symmetry of the data-generating process not stated | **Fixed.** Encoder invariance and predictor equivariance are separated, and the symmetry assumptions on the full data-generating process are listed |
| X10 | medium | No resource inventory or feasibility gate | **Fixed (outline).** Appendix gives family counts, sequence lengths, fit counts and a GPU-hour estimate with a week-2 pilot gate |

**Revised score after Codex.** X1–X3 show that v01's central experiment could not have isolated retention: recent motion leaked the asymmetry, the reference was not exact, and the endpoint was undefined. Soundness drops from 7 to 6 and data fidelity from 7 to 6, giving a corrected total of **59.1**. The scorecard uses the corrected value.
