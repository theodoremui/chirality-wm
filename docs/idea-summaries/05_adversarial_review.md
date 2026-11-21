# What changed after independent review

*Internal research-design review, 19 November 2026.*

Four proposal authors, including the integrating author, produced first drafts after reviewing the literature. Three AI subagents then reviewed drafts they had not written. The attribution reviewer challenged memory and sequential design, the memory reviewer challenged tracking, and the tracking reviewer challenged attribution. The tracking reviewer also inspected the memory design and overview illustration and independently enumerated the sequential example. Reviewers read the drafts and inspected rendered figures at their intended column width. Authors revised the documents, then the reviewers checked the substantive fixes. These are proposal reviews. No conference reviewer evaluated this collection.

## Criteria and exemplars

- **ICLR.** We used the guide's questions about the particular problem, its grounding in the literature, evidence for the claims and value to the community. For each proposal the reviewer had to identify the experiment or counterexample most likely to change the central claim. [ICLR 2026 Reviewer Guide](https://iclr.cc/Conferences/2026/ReviewerGuide)
- **ICML.** Its instructions ask reviewers to assess soundness, presentation, significance and originality separately, and to state questions whose answers would change the assessment. We applied this distinction to the exact toy results. Correct algebra can make a benchmark valuable while leaving an architectural novelty claim unresolved. [ICML 2026 Reviewer Instructions](https://icml.cc/Conferences/2026/ReviewerInstructions)
- **NeurIPS.** The guidelines distinguish theory, general contributions, concept and feasibility, and negative results. We asked what a negative outcome would establish, which assumptions a theorem needs, and which comparisons would isolate a proposed learning advance. We evaluated feasibility against the stated H100 access and the cost of generating independent physical trajectories. [NeurIPS 2026 Reviewing Guidelines](https://neurips.cc/Conferences/2026/ReviewerGuidelines)

Three examples changed the studies. Locatello et al. combined a nonidentification construction with controlled evaluation across datasets, then tested whether the desired representations helped a downstream task. That ICML Best Paper prompted separate tests of what a body response can identify and what control decisions it improves. Oren et al., recognized by ICLR, used exchangeability of benchmark order to give a model-derived score evidential meaning. Their example prompted the explicit conditional null and reset protocol in Proposal 4. Agarwal et al.'s NeurIPS Outstanding Paper showed how few-run reinforcement learning comparisons can change when uncertainty is considered. Here the resampling units are bodies and training seeds, and each main comparison gets a defined physical endpoint. [Locatello et al., ICML 2019](https://proceedings.mlr.press/v97/locatello19a.html) · [ETH award record](https://ethz.ch/en/the-eth-zurich/portrait/latest-honours-and-prizes/2019/06/icml-best-paper-award-for-francesco-locatello.html) · [Oren et al., ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/file/46e624c244cff669223d488defd4e835-Paper-Conference.pdf) · [ICLR award announcement](https://blog.iclr.cc/2024/05/06/iclr-2024-outstanding-paper-awards/) · [Agarwal et al., NeurIPS 2021, award noted on p. 1](https://proceedings.neurips.cc/paper_files/paper/2021/file/f514cec81cb148559cf475e7426eed5e-Paper.pdf)

## 1. Can a useful witness justify spending a memory bit?

**Objection.** The decision gap between two histories is exact for a terminal merger. A finite-memory encoder must preserve the distinguishing signal through the whole sequence. Storing sign can evict phase and make decisions worse elsewhere. Generic refinement could also discover exactly the same pair. In the first draft the split rule and flowchart obscured both costs.

**Revision.** The one-bit example enumerates all 16 ways to encode two fair cues and gives an exact optimum as a function of how often each is requested. The split is now tentative. It requires free capacity, training on the complete prefix, and lower loss on separate development bodies. Unrestricted, mixed and mirrored nomination use the same candidate-scoring and execution budgets. A fixed unilateral rig challenges physically invalid mirror pairs. Simultaneous bounds cover the repeated nominations. At the proposed primary budget a candidate needs an observed gap above 0.0951 to certify a gap above 0.02. The second, higher-precision arm distinguishes an insensitive screen from an absence of useful witnesses.

**Remaining limitation.** Sampling possible hidden states conditional on one recorded history is tractable in the finite system. A walker will need a calibrated approximation and independent action trials. The research claim stands or falls on savings against tuned unrestricted refinement and a codec trained on the action loss. [Proposal 1](01_preserve_interventional_information.md)

## 2. Is the benefit in the filter or in its symmetry?

**Objection.** A correct switching filter already keeps both channel assignments. Comparing a joint filter with a tracker that commits early cannot establish an advantage from reflection sharing. The original side-accuracy calculation also left unclear how a correct guess translates to displacement error under a noisy query.

**Revision.** Cross tying versus separate dynamics with retaining versus committing to naming hypotheses. Give the main competitor both branches, matched computational work, and mechanisms to prevent extinction of particles for a persistent gain sign. The toy now yields a minimum squared error in displacement and the extra error caused by discarding the association. Both forecasts are scored against the same held-out physical outcomes. The delay figure labels the per-step switch probability and separates chance from the axis. Access to SwapPF's full Table 1 also allowed the review to distinguish its person-identification result from its symmetry proxy. [Aoyagi et al., Table 1](https://www.scitepress.org/Papers/2026/144493/144493.pdf)

**Remaining limitation.** Changing the side-specific dynamics or breaking the rig's reflection symmetry can invalidate sharing. An advantage only over early commitment supports a filtering conclusion. A narrow tie with the untied branching filter would leave the data-efficiency hypothesis unsupported. [Proposal 2](02_track_physical_side.md)

## 3. Does the instrument actually produce the claimed bias?

**Objection.** A fixed image offset cancels when displacement is calculated from two positions. The first example could not produce its proposed bias. A second issue concerned the rank argument. The diagonal setting pair can identify the neutral response in an additive model although the two nuisance effects are inseparable. With an unrestricted interaction, one extra cell still leaves the target ambiguous.

**Revision.** Side-dependent magnification produces the proposed bias on actual displacement. The readout derivation also determines which coefficients reverse under a global mirror. Both missing views can be rendered from the existing pair of opposite-load runs. They share motion noise. The diagrams show this pairing and distinguish an interaction term from the measured response. The study now crosses trial allocation with predictor type and includes a correlated optimal-design baseline. Calibration bodies and their neutral measurements are separate from sealed test-body neutral trials.

**Remaining limitation.** An unmodeled effect quadratic in load can remain constant over every reversed setting and still change the neutral response. A sensitivity bound learned on calibration bodies requires a transfer assumption. Neural sample savings and a physical interpretation of learned coordinates are separate claims. [Proposal 3](03_separate_body_and_apparatus.md)

## 4. Does faster evidence growth mean higher power by a deadline?

**Objection.** A one-step ranking reversal does not imply a better sequential experiment. The reviewer found that the greedy two-sided evidence rule can be matched by one fixed probe in the illustrative channel. Fixing the same anatomical stance before every trial also invalidates a reflection null. Active multi-source betting is a closer comparator than passive e-values.

**Revision.** Two independent implementations enumerated all finite histories by sufficient state and agreed on the six rows in the revised proposal. For twelve trials the policy designed for the deadline detects with probability 0.951. Greedy two-sided growth and fixed A both achieve 0.801 with a lower mean capped cost. This changes the proposed training objective and the question in the title. The comparison now includes nonmyopic information about null membership, a fitted controlled-sensing policy and an active betting baseline with appropriately charged pairs. The second figure explicitly labels next-trial log growth. The protocol holds the body fixed across a sequence and matches reset and controller state under reflection.

**Remaining limitation.** The table uses known channels. A learned model could lose to online source selection under misspecification. The null concerns the measured system, and causal attribution requires the apparatus and camera controls in Proposal 3. [Proposal 4](04_design_experiments_with_valid_evidence.md) · [Hsu and Shekhar, full paper](https://arxiv.org/abs/2512.22403)

## Verification boundary

The analytic memory, filtering and reversal examples were checked against finite enumeration or rank calculations. The sequential table was calculated separately from the learned studies. All nine vector figures were rendered, inspected and checked against their captions. The literature review established several concrete precedents and corrected publication records. The pilots, estimated gains, confirmatory sample sizes and neural training costs still require experiments on the stated hardware.

[Collection overview](00_master.md) · [Full source notes](06_sources.md)
