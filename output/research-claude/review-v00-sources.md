# Review 0: the source proposals

**What was graded.** The original proposal *When Symmetry Hides the State: Learning Asymmetric Mechanics through Controlled Response* (PDF, 12 October 2026) and the seven Codex revisions in `notes/archive/ideas-codex/` (v01–v07, 23 October 2026). The two supporting manuscripts, *Evaluating JEPA-Inspired Motion Representations through Geometry and Gait Asymmetry* and the URTC draft *Learning Monocular Gait Representations through Neurologically Informed World Models*, were read as evidence and are not graded. The rubric is in [scoring-rubric.md](scoring-rubric.md).

## Scores

| Dimension (weight) | Original PDF | Codex v01 | v02 | v03 | v04 | v05 | v06 | v07 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ICML significance (14) | 6 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| Novelty and positioning (14) | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 |
| Technical soundness (12) | 8 | 7 | 8 | 7 | 8 | 8 | 8 | 8 |
| Research question, SMART (10) | 4 | 6 | 7 | 7 | 7 | 7 | 7 | 7 |
| Experiments and baselines (12) | 5 | 5 | 6 | 6 | 7 | 7 | 7 | 7 |
| Data fidelity and leakage (8) | 6 | 6 | 7 | 7 | 8 | 8 | 9 | 9 |
| Statistics and falsifiability (8) | 5 | 5 | 6 | 7 | 7 | 7 | 8 | 8 |
| Feasibility and timeline (7) | 3 | 6 | 6 | 6 | 6 | 6 | 5 | 6 |
| Clarity, first principles (10) | 5 | 6 | 5 | 4 | 4 | 3 | 3 | 3 |
| Narrative arc (5) | 4 | 5 | 5 | 4 | 4 | 3 | 3 | 3 |
| **Weighted total** | **51.5** | **54.5** | **58.5** | **56.6** | **59.8** | **58.3** | **59.2** | **59.9** |

The Codex series gains about eight points over the original, nearly all of it in leakage control, statistics, and the definition of the research question. Significance, novelty, and clarity do not improve, and clarity falls steadily from v03 onward as protocol detail accumulates. The series reaches a plateau near 59–60 because none of the revisions adds an idea that would make an ICML reader care about the answer.

## What the original proposal gets right

1. **Identification and retention are different questions.** The proposal asks first whether the experiment contains information about the hidden mechanics, and only then whether the learned representation keeps it. This ordering is the single most valuable idea in the source material, and every later version should keep it.
2. **An even measurement can reveal an odd parameter.** In the two-actuator example, total forward force $F_+ = 2g\bar a + 2bu$ is unchanged by swapping sides, yet its slope with respect to the differential command $u$ is $2b$, whose sign says which side is stronger. Proposition 1 (finite response contrasts have parity $p$, $-p$, $p$) states this cleanly and is correct.
3. **Changing coordinates creates no information.** Identity (10), $(e_L+e_R)^2 + (e_L-e_R)^2 = 2(e_L^2+e_R^2)$, shows that an equal-weight loss on sums and differences is a rescaled bilateral loss. This is an important guardrail against a tempting but empty "asymmetry-aware loss".
4. **Three prediction settings are kept apart.** Prospective known-input prediction, policy-conditional prediction, and retrospective replay receive different information. The warning that logged feedback commands can leak future state (Figure 7) is correct and often ignored in world-model evaluation.
5. **Splitting before windowing** and keeping mirror variants, branches, and renderings of one trajectory family in the same split are correct leakage controls.

## Critiques of the original proposal

**C1. The chemistry section does no technical work.** Section 2 spends about two pages on molecular chirality, enantiomeric excess, and the 2026 Chemistry Nobel. The Codex literature audit found an Académie des sciences announcement corroborating the prize, so the issue is relevance and not accuracy. The proposal itself concedes that "molecular chirality and bilateral gait asymmetry remain different concepts" and that recurrent prediction "is not chemical autocatalysis". An ICML reviewer will read the section as padding. The only transferable lesson, that a normalized imbalance can change because its numerator or its denominator changes, fits in one sentence.

**C2. There is no account of why a learned model would lose the information.** The representation hypothesis says a model trained for ordinary prediction "can discard" recoverable information. Almost any model can discard almost any information, so the hypothesis cannot fail in an informative way. A useful hypothesis names a mechanism and predicts when the loss happens. Without one, the experiments can only report that a gap exists or does not.

**C3. The contribution is an evaluation without a primary endpoint.** The proposal disclaims novelty for equivariance, recurrence, and response supervision, and offers "a controlled account of when information is present, retained, and useful". That is a defensible contribution only if the account produces a sharp measurement. The falsification table (Table 4) lists comparisons but no metric, threshold, or decision rule.

**C4. Scope exceeds any realistic timeline.** The plan moves from the analytic toy to a MuJoCo body, then MyoSuite, then four human datasets with five secondary resources. The proposal itself notes that human records cannot supply matched counterfactual branches and that no human dataset varies mechanics and probes together. The human tier therefore cannot test the central claim, yet it consumes most of the planning text (Section 6.2 and Appendix C).

