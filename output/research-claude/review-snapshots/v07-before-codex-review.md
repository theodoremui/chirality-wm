# Keeping the Hidden Side: How Predictive World Models Lose, and Can Retain, Asymmetric Mechanics

**Version 7 · Final research proposal · 23 October 2026**
**Status:** a 13-week plan for the ICML 2027 submission; no models have been trained and no results are claimed. This version integrates six rounds of review (scores and critiques in [output/research-claude/](../../output/research-claude/README.md)), each including an independent Codex adversarial review. Protocol details that a reader does not need to follow the argument are in the appendices.

## Abstract

World models let a controller ask what will happen before it acts, and many of the bodies we most want to control, such as a robot with a worn motor or a person recovering from a stroke, are stronger on one side than the other. The difference can stay hidden during ordinary movement and appear only when an input pushes the two sides apart, so a world model has to infer it from brief evidence and then carry it, through stretches that reveal nothing new, to the moment a new command depends on it. Common practice works against this: mirrored training data and left–right equivariant layers are correct for a body plan yet can leave no room for one body's departure from it. We argue that a predictive model can lose such an asymmetry in four distinct ways, which concern the form of its predictive distribution, the allocation of its capacity, the training signal that reaches its memory, and its ability to combine context with command. Each comes with a formal statement and a measurable signature. We propose a benchmark that switches each failure on and off while the available evidence stays fixed, scores every prediction against the best answer the data permit, and tests a world model that answers each failure with a removable component. The experiments move from an analyzable two-motor system to a simulated walker seen through joint sensors and through a camera, and then to real human motion, in order to establish when symmetry priors are safe and what keeps a hidden side from being lost.

## 1. Introduction

A world model is a learned simulator. It compresses what a system has done so far into an internal state and predicts what will happen under a planned sequence of actions. Its value is practical: a controller can try candidate actions inside the model, keep those whose predicted outcomes look good, and only then act. This is how DreamerV3 learns to act from pixels across many domains (Hafner et al., 2023) and how V-JEPA 2 plans robot manipulation in a learned feature space (Assran et al., 2025). A prediction can be no better than the state it starts from, and the state carries only what training gave it a reason to keep.

Consider an exoskeleton that assists a person whose left leg was weakened by a stroke. People compensate for a weak side, so ordinary walking can look nearly symmetric to a camera or to a pair of joint sensors. The controller asks its world model what will happen if it adds knee assistance on the left. The answer depends on how much weaker that leg is—information the model saw only in the moments when the two legs were asked to do different things. If its state no longer carries the difference, it predicts the response of an average, symmetric person, and the planned assistance is wrong in size and possibly in direction. A quadruped with a worn motor or an off-center payload poses the same problem.

Left–right symmetry is one of the most effective priors in robot learning. Because a body plan is symmetric, mirroring each training episode doubles the data, and building the symmetry into the network lets a model generalize to mirrored situations—a turn to the left after training on turns to the right—without seeing them (Ordoñez-Apraez et al., 2025; Lan et al., 2026). The prior is correct for the *population* of bodies. A particular body can still break it, and the question is whether a model built around symmetry has a place to store that body's departure from the plan and will use it when a new command arrives.

The user's earlier work suggests the risk is real. In a study of JEPA-inspired motion representations, a baseline that always predicted *no change* in knee asymmetry was more accurate on asymmetry change than every one of sixteen trained models, although those models restored noisy poses well. Heavy penalties for failed measurements explain part of that gap, and the study does not show that any representation erased the asymmetry. Still, improving the large symmetric part of a target while doing worse than a symmetric guess on its small signed part is the pattern this proposal sets out to explain. A second study, on clinical gait video, found that every test video also appeared in training. In a study of memory, where any route by which test information reaches training looks like a model that remembers, that lesson shapes the whole design.

We study the problem in its simplest complete form. A brief **probe** reveals which side is stronger, a **hold** follows in which nothing more about the asymmetry can be observed, and a **query** asks for the response to a new command that pushes the two sides apart. We argue that a predictive world model can fail at this in four distinct ways (Section 5). Its predictive distribution may be unable to describe a body that is either left- or right-stronger and stays so. Squared-error training may spend limited capacity on larger quantities first. Ordinary next-step training gives the memory no reason to hold evidence through the hold. And the model may find it hard to learn the product of the stored asymmetry and the new command, which is how the asymmetry enters the physics. Each failure has a short formal statement and a distinct signature, so an experiment can switch it on and off.

**Contributions.**

1. **A diagnostic account** of four mechanisms by which a predictive model can lose a signed asymmetry, each with a formal statement under explicit assumptions and a measurable signature.
2. **Probe–hold–query episodes**, a benchmark in which each mechanism has its own control knob while the evidence about the asymmetry stays fixed. Every prediction is scored by *contrast skill*, the share of the best achievable improvement over a symmetric guess, computed from exact Bayesian references.
3. **A signed-belief world model** that answers each mechanism with one removable component, tested against faithful versions of the strongest alternatives, including probabilistic symmetry breaking and a model that simply stores its state when the evidence ends.
4. **Evidence at three levels of realism:** a two-motor cart whose Bayesian answer is available in closed form, a simulated walker seen through joint sensors and through a camera, and a re-analysis of the user's JEPA pose encoders on real motion from a cohort they have never seen.
5. **A data contract and a registered analysis plan** that make each conclusion checkable.

The study is organized as a sequence of questions, each answered before the next is asked (Section 10). It asks whether the data contain the asymmetry, whether standard world models keep it, which mechanism explains a loss, whether the matching component repairs it, and whether the account survives contacts, pixels and real motion. Section 12 states in advance what the paper will claim under each pattern of answers.

## 2. The problem from first principles

### 2.1 World models and their internal state

A world model receives a history $H_t = (y_0, a_0, y_1, \dots, a_{t-1}, y_t)$ of observations $y$ and actions $a$, together with a planned sequence of future actions, and returns a prediction of the future observations. Most world models compress the history into a vector $z_t$, the **latent state**, which is updated whenever a new observation arrives. Everything the model can later say about the future must be carried in $z_t$. A property of the body that is not in $z_t$ cannot influence any prediction.

### 2.2 A body with a hidden side

A cart is pushed by a left motor with gain $g+b$ and a right motor with gain $g-b$, with $g > |b|$. The number $b$ is the asymmetry: positive when the left motor is stronger, negative when the right one is. A common command $a$ drives both motors and a differential command $u$ raises the left command and lowers the right. Each motor's activation follows its command through a short lag, $\tau\dot q_L = a+u-q_L$ and $\tau\dot q_R = a-u-q_R$. The activation sum stays at $2a$ once it starts there, and writing $d(t) = q_L - q_R$ for the activation difference, the total force is

$$F_+ = (g+b)q_L + (g-b)q_R = 2ga + b\,d(t).$$

The cart obeys $m\ddot x = F_+ - kx - c\dot x$. Its sensors report position, velocity and total force with noise, as a single load cell under a body would. They never report the two motor forces separately.

When the differential command is zero, $d$ is zero and the total force is $2ga$ whichever motor is stronger, so passive observation cannot tell left from right. A differential command makes $d$ nonzero and changes the total force by $b\,d(t)$, whose sign reveals the stronger side. If the probe happened seconds ago and the cart has since been held still, only the model's memory can carry the answer to the next query.

### 2.3 Reflection, parity and equivariance

A mirror reflection $M$ swaps left and right. Applied to a measured quantity it follows a fixed rule. **Even** quantities are unchanged: total force, position, velocity, the common command $a$ and the common gain $g$. **Odd** quantities change sign: the asymmetry $b$, the differential command $u$, the activation difference $d$, and any left-minus-right difference. The product of two odd quantities is even, which is how $b\,d$ can appear in the total force.

