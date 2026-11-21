# Testing Mechanical Memory Against the Explanations That Could Defeat It

**Version 5 · Research proposal · 23 October 2026**  
**Status:** proposed experiments, revised after the [version 4 review](../../output/research-codex/review-v04.md).

## Abstract

Predicting a new physical input can require information that was visible only earlier in a trajectory. We propose a bilateral actuator benchmark that makes this requirement testable without confusing it with missing sensors, uncertain nuisance parameters, or train–test overlap. A controlled diagnostic condition has a known observation law: an early response reveals mechanical imbalance, while later neutral measurements carry no further information about it. A nonlinear condition then relaxes the known-parameter assumption and permits later observations to remain useful. Recurrent models, stored diagnostic summaries, and ordinary identification receive the same causal records. A modest persistent-context candidate tests whether an explicit update rule helps under limited memory. The study measures complete force trajectories and their integrated response, while treating any gain over conventional methods as an empirical question.

## Motivation and measurable objective

World models predict how observations change under inputs. Bilateral mechanics provide a simple test of what their internal state must retain: similar total motion can arise from a stronger left actuator or a stronger right actuator, yet the same later differential command can produce different responses. Asymmetry is useful here because it creates a signed physical distinction with a declared transformation law.

The supplied JEPA paper studies pose restoration and reports unresolved incremental benefits. The URTC draft reports complete source-video overlap in its classifier split. Neither provides a completed mechanics-memory result. We retain their lessons about anatomical indexing, trivial controls, and independent experimental units, as documented in the [source audit](../../output/research-codex/source-evidence-audit.md).

**Within twelve weeks, can a persistent-context model reduce nonlinear delayed-impulse MSE by a confidence-supported 5% against the strongest validation-selected recurrent or stored-summary comparator, while meeting near-term and uncertainty guardrails?** The fixed horizon is 0.5 seconds and the primary delay is eight seconds. The exact diagnostic validates the interpretation; the nonlinear condition is the main empirical comparison. All targets, schedules, memory budgets, and tuning access are shared. A null result remains evidence about when conventional identification or simple memory is sufficient.

## Physical systems and limits of the observation claim

A cart obeys $m \ddot x = F_L + F_R - kx - c\dot x$. The actuator equations are $\tau  \dot q_L=\phi (a+u)-q_L$ and $\tau  \dot q_R=\phi (a-u)-q_R$, with forces $(g+b)q_L$ and $(g-b)q_R$. Common input $a=0.6$ is even under reflection, differential input $u$ and imbalance $b$ are odd. Forward position, velocity, and total force are even. Reflection swaps actuator labels; it does not reverse the cart's forward axis.

The **exact diagnostic** fixes and discloses $g=1\,\mathrm{N}$, $\tau =0.1\,\mathrm{s}$, $m=1 \mathrm{kg}$, $k=2 \mathrm{N/m}$, $c=0.4 \mathrm{N\,s/m}$, and $\phi (v)=v$. Only signed $b$ is unknown. Following a diagnostic pulse block, set $x=v=0$ and $q_L=q_R=a$, retaining mechanics and model memory. Under subsequent $u=0$, every observation distribution is independent of $b$. Known nuisance values prevent neutral data from refining a nuisance posterior correlated with imbalance. The later impulse under constant query $u$ is

$$
J = 2gaH + 2bu[H - \tau (1 - \exp (-H/\tau ))]
$$


The **nonlinear condition** uses $\phi_\alpha(v)=\frac{\tanh(\alpha v)}{\tanh(\alpha)}$ with unknown $g,\tau ,\alpha ,m$. Reset activations to $\phi _\alpha (a)$. At fixed nuisance parameters neutral observations are sign-independent, but they can refine nuisance uncertainty and thereby alter the posterior over imbalance. We make no claim that this delay is wholly uninformative. An all-observations Bayesian reference tests that distinction. The gated candidate may discard useful information and is explicitly compared with unrestricted context updating. A no-reset condition measures how much ordinary continuous observations reduce the need for stored diagnosis.

For two equally likely histories with the same stored state and conditional means $m_+$ and $m_-$ under the same future query, the best shared prediction has excess MSE $\frac{(m_+-m_-)^2}{4}$. This elementary diagnostic identity concerns fixed queries, not jointly mirrored body/query pairs. It is not a theorem that trained world models collapse.

## Reproducible episode and split contract

Records use SI units and a 100 Hz observation clock. A two-second diagnosis contains eight 0.25-second blocks: $[+0.10,0,-0.10,0,+0.25,0,-0.25,0]$ for $u$; reversing all pulse signs is sampled independently of the body sign. Delay is selected from 0, 1, 4, or 8 seconds. Query input is drawn from $\{-0.25,-0.10,+0.10,+0.25\}$ and announced only at forecast origin. The simulator uses an internal step of 0.001 seconds, with step-halving checks before data lock.

