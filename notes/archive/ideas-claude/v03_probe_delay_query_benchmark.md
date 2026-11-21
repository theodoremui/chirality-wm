# Probe, Delay, Query: A Benchmark That Switches Each Way a World Model Can Lose Asymmetry

**Version 3 · Research proposal · 23 October 2026**
**Status:** plan only; no models have been trained. Revised after [Review 2](../../output/research-claude/review-v02.md) and its Codex adversarial review. The main changes are a primary endpoint that cannot reward amplified predictions, knobs that leave the available information fixed, capacity competition created by distractors with a known spectrum, losses written with explicit time masks, narrower and corrected formal statements, and an experimental plan organized as a sequence of decisions. A change log is at the end.

## Abstract

World models learn to predict how a system responds to actions, and robot learning increasingly builds left–right symmetry into them through mirrored data or equivariant layers. A symmetric body plan does not guarantee a symmetric body, and a stronger side often stays hidden until an input pushes the two sides differently. A model that must predict the response to such an input has to infer the asymmetry from brief evidence, keep it through stretches that carry no further evidence, and combine it with the new command. We describe four ways this can fail—a symmetry constraint that prevents committing to a side, competition for capacity under squared error that removes small signed responses first, a memory that receives no training signal during uninformative stretches, and a response head that cannot combine context with command—and we state the conditions under which each failure is guaranteed. We then propose *probe–delay–query* episodes, a benchmark in which each failure can be switched on and off while the information in the data stays fixed, with exact Bayesian references in a two-motor cart and a simulated walker. Retention is scored as the share of the Bayes-achievable improvement over a symmetric prediction that a model attains. The benchmark is designed to decide which failures matter for reconstruction-based, latent-prediction and response-trained world models, and which design choices prevent them.

## 1. Introduction

A world model is a learned simulator. Given what has been observed and a planned sequence of actions, it predicts what will happen next, so a controller can try an action before committing to it. For legged robots, exoskeleton users and prosthesis wearers, the answer to "what happens if I push harder on the left?" depends on how strong each side is, a property that ordinary motion can hide.

Symmetry is one of the most effective tools in robot learning. Morphological symmetries constrain a robot's dynamics and can be built into learned models (Ordoñez-Apraez et al., 2025), and equivariant world models such as SWAP (Lan et al., 2026) use left–right symmetry to learn faster and generalize to mirrored terrain. These priors describe the body *plan* correctly. A particular body can still break the symmetry through a weak motor, a payload, a brace or a stroke, and the question is whether a model built around symmetry can still represent, keep and use that difference.

The user's earlier work gives a reason to ask. In a study of JEPA-inspired pose restoration, a baseline that always predicted zero change in knee asymmetry had lower asymmetry-change error than all sixteen trained variants, even though those variants restored noisy poses well. Heavy penalties for failed measurements may explain part of the gap, and the study does not show that any representation erased asymmetry. It does show that a model can improve on the large symmetric part of a target while doing worse than a symmetric guess on its small signed part. The endpoint defined in Section 5 makes "worse than a symmetric guess" a measurable quantity.

This proposal turns that observation into a testable account. Its contributions are:

1. **A diagnostic account** of four mechanisms by which a predictive model can lose a signed asymmetry, each with a formal statement whose assumptions are explicit and a signature that can be measured.
2. **A benchmark**, probe–delay–query episodes, in which each mechanism has its own knob while the evidence about the asymmetry is held fixed, scored against exact Bayesian references.
3. **A controlled comparison of training objectives** (reconstruction, latent prediction in the JEPA style, and response supervision), including a deep-linear experiment that matches the assumptions of existing theory on JEPA's implicit bias.
4. **A remedy tested component by component** against strong simple baselines, including one that stores its state at the end of the probe.

The study proceeds as a sequence of questions, each decided before the next is asked (Section 8): does the data contain the asymmetry, do standard world models keep it, which mechanism explains any loss, does the matching remedy repair it, and does the account transfer to a walking body.

## 2. Setting

### 2.1 The two-motor cart

A cart is pushed by a left motor with gain $g+b$ and a right motor with gain $g-b$, with $g > |b|$. The asymmetry $b$ is positive when the left motor is stronger. A common command $a$ goes to both motors, and a differential command $u$ raises the left command and lowers the right. Each activation follows its command through a lag, $\tau\dot q_L = a+u-q_L$ and $\tau\dot q_R = a-u-q_R$, and the motor forces are $F_L = (g+b)q_L$ and $F_R = (g-b)q_R$. Their sum is

$$F_+ = g(q_L+q_R) + b(q_L-q_R),$$

