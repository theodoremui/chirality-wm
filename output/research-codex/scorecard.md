# Multi-dimensional scorecard

The original proposal scores **66.6/100** and the final revision **83.0/100** under the same independent-review rubric. This is an improvement in research-plan quality, not a measured gain in model performance or an acceptance probability. Novelty remains the limiting dimension because the proposed experiment has not yet shown that its memory mechanism improves on ordinary context or stored summaries.

Each dimension is scored from 0 to 5, with half-points allowed. Weighted total = Σ(weight × score / 5). The original source audit's separate **64.2/100** uses different criteria, including evidence maturity; it is not part of this longitudinal series. See the [review protocol](review-protocol.md) for definitions and provenance.

| Dimension | Weight | Original | V1 | V2 | V3 | V4 | V5 | V6 | V7 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Significance | 12% | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 |
| Novelty | 18% | 2.0 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 |
| Conceptual/mathematical correctness | 12% | 4.5 | 4.5 | 4.5 | 4.0 | 4.5 | 4.5 | 4.5 | 4.5 |
| Method specificity | 12% | 3.0 | 3.0 | 3.5 | 4.0 | 4.0 | 4.5 | 4.5 | 4.5 |
| Identification/causal validity | 10% | 4.0 | 4.0 | 4.5 | 4.5 | 4.5 | 4.5 | 4.5 | 4.5 |
| Data fidelity/leakage | 10% | 4.0 | 4.0 | 4.5 | 4.5 | 5.0 | 5.0 | 5.0 | 5.0 |
| Experiments/baselines | 10% | 3.5 | 3.5 | 4.0 | 4.0 | 4.5 | 4.5 | 4.5 | 4.5 |
| Statistics/falsifiability | 8% | 3.0 | 3.0 | 3.5 | 4.0 | 4.0 | 4.0 | 4.5 | 4.5 |
| Feasibility | 4% | 2.0 | 3.5 | 4.0 | 4.0 | 4.0 | 4.5 | 4.5 | 4.5 |
| Clarity | 4% | 3.0 | 4.5 | 4.5 | 4.5 | 4.5 | 4.5 | 4.5 | 5.0 |
| **Weighted total /100** | **100%** | **66.6** | **70.8** | **76.2** | **77.0** | **80.2** | **81.8** | **82.6** | **83.0** |

## What changed, and what remains unproved

| Version | Score | Main improvement | Most important remaining concern |
|---|---:|---|---|
| [Original](review-v00-original.md) | 66.6 | Correct measurement and reflection distinctions | Learning contribution, scope, and primary inference remain underspecified |
| [V1](review-v01.md) | 70.8 | A focused, time-bound memory question | Sensor changes could be mistaken for forgetting |
| [V2](review-v02.md) | 76.2 | Exact observation/reset construction and physical endpoint | Delayed-query training may equal ordinary endpoint supervision |
| [V3](review-v03.md) | 77.0 | A concrete gated context and uncertain sign representation | Neutral observations can refine correlated nuisance uncertainty |
| [V4](review-v04.md) | 80.2 | Exact versus uncertain regimes; complete data and target contract | Matching the learning path and simplest memory baselines |
| [V5](review-v05.md) | 81.8 | Shared proper scores, full gradients, baseline registry, compute limits | Fitting allocation, inference, and failures need final locks |
| [V6](review-v06.md) | 82.6 | Executable confirmation protocol and conditional contact replication | Cross-episode memory leakage and changing-code interpretation |
| [V7](review-v07.md) | 83.0 | Integrated narrative, prior-work distinctions, and final control definitions | Method novelty and generality require actual results |

The mathematical score briefly decreases in V3 because its new gate exposed an overlooked nuisance-inference issue; V4 resolves it by separating known and unknown nuisance regimes. The final novelty score remains 2.5/5. This is deliberate: more precise prose and more controls cannot supply a missing empirical contribution.

## Final assessment

The final version is a strong prospective protocol with a narrow, testable question and unusually explicit information boundaries. It is ready to guide a feasibility pilot. It is **not yet a submission-ready empirical ICML paper**. Its central risk is that standard identification or simply storing the diagnostic summary will already solve the problem. That outcome should change the paper's claim rather than be hidden by additional architecture.

A stronger methods claim requires a reproducible benefit beyond the matched learned baselines, evidence that the benefit concerns retained predictive information, and a successful structurally different replication. A useful benchmark or diagnostic paper remains possible if the controls instead establish where conventional methods suffice. The [selection memo](icml-positioning-and-selection.md) maps these result patterns to appropriate claims.

All seven revisions remain prospective. Completed work in this package consists of source/literature analysis, document revision, original vector illustration, and explicitly labeled analytical checks. The [revision ledger](revision-ledger.md) records how every review issue was handled.
