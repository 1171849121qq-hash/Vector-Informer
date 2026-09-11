"""Validate and visualize the WATraj target-motion preview (NumPy only).

Usage: python inspect_sample.py [--output preview.svg] [--sample 0]
SPDX-License-Identifier: MIT
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path

import numpy as np


def load_preview(path: Path, schema_path: Path):
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual_hash != schema["file_sha256"]:
        raise ValueError("Data SHA256 differs from schema.json")
    with np.load(path, allow_pickle=False) as archive:
        arrays = {key: archive[key] for key in archive.files}
    if set(arrays) != set(schema["arrays"]):
        raise ValueError("Unexpected array names")
    for name, expected in schema["arrays"].items():
        value = arrays[name]
        if list(value.shape) != expected["shape"] or str(value.dtype) != expected["dtype"]:
            raise ValueError(f"Unexpected shape or dtype: {name}")
        if not np.isfinite(value).all():
            raise ValueError(f"Non-finite values: {name}")
    ids = arrays["source_row_indices"]
    if ids.tolist() != schema["selection"]["source_row_indices"] or len(np.unique(ids)) != len(ids):
        raise ValueError("Source row identifiers do not match the manifest")
    labels = arrays["maneuver_labels"].astype(int).ravel()
    if not np.isin(labels, [0, 1, 2]).all():
        raise ValueError("Unexpected maneuver label")
    return arrays, schema


def write_svg(trajectories, labels, indices, output: Path):
    width, height, columns = 1000, 810, 4
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
             '<rect width="100%" height="100%" fill="#f5f7fb"/>',
             '<g font-family="Arial,sans-serif" fill="#18283d">',
             '<text x="28" y="36" font-size="22" font-weight="bold">WATraj | target-motion preview</text>',
             '<text x="28" y="60" font-size="13">Recorded positions: blue = history, orange = future ground truth. No predictions.</text>']
    names = {0: "left lane change", 1: "lane keeping", 2: "right lane change"}
    for panel, index in enumerate(indices):
        left = 20 + (panel % columns) * 245
        top = 82 + (panel // columns) * 235
        points = trajectories[index][:, [1, 0]]
        low, high = points.min(0), points.max(0)
        span = np.maximum(high - low, 1e-6)
        # Equal metric scale for both axes within each panel.
        scale = min(202 / span[0], 155 / span[1])
        center = (low + high) / 2
        xy = (points - center) * scale
        xy[:, 0] += left + 115
        xy[:, 1] = top + 123 - xy[:, 1]
        parts += [f'<rect x="{left}" y="{top}" width="232" height="222" rx="9" fill="white" stroke="#dce2ec"/>',
                  f'<text x="{left+12}" y="{top+21}" font-size="13">Sample {index:02d} · {html.escape(names[int(labels[index])])}</text>']
        for line, color in [(xy[:30], "#2879c4"), (xy[29:], "#e8842f")]:
            coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in line)
            parts.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="2.3"/>')
        parts.append(f'<text x="{left+12}" y="{top+210}" font-size="11" fill="#52647a">x span {span[0]:.1f} m · y span {span[1]:.1f} m</text>')
    parts.append('</g></svg>')
    output.write_text("\n".join(parts) + "\n", encoding="utf-8")


def main():
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=base / "watraj_preview.npz")
    parser.add_argument("--schema", type=Path, default=base / "schema.json")
    parser.add_argument("--output", type=Path, default=Path("preview.svg"))
    parser.add_argument("--sample", type=int, help="Plot a single zero-based preview sample (0-63)")
    args = parser.parse_args()
    arrays, schema = load_preview(args.data, args.schema)
    x = arrays["trajectories"]
    labels = arrays["maneuver_labels"].ravel()
    if args.sample is not None and not 0 <= args.sample < len(x):
        parser.error(f"--sample must be in 0..{len(x)-1}")
    selected = [args.sample] if args.sample is not None else list(range(min(12, len(x))))
    write_svg(x, labels, selected, args.output)
    print(json.dumps({"sha256_verified": True, "shape": list(x.shape),
                      "sample_count": len(x), "frequency_hz": schema["sampling"]["stored_frequency_hz"],
                      "label_counts": {str(i): int((labels == i).sum()) for i in range(3)},
                      "history_shape_5hz": list(x[:, ::2][:, :15].shape),
                      "future_shape_5hz": list(x[:, ::2][:, 15:].shape),
                      "plot": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
