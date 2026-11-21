# Four Ways to Lose the Hidden Side: Asymmetric Mechanics in Predictive World Models

**Version 2 · Research proposal · 23 October 2026**
**Status:** plan only; no models have been trained. Revised after [Review 1](../../output/research-claude/review-v01.md), which found that version 1 had no account of why a world model would lose an asymmetry, no measure separating forgetting from missing data, and no role for JEPA-style training. Its Codex adversarial review also showed that the cart's motion kept revealing the asymmetry during the delay, that the Bayesian reference was not exact, and that the main endpoint was undefined. Section numbers in brackets, such as [X1], point to the findings each change answers.

## Abstract

World models learn to predict how a system responds to actions, and robot-learning practice increasingly builds left–right symmetry into them through mirrored data or equivariant layers. A symmetric body plan does not guarantee a symmetric body, though: a stronger left or right side often stays hidden during ordinary motion until an input pushes the two sides differently. To predict the response to such an input, a model must infer the asymmetry from brief evidence, keep it through periods that carry no further evidence, and combine it with the new command. We argue that this can fail in four distinct ways. A deterministic symmetric model cannot commit to one side when its evidence is mirror-symmetric; squared-error training under limited capacity drops small signed responses before large symmetric ones; ordinary next-step training gives no reward for keeping evidence through an uninformative delay; and a decoder that adds context and command together cannot express a response whose sign depends on both. Each failure has a short formal argument and a distinct signature. We propose controlled episodes that switch each failure on and off, measure retention against an exact Bayesian reference, and compare reconstruction, latent-prediction (JEPA-style) and response-trained world models.

## 1. Motivation

A world model is useful when it can answer "what will happen if I do this?" before the action is taken. For a body, the answer depends on physical properties that a camera or a force plate may not show directly, such as how strong each actuator is. An exoskeleton controller that adds assistance to one leg, or a legged robot compensating for a weakened motor, needs a model whose internal state carries those properties.

Left–right asymmetry is a demanding case. It is common in the bodies we care about, including people after a stroke, prosthesis users and robots with a worn or damaged motor, and yet its effects are small relative to the overall motion and can stay invisible during ordinary movement. It also collides with a widespread modeling habit: because a body plan is symmetric, practitioners mirror their data or build symmetry into the network, a choice that is sound for the population and can silently remove the difference that makes one body unusual.

The user's earlier work illustrates the risk. In a study of JEPA-inspired pose restoration, a baseline that always predicted zero change in knee asymmetry had lower asymmetry-change error than all sixteen trained variants, even though the trained models restored noisy poses well. Several explanations are possible, including heavy penalties for failed measurements, and the study does not show that any representation erased asymmetry. It does show that a model can improve on the large, symmetric part of a target while doing worse than nothing on its small, signed part. This proposal asks when and why that happens in predictive world models, and what prevents it.

## 2. The running example

A cart is pushed by a left motor with gain $g+b$ and a right motor with gain $g-b$, with $g > |b|$. Here $b$ is the asymmetry: positive when the left motor is stronger. A common command $a$ goes to both motors, and a differential command $u$ raises the left command and lowers the right. Each motor's activation $q$ follows its command through a first-order lag, $\tau \dot q_L = a+u-q_L$ and $\tau \dot q_R = a-u-q_R$, and the forces are $F_L = (g+b)q_L$, $F_R = (g-b)q_R$. In steady state $q_L = a+u$ and $q_R = a-u$, so

$$F_+ = F_L + F_R = 2ga + 2bu, \qquad F_- = F_L - F_R = 2ba + 2gu.$$

The cart obeys $m\ddot x = F_+ - kx - c\dot x$. Its sensors report position, velocity and total force $F_+$, each with Gaussian noise; the individual motor forces are never observed. With $u = 0$ the total force is $2ga$ for either sign of $b$, so passive observation cannot tell which motor is stronger. A short differential probe changes the total by about $2bu$, revealing the sign.