Nonlinear body support is $g\in [0.8,1.2]\,\mathrm{N}$, $\lvert b\rvert\in [0.1,0.3]\,\mathrm{N}$, $\tau \in [0.05,0.15]\,\mathrm{s}$, $m\in [0.8,1.2] \mathrm{kg}$, and $\alpha \in [0.5,2]$; $k,c$ remain as above. Each family contains both signs of one magnitude draw and all branches, resets, initial-state continuations, mirrors, and noise replicas. No sign pair becomes two independent bodies. Position, velocity, and total-force observation noise have standard deviations 0.001 m, 0.01 m/s, and 0.03 N, respectively. Additional noise settings are sensitivity analyses.

Split family identifiers 70/15/15 before any derived windows. For support-shift testing, reserve the combination $\lvert b\rvert>0.25\,\mathrm{N}$ and $\tau >0.125\,\mathrm{s}$; neither its training nor validation families are admitted. Each marginal range remains represented outside that corner. Independent interpolation confirmation draws from the remaining support. Query extrapolation to magnitude 0.35 is a separate secondary test; inputs remain physically admissible. Save generator version, seeds, parameter support, family membership, and content hashes in a manifest. The pilot uses separate families and freezes the final counts and manifest before confirmation.

Raw observations are `[episode,time,3]` in the order $(x,v,F_{\mathrm{total}})$. Commands are `[episode,time,2]` in the order $(a,u)$. Flags, timestamps, and masks share the time axis. At time $t_k$, observe $y_k$, then apply command $a_k$ on $[t_k,t_{k+1})$. History contains $y_0\ldots y_k$ and previously applied commands, while the announced query is a separate future input. Filters use only that history. A physical reset is recorded as a discontinuity and flag, not silently interpolated.

For each of 50 forecast intervals, store $(x_{\mathrm{end}},v_{\mathrm{end}},F_{\mathrm{average}})$ where the force average is the simulator integral over that interval divided by 0.01 seconds. Target shape is `[batch,50,3]`, and $J=0.01 \sum  F_{\mathrm{average}}$; this removes endpoint-sampling ambiguity. Raw force observations are instantaneous readings and remain separate from these derived training targets. No target enters the query-origin encoder. Padding retains slots and masks; time is never stretched. Exact geometry is not claimed unchanged by normalization: raw values remain immutable and the documented model view is invertible.

Normalization must commute with reflection. Even scalar channels may use training means; odd channels use zero centering and a shared positive training scale. Paired channels, when exposed in an oracle check, use identical scales. Masks and flags are even, and odd state coordinates negate. Check reflection twice returns the original record, transformed predictions obey the declared law, and preprocessing preserves that equality. Branches clone the full physical and random state and pass identical-input replay before use.

## Candidate and the shared prediction law

The candidate stores 64 dynamic and 64 context-evidence values, partitioned into even and odd channels. Shared-function evaluations on original/reflected inputs yield half-sum/half-difference updates. Dynamics update after every real measurement; context accumulates during diagnosis and is copied afterward. Every model receives the gate. It matches the exact diagnostic's known observation law; in the nonlinear condition it may discard useful nuisance evidence.

For evidence $(e,o)$, use $P(S=s)\propto \exp  d(e,s o)$, $\log  R\mid S=s\sim \mathcal{N}(\mu (e,s o),\sigma ^2(e,s o))$, and odd context $sR$. Reflection exchanges signs and preserves magnitude distributions. Even nuisance context depends on the same component. Draw context once per forecast and initialize changing state conditionally on it. The decoder admits odd-by-odd products in even force predictions. Parity permits signed information but cannot guarantee retention.

Each sample produces 50 future $(x_{\mathrm{end}},v_{\mathrm{end}},F_{\mathrm{average}})$ rows, and its impulse is their force sum times 0.01 seconds. There is no independent impulse head. Samples express uncertain context/state plus a declared residual process model shared across comparators. Future response targets never enter the recurrent input during query rollouts.

## Actual gradient and scoring paths

The shared loss combines a trajectory energy score and impulse CRPS. Energy score compares sampled complete trajectories with the target, then subtracts half the distance between independent predictive samples. CRPS applies this construction to scalar impulse with absolute distance. Both are proper distributional scores in expectation; their sum deliberately reweights a derived outcome rather than treating it as an independent observation.

Normalize trajectory channels by fixed scales $(1\,\mathrm{m},1 \mathrm{m/s},1\,\mathrm{N})$ and divide trajectory Euclidean distance by the square root of 150 scalar entries. Scale impulse by $1 \mathrm{N\,s}$; its loss coefficient is one. A zero-impulse-weight sensitivity tests ordinary reweighting. Add the same one-step physical score during history processing, with coefficient one and averaging over timestamps before combining terms.

For each origin, use two independent sample banks, each containing four reparameterized continuous draws per sign component. The data-distance term sums weighted samples; the pair-distance term sums across banks with product weights. Mixture probabilities receive direct gradients; categorical sampling is not falsely treated as differentiable. Both banks count toward compute. Evaluation uses 128 stratified samples; a validation-only 32/128/512 comparison checks stability before locking 128. Common random numbers reduce Monte Carlo comparison noise without increasing the number of independent families.

