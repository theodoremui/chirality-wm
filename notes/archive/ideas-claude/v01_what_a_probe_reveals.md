# What a Probe Reveals: Do World Models Keep a Body's Hidden Asymmetry?

**Version 1 · Research proposal · 23 October 2026**
**Status:** plan only; no models have been trained. This version responds to [Review 0](../../../output/research-claude/review-v00-sources.md) of the original proposal and the Codex revisions.

## Abstract

A world model is a learned simulator: given what has been observed so far and a planned sequence of actions, it predicts what will happen next. Such models are attractive for robots and assistive devices because they let a controller test an action before taking it. Their usefulness depends on whether the model's internal state contains the facts about the body that decide how it will respond. One such fact is easy to miss. A body whose left side is stronger than its right can move in a way that looks perfectly ordinary until an input pushes the two sides differently, and only then does the difference show. We propose a controlled study of whether predictive world models keep this kind of signed, persistent asymmetry after a brief probe has revealed it and the revealing evidence has passed out of view. The study separates three questions that are easily confused: whether the data contain the information at all, whether the learned state retains it, and whether the model uses it to predict a later response. We introduce a world model that holds an explicit two-sided belief about which side is stronger and compare it with standard recurrent world models and an exact Bayesian reference in two simulated bodies.

## 1. Why world models, and why asymmetry

Planning with a learned model works only if the model's predictions remain correct when the planner tries something new. A model trained to predict the next frame of ordinary walking can be very accurate on ordinary walking and still be wrong about what happens when an exoskeleton adds assistance to one leg. The question this proposal asks is what a world model must keep in its internal state to answer that second kind of question.

Asymmetry between the left and right sides of a body is a good place to study this. It is common in the bodies we most want to model: a person recovering from a stroke, a prosthesis user, a legged robot with a worn motor or an off-center payload. It is also hard to see. The sides of a walking body alternate, so their positions are never equal at the same instant, and a body can compensate for a weak side in ways that keep its overall motion regular. Finally, asymmetry interacts with a design habit that is spreading through robot learning. Practitioners routinely mirror their training data or build left–right symmetry into the network, because a body *plan* is symmetric and the trick halves the data needed. That habit is correct for the body plan, yet a particular body can break the symmetry, and a model that treats the two sides as interchangeable may have no place to store the difference.

The original proposal made a distinction that this version keeps at its center. Before asking whether a learned model has lost information about the asymmetry, one must first ask whether the experiment ever contained it. A model cannot be blamed for failing to retain what the measurements never revealed. We therefore treat the problem as three linked questions:

1. **Availability.** Does the recorded history contain enough information to tell which side is stronger? This is a property of the sensors and the inputs and can be answered without any neural network.
2. **Retention.** When it does, does the learned internal state still carry that information some time later, after the revealing measurements are gone?
3. **Use.** When the state carries it, does the model's prediction of a later response depend on it in the right direction and by the right amount?

## 2. The idea in one example

Consider a small cart pushed forward by two motors, one on the left and one on the right. The left motor has gain $g+b$ and the right has gain $g-b$, with $g > |b|$ so both gains are positive. The number $b$ is the asymmetry: positive when the left motor is stronger, negative when the right one is. The controller sends a common command $a$ to both motors and can add a differential command $u$ that raises the left command and lowers the right by the same amount. The two forces are

$$F_L = (g+b)(a+u), \qquad F_R = (g-b)(a-u),$$

and adding and subtracting them gives

$$F_+ = F_L + F_R = 2ga + 2bu, \qquad F_- = F_L - F_R = 2ba + 2gu.$$

Suppose the only force sensor measures the total $F_+$, which is the usual situation when a single plate or load cell sits under the whole body. When the controller sends no differential command ($u = 0$), the total force is $2ga$ whether the left or the right motor is stronger. The sign of $b$ is invisible. When it sends a small differential command, the total force changes by $2bu$, and the direction of that change reveals the sign of $b$. A short probe of $+u$ followed by $-u$ is enough.

A world model that has seen this probe and must later predict the effect of a new differential command needs to carry the sign of $b$ forward in time. If the probe happened several seconds earlier and the cart has been running with $u = 0$ since then, the recent observations look the same for both signs. The only place the answer can live is the model's memory.

