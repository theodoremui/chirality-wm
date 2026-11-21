# Research strategy and ICML positioning

The strongest paper would explain a consequential failure of predictive compression, establish when it occurs, and show which intervention on learning remedies it under fair resource constraints. Mechanical asymmetry provides a controlled setting for this question because the sign of a hidden parameter can matter for a later command even when ordinary motion looks similar. The general issue is memory for future decisions under partial observation; gait supplies motivation and a possible external application.

This emphasis fits ICML’s stated assessment of soundness, presentation, significance, and originality. Its reviewer instructions explicitly recognize new empirical insights and improved understanding of existing methods as potential contributions. A new architecture is therefore optional; a convincing scientific result is essential. These are the verified 2026 criteria, not a claim about an unannounced 2027 deadline or format. [ICML reviewer instructions](https://icml.cc/Conferences/2026/ReviewerInstructions).

## What the original already gets right

The supplied proposal separates identifiability from representation quality, correctly transforms controls along with bodies under reflection, treats context as persistent within a rollout, and distinguishes prospective forecasting from replay with future logged controls. Its total-force example and loss-coordinate equivalence are useful. These strengths should be preserved rather than rediscovered and advertised as new contributions.

The common-rubric independent review gives the original **66.6/100** for proposal design; the separate source audit gives **64.2/100** under its own broader rubric, including evidence maturity. These are compatible judgments from different criteria and must not be plotted as if they were one measurement. Neither is an acceptance probability.

The main weaknesses are an underspecified learning intervention, an expansive simulator-and-human-data program, and the absence of a fixed primary effect and operational stopping rules. The chemistry material is removable because it does little work in the proposed inference. The supporting manuscripts contribute useful warnings about loss weighting, missingness, anatomical identity, and source leakage, but no completed evidence for hidden-mechanics forecasting.

## Selection of techniques

| Candidate | Decision | Reason and decisive test |
|---|---|---|
| Fixed diagnostic interaction followed by a delayed query | Core experiment | Separates acquiring evidence from using it later. Full-history, recent-window, and no-diagnosis references establish whether memory is needed. |
| Reflection-equivariant recurrence | Strong baseline and structural ablation | Preserves the possibility of signed states and shares statistical strength across reflected systems. Existing constructions already provide this capability. Compare with ordinary recurrence under the same objectives. |
| Persistent probabilistic context | Candidate memory mechanism | Allows episode-constant properties to survive changing motion. Must beat ordinary context inference; mixtures must preserve unresolved signs instead of averaging them into a fictitious symmetric body. |
| Delayed-query training or rehearsal | Shared training design; rejected as standalone novelty | Places supervision where forgotten context matters. The later revisions give the same delayed targets and scores to every comparator, and isolate changes in memory updates instead. |
| Response-conditioned representation metric | Diagnostic, not main method | Functional differences under a fixed command are more meaningful than arbitrary latent distances. A metric based only on the mean can miss different uncertainty distributions. |
| Active probe selection | Defer | Adds experimental design and policy-coverage questions before a retention gap has been established. Fixed probes suffice for the first claim. |
| Large pretrained video JEPA | Optional visual transfer | Valuable for later observations from images, but it confounds the initial study with image decoding, domain shift, and costly pretraining. Start with controlled physical observations. |
| Multiple human archives | Reduce to one gated extension | Different protocols do not create missing crossed interventions. Chronology, prospective control availability, and participant identity must be verified before choosing an endpoint. |
| Parameter-sign supervision | Privileged diagnostic or oracle | Useful for checking simulator truth, but it would add information if supplied only to the candidate during training. A named latent coordinate is not evidence of identified mechanics. |

Reflection-equivariant forecasting is established by [Chirality Nets](https://arxiv.org/abs/1911.00029), while [SWAP](https://arxiv.org/abs/2606.19928) and [VariBAD](https://arxiv.org/abs/1910.08348) constrain architecture and uncertainty claims. [Compact but Moving](https://arxiv.org/abs/2609.21787) is particularly relevant to testing whether latent information remains useful after recurrent updates. The [literature audit](literature-audit.md) details these boundaries and the closest additional work.

## Interpret results before choosing the paper’s claim

| Observed pattern | Defensible conclusion | Next step |
|---|---|---|
| Full history cannot predict better than recent observations | The proposed condition has no established retention problem | Fix the experiment or report its information limit; do not increase model complexity reflexively. |
| A simple identifier and ordinary context model both solve the benchmark | Conventional memory suffices in this regime | Publish the boundary if informative, or find a motivated harder regime without suppressing these results. |
| Native decoder fails but a frozen-memory probe succeeds | Information is recoverable by that probe class | Improve the readout or its objective; avoid claiming erased information. |
| A candidate beats short-horizon training but ties equal delayed supervision | Horizon or weighting explains the gain | Frame the contribution as training guidance and a diagnostic benchmark. |
| A persistent-memory mechanism wins after resource and optimization controls | Evidence supports that mechanism in the tested regime | Replicate with new parameter combinations and a second dynamical setting before broader claims. |
| Improvement appears only after oracle mechanics labels or future feedback controls are supplied | Extra information explains the comparison | Report it as an oracle or retrospective result and restore the prospective comparison. |
| Mean error improves but ambiguous-history uncertainty becomes overconfident | Prediction quality has an unresolved tradeoff | Revise the distributional model and report both outcomes. |

The primary result should be a family-level effect on a physically interpretable future response. Separate plots should expose how that effect changes with delay, probe informativeness, and nuisance variation. A small collection of carefully discriminating experiments will be more persuasive than a long benchmark list whose models receive different information.

## Suggested final paper structure

Open with the practical need to predict responses to changed inputs, then use the bilateral example to define the information problem. State the restricted research question before introducing a network. Describe the benchmark’s information boundaries and split construction, followed by the proposed learning intervention and its strongest alternatives. Present results in the order: information is available; a specified memory fails or succeeds; a controlled intervention changes the result; the retained information improves a new response prediction. End with the limits of the measurement system, the tested action family, and the evidence for transfer.

A final manuscript should report completed negative results as readily as positive ones. Seven better research plans still leave the central empirical question unanswered until the experiment is run.
