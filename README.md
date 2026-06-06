# 🗄️ VecDB Benchmark

> Scientific benchmark suite comparing Qdrant, Pinecone, Weaviate, Chroma at scale.

![Python](https://img.shields.io/badge/Python-3.11-blue) ![Qdrant](https://img.shields.io/badge/Qdrant-1.9-orange) ![Locust](https://img.shields.io/badge/Locust-2.29-green)

---

## Overview

VecDB Benchmark is a rigorous, reproducible benchmarking suite for vector databases. It tests indexing throughput, query latency, recall accuracy, and cost across Qdrant, Pinecone, Weaviate, and Chroma at dataset sizes from 100k to 100M vectors.

## Benchmark Results (1M vectors, dim=1536)

| Database | Insert/s | P99 Query (ms) | Recall@10 | Cost/mo ($) |
|----------|----------|----------------|-----------|-------------|
| **Qdrant** | **8,200** | **12** | **0.987** | **$89** |
| Pinecone | 3,100 | 18 | 0.981 | $210 |
| Weaviate | 4,800 | 21 | 0.974 | $145 |
| Chroma | 1,200 | 45 | 0.961 | $60* |

*Chroma self-hosted on equivalent hardware

## Metrics & Achievements

- Tested at scales: 100k, 1M, 10M, 50M vectors
- Reproducible with Docker Compose for all databases
- Locust-based load testing with realistic query distributions
- Automated cost estimation via cloud pricing APIs

## Quick Start

```bash
docker-compose up -d  # Starts all 4 databases

# Generate test dataset
python -m src.benchmarks.generate --num_vectors 1000000 --dim 1536

# Run benchmark
python -m src.benchmarks.run --databases all --num_vectors 1000000

# Results in metrics/benchmark_results.json
```

## License

MIT