Two further points from this example shape the design. First, if individual motor forces were measured, their difference $F_-$ would reveal $b$ immediately, with no probe needed. The study is only meaningful under a declared restriction on what is observed. Second, a mirror reflection of the whole experiment swaps the motors, so it changes $b$ to $-b$ and $u$ to $-u$, while leaving $F_+$ and the forward motion unchanged. The product $bu$ is unchanged, which is why the total force can respond to it.

## 3. Concepts used throughout

**World model.** A model that predicts future observations $y_{t+1}, y_{t+2}, \dots$ from the history of observations and actions $H_t = (y_0, a_0, \dots, a_{t-1}, y_t)$ and a planned sequence of future actions. Most modern world models compress the history into a vector $h_t$, the **latent state**, which is updated each time a new observation arrives and is used to make predictions.

**Reflection.** A left–right reflection $M$ is the operation that swaps every left-labeled quantity with its right-labeled partner. For a measured quantity it is a fixed rule: total force stays the same, the left-minus-right force difference changes sign, a left joint angle becomes the right joint angle. Applying $M$ twice returns the original.

**Even and odd.** A scalar is **even** if reflection leaves it unchanged (total force, forward speed) and **odd** if reflection flips its sign (force difference, the asymmetry $b$, the differential command $u$). Any pair of left and right measurements can be rewritten as one even sum and one odd difference without losing anything. The product of two odd quantities is even, which is how $bu$ enters the total force.

**Invariance and equivariance.** A model is **invariant** to reflection if reflecting its input does not change its output. A model is **equivariant** if reflecting the input reflects the output in the corresponding way: $f(Mx) = Mf(x)$. An invariant model of the cart would give the same internal state for a left-stronger and a right-stronger body and could never predict the sign of a response. An equivariant model can represent both bodies, as long as its internal state has odd components that flip under reflection. Equivariance is the appropriate symmetry assumption when the population of bodies is equally likely to be stronger on either side, because then the best possible predictor is itself equivariant.

**Identifiability.** A hidden parameter is identifiable from an experiment if different values of the parameter produce distinguishable distributions of measurements. In the cart, $b$ is not identifiable from passive total force, and its sign becomes identifiable after a differential probe.

## 4. Research question and hypotheses

**Research question.** By the ICML 2027 submission deadline (13 weeks, expected late January 2027), can we show on held-out simulated bodies whether a world model with an explicit two-sided belief about persistent asymmetry predicts the response to a differential command issued several seconds after a probe more accurately than an equally informed standard recurrent world model, while matching it on ordinary next-step prediction?

The question is specific (one kind of hidden parameter, one kind of query, one comparison), measurable (the metrics in Section 8), achievable in simulation with modest compute, relevant to how world models are built for asymmetric bodies, and bounded by the submission date.

**H1 (availability).** After a probe, an exact Bayesian filter that knows the equations recovers the sign of $b$ with high probability; under passive observation it remains at chance. This hypothesis checks the benchmark itself.

**H2 (retention).** A standard recurrent world model trained on next-step prediction loses the sign information as the delay between probe and query grows, even though the Bayesian filter keeps it.

**H3 (use).** A world model with a persistent two-sided belief over $b$ keeps the information across the delay and predicts the later response with lower error, without a loss in ordinary prediction.

## 5. Related work

**Reflection-equivariant models.** Chirality Nets (Yeh, Hu and Schwing, NeurIPS 2019) built recurrent layers that respect the left–right symmetry of a skeleton and used them for pose forecasting. SWAP (Lan et al., 2026) builds a reflection-equivariant recurrent world model for legged robot parkour. These works show that equivariant recurrence is established, so this proposal makes no claim to it.

**Memory in world models.** Recurrent state-space models such as PlaNet and DreamerV3 (Hafner et al., 2019; 2023) maintain a latent state across long horizons. Flow Equivariant World Models (Lillemark et al., ICML 2026) give structured memory for partially observed scenes.

