# Review 6: *From a Two-Motor Cart to Pixels and Real Motion* (v06)

**Proposal:** [docs/ideas-claude/v06_from_cart_to_walker_pixels_and_real_motion.md](../../docs/ideas-claude/v06_from_cart_to_walker_pixels_and_real_motion.md)

## Scores

| Dimension (weight) | v05 (corrected) | v06 | Reason for the change |
|---|---:|---:|---|
| ICML significance (14) | 8 | 9 | Pixels with moving backgrounds put the objective comparison where JEPA-style world models are used, and the pose re-analysis connects the account to real motion |
| Novelty and positioning (14) | 7 | 7 | Unchanged; there is still no related-work section that positions the contribution |
| Technical soundness (12) | 6 | 8 | Full reset, faithful baselines, restricted Proposition 1, fixed physical scales and converged references resolve the v05 Codex findings |
| Research question, SMART (10) | 8 | 8 | Adds the replication question; still measurable and dated |
| Experiments and baselines (12) | 6 | 9 | Walker nuisance with an exact grid, varied and held-out queries, an interaction test for capacity, and a real-motion test on an untouched cohort |
| Data fidelity and leakage (8) | 10 | 10 | Background pools split by split; reset check; pose re-analysis inherits person-level splits |
| Statistics and falsifiability (8) | 7 | 9 | Seeds as units, coverage validated by simulation, simultaneous decision intervals |
| Feasibility and timeline (7) | 6 | 7 | Every fit counted; 356 GPU-hours under a 400 cap with protected priorities |
| Clarity, first principles (10) | 7 | 6 | About 10,000 words; the core idea is hard to find in the first ten minutes of reading |
| Narrative arc (5) | 8 | 9 | Six loops and an outcome-to-claim table make the study's logic and its possible endings explicit |
| **Weighted total** | **72.2** | **81.4** | |

## Strengths

- **The pixel tier is well chosen.** The Distracting Control Suite's moving backgrounds supply exactly the high-variance, low-coefficient input under which theory predicts latent prediction and reconstruction to differ. The colored left leg keeps the sides named, and the occlusion caveat is stated rather than hidden.
- **The pose re-analysis is cheap and decisive.** It uses an existing pipeline and a cohort that no design decision has touched, and it asks a question with two clear answers: the earlier zero-change result lies either in the representation or in the readout.
- **The walker's second unknown** restores nuisance competition while keeping an exact reference, because canonical starts and fixed probe patterns make the noiseless trajectory a function of two parameters only.
- **The outcome-to-claim table** commits the paper to a claim and title for each pattern of results before any result is seen.

## Critiques

**R1. There is no related-work section.** Since version 2, prior work has been discussed only in passing in the introduction and the baseline table. The user asked for related work in well-supported detail, and an ICML reviewer will look for a section that groups the closest work, says what each line leaves open, and states the gap. Four lines need it: world models and their objectives, symmetry and symmetry breaking in learned models, inference of hidden context, and probing what representations contain.

**R2. The document is too long to read as a proposal.** At about 10,000 words, with eight hypotheses, five tiers of models and four automated-check lists, a reader cannot find the core idea quickly. The final version should keep a main text of moderate length (motivation, concepts, the four mechanisms, the benchmark, the model, the hypotheses and the plan) and move the data contract details, proofs, inventory and decision rules to appendices.

**R3. The introduction under-sells why world models and why asymmetry.** It states that world models let a controller test an action. It does not show the reader a concrete case of what goes wrong when an asymmetry is lost: a planned assistance profile for one leg that is wrong in sign, or a robot that compensates for the wrong motor. One short example would make the motivation concrete.

**R4. The pose tier needs a stated limit of interpretation.** The ordinary skill score against zero change is now defined, and failed readouts are scored both ways. What remains is to say how far a synthetic knee edit on real motion can speak for a real asymmetry: it tests whether encoders keep a signed geometric difference, which is a narrower question than whether they keep a mechanical one.

**R5. The pixel tier is planned at its reduced size,** which resolves the earlier over-commitment. The remaining risk is that two models and one background give H6 limited power, and the proposal should say what the paper concludes if H6 is inconclusive.

**R6. Eight hypotheses dilute the message.** The final version should lead with one headline hypothesis per mechanism plus the objective comparison, and list the rest as secondary.

