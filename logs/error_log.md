# VecDB Benchmark Error Log

## [ERR-001] Pinecone API rate limiting during bulk insert
**Date:** 2024-03-12 | **Severity:** Medium | **Status:** Resolved

**Description:** Bulk insert of 1M vectors hit Pinecone's 100 req/s rate limit at batch_size=100.
**Fix:** Added token bucket rate limiter capping at 80 req/s + exponential backoff.
**Impact:** Full 1M vector insert completes in 42 min with zero rate limit errors.

---

## [ERR-002] Weaviate HNSW index corrupted after container restart
**Date:** 2024-04-03 | **Severity:** High | **Status:** Resolved

**Description:** After abrupt container stop, Weaviate HNSW index returned wrong recall@10 = 0.21 (expected 0.97).
**Root Cause:** WAL not flushed before container stop caused partial index write.
**Fix:** Set `persistence_data_path` volume + `ENABLE_MODULES=text2vec-openai` with graceful shutdown hook.
**Impact:** Index survives restarts correctly. Added benchmark checkpoint validation.
