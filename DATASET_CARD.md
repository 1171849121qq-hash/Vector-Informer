# WATraj target-motion preview

Release date: September 11, 2026.

## Contents

This is a small, deterministic subset of real vehicle trajectories from the WATraj freeway-weaving dataset. It contains 64 windows from the archived validation input array, projected to the six target-vehicle motion fields. Numeric values are retained exactly, with no rounding, normalization, interpolation, or synthetic replacement.

| Array | Shape | Type | Meaning |
|---|---|---|---|
| `trajectories` | `(64, 80, 6)` | float64 | Target vehicle states, ordered by time |
| `maneuver_labels` | `(64, 1)` | float64 | Archived maneuver categories |
| `source_row_indices` | `(64,)` | int64 | Zero-based row indices in the archived validation input |

`watraj_preview.npz` contains only numeric arrays. Load it with `allow_pickle=False`. The full file checksum and field metadata are provided in `schema.json`.

## Fields and coordinates

The six feature columns preserve the original archive order:

| Index | Field | Unit |
|---|---|---|
| 0 | Target y center | m |
| 1 | Target x center | m |
| 2 | Target y velocity | m/s |
| 3 | Target x velocity | m/s |
| 4 | Target y acceleration | m/s² |
| 5 | Target x acceleration | m/s² |

Positions use the dataset's local coordinate system, not latitude/longitude. Use column 1 as the horizontal plot coordinate and column 0 as the vertical coordinate. The example keeps equal metric scales on both axes within each panel.

The stored sampling interval is 0.1 s (10 Hz): 30 history states followed by 50 future states. The archived model data interface selects every second state, giving 15 history and 25 future states at 5 Hz. Future values in this release are ground truth, not model predictions.

Maneuver labels follow the archived preprocessing: `0` = left lane change, `1` = lane keeping, `2` = right lane change. This preview contains 22, 19, and 23 windows respectively. These categories should not be interpreted as labels of merge/diverge behavior.

## Selection and provenance

The source validation array contains 7,338 windows of shape `(80, 44)`. This release selects 64 windows and only its first six target-motion columns:

```python
indices = np.sort(np.random.default_rng(20260911).choice(7338, size=64, replace=False))
preview = source_validation[indices, :, :6]
```

Selection uses NumPy's PCG64 generator. It is independent of prediction error and does not define a new official evaluation split. Source archive hashes, member names, and the complete selected index list are in `schema.json`.

The source archive calls this dataset `tianjin` (the implementation uses `TJ`). Its six original recording tables contain 98,630; 206,350; 256,682; 272,207; 275,853; and 385,439 vehicle states, totaling 1,495,161, consistent with the WATraj dataset description. The 64 windows here are only a small preview of these processed data; windows may overlap and should not be counted as 64 unique vehicles.

## Intended use and scope

Use this release to inspect real trajectories, understand the target-state format, and exercise a simple data loader or visualization. It does not contain neighbor motion, matched local-map inputs, raw images/video, model predictions, or pretrained weights. The target-only preview is insufficient for full Vector-Informer inference or reproduction of the paper's reported aggregate metrics.

No names, contact details, license plates, faces, vehicle IDs, absolute timestamps, or geographic coordinates are included. The numeric source row indices are for archive traceability.

## License and acknowledgment

The preview data are provided under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). Attribute the WATraj contributors, link to [this repository](https://github.com/1171849121qq-hash/Vector-Informer), and indicate any changes you make. The example code has the MIT License; see `LICENSE.md`.
