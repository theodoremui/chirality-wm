# Revision ledger

Seven successive proposals develop one study. Each new version was authored after the preceding independent review was saved and read. Earlier proposal versions remain intact. Review provenance and the common scoring rubric are in [review-protocol.md](review-protocol.md). The named `codex:adversarial-review` capability was unavailable; independent Codex reviewer agents performed the reviews. This ledger records intellectual decisions, not completed experiments.

## Original → version 1

| Issue | Decision | Where and why |
|---|---|---|
| O1: distinguish a learning claim from ordinary context inference | Accepted as direction; still open after v1 | V1 Research question and Method center delayed mechanical memory; V2 Learning intervention writes a concrete delayed-query objective. Equivariance and persistence alone are retained as established tools. |
| O2: one confirmatory experiment | Accepted | V1 Method and Scope use simulation as the core; human datasets become optional external work. V2 defines the bilateral cart and impulse endpoint. |
| O3: estimand and inference | Accepted progressively | V1 Comparisons establishes body-level averaging; V2 Research question and Comparisons specify impulse, delay, relative improvement, seeds, and pilot-based sizing. Later reviews tighten the decision rule. |
| O4: proportionate narrative | Accepted | V1 Motivation removes extended chemistry framing and accurately characterizes both supplied studies. V2 treats the parity/risk algebra as a diagnostic, not a major theorem. |

## Version 1 → version 2

| Issue | Decision | Where and why |
|---|---|---|
| V1-1: forgetting versus changed observability | Accepted | V2 Establishing what the history can reveal introduces a physical-state reset with unchanged sensors, sign-independent neutral delay, and a separate continuous-dynamics condition. Comparisons adds full-history, recent-window, and no-diagnosis controls. |
| V1-2: specify the learning intervention | Accepted, novelty deliberately conditional | V2 Learning intervention defines delayed query rehearsal and its objective; identical delayed-endpoint recurrence can defeat the method claim. Further implementation detail is the next review's focus. |
| V1-3: target and inferential population | Accepted with pilot-dependent quantities disclosed | V2 RQ and Comparisons choose half-second impulse, eight-second delay, 5% practical reduction, 0.02 N·s guardrail, body-family averaging, and seed treatment. Counts and precision targets await explicit operationalization. |
| V1-4: unresolved laterality | Accepted | V2 Learning intervention uses a two-component context mixture and proper predictive scoring, without equating the latent mean with true mechanics. |
| V1-5: reproducible split/support | Accepted in part; expanded next | V2 Data contract specifies body-family grouping, continuous parameter ranges, interpolation versus held-out combinations, and separate query extrapolation. Damping/stiffness/noise and exact holdout cells remain pilot decisions and are labeled as such. |

## Evidence retained throughout

The supplied restoration and classification papers motivate controls; their findings are not recast as successful world-model results. Identifiability, memory recoverability, useful prediction, and human relevance remain separate claims. Analytical checks validate equations only. A failure of an installed decoder is not proof that information has vanished from memory; probe findings are qualified by their tested function classes.

## Version 2 → version 3

| Issue | Decision | Where and why |
|---|---|---|
| V2-1: identical rehearsal and baseline objectives | Accepted; method claim narrowed | V3 What changes in the candidate explicitly makes delayed-query supervision shared. The tested intervention is gated accumulation versus ordinary context updating, with a reflection factorial. Rehearsal is not claimed as a new loss. |
| V2-2: equivariant belief update and matched mixture | Accepted | V3 specifies stored channels, parity construction, diagnostic gate, two-sign mixture weights/magnitudes, context sampling once per rollout, and a generic context comparator with the same mixture. |
| V2-3: executable confirmation rule | Accepted with remaining protocol work disclosed | V3 Statistical decisions requires a confidence bound for 5% improvement, defines a near-term bound and error floor, selects the comparator on validation, and gives a capped precision-based sizing rule. Multiplicity is explicitly left for later refinement. |
| V2-4: broader evidence | Modified | V3 adds unknown shared actuator saturation as the required nonlinear condition and separates continuous dynamics. It avoids guaranteeing generality from a contact simulator that has not been built; broad world-model relevance remains conditional. |
| V2-5: restricted memory readout audit | Accepted | V3 Comparisons fixes readout inputs to stored state plus query, uses train/validation/confirmation families, matches readout classes, and qualifies conclusions as recoverability rather than erasure. |