which in steady state is $2ga + 2bu$. The cart obeys $m\ddot x = F_+ - kx - c\dot x$. Sensors report position, velocity and total force with Gaussian noise; the individual forces are never observed. With $u = 0$ the total force is $2ga$ for either sign of $b$, so passive observation cannot tell which motor is stronger. A differential command changes the total by about $2bu$, so a short probe reveals the sign.

### 2.2 Reflection and parity

A mirror reflection $M$ swaps left and right. **Even** quantities are unchanged by it (total force, position, velocity, the common command $a$, the common gain $g$), and **odd** quantities change sign (the asymmetry $b$, the differential command $u$, the activation difference $q_L - q_R$). The product of two odd quantities is even, which is how $bu$ enters the total force. A function is **equivariant** if $f(Mx) = Mf(x)$ and **invariant** if $f(Mx) = f(x)$.

Reflecting a whole episode leaves every observation unchanged (they are all even), negates every differential command, and exchanges the query $+u^*$ with $-u^*$. A response target indexed by the query therefore moves with it: the target for $+u^*$ in the original episode becomes the target for $-u^*$ in the reflected one.

**Assumption S (symmetric data-generating process).** The distribution of $(g, |b|)$ does not depend on the sign of $b$, which is $\pm$ with probability one half; the overall sign of each probe is drawn independently of $b$ with probability one half; the initial state, the hold and the set of queries are unchanged by reflection; and sensor noise has the same law after reflection.

Under Assumption S the joint law of histories, queries and outcomes is unchanged by $M$, and the best squared-error predictor is equivariant (Proposition 0, Appendix A). Equivariance is therefore consistent with optimal prediction here; the failures below come from what a model may do with mirror-symmetric evidence, how training spends capacity, and how information flows through memory and the response head.

### 2.3 Episodes

1. **Probe.** From a canonical rest state ($x = \dot x = 0$, $q_L = q_R = a$), the controller applies a fixed pattern of alternating differential pulses with a random overall sign.
2. **Hold.** A fixture returns the cart to the canonical position and holds it at rest with $u = 0$ for a hold of length $D$. The model's memory is kept. The only physical trace of the probe is the activation difference, which decays with time constant $\tau \approx 0.1$ s; after a one-second **washout**, the observations no longer depend on $b$ to numerical precision.
3. **Query.** The fixture releases the cart at the canonical state, and a constant differential command $u^*$ is applied for $H = 0.5$ s. The model predicts the response open-loop, from its memory at the query origin, without seeing any query-phase observation.

**The target.** The total-force impulse during the query is $J(u^*) = 2gaH + 2bu^*\kappa$, with $\kappa = H - \tau(1 - e^{-H/\tau})$. The **query contrast** is half the difference between responses to $+u^*$ and $-u^*$ from the same saved state,

$$r = \tfrac12\left[J(+u^*) - J(-u^*)\right] = 2bu^*\kappa.$$

The simulator computes it from two branches cloned from one saved state. A model computes its predicted contrast $\hat r$ from two copies of its memory at the query origin, and a stochastic model uses **one** sampled body for both branches, since they describe the same body. The pair $\{+u^*, -u^*\}$ is mapped to itself by reflection, so the sum of the two responses is even and the contrast is odd. This is how parity enters a target built entirely from even observations.

## 3. Four ways to lose the hidden side

Proofs are in Appendix A. The assumptions are deliberately simple, and the experiments ask whether the predicted signatures appear in trained nonlinear models.

### M1. Symmetry

**Proposition 1.** *If $f$ is deterministic and equivariant and $Mx = x$, every odd component of $f(x)$ is zero. In particular, for a passive history (all observations even, $u \equiv 0$), a deterministic equivariant model predicts zero query contrast. A stochastic equivariant model is only required to have a reflection-invariant predictive distribution, which may place equal probability on two asymmetric bodies.*

For passive histories, zero contrast is the correct *mean*, so squared error cannot reveal the problem, and passive histories contain no information about the sign, so retention measures do not apply. The cost lies in the joint distribution of the two query branches. For the true system, the pair $(J(+u^*), J(-u^*))$ is either $(\bar J + r, \bar J - r)$ or $(\bar J - r, \bar J + r)$ with equal probability: two points, perfectly anti-correlated. A model with a deterministic latent state and a Gaussian output head can at best match the mean and covariance of this pair; a stochastic latent body shared by both branches can reproduce the two points. M1 is therefore measured with the **energy score** of the predicted joint pair, a proper score that rewards a predictive distribution for matching both location and shape (Gneiting and Raftery, 2007).

*Signature:* on passive histories the stochastic equivariant model attains a lower energy score than the strongest deterministic-latent competitor (one with a full-covariance Gaussian head over the branch pair), and its rollouts form two clusters at $\pm r$. *Knobs:* passive versus probed histories (data) and deterministic versus stochastic latent context (model).