A model $f$ is **invariant** if reflecting its input leaves its output unchanged, $f(Mx) = f(x)$, and **equivariant** if reflecting the input reflects the output, $f(Mx) = Mf(x)$. An invariant history encoder is harmful here: it gives the same state to a body and its mirror twin (with the probe also mirrored), although at the same later query their responses have opposite signs. Equivariance is the appropriate constraint. When left-stronger and right-stronger bodies are equally common and every other part of the experiment is unchanged by reflection (Assumption S, Appendix A), the best possible predictor is itself equivariant (Proposition 0). Equivariance is thus consistent with optimal prediction, and the failures studied here come from what a model does within that constraint.

### 2.4 Availability, retention and use

Before blaming a model for losing an asymmetry, one must know that the data contained it. We separate three questions. **Availability** asks whether the recorded history determines the sign of $b$, which an exact Bayesian computation answers without any neural network. **Retention** asks whether, when it does, the learned state still carries that information after the hold. **Use** asks whether, when the state carries it, the prediction for a new command depends on it in the right direction and by the right amount. Every measurement in this proposal is attached to one of the three.

## 3. Related work

**World models and their training objectives.** Recurrent state-space models learn a latent state by reconstructing observations and use it for planning (PlaNet, Hafner et al., 2019; DreamerV3, Hafner et al., 2023). Joint-embedding predictive architectures (JEPA) predict the *representation* of hidden or future inputs instead of the inputs themselves (Assran et al., 2023); V-JEPA 2 adds an action-conditioned predictor for robot planning (Assran et al., 2025), DINO-WM plans in the features of a frozen image encoder (Zhou et al., 2024), and LeJEPA replaces heuristic anti-collapse terms with an isotropic Gaussian regularizer (Balestriero and LeCun, 2025). The choice between these objectives is usually argued on benchmark returns. Theory on deep linear networks gives a sharper distinction. Latent prediction learns features in the order of their input-to-target regression coefficients, while reconstruction follows their variance (Littwin et al., 2024), and both learn strong directions before weak ones (Saxe, McClelland and Ganguli, 2014). Neither line has asked what happens to a feature that is small, signed and consequential.

**Symmetry in learned dynamics.** Chirality Nets introduced reflection-equivariant recurrent layers for human pose (Yeh, Hu and Schwing, 2019). Morphological symmetries of robots are now routinely built into learned models (Ordoñez-Apraez et al., 2025), SWAP builds a reflection-equivariant world model for legged parkour (Lan et al., 2026), and flow-equivariant world models give structured memory under partial observation (Lillemark et al., 2026). When the dynamics themselves depart from symmetry, approximately equivariant networks relax the constraint (Wang, Walters and Yu, 2022), relaxed group convolutions can locate the departure (Wang et al., 2024), and guarantees for equivariant world models degrade with its size (Wang, 2026). Lawrence et al. (2026) show that augmentation can hurt when a dataset's distribution is not symmetric. Our setting differs from all of these. Each body breaks the symmetry while the population of bodies preserves it, so the best predictor is equivariant and the asymmetry must be inferred and kept body by body.

**Breaking symmetry inside equivariant models.** An equivariant function cannot break the symmetry of its input, a neural form of Curie's principle (Smidt, Geiger and Miller, 2021; Kaba and Ravanbakhsh, 2023). SymPE restores symmetry breaking through randomized canonicalization and equivariant conditional distributions, including weights that depend on the input (Lawrence et al., 2025). The two-sided belief used here is an instance of that idea for a two-element group. What this proposal adds is the question of persistence over a rollout, and of how symmetry breaking interacts with memory and with decoding.

**Inferring hidden context.** RMA (Kumar et al., 2021), context-aware dynamics models (Lee et al., 2020) and CoDA (Kirchmeyer et al., 2022) infer environment properties from recent interaction and condition dynamics on them; VariBAD maintains a posterior over a task embedding (Zintgraf et al., 2020). Recent work studies which directions in a world model's state matter for interventions (Sandilya, Liston and Grosenick, 2026) and shows that those directions can move over time (Chen and Liu, 2026). These methods assume the relevant evidence keeps arriving or study representations in general. The benchmark here isolates the case where evidence is brief and then disappears, so that retention can be separated from inference.

**Reading what a representation contains.** Readouts from frozen representations are informative only relative to the class of readout used (Hewitt and Liang, 2019), a point made precise by usable information (Xu et al., 2020). We use readouts in this sense and never treat a failed readout as proof that information is absent.

**The gap.** To our knowledge, no study asks when a predictive world model keeps a persistent, signed property of an individual body after the evidence for it has passed, under symmetry priors that are correct for the population. None separates the possible reasons for a loss with controls that hold the available information fixed. A search found no paper on this question; absence from a search is weak evidence, and the claim will be rechecked before submission.

## 4. Research question and hypotheses

**Research question.** By the ICML 2027 submission deadline (expected late January 2027, 13 weeks from now), can probe–hold–query episodes, in which the available information is fixed and computed exactly, determine which of four mechanisms make standard world models lose a body's signed asymmetry? And does a signed-belief world model reach a contrast skill of at least 0.9 on held-out simulated bodies, above the best baseline chosen on validation data, with next-step prediction error no more than 5% above that baseline's?

The question names its endpoint (contrast skill, Section 7), its thresholds, its population (independently drawn simulated bodies), and its date. A contrast skill of 0.9 means the model attains 90% of the improvement over a symmetric guess that the data allow, and the 5% margin keeps a gain in retention from being bought with worse ordinary prediction.

**Headline hypotheses**, one per mechanism plus the objective comparison:

| | Hypothesis | Primary test |
|---|---|---|
| H1 | **Symmetry (M1).** On histories that do not favor either side, predictive distributions that cannot represent one persistent, two-sided body score worse than a body drawn once per rollout | Energy score of the joint query prediction, within one backbone |
| H2 | **Capacity (M2).** Raising the variance of competing predictable signals lowers contrast skill more when capacity is scarce than when it is ample, and the loss survives optimization interventions | Variance × width interaction in contrast skill, with restarts, re-tuning, longer training and a frozen-readout trade-off |
| H3 | **Objective (M2).** With distractors that carry little predictive information, latent prediction keeps the asymmetry where reconstruction loses it | Objective × distractor-predictability interaction on one shared backbone, in the cart and in walker images |
| H4 | **Memory (M3).** When only probe and hold losses shape the representation, the asymmetry becomes less recoverable from the frozen state as the hold lengthens | Delay-specific readout skill at a 2 s hold minus an 8 s hold |
| H5 | **Coupling (M4).** Explicit multiplication of stored asymmetry and command learns the response from less data than concatenation | Mean skill over a grid of training-set sizes, on held-out queries |

The walker replicates the memory hypothesis and the comparison of the signed-belief model with its strongest alternatives, which are the parts the budget can support at full statistical strength; H3 is tested separately in walker images. The exact effect sizes, decision rules and validity gate are in Section 11 and Appendix D.

## 5. Four ways to lose the hidden side

Each mechanism is stated in words, then formally (proofs in Appendix A), then as a test.

### M1. A body that is either left- or right-stronger, and stays so

*In words.* When the evidence favors neither side, the correct prediction is "one of two mirror-image bodies, and the same body for the whole rollout". With $|b|$ bounded away from zero, the true distribution of the query response has two separated modes with nothing between them. A deterministic point prediction cannot express this, and neither can a single-peaked distribution. A distribution that redraws the body at every step of a rollout also fails if its draws are independent, because the imagined body can then switch sides mid-trajectory.

*Formally* (Proposition 1). If $f$ is deterministic and equivariant and its input is a fixed point of reflection, $Mx = x$, then $f(x) = Mf(x)$ and every odd component of the output is zero. A passive cart history is such a fixed point, so a deterministic equivariant model predicts zero contrast. An equivariant predictive *distribution* need only be reflection-invariant as a whole, which allows two modes. The pathwise statement applies only to reflection-fixed inputs; for others, such as walker histories with independently noisy left and right sensors, we test calibration and distributional symmetry instead.