## Version 3 → version 4

| Issue | Decision | Where and why |
|---|---|---|
| V3-1: gate may merely copy a summary | Accepted | V4 Comparators adds a 128-value diagnostic snapshot, a 64-snapshot/64-dynamic variant, and fitted-parameter summary. General world-model claims are withheld without structurally different dynamics. |
| V3-2: nuisance learning during neutral delay | Accepted; mathematical claim narrowed | V4 Physical systems fixes and discloses nuisance values in the exact diagnostic. Unknown nonlinear nuisances remain a separate condition with an all-observations Bayesian reference; the gate is explicitly approximate there. |
| V3-3: incoherent trajectory and impulse distributions | Accepted | V4 Memory/training integrates each sampled force trajectory to obtain impulse; CRPS replaces unspecified marginal likelihood. The combined loss is described as a dependent composite score. |
| V3-4: precision relative to actual target effect | Accepted | V4 Inference sets half-width to one quarter of the 5% pilot effect, retains a sample cap and floor fallback, and identifies one combined nonlinear primary claim. Shift/architecture contrasts remain exploratory. |
| V3-5: preprocessing and temporal reflection | Accepted | V4 Data contract defines maps, odd zero centering, compatible scales, involution checks, origin timing, interval-average target forces, and exact impulse aggregation. |

## Version 4 → version 5

| Issue | Decision | Where and why |
|---|---|---|
| V4-1: actual gradient/scoring path | Accepted | V5 Actual gradient/scoring paths specifies energy score + CRPS, fixed physical scales, independent stratified sample banks, mixture-weight gradients, full-history BPTT, no future-observation teacher forcing, and gradient/compute logs. |
| V4-2: comparator registry and fairness | Accepted | V5 table freezes B1–B6 and validation-only selection; information references are distinguished. Active parameter counts are approximately matched, stored values fixed, and additional parity computation disclosed rather than silently called matched compute. |
| V4-3: prediction versus retention | Accepted | V5 Retention uses one locked readout across diagnosis end and 1/4/8-second memories, predicting the same canonical-reset response, with restricted inputs and history controls. Primary MSE is explicitly a predictive result. |
| V4-4: temporal schedule generalization | Accepted | V5 adds untouched switched-order queries using training-supported amplitudes, separately from magnitude extrapolation. The switch protocol is secondary and cannot select models. |

## Version 5 → version 6

| Issue | Decision | Where and why |
|---|---|---|
| V5-1: fitting allocation and initial state | Accepted | V6 Data contract makes linear/nonlinear companions a balanced training population with an even regime flag, grouped by family. The 56-fit registry covers both regimes. Physical systems sets pre-diagnosis and post-reset states. |
| V5-2: complete primary inference | Accepted | V6 Locked inference defines predictive means, query/sign/noise/seed averages, zero-delay half-second near-term guardrail, 10,000 one-sided paired family-bootstrap draws, recomputed RMSE, intersection-union decision, and validation-selected comparator scope. |
| V5-3: resource/failure lock | Accepted | V6 gives AdamW, learning-rate candidates, batch/update counts, pilot/training/validation counts, fresh final seeds, Monte Carlo stability criterion, and mandatory lock fields. Invalid source families are rejected before fitting; model failures veto the claim rather than being removed. Budget shortfall requires a pre-confirmation revision. |

V6 also makes the generality path concrete: a separately gated planar contact-walker replication with restricted model count and prospective open-loop inputs. It is a proposed test, not evidence already obtained. If the gate fails, broader dynamics-method language is removed.

## Version 6 → version 7

| Issue | Decision | Where and why |
|---|---|---|
| V6-1: reset learned state between independent histories | Accepted | V7 Causal pipeline explicitly restarts priors/memory between episodes, signs, regimes, and noise replicas; only within-history physical resets preserve memory. Each query copies origin memory and cannot consume another branch's response. |
| V6-2: walker relative gains and custom channels | Accepted | V7 Generality test multiplies nominal knee gear 50 by 1±b, preserves other motors, labels the 18/19-channel arrays custom instrumentation, and specifies world-frame ground-on-foot extraction and interval averaging. |
| V6-3: moving codes versus lost information | Accepted | V7 Retention adds matched delay-specific readouts alongside common readouts, with partition discipline and extra parameters disclosed. Successful delay-specific decoding leads to a changing-code interpretation. |
| V6-4: nearest-work distinctions | Accepted | V7 Related work explains what reflection recurrence, context adaptation, ConDA, and Compact but Moving already establish, and defines the narrower contribution of the observation/reset diagnostic. |

