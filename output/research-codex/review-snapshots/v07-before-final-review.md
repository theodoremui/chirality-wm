# Predictive Memory for Asymmetric Mechanics

**Version 7 · Final research proposal · 23 October 2026**  
**Status:** a prospective twelve-week study, revised after the independent [version 6 review](../../output/research-claude/review-v06.md). No new neural-training or human-data result is claimed.

## Abstract

Similar motion can arise from different left–right mechanics, yet those differences can matter when a later input changes. A world model must preserve earlier evidence when current measurements no longer reveal the distinction needed for prediction. We propose a controlled benchmark that separates information availability, its recoverability from learned memory, and its usefulness for forecasting physical responses. A bilateral actuator experiment provides an exact diagnostic, while uncertain nonlinear mechanics and a conditional contact-system replication test its limits. A small persistent-context model is compared with ordinary recurrence, stored diagnostic summaries, and conventional identification under explicit information and resource budgets. The intended contribution is an auditable account of when asymmetric mechanical information remains useful, how predictive training preserves it, and when established estimators already provide a sufficient solution.

## Motivation and the research question

Two actuators can move a cart similarly while contributing different forces. An input that increases one actuator and decreases the other reveals their imbalance. Later, a controller may need to predict a different command after the revealing measurements have passed. A sign classifier only identifies a side; a world model predicts the response to a specified input sequence and expresses uncertainty when the available history leaves alternatives unresolved.

The supplied JEPA paper restores observed pose windows, with uncertain incremental benefits and a strong zero-response control. The URTC draft explicitly reports overlapping source videos between training and testing. These studies motivate separate checks of geometry, anatomy, supervision, and provenance; they do not establish that JEPA or equivariance erased mechanics. Their evidence is documented in the [source audit](../../output/research-claude/source-evidence-audit.md).

**Within twelve weeks, can persistent context reduce mean squared error in delayed nonlinear force impulse by a confidence-supported 5% against a validation-selected strong memory baseline, while meeting near-term and uncertainty guardrails?** Impulse means force accumulated over time. The forecast lasts half a second after an eight-second delay. A broader learning-method claim requires supporting evidence from a structurally different contact system; a cart-only finding remains a controlled diagnostic result.

## Relation to established work

