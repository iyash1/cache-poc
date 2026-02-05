from fastapi import FastAPI
import psycopg2, redis, json

app = FastAPI()
r = redis.Redis(host="localhost", port=6379, decode_responses=True) 

# Database connection setup (using psycopg2)
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="admin"
)

@app.get("/users/{user_id}")
def get_user(user_id: int):
    cache_key = f"user:{user_id}"

    # 1. Try cache
    cached_user = r.get(cache_key)
    if cached_user:
        print("CACHE HIT")
        return json.loads(cached_user)

    print("CACHE MISS")

    # 2. Fetch from DB
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, name, email FROM users WHERE id = %s",
            (user_id,)
        )
        row = cur.fetchone()

    if not row:
        return {"error": "User not found"}

    user = {"id": row[0], "name": row[1], "email": row[2]}

    # 3. Store in cache (TTL = 60s)
    r.setex(cache_key, 60, json.dumps(user))

    return user

@app.put("/users/{user_id}")
def update_user(user_id: int, name: str):
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE users SET name = %s, updated_at = NOW() WHERE id = %s",
            (name, user_id)
        )
        conn.commit()

    # Invalidate cache
    r.delete(f"user:{user_id}")

    return {"status": "updated"}

@app.post("/users")
def update_user(name: str, email: str):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (name, email)
        )
        conn.commit()

    return {"status": "added"}
