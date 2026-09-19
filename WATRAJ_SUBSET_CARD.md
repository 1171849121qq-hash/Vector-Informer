# WATraj interaction subset (512 windows)

Release date: September 19, 2026.

This release expands the earlier 64-window target-motion preview into a
deterministic, label-balanced subset of 512 real processed WATraj windows. It
contains the target vehicle, six directional neighbor slots, lane-availability
flags and maneuver labels. It is intended for inspecting the dataset's
interaction representation and building data-loading examples.

The 512 rows are 6.98% of the archived 7,338-window validation array. They are
not 6.98% of all raw WATraj vehicle states. All 64 rows in the first preview are
included in this expanded subset.

## Files

- `watraj_interaction_subset_512.npz`: compressed numeric data.
- `watraj_subset_schema.json`: shapes, field definitions, provenance,
  deterministic selection indices and SHA-256 checksum.
- `verify_watraj_subset.py`: dependency-light integrity and structure check.

Load the data with NumPy:

```python
import numpy as np

with np.load("watraj_interaction_subset_512.npz", allow_pickle=False) as data:
    states = data["agent_states"]          # (512, 80, 7, 6)
    valid = data["neighbor_valid"]         # (512, 80, 6)
    lane_flags = data["lane_availability"] # (512, 80, 2)
    labels = data["maneuver_labels"]       # (512,)
```

## Tensor layout

The 80 chronological states are stored at 10 Hz: 30 history states followed by
50 future ground-truth states. Selecting every second state gives the archived
model's 5 Hz view with 15 history and 25 future states.

The seven agent slots are:

1. target;
2. left-front neighbor;
3. left-rear neighbor;
4. same-lane front neighbor;
5. same-lane rear neighbor;
6. right-front neighbor;
7. right-rear neighbor.

For the target, the six features are `y`, `x`, `vy`, `vx`, `ay`,
`ax` in site-local metric coordinates. For a neighbor, the first two fields
are `delta_y` and `delta_x` relative to the target; the remaining four are
that neighbor's velocity and acceleration components.

Some directional slots have no observed vehicle. The archived preprocessing
encodes these with a second-position sentinel of +1000 or -1000 metres and
copies the target kinematics. Use the supplied `neighbor_valid` mask instead
of treating those placeholders as observations.

`lane_availability[..., 0]` and `lane_availability[..., 1]` indicate
whether a left or right adjacent lane is available. Maneuver labels use
`0 = left lane change`, `1 = lane keeping`, and
`2 = right lane change`. The released class counts are 171, 170 and 171.
These labels should not be interpreted as merge/diverge event labels.

## Selection and provenance

The subset was selected from the archived validation arrays with NumPy PCG64
seed 20260919, stratified by maneuver label. It was not selected using
prediction error, model confidence or qualitative appearance. Original
floating-point values are retained without normalization, interpolation,
rounding or synthetic replacement. The schema records source archive/member
hashes and every selected source row.

The data contain no names, contact details, faces, license plates, vehicle
identifiers, absolute timestamps, latitude/longitude or imagery. Coordinates
are site-local.

## Scope and limitations

This is a processed interaction subset rather than the complete WATraj release.
It excludes the rest of the training, validation and test windows, raw
recordings, matched vector-map inputs and model predictions. Windows may
overlap and should not be counted as 512 unique vehicles. The subset alone
cannot reproduce the paper's aggregate metrics.

The data are provided under
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
Please attribute the WATraj contributors, link to the Vector-Informer
repository and indicate changes.