All recurrent baselines backpropagate through diagnosis and the entire delay. A truncated-gradient arm is a labeled ablation outside the primary comparator set. Query targets enter losses only; predicted futures have no future-observation teacher forcing. Origins, branches, masks, updates, and physical-target exposures are identical. Log auxiliary/main gradient norms, clipping frequency, wall time, and peak memory. The supplied JEPA paper's unequal auxiliary influence makes these controls especially relevant.

## Frozen comparator registry

| ID | Stored memory and update | Role |
|---|---|---|
| C | 64 dynamic + 64 gated parity context | Candidate |
| B1 | 128-value ordinary recurrence | Primary competitor |
| B2 | 64 dynamic + 64 generic context, always updated | Primary competitor |
| B3 | 64 dynamic + 64 parity context, always updated | Primary competitor |
| B4 | 64 dynamic + 64 generic gated context | Primary competitor |
| B5 | Copy final diagnostic state, 128 values | Primary competitor |
| B6 | 64-value diagnostic snapshot + 64 changing values | Primary competitor |

Each receives the same mixture family, current origin observation, and known query. Match useful trainable parameter counts within 10% by changing active decoder widths; report actual differences. The principal constraint is 128 stored real values, not an information-theoretic bit budget. Precision, query storage, and sensor buffers are shared. Parity requires two evaluations, so fixed-memory results do not imply fixed-compute efficiency. A secondary equal-wall-time comparison reports that different question.

The primary comparator is the B1–B6 model with lowest validation impulse MSE, with ID order breaking ties. Test scores never select it. Full-history learned prediction, recent-window prediction, equation-aware Bayesian identification, compact fitted-parameter summaries, and privileged mechanics oracles are separately labeled references. Their extra history storage or simulator-law knowledge is disclosed; their success remains scientifically important.

## Retention and temporal-composition tests

Lower eight-second error can reflect better dynamics or calibration. For a retention interpretation, measure recoverability at diagnosis end and after 1, 4, and 8 seconds. Freeze encoders. Fit one linear and one two-layer nonlinear readout on training-family memories pooled across these times, tune on validation, then lock it. Each receives only memory and query; its target is the same canonical-reset impulse for that body's mechanics at every delay. This removes changing physical state from the target. Report paired deterioration from diagnosis end alongside full-history, recent-window, and no-diagnosis references. Readout failure establishes only a limitation of tested function classes.

The secondary temporal test announces either $+0.25$ then $-0.25$, or the reversed order, switching at 0.25 seconds. These amplitudes occur in training, while switched schedules never enter training, validation, or selection. This tests temporal composition separately from magnitude extrapolation. All branches begin from cloned physical state after their schedule is declared; logged future feedback commands cannot enter the forecast.

## Inference, resources, and contribution boundary

Average queries, signs, replicas, and five fitted seeds within independent families. The primary contrast is $D=R_C-0.95R_B$, with validation-selected B fixed. Require its upper 95% paired family interval below zero, a near-term RMSE deterioration bound below 0.02 N·s, and a CRPS deterioration bound below 0.01 N·s. These conjunctive conditions support one combined claim. Architecture, shifted-support, switched-query, and delay comparisons remain exploratory. The main interval is conditional on the five fits; show each seed's effect separately.

Pilot risk sets $\delta =0.05R_B$ and precision target $\epsilon =\delta /4$; pilot paired standard deviation gives $n=\left\lceil\left(\frac{1.96s_D}{\epsilon}\right)^2\right\rceil$, capped at 200–2,000 confirmation families. If the cap is insufficient, disclose this limitation. Validation comparator RMSE below 0.01 N·s triggers a floor report rather than a relative superiority claim.

The seven core methods each receive three learning-rate configurations with one tuning seed; each selected configuration then receives five seeds, for 56 principal fits. Keep update count and data exposure equal. Pilot timing sets the per-fit budget under a total 120 accelerator-hour ceiling including ablations. The pilot must establish that the registry fits before execution. Drop optional studies before altering the primary contrast. Weeks 1–2 verify the generator, weeks 3–5 establish controls, weeks 6–8 train, weeks 9–10 confirm, and weeks 11–12 analyze. Human acquisition and adaptive probing are excluded.

A cart result remains a controlled identification-memory study. A broader claim requires a preregistered structurally different replication, such as a compact bilateral contact walker, with candidate, selected recurrent comparator, and snapshot control. Its observation audit must be repeated; the cart's exact ambiguity argument does not transfer automatically. This extension is conditional on a successful core study and the resource gate, rather than promised evidence.

[Chirality Nets](https://arxiv.org/abs/1911.00029), [SWAP](https://arxiv.org/abs/2606.19928), [RMA](https://arxiv.org/abs/2107.04034), and [VariBAD](https://arxiv.org/abs/1910.08348) establish the architectural and context-inference ingredients. [V-JEPA 2](https://arxiv.org/abs/2506.09985), [Identifiable World Models](https://arxiv.org/abs/2610.07028), and [Compact but Moving](https://arxiv.org/abs/2609.21787) constrain broad predictive-memory novelty. The intended contribution is an experimentally discriminating benchmark and a mechanism result only if snapshot, optimization, and identification alternatives fail to explain it.
