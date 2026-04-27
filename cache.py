import sqlite3
import json
import time

conn = sqlite3.connect("trends_cache.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS trends_cache (
    query TEXT PRIMARY KEY,
    response TEXT,
    timestamp INTEGER
)
""")

CACHE_TTL = 60 * 60 * 24  # 24h


def get_cached(query):
    cursor.execute(
        "SELECT response, timestamp FROM trends_cache WHERE query=?",
        (query,)
    )
    row = cursor.fetchone()

    if not row:
        return None

    data, ts = row

    if time.time() - ts > CACHE_TTL:
        return None

    return json.loads(data)


def set_cache(query, response):
    cursor.execute("""
    INSERT OR REPLACE INTO trends_cache VALUES (?, ?, ?)
    """, (query, json.dumps(response), int(time.time())))
    conn.commit()