# A Signed-Belief World Model, and the Baselines That Could Explain It Away

**Version 4 · Research proposal · 23 October 2026**
**Status:** plan only; no models have been trained. Revised after [Review 3](../../output/research-claude/review-v03.md) and its Codex adversarial review. Version 3 defined the benchmark and four mechanisms. This version specifies the remedy model completely and adds the strongest competing remedies as baselines, with every budget matched. It also corrects several mechanism tests that could not identify what they claimed: symmetry now concerns the family and persistence of the predictive distribution, capacity is tested by an exact linear experiment, memory is tested with every arm's response readout trained equally, and coupling is tested through sample efficiency. Each hypothesis now has three possible outcomes. A change log is at the end.

## Abstract

World models learn to predict how a system responds to actions, and robot learning increasingly builds left–right symmetry into them. A symmetric body plan does not guarantee a symmetric body. A stronger side often stays hidden until an input pushes the two sides differently, and a model that must predict the response to such an input has to infer the asymmetry from brief evidence, keep it through uninformative stretches, and combine it with the new command. We describe four ways this can fail (a predictive distribution that cannot represent an undecided but persistent body, competition for capacity, an unrewarded memory, and a hard-to-learn interaction between context and command), each with a formal statement and a measurable signature. Probe–delay–query episodes switch each failure on and off while the information in the data stays fixed. Against this benchmark we specify a signed-belief world model: its internal state is split into parts that do and do not change sign under reflection, it accumulates evidence about the asymmetry in a persistent slot, it holds a two-sided belief that can stay undecided or commit, and it lets that belief multiply the command. The model is compared with reconstruction-based and latent-prediction world models, with existing ways of breaking symmetry in equivariant networks, and with baselines that simply store their state when the evidence ends, under matched budgets and against exact Bayesian references.

## 1. Introduction

A world model is a learned simulator. Given the history of observations and a planned sequence of actions, it predicts what will happen, so that a controller can test an action before committing to it. For legged robots, exoskeleton users and prosthesis wearers, the answer to "what happens if I push harder on the left?" depends on how strong each side is, which ordinary motion can hide.

Symmetry is one of the most effective tools in robot learning. Morphological symmetries constrain a robot's dynamics and can be built into learned models (Ordoñez-Apraez et al., 2025), and equivariant world models such as SWAP (Lan et al., 2026) use left–right symmetry to learn faster and generalize to mirrored terrain. These priors describe the body *plan*. A particular body can break the symmetry through a weak motor, a payload, a brace or a stroke, and the question is whether a model built around symmetry can still represent, keep and use the difference.

The user's earlier work gives a reason to ask. In a study of JEPA-inspired pose restoration, a baseline that always predicted zero change in knee asymmetry had lower asymmetry-change error than all sixteen trained variants, which nonetheless restored noisy poses well. Heavy failure penalties may explain part of the gap, and the study does not show that any representation erased asymmetry. It does show that a model can improve on the large symmetric part of a target while doing worse than a symmetric guess on its small signed part.

**Contributions.**

1. A diagnostic account of four mechanisms by which a predictive model can lose a signed asymmetry, each with a formal statement under explicit assumptions and a signature that can be measured (Section 3).
2. Probe–delay–query episodes, a benchmark in which each mechanism has its own knob while the evidence about the asymmetry stays fixed, scored by *contrast skill* against exact Bayesian references (Sections 4–5).
3. A signed-belief world model that addresses each mechanism with one removable component (Section 7).
4. A controlled comparison with reconstruction-based and JEPA-style world models, with SymPE-style probabilistic symmetry breaking and approximately equivariant networks, and with snapshot and belief-state baselines, under matched parameters, storage, updates and tuning (Section 8).

The study runs as a sequence of decisions (Section 9): confirm that the data contain the asymmetry, test whether standard world models keep it, find which mechanism explains any loss, test whether the matching component repairs it, and check whether the account transfers to a walking body.

## 2. Setting

### 2.1 The two-motor cart

A cart is pushed by a left motor with gain $g+b$ and a right motor with gain $g-b$, with $g > |b|$, so $b$ is positive when the left motor is stronger. A common command $a$ drives both motors, and a differential command $u$ raises the left command and lowers the right. Each activation follows its command through a lag, $\tau\dot q_L = a+u-q_L$ and $\tau\dot q_R = a-u-q_R$, and the forces are $F_L = (g+b)q_L$ and $F_R = (g-b)q_R$. Because the commands are symmetric about $a$, the activation sum stays at $q_L + q_R = 2a$ once the canonical state is reached, and writing $d(t) = q_L - q_R$ for the activation difference gives

$$F_+ = 2ga + b\,d(t).$$

The cart obeys $m\ddot x = F_+ - kx - c\dot x$. Sensors report position, velocity and total force with Gaussian noise; individual motor forces are never observed. With $u = 0$, $d$ decays to zero and total force is $2ga$ for either sign of $b$, so passive observation cannot tell which side is stronger. A differential probe makes $d(t)$ nonzero and changes the total by $b\,d(t)$, so it reveals the sign.

### 2.2 Reflection and parity

