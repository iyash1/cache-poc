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
┗ app.py
```
Each folder is a **self-contained FastAPI application** implementing a specific caching strategy.

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