# Data fidelity and leakage contract

This contract states what “preserving the dataset’s shape” means operationally. It distinguishes immutable measurements, physically faithful derived views, and the compressed learned state. A learned representation is intentionally smaller than the input; its invertibility is not assumed. The final proposal supplies the concrete cart dimensions and timing; a later skeleton study must declare its own joint schema.

| Stage | Data structure and physical meaning preserved | Allowed transformation | Leakage or distortion check |
|---|---|---|---|
| Acquire or simulate | Original time axis, units, channel meanings, side labels, complete episode boundaries | Write an immutable record plus metadata | Hash the record; record simulator/pose-extractor version and provenance; exclude paths and IDs from model features |
| Assign families | Every physical body or person and all dependent descendants | Partition family IDs before creating model windows | Disjoint ID sets; mirrored copies, cloned states, noise replicas, recordings from the same person, and reused source videos stay together |
| Define evaluation support | Intended population of mechanics and input schedules | Reserve complete parameter cells or waveform families | Verify both training and validation exclude held-out support; distinguish independent interpolation from extrapolation |
| Derive measured channels | Anatomical order and a named coordinate frame | A documented physical coordinate transform | Transform positions, forces, commands, and uncertainty consistently; no side canonicalization or per-side amplitude normalization |
| Filter and normalize | Information available at the prediction origin | Fixed engineering scales or statistics fitted on training observations; causal filters | Future samples, future heel strikes, full-sequence medians, or test-cohort statistics cannot determine a forecast input |
| Form windows | Sampling interval, event timing, reset discontinuities, channels | Slice contiguous history; pad short sequences with explicit masks | No time stretching, artificial joins, interpolation across reset boundaries, or cross-split overlap |
| Mask or corrupt | One slot for every original time/channel index | Mark unavailable observations; create separately tracked noise views | Masks travel with values and follow the same split; corrupt labels are not silently treated as valid physical reflections |
| Generate branches | Complete state and context at one origin | Clone physical, actuator, controller, and random state; vary only declared input | Identical-input replay agrees before a branch comparison is admitted; future branch targets never enter encoded history |
| Train memory | Chronological input contract and fixed storage budget | Compress history into changing state and persistent context | No simulator parameters, sign labels, response-derived metadata, or query outcomes supplied only to the candidate |
| Roll out a query | Declared future schedule, output time grid, physical units | Predict a complete physical trajectory; integrate its force for impulse | Keep persistent sample fixed; no teacher-forced target observations during the scored forecast; no extra inference from imagined samples |
| Fit diagnostic readouts | Frozen model state plus the same query available to its decoder | Fit readout on training, select capacity/regularization on validation | Locked-test labels score the readout only; state, current observation, and query access are identical across readout comparisons |
| Evaluate and aggregate | Full preregistered eligibility denominator and family structure | Average conditions within families, then compare paired family means | No frame-level pseudoreplication; log numerical failures; report seed dependence and all prespecified outcomes |

## Three transformations that require different claims

**A physical reflection** transforms the whole experiment, including mechanics and inputs. Its purpose is to test an equivariance law. A mirrored descendant remains part of the original statistical family.

**An observation naming error** corrupts which measured channel is called left or right while the physical body and ground truth remain fixed. Its purpose is to test robustness to labeling error. It is not an admissible symmetry transformation of the complete experiment.

**A mechanical intervention** changes a body parameter or applies a specified physical input. It can change the dynamics and the response. Matched simulator branches can support a controlled comparison when the initial state and disturbance coupling are declared. An edited pose window or a synthetic reflection alone does not constitute observed evidence for a new body's causal response.

## Human-data extension boundary

The supplied URTC pipeline resizes sequences and uses completed-window processing. Those operations must be redesigned before prospective forecasting. Source-video overlap also prevents its existing results from establishing independent-video generalization. The JEPA restoration study has person-disjoint fitting, but repeated use of its development people does not replace an untouched confirmation set. These are findings about the supplied documents, not newly reproduced experiments; see the [source evidence audit](source-evidence-audit.md).

A candidate human archive should enter only after a small ingestion audit verifies participant identity, chronology, simultaneous bilateral channels, units, sensor calibration, and which controls were available at each forecast origin. For example, the [Baček et al. dataset paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11189391/) describes a left-knee constraint protocol. It can motivate a condition-generalization study, but it does not provide matched left/right weakness interventions or calibrated strength labels. Its full archive was not acquired in this task. A human test would receive its own protocol and would not inherit the simulator's identification guarantee.

## Release requirements

Publish generator settings and version, split IDs, preprocessing parameters, seed lists, target construction, reflection maps, training budgets, and all declared failures. Release measured outcomes and model predictions at the independent-family level so effect estimates can be recomputed without treating correlated frames as new observations. Freeze the manifest and analysis specification before opening the locked test; if a design changes afterward, record the old test as development evidence and obtain fresh confirmation data.
