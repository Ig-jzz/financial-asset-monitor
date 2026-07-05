import sqlite3
import os
from config import DB_PATH


def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def setup_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS assets (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker     TEXT UNIQUE NOT NULL,
            name       TEXT,
            type       TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS price_history (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER NOT NULL,
            date     TEXT NOT NULL,
            open     REAL,
            high     REAL,
            low      REAL,
            close    REAL,
            volume   INTEGER,
            FOREIGN KEY (asset_id) REFERENCES assets(id),
            UNIQUE(asset_id, date)
        );

        CREATE TABLE IF NOT EXISTS daily_indicators (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id         INTEGER NOT NULL,
            date             TEXT NOT NULL,
            daily_change_pct REAL,
            change_7d_pct    REAL,
            change_30d_pct   REAL,
            ma_7             REAL,
            ma_30            REAL,
            volume_avg_7d    REAL,
            FOREIGN KEY (asset_id) REFERENCES assets(id),
            UNIQUE(asset_id, date)
        );
    """)

    conn.commit()
    conn.close()
    print("[db] Tabelas verificadas/criadas.")


def upsert_asset(ticker, name, asset_type):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO assets (ticker, name, type) VALUES (?, ?, ?)",
        (ticker, name, asset_type)
    )
    conn.commit()
    cur.execute("SELECT id FROM assets WHERE ticker = ?", (ticker,))
    asset_id = cur.fetchone()[0]
    conn.close()
    return asset_id


def insert_prices(rows):
    # rows: list de (asset_id, date, open, high, low, close, volume)
    conn = get_conn()
    cur = conn.cursor()
    cur.executemany("""
        INSERT OR REPLACE INTO price_history
            (asset_id, date, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, rows)
    conn.commit()
    conn.close()


def insert_indicators(rows):
    # rows: list de (asset_id, date, daily_pct, 7d_pct, 30d_pct, ma7, ma30, vol_avg7)
    conn = get_conn()
    cur = conn.cursor()
    cur.executemany("""
        INSERT OR REPLACE INTO daily_indicators
            (asset_id, date, daily_change_pct, change_7d_pct, change_30d_pct,
             ma_7, ma_30, volume_avg_7d)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)
    conn.commit()
    conn.close()
