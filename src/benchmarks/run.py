"""VecDB Benchmark runner"""
import argparse, json, time
from pathlib import Path
import numpy as np

def generate_vectors(num_vectors: int, dim: int = 1536) -> np.ndarray:
    """Generate random unit-normalized vectors."""
    vecs = np.random.randn(num_vectors, dim).astype(np.float32)
    return vecs / np.linalg.norm(vecs, axis=1, keepdims=True)

def benchmark_database(db_name: str, vectors: np.ndarray, queries: np.ndarray) -> dict:
    """Run insert + query benchmark for a single database."""
    results = {}

    # Insert benchmark
    start = time.time()
    insert_count = _bulk_insert(db_name, vectors)
    insert_time = time.time() - start
    results["insert_throughput_per_sec"] = insert_count / insert_time

    # Query benchmark
    latencies = []
    for q in queries[:100]:
        t = time.time()
        _query(db_name, q, top_k=10)
        latencies.append((time.time() - t) * 1000)
    latencies.sort()
    results["p50_query_ms"] = latencies[50]
    results["p95_query_ms"] = latencies[95]
    results["p99_query_ms"] = latencies[99]

    return results

def _bulk_insert(db: str, vectors: np.ndarray) -> int:
    """Placeholder for database-specific insert."""
    return len(vectors)

def _query(db: str, query: np.ndarray, top_k: int) -> list:
    """Placeholder for database-specific query."""
    return []

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--databases", nargs="+", default=["qdrant", "pinecone", "weaviate", "chroma"])
    parser.add_argument("--num_vectors", type=int, default=1_000_000)
    parser.add_argument("--dim", type=int, default=1536)
    parser.add_argument("--output", default="metrics/benchmark_results.json")
    args = parser.parse_args()

    vectors = generate_vectors(args.num_vectors, args.dim)
    queries = generate_vectors(200, args.dim)

    results = {}
    for db in args.databases:
        print(f"Benchmarking {db}...")
        results[db] = benchmark_database(db, vectors, queries)

    Path(args.output).parent.mkdir(exist_ok=True)
    with open(args.output, "w") as f:
        json.dump({"num_vectors": args.num_vectors, "dim": args.dim, "results": results}, f, indent=2)
    print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main()
