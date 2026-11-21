# Review 7: *Keeping the Hidden Side* (v07, final)

**Proposal:** [docs/ideas-claude/v07_keeping_the_hidden_side.md](../../docs/ideas-claude/v07_keeping_the_hidden_side.md)
**Pre-review snapshot:** [review-snapshots/v07-before-codex-review.md](review-snapshots/v07-before-codex-review.md)

## Scores before the Codex review

| Dimension (weight) | v06 (corrected) | v07 draft | Reason for the change |
|---|---:|---:|---|
| ICML significance (14) | 9 | 9 | Unchanged; the motivating exoskeleton case makes the stakes concrete |
| Novelty and positioning (14) | 7 | 8 | A related-work section with five groups and an explicit gap; the model is honestly presented as a combination, so the novelty rests on the diagnostic account, the benchmark and the controlled objective comparison |
| Technical soundness (12) | 6 | 8 | All eleven v06 Codex findings addressed: deterministic encoder for output families, optimization interventions, delay-specific readouts, privileged pixel reference, recomputed mirrored labels, continuous magnitudes, centered statistic, two-part verdicts |
| Research question, SMART (10) | 8 | 9 | One sentence states endpoint, thresholds, population and date |
| Experiments and baselines (12) | 7 | 9 | Shared-backbone factorials isolate the objective and the output family; the walker replicates what the budget supports at full strength |
| Data fidelity and leakage (8) | 10 | 10 | The pipeline table now states shape, split, leakage guard and independent unit for each step in the main text |
| Statistics and falsifiability (8) | 9 | 9 | Two-part verdicts separate direction from magnitude |
| Feasibility and timeline (7) | 5 | 7 | Every fit counted, 365 GPU-hours under a 400 cap, with a reducible camera tier |
| Clarity, first principles (10) | 6 | 8 | First-principles section, plain-language statement before each formal one, protocol detail moved to appendices |
| Narrative arc (5) | 9 | 9 | Six loops, each a hypothesis, a test and a decision; outcomes mapped to claims |
| **Weighted total** | **75.2** | **85.8** | |

## Strengths

- **The argument can be followed from the first page.** The exoskeleton example shows why a world model needs the asymmetry, the cart shows how it hides, and the four mechanisms say how it can be lost, before any protocol detail appears.
- **The contribution is stated at its true size.** The related-work section places the two-sided belief inside SymPE's framework and locates the gap in persistence, retention and the separation of causes. A reviewer who knows the symmetry-breaking literature will find no overclaim.
- **Every mechanism test now identifies its mechanism.** Output families share a deterministic encoder, capacity is separated from optimization by interventions and a readout trade-off, memory loss is separated from code drift by delay-specific readouts and a contracting control, and the objective is separated from architecture by a shared backbone.
- **The user's data requirements are met in the main text.** The pipeline table states, step by step, what shape and structure are kept, how the split prevents leakage, and which unit is independent.
- **The study has a story.** Each loop's answer decides the next question, and the outcome table commits the paper to a claim under every pattern of results.

## Remaining critiques

**R1. The main text is still long for ICML.** At roughly 8,000 words before the appendices, the proposal would need trimming to fit an eight-page paper. For a proposal this length is defensible, since every section carries a decision the reader needs, but Sections 6 and 8 could lose a third of their words in the paper itself.

**R2. The plan is ambitious for 13 weeks.** Two simulators, an exact reference for each, six output families, four memory arms, a camera factorial and a re-analysis is a heavy load for one researcher. The proposal protects a minimal paper (the cart core plus the walker replications), and that minimal paper should be named explicitly as the fallback deliverable.

**R3. Novelty depends on the results.** The formal statements are elementary, and the paper's value rests on the experiments producing clean signatures. The outcome table handles this honestly, but a reviewer will judge the paper on which row it lands in.

**R4. The population-balance knob deserves more weight.** When left-stronger bodies are more common, exact equivariance and mirror augmentation both impose a wrong prior. Practitioners mirror data by default, so this secondary knob may give the most directly useful advice in the paper. It could become a short headline result at little cost.

## Codex adversarial review