*Test.* Six output families are compared on passive histories by the energy score, a proper score that rewards a predicted distribution for matching both the location and the shape of the outcomes (Gneiting and Raftery, 2007). They share one *deterministic* equivariant history encoder, and all sampling is confined to the output module, so each family's complete predictive law is the one written down for it. A stochastic backbone would let even a Gaussian head produce several modes through its latent samples. The families are a Gaussian fitted under the energy score itself, a flexible single-peaked distribution, a two-component mixture at the query horizon, an independent per-step mixture, an autoregressive per-step mixture that conditions on its own generated history, and a body drawn once per rollout. The faithful stochastic SWAP-style model is evaluated separately as a baseline. M1 concerns predictive distributions, and under passive histories a zero-mean point prediction is optimal, so M1 explains a loss of contrast skill on probed episodes only if swapping the failing model's output family, with everything else fixed, raises its skill.

### M2. Competition for capacity

*In words.* A model trained by squared error with limited capacity keeps the quantities whose predictable variance is largest. A small signed response can therefore be dropped although it is perfectly predictable.

*Formally* (Proposition 2). Among linear predictors of rank at most $k$, with centered variables and an intercept outside the rank budget, the squared-error optimum keeps the $k$ leading eigenvectors of the covariance of the best linear prediction (Izenman, 1975). Under Assumption S, even and odd quantities are uncorrelated, so that covariance splits into an even block and an odd block, and the odd response is predicted as zero once all of its eigenvalues fall below the $k$-th largest even one.

*Test.* An exact linear experiment adds predictable distractor channels with a designed spectrum, so reduced-rank regression should drop the asymmetry at a boundary computed in advance. Its input is the centered probe statistic $\sum_t (d_t - \bar d)F_{+,t} = b\sum_t (d_t - \bar d)^2 + \text{noise}$, which removes the common-gain term for any probe pattern and identifies $b$ for either probe sign. In nonlinear world models, raising distractor variance must lower contrast skill *more at width 16 than at width 64*, where capacity is ample. Width also changes how easily a network optimizes, so the interaction alone is not enough. Capacity competition is claimed only if the narrow model's drop survives three optimization interventions at fixed width (independent restarts, a learning rate re-tuned for each variance level, and doubled training). Frozen readouts must also show the trade-off itself, with the asymmetry becoming less recoverable from the state as the distractors become more recoverable. Otherwise the result is reported as width-dependent interference. Channel scales are frozen across conditions so that normalization cannot undo the manipulation.

*Objectives.* Littwin et al. (2024) analyze deep linear networks and show that latent prediction learns features in the order of their input-to-target regression coefficients. For the asymmetry that coefficient is $st\,\mathrm{Var}(b)/(s^2\mathrm{Var}(b) + \sigma^2)$, where $s$ and $t$ scale its effect on probe evidence and on the response and $\sigma^2$ is the evidence noise. It approaches $t/s$ when the probe is informative, so the asymmetry has small variance but an undiminished coefficient. Predictable distractors also have high coefficients, so the tested prediction (H3) is limited to distractors with *low* coefficients, such as white noise in sensors or moving backgrounds in images. A deep-linear study first reproduces the theorem's exact setting before extending it (Appendix B).

### M3. A memory that nothing rewards

*In words.* While the hold reveals nothing about the asymmetry, the losses computed on hold observations give no reason to keep it. Only losses computed after the hold can teach the memory to hold on, and their signal must travel back through every step of the hold.

*Formally* (Proposition 3). If hold observations are independent of $b$ given the rest of the history, and the model's predictions of them do not depend on the odd part $z_o$ of its state, hold losses have zero gradient with respect to $z_o$. For a linear odd update with operator norm at most $r < 1$, the stored value and any later training signal both shrink at least as fast as $r^D$ over a hold of $D$ steps (Bengio, Simard and Frasconi, 1994).

*Test.* With the common gain known, so the hold cannot change what the data say about $b$, the representation is shaped by four loss sets: probe and hold only, with teacher-forced query steps added, with the open-loop query loss added, and a version with matched total query weight. In every arm, response readouts are trained on the frozen state with gradients stopped at the memory, so decoding effort is equal across arms. A code that shrinks, $z_D = r^D b$, still contains $b$, and a readout shared across holds can fail on it simply because the scale changed. Each arm therefore gets both a shared readout and a delay-specific readout with matched budgets, together with the recoverability of $b$ at the end of the probe. A control model whose odd state contracts by a known factor but stays invertible checks that delay-specific readouts recover it. H4 is scored on the delay-specific readouts, and a negative result is stated as a limit on information usable by the tested readout classes.

### M4. A product that must be learned

*In words.* The asymmetry changes total force only through its product with the differential command. A model must form that product somewhere, and some architectures make it harder to learn than others.

*Formally* (Proposition 4). An equivariant head that predicts an even outcome from a frozen state, and is additively separable in state and odd command, predicts zero contrast for every state. This is a construction check: in a rollout, any nonlinear transition can form the product inside the state.

*Test.* Query amplitude and shape vary across episodes, with some combinations held out for testing, so that a decoder cannot fake the product with a fixed offset for a single query. On the same frozen encoder, explicit multiplicative fusion is compared with concatenation by mean contrast skill over a registered grid of training-set sizes. The additive head and a fixed-query linear decoder serve as controls.

**A shared cost.** If two equally likely histories with mean responses $m_+$ and $m_-$ at the same query are mapped to the same memory state, the best shared prediction is their midpoint, and the excess squared error is $(m_+ - m_-)^2/4$ (Lemma A1). Whichever mechanism merges a left-stronger with a right-stronger history, this is what it costs.

## 6. The benchmark: probe–hold–query episodes

### 6.1 Episodes

1. **Probe.** From a canonical rest state ($x = \dot x = 0$, $q_L = q_R = a$), a balanced pattern of differential pulses whose overall sign is random.
2. **Reset and hold.** The simulator resets the complete physical state, both activations included, to the canonical values and holds it with $u = 0$ for $D$ seconds, while the model's memory is kept. After the reset, bodies that differ only in $b$ produce identical hold records under identical noise, which the validity gate checks directly.
3. **Query.** From the canonical state, a differential command schedule $u(t) = \alpha\,\phi(t)$ over $H = 0.5$ s, predicted open-loop from the memory at the start of the query. The amplitude $\alpha$ takes one of three values with random sign, and the shape $\phi$ is a step, a ramp, or a step that reverses halfway; two amplitude–shape combinations appear only in testing.

The **query contrast** is half the difference between the responses to $+u$ and $-u$ from one saved state, $r = \tfrac12[J(+u) - J(-u)]$, where $J$ is the total-force impulse over the query. After the reset, $J(u) = 2gaH + b\int_0^H d_u(t)\,dt$, so $r = b\int_0^H d_u(t)\,dt$. The simulator computes $r$ from two branches cloned from the same state, and a model computes its prediction from two copies of its memory, using one sampled body for both branches.

### 6.2 Knobs

| Knob | Values | Mechanism | What it leaves fixed |
|---|---|---|---|
| Probe present | passive / probed | M1 | Body distribution |
| Output family | six families (Section 5) | M1 | Backbone, loss, state budget |
| Predictable distractors | three variances around the linear boundary; coefficient below, equal to and above the asymmetry's | M2 | Body, probe, noise |
| Width | 1–9 (linear); 16 and 64 (nonlinear) | M2 | Data |
| Hold length | 0, 2, 4, 8 s | M3 | Evidence at the start of the hold |
| Losses shaping the representation | four arms (Section 5) | M3 | Data, readout training |
| Fusion and training-set size | concatenation or multiplication; five sizes from 250 to 4,000 episodes | M4 | Encoder, queries |
| Secondary | white distractors, spread of $g$, hold flag, random probe length, population balance | — | — |

Population balance deliberately violates Assumption S: when left-stronger bodies are more common, exact equivariance and mirror augmentation both force a 50:50 belief on passive histories although the correct belief is skewed.

