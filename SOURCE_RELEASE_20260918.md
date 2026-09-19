# Network-core source preview — September 2026

This source preview contains the archived Vector-Informer network core and small inference/metric helpers. [Download the source archive](vector_informer_source_preview_20260918.zip), extract it, then follow its `README.md`.

Included: the compact history encoder, GraphSAGE vehicle/road fusion, temporal attention encoder and decoder, social pooling, archived model configuration, a CPU inference helper, synthetic smoke check, and coordinate-RMSE metric calculator with analytic tests.

This is a source preview for architecture inspection. It does not include trained weights, additional real trajectories, matched maps, or the full training/preprocessing pipeline. The earlier six-feature target-motion data preview is not sufficient input for the complete network. This release does not claim to reproduce all paper metrics.

The code retains upstream Informer, SocialGAN and CRAT-Pred attribution and licenses. The combined model includes noncommercially licensed components; see the included license notices.

The accompanying `SOURCE_RELEASE_MANIFEST_20260918.json` records the archive checksum and package contents.