A mirror reflection $M$ swaps left and right. **Even** quantities are unchanged (total force, position, velocity, $a$, $g$) and **odd** quantities change sign ($b$, $u$, $d$). The product of two odd quantities is even, which is how $b\,d$ enters the total force. A function is **equivariant** if $f(Mx) = Mf(x)$ and **invariant** if $f(Mx) = f(x)$. Reflecting an episode leaves every observation unchanged, negates every differential command, and exchanges the query $+u^*$ with $-u^*$, so a query-indexed target moves with its query.

**Assumption S (symmetric data-generating process).** The distribution of $(g, |b|)$ does not depend on the sign of $b$, which is $\pm$ with probability one half; each probe's overall sign is drawn independently of $b$ with probability one half; the initial state, hold and query set are unchanged by reflection; and sensor noise has the same law after reflection. Under S, the best squared-error predictor is equivariant (Proposition 0, Appendix A).

### 2.3 Episodes, target and point prediction

1. **Probe.** From a canonical rest state ($x = \dot x = 0$, $q_L = q_R = a$), a fixed pattern of alternating differential pulses with a random overall sign. The pattern is balanced, $\sum_t d(t) = 0$, which Section 4.2 uses.
2. **Hold.** A fixture returns the cart to the canonical position and holds it with $u = 0$ for a hold of length $D$, while the model's memory is kept. The activation difference decays with $\tau \approx 0.1$ s, and after a one-second washout the hold observations no longer depend on $b$.
3. **Query.** Release at the canonical state and a constant differential command $u^*$ for $H = 0.5$ s, predicted open-loop from the memory at the query origin.

The query impulse is $J(u^*) = 2gaH + 2bu^*\kappa$ with $\kappa = H - \tau(1 - e^{-H/\tau})$, and the **query contrast** is $r = \tfrac12[J(+u^*) - J(-u^*)] = 2bu^*\kappa$. The simulator computes it from two branches cloned from one saved state.

**A model's point prediction** is its predictive mean contrast. A stochastic model draws $N$ samples of the body; each sample is used for *both* branches, giving one sampled contrast, and $\hat r$ is the average of the $N$ sampled contrasts. Scoring a single sample against $r$ would penalize an exact posterior sampler with twice the Bayes risk, so individual samples are reserved for distributional scores. $N$ is fixed before testing at a value for which doubling it changes contrast skill on validation by less than 0.005.

## 3. Four ways to lose the hidden side

Each mechanism is stated first in plain words and then formally; proofs are in Appendix A.

### M1. The predictive distribution must represent an undecided but persistent body

*In words:* when the evidence favors neither side, the right prediction is "one of two mirror-image bodies, and the same body throughout". A deterministic point prediction cannot say this, and neither can a unimodal distribution or one that redraws the body at every step.

*Proposition 1.* If $f$ is deterministic and equivariant and $Mx = x$, every odd component of $f(x)$ is zero; for a passive history, a deterministic equivariant point predictor gives zero contrast. An equivariant predictive distribution need only be reflection-invariant, which allows two modes of opposite contrast.

The Codex review of version 3 showed that this is a statement about the *output family*, not about where the randomness lives: a deterministic latent state feeding an equivariant mixture head over the joint branch pair can represent the same two modes as a sampled latent body. What separates the designs is persistence. Over a multi-step rollout, a per-step mixture head redraws its component at each step and so mixes bodies across time, while a body drawn once at the origin stays fixed. Under the actual prior, with $|b|$ continuous on $[0.1, 0.3]$ and $g$ uncertain, the passive predictive law of the branch pair is not two points: the contrast is spread over two intervals of opposite sign and the sum spreads with $g$. The two-point picture is exact only when $|b|$ and $g$ are fixed, and the benchmark includes that case as an illustration.

*Signature:* on passive histories, unimodal heads score worse than bimodal ones on the energy score of the branch pair; among bimodal models, those that redraw the body at each step score worse on the energy score of whole query trajectories than those that draw it once. *Knobs:* passive versus probed histories; output family (Gaussian, joint mixture, per-step mixture, persistent draw).

### M2. Capacity: a small signed response can be the first to go

*In words:* when a model must squeeze many predictable quantities through limited capacity and is trained by squared error, it keeps the quantities with the most predictable variance, and a small signed response can be dropped although it is perfectly predictable.

*Proposition 2.* Among linear predictors $\hat y = Ws$ of rank at most $k$ trained by squared error, the optimum keeps the $k$ leading eigenvectors of $C = \Sigma_{ys}\Sigma_{ss}^{-1}\Sigma_{sy}$, the covariance of the best linear prediction (Izenman, 1975). Under S, $C$ is block-diagonal in even and odd parts, so the odd target is predicted as zero whenever all odd eigenvalues lie below the $k$-th largest even one.

The proposition applies only to the inputs and loss it names, so the exact test is a linear experiment with an explicit statistic. With a balanced probe, the odd statistic $s_o = \sum_t d(t) F_{+,t}$ equals $b\sum_t d(t)^2$ plus noise, for either probe sign, and the even statistic $s_e$, the mean total force during the hold, equals $2ga$ plus noise. Raw observations alone would not do: with a random probe sign, each raw channel has zero covariance with $b$, and only the product with $d(t)$ identifies it. The statistic is completed by the recent values of $n_d = 8$ predictable distractor channels, slow oscillations with designed variance and known one-step regression coefficient. The target vector holds the branch sum, the contrast and the distractors' future values. Under squared error, $C$ is computed in closed form, and the experiment checks reduced-rank regression against the predicted boundary across widths 1, 2, 3, 5 and 9 and six distractor variances. Nonlinear world models trained with likelihood and energy-score losses are separate empirical experiments, whose collapse points are compared with the linear boundary without being claimed to match it.