**Episodes.** Each episode has three phases.

1. **Probe.** Starting from a canonical rest state ($x = \dot x = 0$, $q_L = q_R = a$), the controller applies alternating differential pulses whose overall sign is chosen at random, independently of $b$.
2. **Reset and hold.** A fixture returns the cart to the canonical position and holds it at rest, with $u = 0$. A visible flag marks the hold. The model's memory is *not* reset. Version 1 let the cart coast instead, and the Codex review showed that the probe's effect on position and velocity can persist for many seconds, so recent motion would reveal $b$ without any memory [X1]. Under the hold, position and velocity are fixed, and the only trace of the probe is the activation difference $q_L - q_R$, which decays with time constant $\tau$ (about 0.1 s). After the first second of hold, the observations carry essentially no information about $b$; Section 3 says how this is checked.
3. **Query.** The fixture releases the cart at the canonical state and a constant differential command $u^*$ is applied for $H = 0.5$ s. The model must predict the resulting force and motion.

A secondary **free-delay** condition omits the reset, so the cart coasts. There the observations keep some information about $b$, and the condition measures how much a model gains from recent motion when it is available. It is reported separately and never pooled with the main condition.

**The endpoint.** Version 1 spoke of a "signed response" without defining it [X3]. We define the **query contrast** as half the difference between the responses to $+u^*$ and $-u^*$ from the same origin state. For the cart, the total-force impulse over the query is

$$J(u^*) = 2gaH + 2bu^*\,\kappa, \qquad \kappa = H - \tau\left(1 - e^{-H/\tau}\right),$$

so the true query contrast is $r = [J(+u^*) - J(-u^*)]/2 = 2bu^*\kappa$. The simulator computes it from two branches cloned from the same saved state. A model's predicted contrast is $\hat r = [\hat J(H_t, +u^*) - \hat J(H_t, -u^*)]/2$, computed from one history $H_t$ with two copies of the same memory. Neither branch's outcome is ever fed back into the other.

## 3. Concepts, stated carefully

**Reflection and parity.** A mirror reflection $M$ swaps left and right. It leaves **even** quantities unchanged (total force, forward motion, the common command $a$) and flips the sign of **odd** ones (the asymmetry $b$, the differential command $u$, any left-minus-right difference). The product of two odd quantities is even, which is why $bu$ appears in the total force.

**Invariance and equivariance.** A function $f$ is equivariant if $f(Mx) = Mf(x)$ and invariant if $f(Mx) = f(x)$. Version 1 blurred two different things that can be invariant [X9]. An invariant *predictor* of total force is entirely sensible, since the physics gives $F_+(b, u) = F_+(-b, -u)$. The damaging case is an invariant *history encoder* followed by a decoder that receives the query unreflected. Take two mirror-twin bodies, $b$ and $-b$, whose probes were also mirror images. An invariant encoder gives them the same latent state. At the same later query $u^*$, their true contrasts are $+2bu^*\kappa$ and $-2bu^*\kappa$, yet the model must predict the same value for both.

**When equivariance is the right constraint.** Equivariance of the best predictor follows from symmetry of the whole data-generating process, not only from a balanced population. We assume: the distribution of $(g, |b|)$ is the same for both signs of $b$; the probe's overall sign is drawn independently of $b$ with probability one half; the canonical initial state, the hold and the query distribution are unchanged by reflection; and sensor noise is unchanged by reflection. Under these assumptions the joint law of histories, queries and outcomes is unchanged by $M$, and the conditional mean of the outcome given history and query, which is the best squared-error predictor, is equivariant. The failures below arise from what a model can do with mirror-symmetric evidence and from how training spends capacity; equivariance itself is consistent with the optimum.

**Identifiability.** A parameter is identifiable from an experiment if different values produce different distributions of measurements. Here the sign of $b$ is not identifiable from passive data and becomes identifiable after a probe.

## 4. What the data allow: an exact reference

