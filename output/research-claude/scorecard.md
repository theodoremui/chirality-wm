# Scorecard

All scores use the ten-dimension rubric in [scoring-rubric.md](scoring-rubric.md); each dimension is scored 1–10 and the weighted total is out of 100. For the Claude versions, the table shows the score *after* that version's Codex adversarial review, so each total reflects the errors Codex found in it. The first-scored values, before Codex, are in each review.

## Every version on one rubric

| Dimension (weight) | Original PDF | Codex v07 | C-v01 | C-v02 | C-v03 | C-v04 | C-v05 | C-v06 | C-v07 final |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ICML significance (14) | 6 | 5 | 6 | 7 | 8 | 8 | 8 | 9 | 9 |
| Novelty and positioning (14) | 4 | 4 | 4 | 6 | 7 | 7 | 7 | 7 | 8 |
| Technical soundness (12) | 8 | 8 | 6 | 6 | 6 | 6 | 6 | 6 | 8 |
| Research question, SMART (10) | 4 | 7 | 6 | 8 | 8 | 8 | 8 | 8 | 9 |
| Experiments and baselines (12) | 5 | 7 | 6 | 6 | 6 | 7 | 6 | 7 | 9 |
| Data fidelity and leakage (8) | 6 | 9 | 6 | 8 | 8 | 8 | 10 | 10 | 10 |
| Statistics and falsifiability (8) | 5 | 8 | 5 | 7 | 6 | 7 | 7 | 9 | 9 |
| Feasibility and timeline (7) | 3 | 6 | 7 | 6 | 6 | 6 | 6 | 5 | 7 |
| Clarity, first principles (10) | 5 | 3 | 8 | 7 | 7 | 6 | 7 | 6 | 8 |
| Narrative arc (5) | 4 | 3 | 6 | 6 | 8 | 8 | 8 | 9 | 9 |
| **Weighted total** | **51.5** | **59.9** | **59.1** | **66.8** | **69.8** | **70.8** | **72.2** | **75.2** | **85.8** |

C-vNN denotes the Claude versions in [docs/ideas-claude/](../../notes/archive/ideas-claude/). The full Codex series (v01–v07, 54.5 to 59.9) is graded in [Review 0](review-v00-sources.md).

## How each version moved the score

| Version | First scored | After Codex | Main gain | What Codex found that I had missed |
|---|---:|---:|---|---|
| [C-v01](review-v01.md) | 61.1 | 59.1 | Readable first-principles framing; availability, retention and use as the spine | Probe transients persisted in cart motion; the "exact" reference ignored nuisance parameters; the endpoint was undefined |
| [C-v02](review-v02.md) | 70.4 | 66.8 | Four mechanisms with formal statements; reset-and-hold; exact linear-Gaussian reference | The retention ratio rewarded amplified predictions; the cart's targets had rank two, so width could not create competition; the JEPA ordering was misattributed |
| [C-v03](review-v03.md) | 74.2 | 69.8 | Knobs that hold information fixed; contrast skill; experiments as loops | Scoring single samples doubled an exact sampler's risk; M1 confused latent randomness with output family; the hold could refine a coupled nuisance |
| [C-v04](review-v04.md) | 76.6 | 70.8 | The signed-belief model specified; matched budgets; deep-linear study | SymPE already has evidence-dependent weights; the control task divided by $2\hat\gamma$; normalization would have cancelled the capacity knob |
| [C-v05](review-v05.md) | 79.3 | 72.2 | Data contract with automated checks; registered analysis plan; pipeline figure | The reset left activations carrying $b$; five-seed bootstraps under-covered; stochastic baselines were mislabeled as unimodal |
| [C-v06](review-v06.md) | 81.4 | 75.2 | Walker through joint sensors and a camera; re-analysis of real motion | Stochastic backbones defeat output-family controls; mirroring need not flip the pose response sign (from the user's own paper); the walker budget could not replicate |
| [C-v07](review-v07.md) | 85.8 | 78.7 → **85.8** after final revision | Related work, restructured text, every earlier finding addressed | H3's contrast had the wrong sign; seed-only intervals; featureless readouts could pass the pose test; a confirmation pass then found a zero-covariance linear check |

Two things stand out. First, every Codex review lowered my own score, by 2 points for version 1 and by 4 to 7 points from version 3 on, almost always in soundness, experiments or statistics, so self-assessment alone was consistently optimistic about whether an experiment identified what it claimed. Second, the final version's gain over the original proposal (+34.3) comes mostly from dimensions an ICML committee weighs heavily: significance (the question became one about world models in general), the research question, experiments, data integrity and statistics. Novelty rose less (4 to 8), because the honest positioning against SymPE and VariBAD narrowed the claim even as the contribution sharpened.

## What the final score means

At 85.8 the final proposal sits in the rubric's "strong plan with one or two weaknesses" band. Those weaknesses are a main text longer than an ICML paper allows (about 9,000 words before appendices) and a novelty that depends on the experiments producing clean mechanism signatures. No score here predicts a result or an acceptance decision, since no experiment has been run.