**Objectives.** Littwin et al. (NeurIPS 2024) show that in deep linear networks JEPA-style latent prediction learns features in an order governed by their input-to-target regression coefficients (with a dependence on cross-covariance in the learning times), while reconstruction is governed by variance. For the asymmetry feature the coefficient is $st\,\mathrm{Var}(b)/(s^2\mathrm{Var}(b) + \sigma^2)$, which approaches $t/s$ for informative probes. That alone does not decide an ordering: predictable distractors also have high coefficients. The deep-linear study (Section 8.4) therefore computes every feature's variance, cross-covariance and coefficient after preprocessing and derives the predicted learning order. It includes distractors with coefficients below, equal to and above the asymmetry's. The prediction that latent prediction keeps the asymmetry where reconstruction loses it is made only for distractors whose coefficients lie below the asymmetry's: white noise and weakly predictable channels.

*Signature:* reduced-rank regression drops the contrast exactly at the computed boundary; nonlinear models lose contrast skill as distractor variance rises; with low-coefficient distractors, reconstruction loses it before latent prediction. *Knobs:* distractor variance and coefficient, even spread, probe frequency in training, width, objective.

### M3. Memory: nothing during the hold rewards keeping the evidence

*In words:* while the hold reveals nothing about the asymmetry, losses on hold observations give no reason to keep it; only losses computed after the hold can teach the memory to hold on.

*Proposition 3.* If hold observations after washout are independent of $b$ given the rest of the history, and the model's predictions of them do not depend on the odd part $z_o$ of its state, hold losses have zero gradient with respect to $z_o$. Later losses reach $z_{o,t}$ through the product of state Jacobians across the hold. If the odd part of the update is linear with operator norm $\|A_o\| \le r < 1$, both the stored value and that signal shrink at least as fast as $r^D$. With only a spectral-radius bound, non-normal updates can amplify transiently before decaying, so the experiments also measure the Jacobian norms.

The independence condition fails if the hold refines a nuisance parameter that is coupled to $b$. Total force during the hold measures $g$ through $2ga$, and if the probe left the posteriors of $g$ and $b$ correlated, learning $g$ would sharpen $b$. The primary memory experiment therefore fixes $g$ at a known value, and every other condition reports an information audit (Section 4.2).

*Signature:* when the representation is shaped only by probe and hold losses, contrast skill read from the frozen state falls as the hold lengthens; adding post-hold losses slows the fall; truncating backpropagation to fewer steps than the hold removes the benefit; a persistent slot with an identity update prevents it. *Knobs:* hold length, which losses shape the representation, truncation length, persistent slot.

### M4. Coupling: the asymmetry must multiply the command

*In words:* the asymmetry changes total force only through its product with the differential command, so a model must form that product somewhere.

*Proposition 4.* An equivariant head that predicts an even query outcome from a frozen origin state and is additively separable in state and odd command predicts zero contrast for every state.

Codex pointed out that this result is a construction check: an additive head scores zero by design, so its failure says nothing about why a real model loses the asymmetry. In rollout models, any nonlinear transition can form the product inside the state. The mechanism question is therefore one of learnability: does a model that is given an explicit product $\kappa^- \odot u$ learn the response from fewer episodes than one that concatenates context and command and must discover the product? The additive head stays as an implementation control.

*Signature:* at matched recoverability of $b$ from the frozen state, multiplicative fusion reaches a contrast skill of 0.8 with fewer training episodes than concatenation. *Knob:* fusion type in the baseline architecture.

**A shared cost.** Merging two equally likely histories whose mean responses at the same query are $m_+$ and $m_-$ costs at least $(m_+ - m_-)^2/4$ in squared error (Lemma A1).

## 4. The benchmark

### 4.1 Knobs

| Knob | Values | Mechanism |
|---|---|---|
| Probe present | passive / probed | M1 |
| Output family | Gaussian / joint mixture / per-step mixture / persistent draw | M1 |
| Predictable distractors ($n_d = 8$) | variance in 6 steps spanning the linear boundary; coefficient below, equal to, above the asymmetry's | M2 |
| White distractors | 0, 8, 32 channels | M2 |
| Even spread (half-width of $g$ range) | 0, 0.1, 0.2, 0.3 | M2 |
| Probe frequency in training | 100%, 30%, 10% | M2 |
| Width | 1, 2, 3, 5, 9 (linear); 8, 16, 64 (nonlinear) | M2 |
| Hold length | 0, 2, 4, 8 s | M3 |
| Hold flag visible | yes / no | M3 |
| Losses shaping the representation | probe+hold; +teacher-forced query; +open-loop query; weight-matched | M3 |
| Fusion | concatenation / multiplicative (additive head as control) | M4 |
| Population balance $P(b > 0)$ | 0.5, 0.7, 0.9 | secondary |

Odd distractors change sign under reflection and compete with the asymmetry inside the odd block. The population-balance knob violates Assumption S on purpose: exact equivariance and mirror augmentation then force a 50:50 belief under passive histories although the correct belief is skewed (Lawrence et al., ICLR 2026).