In the core condition the lag $\tau$, mass $m$, stiffness $k$ and damping $c$ are fixed, known constants, while the common gain $g$ and the asymmetry $b$ are unknown and vary across bodies [X2]. Because every command is known and $\tau$ is known, the activations $q_L(t)$ and $q_R(t)$ are known functions of time. Total force is $F_+ = g(q_L + q_R) + b(q_L - q_R)$, which is linear in $(g, b)$, and position and velocity are linear responses to $F_+$ from a known initial state. Every observation is therefore a known linear function of $(g, b)$ plus Gaussian noise. The posterior over $(g, b)$ given any history is the prior multiplied by a Gaussian likelihood whose mean and covariance come from a two-parameter linear regression. We evaluate it on a fine grid over the bounded prior and confirm that halving the grid spacing changes the posterior mean by less than 1% of the prior range of $b$.

A secondary condition makes $\tau$ and $m$ unknown as well. Given $(\tau, m)$ the model is again linear in $(g, b)$, so the reference integrates $(g, b)$ out exactly and samples $(\tau, m)$ by importance sampling, a Rao–Blackwellized scheme whose Monte Carlo error we report. Any reference that receives true nuisance values is labeled **privileged** and used only as a ceiling.

Three further references measure information directly. The **full-history** reference is the Bayesian posterior from the whole episode. The **recent-window** reference uses only the last two seconds before the query. The **no-probe** reference uses an episode whose probe was replaced by zero command. In the main condition the recent-window and no-probe references should sit at chance; if they do not, the hold has failed and the condition is redesigned before any model is trained.

## 5. Measuring retention and use

**Fidelity slope.** Across test bodies, regress predicted contrast $\hat r$ on true contrast $r$ through the origin, $\beta = \sum_i \hat r_i r_i / \sum_i r_i^2$. A slope of 1 means predictions carry the asymmetry at full strength; 0 means they have collapsed to a symmetric body.

**Retention ratio.** Even the Bayesian reference shrinks its predictions toward zero when the probe is weak, because the best estimate of $b$ from noisy evidence lies between the two signs. Its slope $\beta_{\text{Bayes}}$ is computed from the same histories. The retention ratio $\rho = \beta_{\text{model}} / \beta_{\text{Bayes}}$ asks what share of the available signed information reaches the model's prediction. The primary analysis uses probe strengths at which $\beta_{\text{Bayes}} \geq 0.8$, so the ratio is stable.

**Is the information still in the state?** Prediction error alone cannot separate a state that lost the information from a decoder that cannot read it [X4]. At the end of the probe and after 1, 2, 4 and 8 seconds of hold, we freeze each trained model and fit small readouts (linear and two-layer) from its latent state to the sign and value of $b$, using training families only and choosing readout settings on validation families. We fit one readout shared across delays and one per delay, since a representation can move to a new direction over time while keeping the information (Chen and Liu, 2026). Readout accuracy measures *usable* information for that readout class, in the sense of Xu et al. (ICLR 2020). A failure means the tested readouts could not find the information; it does not prove the information is absent.

**Does the prediction use it?** For a pair of mirror-twin test bodies, we swap the persistent context (or, for models without one, the odd part of the latent state) between the twins at the query origin. A model that uses the stored asymmetry should flip the sign of its predicted contrast; one that ignores it should not change.

**Guardrails.** Next-step prediction error during the hold and the probe, the Brier score of the predicted probability that $b > 0$, and coverage of 90% predictive intervals.

## 6. Four ways to lose the hidden side

### M1. Symmetry: a deterministic equivariant model cannot commit to a side

If a deterministic equivariant model receives an input that reflection leaves unchanged, $Mx = x$, then $f(x) = f(Mx) = Mf(x)$, so every odd component of its output is zero. This is Curie's principle in neural form (Smidt, Geiger and Miller, 2021; Kaba and Ravanbakhsh, 2023).

