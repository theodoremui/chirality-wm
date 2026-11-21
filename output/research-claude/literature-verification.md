# Literature verification

Checked on 23 October 2026. Each entry was confirmed against its arXiv record or a conference page, or (for well-established papers) against the publication record I already know. The "use in the proposal" column says what each source is allowed to support. Recent 2026 preprints that the Codex literature audit had already verified ([output/research-codex/literature-audit.md](../research-codex/literature-audit.md)) are marked "Codex audit".

## Sources added in the Claude revisions

| Source | How verified | Use in the proposal |
|---|---|---|
| Littwin, Saremi, Advani, Thilak, Nakkiran, Huang, Susskind. *How JEPA Avoids Noisy Features: The Implicit Bias of Deep Linear Self Distillation Networks.* NeurIPS 2024. [arXiv:2407.03475](https://arxiv.org/abs/2407.03475) | arXiv abstract; NeurIPS 2024 poster page | In deep linear networks, JEPA-style training favors features with large regression coefficients and reconstruction favors high-variance features. Grounds the JEPA-versus-reconstruction prediction (M2). Only deep linear theory, so it predicts and does not prove behavior in nonlinear world models |
| Lawrence, Portilheiro, Zhang, Kaba. *Improving Equivariant Networks with Probabilistic Symmetry Breaking.* ICLR 2025. [arXiv:2503.21985](https://arxiv.org/abs/2503.21985) | arXiv abstract; ICLR 2025 poster page | Equivariant networks cannot break input symmetry; equivariant conditional distributions (SymPE) can. Grounds M1 and the stochastic two-component belief |
| Kaba, Ravanbakhsh. *Symmetry Breaking and Equivariant Neural Networks.* [arXiv:2312.09016](https://arxiv.org/abs/2312.09016) (2023; workshop version) | arXiv abstract | Equivariant functions cannot break symmetry at the level of a single sample; relaxed equivariance. Grounds M1 |
| Smidt, Geiger, Miller. *Finding Symmetry Breaking Order Parameters with Euclidean Neural Networks.* Phys. Rev. Research 3, 012002 (2021). [arXiv:2007.02005](https://arxiv.org/abs/2007.02005) | arXiv record with journal reference | Curie's principle for equivariant networks. Grounds M1 |
| Wang, Walters, Yu. *Approximately Equivariant Networks for Imperfectly Symmetric Dynamics.* ICML 2022. [arXiv:2201.11969](https://arxiv.org/abs/2201.11969) | arXiv abstract | Relaxed equivariance for dynamics that depart from symmetry. Baseline family |
| Wang, Hofgard, Gao, Walters, Smidt. *Discovering Symmetry Breaking in Physical Systems with Relaxed Group Convolution.* ICML 2024. [arXiv:2310.02299](https://arxiv.org/abs/2310.02299) | arXiv abstract | Relaxed weights reveal where symmetry breaks. Related work and a possible baseline |
| Lawrence, Hofgard, Portilheiro, Chen, Smidt, Walters. *To Augment or Not to Augment? Diagnosing Distributional Symmetry Breaking.* ICLR 2026. [arXiv:2510.01349](https://arxiv.org/abs/2510.01349) | arXiv record stating ICLR 2026 | When the data distribution is not mirror-symmetric, augmentation and equivariance can hurt. Grounds the population-imbalance condition |
| Ordoñez-Apraez et al. *Morphological Symmetries in Robotics.* IJRR (2025). [arXiv:2402.15552](https://arxiv.org/abs/2402.15552) | arXiv record with journal reference | Morphological symmetry is widely exploited in robot learning. Motivation |
| Wang, H. *Certified World Models: Predictability Across Configuration, Horizon, and Resolution.* [arXiv:2606.13092](https://arxiv.org/abs/2606.13092) (2026 preprint) | arXiv abstract | Guarantees for equivariant world models degrade with the size of the symmetry break in the dynamics. Related work only |
| Xu, Zhao, Song, Stewart, Ermon. *A Theory of Usable Information under Computational Constraints.* ICLR 2020. [arXiv:2002.10689](https://arxiv.org/abs/2002.10689) | arXiv record stating ICLR 2020 | Defines information relative to a class of readouts. Grounds the interpretation of frozen-state readouts |
| Lee, Seo, Lee, Lee, Shin. *Context-aware Dynamics Model for Generalization in Model-Based RL.* ICML 2020. [arXiv:2005.06800](https://arxiv.org/abs/2005.06800) | arXiv record stating ICML 2020 | Context-inference baseline family |
| Kirchmeyer et al. *Generalizing to New Physical Systems via Context-Informed Dynamics Model (CoDA).* ICML 2022. [arXiv:2202.01889](https://arxiv.org/abs/2202.01889) | arXiv record stating ICML 2022 | Context-inference baseline family |
| Zhou, Pan, LeCun, Pinto. *DINO-WM.* [arXiv:2411.04983](https://arxiv.org/abs/2411.04983) | arXiv abstract | Latent-feature world models used for planning. Related work |
| Balestriero, LeCun. *LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics.* [arXiv:2511.08544](https://arxiv.org/abs/2511.08544) (2025) | arXiv abstract | SIGReg pushes embeddings toward an isotropic Gaussian. Candidate anti-collapse regularizer for the JEPA arm |
| Saxe, McClelland, Ganguli. *Exact Solutions to the Nonlinear Dynamics of Learning in Deep Linear Neural Networks.* ICLR 2014. arXiv:1312.6120 | Known publication record | Strong directions are learned first. Grounds the training-dynamics part of M2 |
| Izenman. *Reduced-Rank Regression for the Multivariate Linear Model.* J. Multivariate Analysis 5(2), 1975 | Known publication record | Optimal rank-limited linear prediction. Grounds M2 |
| Bengio, Simard, Frasconi. *Learning Long-Term Dependencies with Gradient Descent Is Difficult.* IEEE TNN 5(2), 1994 | Known publication record | Vanishing gradients across long delays. Grounds M3 |
| Hewitt, Liang. *Designing and Interpreting Probes with Control Tasks.* EMNLP 2019. arXiv:1909.03368 | Known publication record | Readout controls |
| Gneiting, Raftery. *Strictly Proper Scoring Rules, Prediction, and Estimation.* JASA 102(477), 2007 | Codex audit | CRPS and energy score |

## Sources carried over from the original proposal

| Source | How verified | Use |
|---|---|---|
| Yeh, Hu, Schwing. *Chirality Nets for Human Pose Regression.* NeurIPS 2019. arXiv:1911.00029 | Codex audit | Reflection-equivariant recurrent layers |
| Lan et al. *SWAP: Symmetric Equivariant World-Model for Agile Robot Parkour.* arXiv:2606.19928 (2026) | Codex audit; also returned by a fresh search | Equivariant recurrent world model; baseline family |
| Lillemark et al. *Flow Equivariant World Models.* ICML 2026. arXiv:2601.01075 | Codex audit; fresh search | Equivariant memory for partially observed scenes |
| Sandilya, Liston, Grosenick. *Identifiable World Models from Pretrained Diffusion Representations.* arXiv:2610.07028 (2026) | Codex audit | Related work on intervention-relevant representations |
| Chen, Liu. *Compact but Moving.* arXiv:2609.21787 (2026) | Codex audit | Representations can keep information in moving directions; motivates delay-specific readouts |
| Assran et al. *I-JEPA.* CVPR 2023; *V-JEPA 2.* arXiv:2506.09985 | Codex audit | JEPA family and action-conditioned JEPA |
| Kumar et al. *RMA.* RSS 2021; Zintgraf et al. *VariBAD.* ICLR 2020 | Codex audit | Context-inference baselines |
| Hafner et al. *PlaNet* (ICML 2019); *DreamerV3* (arXiv:2301.04104) | Known publication record | Reconstruction world-model baseline |

## Claims deliberately not made

- No source shows that JEPA or equivariance erased asymmetry in a world model. The user's JEPA manuscript shows a zero-change baseline beating sixteen trained variants on asymmetry-change error, under a failure-cost rule that inflates errors; it is cited as an observation that motivates a hypothesis.
- The 2026 Chemistry Nobel framing in the original proposal is dropped as irrelevant to the learning question, not because it is false.
- A fresh search found no paper that treats retention of a hidden signed body parameter in world models as its subject. Absence from a search does not establish novelty, and the proposals say so.