**Inferring hidden context from history.** RMA (Kumar et al., 2021) and VariBAD (Zintgraf et al., 2020) infer properties of a robot or task from recent interaction and condition a policy on them. These methods are natural baselines for our persistent-context component.

**Predictive representation learning.** Joint-embedding predictive architectures (JEPA; Assran et al., 2023) learn by predicting the representation of a hidden part of the input, and V-JEPA 2 (Assran et al., 2025) adds action-conditioned prediction for robot planning.

**Recent work on intervention-relevant representations.** *Identifiable World Models from Pretrained Diffusion Representations* (Sandilya, Liston and Grosenick, 2026) and *Compact but Moving* (Chen and Liu, 2026) study when representations support predictions under interventions. Our study is narrower: one hidden signed parameter, a declared observation restriction, and an exact reference.

**Our own earlier studies.** In a study of JEPA-inspired pose restoration, a baseline that always predicts zero change in knee asymmetry had lower asymmetry-change error than every trained variant, although the trained models restored noisy poses well. A second study disabled mirror augmentation by hand because laterality matters in stroke and Parkinson's disease, and found that every test video also appeared in training. These results do not show that any model erased asymmetry. They do show that asymmetry is easy to lose in evaluation, and that leakage between training and test sets can make any conclusion meaningless.

## 6. Method

### 6.1 Two simulated bodies

**Tier A: the two-motor cart.** The cart obeys $m\ddot x = F_L + F_R - kx - c\dot x$, with each motor's activation following its command through a first-order lag of time constant $\tau$. The model observes position, velocity and noisy total force, together with the commands $a$ and $u$. Individual motor forces are never observed. Each episode has three phases: a **probe** of a few alternating differential pulses, a **delay** with $u = 0$ that lasts from zero to eight seconds, and a **query**, a new constant differential command held for half a second, whose force response the model must predict. Because activations re-equalize within a few time constants after the probe, the observations during a long delay carry almost no information about $b$. The exact Bayesian filter measures how much remains. Because the system is linear once $b$ is fixed, the filter can be computed on a fine grid of $b$ values with one Kalman filter per grid point.

**Tier B: a planar walker.** A MuJoCo walker with two legs is given asymmetric knee actuators by scaling the left and right knee gains by $1+b$ and $1-b$. A nominal controller keeps the walker moving. A probe adds a short differential knee command; after a delay, the query is a new differential command whose effect on the joint angles and foot forces must be predicted. The command sequence during the query window is fixed before the window starts, so the world model never receives commands that a feedback controller chose in response to future states.

### 6.2 A world model with a two-sided belief

The model has two parts of internal state. A **changing state** $z_t$ describes the body's current motion and is updated at every step. A **persistent context** $c$ describes properties that do not change within an episode, such as $b$. The persistent context is represented as a probability distribution with two mirror-image components: one for "left stronger" and one for "right stronger". Reflection swaps the two components. Under passive observation the two components can keep equal weight, and after a probe the weight can move to one side.

When the model predicts the future, it draws one sample of $c$ and keeps it fixed for the whole imagined trajectory. This matters: a model that resamples the asymmetry at every step would imagine a body whose stronger side changes from moment to moment. Real observations update the belief; the model's own predictions never do.

All layers are reflection-equivariant, using the constructions of Chirality Nets. The decoder that predicts total force receives the product of odd context features and the odd differential command, so a term like $bu$ can reach an even output.

### 6.3 Training objectives

The model is trained with the usual next-step prediction loss on the full episode, plus a **query loss** on the response to the query command:

$$\mathcal L = \mathcal L_{\text{next}} + \lambda\, \mathcal L_{\text{query}}.$$

Both terms are negative log-likelihoods of the observed outcomes under the model's predictive distribution. Every baseline receives the same two terms with the same $\lambda$, so a gain cannot come from supervision that only the proposed model sees.

### 6.4 Baselines and references

- A standard recurrent world model (a GRU-based recurrent state-space model in the style of DreamerV3).
- The same model trained with mirror-augmented data, where each episode is reflected together with its labels.
- A deterministic equivariant recurrent world model in the style of SWAP, without the two-sided belief.
- A context model in the style of RMA that infers a context vector from a fixed recent window.
- The exact Bayesian filter (Tier A only), which defines what the data allow.
- A parameter oracle that receives the true $b$, which defines the best achievable prediction.