A passive history is unchanged by reflection, because every observation is even and $u = 0$. Reflecting the pair (history, $+u^*$) gives (history, $-u^*$), and total force is even, so a deterministic equivariant model predicts the same impulse for both queries: its predicted contrast is exactly zero. As a mean over bodies this is correct. Each imagined rollout, however, describes an average body that does not exist, and a planner using those rollouts would be wrong for every actual body. A stochastic equivariant model can avoid this: its predictive distribution can be unchanged by reflection while each sample is asymmetric, for example an equal mixture of a left-stronger and a right-stronger body (Lawrence et al., ICLR 2025).

*Signature:* under passive histories, deterministic equivariant models predict zero contrast in every rollout; stochastic ones produce two clusters of rollouts with opposite contrast and equal weight. After probes, both can commit. *Knob:* deterministic versus stochastic context, crossed with passive versus probed histories.

### M2. Capacity: squared error drops small signed responses first

Consider a linear predictor that maps history features to a fixed set of query responses through a bottleneck of width $k$, trained by squared error. The best such predictor keeps the $k$ directions along which the predictable part of the response varies most; this is reduced-rank regression (Izenman, 1975). Under the symmetry assumptions of Section 3, odd quantities have mean zero and are uncorrelated with even ones, since $\mathbb E[y_e y_o] = \mathbb E[y_e(-y_o)]$. Every retained direction is therefore purely even or purely odd, and the two kinds compete for the $k$ slots on predictable variance alone.

The predictable variance of the odd response grows with the typical asymmetry $\mathbb E[b^2]$ and with the size and frequency of probes in training. When it falls below the $k$-th largest even variance, the best width-$k$ predictor ignores the asymmetry, although it is perfectly predictable. Training dynamics point the same way, since deep linear networks learn strong directions before weak ones (Saxe, McClelland and Ganguli, 2014), so an early-stopped network can miss weak directions even without a hard bottleneck. Littwin et al. (NeurIPS 2024) show that in deep linear self-distillation networks, JEPA-style latent prediction favors features with large regression coefficients, while reconstruction favors features with large variance. The asymmetry is a small-variance feature with a large effect per unit of evidence, so their result predicts that latent prediction keeps it at smaller magnitudes than reconstruction does.

*Signature:* the fidelity slope collapses below a critical asymmetry magnitude that grows as the bottleneck narrows; reconstruction collapses before latent prediction; normalizing the even and odd parts of the loss by their own variances shifts the threshold. *Knob:* asymmetry magnitude, probe frequency, latent width, training objective.

### M3. Memory: nothing in next-step training rewards keeping evidence

During the hold, the true observations do not depend on $b$. If the model's predicted observations during the hold do not depend on the odd part of its state either, the next-step loss is flat along that part, and its gradient with respect to the stored value is zero. The only signal that rewards keeping the value comes from the query loss after the delay, passed backward through every step of the hold. For a recurrent update whose odd part shrinks by a factor $r < 1$ per step, the stored value and that gradient both shrink like $r^D$ over $D$ steps (Bengio, Simard and Frasconi, 1994).

*Signature:* readout accuracy and retention ratio decay with delay for models trained on next-step loss alone; adding a query loss slows the decay; truncating backpropagation to fewer steps than the delay removes the benefit. *Knob:* delay, query loss on or off, truncation length, persistent slot on or off.

### M4. Coupling: an additive decoder cannot express a signed response

Write the decoder's prediction of an even output as $y_e(z_e, z_o, a_e, a_o)$, a function of even and odd latent features and even and odd command components. Equivariance requires $y_e(z_e, -z_o, a_e, -a_o) = y_e(z_e, z_o, a_e, a_o)$. Suppose the decoder fuses state and command additively, $y_e = g_1(z_e, z_o, a_e) + g_2(a_e, a_o)$. Setting $a_o = 0$ shows $g_1$ is even in $z_o$, and then $g_2$ must be even in $a_o$. The predictions for $+u^*$ and $-u^*$ are then equal whatever the latent state, so the predicted contrast is zero for every body. The term $bu$ requires a multiplicative interaction between odd state and odd command.

