import os

import psycopg2
from fastapi import FastAPI, HTTPException

app = FastAPI()

DB_CONFIG = {
    "host": os.environ["DB_HOST"],
    "port": os.environ.get("DB_PORT", "5432"),
    "dbname": os.environ["DB_NAME"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


@app.on_event("startup")
def create_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS health_checks (
                    id SERIAL PRIMARY KEY,
                    checked_at TIMESTAMP DEFAULT NOW()
                )
                """
            )
        conn.commit()


@app.get("/ping")
def ping():
    return {"message": "pong"}


@app.get("/db/health")
def db_health():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/db/check")
def insert_check():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO health_checks DEFAULT VALUES RETURNING id, checked_at"
                )
                row = cur.fetchone()
            conn.commit()
        return {"id": row[0], "checked_at": row[1].isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/db/checks")
def list_checks():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, checked_at FROM health_checks ORDER BY id DESC LIMIT 20"
                )
                rows = cur.fetchall()
        return [{"id": r[0], "checked_at": r[1].isoformat()} for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