### 4.2 Exact references and the information audit

**Cart.** With $\tau$, $m$, $k$ and $c$ known, every observation is linear in $(g, b)$: total force through $2ga + b\,d(t)$, and position and velocity as linear responses to it from a known state. The posterior under Gaussian noise follows from a two-parameter linear regression, evaluated on a grid whose spacing is halved until the posterior mean of $b$ moves by less than 1% of its prior range. A secondary condition with unknown $\tau$ and $m$ integrates $(g, b)$ exactly and samples $(\tau, m)$ by importance sampling. Distractors are forecast with their known model.

**Information audit.** Codex noted that a hold which cannot classify the sign on its own can still change what the whole history says about $b$, by sharpening $g$ when the probe left the two coupled. For every condition and hold length we therefore report the Bayes risk of the contrast given the full history, $R_{\text{Bayes}}(D)$, and the posterior correlation of $g$ and $b$ at the end of the probe. In the primary memory condition $g$ is known, so the hold cannot change the posterior of $b$, and the audit must show $R_{\text{Bayes}}(D)$ constant in $D$ to Monte Carlo precision. In other conditions, contrast skill is always normalized by the Bayes risk at the same hold, so any change in available information moves the denominator and not the model's score.

**Walker.** With all parameters except $b$ fixed, a canonical start and Gaussian sensor noise, the harnessed probe is simulated on a grid of $b$ to give the exact likelihood up to integrator tolerance; the Bayes contrast is the posterior average of simulated contrasts.

**Information references.** Full-history posterior; recent-window posterior from the last second of the hold, at holds of two seconds or more; no-probe posterior.

### 4.3 The walker tier

The dm_control planar walker (Tassa et al., 2018) gets knee gains $1+b$ (left) and $1-b$ (right). Episodes use a **harnessed probe** of differential knee pulses with the feet off the ground, a **harnessed hold** with the legs reset to a canonical hanging pose and zero commands, and a **released query**: from a canonical standing pose, a 0.5 s open-loop sequence $a_{\text{nom}}(t) + u^*d(t)$, where $a_{\text{nom}}$ is a symmetric push-off and $d(t)$ raises the left knee command and lowers the right. The model observes joint angles and velocities for both legs, torso pose and total vertical ground force. The endpoint is the contrast in total vertical ground impulse between $\pm u^*$, divided by body weight times $H$. A week-2 check confirms that the released walker stays upright for 0.5 s and that the contrast is monotone in $b$. A secondary **walking** condition, with a fixed policy walking during the delay and therefore revealing $b$ continuously, is reported separately.

## 5. Measurements

**Contrast skill (primary).** With $R_{\text{model}} = \mathbb E[(\hat r - r)^2]$ over test episodes, $R_0 = \mathbb E[r^2]$ for a model that always predicts a symmetric body, and $R_{\text{Bayes}}$ for the exact Bayes predictor at the same hold,

$$S = \frac{R_0 - R_{\text{model}}}{R_0 - R_{\text{Bayes}}}.$$

$S = 1$ is as good as the data allow, $S = 0$ is no better than a symmetric body, and $S < 0$ is worse than a symmetric body. The Bayes predictor minimizes squared error given the history, so $S \le 1$ in expectation, and over-confident or amplified predictions lose skill. The primary analysis uses probe strengths at which $R_0 - R_{\text{Bayes}} \ge 0.8\,R_0$. Contrast skill is estimated as a ratio of sums over test episodes, not a mean of per-episode ratios.

**What a loss of skill costs: the dial-a-force task.** Given the history, a controller must choose $u \in [-u_{\max}, u_{\max}]$ so that the query impulse changes from its $u = 0$ value by a target $\Delta J^*$ of random sign. It sets $u = \Delta J^*/(2\hat\gamma)$, where $\hat\gamma$ is the predicted contrast per unit command, clipped to the admissible range. The cost is the squared miss relative to the Bayes predictor's. A model that predicts the wrong sign misses by twice as much as a model that does nothing, and shrinkage leaves a proportional shortfall. This secondary endpoint translates contrast skill into control error.

**Diagnostics.**
- *Attenuation relative to the data:* the slope from regressing $\hat r$ on the Bayes mean $m(H)$. A slope of 1 means the model's predictions move one-for-one with what the data support; below 1 is loss, above 1 is amplification. The Codex review showed that regressing $\hat r$ on $r$ would mislabel the Bayes predictor itself as shrunk, since its slope is $1 - R_{\text{Bayes}}/R_0$.
- *Calibration:* regress $r$ on $\hat r$ with an intercept; a slope of 1 and intercept 0 mean the point predictions are calibrated.
- *Frozen-state readouts* of the sign and value of $b$ at probe end and after each hold (linear and two-layer, shared across delays and per delay, fit on training families), read as usable information for each readout class (Xu et al., ICLR 2020).
- *Context transplants* between bodies with matched command and noise sequences but different $b$, with sham transplants (same $b$) and nuisance transplants (same $b$, different $g$), validated by readouts.
- *Distributional scores:* energy score of the branch pair and of whole query trajectories, CRPS, Brier score of $P(b > 0)$, coverage of 90% intervals.
- *Guardrail:* next-step error during probe and hold.

## 6. Research question and hypotheses