**R7. Some sentences fall into patterns the user asked to avoid.** "The pixel tier adds realism of observation, not of physics" is the corrective antithesis the user named, and "The first result motivates the question. The second explains why..." is a pair of short pivots. A style pass is needed.

## Suggestions for version 7

1. Write a related-work section with four groups and an explicit gap statement.
2. Restructure into a main text of moderate length plus appendices.
3. Open the introduction with a concrete failure case.
4. State the interpretive limit of the pose re-analysis.
5. Say what an inconclusive H6 would mean for the paper's claim.
6. Lead with five headline hypotheses.
7. Do a style pass for antithesis, staccato pairs, triads and intensifiers.
8. Choose the title and give seven alternatives.

## Codex adversarial review

Codex returned **needs-attention** with nine high and two medium findings ([raw output](codex-adversarial/codex-review-v06.txt)). X6 is notable because it cites the user's own manuscript against the proposal: the JEPA asymmetry paper states that physical mirroring followed by projection need not reverse the response's sign.

| # | Severity | Finding | Disposition in v07 |
|---|---|---|---|
| X1 | high | A stochastic backbone lets a "unimodal" head produce multimodal, persistent marginals | **Fixed.** Output families sit on a shared *deterministic* history encoder with all sampling confined to the output module; the faithful stochastic SWAP-style model stays as a separate baseline |
| X2 | high | Width changes optimization as well as capacity | **Fixed.** Capacity competition is claimed only if the interaction survives restarts, per-condition learning-rate tuning and doubled training, *and* frozen readouts show the trade-off (asymmetry recoverability falls as distractor recoverability rises); otherwise the result is reported as width-dependent interference |
| X3 | high | A shrinking code ($z_D = r^D b$) still contains $b$; a shared decoder can fail for other reasons | **Fixed.** Probe-end recoverability is measured; shared and delay-specific readouts have matched budgets; an invertible contracting-code control checks that the metrics separate rescaling from loss; negative results are limited to the tested readout classes |
| X4 | high | H6 changes architecture and regularization along with the objective, and DCS video is smooth and predictable | **Fixed.** A shared backbone and readout in an objective × background-predictability factorial (static, smooth video, temporally white video), with each background's predictability measured at the training horizon |
| X5 | high | No pixel-conditioned Bayes reference | **Fixed.** The joint-sensor reference is labeled privileged for the camera tier; raw risk and privileged skill are reported, and no exact-information claim is made there |
| X6 | high | The user's paper says mirroring need not reverse the response sign | **Fixed.** $\Delta A$ is recomputed from projected references for every mirrored pair, the sign distribution is audited, and edit-side balance is kept distinct from response-sign balance |
| X7 | high | New readouts cannot localize the earlier failure without rescoring the original decoders on the same cases | **Fixed.** Original decoders, new readouts and zero response are scored on identical locked-cohort cases with the original study's risk definition, failure costs and weights; the binary verdict and capacity attribution are removed |
| X8 | high | The belief gives one magnitude per sign | **Fixed.** A component-conditioned log-normal magnitude with reparameterized sampling; Monte Carlo estimation within components and exact weighting across them; comparators get the same magnitude family |
| X9 | high | The walker budget cannot replicate H2–H5 at ten seeds | **Fixed.** The walker replication family is narrowed to what the budget supports (memory and the remedy comparison) at ten seeds, every fit is costed, and the camera factorial is sized to keep the total under 400 GPU-hours |
| X10 | medium | Balanced commands do not make $\sum_t d_t = 0$ under lag | **Fixed.** The statistic uses a centered regressor, $\sum_t (d_t - \bar d)F_{+,t}$, which removes the common-gain term for any probe |
| X11 | medium | "Supported" did not require the lower bound to exceed the meaningful effect | **Fixed.** Verdicts are split into direction (lower bound above zero) and magnitude (established only if the lower bound reaches $\delta$) |

**Revised score after Codex.** X1–X4 mean four mechanism tests could not have identified their mechanisms as written, X6 and X7 misread the source, and X9 broke the budget. Soundness drops from 8 to 6, experiments from 9 to 7, and feasibility from 7 to 5, giving a corrected total of **75.2**. The scorecard uses the corrected value.
