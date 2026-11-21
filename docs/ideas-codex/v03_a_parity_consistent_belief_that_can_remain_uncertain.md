# A Controlled Test of Signed Mechanical Memory in World Models

**Version 3 · Research proposal · 23 October 2026**  
**Status:** proposed work following the [version 2 review](../../output/research-codex/review-v02.md). No learned-model advantage has been measured.

## Abstract

A predictive world model may need to retain a mechanical difference long after the observations that revealed it have passed. We propose a benchmark that makes this requirement explicit and a small structured memory model to test it. Bilateral actuators first produce an informative response, then enter a period whose observations do not reveal which side is stronger. A later command tests whether the retained state supports physical prediction. The candidate stores uncertain signed context separately from changing motion, using a declared observation gate to preserve context during the uninformative interval. Reflection consistency and uncertainty are evaluated independently of this update rule. Comparisons with conventional identification and equally supervised recurrent models will determine whether the contribution is a useful memory mechanism, a training recommendation, or a diagnostic benchmark documenting where established methods already suffice.

## Motivation and twelve-week question

A world model forecasts how a system responds to inputs. In a bilateral machine, total output can conceal how force is distributed between sides. A differential command reveals that distribution; a later forecast may depend on remembering the response. This connects asymmetry to predictive sufficiency: memory is sufficient for a declared query family when access to the original history would not improve those predictions.

The supplied pose-restoration paper reports uncertain JEPA benefits and a strong zero-response baseline. The URTC draft's source-video overlap prevents an independent generalization claim. These findings justify response and provenance tests, not an assumption that JEPA or symmetry caused information loss. The proposed study begins with controlled physical histories rather than clinical classification.

**Within twelve weeks, does a structured persistent-context model achieve a confidence-supported reduction of at least 5% in delayed impulse MSE against a validation-selected recurrent comparator, with near-term RMSE deterioration below 0.02 N·s?** The query horizon is 0.5 seconds and primary neutral delay is eight seconds. Learned models receive identical observations, physical targets, query origins, loss weights, and optimization budgets. A general methods claim additionally requires an advantage in the nonlinear actuator condition; success confined to the analytical system supports a diagnostic result.

## The physical experiment and its information boundary

The analytical system has actuator states $\tau\frac{dq_L}{dt}=a+u-q_L$ and $\tau\frac{dq_R}{dt}=a-u-q_R$. Forces are $(g+b)q_L$ and $(g-b)q_R$; their sum drives a damped cart. Common command $a=0.6$ and differential command $u$ are observed. Position, velocity, and total force are measured; individual forces and gains are hidden.

After opposite diagnostic pulses, reset physical state to common position, velocity, and equal activations. Do not reset model memory or mechanics. Neutral input then produces sign-independent observations with unchanged sensors. Every model receives the reset flag and diagnostic schedule. At the forecast origin announce a half-second differential input. Its exact impulse is

$$
J = 2gaH + 2bu[H - \tau (1 - \exp (-H/\tau ))]
$$


If two equally likely histories collapse to one stored state, the minimum extra squared-error risk at the same anatomical query is one quarter of their conditional-mean separation squared. This elementary identity motivates the diagnostic; it does not prove learned collapse. Jointly reflecting body and query reverses both $b$ and $u$ and preserves total force, so that operation is distinct from the fixed-query test.

The nonlinear condition replaces activation input by the shared saturating law $\phi_\alpha(v)=\frac{\tanh(\alpha v)}{\tanh(\alpha)}$, using $\tau\frac{dq_s}{dt}=\phi_\alpha(a\pm u)-q_s$. The unknown positive saturation parameter $\alpha$ varies across bodies. Equal post-reset activations still give sign-independent neutral observations; differential responses now depend jointly on imbalance, lag, and saturation. Compute impulse by integrating this law, rather than applying the linear formula. A nonlinear parameter estimator remains mandatory. A no-reset condition tests continuous dynamics, where recent observations may suffice.

## What changes in the candidate

Delayed query rehearsal becomes a shared training protocol: with matched origins, targets, and weights, it is ordinary delayed-outcome supervision. The candidate instead changes the persistent evidence update.

Store 128 real values: 64 for changing dynamics and 64 for context evidence, each partitioned equally into even and odd channels. Even channels remain unchanged by reflection; odd channels change sign. An exact parity update evaluates a shared base function on an input and its reflection, then takes their half-sum and half-difference. This is a standard symmetry construction; both evaluations count toward compute.

The changing state updates after every real measurement. The context accumulator updates during the declared diagnostic block, using changing state and current measurement, then is copied unchanged outside that block. This publicly known gate is supplied to all models and contains no mechanical sign. It is a conventional structural assumption matched to the reset experiment's observation law, with no claim to handle unannounced fatigue. The no-reset condition compares the gate with unrestricted updates to expose this limitation.

A mixture head converts context evidence into a two-sign belief. For even evidence $e$, odd evidence $o$, and component $S\in \{-1,+1\}$, set

$P(S=s) \propto  \exp  d(e,s o)$,

$\log  R \mid  S=s\sim \mathcal{N}(\mu (e,s o), \sigma ^2(e,s o))$, and $C_{\mathrm{odd}}=s R$.

Reflection negates $o$, exchanges sign probabilities, and negates $C_{\mathrm{odd}}$ while preserving magnitude distributions. Even nuisance context may depend on the same component. Both signs can remain plausible; their average near zero is not evidence of symmetric mechanics. A latent component name acquires physical meaning only through independent evaluation.

