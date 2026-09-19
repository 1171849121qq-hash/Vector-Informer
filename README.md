# Vector-Informer

Vector-Informer is a relation-first road-conditioning framework for long-horizon vehicle trajectory prediction in freeway weaving areas, developed alongside the WATraj dataset.

## WATraj interaction dataset preview — September 2026

The primary dataset preview contains **512 real processed trajectory windows**
with the target vehicle, six directional neighbor slots, lane-availability
flags and maneuver labels. Each window contains 80 states at 10 Hz: 3 seconds
of history followed by 5 seconds of future ground truth. The download is
approximately 2.1 MiB.

- [Download the 512-window interaction subset](watraj_interaction_subset_512.npz)
- [Subset data card](WATRAJ_SUBSET_CARD.md)
- [Machine-readable schema and checksum](watraj_subset_schema.json)
- [Integrity and structure check](verify_watraj_subset.py)

The subset is a deterministic, label-balanced sample from the archived
validation array and was not chosen using prediction error. It is a processed
partial release: raw recordings, matched vector maps and the remaining data
splits are still excluded.

### Lightweight target-only preview

The earlier **64-window target-motion preview** remains available as a smaller
example. It contains target positions, velocities and accelerations without
the six neighbor slots. All 64 rows are also included in the 512-window
interaction subset.

- [Download the 64-window target-only preview](watraj_preview.npz)
- [Target-only data card and field definitions](DATASET_CARD.md)
- [Target-only schema and SHA256](schema.json)
- [Data loading and visualization example](inspect_sample.py)
- [Preview of 12 released trajectories](preview.svg)

## Network-core source preview — September 2026

The archived Vector-Informer network core is now available for architecture inspection, together with CPU inference and coordinate-RMSE metric helpers.

- [Download the source archive](vector_informer_source_preview_20260918.zip)
- [Release contents and scope](SOURCE_RELEASE_20260918.md)
- [Source archive checksum and file manifest](SOURCE_RELEASE_MANIFEST_20260918.json)

The archive includes synthetic architecture checks and analytic metric tests. It does not include pretrained checkpoints or matched map inputs and is not a complete reproduction package. Upstream attribution and licenses are included; parts of the combined model have noncommercial license terms.

## Quick start

Download the repository, then run:

```bash
python -m pip install numpy
python verify_watraj_subset.py
```

The script verifies the 512-window file's checksum, array shapes, dtypes and
class counts. It uses NumPy and the Python standard library; a GPU is not
required.

```python
import numpy as np

with np.load("watraj_interaction_subset_512.npz", allow_pickle=False) as data:
    states = data["agent_states"]          # (512, 80, 7, 6)
    neighbor_valid = data["neighbor_valid"] # (512, 80, 6)
    labels = data["maneuver_labels"]       # (512,)

# Select every second frame for the 5 Hz trajectory format:
states_5hz = states[:, ::2, :]
history = states_5hz[:, :15, :, :]    # 15 history states
future = states_5hz[:, 15:, :, :]     # 25 future ground-truth states
```

Run `python inspect_sample.py` to verify and visualize the smaller 64-window
target-only preview.

## Release scope

The primary 512-window file includes the target vehicle, six directional
neighbor slots and lane-availability flags. The smaller 64-window file remains
as a compact target-only example. Both are processed subsets; paired vector
maps, the remaining data splits, the full training/evaluation pipeline and
pretrained checkpoints are being prepared for subsequent releases.

Updates will be published in this repository. Thank you for your interest and patience.

## License

The released data are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The original loading example is licensed under the MIT License. See [LICENSE.md](LICENSE.md). Please acknowledge the WATraj contributors and link to this repository when using the data.