*Signature:* readouts recover $b$ from the latent state, yet the fidelity slope is zero. *Knob:* additive versus multiplicative fusion.

### How the mechanisms fit together

The four mechanisms act at different points of the same pipeline. M1 governs whether a model can stay undecided and then commit; M2 governs whether training gives the asymmetry any capacity; M3 governs whether the information survives the hold; M4 governs whether it reaches the prediction. A model must clear all four to keep the hidden side, and each experiment below switches on one mechanism while the others are held off.

## 7. Research question and hypotheses

**Research question.** By the ICML 2027 submission deadline (expected late January 2027, 13 weeks from now), can we determine for each of the four mechanisms whether switching it on lowers the retention ratio of a standard world model at an eight-second hold, and can a world model built to avoid all four keep a retention ratio of at least 0.9 on held-out simulated bodies while its next-step error stays within 5% of the best baseline's?

**H1 (availability).** The full-history reference is near chance on passive histories and accurate after probes; the recent-window and no-probe references are near chance at every hold longer than one second.

**H2 (symmetry).** Under passive histories, deterministic equivariant models predict zero contrast in every rollout, and stochastic equivariant models produce balanced two-cluster rollouts.

**H3 (capacity).** Below a critical asymmetry magnitude, the fidelity slope falls toward zero; the critical magnitude increases as latent width decreases and is smaller for latent prediction than for reconstruction.

**H4 (memory).** Models trained on next-step loss alone lose readout accuracy and retention ratio as the hold lengthens; a query loss with full backpropagation and a persistent slot prevent the loss.

**H5 (coupling).** With additive fusion, readouts recover $b$ but the fidelity slope is near zero; multiplicative fusion restores it.

## 8. Related work

**World models.** Recurrent state-space models such as PlaNet and DreamerV3 (Hafner et al., 2019, 2023) learn latent dynamics by reconstructing observations. Joint-embedding predictive architectures (JEPA; Assran et al., 2023) instead predict the representation of hidden or future inputs; V-JEPA 2 (Assran et al., 2025) adds action-conditioned prediction for planning, and DINO-WM (Zhou et al., 2024) plans in the feature space of a pretrained image encoder. Which objective keeps small but consequential information is open, and this study tests it in a setting where the answer can be checked exactly.

**Symmetry in robot learning.** Chirality Nets (Yeh, Hu and Schwing, NeurIPS 2019) introduced reflection-equivariant recurrent layers for human pose. Ordoñez-Apraez et al. (IJRR 2025) show that morphological symmetries constrain robot dynamics and can be built into learned models, and SWAP (Lan et al., 2026) builds a reflection-equivariant world model for legged parkour. These works use symmetry; our question concerns an individual body that breaks it.

**Symmetry breaking.** Equivariant functions cannot break the symmetry of their inputs (Smidt, Geiger and Miller, 2021; Kaba and Ravanbakhsh, 2023). Lawrence et al. (ICLR 2025) restore symmetry breaking with equivariant conditional distributions and randomized canonicalization. Approximately equivariant networks relax the constraint where data depart from symmetry (Wang, Walters and Yu, ICML 2022), and relaxed group convolutions can locate where symmetry is broken (Wang et al., ICML 2024).

**Inferring hidden context.** RMA (Kumar et al., 2021) and context-aware dynamics models (Lee et al., ICML 2020; Kirchmeyer et al., ICML 2022) infer environment properties from recent interaction. VariBAD (Zintgraf et al., 2020) maintains a posterior over a task embedding from the full history and is the closest existing design to our two-sided belief.

**Representations under intervention.** *Identifiable World Models* (Sandilya, Liston and Grosenick, 2026) and *Compact but Moving* (Chen and Liu, 2026) study when representations support predictions under interventions, the latter showing that relevant directions can move over time.

