"""Qdrant connector for VecDB Benchmark"""
import time, uuid
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, SearchRequest

class QdrantConnector:
    NAME = "qdrant"

    def __init__(self, url: str = "http://localhost:6333", collection: str = "benchmark"):
        self.client = QdrantClient(url=url, timeout=300)
        self.collection = collection

    def setup(self, dim: int):
        self.client.recreate_collection(
            collection_name=self.collection,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
            timeout=300
        )

    def bulk_insert(self, vectors: np.ndarray, batch_size: int = 1000) -> float:
        start = time.time()
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i+batch_size]
            points = [PointStruct(id=str(uuid.uuid4()), vector=v.tolist()) for v in batch]
            self.client.upsert(self.collection, points=points)
        return time.time() - start

    def query(self, vector: np.ndarray, top_k: int = 10) -> list:
        return self.client.search(self.collection, vector.tolist(), limit=top_k)

    def teardown(self):
        self.client.delete_collection(self.collection)
