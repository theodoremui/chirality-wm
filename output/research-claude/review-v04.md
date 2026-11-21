# Review 4: *A Signed-Belief World Model, and the Baselines That Could Explain It Away* (v04)

**Proposal:** [docs/ideas-claude/v04_signed_belief_world_model.md](../../docs/ideas-claude/v04_signed_belief_world_model.md)

## Scores

| Dimension (weight) | v03 (corrected) | v04 | Reason for the change |
|---|---:|---:|---|
| ICML significance (14) | 8 | 8 | Unchanged |
| Novelty and positioning (14) | 7 | 8 | The remedy is concrete and positioned against its nearest competitors (SymPE, a deterministic mixture head); the deep-linear test of the JEPA ordering is a new experiment |
| Technical soundness (12) | 6 | 8 | All ten v03 Codex findings resolved; the mechanisms are stated as narrowly as their proofs allow |
| Research question, SMART (10) | 8 | 8 | Unchanged in form; endpoints per mechanism now have meaningful-effect sizes |
| Experiments and baselines (12) | 6 | 8 | Registry with matched storage, parameters, updates, supervision, tuning and Monte Carlo budget; equalized readouts in the memory arms; sample-efficiency endpoint for coupling |
| Data fidelity and leakage (8) | 8 | 8 | Distractor and augmentation rows added; array specifications and per-step statistical units still missing |
| Statistics and falsifiability (8) | 6 | 8 | Supported / excluded / inconclusive outcomes, equivalence margins and per-endpoint precision targets |
| Feasibility and timeline (7) | 6 | 6 | Compute is still a lump estimate |
| Clarity, first principles (10) | 7 | 6 | Every correction added a caveat, and the mechanisms section is now hard to read in one pass |
| Narrative arc (5) | 8 | 8 | Unchanged |
| **Weighted total** | **69.8** | **76.6** | |

## Strengths

- **The remedy is a model.** Parity-split gated layers, an additive evidence slot, a two-sided belief built by evaluating one network on the evidence and its reflection, a persistent body draw shared across branches, and an explicit $\kappa^- \odot u$ term can each be implemented and removed.
- **M1 is now the right claim.** The requirement is on the predictive distribution (bimodal and persistent), and the baselines separate the three ways to meet or miss it: a unimodal head (B4), a bimodal head without persistence (B4m), and a shared random sign (B5).
- **Scoring is coherent.** The predictive mean is the point prediction, contrast skill is a ratio of sums, attenuation is measured against the Bayes mean and calibration against outcomes, so none of the diagnostics mislabels the optimal predictor.
- **The memory test isolates memory.** Training every arm's readout on the frozen state with stopped gradients means a loss of skill cannot come from an untrained decoder.
- **Three-way outcomes** let the paper report a mechanism as excluded only when the data show its effect is smaller than a stated size.

## Critiques

**R1. The data contract stops at prose.** The user asked that every methodology step say how the exact shape of the data is preserved. The table names a shape only for raw episodes. The query-target array (two branches, horizon, channels), distractor channels with parity labels, masks and flags, the store of hidden parameters that training code must never read, and the reflection operator acting on all of these need explicit specifications, with automated checks: the operator applied twice is the identity, and simulating a reflected twin reproduces the reflected record.

**R2. No step names its statistical unit.** Each pipeline step should say what is independent at that point (a family, a seed, an episode nested in a family), so a reader can see why windows, branches and noise replicates never inflate the sample size.

**R3. The analysis plan is not frozen.** There is no preregistration, no analysis-code hash, no rule for when the locked test set is opened, and no statement of how many bootstrap draws are used or how the paired two-way bootstrap is constructed.

**R4. The walker's role in inference is undefined.** It is not said whether walker results enter the Holm family, form their own family, or count as replications under a stated criterion.

**R5. Meaningful-effect sizes are unexplained.** 5% of an energy score, 0.1 of contrast skill and 25% fewer episodes are plausible, but each needs a sentence on why a smaller effect would not matter. For contrast skill, the dial-a-force task offers a principled conversion.

**R6. "Best unimodal" and "best bimodal" need definitions.** H2 compares the best model in each class. The classes, the candidates in each and the validation rule that picks the best must be fixed in advance, or the comparison can be steered.

**R7. B4m is ambiguous over time.** The registry describes a mixture head over the branch *pair*, which is a single-horizon output, while H2b compares per-step and persistent draws over whole *trajectories*. Both a per-step-mixture variant and a trajectory-level mixture variant need to be listed.