Codex reviewed the draft twice. The first pass returned **needs-attention** with six high and one medium finding ([raw output](codex-adversarial/codex-review-v07.txt)). After the revision, a confirmation pass ([raw output](codex-adversarial/codex-review-v07-confirmation.txt)) judged all seven resolved and raised two new high findings, which were then fixed as well.

**First pass.**

| # | Severity | Finding | Disposition in the final v07 |
|---|---|---|---|
| X1 | high | H3's registered contrast had the wrong sign and would have rejected the intended result | **Fixed.** Registered as $(S_{\text{latent,low}} - S_{\text{recon,low}}) - (S_{\text{latent,high}} - S_{\text{recon,high}})$, positive under the hypothesis, with a synthetic sign check before registration. *Confirmed resolved* |
| X2 | high | Temporally independent distractors add no predictable direction for future-target prediction | **Fixed.** Input and target timing specified for both objectives; H3 uses distractors with low but nonzero coefficient and large predictable variance; independent noise is a control attributed only to current-frame reconstruction. *Confirmed resolved* |
| X3 | high | The cart inventory never varied distractor predictability, so H3's interaction could not be estimated | **Fixed.** H3 crosses coefficient (0.3 vs 0.95) with objective in its own inventory row, within the same budget. *Confirmed resolved* |
| X4 | high | Seed-only intervals ignore the shared test families | **Fixed.** Crossed seed-by-family random-effects model with Satterthwaite degrees of freedom; the coverage simulation includes a shared family effect. *Confirmed resolved* |
| X5 | high | Beating the original pose decoder can be done with uninformative features | **Fixed.** Retained information is credited only over featureless and shuffled-feature readouts; scalar readouts are scored apart from pose restoration. *Confirmed resolved* |
| X6 | high | The baseline contract could weaken native methods or bar the full-history reference | **Fixed.** Three groups with separate contracts (native methods, controlled experiments, references); the full-history transformer is exempt from storage matching. *Confirmed resolved* |
| X7 | medium | The distinction from VariBAD was overstated | **Fixed.** Novelty narrowed to the symmetry-controlled diagnosis; VariBAD run in its original form. *Confirmed resolved* |

**Confirmation pass.**

| # | Severity | Finding | Disposition |
|---|---|---|---|
| Y1 | high | H3's interaction can pass while latent prediction is worse in both conditions | **Fixed.** The claim that latent prediction keeps the asymmetry also requires a supported low-coefficient simple effect; otherwise the result is reported as differential sensitivity |
| Y2 | high | With randomly signed queries the contrast has zero covariance with every linear input, so the linear capacity check would show nothing at any width | **Fixed.** The linear check uses one fixed registered query and the branch-pair target, with the spectrum derived for that pair and full-rank recovery verified first |

No further review was run after these two fixes; they are narrow amendments to a hypothesis's success rule and to one check's input definition.

## Final scores

| Dimension (weight) | v07 draft as first scored | v07 draft, corrected by Codex | v07 final |
|---|---:|---:|---:|
| ICML significance (14) | 9 | 9 | 9 |
| Novelty and positioning (14) | 8 | 8 | 8 |
| Technical soundness (12) | 8 | 6 | 8 |
| Research question, SMART (10) | 9 | 9 | 9 |
| Experiments and baselines (12) | 9 | 7 | 9 |
| Data fidelity and leakage (8) | 10 | 10 | 10 |
| Statistics and falsifiability (8) | 9 | 7 | 9 |
| Feasibility and timeline (7) | 7 | 6 | 7 |
| Clarity, first principles (10) | 8 | 8 | 8 |
| Narrative arc (5) | 9 | 9 | 9 |
| **Weighted total** | **85.8** | **78.7** | **85.8** |

The final total equals the first-scored draft's, and the arithmetic hides a real change. The draft scored 85.8 only because its errors had not yet been found. The final version earns the same scores with those errors removed. By the rubric's anchors, it is a strong plan with the two weaknesses a reviewer would raise: a main text long for the venue, and a novelty that depends on the experiments delivering clean signatures. Neither can be fixed by further revision before results exist.
