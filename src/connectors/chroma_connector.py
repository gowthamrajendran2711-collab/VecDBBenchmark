"""Chroma connector for VecDB Benchmark"""
import time, uuid
import numpy as np
import chromadb

class ChromaConnector:
    NAME = "chroma"

    def __init__(self, host: str = "localhost", port: int = 8000, collection: str = "benchmark"):
        self.client = chromadb.HttpClient(host=host, port=port)
        self.collection_name = collection
        self.collection = None

    def setup(self, dim: int):
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def bulk_insert(self, vectors: np.ndarray, batch_size: int = 500) -> float:
        start = time.time()
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i+batch_size]
            ids = [str(uuid.uuid4()) for _ in batch]
            self.collection.add(ids=ids, embeddings=batch.tolist())
        return time.time() - start

    def query(self, vector: np.ndarray, top_k: int = 10) -> list:
        return self.collection.query(query_embeddings=[vector.tolist()], n_results=top_k)

    def teardown(self):
        self.client.delete_collection(self.collection_name)