### M2. Capacity

**Proposition 2.** *Let $y$ be a vector of future quantities to be predicted, split into an even part $y_e$ and an odd part $y_o$ (with query-indexed targets transformed as in Section 2.2), and let $s = (s_e, s_o)$ be a parity-split statistic of the history. Among linear predictors $\hat y = Ws$ of rank at most $k$, the squared-error optimum keeps the $k$ leading eigenvectors of the covariance $C$ of the best linear prediction (Izenman, 1975). Under Assumption S, $C$ is block-diagonal in even and odd parts, so every retained direction is purely even or purely odd, and the odd target is predicted as zero whenever all eigenvalues of the odd block lie below the $k$-th largest eigenvalue of the even block.*

The Codex review of version 2 pointed out that the cart alone cannot create competition: for a fixed query, the predictable response depends only on $(g, b)$, so its predictable part has rank at most two. We therefore add **predictable distractor channels** to what the model must predict. Each is an observed slow oscillation, independent of the body and commands, whose future over the query window can be forecast from its past; its predictable variance is set by design. With $n_d$ distractors of predictable variance $\lambda_d$ each, the odd contrast has eigenvalue $\lambda_o = (2u^*\kappa)^2\,\mathrm{Var}(\mathbb E[b \mid H])$, and a width-$k$ linear predictor drops it as soon as the number of even directions with eigenvalue above $\lambda_o$ (distractors plus the common gain) reaches $k$. This gives an exact phase boundary in the plane of distractor variance and width, which we test with widths 1, 2, 3, 5 and 9 and $n_d = 8$.

A second, purely physical knob is the **even spread**, the range of the common gain $g$. The leading even eigenvalue is $\lambda_e = (2aH)^2\,\mathrm{Var}(\mathbb E[g \mid H])$. With a rank-one predictor and the planning values ($a = 0.6$, $u^* = 0.25$, $H = 0.5$ s, $\tau = 0.1$ s, $|b|$ uniform on $[0.1, 0.3]$), the contrast is dropped once $g$ is spread more widely than about $\pm 0.12$ around 1, although the asymmetry remains just as easy to infer.

**What existing theory says about objectives.** Littwin et al. (NeurIPS 2024) analyze deep linear networks and show that JEPA-style latent prediction favors features with large *regression coefficients* from input to target, while reconstruction favors features with large variance. The relevant coefficient must be derived for the actual training pair. If the probe evidence is $X = sb + \varepsilon$ with noise variance $\sigma^2$ and the response is $Y = tb$, the coefficient is

$$\frac{st\,\mathrm{Var}(b)}{s^2\,\mathrm{Var}(b) + \sigma^2},$$

which approaches $t/s$, independent of the size of the asymmetry, when the probe is informative ($s^2\mathrm{Var}(b) \gg \sigma^2$), and falls to zero when it is not. In the informative regime the asymmetry feature therefore has small variance but an unchanged regression coefficient, which is the situation in which Littwin et al.'s result favors latent prediction. Their analysis assumes deep linear encoders, particular objectives and simultaneously diagonalizable covariances (their Assumption 4.1), which a recurrent, nonlinear, regularized world model does not satisfy. We test the prediction in two places: a controlled deep-linear experiment built to meet their assumptions, where it is a theoretical prediction, and the nonlinear world models, where it is an empirical hypothesis.

*Signature:* the contrast skill (Section 5) falls across the predicted phase boundary for linear predictors and near it for narrow nonlinear ones; reconstruction objectives lose the contrast at fewer distractors than latent prediction in the informative regime; normalizing even and odd parts of the loss by their own variances moves the boundary. *Knobs:* predictable distractors, unpredictable (white) distractors, even spread, fraction of training episodes containing probes, latent width, objective.

### M3. Memory

**Proposition 3.** *Suppose that during the hold, after washout, the observations are independent of $b$ (Assumption H), and that the model's predictive distribution for those observations does not depend on the odd part $z_o$ of its state. Then losses computed on hold observations have zero gradient with respect to $z_o$. Any training signal that rewards keeping $z_o$ must come from losses computed after the hold, passed back through the state updates across the hold. If the odd part of the update is linear with spectral radius $r < 1$, the stored value and that signal both shrink like $r^D$ over $D$ steps.*

The statement concerns hold losses only. Losses on query-phase observations do depend on $b$ and do reward retention, as the Codex review noted, so the experiments separate them explicitly (Section 7.3).

*Signature:* models trained only on probe and hold losses lose the contrast as the hold lengthens; adding query-phase losses slows the loss; truncating backpropagation to fewer steps than the hold removes the benefit; a persistent slot with an identity update prevents it. *Knobs:* hold length, which losses are present, truncation length, persistent slot.