Parameter counts, latent sizes and training updates are matched across learned models.

## 7. Pipeline, splits and leakage

The unit of independence is a **body family**: one draw of the body's parameters, together with its mirror twin (the same draw with $b$ replaced by $-b$). Every episode, probe variant, delay and noise replicate generated from a family belongs to that family.

| Step | What happens | What is preserved | Split and leakage guard |
|---|---|---|---|
| 1. Sample bodies | Draw $(g, b, \tau, m)$ for each family and pair it with its mirror twin | Raw parameter values and seeds are saved with each family | Families are assigned to training (70%), validation (15%) and test (15%) before anything else is generated |
| 2. Simulate episodes | Run probe, delay and query phases | Native time step, SI units, named left/right channels, array shape `[episode, time, channel]` | All episodes inherit their family's split |
| 3. Make windows | Cut histories that end at the query start | No resampling or time stretching; shorter histories are padded and masked | Windows never cross families; query targets never appear in the input |
| 4. Normalize | Scale inputs and targets | Odd channels are scaled around zero so reflection still flips their sign; the transform is saved and invertible | Statistics come from training families only |
| 5. Train and select | Fit models; choose settings on validation | Model inputs keep the channel order and time grid of Step 2 | Test families are never used for selection |
| 6. Test | Score predictions on test families once | Predictions are returned on the same grid and in the same units as the targets | Test results are computed after all settings are frozen |

## 8. Evaluation and statistics

The primary metric is the error in the predicted **signed response**, the part of the query response that depends on the sign of $b$, measured after the longest delay. Secondary metrics are the accuracy of the predicted sign, ordinary next-step error, and the calibration of the predictive distribution. Each metric is averaged within a family, then compared between methods with a paired bootstrap over test families. Each model is trained with five seeds; seed-to-seed variation is reported separately from family-to-family variation.

## 9. Plan

Weeks 1–2: build the cart simulator and Bayesian filter, and confirm H1. Weeks 3–5: train baselines and measure how retention changes with delay. Weeks 6–8: train the proposed model and its ablations. Weeks 9–11: repeat the key comparison on the walker. Weeks 12–13: test once on held-out families, analyze, write.

## 10. Limitations

The study uses simulated bodies. A positive result would show that a particular kind of state representation helps when an asymmetry must be carried across a delay. It would not show that the method identifies muscle strength in people, and no clinical claim is intended.

## References

- Assran, M. et al. (2023). Self-supervised learning from images with a joint-embedding predictive architecture. *CVPR*. arXiv:2301.08243.
- Assran, M. et al. (2025). V-JEPA 2: Self-supervised video models enable understanding, prediction and planning. arXiv:2506.09985.
- Chen, Y. and Liu, Y. (2026). Compact but moving: Intervention-relevant geometry in recurrent world models. arXiv:2609.21787.
- Hafner, D. et al. (2019). Learning latent dynamics for planning from pixels. *ICML*. arXiv:1811.04551.
- Hafner, D. et al. (2023). Mastering diverse domains through world models. arXiv:2301.04104.
- Kumar, A. et al. (2021). RMA: Rapid motor adaptation for legged robots. *RSS*. arXiv:2107.04034.
- Lan, K. et al. (2026). SWAP: Symmetric equivariant world-model for agile robot parkour. arXiv:2606.19928.
- Lillemark, H. J. et al. (2026). Flow equivariant world models: Memory for partially observed dynamic environments. *ICML*. arXiv:2601.01075.
- Sandilya, R., Liston, C. and Grosenick, L. (2026). Identifiable world models from pretrained diffusion representations. arXiv:2610.07028.
- Yeh, R. A., Hu, Y.-T. and Schwing, A. G. (2019). Chirality nets for human pose regression. *NeurIPS*. arXiv:1911.00029.
- Zintgraf, L. et al. (2020). VariBAD: A very good method for Bayes-adaptive deep RL via meta-learning. *ICLR*. arXiv:1910.08348.
