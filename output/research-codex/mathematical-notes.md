# Mathematical notes: what preservation can mean

These notes explain the proposal’s diagnostic arguments. They do not establish a new general theorem, prove that a trained network loses information, or identify human mechanics. The elementary identities make assumptions visible and help design experiments that could reject the proposed mechanism.

## 1. Reflection preserves a relationship, not a symmetric state

Let \(R\) exchange the left and right sides of the complete physical experiment. Because reflecting twice restores the original, \(R^2=I\). This two-element transformation group is often written \(\mathbb Z_2\). An even scalar is unchanged by \(R\); an odd scalar changes sign. For bilateral forward scalar forces in this example, \(F_L+F_R\) is even and \(F_L-F_R\) is odd. Both are needed to reconstruct the original pair.

In three spatial dimensions, choose mediolateral, forward, and vertical axes. A spatial reflection has matrix \(S=\operatorname{diag}(-1,1,1)\). Positions and forces transform by \(S\), while axial quantities such as angular momentum transform by \(\det(S)S\). Labeled skeletons also require a permutation of homologous joints. A side swap in the cart system is a simpler operation and should not be advertised as a full 3D biomechanical validation. The original proposal’s Appendix A already explains these distinctions.

Equivariance requires a predictor to transform consistently:

\[
P_\theta(\,\cdot\mid RH,RQ)=R_*P_\theta(\,\cdot\mid H,Q),
\]

where \(H\) is the available history, \(Q\) is a future input schedule, and \(R_*\) means transforming every outcome drawn from the original distribution. Each occurrence of \(R\) uses the reflection appropriate to its history, query, or output space. More precisely, the distribution on the left equals the pushforward of \(P_\theta(\,\cdot\mid H,Q)\) under the output reflection. A Gaussian requires both transformed mean and covariance; a mixture requires transformed component parameters and the weights associated with those components. Exchanging sign labels permutes their associated weights. This condition permits asymmetric physical states. It does not imply \(p(Y\mid RH,Q)=p(Y\mid H,Q)\), which holds the query fixed and asks a different question.

An odd hidden variable can interact with an odd command to produce an even output. Thus isolated even and odd streams without allowed cross-products can exclude the motivating physics. An odd feature also admits the zero function; an architectural parity label cannot guarantee that a useful signal is learned.

## 2. The sensor determines which parameter is identifiable

For the original two-actuator example,

\[
F_+=2ga+2bu,\qquad F_-=2ba+2gu.
\]

Observing only \(F_+\) at \(u=0\) leaves \(b\) unidentified. Observing labeled \(F_-\) at nonzero known \(a\) exposes it. With total-only sensing and positive admissible probe magnitude \(\delta>0\), an opposite probe pair provides

\[
\widehat b=\frac{F_+(\delta)-F_+(-\delta)}{4\delta}.
\]

For \(\sigma>0\), if the two force observations have independent Gaussian noise with variance \(\sigma^2\), the estimate has variance \(\sigma^2/(8\delta^2)\). With equally likely signs of a fixed magnitude \(b_0>0\), optimal sign error is \(\Phi(-2\sqrt 2\,b_0\delta/\sigma)\). This is a useful calibration reference under those assumptions. It does not survive unchanged when sensor scale, common gain, activation lag, or the input itself is unknown.

For an outcome response \(r_p(u;b,\xi)\) with reflection parity \(p\in\{+1,-1\}\), assume the complete context satisfies

\[
r_p(-u;-b,R\xi)=p\,r_p(u;b,\xi).
\]

Its finite slope \([r_p(\delta)-r_p(-\delta)]/(2\delta)\) has parity \(-p\) under reflected mechanics and context. This permits a total-force slope to reveal signed mechanics; it does not guarantee a nonzero or uniquely identifying slope in another physical system. Fixing gait phase incorrectly can invalidate the assumed context transformation.

## 3. Compression has a task-relative cost

Let \(Z=E(H)\) be a deterministic compressed history. The future query \(Q\) and target \(Y\) must be specified, including horizon, physical units, and sensor availability. A memory is predictively sufficient for this task family if

\[
p(Y\mid Z,Q)=p(Y\mid H,Q)
\]

almost surely under the declared experiment distribution. Sufficiency for neutral motion need not imply sufficiency for differential commands. Sufficiency for the response mean is weaker than sufficiency for its whole distribution.