**C5. The symmetry literature that most constrains the design is missing.** A deterministic function that is equivariant under a reflection must return a mirror-symmetric output when its input is mirror-symmetric. This is Curie's principle in neural form, studied by Smidt, Geiger and Miller (2021), Kaba and Ravanbakhsh (2023), and Lawrence et al. (ICLR 2025). A passive history in the toy is exactly mirror-symmetric, so any deterministic equivariant model must predict zero slope to a differential probe. The proposal's idea of sampling persistent mechanics once per rollout is the correct remedy, but it is not connected to this work and there is no deterministic-equivariant baseline to show the remedy matters.

**C6. The user's own most interesting result is under-used.** In the JEPA asymmetry manuscript, a baseline that always predicts zero change in knee asymmetry had lower error (5.81°) than all sixteen trained variants, even though those variants improved pose restoration. The proposal cites the manuscript only as motivation that "does not establish" erasure. That caution is right, but the observation deserves a hypothesis: small signed components of a target may be the first to be sacrificed by squared-error training. Littwin et al. (NeurIPS 2024) show that latent-prediction (JEPA) and reconstruction objectives prioritize different features in deep linear networks, which turns the observation into a testable comparison.

**C7. Hedging hides the claims.** Almost every paragraph closes with a disclaimer ("This is prior work, not the proposed model", "it does not establish..."). Each disclaimer is accurate, but at this density the reader cannot find what the authors believe.

## Critiques of the Codex revisions

**K1. Precision replaced significance.** Across seven versions the question narrows to whether a gated persistent context lowers delayed impulse MSE on a cart by 5% relative to a validation-selected baseline. The question is measurable and achievable, but a 5% MSE gain on a two-motor cart is unlikely to interest an ICML audience, and the threshold is not tied to any practical consequence.

**K2. The candidate's success is close to built in.** From v03 onward the context accumulator is opened by a public "diagnosis gate" and copied unchanged afterward, while the reset makes delay observations exactly uninformative. A model told when to write and then told to stop writing will retain the diagnostic evidence. The proposals acknowledge that gated copying is conventional (v07, "Gated copying remains conventional"), which leaves the method with little to contribute.

**K3. Protocol detail crowds out ideas.** Training seeds 17, 29, 43, 61, 89; bootstrap seed 20261023; 56 principal fits; 120 accelerator-hours; a 0.02 N·s guardrail; 4,200 training families. These belong in a preregistration appendix. In the main text they bury the argument. The abstracts of v04, v05, and v06 are identical, which suggests the framing stopped being revisited.

**K4. Readability declines with each version.** Equations appear as inline code (`τ q'_L=φ(a+u)−q_L`), terms such as CRPS, energy score, intersection–union test, and stratified sample banks appear with one-clause definitions, and paragraphs pack five or six technical decisions. A reader outside the subfield cannot follow v05–v07.

**K5. JEPA disappears as a subject of study.** The supplied manuscripts are about JEPA-style representations, and the user's interest is in predictive world models. The Codex versions cite V-JEPA 2 only to rule out the claim that "adding actions to JEPA" is new. The more interesting question, whether latent-prediction objectives keep small signed information better or worse than reconstruction objectives, is never asked.

**K6. There is no theory of failure.** The factorial compares update rules and parity structures, but no version says which failure each comparison is meant to detect. Without a mechanism-to-experiment map, a positive result cannot be explained and a negative result cannot be diagnosed.

**K7. The walker extension is unworkable as written.** v06–v07 propose open-loop schedules on the dm_control planar walker. An open-loop planar walker falls within a few hundred milliseconds of losing balance, so the plan needs either a nominal feedback policy with open-loop query windows or a different body.

**K8. There is no story.** The documents read as protocols. Nothing tells the reader what was learned at each step or why the next experiment follows.

What the Codex series did well should be kept: exact-versus-uncertain regimes (v04), the excess-risk identity for merged histories, $(m_+ - m_-)^2/4$ (v02), normalization that commutes with reflection (v04), branch cloning with identical-input replay checks (v03), memory resets between independent episodes (v07), and the rule that crashed fits veto a superiority claim (v06).

## Suggestions for the first Claude revision

1. **Cut the chemistry and the human datasets from the core.** Keep one sentence on the ratio lesson and, at most, one optional real-motion check that uses data already in hand.
2. **Open with the world-model motivation.** A world model is valuable because it can answer "what happens if I do this?" before acting. An asymmetric body breaks that answer whenever the model treats its two sides as interchangeable.
3. **Organize the work around availability, retention, and use**, and measure retention relative to an exact Bayesian reference so that information the data never contained is not counted as forgetting.
4. **Represent uncertainty about the sign explicitly**, using a belief with one component per side, so that a model can stay undecided under passive observation and commit after a probe.
5. **Bring JEPA back as an object of study** by comparing latent-prediction, reconstruction, and response-trained world models on the same episodes.
6. **Limit the simulation ladder to two tiers**: the two-actuator system, where the exact Bayesian answer is computable, and one articulated walker.
7. **Write the mathematics in standard notation**, define each term once in plain language, and move protocol constants to an appendix.
8. **Give the paper a line of inquiry**: each experiment should answer a question whose answer decides the next one.