**Research question.** By the ICML 2027 submission deadline (expected late January 2027, 13 weeks from now), can probe–delay–query episodes determine which of four mechanisms make standard world models lose a body's signed asymmetry, by showing for each that its knob changes the mechanism's primary endpoint in the predicted direction while the available information stays fixed? And does a signed-belief world model reach a contrast skill of at least 0.9 on held-out bodies, above the best validation-selected baseline, with next-step error within 5% of that baseline's?

**Three possible outcomes.** A failure to reject does not rule a mechanism out, since a real effect can be missed through seed variance or weak power. Each hypothesis is therefore classified as **supported** (the preregistered test rejects after adjustment), **excluded** (an equivalence test shows the effect is smaller than a preregistered meaningful size), or **inconclusive** (neither). Each endpoint has a meaningful-effect size and a precision target set from the pilot.

**Validity gate G.** Before any hypothesis is tested: recent-window and no-probe sign accuracy must be equivalent to chance within ±0.02 at holds of two seconds or more (two one-sided tests); in the primary memory condition, $R_{\text{Bayes}}(D)$ must be constant across holds within 1%; and on probed episodes the full-history reference must reach $R_0 - R_{\text{Bayes}} \ge 0.8\,R_0$. If the gate fails, the episode design is revised and nothing else is run.

| Hypothesis | Primary endpoint | Predicted direction | Meaningful effect |
|---|---|---|---|
| H2 (M1) | Energy score of the branch pair on passive histories: best unimodal head minus best bimodal head | Positive | 5% of the unimodal score |
| H2b (M1) | Trajectory energy score on passive histories: per-step mixture minus persistent draw | Positive | 5% |
| H3 (M2, linear) | Width at which reduced-rank regression drops the contrast, measured minus predicted | Zero (equivalence) | ±0 widths |
| H3n (M2, nonlinear) | Contrast skill at the highest minus lowest distractor variance, reconstruction, width 16 | Negative | 0.1 |
| H3b (M2, objective) | That difference, latent prediction minus reconstruction, low-coefficient distractors | Positive | 0.1 |
| H4 (M3) | Frozen-state contrast skill at 8 s minus 2 s, representation shaped by probe and hold losses only, no flag, $g$ known | Negative | 0.1 |
| H5 (M4) | Training episodes to reach contrast skill 0.8: concatenation minus multiplicative fusion, at matched readout recoverability | Positive | 25% fewer episodes |

H3 is a deterministic check of linear algebra and is reported exactly, outside the statistical family.

## 7. The signed-belief world model

The model has four components, one per mechanism, and each can be removed.

### 7.1 Parity-split layers

Every hidden vector is split into an even part and an odd part, $h = (h^+, h^-)$, on which reflection acts as $(h^+, h^-) \mapsto (h^+, -h^-)$. A linear layer is equivariant when it maps even to even and odd to odd, with a bias on the even part only. Nonlinearities follow the gated construction used in equivariant networks (Weiler et al., 2018): even units pass through any pointwise function, odd units are multiplied by an even gate, $h^- \mapsto h^- \odot \sigma(W_g h^+)$, and products of two odd vectors, $(Uh^-) \odot (Vh^-)$, feed even units. Any composition of these pieces is equivariant, and the product term is what lets odd information reach even outputs. The recurrent update is a GRU built from these layers, with even update and reset gates.

### 7.2 Evidence slot (for M3)

Alongside the recurrent state, the model keeps a persistent slot $c = (c^+, c^-)$ that accumulates evidence additively, $c_t = c_{t-1} + \gamma_t \odot \Delta_t$, where $\Delta_t$ is a parity-split increment and $\gamma_t \in [0,1]$ an even, learned gate. When the gate is closed, the slot is copied unchanged and its odd part does not decay. An additive accumulator matches how evidence about $b$ arrives in the cart: the statistic $\sum_t d(t) F_{+,t}$ is a running sum. The hold flag is given to every model or to none; the flag-free arm is primary.

### 7.3 Two-sided belief (for M1)

One small network $\psi$ is evaluated twice, on $(c^+, +c^-)$ and on $(c^+, -c^-)$. Evaluation $s \in \{+1, -1\}$ returns a logit $\ell_s$, a log-normal distribution for a positive magnitude $\rho$ and a distribution for the even context. Component $s$ has weight $\pi_s = e^{\ell_s}/(e^{\ell_+} + e^{\ell_-})$ and odd context $\kappa^- = s\rho$. Reflecting the slot negates $c^-$, which exchanges the two evaluations and negates the odd context, so the mixture is equivariant (Appendix A). Under passive histories nothing favors either evaluation, so the weights stay at one half; after a probe, the evidence in $c^-$ moves weight to one side. Small magnitudes remain possible, so nearly symmetric bodies are representable. The component labels are latent predictive variables, and calling component $+1$ "left stronger" is a claim the readouts and transplants must support.

### 7.4 Rollout and multiplicative fusion (for M4)

At the query origin the model draws one component and one magnitude per sample, holds them fixed for the whole imagined trajectory, and uses the same draw for both branches. The transition and decoder receive the product $\kappa^- \odot (Wu)$ of odd context and odd command as an even input, along with the even context and the recurrent state. Predicted observations never update the slot or the belief.

### 7.5 Training objective

Losses are separated by time,