### M4. Coupling

**Proposition 4.** *Let a response head predict an even query outcome directly from the frozen origin state $z$ and the query, and suppose it is additively separable in state and odd command, $\hat y_e = g_1(z_e, z_o, a_e) + g_2(a_e, a_o)$. If the head is equivariant, $g_1$ is even in $z_o$, $g_2$ is even in $a_o$, and the predicted contrast is zero for every state.*

The statement covers a direct response head only. In a rollout, a nonlinear transition can create the interaction $b \cdot u$ inside the latent state, and an additive decoder can then read it, so the proposition says nothing about rollout models. For those, the question is empirical: does explicit multiplicative fusion learn the interaction from less data than generic concatenation?

*Signature:* with a frozen origin state and an additive head, readouts recover $b$ while the contrast is zero; with a multiplicative head it is recovered. In rollout models, multiplicative fusion reaches a given contrast skill with fewer training episodes. *Knob:* fusion type.

**A shared cost.** If two equally likely histories with conditional mean responses $m_+$ and $m_-$ at the same query are mapped to the same memory state, the best shared prediction is their midpoint, with excess squared error $(m_+ - m_-)^2/4$ (Lemma A1). Each mechanism, when it merges a left-stronger and a right-stronger history, costs this amount.

## 4. The benchmark

### 4.1 Knobs that leave availability fixed

| Knob | Values | Mechanism | Changes | Leaves fixed |
|---|---|---|---|---|
| Probe present | passive / probed | M1 | Whether the history is mirror-symmetric | Body distribution |
| Predictable distractors | variance scale $\lambda_d$ in 6 steps spanning the predicted boundary; $n_d = 8$ | M2 | Competing predictable variance | Body, probe, noise |
| White distractors | 0, 8, 32 channels of high-variance noise | M2 | Unpredictive input variance (affects reconstruction) | Body, probe, noise |
| Even spread | half-width of $g$ range: 0, 0.05, 0.1, 0.15, 0.2, 0.3 | M2 | Predictable variance of the even response | Distribution of $b$, probe, noise |
| Probe frequency in training | 100%, 30%, 10% | M2 | How often the contrast appears in training | Test episodes always probed |
| Latent width | 1, 2, 3, 5, 9 (linear); 8, 16, 64 (nonlinear) | M2 | Capacity | Data |
| Hold length | 0, 2, 4, 8 s | M3 | Time the information must survive | Evidence at hold onset |
| Hold flag visible | yes / no | M3 | Whether the model is told when evidence ends | Data |
| Losses present | probe+hold; +teacher-forced query steps; +open-loop query | M3 | Which losses reward retention | Data |
| Response head | additive / multiplicative | M4 | Whether odd state meets odd command | Data |
| Population balance | $P(b > 0) = 0.5$, 0.7, 0.9 | Secondary | Whether Assumption S holds | Per-body physics |

Distractor channels are even or odd: odd distractors change sign under reflection and compete with the asymmetry inside the odd block. The population-balance knob violates Assumption S on purpose. When left-stronger bodies are more common, exact equivariance forces a 50:50 belief under passive histories although the correct belief is 70:30 or 90:10, and mirror augmentation imposes the same error on an unconstrained model, as studied for distributional symmetry breaking by Lawrence et al. (ICLR 2026).

### 4.2 Exact references

**Cart.** In the main condition, $\tau$, $m$, $k$ and $c$ are known constants and $(g, b)$ are unknown. Because the commands and $\tau$ are known, the activations are known functions of time, every observation is linear in $(g, b)$, and the posterior under Gaussian noise follows from a two-parameter linear regression. It is evaluated on a grid over the bounded prior, and halving the grid spacing must change the posterior mean of $b$ by less than 1% of its prior range. A secondary condition with unknown $\tau$ and $m$ integrates $(g, b)$ out exactly and samples $(\tau, m)$ by importance sampling, with reported Monte Carlo error. Distractors are independent of the body and do not enter the posterior over $(g, b)$; the reference forecasts them with their known generating model.

**Walker.** With every parameter except $b$ fixed and known, a canonical start and Gaussian sensor noise, the harnessed probe can be simulated for each value on a grid of $b$, which gives the exact likelihood of the observed history up to integrator tolerance. The Bayes predictor of the query contrast is the posterior average of the simulated contrast on that grid.

**Information references.** The full-history posterior; a **recent-window** posterior that uses only the last second of the hold, evaluated at holds of two seconds or more so that the window starts after washout; and a **no-probe** posterior from episodes with the probe replaced by zero command. A reference given values the models cannot see is labeled privileged and used only as a ceiling.

### 4.3 The walker tier

