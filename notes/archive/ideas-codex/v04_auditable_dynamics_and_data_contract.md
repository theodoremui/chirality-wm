# An Auditable Benchmark for Mechanical Memory

**Version 4 · Research proposal · 23 October 2026**  
**Status:** proposed experiments, revised after the [version 3 review](../../output/research-codex/review-v03.md).

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

## Memory, training, and coherent prediction

The candidate stores 64 dynamic and 64 context-evidence values, with even/odd partitions. Shared-function evaluations on original and reflected inputs produce half-sum/half-difference updates. Dynamic state updates on every observation; context accumulates during the known diagnosis block and is copied later. The gate is an experimental protocol input available to every model, not a hidden sign label. In the nonlinear condition it is an approximate inductive bias whose cost is measurable.

For context evidence $(e,o)$, a two-sign mixture uses $P(S=s)\propto \exp  d(e,s o)$ and $\log  R\mid S=s\sim \mathcal{N}(\mu (e,s o),\sigma ^2(e,s o))$, with odd context $sR$. Reflection exchanges sign components and leaves their magnitude distributions unchanged. Even nuisance context can depend on the same component. Draw context once per forecast and initialize the changing latent state conditionally on it; retain context through the rollout. Odd-by-odd interactions permit the mechanical response to appear in even force predictions.

Every predictive sample produces the complete 50-interval trajectory. Integrate its force averages to obtain that sample's impulse; no separate impulse head can improve the score while contradicting the force trajectory. The simulator has deterministic mechanics with noisy past sensors. Future physical-sample uncertainty arises from inferred context/state and the model's declared residual process distribution, shared across baselines. Use a proper sample-based score, CRPS, for impulse: it rewards accurate distributions and penalizes unnecessary spread. Trajectory and derived-impulse losses form a weighted composite objective; their dependence precludes describing the sum as a likelihood of independent observations. Freeze loss scales and sample count using training/validation only.

## Comparators and interpretation

The core factorial crosses gated versus ordinary context updates with parity-consistent versus unrestricted dynamics, keeping memory, mixture family, targets, and decoder capacity equal. Add a simple baseline that copies its 128-value final diagnostic encoder state and uses the same current observation and query decoder; a 64-value snapshot plus 64-value changing-state variant matches the candidate's partition. A compact fitted-parameter summary is an even simpler competitor. These controls test whether the supplied gate, rather than a new representation mechanism, explains success.

Full-history learned prediction and all-observations nonlinear identification are information references with their storage and equation knowledge disclosed. Recent-window, no-diagnosis, zero-response, and parameter-oracle controls delimit observability and floor performance. Frozen linear/nonlinear probes fit only on training families, tune on validation, and receive stored state plus the same query. They diagnose recoverability within their classes; failed readouts do not prove erasure.

## Inference, decision gates, and related work

Average queries, signs, replicas, and five fitted seeds within each independent family. The primary contrast is $D=R_{\mathrm{candidate}}-0.95R_{\mathrm{comparator}}$, where risks are physical impulse MSE in $(\mathrm{N\,s})^2$. Select the comparator on validation only. Require an upper 95% paired family interval below zero, near-term RMSE deterioration below 0.02 N·s, and CRPS deterioration below 0.01 N·s. All conditions are required for one combined improvement claim; separate architecture and delay comparisons are exploratory. Conditional-family intervals do not establish reliability over arbitrary new training runs; show seed-specific contrasts separately.

Pilot comparator risk sets the target effect $\delta =0.05R_{\mathrm{comparator}}$ and interval half-width $\epsilon =\delta /4$. With pilot paired standard deviation $s_D$, choose $n=\left\lceil\left(\frac{1.96s_D}{\epsilon}\right)^2\right\rceil$, capped at 200–2,000 confirmation families. This is a precision approximation, not a power guarantee. If the cap is inadequate or comparator validation RMSE is below 0.01 N·s, report a floor or precision limitation rather than weakening the threshold. The exact diagnostic is a validation of the benchmark law; the nonlinear condition supplies the single primary learned-model claim. Support-shift and extrapolation claims use separately labeled exploratory intervals until a final multiplicity plan is frozen.

Weeks 1–2 verify data and observation laws; weeks 3–5 establish identification and snapshot baselines; weeks 6–8 run matched learning comparisons; weeks 9–10 open the frozen confirmation set; weeks 11–12 analyze and write. No human acquisition or active probing is required. A result limited to these cart systems remains a controlled identification-memory study; broader claims require structurally different dynamics.

[Chirality Nets](https://arxiv.org/abs/1911.00029) and [SWAP](https://arxiv.org/abs/2606.19928) establish equivariant recurrence. [RMA](https://arxiv.org/abs/2107.04034), [VariBAD](https://arxiv.org/abs/1910.08348), and [model adaptation](https://arxiv.org/abs/1803.11347) establish history-based context. [V-JEPA 2](https://arxiv.org/abs/2506.09985) already supplies action-conditioned predictive learning. [Identifiable World Models](https://arxiv.org/abs/2610.07028) and [Compact but Moving](https://arxiv.org/abs/2609.21787) make an unrestricted intervention-memory novelty claim untenable. The possible contribution is the auditable diagnostic and a result that survives these conventional alternatives.
