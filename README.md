# Vector-Informer

Vector-Informer is a relation-first road-conditioning framework for long-horizon vehicle trajectory prediction in freeway weaving areas, developed alongside the WATraj dataset.

## Initial data release — September 11, 2026

A small **WATraj target-motion preview** is now available: **64 real trajectory windows**, each containing 80 recorded states at 10 Hz. The download is approximately **211 KiB** and includes target positions, velocities, accelerations, maneuver labels, and source row indices.

- [Download the data](watraj_preview.npz)
- [Dataset card and field definitions](DATASET_CARD.md)
- [Machine-readable schema and SHA256](schema.json)
- [Data loading and visualization example](inspect_sample.py)
- [Preview of 12 released trajectories](preview.svg)

## Quick start

Download the repository, then run:

```bash
python -m pip install numpy
python inspect_sample.py
```

The script verifies the data checksum and schema, prints a summary, and writes `preview.svg`. It uses NumPy and the Python standard library; a GPU is not required.

```python
import numpy as np

with np.load("watraj_preview.npz", allow_pickle=False) as data:
    states = data["trajectories"]       # (64, 80, 6), original recorded values
    labels = data["maneuver_labels"]   # (64, 1)
    rows = data["source_row_indices"]  # (64,)

# Original feature order: y, x, vy, vx, ay, ax.
# Select every second frame for the 5 Hz trajectory format:
states_5hz = states[:, ::2, :]
history = states_5hz[:, :15, :]        # 15 history states
future = states_5hz[:, 15:, :]         # 25 future ground-truth states
```

## Release scope

This initial release provides a compact subset for inspecting the trajectory format and using the loading example. The 64 windows were selected using a fixed random seed, without filtering by model prediction error.

It contains target-vehicle motion only. Neighbor features, paired local maps, the full training/evaluation pipeline, and pretrained checkpoints are being prepared for subsequent releases. This preview is not an official benchmark split and does not reproduce the paper's aggregate metrics.

Updates will be published in this repository. Thank you for your interest and patience.

## License

The released data are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The original loading example is licensed under the MIT License. See [LICENSE.md](LICENSE.md). Please acknowledge the WATraj contributors and link to this repository when using the data.