At a query origin, draw context once, initialize the changing state conditionally on it, and retain context throughout the forecast. This allows state/context dependence. A parity-consistent decoder permits odd-context × odd-input products in even total force. Neither odd channels nor exact equivariance prevents a zero solution; the physical prediction tests establish utility. Score the complete predictive mixture under informative, noisy, and absent diagnoses using log likelihood, interval coverage, and width. No predicted observation becomes evidence for updating context.

## Comparisons that can defeat the proposal

All models optimize identical sequence and delayed-impulse likelihoods. A small factorial comparison changes context updating (ordinary recurrent update versus diagnostic-gated accumulation) and reflection structure (unconstrained versus parity-consistent). Every cell has 128 stored values, the same mixture family and decoder capacity, and matched targets. An ordinary recurrent model without the persistent partition tests the partition itself. Comparing only against single-Gaussian context would confound uncertainty capacity with the update mechanism.

Known-equation Bayesian/least-squares identification and learned full-history prediction provide information references. Their extra storage and equation knowledge are disclosed. A recent-window predictor and a neutral-history control establish whether diagnosis helps. A privileged mechanics oracle only checks a ceiling.

Frozen readouts receive stored state and announced query, with no hidden sign, reset-time label beyond model inputs, or extra observation history. Linear and two-layer nonlinear readouts fit on training families, tune on validation families, and evaluate on confirmation families. Apply the same readout classes to recent-window and full-history features. If a new readout succeeds while the installed decoder fails, the problem is decoding. If both fail, the conclusion concerns recoverability within tested classes rather than information-theoretic erasure. Delay and noise sweeps expose dependence on episode timing.

## Shape, splits, and causal training

Immutable records preserve 100 Hz timestamps, SI units, and command-side conventions. Observations are `[episode,time,3]`, commands `[episode,time,2]`, and reset/diagnostic flags and masks `[episode,time]`. The 50-step force target is `[batch,50,1]`; impulse is its physical-time integral, checked against finer integration. Padding retains slots without stretching time. This cart has no skeletal joint axis.

A family contains both imbalance signs, all continuations, query branches, reflections, and noise views of one mechanics draw. Assign families to 70/15/15 train/validation/confirmation partitions before windows. Suggested support is $g\in [0.8,1.2]\,\mathrm{N}$, $\lvert b\rvert\in [0.1,0.3]\,\mathrm{N}$, $\tau \in [0.05,0.15]\,\mathrm{s}$, $m\in [0.8,1.2] \mathrm{kg}$, and nonlinear $\alpha \in [0.5,2]$. The generation lock will declare damping, stiffness, noise, query sets, and withheld combinations. New draws within support test interpolation; held-out combinations and query extrapolation are separate.

Normalization fits only training observations and retains inverse transforms. Every input ends before its target, including filtering and interpolation. Branches clone activation, cart state, controller state, and random state; identical-input replay verifies cloning. No branch or reflection crosses partitions. Diagnostic and query schedules are known controls, whereas responses become available only after they occur. The fixed tensor layout is preserved after preparation, while normalization's numerical changes remain traceable.

## Statistical decisions and resources

Select the strongest recurrent comparator by validation impulse error before opening confirmation. The primary decision requires the upper 95% paired confidence bound on $\operatorname{MSE}_{\mathrm{candidate}}-0.95\operatorname{MSE}_{\mathrm{comparator}}$ below zero. If validation comparator RMSE is below 0.01 N·s, the task has reached a floor and no relative-improvement claim is pursued. The near-term guardrail requires the upper bound on RMSE deterioration below 0.02 N·s. These are study-design thresholds, not clinical thresholds.

Average five fitted seeds within each body family. The main interval resamples families and is conditional on those fits; report seed-level effects separately. Pilot paired variance sets confirmation size by $\left\lceil\left(\frac{1.96s}{\epsilon}\right)^2\right\rceil$, capped between 200 and 2,000 families, with $\epsilon =0.0005 (\mathrm{N\,s})^2$ for the primary contrast. If the cap cannot achieve the target precision, disclose that limitation without changing the threshold after test inspection. A later protocol revision will freeze multiplicity handling and nonlinear uncertainty scoring.

Weeks 1–2 verify laws and observability; weeks 3–5 fit identification references; weeks 6–8 perform the factorial study; weeks 9–10 run frozen confirmation; weeks 11–12 analyze and write. Human acquisition and adaptive probing are excluded. One optional contact system is considered only after core success and resource review. If ordinary identification or generic context succeeds throughout, report the boundary on special memory's usefulness.

## Related work and intended contribution

[Chirality Nets](https://arxiv.org/abs/1911.00029) and [SWAP](https://arxiv.org/abs/2606.19928) establish equivariant recurrence. [RMA](https://arxiv.org/abs/2107.04034), [VariBAD](https://arxiv.org/abs/1910.08348), and [meta-learned dynamics adaptation](https://arxiv.org/abs/1803.11347) require strong ordinary context comparisons. [V-JEPA 2](https://arxiv.org/abs/2506.09985) demonstrates action-conditioned predictive learning. [Identifiable World Models](https://arxiv.org/abs/2610.07028) and [Compact but Moving](https://arxiv.org/abs/2609.21787) constrain broad intervention-memory novelty.

The possible ICML contribution is a reproducible retention phenomenon and its limits, with a structured-update benefit only if it survives conventional alternatives. A linear cart solved by a tiny sufficient statistic is an implementation check. Richer evidence and a demonstrated failure mechanism are necessary before claiming relevance to complex world models.
