# app/data/

This directory contains cached and preprocessed data files used by the AI assistant.

Files in this directory are either:
- Preloaded mock data (for demo/testing purposes)
- Auto-generated during runtime (e.g., embeddings, checksums)

### Included Files

| File                     | Description                                                   |
|--------------------------|---------------------------------------------------------------|
| `orders.json`            | Sample enriched order records used for vector search          |
| `order_chunks.json`      | Flattened order fields prepared for LLM embedding             |
| `order_embeddings.npy`   | (Excluded) — runtime generated embeddings (not versioned)     |
| `order_checksum.txt`     | Hash to avoid redundant processing of unchanged orders        |
| `cached_trucks.json`     | Simulated live vehicle telemetry data (for offline testing)   |

> These files allow the assistant to work immediately without requiring a live database or API during local or demo runs.