### 6.3 Exact references

With $\tau$, $m$, $k$ and $c$ known, every cart observation is a linear function of $(g, b)$ plus Gaussian noise, so the posterior over $(g, b)$ follows from a two-parameter linear regression. It is evaluated on a grid refined until the predictive mean and second moment of the contrast, the Bayes risk and the energy score of the reference all change by less than a tenth of the corresponding meaningful effect. For the walker, the probe starts from a canonical state with a fixed command pattern, so its noiseless trajectory depends only on the asymmetry and one nuisance parameter, and precomputed simulations on a grid give an exact posterior from joint-sensor histories, up to integrator and grid tolerance. No such reference exists for images, where occlusion, quantization and random backgrounds would need their own likelihood. In the camera tier the joint-sensor reference is therefore labeled *privileged*: results are reported as raw risk and as skill relative to that privileged reference, and no claim is made about what the images themselves allow. An **information audit** reports the Bayes risk at every hold, so a claim that a model loses information is made only where the audit shows that the data's information is constant.

### 6.4 Three levels of realism

**The walker through joint sensors.** The dm_control planar walker (Tassa et al., 2018) gets knee gears $50(1+b)$ on the left and $50(1-b)$ on the right, and a common scale $\eta \in [0.9, 1.1]$ on all six motors as a competing unknown. A harnessed probe applies differential knee pulses with the feet off the ground. A harnessed reset and hold follows, with zero commands. The released query applies a 0.5 s open-loop push-off from a canonical standing pose, with a differential knee component of varying amplitude and shape. The endpoint is the contrast in total vertical ground impulse, divided by body weight times $H$. A week-2 check confirms that the released walker stays upright and that the contrast increases with $b$.

**The walker through a camera.** The same episodes are rendered at $64 \times 64$ pixels. The stock walker gives both legs one material, so we color the left leg to keep the sides named in the image. In a side view the legs occlude each other, so swapping the leg colors only approximates the image of the reflected state, and the discrepancy is reported. H3 needs distractors whose predictive value is low at the horizon the models are trained on. Task-irrelevant video is not enough: the Distracting Control Suite's backgrounds (Stone et al., 2021) evolve smoothly and can be quite predictable. The camera tier is therefore a factorial over two objectives (reconstruction and latent prediction, on one shared backbone and readout) and three backgrounds: a static image, smooth natural video from that suite, and video whose frames are shuffled in time so that it carries the same pixel statistics with almost no temporal predictability. Each background's predictable variance at the training horizon is measured directly.

**Real motion.** The user's JEPA asymmetry study paired AMASS walking windows with copies carrying a synthetic right-knee edit, trained direct-coordinate and JEPA-style encoders on 112 people, evaluated on 14, and kept a confirmation cohort that has never been evaluated. Physical mirroring, already part of that pipeline, turns right-knee edits into left-knee edits. As the original paper notes, projection after mirroring need not reverse the measured asymmetry change $\Delta A$. For every mirrored pair, $\Delta A$ is therefore recomputed from the projected references and never obtained by negating the original label, and the resulting sign distribution is audited and reported, with edit-side balance kept distinct from response-sign balance. On identical cases of the untouched cohort, three things are scored with the original study's error definition, failure costs and hierarchical weights: the original trained decoders, new linear and two-layer readouts fitted on frozen features from the training people, and the zero-change predictor. Recoverability is reported by readout class. A new readout that beats the original decoder on the same cases shows that the frozen features held usable information the original decoder did not use. A failure of the tested readouts bounds only what those readouts can find. This tier measures whether encoders keep a signed geometric difference, a narrower question than whether they keep a mechanical one, and it runs only if the original checkpoints are available.

## 7. Measuring retention

**Contrast skill (primary).** Let $R_{\text{model}}$ be a model's mean squared error in predicting the query contrast on test episodes, $R_0$ the error of always predicting zero contrast (a symmetric body), and $R_{\text{Bayes}}$ the error of the exact Bayes predictor from the same histories. Then

$$S = \frac{R_0 - R_{\text{model}}}{R_0 - R_{\text{Bayes}}}.$$

A skill of 1 is as good as the data allow, 0 is no better than a symmetric body, and a negative value is worse than a symmetric body—which is how the zero-change result in the user's JEPA study would register. Because the Bayes predictor minimizes squared error given the history, a model cannot exceed 1 in expectation, and predictions that exaggerate the asymmetry lose skill as surely as predictions that shrink it. The point prediction of a stochastic model is its predictive mean over many sampled bodies; scoring a single sample would penalize even an exact posterior sampler with twice the Bayes risk. Skill is always reported with its parts (model risk, Bayes risk and excess risk), because a change in available information moves the denominator.

**What skill costs in control.** In a *dial-a-force* task, a controller must choose a query amplitude that changes the impulse by a target amount, using the same moment-based rule for every model and for the Bayes reference. The meaningful difference in skill, $\delta_S$, is calibrated in the pilot as the difference that raises this task's mean cost by 10%, with a provisional value of 0.1.

**Diagnostics.** Attenuation is the slope from regressing a model's prediction on the Bayes mean, where 1 means the prediction moves one-for-one with what the data support. We also report calibration, frozen-state readouts of $b$ at the end of the probe and after each hold, context transplants between bodies with matched command and noise sequences (with sham and nuisance controls), energy scores of the branch pair and of whole query trajectories, and next-step error during probe and hold as a guardrail.

## 8. Models

### 8.1 The signed-belief world model

The model has four components, one per mechanism, and each can be removed.

**Parity-split layers.** Every hidden vector is split into an even part and an odd part, $h = (h^+, h^-)$, and reflection acts as $(h^+, -h^-)$. Linear maps connect even to even and odd to odd, with biases on the even part only. Odd units are multiplied by even gates, and products of two odd vectors feed even units, following the gated construction used in equivariant networks (Weiler et al., 2018). Any composition of these pieces is equivariant, and the product term is what lets odd information reach an even prediction. The recurrent update is a GRU built from them.

**Evidence slot (M3).** A persistent slot $c = (c^+, c^-)$ accumulates evidence, $c_t = c_{t-1} + \gamma_t \odot \Delta_t$, through an even gate $\gamma_t \in [0,1]$ that the network learns. A closed gate copies the slot unchanged, so its odd part does not decay over the hold.

**Two-sided belief (M1).** One small network $\psi$ is evaluated twice, on $(c^+, +c^-)$ and on $(c^+, -c^-)$. Evaluation $s \in \{+1, -1\}$ returns a logit $\ell_s$, the parameters $(\mu_s, \sigma_s)$ of a log-normal distribution for a positive magnitude, and a Gaussian for the body's even properties. Component $s$ has weight $\pi_s \propto e^{\ell_s}$, and its odd context is $\kappa^- = s\rho$ with $\rho = \exp(\mu_s + \sigma_s\varepsilon)$ and $\varepsilon$ standard normal, so magnitudes are continuous and sampled by reparameterization. Reflection swaps the two evaluations and negates the odd context, so the belief is equivariant by construction. Under passive histories the weights stay at one half; after a probe, evidence in $c^-$ moves weight toward one side. For a two-element group this is an instance of SymPE's input-conditioned symmetry breaking (Lawrence et al., 2025), and we present it as such.

**Persistent draw and explicit product (M1, M4).** At the start of a query the model draws one side and one magnitude per sample, keeps them for the whole imagined trajectory, and uses them for both branches. The transition and decoder receive the product of the odd context and the odd command at every step. Predicted observations never update the slot or the belief.

