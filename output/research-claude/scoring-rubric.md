# Scoring rubric

Every proposal in this folder is graded on the same ten dimensions. Each dimension gets a score from 1 to 10, and the weighted total is out of 100:

$$\text{Total} = \sum_i w_i \cdot s_i / 10, \qquad \sum_i w_i = 100.$$

The weights reflect what an ICML program committee rewards in a methods-and-analysis paper about world models: a question that matters beyond one application, an idea that is new relative to the closest work, and evidence that would convince a skeptical reader. Clarity carries more weight than usual because the user asked for proposals that a non-specialist can follow from first principles.

| # | Dimension | Weight | What a 9–10 looks like |
|---|---|---:|---|
| 1 | ICML significance and generality | 14 | The question concerns how learned predictive models behave in general, with the bilateral body serving as a clean test case. A result in either direction changes how practitioners build or evaluate world models. |
| 2 | Novelty and positioning | 14 | The proposal names the closest prior work, states what that work leaves open, and has a contribution that survives the comparison. Claimed novelty comes from an idea or finding, and assembling known parts does not count. |
| 3 | Technical soundness | 12 | Definitions are correct, formal statements have explicit assumptions, and nothing claimed exceeds what the argument shows. |
| 4 | Research question (SMART) | 10 | Specific, measurable with a named metric and decision rule, achievable with the stated resources, relevant to ICML, and tied to a date. |
| 5 | Experimental design and baselines | 12 | Each hypothesis has an experiment that can falsify it, each mechanism has its own control, and the baselines include the strongest simple explanation. Budgets are matched. |
| 6 | Data fidelity and leakage control | 8 | Every pipeline step says what shape and structure it preserves, how units are split before any derived data are made, and why no test information reaches training. |
| 7 | Statistical inference and falsifiability | 8 | The unit of analysis is the independent unit, the primary endpoint is fixed in advance, uncertainty covers both data and training seeds, and multiplicity is handled. |
| 8 | Feasibility and timeline | 7 | The plan fits the calendar and compute, with gates that drop optional work before core work. |
| 9 | Clarity and first-principles accessibility | 10 | A reader with undergraduate mathematics can follow every concept, each term is explained when it first appears, and the prose reads naturally. |
| 10 | Narrative arc and persuasiveness | 5 | The proposal reads as a line of inquiry where each result decides the next question, and the reader finishes it wanting to know the answer. |

## Calibration anchors

- **90+**: ready to execute and, if the main experiments come out as designed, likely to be competitive at ICML.
- **80–89**: strong plan with one or two weaknesses a reviewer would raise.
- **70–79**: solid idea; design or positioning gaps would draw a weak-reject from at least one reviewer.
- **60–69**: interesting direction with a contribution that is not yet clear or experiments that cannot yet separate explanations.
- **below 60**: important problems with question, scope, or soundness.

These scores grade the quality of a research plan. No experiment in this folder has been run, so none of the scores predicts model performance or acceptance.

## How scores move between versions

A dimension rises only when the new version fixes a specific critique from the previous review, and the review says which one. A dimension can fall when a new addition introduces a problem (for example, a proposition stated without its assumptions). Each review also records the findings from an independent Codex adversarial review and how the next version handles each one.
