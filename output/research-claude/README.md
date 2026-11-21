# Reviews, scores and supporting material for the Claude revisions

This folder holds the critique behind each of the seven proposal versions in [docs/ideas-claude/](../../docs/ideas-claude/). Start with the [final proposal](../../docs/ideas-claude/v07_keeping_the_hidden_side.md), then the [scorecard](scorecard.md).

## The seven versions and their reviews

Each version responds to the review of the one before it. Every review has two parts: my own multi-dimensional critique, and an independent adversarial review by Codex, with a table recording how the next version handled each finding.

| Version | Main step forward | Proposal | Review |
|---|---|---|---|
| Sources | The original PDF and the seven Codex revisions, graded on the same rubric | — | [Review 0](review-v00-sources.md) |
| 1 | Rebuilt around one example and three questions: is the asymmetry available, retained, used? | [What a Probe Reveals](../../docs/ideas-claude/v01_what_a_probe_reveals.md) | [Review 1](review-v01.md) |
| 2 | Four mechanisms by which a model can lose the asymmetry, an exact Bayesian reference, and a defined endpoint | [Four Ways to Lose the Hidden Side](../../docs/ideas-claude/v02_four_ways_to_lose_the_hidden_side.md) | [Review 2](review-v02.md) |
| 3 | A benchmark whose knobs leave the evidence fixed; contrast skill as the endpoint; experiments as a chain of decisions | [Probe, Delay, Query](../../docs/ideas-claude/v03_probe_delay_query_benchmark.md) | [Review 3](review-v03.md) |
| 4 | The signed-belief world model specified, with matched baselines and corrected mechanism tests | [A Signed-Belief World Model](../../docs/ideas-claude/v04_signed_belief_world_model.md) | [Review 4](review-v04.md) |
| 5 | A data contract and a registered analysis plan; the pipeline figure | [A Leakage-Proof Pipeline](../../docs/ideas-claude/v05_leakage_proof_pipeline_and_preregistered_analysis.md) | [Review 5](review-v05.md) |
| 6 | A walker seen through joint sensors and a camera, and real human motion | [From a Cart to Pixels and Real Motion](../../docs/ideas-claude/v06_from_cart_to_walker_pixels_and_real_motion.md) | [Review 6](review-v06.md) |
| 7 | An integrated final version: related work, a moderate main text with appendices, and the last round of corrections | [Keeping the Hidden Side](../../docs/ideas-claude/v07_keeping_the_hidden_side.md) | [Review 7](review-v07.md) |

## Supporting files

- [scoring-rubric.md](scoring-rubric.md): the ten weighted dimensions and calibration anchors used for every score.
- [scorecard.md](scorecard.md): all scores in one table, including the corrections each Codex review forced.
- [title-options.md](title-options.md): seven titles for the final proposal, with when to use each.
- [literature-verification.md](literature-verification.md): how each cited source was checked and what it is allowed to support.
- [figures/training-pipeline.svg](figures/training-pipeline.svg): the training and evaluation pipeline as editable vector art, with a [PNG preview](figures/training-pipeline.png) and a [caption and alt text](figures/training-pipeline-caption.md).
- [codex-adversarial/](codex-adversarial/): the raw output of every Codex adversarial review, one file per version.
- [review-snapshots/](review-snapshots/): version 7 as it stood before its Codex review, so the final changes can be compared.

## How the Codex reviews were run

The `codex:adversarial-review` command is defined by the installed Codex plugin (version 1.0.6) and cannot be invoked as a model tool, so each review ran the plugin's own runtime directly: `codex-companion.mjs adversarial-review --wait --scope working-tree` with a fixed focus text. To keep each review on a single proposal, it ran in a scratch git repository holding the proposal under review, plain-text copies of the three source PDFs, and the final Codex-series proposal. The focus text asked Codex to attack correctness, mechanism identification, baseline fairness, leakage, statistical validity, feasibility, novelty and source support, and to anchor every finding to a line. All seven reviews, and a confirmation pass on the revised version 7, returned "needs-attention"; their findings are recorded verbatim in `codex-adversarial/`, and each review file in this folder records how every finding was handled.

## What these files do and do not establish

Every score grades a research plan. No model has been trained and no experiment has been run, so no score predicts model performance or acceptance at ICML. The formal statements in the proposals are elementary results under stated assumptions, and the reviews say where each one stops applying.
