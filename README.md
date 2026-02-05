# Cache POC – Cache-Aside vs Write-Through

This repository contains **two independent Proof of Concepts (POCs)** demonstrating commonly used caching strategies using **FastAPI, Redis, and PostgreSQL**.

The goal of this project is to:
- Understand how different caching strategies behave at runtime
- Observe cache hits, cache misses, and consistency trade-offs
- Gain hands-on experience with real-world cache patterns

---

## Folder Structure
```
cache-poc/
┣ cache-aside-poc/
┃ ┗ app.py
┗ write-through-poc/
┃  ┗ app.py
┣ test_cache_stampede.py
┗ users.json
```
Each folder is a **self-contained FastAPI application** implementing a specific caching strategy.
`test_cache_stampede.py` can be used to test the cache hit or miss. Run it as `python test_cache_stampede.py`. This program checks for records, updates it if found, inserts it if not. It uses the `users.json` file for mock users.
The records in `users.json` is generated with the help of Mockaroo.

The cache behviour could be tested using the library `hey`.

Either using `hey` or `test_cache_stampede.py` the fetch, update or insert mechanism and timings change based on the type of cache you are testing, even though they might look the same on the surface going by the logs on terminal.

---

## Prerequisites

### Software
- Python **3.10+**
- Redis (running locally)
- PostgreSQL (running locally)

### Python dependencies
Install once (recommended in a virtual environment):

```bash
pip install fastapi uvicorn redis psycopg2-binary
```
---

## Example Database Schema
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO users (name, email)
VALUES
('Alice', 'alice@test.com'),
('Bob', 'bob@test.com');
```

---

## How to Run
```bash
cd cache-aside-poc
uvicorn app:app --reload
```
(or)

```bash
cd write-through-poc
uvicorn app:app --reload
```

## Example Requests
### Read user
```bash
curl http://localhost:8000/users/1
```

### Update user (cache invalidated)
```bash
curl -X PUT "http://localhost:8000/users/1?name=Charlie"
```

---

## Redis Utilities (Optional but Recommended)
### Check keys
```bash
redis-cli KEYS "*"
```
### Inspect cached value
```bash
redis-cli GET user:1
```
### Check TTL
```bash
redis-cli TTL user:1
```
### Flush cache
```bash
redis-cli FLUSHALL
```

---

## Load Testing (Optional)
### Using hey
```bash
hey -n 1000 -c 100 http://localhost:8000/users/1
```
This helps observe:
- Cache hit ratio
- Latency differences
- Cache stampede behavior

---

## Eviction Policy
Since both the cache POCs use Redis as their cache, the eviction policy is managed by Redis by it's built-in eviction policy.
### Eviction Policies in Redis
| Policy           | Description                     |
| ---------------- | ------------------------------- |
| `allkeys-lru`    | Evict least recently used key   |
| `allkeys-lfu`    | Evict least frequently used key |
| `allkeys-random` | Random eviction                 |
| `volatile-lru`   | LRU but only keys with TTL      |
| `noeviction`     | Writes fail when full           |

### Check the Redis currect eviction policy
```bash
redis-cli CONFIG GET maxmemory-policy
```

### Change the Redis eviction policy
```bash
redis-server --maxmemory <MEMORY_SIZE | 5mb, 50mb, etc.> --maxmemory-policy <EVICTION_POLICY>
```

### Checking the Redis stats
```bash
redis-cli INFO stats
```