The dm_control planar walker (Tassa et al., 2018) has hip, knee and ankle motors on two legs. Its knee gains are scaled by $1+b$ (left) and $1-b$ (right). Episodes copy the cart's structure.

1. **Harnessed probe.** The torso is held by a harness while differential knee pulses are applied with the feet off the ground.
2. **Harnessed hold.** The legs are reset to a canonical hanging pose and all commands are zero; zero commands make the gains irrelevant, and the reset removes any swing left by the probe.
3. **Released query.** The walker is placed in a canonical standing pose and released, and a 0.5 s open-loop command sequence $a_{\text{nom}}(t) + u^* d(t)$ is applied, where $a_{\text{nom}}$ is a fixed bilateral push-off pattern identical on both sides and $d(t)$ raises the left knee command and lowers the right. Reflection maps $u^*$ to $-u^*$.

The model observes joint angles and velocities for both legs, torso pose and total vertical ground force. The **walker endpoint** is the contrast in total vertical ground impulse between $+u^*$ and $-u^*$, divided by body weight times $H$ so that it is dimensionless. As in the cart, a stronger left knee under a left-favoring command adds extension force, so the contrast is approximately proportional to $b u^*$. A week-2 feasibility check confirms that the released query does not fall within 0.5 s and that the contrast varies monotonically with $b$; otherwise the push-off pattern is revised before data generation.

A secondary **walking** condition replaces the hold with walking under a fixed feedforward policy trained on separate symmetric bodies. Walking with unequal knees reveals $b$ continuously, so this condition measures how much a model relies on stored evidence when fresh evidence is available, and it is reported separately.

## 5. Measurements

**Primary endpoint: contrast skill.** For each model, let $R_{\text{model}} = \mathbb E[(\hat r - r)^2]$ over test episodes at a given hold, $R_0 = \mathbb E[r^2]$ the risk of always predicting zero contrast (a symmetric body), and $R_{\text{Bayes}}$ the risk of the exact Bayes predictor from the same histories. The contrast skill is

$$S = \frac{R_0 - R_{\text{model}}}{R_0 - R_{\text{Bayes}}}.$$

It equals 1 when the model's contrast predictions are as good as the data allow, 0 when they are no better than a symmetric body, and is negative when they are worse than a symmetric body, which is how the zero-change result in the user's JEPA study would register. Because the Bayes predictor minimizes squared error given the history, $S \le 1$ in expectation. A model that scales up the Bayes predictions by a factor $c \ne 1$ loses skill, which the retention ratio of version 2 failed to penalize. The primary analysis uses probed episodes and probe strengths at which $R_0 - R_{\text{Bayes}}$ is at least 80% of $R_0$, so the denominator is stable.

**Diagnostics.**
- *Calibration slope* $\beta = \sum_i \hat r_i r_i / \sum_i r_i^2$ with its residual error: values below 1 indicate shrinkage toward symmetry, above 1 amplification.
- *Frozen-state readouts* of the sign and value of $b$ at the end of the probe and after each hold, linear and two-layer, fit on training families with one readout shared across delays and one per delay. They measure *usable* information for each readout class (Xu et al., ICLR 2020); a failure marks the limit of the tested readouts.
- *Context interventions*, defined per representation class. For models with an explicit context slot, transplant the slot from a donor to a recipient body with the same command and noise sequences but a different $b$, and check whether the predicted contrast moves to the donor's. A *sham* transplant between bodies with the same $b$ should change nothing, and a *nuisance* transplant between bodies with the same $b$ and different $g$ should change only the even sum. For unconstrained models, move the state along the direction found by a trained readout and treat the result as exploratory. Flipping the odd block of a mirrored equivariant state is an algebraic identity and is not used as evidence.
- *Distributional scores:* energy score of the predicted branch pair, CRPS of each impulse, Brier score of the predicted probability that $b > 0$, coverage of 90% intervals.
- *Guardrail:* next-step prediction error during probe and hold.

## 6. Research question and hypotheses

**Research question.** By the ICML 2027 submission deadline (expected late January 2027, 13 weeks from now), can probe–delay–query episodes determine which of four mechanisms make standard world models lose a body's signed asymmetry, by showing for each mechanism that its knob changes contrast skill at an eight-second hold in the predicted direction while the available information stays fixed? And does a world model designed against all four reach a contrast skill of at least 0.9 on held-out bodies, with next-step error within 5% of the best baseline's?

A contrast skill of 0.9 means the model attains 90% of the improvement over a symmetric guess that the data allow. The 5% margin on next-step error ensures that any gain does not come from neglecting ordinary prediction.

