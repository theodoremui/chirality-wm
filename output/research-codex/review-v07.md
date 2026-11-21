# Independent adversarial review: version 7

**Reviewed artifact:** [v07_predictive_memory_for_asymmetric_mechanics.md](../../docs/ideas-codex/v07_predictive_memory_for_asymmetric_mechanics.md).  
**Preserved pre-review snapshot:** [v07-before-final-review.md](review-snapshots/v07-before-final-review.md).  
**Sequence:** reviewed after version 7 was saved. The initial assessment below is preserved; any final corrections will receive an appended verification note. Independent reviewer agent substitutes for the unavailable `codex:adversarial-review` capability.

## Assessment

The final proposal has a coherent argument: specify when measurements contain signed mechanical information, test whether it remains recoverable, then ask whether it improves later physical prediction. It distinguishes moving representation codes from lost information and gives stored-summary and identification baselines a real opportunity to defeat the preferred explanation. The source papers are used within their evidential limits. The contact extension is concrete and conditional, while the main study can be executed independently.

The work is now a well-specified prospective study. Its strongest unresolved risk is scientific rather than editorial: ordinary context or a copied diagnostic summary may already solve the benchmark. No amount of proposal polishing establishes a novel method or an ICML-ready result before that experiment is run.

| Dimension | Weight | Score /5 |
|---|---:|---:|
| Significance | 12% | 4.0 |
| Novelty | 18% | 2.5 |
| Conceptual/mathematical correctness | 12% | 4.5 |
| Method specificity | 12% | 4.5 |
| Identification/causal validity | 10% | 4.5 |
| Data fidelity/leakage | 10% | 5.0 |
| Experiments/baselines | 10% | 4.5 |
| Statistics/falsifiability | 8% | 4.5 |
| Feasibility | 4% | 4.5 |
| Clarity | 4% | 5.0 |
| **Weighted total** | **100%** | **83.0/100** |

**Change from version 6:** +0.4 points, reflecting clearer presentation and specific prior-work comparisons. **Empirical readiness:** no neural models or human prediction experiments have been completed. The score evaluates the design and is neither an acceptance probability nor an empirical quality score.

## Feedback from version 6

- **V6-1:** addressed: learned state restarts across independent histories, and each query branch copies origin memory without cross-branch updates.
- **V6-2:** addressed: relative knee gears, custom measurements, contact-wrench transformation, and dimension checks are explicit.
- **V6-3:** addressed: common and delay-specific probes distinguish changing codes from lost recoverability.
- **V6-4:** addressed: the related-work discussion explains what existing methods already provide and what the controlled diagnostic adds.

## Small corrections before sealing the final version

1. **V7-1 — Finish the simulator noise and state specification (Physical diagnostic; Data pipeline).** State the sensor-noise distribution and dependence, rather than only its standard deviations: for example, independent zero-mean Gaussian noise across channels/times, with model-independent paired random streams for controlled comparisons. State whether future targets are noise-free physical trajectories. Explicitly retain `k,c` and reset `x=x'=0` in the nonlinear condition, so implementation does not depend on readers inferring inheritance from the linear example.

2. **V7-2 — Close the remaining predictive-distribution and numerical locks (Candidate; Objectives; Execution).** Specify a compact default or mandatory pilot-lock fields for the dimension/distribution of even context, the conditional initial-state distribution, and the residual transition law. “May depend on the component” currently leaves materially different uncertainty models compatible with the text; all competitors must share those choices, with parity respected by means and covariances where relevant. Specify the reference sample count used to assess Monte Carlo stability, such as increasing each evaluation bank from 128 to 512 before locking a common count. Write the fit count unambiguously as `7 × (3 + 5) = 56`.

3. **V7-3 — Restore the explicit ambiguous-history uncertainty audit (Retention; Statistical decision).** Earlier versions included uncertainty checks when diagnosis is absent or too noisy; the final version currently mentions a no-diagnosis reference without saying how the candidate's uncertainty is assessed there. For the existing physically generated neutral-diagnosis control, report CRPS and predictive interval coverage/width under balanced signs, and state whether this condition is represented during training or is a labeled distribution-shift test. Do not create an inconsistent history by merely erasing a pulse while retaining its force response. This is a diagnostic check, not another confirmatory superiority claim.

## Research recommendations that remain conditional

- If generic gated memory matches the candidate, report the value of the known diagnostic protocol and avoid claiming a new equivariant memory mechanism.
- If the copied-summary baseline matches all learned variants, center the paper on the information diagnostic and the failure of unnecessary architectural complexity to improve it.
- If fixed readouts fail but delay-specific readouts succeed, report representation reorganization rather than erasure.
- If the cart succeeds but the contact gate fails, retain the narrow controlled contribution. Generality should follow evidence rather than the number of proposed applications.

The next substantive step is implementation of the generator and its information references, followed by the frozen baseline registry. The proposal should not be expanded again before those controls establish whether a meaningful learning problem remains.

## Final verification after corrections

**Verified on 23 October 2026.** I reread the corrected canonical proposal and the revision ledger. The initial review and pre-review snapshot remain available above.

| Final issue | Verification | Status |
|---|---|---|
| V7-1 | The nonlinear condition now fixes damping/stiffness and zero cart position/velocity at initialization/reset. The data contract specifies independent uniform parameter draws, Gaussian sensor errors independent across time/channels, paired random streams, and noise-free physical targets. | Closed |
| V7-2 | The model now specifies four even diagonal-Gaussian context coordinates, a 64-dimensional conditional initial-state Gaussian, shared sampling dimensions, parity mean/variance rules, and deterministic latent transitions. Evaluation compares 128 with 512 samples per bank. The fit count is explicitly `7 × (3 + 5) = 56`. | Closed |
| V7-3 | Neutral diagnoses are physically regenerated and represented in 20% of training histories; pulse diagnoses alone determine primary selection/testing. The balanced-sign control reports CRPS, 90% coverage, and interval width. Triple-noise diagnosis is a separately labeled shift test. | Closed |

**Final design score: 83.0/100, unchanged.** These corrections remove implementation ambiguities rather than supplying stronger empirical evidence. All requested documentation/design corrections in the seven-review cycle have been addressed or explicitly bounded in the revision ledger. The remaining questions—whether ordinary summaries suffice, whether parity helps, and whether contact replication is feasible—require the proposed experiments.

Reviewed canonical V7 SHA-256: `53140ea27f723743667a8281cbfb722012ad783e5de0cd4696a6ea7d2ee9126a`.

Preserved pre-review snapshot SHA-256: `bf95910329bd0b6db09f6f956083f1856deaa54395e78dae09f9575722cb93db`.
