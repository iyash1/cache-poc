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
    cached = r.get(f"user:{user_id}")
    if cached:
        print("CACHE HIT")
        return json.loads(cached)

    # Fallback (rare)
    print("CACHE MISS")
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, name FROM users WHERE id = %s",
            (user_id,)
        )
        row = cur.fetchone()

    if not row:
        print("DB MISS")
        return {"error": "not found"}

    user = {"id": row[0], "name": row[1]}
    r.setex(f"user:{user_id}", 60, json.dumps(user))
    return user


@app.put("/users/{user_id}")
def update_user(user_id: int, name: str):
    user = {"id": user_id, "name": name}

    # 1. Write to DB
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE users SET name = %s WHERE id = %s",
            (name, user_id)
        )
        conn.commit()
    print("DB UPDATED")

    # 2. Write to cache
    r.setex(f"user:{user_id}", 60, json.dumps(user))
    print("CACHE UPDATED")

    return {"status": "updated"}

@app.post("/users")
def update_user(name: str, email: str):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
            (name, email)
        )
        user_id = cur.fetchone()[0]
        conn.commit()

    # 2. Write to cache
    r.setex(f"user:{user_id}", 60, json.dumps({"id": user_id, "name": name, "email": email}))
    print("CACHE UPDATED")

    return {"status": "added"}