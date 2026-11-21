# Remembering Mechanical Asymmetry After the Evidence Has Passed

**Version 2 · Research proposal · 23 October 2026**  
**Status:** proposed experiments; no new learned-model or human results. This version follows the independent [version 1 review](../../../output/research-codex/review-v01.md).

## Abstract

World models use past observations to predict physical responses to future inputs. Their memory matters when an earlier interaction reveals a mechanical difference that current measurements no longer expose. We propose a controlled bilateral dynamics study that separates this situation from ordinary sensor uncertainty. A brief diagnostic input reveals which actuator is stronger; a documented reset then removes its effects on the current physical state while preserving the body's mechanics. Models must use the earlier evidence to predict a later input. The study compares ordinary identification, recurrent prediction, and training on delayed response queries under the same data budget. A companion condition retains continuous dynamics to test whether the phenomenon survives beyond the diagnostic construction. The intended result is a precise account of when compressed predictive states retain useful signed information and when simpler identification already solves the problem.

## Motivation and research question

Suppose two motors move the same cart. Their combined force can remain unchanged when strength shifts from the left motor to the right. A command that increases one motor while decreasing the other exposes that difference. A world model is useful because a controller eventually needs a prediction for a new command, possibly long after the exposing interaction. Accurate prediction during intervening neutral motion may place little demand on remembering the stronger side.

The supplied JEPA study restores observed pose windows and finds uncertain benefits from paired-feature objectives. The URTC study's classification split shares source videos across training and testing. Neither establishes a loss of mechanical information caused by equivariance. Their relevant lessons concern fair supervision, anatomical indexing, and independent evaluation; the [source audit](../../../output/research-codex/source-evidence-audit.md) records these boundaries.

**Within twelve weeks, can delayed-query training reduce body-averaged squared error in half-second total-force impulse by at least 5% relative to the strongest selected recurrent comparator, after an eight-second neutral delay, without worsening near-term impulse RMSE by more than 0.02 N·s?** The comparator receives identical histories and delayed targets. The 5% threshold is a proposed practical criterion, to be frozen with the pilot protocol before confirmation; it is not an expected result. The primary population is independently generated bilateral body families within the declared parameter support. Continuous-dynamics and shifted-support tests are secondary.

## Establishing what the history can reveal

The first environment is a cart driven by two first-order actuators. Their activation states satisfy

$$
\begin{aligned}\tau\dot q_L&=a+u-q_L, \\ \tau\dot q_R&=a-u-q_R.\end{aligned}
$$

and their forces are $F_L=(g+b)q_L$, $F_R=(g-b)q_R$, with $g>|b|$. The cart obeys $m\ddot x=F_L+F_R-kx-c\dot x$. Here $b$ is signed gain imbalance, $g$ is common gain, $a$ is a common command, and $u$ is a known differential command. Observations are position, velocity, and noisy total force. Individual forces and mechanics remain hidden from evaluated models.

A diagnostic block applies two opposite differential pulses. The physical state is then set to $x=\dot x=0$ and $q_L=q_R=a$, without changing mechanics. The reset flag is visible to every model; recurrent memory is retained. During the neutral delay, $u=0$, both activations remain equal, and total force is $2ga$, independent of the sign of $b$. Matched bodies with identical other parameters therefore have the same delay-observation distribution under both signs. The same sensor channels operate throughout, avoiding a new sensor-missingness regime.

At the forecast origin, a constant query $u_*$ is announced for horizon $H=0.5$ seconds. The target is the physical impulse

$$
\begin{aligned}
J&=\int_0^H(F_L(s)+F_R(s))\,ds\\
&=2gaH+2bu_*[H-\tau(1-e^{-H/\tau})].
\end{aligned}
$$

This identity provides an exact simulator check. The later query is fixed in anatomical coordinates when comparing the two signs. Reflecting both body and query would preserve the total-force outcome and answer a different question.

If two equally likely diagnostic histories are compressed to the same memory and have conditional query means $m_+$ and $m_-$, their best shared squared-error prediction is the midpoint. Its excess risk over the separate means is $(m_+-m_-)^2/4$. Outcome noise adds the same irreducible variance to both risks. This elementary identity explains why collapsing useful history can matter; it does not prove that a trained network collapses or that a human gait contains the required information. The [analytical checks](../../../output/research-codex/checks/README.md) verify the simpler force identities and this risk calculation.

A second condition omits the reset. Residual motion can then reveal mechanics, so it is analyzed separately. If a recent-window estimator succeeds there, memory is less necessary in that condition. This limits the phenomenon rather than invalidating the estimator.

## Learning intervention and uncertainty

A recurrent model updates fixed-width memory $h_t$ from observations, past commands, timestamps, and the reset flag. Context inferred from this memory is held fixed throughout one predicted future. A decoder receives memory and the future query schedule, then predicts the force trajectory and impulse distribution. Predicted observations do not count as new context evidence.

The candidate training change is **delayed query rehearsal**: at post-diagnostic origins, reuse the retained memory to predict several saved future schedules branched from the same physical state. Its objective is