[Chirality Nets](https://arxiv.org/abs/1911.00029) already provides anatomical reflection-consistent recurrence and pose prediction, while [SWAP](https://arxiv.org/abs/2606.19928) extends equivariant recurrent world modeling to robot locomotion. Equivariance means that transforming the complete input transforms predictions consistently; it does not require an asymmetric body to become symmetric. Explicit even/odd channels and recurrence are therefore established ingredients.

[RMA](https://arxiv.org/abs/2107.04034) and [VariBAD](https://arxiv.org/abs/1910.08348) infer hidden context from interaction histories. Storing a diagnostic summary and maintaining uncertainty have strong precedents. [V-JEPA 2](https://arxiv.org/abs/2506.09985) also demonstrates action-conditioned predictive learning, so the contribution cannot be “adding actions to JEPA.”

[Identifiable World Models](https://arxiv.org/abs/2610.07028) studies recoverable coordinates and intervention responses using pretrained representations under explicit assumptions. [Compact but Moving](https://arxiv.org/abs/2609.21787) studies how intervention-relevant directions change through recurrent states. Our proposed diagnostic supplies a known observation law and a fixed physical query, allowing availability, moving representation codes, and delayed usefulness to be tested separately. Gated copying remains conventional; any methodological novelty must come from evidence that survives these alternatives.

## Physical diagnostic and nonlinear extension

A cart follows `m x''=F_L+F_R−kx−cx'`. Actuator states satisfy `τ q'_L=φ(a+u)−q_L` and `τ q'_R=φ(a−u)−q_R`, with `F_L=(g+b)q_L` and `F_R=(g−b)q_R`. Common command `a=0.6` is fixed; signed command `u` changes the two sides oppositely. Reflection exchanges sides and negates `b,u`, while forward position, velocity, and total force remain unchanged. This sign behavior is called parity.

The exact diagnostic fixes known `g=1 N`, `τ=0.1 s`, `m=1 kg`, `k=2 N/m`, `c=0.4 N·s/m`, and `φ(v)=v`; only `b` is unknown. Begin diagnosis at `x=x'=0,q_L=q_R=a`. After diagnostic pulses, reset this physical state while retaining mechanics and within-episode model memory. Neutral input then has an observation distribution independent of `b`, including after nuisance uncertainty is considered because those nuisance values are known. A constant later input has impulse

`J=2gaH+2bu[H−τ(1−exp(−H/τ))]`.

Two equally likely histories compressed to identical memory incur minimum excess squared error `(m_+−m_−)²/4` when their means differ at the **same** future query. Jointly reflecting body and query answers a different question. This elementary identity diagnoses the cost of a collapsed distinction; it does not prove learned collapse. See the [mathematical notes](../../output/research-claude/mathematical-notes.md).

The nonlinear condition uses `φ_α(v)=tanh(αv)/tanh(α)` and unknown `g,τ,α,m`. Initial and reset activation is `φ_α(a)`. Neutral observations remain sign-independent at fixed nuisances but can refine nuisance uncertainty and thereby improve the imbalance posterior. An all-observations identifier checks this; freezing context may discard useful evidence. A separate continuous, no-reset condition tests how current motion changes the memory requirement.

## Causal data and training pipeline

![Training and evaluation pipeline](../../output/research-claude/figures/training-pipeline.svg)

*Split source families before derived records, retain time and channel identity, and reserve confirmation targets for scoring. The concrete cart and walker shapes are specified here.*

Use immutable 100 Hz records with 0.001-second simulator steps and a step-halving check. Diagnosis lasts two seconds: eight 0.25-second differential-input blocks `[+0.10,0,−0.10,0,+0.25,0,−0.25,0]`, optionally sign-reversed independently of body sign. Delays are 0, 1, 4, or 8 seconds. Forecast queries are constant inputs from `{−0.25,−0.10,+0.10,+0.25}`, announced at the origin.

| Quantity | Nonlinear support or record |
|---|---|
| Common gain; imbalance magnitude | `g∈[0.8,1.2] N`; `|b|∈[0.1,0.3] N` |
| Activation lag; mass; saturation | `τ∈[0.05,0.15] s`; `m∈[0.8,1.2] kg`; `α∈[0.5,2]` |
| Observations | `(x,x',F_total)`, `[episode,time,3]` |
| Commands | `(a,u)`, `[episode,time,2]` |
| Sensor-noise standard deviations | `0.001 m`, `0.01 m/s`, `0.03 N` |
| Forecast target | `[batch,50,3]`: interval-end position/velocity and interval-average force |

Each family groups both imbalance signs, a fixed-nuisance linear companion, its nonlinear companion, and all branches/noise replicas. Use 200 separate pilot, 4,200 training, 900 validation, and 200–2,000 pilot-sized confirmation families. Assign families before windows; companions train in an equal mixture with an even regime flag revealing no hidden gain. Withhold the joint corner `|b|>0.25 N, τ>0.125 s` from training/validation for a separate support-shift test. Interpolation confirmation excludes that corner. Changing amplitudes or temporal schedules are separate tests.

At time `t_k`, observe `y_k`, then apply the command over `[t_k,t_{k+1})`. Inputs contain observations through `t_k`, past commands, flags, timestamps, and masks; the announced future schedule is separate. Filters use only available history. Targets integrate force within each interval: `J=0.01ΣF_average`. Averaging preserves interval impulse while removing within-interval detail; instantaneous raw measurements remain unchanged. Padding retains slots and timing instead of stretching trajectories.

Normalization fits training data only and must commute with reflection: odd channels have zero center, paired channels compatible scales, and even channels may use training means. Record inverse transforms, units, simulator versions, hashes, and split manifests. Check reflection involution, transformed predictions, complete-state cloning, and identical-input replay.

Restart learned memory and context priors between independent episodes, signs, regimes, and noise replicas. The physical reset preserves memory only within its own history. Every query branch copies the same origin memory; neither another branch's target nor its simulated response updates that memory. These rules prevent paired data from becoming hidden information transfer.

## Candidate, objectives, and strong alternatives

The candidate stores 64 changing-state and 64 context-evidence values, each with even/odd partitions. A shared update evaluated on original and reflected inputs produces parity-consistent half-sums and half-differences. Changing state uses every observation; context accumulates during the public diagnosis gate and is copied afterward. All models receive that gate. Its nonlinear limitations remain part of the test.

For evidence `(e,o)`, define `P(S=s)∝exp d(e,s o)`, `log R|S=s ~ Normal(μ(e,s o),σ²(e,s o))`, and odd context `sR`. Reflection exchanges the two sign components while preserving magnitude distributions. Even nuisance context may depend on the component. Draw context once per forecast, initialize changing state conditionally, and retain context during rollout. Odd-by-odd interactions allow signed mechanics to affect even total force. Latent names are not evidence of physical identification.

Every sample predicts the complete trajectory and obtains impulse by integration, without a separate impulse head. Train with trajectory energy score, impulse CRPS, and a one-step history score, each weighted one. Energy score compares full trajectory samples with outcomes and with one another; CRPS makes the corresponding scalar comparison and rewards accurate uncertainty without needless spread. Fixed scales are `(1 m,1 m/s,1 N)` and `1 N·s`, with trajectory distance divided by `sqrt(150)`. This composite reweights related outcomes rather than adding information.

Two independent training banks each contain four continuous samples per sign, with explicit mixture weights and cross-bank pair distances; continuous samples are reparameterized for gradients. Evaluation uses two 128-sample banks. Their weighted mean supplies point predictions. Increase samples before locking if validation risk changes by more than 10% of the intended gain or comparator selection changes. Backpropagate through the complete diagnosis and delay, with future targets confined to losses. Record gradient norms, clipping, runtime, and transient memory.

The locked competitors are ordinary 128-state recurrence; generic and parity-consistent 64+64 contexts updated continuously; generic gated context; a stored 128-value diagnostic summary; and a 64-value summary plus 64 changing values. All share mixtures, targets, current-origin observations, and query inputs. Match useful parameter counts within 10%, disclose residual differences, and select B by validation nonlinear impulse error with fixed-order tie breaking. Persistent storage is 128 float32 values; parity's extra evaluations mean this is not a claim of equal computation. Full-history prediction, recent-window prediction, equation-aware identification, fitted-parameter summaries, and privileged oracles are separately labeled information references.

## What would establish retention

Measure recoverability at diagnosis end and after 1, 4, and 8 seconds. Frozen readouts receive memory and query and predict the same canonical-reset impulse at each delay. Fit a common linear/nonlinear readout and matched delay-specific readouts on training families; tune only on validation and disclose their extra parameters. If delay-specific decoding succeeds while common decoding fails, describe a changing code rather than lost information. Failed tested readouts cannot prove information-theoretic erasure. Full-history, recent-window, and no-diagnosis controls must support the memory interpretation; primary prediction improvement alone is insufficient.

Secondary forecast schedules switch `+0.25` to `−0.25` or reverse order halfway through the horizon. They remain untouched by training and tuning, although diagnostic histories contain switching inputs. Separate these temporal-composition findings from magnitude-0.35 extrapolation, parameter-support shift, and the no-reset condition. Zero impulse-weight and truncated-gradient ablations test optimization explanations; truncated models cannot serve as the primary comparator.

## Statistical decision and execution gates

Within each confirmation family, average error over four queries, both signs, four independent sensor-noise histories, and final training seeds 17, 29, 43, 61, and 89. The point estimate is the predictive mean; MSE is its mean squared error against physical impulse. “Near-term” means the same half-second query at zero delay after reset.

Use 10,000 paired family-bootstrap draws, seed 20261023, preserving all repeated observations and method pairing. Recompute risks and RMSE within each draw. One-sided 95% upper bounds must satisfy all three conditions: `R_C−0.95R_B<0`, zero-delay RMSE deterioration `<0.02 N·s`, and CRPS deterioration `<0.01 N·s`. This intersection-union decision supports one combined claim against validation-selected B, which need not be test-best. Exploratory contrasts have no confirmatory guarantee. Intervals condition on five fitted seeds; show seed-specific effects separately.

Pilot risk sets improvement margin `δ=0.05R_B` and precision target `δ/4`. Use paired pilot variance to size 200–2,000 families, starting from `ceil((1.645s_D/(δ/4))²)` and checking by resampling; guardrail precision targets are one quarter of their margins, with the largest required cohort retained. Insufficient precision at the cap or validation comparator RMSE below 0.01 N·s leads to limited-evidence or floor reporting. Thresholds never change after confirmation.

Use AdamW, batch 16, 10,000 updates, weight decay `10⁻⁴`, and learning-rate candidates `{10⁻⁴,3×10⁻⁴,10⁻³}` with tuning seed 5. Seven methods × three tuning fits plus five final fits gives 56 fits across both regimes. Pilot profiling must fit these within 80 accelerator-hours, reserving 20 for controls and 20 for replication. A resource shortfall requires a documented protocol revision before confirmation, not dropped competitors.

Freeze manifests, hyperparameters, samples, tolerances, and analysis hashes. Reject invalid simulator families using method-independent checks before fitting and record replacements. Crashed final fits or nonfinite forecasts veto superiority rather than disappearing from averages; finite poor forecasts remain included. Model-dependent fixes require an amended protocol and fresh confirmation data. Weeks 1–2 establish validity and resources; weeks 3–5 establish references; weeks 6–8 train; weeks 9–10 confirm once; weeks 11–12 analyze and write.

## Conditional generality test and publication boundary

A broader claim requires a gated replication on the [dm_control planar walker](https://github.com/google-deepmind/dm_control/blob/main/dm_control/suite/walker.py). Pin its release; preserve its [six nominal motors](https://github.com/google-deepmind/dm_control/blob/main/dm_control/suite/walker.xml), multiplying knee gears by `1±b`, hence `50(1±b)`, with `|b|∈[0.05,0.2]`. These are proposed custom measurements, not the stock observation interface: at 40 Hz record eight positions excluding global forward translation, nine velocities, and summed vertical foot force (`[time,18]`), alongside six commands. Targets are 20 intervals of positions, velocities, and two labeled foot forces (`[20,19]`). Transform each contact wrench into world coordinates, select ground-on-foot forces by named foot, check signs, then average vertically over intervals. Verify dimensions against the pinned model.

Use open-loop schedules prepared on a separate nominal body and frozen before target-body generation, so future commands are known at forecast origin. Compare C, selected B, snapshot, and equation-aware references on independent families; repeat full/recent-history audits. The endpoint is signed bilateral foot impulse divided by nominal body weight times horizon. Retain falls as outcomes. Cart ambiguity and gate validity are not assumed. The week-2 gate requires stable schedules, verified contact extraction/reflection, and compute feasibility; failure removes the broader claim. Human acquisition and adaptive probing are excluded.

The defensible target is an auditable experiment separating available evidence, representation geometry, and predictive use. A structured-memory finding requires success beyond stored summaries and ordinary context. If those controls match the candidate, that result determines the paper's claim. The benchmark, complete comparison records, and negative boundaries remain the deliverables; no architectural breakthrough is presumed.