For a scalar target \(Y\), under squared loss, finite second moments, and unrestricted Bayes-optimal decoders, the excess risk caused by compression is

\[
\mathcal R_Z^*-\mathcal R_H^*
=\mathbb E\left[\left(\mathbb E[Y\mid H,Q]-\mathbb E[Y\mid Z,Q]\right)^2\right].
\]

The result follows by writing the residual around the conditional expectation and applying the tower property; the cross-term vanishes. For two histories that are conditionally equally likely given the merged memory and the same query, this reduces to one quarter of their squared mean separation. Conditional weights \(w,1-w\) instead give \(w(1-w)(m_+-m_-)^2\). Assigning queries independently of hidden sign prevents the query from becoming a side channel. A trajectory-vector version requires a declared squared norm or weighted quadratic loss. Different conditional variances would still contribute to irreducible mean-squared error. Therefore a zero mean-risk gap does not establish distributional sufficiency.

For correctly defined discrete probabilities, or continuous densities with finite expected log losses and a common reference measure, the corresponding optimal log-loss gap is

\[
\mathcal L_Z^*-\mathcal L_H^*=I(Y;H\mid Z,Q).
\]

This is a conditional-information identity, not a practical estimator supplied by the proposal. A learned decoder gap can include approximation error, training error, and finite-sample variation. It cannot be relabeled as measured mutual information. In a deterministic simulator, an arbitrary continuous density score may be ill-defined at a point-mass target; declare an observation-noise model or use an appropriate predictive score whose target distribution is explicit.

## 4. Recoverability and forgetting require different evidence

A decoder’s poor forecast establishes poor performance for that decoder. A separately fitted nonlinear probe may recover the useful quantity from the same frozen state. This would show that the representation supports that readout, even if the original decoder does not exploit it. Linear and nonlinear probes should have fixed capacities, training budgets, and validation selection; only their final performance is evaluated on locked families.

If both probes fail, the warranted statement is limited to their classes and fitting procedures. The full-history reference can establish attainable prediction from the available record, but its larger storage must be reported. A comparison between a full-history transformer and a small recurrent state combines memory representation and resource allocation unless those factors are separately controlled.

A useful experiment crosses the presence of informative diagnosis with delay length. A candidate that improves only the diagnostic measurement fit has not necessarily improved retention. Testing the interaction between diagnosis availability and delay helps distinguish a broad accuracy improvement from a benefit concentrated where persistent memory is needed. This interaction is secondary unless it is separately powered and preregistered.

## 5. New coordinates do not supply new supervision

For bilateral prediction errors \(e_L,e_R\),

\[
(e_L+e_R)^2+(e_L-e_R)^2=2(e_L^2+e_R^2).
\]

Equal weights on total and difference therefore reproduce the bilateral squared loss up to scale. Unequal weights change the optimization geometry; paired response contrasts can change which errors are penalized. Their statistical noise covariance and the reused outcomes must still be accounted for. Neither operation adds information unavailable in the original measured endpoints.

Likewise, summing losses from several queries using the same retained memory is algebraically the same objective as summing those endpoint losses separately, unless the implementation changes the computation graph, available information, memory update, or effective optimization. Reusing memory may save compute; a benefit must be compared with the same target weighting and a fair compute budget before it supports a distinct learning principle.

## 6. Simulator branches and causal scope

Saved branches support controlled response comparisons only when the entire relevant initial state is shared. A MuJoCo implementation must preserve integration state and external controller, random-generator, and apparatus state; positions and velocities alone can omit actuator activation and other inputs. Pin the engine and model versions and verify identical-input replay before comparing different branches. [MuJoCo state documentation](https://mujoco.readthedocs.io/en/stable/computation/index.html#the-state).

The joint distribution of two branch outcomes depends on how disturbances are coupled. Shared randomness is a declared simulator construction. It does not identify the corresponding individual-level counterfactual coupling in human data. Marginal response forecasts can still be evaluated without claiming that their difference recovers an individual causal effect.

The [analytical check script](checks/analytic_checks.py) verifies the original force identities, parity, Gaussian toy sign error, and two-history squared-risk bound. The broader conditional-expectation identities above are explanatory mathematics; no trained-model estimate of either risk gap has been produced.
