# When a World Model Must Remember Which Side Is Different

**Version 1 · Research proposal · 23 October 2026**  
**Status:** proposed experiments; no new model-training or human results.

## Abstract

A useful model of movement should predict how a body responds when its inputs change. Similar visible motion can arise from different left–right mechanics, so reconstructing a walking sequence may leave important differences unresolved. We propose a controlled study of whether predictive world models retain information about those differences after a brief diagnostic interaction. A simulator will separate the availability of information from its preservation in memory, while reflection-consistent models will preserve the distinction between left and right without treating mirror-related bodies as unrelated. The study compares learned models with ordinary system identification under the same observation and interaction budgets. Its intended contribution is an experimentally grounded account of when signed mechanical information is recoverable, retained, and useful for predicting a later physical response.

## Motivation and evidence

A world model predicts future measurements from past observations and specified inputs. For a bilateral body, inputs might be separate actuator commands and measurements might be joint positions and total force. Two bodies can look similar during ordinary motion even if their left and right actuators have different gains. When assistance changes on one side, their responses can diverge. The predictive model therefore needs a memory of whatever earlier observations distinguished the bodies.

The supplied JEPA manuscript evaluates restoration of observed pose windows. JEPA learns internal feature vectors by predicting target features; that task need not include future physical inputs. Its uncertain comparison between feature-difference and endpoint objectives, and the strong zero-change baseline, do not demonstrate that a symmetry constraint erased mechanics. The URTC draft explicitly reports source-video overlap across training and testing. These manuscripts motivate measurement and provenance controls, rather than supplying evidence for a completed mechanics-prediction method. See the [source audit](../../output/research-codex/source-evidence-audit.md).

The study keeps the original proposal’s distinction between **identification**, meaning what measurements reveal about unknown parameters, and **retention**, meaning what a learned memory preserves. It removes the extended chemistry analogy because physical prediction motivates the learning question directly. Bilateral asymmetry means a signed difference between sides; molecular chirality has a different geometric definition.

## Research question

Within twelve weeks, does a reflection-consistent recurrent world model with persistent mechanical context improve delayed response prediction over an equally informed recurrent baseline, on unseen bodies and input schedules, after the diagnostic measurements leave the immediate observation window?

The hypothesis is that training for later physical responses encourages retention of information that short-horizon prediction can overlook. It is conditional: the supplied history must first permit an ordinary estimator to distinguish the relevant mechanics. Passive observations may already suffice; when all histories remain ambiguous, a useful model should retain uncertainty.

## A minimal physical example

Let left and right actuator gains be $g+b$ and $g-b$, with $g>|b|$. Under common command $a$ and differential command $u$,

$$
\begin{aligned}
F_L &= (g+b)(a+u), \\
F_R &= (g-b)(a-u), \\
F_+ &= 2ga+2bu, \\
F_- &= 2ba+2gu.
\end{aligned}
$$

If only total force $F_+$ is observed at $u=0$, the sign of $b$ is hidden. Opposite known probes reveal it through the change in total force. If individual baseline forces are visible, their difference already contains that information. This analytical control requires no neural network.

Reflection swaps the body’s sides and corresponding commands. It maps $b$ and $u$ to their negatives, leaving their product unchanged. An **equivariant** predictor follows this transformation consistently. An **invariant** representation instead makes mirrored histories identical, which can be harmful when a later command retains a fixed anatomical meaning. Existing equivariant models already support asymmetric states.

## Method and data pipeline

1. **Generate episodes.** Begin with the analytical actuators and a compact bilateral simulator. Vary signed gain, common gain, initial state, and sensor noise independently. Preserve raw trajectories, timestamps, units, anatomical channel names, and simulator configurations. Each episode contains a diagnostic input, a delay, and a later input whose response is predicted.

2. **Split complete families.** Assign 70% of independent body families to training, 15% to validation, and 15% to locked testing before extracting windows. Keep all episodes, continuations, mirror copies, and sensor variants from a body together. Withhold schedules for a separate harder test, distinguishing new bodies under familiar schedules from joint body-and-schedule shift.

3. **Construct causal inputs.** Pose inputs have shape $[B,T,J,C]$: batch, timestamps, labeled joints, and channels. Commands have shape $[B,T,A]$; Boolean masks identify unavailable measurements. Preserve joint order, timestamps, and left/right names. Pad short sequences with masks instead of stretching gait cycles. Fit normalization on training observations, consistently across sides. Raw data remain unchanged; normalization creates a documented model view.

4. **Learn state and context.** Process observations chronologically. A changing state describes motion, while persistent context describes episode-constant mechanics. Sample context once per imagined future and reuse it, so the predicted body cannot randomly change its stronger side. Real measurements update the context belief; predictions do not count as new evidence.

5. **Train physical prediction.** Add a later-response loss to the baseline probabilistic sequence objective. Give all comparators the same saved branches and physical targets. Preserve trajectory shapes and target masks; a scalar asymmetry index does not replace the trajectory. Evaluate total force, bilateral force difference, and joint motion separately.

6. **Test retention.** After diagnosis, remove the identifying sensor channel using an explicit mask. Predict a later input under original anatomical labels, without adding its response to the history. Use schedules fixed at forecast origin. Logged future feedback commands would instead define retrospective replay.

Exact tensor dimensions and preserved physical geometry are different requirements. Normalization changes numerical coordinates; its transformation must be recorded and invertible. Anatomical structure, timing, missingness, and source provenance remain traceable throughout training.

## Comparisons and interpretation

Compare persistence, zero response, an analytical or Bayesian parameter estimator, ordinary recurrence, recurrence with ordinary context, and reflection-equivariant context. A privileged mechanics oracle estimates a ceiling. Match learned models’ parameter counts, training data, probe counts, available observations, and tuning budgets.

The primary outcome is later physical-response error, averaged within bodies before averaging across bodies. Report delay-dependent error, uncertainty coverage, ordinary forecast error, and mechanics-sign accuracy as a diagnostic. A successful sign classifier alone does not show useful prediction. Use multiple training seeds and paired body-level intervals; windows and mirror branches are repeated observations, not additional subjects.

If an ordinary estimator cannot recover information, revise sensing and excitation before blaming representation learning. If ordinary context matches the proposed model, report the value of memory without claiming a new equivariant architecture. If response improvement requires extra observations or degrades ordinary forecasts, investigate that tradeoff before claiming preservation.

## Related work and scope

[Chirality Nets](https://arxiv.org/abs/1911.00029) already provides anatomical reflection-equivariant recurrence and pose prediction; [SWAP](https://arxiv.org/abs/2606.19928) supplies an equivariant recurrent world-model precedent. [V-JEPA 2](https://arxiv.org/abs/2506.09985) separates representation pretraining from action-conditioned prediction. [Identifiable World Models](https://arxiv.org/abs/2610.07028) and [Compact but Moving](https://arxiv.org/abs/2609.21787) constrain broad intervention-representation claims. The study must establish a specific retention failure and useful remedy beyond these mechanisms.

Weeks 1–2 establish simulator controls; weeks 3–5 build baselines; weeks 6–8 compare objectives; weeks 9–10 run locked tests; weeks 11–12 analyze and write. Human gait data remain an external extension because they do not supply the matched hidden-mechanics interventions required for the central experiment. ICML relevance depends on an informative benchmark and reproducible learning result.