**Implicit bias of objectives and probing.** Deep linear networks learn strong directions first (Saxe, McClelland and Ganguli, 2014); JEPA and reconstruction prioritize different features (Littwin et al., NeurIPS 2024). Usable information (Xu et al., ICLR 2020) and control tasks for probes (Hewitt and Liang, 2019) guide how readouts are interpreted.

## 9. Method

### 9.1 The walker tier

The second body is the dm_control planar walker, which has two legs with hip, knee and ankle motors. Its left and right knee gains are scaled by $1+b$ and $1-b$. Version 1 let it walk under a nominal controller throughout, and the Codex review pointed out that ordinary walking with unequal knees produces a visible limp, while a feedback controller writes the asymmetry into its own commands, so the delay would never be uninformative [X5]. The main walker episodes therefore copy the cart's structure.

1. **Harnessed probe.** The torso is held by a harness. Differential knee commands are applied while the feet are off the ground.
2. **Harnessed hold.** The legs are reset to a canonical hanging pose, as the cart is reset, and all commands are zero. With zero commands the actuator gains have no effect, and the reset removes any leftover swing from the probe, so the observations do not depend on $b$.
3. **Released query.** The walker is set on the ground in a canonical standing pose, released, and driven for 0.5 s by an open-loop bilateral command sequence fixed before release. The model predicts joint angles and the vertical force under each foot.

The model observes joint angles and velocities for both legs, torso pose, and total vertical ground force. A secondary **walking** condition uses a fixed feedforward policy, trained on separate symmetric bodies, during the delay. It is labeled as a continuous-evidence condition. Its recent-window references measure how much the limp reveals, and it supports a retention claim only if those references show a real information gap. No exact Bayesian reference exists for the walker, so the full-history transformer of Section 9.2 serves as the empirical information reference.

### 9.2 Models

All learned models share an encoder per observation, a recurrent update, a decoder, a latent width $k$ and a training budget. They differ along five axes.

- **Objective:** reconstruction of future observations (DreamerV3-style); latent prediction of future encoder features with a slowly updated target encoder and a variance–covariance regularizer (JEPA-style), with physical responses read by a head trained on the same targets; or reconstruction plus a query-response loss.
- **Symmetry:** unconstrained; unconstrained with mirror augmentation, reflecting each episode together with its targets; deterministic equivariant; stochastic equivariant with a two-component belief. A negative control reflects inputs but keeps the original targets, which pushes the model toward invariance.
- **Memory:** ordinary recurrent state; recurrent state plus a persistent context slot written through a learned gate.
- **Decoder fusion:** additive or multiplicative.
- **Loss weighting:** raw squared error, or even and odd parts of the target each divided by their own training variance. Equal weights on sums and differences would only rescale the ordinary loss, since $(e_L+e_R)^2 + (e_L-e_R)^2 = 2(e_L^2+e_R^2)$; variance normalization changes which directions the loss emphasizes.

**Strong simple baselines** [X6]: a **snapshot** model that stores its recurrent state at the onset of the hold flag and passes it to the query decoder; a **full-history transformer** that attends over the whole episode without compression; and a **VariBAD-style** model that updates a Gaussian posterior over a task embedding at every step. A recent-window context model in the style of RMA is labeled an information-restricted reference, since it cannot see the probe by design.

**The remedy model** combines a stochastic two-component belief, a persistent slot, multiplicative fusion, variance-normalized query loss and full backpropagation. Each component is also removed one at a time.

### 9.3 Training

Every model is trained on whole episodes with backpropagation through the full probe, hold and query [X8]. Arms for H4 use next-step loss only; all other arms add the same query loss with the same weight. Query targets enter the loss and never the recurrent input. Models are reset to their initial state at the start of each episode. Each query branch starts from a copy of the same origin memory, and no branch's outcome updates any other branch.

### 9.4 Experiments