| Hypothesis | Primary contrast (one per mechanism) | Predicted direction |
|---|---|---|
| H1 Availability | Recent-window and no-probe reference sign accuracy at holds ≥ 2 s | At chance |
| H2 Symmetry (M1) | Energy score of the branch pair on passive histories, deterministic-latent minus stochastic equivariant | Positive |
| H3 Capacity (M2) | Contrast skill above minus below the predicted distractor boundary, reconstruction objective, width 3 | Negative |
| H3b Objective (M2) | Same difference, latent prediction minus reconstruction, informative probes | Positive |
| H4 Memory (M3) | Contrast skill at 8 s minus 2 s, probe+hold losses only, no flag | Negative |
| H5 Coupling (M4) | Contrast skill with frozen origin state and additive head, given readout accuracy above 0.9 | Equivalent to zero within ±0.1 |

## 7. Models

### 7.1 Shared design

All learned models share a per-step observation encoder, a recurrent update, a response head, a latent width and a training budget, and differ along these axes.

- **Objective:** reconstruction of observations (DreamerV3-style); latent prediction of future encoder features with a slowly updated target encoder and a variance–covariance regularizer (JEPA-style), with physical responses read by a head trained on the same targets; or either plus response supervision.
- **Symmetry:** unconstrained; mirror augmentation with targets transformed as in Section 2.2; deterministic equivariant; stochastic equivariant with a two-component belief. The negative control is an invariant history encoder followed by a head that receives the query unreflected.
- **Memory:** ordinary recurrence, or recurrence with a persistent slot written through a learned gate.
- **Response head:** additive or multiplicative fusion.
- **Loss weighting:** raw, or even and odd parts each divided by their training variance.

Every model is trained with proper scores: next-step negative log-likelihood under a Gaussian head and the energy score of the predicted query-branch pair.

### 7.2 Baselines and references

A **snapshot** model stores its state at the hold onset and passes it to the response head; a **full-history transformer** attends over the whole episode; a **VariBAD-style** model keeps a Gaussian posterior over a task embedding updated at every step. A recent-window context model in the style of RMA is labeled information-restricted. The exact Bayes predictor and a privileged parameter oracle bound the achievable skill.

The **remedy model** combines a stochastic two-component belief, a persistent slot, multiplicative fusion, variance-normalized response loss and full backpropagation through the episode. Each component is removed in turn.

### 7.3 Losses and time masks

Each episode is split into four loss terms by time:

$$\mathcal L = \mathcal L_{\text{probe}} + \mathcal L_{\text{hold}} + \lambda_1\,\mathcal L_{\text{qstep}} + \lambda_2\,\mathcal L_{\text{qopen}},$$

where $\mathcal L_{\text{probe}}$ and $\mathcal L_{\text{hold}}$ are next-step losses on the probe and hold, $\mathcal L_{\text{qstep}}$ is teacher-forced next-step loss during the query (the model sees each query observation before predicting the next), and $\mathcal L_{\text{qopen}}$ is the open-loop query loss, predicting the whole query response from the origin memory. The M3 arms are: (A) $\lambda_1 = \lambda_2 = 0$, with no signal that rewards retention; (B) $\lambda_1 > 0$, $\lambda_2 = 0$, a weak signal, since query observations soon reveal $b$ again; (C) $\lambda_2 > 0$, the full signal; and (D) arm C with $\lambda_1 + \lambda_2$ equal to arm B's $\lambda_1$, which controls for total query weight. All non-M3 experiments use arm C. Query targets enter losses only and never the recurrent input during open-loop prediction; every model is reset at the start of each episode, and query branches start from copies of the same origin memory without updating one another.

## 8. The line of inquiry

**Loop 0: is the information there?** Run the references on probed and passive episodes at every hold. *Decision:* if the recent-window or no-probe reference is above chance at holds of two seconds or more, the hold leaks and the episode is redesigned before any model is trained.

**Loop 1: do standard world models keep it?** Train the reconstruction, latent-prediction, mirror-augmented and deterministic equivariant baselines at default settings and measure contrast skill against hold length. *Decision:* if every baseline reaches $S \ge 0.9$, the preregistered knob grid of Section 4.1 maps the conditions under which they fall below it, and the paper becomes a map of where standard practice suffices. If some fail, Loop 2 asks why. The knob grid is fixed in advance in both cases, so the outcome of Loop 1 cannot steer which conditions are reported.

**Loop 2: which mechanism explains the loss?** Run the knob experiments for H2–H5 with their primary contrasts. *Decision:* a mechanism stays in the account only if its primary contrast survives adjustment for the family of mechanism tests; the others are reported as ruled out under these conditions.

**Loop 3: does the matching remedy repair it?** Add each remedy to the best baseline one at a time, then all together. *Decision:* if the snapshot or VariBAD baseline matches the full remedy, the contribution narrows to diagnosis, and the paper says so.