**Training.** Losses are separated by time: next-step likelihood on probe and hold, teacher-forced next-step loss during the query, and the energy score of the open-loop query prediction. In the energy score, the average over the two sides is computed exactly with the weights $\pi_s$, and within each side the continuous magnitude is handled by $K$ reparameterized samples, with independent sample banks for the term that compares the prediction with itself. The SymPE-style comparator uses the same magnitude family and sample count. In the remedy experiments, each branch pair is rewritten as its sum and its contrast, and each is divided by a fixed physical scale so that the small contrast is not swamped by the large sum. Equal weights on sums and differences would change nothing, since $(e_L+e_R)^2 + (e_L-e_R)^2 = 2(e_L^2 + e_R^2)$; separate scales change which errors the loss emphasizes, which is what M2 calls for.

Each component exists in some form. The contribution lies in answering each mechanism with one removable part and testing it against the strongest alternative.

### 8.2 Baselines

| Model | What it tests |
|---|---|
| DreamerV3-style world model with categorical stochastic latents, as published | Standard practice, reconstruction objective |
| JEPA-style latent-prediction world model (EMA target encoder, action-conditioned predictor, VICReg; SIGReg as a check), with readouts trained on frozen and jointly trained features | Objective, as practiced |
| Reconstruction and latent-prediction objectives on one shared backbone and readout | Objective, controlled (H3) |
| DreamerV3-style model with mirror augmentation applying the full reflection operator | Augmentation |
| SWAP-style equivariant world model with stochastic latents, as published | Equivariant practice |
| Six output families on one deterministic equivariant encoder | M1, controlled (H1) |
| Input-conditioned SymPE with a persistent draw, with and without the evidence slot | Strongest existing symmetry-breaking remedy |
| Approximately equivariant model (Wang, Walters and Yu, 2022) | Relaxed symmetry |
| Snapshot that stores the state when the observed differential command returns to zero | Simplest memory remedy, needing no extra signal |
| VariBAD-style belief over a task embedding | Existing belief-state approach |
| Full-history transformer | Uncompressed memory |
| Recent-window context model; invariant encoder; exact Bayes predictor | Information-restricted reference, negative control, ceiling |

All learned models get the same persistent storage (80 values between steps, counting any stored copy), parameter counts within 10%, identical training updates, episodes and losses, the same tuning budget on validation data, and the same number of samples for predictive means.

## 9. The training and evaluation pipeline

![Training and evaluation pipeline](../../output/research-claude/figures/training-pipeline.svg)

*Figure 1. The pipeline from simulation to a locked test. Whole body families are split before any episode, window or mirror copy exists. Each stage keeps the time grid, units and left/right channel names; the strip under each stage states what it preserves and how it keeps test information out. The test split is scored once, against the exact Bayes predictor.*

A **body family** is one draw of body parameters together with its mirror twin, the same draw with $b$ replaced by $-b$. Families are the unit of independence for the data: every episode, probe variant, hold, query branch, noise replicate and mirrored copy generated from a family stays in that family's split. Training seeds are the unit of independence for comparisons between training procedures. The table states, for each step, what is preserved, what keeps test information out of training, and which unit is independent at that point.

| Step | What happens | Shape and structure kept | Split and leakage guard | Independent unit |
|---|---|---|---|---|
| 1. Sample | Draw body parameters and form mirror twins; draw probe and query signs | Parameters and seeds saved with the generator version | Families are assigned to pilot, training, validation and test before anything is simulated, from a separate seed stream | Family |
| 2. Simulate | Probe, full reset, hold and query; clone the state at the query start for each branch | Native time step and SI units; named left/right channels; arrays `[episode, time, channel]` and query targets `[episode, branch, horizon, channel]` | Branches and replicates inherit their family's split; held-out query combinations appear only in test | Episode within family |
| 3. Window | One history per episode, ending at the start of the query | No resampling or time stretching; shorter histories padded and masked | Query targets never enter inputs; memory reset at each episode; branches never update one another | Episode within family |
| 4. Mirror (augmented baseline only) | Apply the reflection operator: negate odd channels and swap query branches, and for the walker exchange left and right joints, motors and feet | Every shape, unit and time stamp | Mirrored copies stay in their source family's split; each is checked against a simulation of the reflected body | Not a new unit |
| 5. Normalize | Scale channels | Odd channels centered at zero with symmetric scales, so reflection still flips their sign; scales frozen across conditions; transforms saved and invertible | Scales come from training families or fixed physical constants | — |
| 6. Train and select | Fit models and readouts; choose settings | Channel order and time grid | Settings chosen on validation families only; hidden body parameters stored in a file the training code cannot open | Training seed |
| 7. Test | Score once | Predictions on the target's grid and in its units | Run only after the analysis plan is registered and every setting is frozen | Seed, with families nested |

Appendix C lists every array with its shape, type and channel parity, the reflection operator for each tier, and seven automated checks. Among them: reflecting twice returns the original array, a simulated mirror twin reproduces the mirrored record, and bodies differing only in $b$ give identical hold records.

## 10. The line of inquiry

The study proceeds as a chain of hypothesis, test and decision, so that each result determines what is asked next.

**Loop 0: is the information there?** *Hypothesis:* after a probe the data determine the sign of $b$, and after the reset nothing more is revealed. *Test:* exact references, the reset check and the information audit, in the cart and the walker. *Decision:* if the recent-window or no-probe references beat chance, or the Bayes risk drifts across holds, the episode is redesigned before any model is trained.

**Loop 1: do standard world models keep it?** *Hypothesis:* at least one standard world model loses contrast skill as the hold lengthens. *Test:* the published-style reconstruction, latent-prediction, augmented and equivariant models at default settings. *Decision:* if all keep $S \ge 0.9$, the registered knob grid is used to map where they stop doing so, and the paper becomes a map of where symmetry priors are safe. If some fail, Loop 2 asks why.

**Loop 2: which mechanism explains the loss?** *Hypotheses:* H1–H5. *Test:* each mechanism's knob, with the others held off, and the linear studies. *Decision:* each mechanism receives one verdict (supported, detectable but small, excluded, or inconclusive). Only supported mechanisms enter the explanation of Loop 1, and M1 additionally requires that swapping the output family repairs the failing model.

**Loop 3: does the matching component repair it?** *Hypothesis:* adding the component that answers a supported mechanism restores skill, and removing it from the full model removes the gain. *Test:* single additions to the best baseline and single removals from the signed-belief model, against SymPE, the snapshot and the belief-state baselines. *Decision:* if a simpler baseline matches the full model, the contribution narrows to diagnosis with a simple fix, and the paper says so.

**Loop 4: does the account survive contacts and pixels?** *Hypothesis:* the memory mechanism and the remedy comparison replicate in the walker, and H3 holds in walker images. *Test:* memory arms and the signed-belief model against the snapshot and SymPE through joint sensors; the objective × background factorial through the camera. *Decision:* a finding is called general only if it replicates; findings tested only in the cart are reported as such.

**Loop 5: does it say anything about real motion?** *Hypothesis:* frozen features of the user's pose encoders hold usable information about the signed knee edit that their original decoders did not use. *Test:* original decoders, new readouts and the zero-change predictor on identical cases of the untouched cohort. *Decision:* the discussion of the user's earlier finding reports recoverability by readout class and makes no claim beyond it.

## 11. Statistical analysis

**Validity gate.** Before any hypothesis is tested, hold records must be identical across bodies that differ only in $b$, recent-window and no-probe references must be at chance (equivalence within ±0.02), the Bayes risk must be constant across holds within 1% in the primary memory condition, probed episodes must leave at least 80% of the symmetric-guess error explainable, and the references must meet their convergence tolerance.

**Inference.** Because the claims compare training procedures, the independent unit is the training seed. For each endpoint and seed, the difference between methods is computed on the full test set, pairing seeds by index so that both methods share data order and initialization stream. A paired $t$ interval over 10 seeds is then taken, and a bootstrap over families within each seed reports test-set sampling error separately, which shows whether a conclusion is robust to the particular bodies drawn for the test set. In an adversarial check, a five-seed percentile bootstrap excluded a true zero 16% of the time at a nominal 5%. The pilot's variance components are therefore used to simulate the full design before registration, and the procedure must achieve at least 94% coverage of 95% intervals and family-wise error at or below 5%; otherwise more seeds or a crossed random-effects model are used.

