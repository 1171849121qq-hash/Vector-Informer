#!/usr/bin/env python3
"""Verify the WATraj 512-window interaction subset."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
DATA = HERE / "watraj_interaction_subset_512.npz"
SCHEMA = HERE / "watraj_subset_schema.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    actual_hash = sha256_file(DATA)
    assert actual_hash == schema["file"]["sha256"], "dataset checksum mismatch"

    with np.load(DATA, allow_pickle=False) as data:
        expected = {
            "agent_states": ((512, 80, 7, 6), np.dtype("float64")),
            "lane_availability": ((512, 80, 2), np.dtype("int8")),
            "neighbor_valid": ((512, 80, 6), np.dtype("bool")),
            "maneuver_labels": ((512,), np.dtype("int8")),
            "source_row_indices": ((512,), np.dtype("int64")),
        }
        assert set(data.files) == set(expected)
        for name, (shape, dtype) in expected.items():
            assert data[name].shape == shape, f"{name}: unexpected shape"
            assert data[name].dtype == dtype, f"{name}: unexpected dtype"
        assert np.isfinite(data["agent_states"]).all()
        assert set(np.unique(data["lane_availability"])) <= {0, 1}
        assert np.array_equal(
            np.bincount(data["maneuver_labels"], minlength=3),
            np.array([171, 170, 171]),
        )
        assert np.all(np.diff(data["source_row_indices"]) > 0)

    print("WATraj subset verified")
    print(f"SHA-256: {actual_hash}")
    print("Samples: 512; class counts: [171, 170, 171]")


if __name__ == "__main__":
    main()