**Loop 4: does the account transfer?** Repeat Loops 0–3 in reduced form on the walker, and run the population-balance knob. *Decision:* a mechanism counts as general only if its signature reappears in the walker.

## 9. Pipeline, splits and leakage

A **body family** is one draw of body parameters together with its mirror twin. Every episode, probe variant, hold, branch, noise replicate and distractor draw from a family stays in that family.

| Step | What happens | What is preserved | Split and leakage guard |
|---|---|---|---|
| 1. Sample | Draw $(g, |b|)$; form the twin pair; draw probe signs and distractor seeds | Parameters, seeds, generator version | Families assigned to pilot, training, validation and test before any simulation |
| 2. Simulate | Probe, hold, query; clone the full state at the query origin for each branch | Native time step, SI units, named channels, shape `[episode, time, channel]` | Episodes and branches inherit the family's split; cloning checked by replaying identical inputs |
| 3. Window | Histories end at the query origin | No resampling or stretching; padding with masks | Query targets never in inputs; memory reset per episode; branches never update one another |
| 4. Normalize | Scale channels | Odd channels centered at zero with symmetric scales; transforms saved and invertible | Training statistics only |
| 5. Train and select | Fit models and readouts; tune | Channel order and time grid unchanged | Validation families only; walker policy trained on separate bodies |
| 6. Test | Score once | Same grid and units as targets | After every setting is frozen |

## 10. Statistics

Each mechanism has one primary contrast (Section 6), and H1–H5 with H3b form one family adjusted by the Holm procedure; H5 uses two one-sided tests of equivalence to zero within ±0.1. A pilot on separate families estimates the variance of each endpoint between test families and between training seeds; seeds (between 5 and 10) and test families are then sized jointly so that the 95% interval half-width for contrast skill is at most 0.03. If the compute cap prevents this, the study reports an insufficient-precision outcome instead of loosening the criterion. Intervals come from a two-way bootstrap that resamples families and seeds while keeping methods paired. The remedy succeeds if the lower 95% bound of its contrast skill is at least 0.9, its difference from the validation-selected best baseline is above zero, and the upper 95% bound on its relative increase in next-step error is below 5%. Crashed fits and non-finite predictions count against the model that produced them.

## 11. Plan and resources

Weeks 1–2: simulators, references, Loop 0, training-cost pilot, walker feasibility check. Weeks 3–4: Loop 1. Weeks 5–7: Loop 2. Weeks 8–9: Loop 3. Weeks 10–11: Loop 4. Weeks 12–13: final test, analysis and writing. Planning figures are 4,000 training, 500 validation and 1,000 test families for the cart, about 120 GPU-hours for the cart and 90 for the walker, under a cap of 250.

## 12. Limitations

All results are in simulation. The formal statements assume linear predictors (M2), an uninformative hold (M3), a direct response head (M4) and Assumption S. The experiments test whether their signatures appear in trained nonlinear models. A clean map of where standard practice suffices is a useful outcome in its own right.

## Appendix A. Proofs

**Proposition 0.** Under Assumption S, $(MH, Mq, MY)$ has the same law as $(H, q, Y)$, so $\mathbb E[Y \mid Mh, Mq_0] = \mathbb E[MY \mid h, q_0] = M\,\mathbb E[Y \mid h, q_0]$ by linearity of $M$.

**Proposition 1.** $f(x) = f(Mx) = Mf(x)$, and $M$ negates odd components, so they vanish. For a passive history $h$, $Mh = h$ and $M(h, +u^*) = (h, -u^*)$; total force is even, so $\hat J(h, -u^*) = \hat J(h, +u^*)$ and $\hat r = 0$. For a stochastic model, $p(\cdot \mid x)$ equals its own reflection when $Mx = x$, a constraint on the distribution and not on each sample.

**Proposition 2.** The rank-$k$ squared-error optimum is $W = P_k\Sigma_{ys}\Sigma_{ss}^{-1}$, where $P_k$ projects onto the $k$ leading eigenvectors of $C = \Sigma_{ys}\Sigma_{ss}^{-1}\Sigma_{sy}$ (Izenman, 1975). Under Assumption S, $\mathbb E[y_e s_o^\top] = \mathbb E[y_e(-s_o)^\top] = 0$ and likewise for the other cross terms, so $\Sigma_{ys}$, $\Sigma_{ss}$ and $C$ are block-diagonal. Eigenvectors of a block-diagonal matrix with distinct eigenvalues lie within blocks.

**Proposition 3.** If the predictive distribution on hold observations does not depend on $z_o$, the hold loss is constant in $z_o$. Later losses reach $z_{o,t}$ through $\partial z_{o,T}/\partial z_{o,t} = A_o^{T-t}$ for a linear odd update $A_o$, whose norm is at most $c\,r^{T-t}$.