| Experiment | What changes | Mechanism | What would confirm it | What would refute it |
|---|---|---|---|---|
| E1 | Probe vs passive; references only | Availability | Recent-window and no-probe at chance; full-history accurate | Recent window accurate at long holds |
| E2 | Deterministic vs stochastic equivariant context | M1 | Zero contrast vs balanced two-cluster rollouts on passive histories | Deterministic model produces asymmetric rollouts |
| E3 | Asymmetry magnitude × width × objective, next-step and query arms | M2 | Collapse threshold rises as width falls, lower for latent prediction | No threshold, or no dependence on width |
| E4 | Hold length × query loss × truncation × slot | M3 | Decay without query loss or slot; none with both | No decay under next-step loss alone |
| E5 | Additive vs multiplicative fusion | M4 | Readout succeeds, slope zero with additive fusion | Additive fusion gives nonzero slope |
| E6 | Remedy vs all baselines, both tiers | All | $\rho \geq 0.9$ at 8 s, above the best baseline | Snapshot or VariBAD baseline matches the remedy |

## 10. Pipeline, splits and leakage

A **body family** is one draw of body parameters together with its mirror twin, with $b$ replaced by $-b$. Every episode, probe variant, hold length, query branch and noise replicate generated from a family stays in that family.

| Step | What happens | What is preserved | Split and leakage guard |
|---|---|---|---|
| 1. Sample | Draw $(g, |b|)$; form the twin pair; draw probe signs independently | Parameters, seeds, generator version | Families assigned to pilot, training, validation and test before any simulation |
| 2. Simulate | Probe, hold, query; clone the state at the query origin for each query branch | Native time step, SI units, named left/right channels, shape `[episode, time, channel]` | All episodes and branches inherit the family's split; cloning is checked by replaying identical inputs |
| 3. Window | Histories end at the query origin | No resampling or stretching; padding with masks | Query targets never in inputs; memory reset per episode; branches never update one another |
| 4. Normalize | Scale channels | Odd channels centered at zero with a symmetric scale, so reflection still flips their sign; transforms saved and invertible | Training statistics only |
| 5. Train and select | Fit models and readouts; tune | Channel order and time grid unchanged | Validation families only; the walker policy is trained on separate bodies |
| 6. Test | Score once | Predictions on the target grid and units | After all settings are frozen |

## 11. Statistics

**Primary endpoint.** Retention ratio $\rho$ at the eight-second hold in the cart's main condition, on test families.

**Decision rule** [X7]. The remedy succeeds if the lower end of the 95% confidence interval for its $\rho$ is at least 0.9, the interval for its difference from the best baseline (chosen on validation) lies above zero, and the upper end of the 95% interval for its relative increase in next-step error is below 5%. All three must hold.

**Uncertainty.** Each model is trained with five seeds. Confidence intervals come from a bootstrap that resamples test families and training seeds together, so they reflect both sources of variation. Mechanism tests E2–E5 are adjusted with the Holm procedure. A crashed fit or a non-finite prediction counts against the model that produced it and is never dropped.

**Sample size.** A pilot on separate families estimates the variance of $\rho$; the number of test families is set so that the confidence interval half-width is at most 0.03.

## 12. Plan and resources

Weeks 1–2: simulators, references, E1, and a pilot that measures training cost; the walker harness and contact extraction must work by the end of week 2 or the walker tier is reduced to the walking condition. Weeks 3–6: E2–E5 on the cart. Weeks 7–8: remedy model. Weeks 9–11: walker. Weeks 12–13: final test, analysis, writing.

**Resource estimate** [X10]. Cart episodes run at 100 Hz for at most 11.5 s (about 1,150 steps). The pilot sets family counts; the planning figure is 4,000 training, 500 validation and 1,000 test families. Cart models have about 0.2 M parameters and train in about 20 minutes on one GPU; E2–E6 need roughly 300 fits, about 100 GPU-hours. Walker models need about 3 GPU-hours each, about 30 fits, about 90 GPU-hours. The total cap is 250 GPU-hours, and optional sweeps are dropped before any primary comparison.

## 13. Limitations