**R8. The experiment inventory is not costed.** Twelve knobs, thirteen registry entries, two objectives, two tiers and five to ten seeds can multiply into thousands of fits. A table should list, for each loop, which factors are crossed, how many fits follow, and the GPU-hours.

**R9. The pipeline figure is not in the proposal,** and its final card still shows the retired retention ratio.

**R10. External validity is thin.** Both tiers are simulated, low-dimensional and proprioceptive. An ICML reviewer will ask whether the findings hold for high-dimensional observations, where JEPA-style models are used, and whether they say anything about real motion. A rendered-pixel variant of the walker and a re-analysis of the user's own JEPA pose encoders would address both at modest cost.

**R11. The corrections have made the text harder to read.** The mechanisms section now interleaves statement, caveat, prior-review history and design. Readers need the plain statement and the experiment together; the history belongs in the change log.

## Suggestions for version 5

1. Write a full data contract: every array with shape, dtype, channel order and parity label, the reflection operator, the hidden-parameter store and automated checks.
2. Give each pipeline step its statistical unit.
3. Freeze a preregistered analysis plan: estimators, bootstrap construction, multiplicity, walker replication criteria, lockbox rule.
4. Justify every meaningful-effect size, define the model classes in H2, and list both B4m variants.
5. Add a costed experiment inventory.
6. Insert the pipeline figure with the current endpoint.
7. Move review history out of the mechanism section.

## Codex adversarial review

Codex returned **needs-attention** with eight high and three medium findings ([raw output](codex-adversarial/codex-review-v04.txt)). Two of them change the paper's claims. SymPE already allows evidence-dependent sign weights, so the two-sided belief is not new in that respect. And the dial-a-force controller as written would have ranked a shrunk model above the exact one.

| # | Severity | Finding | Disposition in v05 |
|---|---|---|---|
| X1 | high | SymPE was weakened to a uniform coin; its inversion kernel already gives evidence-dependent weights | **Fixed.** Input-conditioned SymPE with persistent sampling and matched continuous uncertainty (B5), plus B5 with the evidence slot (B5+); the belief's sign weights are described as an existing construction, and the model's novelty claim is narrowed to the combination, tested by removal |
| X2 | high | Per-step mixtures need not switch bodies; an autoregressive mixture can keep a side | **Fixed.** Independent (B4s) and autoregressive (B4a) per-step mixtures are separate baselines; trajectory factorizations are stated; only the independent one is claimed to fail |
| X3 | high | Passive distributional results cannot explain probed contrast-skill failures | **Fixed.** M1 is a distributional claim; it enters the explanation of a probed failure only if swapping the failing model's output family raises its contrast skill |
| X4 | high | Per-condition normalization would cancel the distractor-variance knob | **Fixed.** Scales are frozen from the base condition; the post-normalization spectrum is reported; capacity experiments use raw loss |
| X5 | high | The deep-linear design does not match the theorem's setting | **Fixed.** Stage 1 reproduces the exact setting (stop-gradient current encoder, square weights, aligned initialization, gradient-flow check); EMA and bottleneck are Stage 2 empirical extensions |
| X6 | high | The controller divided by $2\hat\gamma$, delivering half the target and rewarding shrinkage | **Fixed.** $u = \mathrm{clip}(\Delta J^*/\hat\gamma)$ with a zero-gain rule; Bayes decision $\mathrm{clip}(\Delta J^*\mathbb E[\gamma]/\mathbb E[\gamma^2])$ as reference; qualitative claims rederived (shrinkage over-commands) |
| X7 | high | The snapshot was excluded from the primary arm although the probe schedule is public | **Fixed.** A flag-free snapshot triggered by the observed commands (B7) is in the primary arm; a randomized-probe-length condition is added |
| X8 | high | The augmentation rule ignores walker left/right joint channels | **Fixed.** Augmentation applies each tier's full operator, and check 2 verifies each transformed record against a simulated reflected body |
| X9 | medium | Reduced-rank regression needs centering or an intercept | **Fixed.** Centered variables, intercept outside the rank budget, pseudoinverse |
| X10 | medium | Bayes normalization does not hold information effects constant | **Fixed.** The claim is removed; raw, Bayes and excess risks are reported; forgetting claims are restricted to information-matched conditions |
| X11 | medium | Supported and excluded verdicts can hold at once | **Fixed.** An ordered decision table with four mutually exclusive verdicts |

**Revised score after Codex.** X1 lowers novelty from 8 to 7. X2, X4, X5 and X6 are errors of substance, so soundness falls from 8 to 6. X7 and X8 weaken the experiments (8 to 7), and X11 the statistics (8 to 7). The corrected total is **70.8**. The scorecard uses the corrected value.
