# The model in plain terms

## What is simulated

Ten brain regions, wired along the routes tau spreads in people:

| Region | Why it is included |
|---|---|
| Entorhinal cortex | First region with tangles; the gateway to the hippocampus |
| Hippocampus (CA1/subiculum) | Forming new memories; heavy early neuron loss |
| Parahippocampal cortex / amygdala | Early tangles; TDP-43 co-pathology |
| Inferior temporal / fusiform | Where tau-PET positivity usually begins (Braak III–IV) |
| Lateral temporal | Language and semantic memory |
| Posterior cingulate / precuneus | Hub with the earliest drop in glucose use (FDG) |
| Inferior parietal | Attention, spatial skills |
| Prefrontal | Planning, executive function |
| Occipital association | Visual processing; late |
| Primary sensory/motor | Spared until late |

For every virtual person and region the model tracks four quantities:

1. **Amyloid** (Centiloid, one value per person: plaque is spread across the cortex)
2. **Tau tangles** (0 = none, 1 = maximal)
3. **Neurons alive** (fraction; loss is permanent)
4. **Function of the surviving neurons** (synapses and activity; can recover in principle when what is harming them is removed)

## How the disease moves

- Amyloid rises slowly over decades toward a person-specific ceiling.
- Tau grows in the medial temporal lobe with age, faster once amyloid passes a threshold (a "permission" switch around 35–65 Centiloid), and spreads along connections. Once established it propagates largely on its own. People differ in how fast each of these happens.
- Tangles kill neurons, most in the vulnerable medial temporal regions. TDP-43 co-pathology (LATE) adds medial temporal loss in about a quarter of people in their 70s and 80s.
- Surviving neurons work less well when tau sits in them, when soluble amyloid is high, and when their inputs from dead neurons upstream are gone. Their function falls quickly and recovers slowly when an insult is removed; the recovery speed is not known and is carried as two ensemble members (slow and moderate).
- Older brains progress faster (rates double every ~15 years of age; an assumption).

## From brain to symptoms

Cognition (the CDR sum of boxes, 0–18) is computed from the network's total function: each region contributes in proportion to how much everyday cognition depends on it, a reserve threshold absorbs early damage, and people differ in resilience. A separate, fully reversible non-Alzheimer part (sleep, medication, mood, hearing) is present in some people. This mapping is the least constrained part of the model and is carried as ensemble variants (linear vs convex; more vs less dependence on memory circuits).

## Treatments

| Class | How it acts in the model | Status |
|---|---|---|
| Antibody, finite course (donanemab-like) | Clears amyloid at person-specific rates fitted to trial PET data; stops when plaque falls below ~11 Centiloid at a 6/12/18-month scan | Approved |
| Antibody, continuous (lecanemab-like) | Slower clearance, never stopped | Approved |
| Tau blocker (half or all) | Reduces new tangle formation and spread; existing tangles still harm | Hypothetical (trials ongoing) |
| Neuroprotection | Stops further neuron death | Hypothetical |
| Local repair | Removes the harm tau and amyloid do to surviving neurons; recovery at the calibrated pace or a faster hypothetical pace | Hypothetical |
| Ceiling | Every surviving neuron restored to full function, including rewiring | Theoretical upper bound |
| Non-Alzheimer fixes | Removes the reversible non-Alzheimer part | Available (sleep, medication review, mood, hearing) |

No neuron replacement is modeled: lost neurons, and what they encoded, are treated as permanent.

**No side effects are modeled.** There is no ARIA (amyloid-related imaging abnormalities: brain swelling or microbleeds) module, and APOE genotype has no effect anywhere in the simulation. Treatment scenarios therefore show modeled benefit only, never benefit against harm.

## What it is calibrated to and how it is tested

See `CALIBRATION.md` (28 targets: 22 with a cited published source, 4 derived or extrapolated from published figures and marked as such, and 2 without a specific citation; fit by ensemble member) and `VALIDATION.md` (checks against long-term data the model never saw). The independent vetting record is `research/reproductions/open-ad-sim/README.md` at the repository root.

## What it cannot do

- Simulate any individual's brain, or predict any individual's course.
- Tell which mechanism is true when several fit the data equally well — that is why results are ranges across an ensemble.
- Say anything reliable about therapies that do not exist, beyond "this is the most such a therapy could do under these assumptions".