$$\mathcal L = \mathcal L_{\text{probe}} + \mathcal L_{\text{hold}} + \lambda_1\,\mathcal L_{\text{qstep}} + \lambda_2\,\mathcal L_{\text{qopen}},$$

with next-step Gaussian negative log-likelihood on probe and hold, teacher-forced next-step loss during the query, and the energy score of the open-loop query trajectory pair. With two components, the expectation over components is computed exactly, including the cross-component terms of the energy score, so the weights receive exact gradients without a score-function estimator; magnitudes and context are reparameterized. Before distances are computed, each branch pair is rewritten as its sum (even) and contrast (odd), and each is divided by its training standard deviation. This **parity normalization** keeps the small contrast from being swamped by the large sum. Equal weights on sums and differences would only rescale ordinary error, since $(e_L+e_R)^2 + (e_L-e_R)^2 = 2(e_L^2+e_R^2)$, whereas dividing each by its own scale changes which errors the loss emphasizes. Training backpropagates through the whole episode.

**Memory arms.** For H4 the representation is shaped by one of four loss sets: probe and hold only; plus teacher-forced query steps; plus the open-loop query loss; and the last with total query weight matched to the second. Codex noted that removing every query loss would also leave a response head untrained, so that poor skill could reflect an untrained decoder. In every arm and at every hold, a response readout is therefore trained on the frozen origin state with gradients stopped at the memory, using the same targets and budget. H4 is scored on these readouts, and end-to-end query gradients are reported alongside.

## 8. Baselines and fairness

### 8.1 Registry

| ID | Model | What it tests |
|---|---|---|
| B1 | Reconstruction world model (DreamerV3-style recurrent state-space model) | Standard practice |
| B2 | Latent-prediction world model (JEPA-style, Section 8.3) | Objective (M2) |
| B3 | B1 with mirror augmentation, targets moved with their queries | Augmentation as approximate equivariance |
| B4 | Deterministic-latent equivariant model (SWAP-style) with a full-covariance Gaussian head over the branch pair | M1, unimodal |
| B4m | B4 with an equivariant two-component joint mixture head over the branch pair | M1, bimodal without a persistent draw |
| B5 | B4 with SymPE-style symmetry breaking: a random sign reflected with the input and shared by both branches and all rollout steps (Lawrence et al., ICLR 2025) | Strongest existing M1 remedy |
| B6 | Approximately equivariant model (Wang, Walters and Yu, ICML 2022) | Relaxed symmetry |
| B7 | Snapshot: B1 storing its state at the hold flag for the response head; flag arm only | Simplest memory fix |
| B8 | VariBAD-style belief over a task embedding (Zintgraf et al., 2020) | Existing belief-state approach |
| B9 | Full-history transformer | Uncompressed memory |
| R1 | Recent-window context model (RMA-style) | Information-restricted reference |
| R2 | Invariant history encoder with unreflected query | Negative control |
| R3 | Exact Bayes predictor; privileged parameter oracle | Ceilings |

B4m and B5 matter most for M1. B4m shows how far a bimodal output alone gets. B5's shared random sign gives an equivariant distribution that can be bimodal and persistent, much like the two-sided belief; the difference is that the signed belief's weights are computed from the evidence and its odd context lives in a slot that does not decay, while SymPE's sign is a uniform coin whose influence the network must learn to override. B7 exists only in the flag arm, so the signed-belief model is compared with it there.

### 8.2 Matched budgets

- **Persistent storage:** 80 values between steps (signed belief: 64 recurrent + 16 slot; others: 80 recurrent); B9's attention cache is disclosed as extra memory.
- **Parameters:** within 10% of the signed-belief model, by adjusting width.
- **Updates and data:** identical gradient updates, episode batches and query branches.
- **Supervision:** identical time-masked losses and weights, except in the memory arms, where the manipulation applies to every model in the arm.
- **Tuning:** eight configurations per model (four learning rates × two loss weights), chosen on validation families with one tuning seed.
- **Monte Carlo:** the same number of samples $N$ for every stochastic model's predictive mean.

### 8.3 The JEPA-style arm

A context encoder maps each observation window to an embedding; a target encoder of the same architecture is an exponential moving average of it. An action-conditioned recurrent predictor receives context embeddings and commands and predicts future target embeddings, trained by squared error in embedding space, with a variance–covariance regularizer against collapse (VICReg; Bardes, Ponce and LeCun, ICLR 2022) and SIGReg (Balestriero and LeCun, 2025) as a sensitivity analysis. Physical responses are read by a head trained on the same query targets in two variants: on a frozen encoder and predictor, and jointly.

### 8.4 The deep-linear experiment

A synthetic study built to satisfy Littwin et al.'s assumptions generates inputs and targets from independent latent factors with simultaneously diagonal covariances: a *common* factor (large variance, high coefficient; the analogue of $g$), a *signed* factor (small variance, coefficient $t/s$; the analogue of $b$ under an informative probe) and distractor factors whose coefficients are set below, equal to and above the signed factor's, at two variances each. Deep linear encoders of depth 1, 2 and 4, with small balanced initialization, are trained for a fixed horizon of $10^4$ steps with a JEPA objective (EMA target, linear predictor) and with reconstruction, at matched width and step size. For each factor, the predicted learning time is computed from Littwin et al.'s expressions, which depend on variance, cross-covariance and coefficient; the measured quantity is the step at which the factor's projection reaches half its final norm, and its final norm when the width cannot hold every factor. The prediction tested is the computed order, including the cases where it does not favor the signed factor.