$$
L=L_{\mathrm{sequence}}+
\lambda\,\mathbb E_{t,Q}[-\log p_\theta(J_{t,Q}\mid h_t,Q)],
$$

where $Q$ is a schedule known at that origin. The first term predicts physical sequences; the second scores delayed outcomes. All methods receive the same branches and targets. Ordinary recurrence trained on identical delayed endpoints is decisive. A benefit that disappears after matching endpoint weights or training horizon supports a training-distribution explanation rather than a new representation principle.

A two-component Gaussian mixture over signed context can retain unresolved alternatives. Reflection exchanges the components and negates odd coordinates. A mixture mean near zero does not establish symmetric mechanics. Predictive log score, interval coverage, and ambiguous-history controls evaluate uncertainty. The latent coordinates remain predictive variables unless independent checks connect them to physical gains.

## Data contract and leakage prevention

Generate immutable records at 100 Hz in SI units. Observations have shape `[episode,time,3]` for position, velocity, and total force; commands have `[episode,time,2]` for common and differential input. Reset flags, timestamps, and masks use the same time index. This cart system has no skeletal joint axis; a later skeleton extension must declare its own schema.

A body family groups a sampled parameter tuple, both imbalance signs, all branches, and all sensor-noise views. Split families 70/15/15 into training, validation, and locked confirmation before windows or reflected copies. Initial support uses $g\in [0.8,1.2]\,\mathrm{N}$, $\lvert b\rvert\in [0.1,0.3]\,\mathrm{N}$, $\tau \in [0.05,0.15]\,\mathrm{s}$, and $m\in [0.8,1.2] \mathrm{kg}$, with $a=0.6$ and $\lvert u\rvert\le 0.25$. Damping and stiffness are recorded. The pilot will fix their ranges, sensor noise, family count, and support-shift cells before confirmation generation.

New draws within these intervals test interpolation to independent bodies. A separate test withholds a predeclared combination of imbalance magnitude and activation time constant while retaining their marginal ranges in training. Query extrapolation is separate from body interpolation. A new seed or numerically distinct tuple alone does not establish extrapolation.

Windowing preserves the physical sampling interval. Batches pad shorter histories and use masks; they do not stretch time. Training-derived normalization uses a common rule for bilateral quantities, with raw targets retained in SI units. At each origin, the input ends before any query outcome. Target trajectories have `[batch,50,1]` total-force values; impulse uses the documented horizon integral. Masks never delete or reorder slots. Derived windows inherit source-family identifiers. Exact array shape is preserved after preparation, while numerical normalization is explicitly recorded as a change of coordinates.

## Comparisons, inference, and failure criteria

The observability audit comes first: compare full-history identification, recent-window identification, and histories with diagnosis replaced by neutral input. A Bayesian or least-squares actuator estimator uses the same records and known equations. Full-history storage is an information reference, with its extra memory reported. A privileged mechanics oracle checks only the simulator ceiling.

Learned comparisons include generic recurrence, ordinary persistent context, reflection-consistent context, and each architecture with matched delayed endpoints. An invariant representation is a diagnostic negative control. Frozen linear and nonlinear probes test recoverability from memory. Failure of the model's decoder alone does not demonstrate erased information; failure of finite probe classes cannot establish information-theoretic absence.

The primary endpoint is squared impulse error scaled by $(1 \mathrm{N\,s})^2$, averaged over queries and signs within families, then over families. Report the paired candidate-minus-comparator difference and relative reduction. Use five training seeds, paired family bootstrap intervals conditional on those fits, and a separate seed-sensitivity display. Proper predictive log score and coverage remain required. The pilot estimates between-family paired variance and sets a confirmation count for a prespecified precision target. The lockbox opens once after methods and thresholds freeze.

The claim fails if diagnosis does not help the information reference, if a recent window suffices in the declared memory condition, if ordinary context matches rehearsal, or if gains require extra targets or input access. A successful diagnostic construction alone does not establish gait mechanics.

## Related work and schedule

[Chirality Nets](https://arxiv.org/abs/1911.00029) and [SWAP](https://arxiv.org/abs/2606.19928) already provide reflection-consistent recurrence. [RMA](https://arxiv.org/abs/2107.04034) and [VariBAD](https://arxiv.org/abs/1910.08348) establish history-based context inference. [V-JEPA 2](https://arxiv.org/abs/2506.09985) supplies action-conditioned learning, while [Identifiable World Models](https://arxiv.org/abs/2610.07028) and [Compact but Moving](https://arxiv.org/abs/2609.21787) constrain broad intervention-memory claims. The distinction proposed here is a controlled observability-versus-retention test and any delayed-training benefit that survives conventional alternatives.

Weeks 1–2 verify equations, resets, and observability; weeks 3–5 fit identification and recurrent controls; weeks 6–8 compare objectives; weeks 9–10 run frozen confirmation; weeks 11–12 analyze and write. One optional contact system can test transfer if the core comparison survives. Human archives remain outside the central causal claim, and no clinical effectiveness claim is planned.
