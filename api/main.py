from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import psycopg2.extras
from datetime import datetime, timezone
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Stock Research API")
Instrumentator().instrument(app).expose(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


DB_CONFIG = {
    "host" : "localhost",
    "port" : 5432,
    "dbname" : "stockdb",
    "user" : "stockuser",
    "password" : "stockpass"
}

def get_conn():
    return psycopg2.connect(**DB_CONFIG)

@app.get("/")
def root():
    return {"status" : "ok", "message": "Stock Research API is running."}

@app.get("/headlines")
def get_headlines(limit:int =Query(20, le=100), offset: int = 0):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT headline, url, sentiment, sentiment_score, published_at, processed_at
        FROM headlines
        ORDER BY published_at DESC
        LIMIT %s OFFSET %s;
""", (limit, offset))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"data":rows, "count":len(rows)}


@app.get("/sentiment/summary")
def sentiment_summary():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT sentiment, COUNT(*) as count
        FROM headlines
        GROUP BY sentiment
        ORDER BY count DESC;
""")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"data": rows}

@app.get("/sentiment/trend")
def sentiment_trend():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
            SELECT
            time_bucket('1 hour', published_at) AS bucket,
            AVG(sentiment_score) AS avg_score,
            COUNT(*) AS count
        FROM headlines
        GROUP BY bucket
        ORDER BY bucket DESC
        LIMIT 24;
""")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"data" : rows}

@app.get("/headlines/search")
def search_headlines(q: str = Query(..., min_length=2)):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT headline, url, sentiment, sentiment_score, published_at
        FROM headlines
        WHERE headline ILIKE %s
        ORDER BY published_at DESC
        LIMIT 20;
    """, (f"%{q}%",))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"data": rows, "count": len(rows)}