## 9. The line of inquiry

**Loop 0: is the information there?** Run the references and the information audit. *Decision:* if gate G fails, revise the episode before any model is trained.

**Loop 1: do standard world models keep it?** Train B1–B4 at default settings and measure contrast skill against hold length. *Decision:* if every one reaches $S \ge 0.9$, the preregistered knob grid maps where they stop doing so, and the paper becomes a map of where standard practice suffices. If some fail, Loop 2 asks why. The knob grid is fixed in advance either way.

**Loop 2: which mechanism explains the loss?** Run the experiments for H2–H5 and the deep-linear study. *Decision:* each mechanism is reported as supported, excluded or inconclusive, and only supported mechanisms enter the explanation of Loop 1's failures.

**Loop 3: does the matching component repair it?** Add each component of the signed-belief model to the best baseline, then remove each from the full model. *Decision:* if B4m, B5, B7 or B8 matches the full model on contrast skill and the trajectory energy score, the contribution narrows to diagnosis and the paper says so.

**Loop 4: does the account transfer?** Repeat the key comparisons on the walker and run the population-balance knob. *Decision:* a mechanism counts as general only if its signature reappears in the walker.

## 10. Pipeline, splits and leakage

A **body family** is one draw of body parameters with its mirror twin; every episode, probe variant, hold, branch, noise replicate and distractor draw from it stays in it.

| Step | What happens | What is preserved | Split and leakage guard |
|---|---|---|---|
| 1. Sample | Draw $(g, \lvert b\rvert)$, form the twin pair, draw probe signs | Parameters, seeds, generator version | Families assigned to pilot, training, validation and test before any simulation |
| 2. Distractors | Generate distractor channels from family-specific seeds | Designed variance, coefficient and parity labels | Seeds never shared across families |
| 3. Simulate | Probe, hold, query; clone the full state at the query origin for each branch | Native time step, SI units, named channels, shape `[episode, time, channel]` | Branches inherit the family's split; cloning checked by replaying identical inputs |
| 4. Window | Histories end at the query origin | No resampling or stretching; padding with masks | Query targets never in inputs; memory reset per episode; branches never update one another |
| 5. Augment (B3 only) | Reflect an episode: negate $u$ and odd distractors, swap query labels | Shapes and units; targets move with their queries | Reflected copies stay in their source family's split |
| 6. Normalize | Scale channels | Odd channels centered at zero with symmetric scales; transforms saved and invertible | Training statistics only |
| 7. Train and select | Fit models and readouts; tune | Channel order and time grid | Validation families only; walker policy trained on separate bodies |
| 8. Test | Score once | Same grid and units as targets | After every setting is frozen |

## 11. Statistics

The statistical family is H2, H2b, H3n, H3b, H4 and H5; gate G and the exact check H3 are outside it. Superiority tests use the Holm procedure at a family-wise level of 0.05. Each "excluded" verdict uses two one-sided tests against the preregistered meaningful effect, also Holm-adjusted. A pilot on separate families estimates each endpoint's variance between test families and between training seeds, and seeds (5 to 10) and test families are sized jointly so that each primary interval's half-width is at most half its meaningful effect; if the compute cap prevents this, the endpoint is reported as underpowered. Intervals come from a two-way bootstrap over families and seeds with methods paired. The signed-belief model succeeds if the lower 95% bound of its contrast skill is at least 0.9, its difference from the validation-selected best baseline is above zero, and the upper 95% bound on its relative increase in next-step error is below 5%. Crashed fits and non-finite predictions count against their model.

## 12. Plan and resources

Weeks 1–2: simulators, references, information audit, gate G, training-cost pilot, walker feasibility. Weeks 3–4: Loop 1. Weeks 5–7: Loop 2 and the deep-linear study. Weeks 8–9: Loop 3. Weeks 10–11: Loop 4. Weeks 12–13: final test, analysis and writing. The cart needs roughly 120 GPU-hours and the walker 90, under a cap of 250; the linear studies run on a CPU.

## 13. Limitations

All results are in simulation. The propositions hold under their stated assumptions (linear predictors and squared error for M2, a conditionally uninformative hold and a contracting odd update for M3, a direct response head for M4, and Assumption S). Each component of the signed-belief model exists in some form; its contribution is to address the four mechanisms with one removable component each and to be tested against the strongest version of each alternative. If the snapshot, mixture-head or SymPE-style baseline matches it, that is the finding.

## Appendix A. Proofs

**Proposition 0.** Under S, $(MH, Mq, MY)$ has the law of $(H, q, Y)$, so $\mathbb E[Y \mid Mh, Mq_0] = M\,\mathbb E[Y \mid h, q_0]$.

**Proposition 1.** $f(x) = f(Mx) = Mf(x)$, so odd components vanish. For a passive history $h$, $M(h, +u^*) = (h, -u^*)$ and total force is even, so $\hat r = 0$. A stochastic model's distribution must equal its reflection when $Mx = x$; individual samples are unconstrained.