**Proposition 4.** Setting $a_o = 0$ in the equivariance condition gives $g_1(z_e, -z_o, a_e) = g_1(z_e, z_o, a_e)$; substituting back gives $g_2(a_e, -a_o) = g_2(a_e, a_o)$. Then $\hat y_e(+u^*) - \hat y_e(-u^*) = g_2(a_e, u^*) - g_2(a_e, -u^*) = 0$.

**Lemma A1.** The midpoint $c$ minimizes $\tfrac12(m_+ - c)^2 + \tfrac12(m_- - c)^2$, with value $(m_+ - m_-)^2/4$; outcome noise adds the same constant to every predictor.

**Regression coefficient.** For $X = sb + \varepsilon$, $Y = tb$, with $b$ and $\varepsilon$ independent and zero-mean, $\mathrm{Cov}(X, Y)/\mathrm{Var}(X) = st\,\mathrm{Var}(b)/(s^2\mathrm{Var}(b) + \sigma^2)$.

## Change log from version 2

- **Primary endpoint.** The retention ratio, which rewarded amplified predictions, is replaced by contrast skill relative to the symmetric and Bayes predictors; the slope becomes a calibration diagnostic.
- **M1.** Proper scores in training; one shared latent body across query branches; passive histories scored by the energy score of the branch pair, never by retention.
- **M2.** Predictable distractors with a known spectrum create capacity competition, with widths down to 1; even spread, probe frequency and white distractors leave the evidence about $b$ unchanged; the JEPA prediction is derived for the actual training pair and restricted to informative probes, with a deep-linear test.
- **M3.** Losses are separated by time masks, with a weight-matched control; the zero-gradient claim covers hold losses only.
- **M4.** The proposition is restricted to a direct response head on a frozen state; rollout models are compared empirically.
- **Walker.** A defined endpoint, a simulation-grid Bayes reference and a week-2 feasibility check.
- **Controls.** Correct negative augmentation control; recent window placed after washout; context interventions with sham and nuisance swaps.
- **Statistics.** Family and seed variance sized jointly, with an insufficient-precision outcome.
- **Structure.** Contributions stated; experiments organized as loops; change tracking moved out of the text.

## References

- Assran, M. et al. (2023). Self-supervised learning from images with a joint-embedding predictive architecture. *CVPR*. arXiv:2301.08243.
- Assran, M. et al. (2025). V-JEPA 2. arXiv:2506.09985.
- Bengio, Y., Simard, P. and Frasconi, P. (1994). Learning long-term dependencies with gradient descent is difficult. *IEEE Trans. Neural Networks* 5(2).
- Chen, Y. and Liu, Y. (2026). Compact but moving. arXiv:2609.21787.
- Gneiting, T. and Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. *JASA* 102(477).
- Hafner, D. et al. (2023). Mastering diverse domains through world models. arXiv:2301.04104.
- Izenman, A. J. (1975). Reduced-rank regression for the multivariate linear model. *J. Multivariate Analysis* 5(2).
- Kaba, S.-O. and Ravanbakhsh, S. (2023). Symmetry breaking and equivariant neural networks. arXiv:2312.09016.
- Kumar, A. et al. (2021). RMA. *RSS*. arXiv:2107.04034.
- Lan, K. et al. (2026). SWAP. arXiv:2606.19928.
- Lawrence, H. et al. (2025). Improving equivariant networks with probabilistic symmetry breaking. *ICLR*. arXiv:2503.21985.
- Lawrence, H. et al. (2026). To augment or not to augment? Diagnosing distributional symmetry breaking. *ICLR*. arXiv:2510.01349.
- Littwin, E. et al. (2024). How JEPA avoids noisy features. *NeurIPS*. arXiv:2407.03475.
- Ordoñez-Apraez, D. et al. (2025). Morphological symmetries in robotics. *IJRR*. arXiv:2402.15552.
- Saxe, A. M., McClelland, J. L. and Ganguli, S. (2014). Exact solutions to the nonlinear dynamics of learning in deep linear neural networks. *ICLR*. arXiv:1312.6120.
- Smidt, T. E., Geiger, M. and Miller, B. K. (2021). Finding symmetry breaking order parameters with Euclidean neural networks. *Phys. Rev. Research* 3, 012002.
- Tassa, Y. et al. (2018). DeepMind control suite. arXiv:1801.00690.
- Xu, Y. et al. (2020). A theory of usable information under computational constraints. *ICLR*. arXiv:2002.10689.
- Zintgraf, L. et al. (2020). VariBAD. *ICLR*. arXiv:1910.08348.