The first complete V7 text was preserved before its final independent review at [review-snapshots/v07-before-final-review.md](review-snapshots/v07-before-final-review.md). Any final corrections to canonical V7 will be recorded below; the reviewed pre-correction text remains available. Earlier V1–V6 proposals are unchanged.

## Final V7 review and corrections

| Issue | Decision | Final location and change |
|---|---|---|
| V7-1: sensor-noise law and nonlinear initial/reset state | Accepted | Physical diagnostic explicitly retains nonlinear `k,c` and zero cart position/velocity at both boundaries. Data pipeline states independent uniform parameter draws, Gaussian sensor noise with paired random streams, and noise-free physical targets. |
| V7-2: predictive distribution and numerical locks | Accepted | Candidate fixes four even diagonal-Gaussian context coordinates, a 64-dimensional conditional initial-state Gaussian, deterministic latent transitions, and parity-specific mean/variance rules. Generic competitors share distributions without symmetry tying. Evaluation compares 128 versus 512 samples per bank; fit count is explicitly `7 × (3 + 5) = 56`. |
| V7-3: ambiguous-history uncertainty | Accepted | Retention section adds physically generated neutral diagnosis in 20% of training histories, separate pulse-only primary selection/testing, balanced-sign CRPS/90% coverage/width, and a labeled triple-noise shift test. It forbids erasing inputs while retaining their responses and separates proper scoring from calibration. |

The final correction also adds the primary proper-scoring-rule reference supplied and verified by the root researcher. The initial V7 snapshot remains unchanged. These changes refine the protocol; they do not supply empirical evidence. Final independent verification is appended to [review-v07.md](review-v07.md).

## Deliberate boundaries after all reviews

- The gated update and symmetry ingredients are established. A novel general-purpose method is not claimed without superiority beyond matched stored-summary and ordinary-context controls.
- Cart-only evidence supports a controlled memory/identification contribution. The contact replication is a gated path toward broader relevance and may fail feasibility or observability checks.
- A failure of fixed readouts can reflect changing codes. Even matched nonlinear and delay-specific failures establish limited recoverability, not a proof of information erasure.
- Proper predictive scores, calibration checks, physical errors, and recoverability curves answer different questions; no favorable metric substitutes for the others.
- Scores assess prospective design. The original source audit's 64.2/100 uses a separate rubric; longitudinal comparisons use the common reviewer rubric, beginning at 66.6/100.

## Sealed review outcome

The independent reviewer reread corrected canonical V7 and appended final verification to `review-v07.md`: V7-1, V7-2, and V7-3 are closed, with the design score retained at **83.0/100**. No additional documentation correction remains open. Canonical V7 SHA-256 is `53140ea27f723743667a8281cbfb722012ad783e5de0cd4696a6ea7d2ee9126a`; the preserved pre-review snapshot is `bf95910329bd0b6db09f6f956083f1856deaa54395e78dae09f9575722cb93db`. Scientific efficacy, novelty beyond existing methods, and external generality remain empirical questions rather than unfinished writing tasks.


## Presentation repair — 23 October 2026

After the folders were renamed to `ideas-codex` and `research-codex`, stale relative links prevented the pipeline figure and supporting documents from opening. The seven canonical versions now use the current paths, Markdown-compatible PNG previews, and consistent mathematical markup. The original SVG remains available and is embedded as vector artwork in the new HTML/PDF reading editions. Table syntax, long equations, and time-index subscripts were checked during rendering.

These changes preserve the revision-specific research designs and scores. The sealed-review SHA-256 above identifies the pre-formatting text; current source hashes appear in [artifact validation](artifact-validation.json) and the [render audit](rendering/render-audit.json). The complete [pre-repair archive](rendering/pre-rendering-repair.tar.gz) preserves the files before these presentation changes. The historical review snapshot remains byte-for-byte unchanged. See the [rendering report](rendering/README.md) for formats, verification, and reproduction.