**Proposition 2.** The rank-$k$ optimum projects the least-squares fit onto the $k$ leading eigenvectors of $C = \Sigma_{ys}\Sigma_{ss}^{-1}\Sigma_{sy}$ (Izenman, 1975). Under S, even–odd cross-covariances vanish because $\mathbb E[y_e s_o^\top] = \mathbb E[y_e(-s_o)^\top]$, so $C$ is block-diagonal and, for distinct eigenvalues, its eigenvectors lie within blocks.

**Proposition 3.** A hold loss independent of $z_o$ has zero gradient with respect to it. Later losses reach $z_{o,t}$ through $A_o^{T-t}$, and $\|A_o^{n}\| \le \|A_o\|^{n} \le r^{n}$ under the operator-norm assumption. A spectral-radius bound alone does not give this: for $A_o = \begin{pmatrix} r & 1 \\ 0 & r\end{pmatrix}$ the off-diagonal entry of $A_o^n$ is $n r^{n-1}$.

**Proposition 4.** With $a_o = 0$, equivariance makes $g_1$ even in $z_o$; then $g_2$ is even in $a_o$, and $\hat y_e(+u^*) = \hat y_e(-u^*)$.

**Lemma A1.** The midpoint minimizes $\tfrac12(m_+ - c)^2 + \tfrac12(m_- - c)^2$, with value $(m_+ - m_-)^2/4$.

**Balanced-probe statistic.** With $q_L + q_R = 2a$, $F_{+,t} = 2ga + b\,d(t) + \varepsilon_t$, so $\sum_t d(t) F_{+,t} = 2ga\sum_t d(t) + b\sum_t d(t)^2 + \sum_t d(t)\varepsilon_t$, and the first term vanishes for a balanced probe. Reversing the probe sign negates $d$ and leaves $b\sum_t d(t)^2$ unchanged.

**Equivariance of the two-sided belief.** Write $q(\kappa \mid c) = \sum_s \pi_s(c)\,q_s(\kappa \mid c)$ with component $s$ computed from $\psi(c^+, s c^-)$. Under $c^- \mapsto -c^-$, evaluation $s$ becomes $\psi(c^+, -s c^-)$, the original evaluation $-s$, and the odd context $s\rho$ becomes $-s\rho$. Hence $q(M\kappa \mid Mc) = q(\kappa \mid c)$.

**Point prediction from samples.** If $\tilde r$ is a single draw from the exact posterior predictive and $m = \mathbb E[r \mid H]$, then $\mathbb E[(\tilde r - r)^2] = 2\,\mathbb E[\mathrm{Var}(r \mid H)] = 2R_{\text{Bayes}}$, since $\tilde r$ and $r$ are independent given $H$. Averaging $N$ draws gives $(1 + 1/N)R_{\text{Bayes}}$.

## Change log from version 3

**From Review 3.** The signed-belief model is specified (R1); SymPE-style and approximately equivariant baselines are added (R2); budgets are matched (R3); the JEPA arm (R4) and the deep-linear study (R5) are designed; the dial-a-force task gives contrast skill a physical meaning (R6); the validity gate is separated from the hypothesis family (R7); the pipeline table gains distractor and augmentation rows (R8); each mechanism opens with a plain-language statement (R10).

**From the Codex review of version 3.**
- M1 is restated as a requirement on the family and persistence of the predictive distribution; a deterministic-latent mixture head (B4m) is added; the passive law under the continuous prior is described correctly.
- Point predictions are predictive means over samples, each sample shared across branches, with a fixed Monte Carlo accuracy.
- M2's exact test is a linear experiment with an explicit balanced-probe statistic and squared error; nonlinear results are separate empirical experiments.
- The JEPA ordering is derived from every feature's variance, cross-covariance and coefficient, with distractors below, equal to and above the asymmetry's coefficient.
- An information audit reports Bayes risk across holds and the posterior coupling of $g$ and $b$; the primary memory condition fixes $g$.
- Every memory arm trains its response readout on the frozen state, so decoding is equalized.
- M4 is tested through sample efficiency; the additive head is an implementation control.
- Each hypothesis has three outcomes (supported, excluded, inconclusive), with meaningful effects, equivalence margins and precision targets.
- Attenuation is measured against the Bayes mean, and calibration by regressing outcomes on predictions.
- Proposition 3 assumes an operator-norm contraction and notes transient amplification.

## References

- Assran, M. et al. (2023). Self-supervised learning from images with a joint-embedding predictive architecture. *CVPR*. arXiv:2301.08243.
- Assran, M. et al. (2025). V-JEPA 2. arXiv:2506.09985.
- Balestriero, R. and LeCun, Y. (2025). LeJEPA. arXiv:2511.08544.
- Bardes, A., Ponce, J. and LeCun, Y. (2022). VICReg. *ICLR*.
- Bengio, Y., Simard, P. and Frasconi, P. (1994). Learning long-term dependencies with gradient descent is difficult. *IEEE Trans. Neural Networks* 5(2).
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
- Wang, R., Walters, R. and Yu, R. (2022). Approximately equivariant networks for imperfectly symmetric dynamics. *ICML*. arXiv:2201.11969.
- Weiler, M. et al. (2018). 3D steerable CNNs. *NeurIPS*. arXiv:1807.02547.
- Xu, Y. et al. (2020). A theory of usable information under computational constraints. *ICLR*. arXiv:2002.10689.
- Zintgraf, L. et al. (2020). VariBAD. *ICLR*. arXiv:1910.08348.