The study is in simulation, and its formal statements hold under stated assumptions, such as linear predictors for M2 and an uninformative hold for M3. The experiments decide whether these mechanisms matter for trained nonlinear world models.

## References

- Assran, M. et al. (2023). Self-supervised learning from images with a joint-embedding predictive architecture. *CVPR*. arXiv:2301.08243.
- Assran, M. et al. (2025). V-JEPA 2: Self-supervised video models enable understanding, prediction and planning. arXiv:2506.09985.
- Bengio, Y., Simard, P. and Frasconi, P. (1994). Learning long-term dependencies with gradient descent is difficult. *IEEE Trans. Neural Networks* 5(2).
- Chen, Y. and Liu, Y. (2026). Compact but moving: Intervention-relevant geometry in recurrent world models. arXiv:2609.21787.
- Hafner, D. et al. (2019). Learning latent dynamics for planning from pixels. *ICML*. arXiv:1811.04551.
- Hafner, D. et al. (2023). Mastering diverse domains through world models. arXiv:2301.04104.
- Hewitt, J. and Liang, P. (2019). Designing and interpreting probes with control tasks. *EMNLP*. arXiv:1909.03368.
- Izenman, A. J. (1975). Reduced-rank regression for the multivariate linear model. *J. Multivariate Analysis* 5(2).
- Kaba, S.-O. and Ravanbakhsh, S. (2023). Symmetry breaking and equivariant neural networks. arXiv:2312.09016.
- Kirchmeyer, M. et al. (2022). Generalizing to new physical systems via context-informed dynamics model. *ICML*. arXiv:2202.01889.
- Kumar, A. et al. (2021). RMA: Rapid motor adaptation for legged robots. *RSS*. arXiv:2107.04034.
- Lan, K. et al. (2026). SWAP: Symmetric equivariant world-model for agile robot parkour. arXiv:2606.19928.
- Lawrence, H. et al. (2025). Improving equivariant networks with probabilistic symmetry breaking. *ICLR*. arXiv:2503.21985.
- Lee, K. et al. (2020). Context-aware dynamics model for generalization in model-based reinforcement learning. *ICML*. arXiv:2005.06800.
- Littwin, E. et al. (2024). How JEPA avoids noisy features: The implicit bias of deep linear self distillation networks. *NeurIPS*. arXiv:2407.03475.
- Ordoñez-Apraez, D. et al. (2025). Morphological symmetries in robotics. *IJRR*. arXiv:2402.15552.
- Sandilya, R., Liston, C. and Grosenick, L. (2026). Identifiable world models from pretrained diffusion representations. arXiv:2610.07028.
- Saxe, A. M., McClelland, J. L. and Ganguli, S. (2014). Exact solutions to the nonlinear dynamics of learning in deep linear neural networks. *ICLR*. arXiv:1312.6120.
- Smidt, T. E., Geiger, M. and Miller, B. K. (2021). Finding symmetry breaking order parameters with Euclidean neural networks. *Phys. Rev. Research* 3, 012002.
- Tassa, Y. et al. (2018). DeepMind control suite. arXiv:1801.00690.
- Wang, R., Walters, R. and Yu, R. (2022). Approximately equivariant networks for imperfectly symmetric dynamics. *ICML*. arXiv:2201.11969.
- Wang, R. et al. (2024). Discovering symmetry breaking in physical systems with relaxed group convolution. *ICML*. arXiv:2310.02299.
- Xu, Y. et al. (2020). A theory of usable information under computational constraints. *ICLR*. arXiv:2002.10689.
- Yeh, R. A., Hu, Y.-T. and Schwing, A. G. (2019). Chirality nets for human pose regression. *NeurIPS*. arXiv:1911.00029.
- Zhou, G. et al. (2024). DINO-WM: World models on pre-trained visual features enable zero-shot planning. arXiv:2411.04983.
- Zintgraf, L. et al. (2020). VariBAD: A very good method for Bayes-adaptive deep RL via meta-learning. *ICLR*. arXiv:1910.08348.
