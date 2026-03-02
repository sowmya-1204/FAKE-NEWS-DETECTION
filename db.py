import sqlite3
from datetime import datetime

DB_NAME = "fake_news.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article TEXT NOT NULL,
        prediction TEXT,
        fake_score REAL,
        real_score REAL,
        verified_true INTEGER,
        verified_false INTEGER,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_analysis(article, prediction, fake_score, real_score, true_count, false_count):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO analyses 
    (article, prediction, fake_score, real_score, verified_true, verified_false, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        article,
        prediction,
        fake_score,
        real_score,
        true_count,
        false_count,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()