**Decisions.** Within each family of tests, intervals are simultaneous at the Bonferroni level, and each hypothesis's effect is oriented so that the predicted direction is positive. Every verdict has two parts. *Direction* is supported when the lower bound is above zero. *Magnitude* is compared with the meaningful effect $\delta$: it is *established* when the lower bound reaches $\delta$, *unresolved* when $\delta$ lies inside the interval, and *excluded* when the upper bound falls below $\delta$. A mechanism enters the explanation of Loop 1 when its direction is supported and its magnitude is not excluded, and the paper calls an effect meaningful only when its magnitude is established. The cart hypotheses form one family, the walker's replications another, the camera factorial a third, and the pose re-analysis is descriptive.

**Registration.** After the pilot and the coverage simulation, and before Loop 1, the knob grid, hypotheses, effect sizes, estimators, analysis code and data manifests are registered with a timestamp on OSF. Test splits are generated from their own seed streams and scored once, in week 12, by a script that checks the registration first. Any later change is logged with its reason, and the analyses it affects are labeled exploratory. Appendix D gives the full plan.

## 12. What each outcome would mean

| Pattern of results | What the paper claims | Title |
|---|---|---|
| Standard models fail; mechanisms supported; the signed belief beats every simpler alternative | A diagnosis and a remedy | *Keeping the Hidden Side* (this proposal's title) |
| Standard models fail; mechanisms supported; a snapshot or SymPE matches the signed belief | A diagnosis, with simple fixes that suffice | *Four Ways to Lose a Weak Side* |
| Standard models succeed by default and fail only when the knobs are pushed | A map of where symmetry priors are safe | *Probe, Hold, Query* |
| H3 strongly supported in pixels | The training objective decides what a world model keeps | *Symmetric Plans, Asymmetric Bodies* |
| Mechanisms excluded or inconclusive | A benchmark with negative findings, reported as such | *Probe, Hold, Query* |

## 13. Plan, compute and risks

**Timeline.** Week 1: simulators, references, and a check that the pose checkpoints exist. Week 2: reset check, information audit, validity gate, pilot, coverage simulation, walker and camera feasibility, registration. Weeks 3–4: Loop 1. Weeks 5–7: Loop 2 and the linear studies. Weeks 8–9: Loop 3. Weeks 10–11: Loops 4 and 5. Week 12: locked tests. Week 13: writing.

**Compute.** Counting every combination of model, condition, tuning configuration and seed (Appendix E), the core cart experiments need about 150 GPU-hours, the walker through joint sensors 68, the camera factorial 102, the pose re-analysis 10, and pilot, coverage simulation and scoring 35, about 365 in total under a cap of 400. The core cart experiments and the walker are protected; the camera tier is reduced before either.

| Risk | Early sign | Response |
|---|---|---|
| Every standard model already keeps the asymmetry | Loop 1 | Map the boundary with the registered knobs; report the benchmark outcome |
| The released walker falls, or its contrast does not increase with $b$ | Week-2 check | Revise the push-off once; otherwise limit claims to the cart and the pose re-analysis |
| Coverage simulation fails at 10 seeds | Week 2 | Crossed random-effects inference, or more seeds with a smaller grid |
| H3 is inconclusive in pixels | Loop 4 | Report the cart result alone for the objective comparison |
| Pose checkpoints unavailable | Week 1 | Drop the re-analysis and name it as future work |
| A simple baseline matches the signed belief | Loop 3 | Report the diagnosis with the simple fix |

## 14. Limitations

The analyzable results come from simulation, and each formal statement holds only under its assumptions. M1's pathwise statement needs reflection-fixed inputs, M2's needs linear predictors and squared error, M3's needs a conditionally uninformative hold and a contracting update, and M4's needs a frozen direct head, all under Assumption S. The camera tier changes what the model sees and keeps the walker's physics. The pose re-analysis uses synthetic edits on real motion and supports no clinical claim. The signed-belief model's parts each exist in some form, and if a simpler alternative matches it, that is the finding the paper will report.

## References

- Assran, M. et al. (2023). Self-supervised learning from images with a joint-embedding predictive architecture. *CVPR*. arXiv:2301.08243.
- Assran, M. et al. (2025). V-JEPA 2: Self-supervised video models enable understanding, prediction and planning. arXiv:2506.09985.
- Balestriero, R. and LeCun, Y. (2025). LeJEPA: Provable and scalable self-supervised learning without the heuristics. arXiv:2511.08544.
- Bardes, A., Ponce, J. and LeCun, Y. (2022). VICReg: Variance-invariance-covariance regularization for self-supervised learning. *ICLR*.
- Bengio, Y., Simard, P. and Frasconi, P. (1994). Learning long-term dependencies with gradient descent is difficult. *IEEE Transactions on Neural Networks* 5(2).
- Chen, Y. and Liu, Y. (2026). Compact but moving: Intervention-relevant geometry in recurrent world models. arXiv:2609.21787.
- Gneiting, T. and Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. *JASA* 102(477).
- Hafner, D. et al. (2019). Learning latent dynamics for planning from pixels. *ICML*. arXiv:1811.04551.
- Hafner, D. et al. (2023). Mastering diverse domains through world models. arXiv:2301.04104.
- Hewitt, J. and Liang, P. (2019). Designing and interpreting probes with control tasks. *EMNLP*. arXiv:1909.03368.
- Izenman, A. J. (1975). Reduced-rank regression for the multivariate linear model. *Journal of Multivariate Analysis* 5(2).
- Kaba, S.-O. and Ravanbakhsh, S. (2023). Symmetry breaking and equivariant neural networks. arXiv:2312.09016.
- Kirchmeyer, M. et al. (2022). Generalizing to new physical systems via context-informed dynamics model. *ICML*. arXiv:2202.01889.
- Kumar, A. et al. (2021). RMA: Rapid motor adaptation for legged robots. *RSS*. arXiv:2107.04034.
- Lan, K. et al. (2026). SWAP: Symmetric equivariant world-model for agile robot parkour. arXiv:2606.19928.
- Lawrence, H., Portilheiro, V., Zhang, Y. and Kaba, S.-O. (2025). Improving equivariant networks with probabilistic symmetry breaking. *ICLR*. arXiv:2503.21985.
- Lawrence, H. et al. (2026). To augment or not to augment? Diagnosing distributional symmetry breaking. *ICLR*. arXiv:2510.01349.
- Lee, K. et al. (2020). Context-aware dynamics model for generalization in model-based reinforcement learning. *ICML*. arXiv:2005.06800.
- Lillemark, H. J. et al. (2026). Flow equivariant world models: Memory for partially observed dynamic environments. *ICML*. arXiv:2601.01075.
- Littwin, E. et al. (2024). How JEPA avoids noisy features: The implicit bias of deep linear self distillation networks. *NeurIPS*. arXiv:2407.03475.
- Mahmood, N. et al. (2019). AMASS: Archive of motion capture as surface shapes. *ICCV*.
- Ordoñez-Apraez, D. et al. (2025). Morphological symmetries in robotics. *International Journal of Robotics Research*. arXiv:2402.15552.
- Sandilya, R., Liston, C. and Grosenick, L. (2026). Identifiable world models from pretrained diffusion representations. arXiv:2610.07028.
- Saxe, A. M., McClelland, J. L. and Ganguli, S. (2014). Exact solutions to the nonlinear dynamics of learning in deep linear neural networks. *ICLR*. arXiv:1312.6120.
- Smidt, T. E., Geiger, M. and Miller, B. K. (2021). Finding symmetry breaking order parameters with Euclidean neural networks. *Physical Review Research* 3, 012002.
- Stone, A., Ramirez, O., Konolige, K. and Jonschkowski, R. (2021). The Distracting Control Suite: A challenging benchmark for reinforcement learning from pixels. arXiv:2101.02722.
- Tassa, Y. et al. (2018). DeepMind control suite. arXiv:1801.00690.
- Wang, H. (2026). Certified world models: Predictability across configuration, horizon, and resolution. arXiv:2606.13092.
- Wang, R., Walters, R. and Yu, R. (2022). Approximately equivariant networks for imperfectly symmetric dynamics. *ICML*. arXiv:2201.11969.
- Wang, R., Hofgard, E., Gao, H., Walters, R. and Smidt, T. E. (2024). Discovering symmetry breaking in physical systems with relaxed group convolution. *ICML*. arXiv:2310.02299.
- Weiler, M. et al. (2018). 3D steerable CNNs: Learning rotationally equivariant features in volumetric data. *NeurIPS*. arXiv:1807.02547.
- Xu, Y. et al. (2020). A theory of usable information under computational constraints. *ICLR*. arXiv:2002.10689.
- Yeh, R. A., Hu, Y.-T. and Schwing, A. G. (2019). Chirality nets for human pose regression. *NeurIPS*. arXiv:1911.00029.
- Zhou, G., Pan, H., LeCun, Y. and Pinto, L. (2024). DINO-WM: World models on pre-trained visual features enable zero-shot planning. arXiv:2411.04983.
- Zintgraf, L. et al. (2020). VariBAD: A very good method for Bayes-adaptive deep RL via meta-learning. *ICLR*. arXiv:1910.08348.

---

## Appendix A. Assumptions and proofs

**Assumption S (symmetric data-generating process).** The distribution of $(g, |b|)$ does not depend on the sign of $b$, which is $\pm$ with probability one half; the overall signs of probes and queries are drawn independently of $b$; the initial and reset states are unchanged by reflection; and sensor noise has the same law after reflection. The body distribution is frozen as $g \sim \mathrm{U}[1-w, 1+w]$ (with $w = 0$ in the primary memory condition) and $|b| \sim \mathrm{U}[0.1, 0.3]$.

**Proposition 0 (the best predictor is equivariant).** Under S, $(MH, Mq, MY)$ has the same law as $(H, q, Y)$, so $\mathbb E[Y \mid Mh, Mq_0] = \mathbb E[MY \mid h, q_0] = M\,\mathbb E[Y \mid h, q_0]$, because $M$ is linear.

**Proposition 1 (symmetry).** For an input with $Mx = x$, equivariance gives $f(x) = f(Mx) = Mf(x)$, and $M$ negates odd components, so they vanish. A passive cart history with only even channels satisfies $Mh = h$, and $M(h, +u) = (h, -u)$; since total force is even, $\hat J(h, -u) = \hat J(h, +u)$ and the predicted contrast is zero. A stochastic model's predictive distribution on such an input must equal its own reflection, which constrains the distribution and leaves each sample free. Inputs with odd channels are not fixed points, and the statement does not apply to them.

**Proposition 2 (capacity).** With centered variables, or an intercept fitted outside the rank budget, the rank-$k$ squared-error optimum projects the least-squares fit onto the $k$ leading eigenvectors of $C = \Sigma_{ys}\Sigma_{ss}^{+}\Sigma_{sy}$, with $\Sigma_{ss}^{+}$ the pseudoinverse (Izenman, 1975). Under S, $\mathbb E[y_e s_o^\top] = \mathbb E[y_e(-s_o)^\top]$, so every even–odd cross-covariance is zero and $C$ is block-diagonal; for distinct eigenvalues its eigenvectors lie within blocks.

**Proposition 3 (memory).** A hold loss that does not depend on $z_o$ has zero gradient with respect to it. Later losses reach $z_{o,t}$ through $A_o^{T-t}$, and $\|A_o^{n}\| \le \|A_o\|^{n} \le r^{n}$. A bound on the spectral radius alone would not suffice: for $A_o = \begin{pmatrix} r & 1 \\ 0 & r \end{pmatrix}$ the off-diagonal entry of $A_o^n$ is $n r^{n-1}$, so non-normal updates can amplify before they decay, and the experiments measure Jacobian norms.

**Proposition 4 (coupling).** Write the head as $\hat y_e = g_1(z_e, z_o, a_e) + g_2(a_e, a_o)$. Setting $a_o = 0$ in the equivariance condition shows $g_1$ is even in $z_o$; substituting back shows $g_2$ is even in $a_o$; hence $\hat y_e(+u) = \hat y_e(-u)$.

**Lemma A1 (cost of merging).** The midpoint $c$ minimizes $\tfrac12(m_+ - c)^2 + \tfrac12(m_- - c)^2$, with value $(m_+ - m_-)^2/4$; outcome noise adds the same constant to every predictor.

**Query impulse after a full reset.** With $q_L + q_R = 2a$ throughout and $d(0) = 0$, $F_+ = 2ga + b\,d(t)$ with $\tau\dot d = 2u - d$, so $J = 2gaH + b\int_0^H d\,dt$. For a step of amplitude $\alpha$, $\int_0^H d\,dt = 2\alpha\kappa$ with $\kappa = H - \tau(1 - e^{-H/\tau})$.

**Centered probe statistic.** With $\bar d$ the mean of $d_t$ over the probe, $\sum_t (d_t - \bar d)F_{+,t} = 2ga\sum_t (d_t - \bar d) + b\sum_t (d_t - \bar d)d_t + \sum_t (d_t - \bar d)\varepsilon_t$. The first term is zero for any probe, and $\sum_t (d_t - \bar d)d_t = \sum_t (d_t - \bar d)^2$. Reversing the probe's sign negates $d_t - \bar d$ and leaves $b\sum_t (d_t - \bar d)^2$ unchanged. Centering is needed because, with actuator lag, equal positive and negative command areas do not make $\sum_t d_t$ vanish: $\int d\,dt = 2\int u\,dt - \tau[d(T) - d(0)]$.

**Regression coefficient of the asymmetry.** For evidence $X = sb + \varepsilon$ and response $Y = tb$, with $b$ and $\varepsilon$ independent and zero-mean, $\mathrm{Cov}(X, Y)/\mathrm{Var}(X) = st\,\mathrm{Var}(b)/(s^2\mathrm{Var}(b) + \sigma^2)$.

**Equivariance of the two-sided belief.** With component $s$ computed from $\psi(c^+, sc^-)$, the map $c^- \mapsto -c^-$ turns evaluation $s$ into the original evaluation $-s$ and the odd context $s\rho$ into $-s\rho$, so $q(M\kappa \mid Mc) = q(\kappa \mid c)$.

**Point prediction from samples.** One draw $\tilde r$ from the exact posterior predictive has $\mathbb E[(\tilde r - r)^2] = 2R_{\text{Bayes}}$, since $\tilde r$ and $r$ are independent given the history; the mean of $N$ draws has $(1 + 1/N)R_{\text{Bayes}}$.

## Appendix B. The deep-linear study

Inputs and targets are generated from independent latent factors with simultaneously diagonal covariances: a *common* factor with large variance and a high coefficient (the analogue of $g$), a *signed* factor with small variance and coefficient $t/s$ (the analogue of $b$ under an informative probe), and distractors whose coefficients lie below, at and above the signed factor's, each at two variances.

*Stage 1* reproduces the setting of Littwin et al.'s solved dynamics: square weight matrices, targets from the current encoder with stopped gradients, their aligned initialization, and a step size small enough that halving it changes each factor's learning time by less than 2%, at depths 1, 2 and 4. The learning order predicted by their expressions, which depend on variance, cross-covariance and coefficient, is compared with the step at which each factor's projection reaches half its final norm, including cases in which the prediction does not favor the signed factor.

*Stage 2* replaces the stop-gradient target with an exponential moving average and narrows the width below the number of factors. These leave the theorem's setting, so their results are reported as empirical extensions without a derived prediction.

## Appendix C. The data contract

**Arrays.**

| Array | Shape and type | Channels and parity |
|---|---|---|
| Cart observations | `[N_ep, 1000, 3 + n_d]` float32, 100 Hz | position, velocity, total force (even); distractors with parity labels |
| Cart commands | `[N_ep, 1000, 2]` float32 | common $a$ (even), differential $u$ (odd) |
| Flags, mask, time | `[N_ep, T, 2]` uint8; `[N_ep, T]` bool; `[N_ep, T]` float32 | probe and hold flags (even); padding masked; time never stretched |
| Cart query commands and targets | `[N_ep, 2, 50, 2]`; `[N_ep, 2, 50, 3 + n_d]` float32 | branch axis $(+u, -u)$; per 10 ms interval: end position, end velocity, average force, distractors |
| Walker observations | `[N_ep, T, 18]` float32, 40 Hz | eight positions excluding forward translation, nine velocities, total vertical ground force |
| Walker frames | `[N_ep, T, 64, 64, 3]` uint8 | rendered frames with the left leg colored |
| Walker commands and targets | `[N_ep, T, 6]`; `[N_ep, 2, 20, 19]` | six motors; positions, velocities and the vertical force under each foot |
| Index | `[N_ep, 5]` int64 | family, twin sign, probe sign, query type, replicate |
| Hidden parameters | separate file keyed by family | every body parameter and seed; readable only by reference and scoring code |
| Pose re-analysis | `[N_win, 128, 12, 2]` float32 at 25 Hz, with confidence and availability `[N_win, 128, 12]` | the original study's layout, unchanged |

Interval-averaged force targets make the impulse an exact sum, $J = 0.01\sum F$, so no endpoint interpolation is needed.

**Reflection operator.** For the cart, multiply each channel by its parity label, negate $u$, and swap the branch axis. For the walker, exchange left and right joint, motor and foot channels and swap the branch axis; for frames, render the reflected state. For the pose data, use the original pipeline's physical mirroring, which reflects the 3D body, exchanges side indices and re-projects. Reflection never changes a shape, a unit or a time stamp.

**Automated checks**, run on every generated file and in continuous integration:
1. Reflecting twice returns every array unchanged.
2. A simulated mirror twin reproduces the mirrored record to $10^{-9}$ relative error; for frames, the discrepancy between the color swap and the reflected render is reported.
3. Normalization commutes with reflection.
4. Every equivariant model satisfies $f(Mx) = Mf(x)$ to $10^{-5}$ on random inputs.
5. Replaying identical inputs from a cloned state reproduces the trajectory.
6. After the reset, bodies that differ only in $b$ produce identical hold records under identical noise.
7. No two splits share a family, seed, background clip or content hash, and the training loader raises an error if asked to open the hidden-parameter file.

**Pose re-analysis splits.** Readouts are fitted on the original 112 training people, tuned on the 14 development people and scored once on the locked cohort; every derived window, mirrored copy and edit level inherits its person's split, and intervals resample people.

## Appendix D. Registered analysis plan

**Primary endpoints and meaningful effects.**

| Hypothesis | Endpoint (oriented so the prediction is positive) | Meaningful effect |
|---|---|---|
| H1 | Energy score of the branch pair on passive, reflection-fixed histories: best single-peaked family minus persistent draw; trajectory version for independent per-step minus persistent draw | A quarter of the gap between the true passive law and the best Gaussian under the energy score |
| H2 | (Drop in skill from low to high distractor variance at width 16) minus (the same drop at width 64), reconstruction objective. Capacity competition additionally requires the width-16 drop to persist under restarts, per-level learning-rate tuning and doubled training, and a frozen-readout trade-off between asymmetry and distractor recoverability; otherwise the verdict is "width-dependent interference" | $\delta_S$ |
| H3 | Interaction of objective (reconstruction minus latent prediction) with distractor predictability (low minus high), shared backbone and readout; in the cart and, as a separate family, in walker images with shuffled versus smooth video backgrounds | $\delta_S$ |
| H4 | Delay-specific readout skill at a 2 s hold minus an 8 s hold, probe and hold losses only, no flag, $g$ known; shared readouts, probe-end recoverability and the invertible contracting control reported alongside | $\delta_S$ |
| H5 | Mean skill over five training-set sizes on held-out queries, multiplication minus concatenation | $\delta_S$ |
| Linear check | Width at which reduced-rank regression drops the contrast, measured minus predicted | Exact, outside the family |

**Validity gate.** As in Section 11, plus reference convergence: predictive means and second moments, Bayes risk and reference scores each within a tenth of their meaningful effect, and for importance sampling an effective sample size of at least 1,000 per history with agreement across two seeds.

**Inference.** Seeds are the independent units, with 10 seeds per primary comparison and a paired $t$ interval with nine degrees of freedom. A within-seed bootstrap over families (10,000 draws, keeping twins, episodes, branches and replicates together) reports test-set error. The coverage simulation uses the pilot's family and seed variance components and must show at least 94% coverage and family-wise error at most 0.05.

**Families and decisions.** The cart family (H1 with its trajectory version, H2, H3, H4, H5; $m = 6$) uses simultaneous intervals at level $1 - 0.05/6$. The walker family has two tests, the H4 replication and the comparison of the signed-belief model with the snapshot and SymPE baselines, each one-sided at level $1 - 0.05/2$ and run with 10 seeds. The camera family is the H3 interaction alone, with 5 seeds and a $t$ interval with four degrees of freedom; its coverage is checked in the same simulation, and its lower power is stated. Verdicts have the two parts given in Section 11: direction, and magnitude relative to $\delta$.

**The signed-belief model succeeds** if the lower simultaneous bound of its contrast skill is at least 0.9, its difference from the validation-selected best baseline is above zero, and the upper bound on its relative increase in next-step error is below 5%. Crashed fits and non-finite predictions count against the model that produced them.

**Registration and deviations.** Registered at the end of week 2: knob grid, hypotheses, $\delta_S$, estimators, thresholds, analysis code and its hash, family manifest hashes and the Monte Carlo sample count. The test splits are scored once, in week 12. Deviations are logged with their date and reason, and every affected analysis is labeled exploratory.

## Appendix E. Experiment inventory

One cart fit takes about 15 GPU-minutes (6 for the smallest training sets). A walker joint-sensor fit takes about 1 GPU-hour, since its episodes are about 220 steps at 40 Hz, and a walker camera fit about 3. The pilot measures all three before registration. Four tuning configurations per model run once at the base condition and are reused across knob levels, as registered.

| Priority | Work | Fits | GPU-hours |
|---|---|---:|---:|
| Core | Loop 1: four standard models × (4 tuning + 10 seeds) | 56 | 14 |
| Core | H1: six output families × (4 + 10) | 84 | 21 |
| Core | H2/H3: 3 variances × 2 widths × 2 objectives × 10 seeds, plus restarts, per-level re-tuning and doubled training at width 16 | 120 + 52 fit-equivalents | 43 |
| Core | H4: 4 loss arms × 2 memory types × 10 seeds, plus a 3-seed flag arm; the contracting-code control runs on a CPU | 104 | 26 |
| Core | H5: 2 fusion types × 5 sizes × 10 seeds, plus the shortcut control | 110 | 11 |
| Core | Loop 3: full model, 4 removals, SymPE ± slot, snapshot, belief state, persistent-draw ablation × (4 + 10) | 140 | 35 |
| Protected | Walker joint sensors: 2 memory arms × 10 seeds; 4 models (reconstruction, SymPE, snapshot, signed belief) × (2 tuning + 10 seeds) | 68 | 68 |
| Reducible | Walker camera: 2 objectives × 3 backgrounds × 5 seeds, plus 4 tuning fits | 34 | 102 |
| Cheap | Pose re-analysis readouts | — | 10 |
| Overhead | Pilot, profiling of the longest episodes, coverage simulation, readouts and scoring | — | 35 |
| **Total** | | **≈ 770** | **≈ 365** |

Secondary knobs run at three seeds only if the pilot leaves budget under the 400 GPU-hour cap.
