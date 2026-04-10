import psycopg2
from psycopg2.extras import execute_values

DB_CONFIG = {
    "host":"localhost",
    "port":5432,
    "dbname":"stockdb",
    "user":"stockuser",
    "password":"stockpass"
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)

# def create_tables():
#     conn = get_connection()
#     cur = conn.cursor()

#     #Execute the TimescaleDB extension
#     cur.execute("CREATE EXTENSION IF NOT EXISTS timescaledb;")

#     #Create headlines table
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS headlines (
#             id          BIGSERIAL,
#             published_at TIMESTAMPTZ NOT NULL,
#             scraped_at  TIMESTAMPTZ NOT NULL,
#             headline    TEXT NOT NULL,
#             url         TEXT UNIQUE NOT NULL,
#             sentiment   TEXT,
#             sentiment_score FLOAT,
#             processed_at TIMESTAMPTZ
#         );
# """)
    
#     #Convert to hypertable (TimescaleDB time-series table)
#     cur.execute("""
#         SELECT create_hypertable('headlines', 'published_at',
#                if_not_exists => TRUE);
# """)
#     conn.commit()
#     cur.close()
#     conn.close()
#     print("[db] Tables created successfully.")

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Enable TimescaleDB extension
    cur.execute("CREATE EXTENSION IF NOT EXISTS timescaledb;")

    # Drop and recreate cleanly
    cur.execute("DROP TABLE IF EXISTS headlines;")

    # Create headlines table — no separate primary key, published_at is part of it
    cur.execute("""
        CREATE TABLE IF NOT EXISTS headlines (
            published_at    TIMESTAMPTZ NOT NULL,
            scraped_at      TIMESTAMPTZ NOT NULL,
            headline        TEXT NOT NULL,
            url             TEXT NOT NULL,
            sentiment       TEXT,
            sentiment_score FLOAT,
            processed_at    TIMESTAMPTZ,
            UNIQUE (url, published_at)
        );
    """)

    # Convert to hypertable
    cur.execute("""
        SELECT create_hypertable('headlines', 'published_at',
               if_not_exists => TRUE);
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("[db] Tables created successfully.")


def insert_headlines(headlines: list[dict]):
    if not headlines:
        return
    conn= get_connection()
    cur = conn.cursor()

    rows = []
    for h in headlines:
        rows.append((
            h.get("published_at"),
            h.get("scraped_at"),
            h.get("headline"),
            h.get("url"),
            h.get("sentiment"),
            h.get("sentiment_score"),
            h.get("processed_at")
        ))
    execute_values(cur, """
INSERT INTO headlines
            (published_at, scraped_at, headline, url, sentiment, sentiment_score, processed_at)
        VALUES %s
        ON CONFLICT (url, published_at) DO NOTHING;
""", rows)
    
    inserted= cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    print(f"[db] Inserted {inserted} rows into headlines table.")

if __name__=="__main__":
    create_tables()