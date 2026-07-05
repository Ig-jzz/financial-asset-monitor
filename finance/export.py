import sqlite3
import pandas as pd
import os
from config import DB_PATH, EXPORTS_PATH


def export_all():
    os.makedirs(EXPORTS_PATH, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            a.ticker,
            a.name,
            a.type,
            p.date,
            p.open,
            p.high,
            p.low,
            p.close,
            p.volume,
            i.daily_change_pct,
            i.change_7d_pct,
            i.change_30d_pct,
            i.ma_7,
            i.ma_30,
            i.volume_avg_7d
        FROM price_history p
        JOIN assets a ON a.id = p.asset_id
        LEFT JOIN daily_indicators i ON i.asset_id = p.asset_id AND i.date = p.date
        ORDER BY a.ticker, p.date
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    cols_numericas = ["open", "high", "low", "close", "volume",
                      "daily_change_pct", "change_7d_pct", "change_30d_pct",
                      "ma_7", "ma_30", "volume_avg_7d"]
    for col in cols_numericas:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    cols_preco = ["open", "high", "low", "close", "ma_7", "ma_30", "volume_avg_7d"]
    cols_pct   = ["daily_change_pct", "change_7d_pct", "change_30d_pct"]
    df[cols_preco] = df[cols_preco].round(2)
    df[cols_pct]   = df[cols_pct].round(4)

    def salvar(dataframe, path):
        dataframe.to_csv(path, index=False, encoding="utf-8-sig", decimal=".")
        print(f"[export] {path} — {len(dataframe)} linhas")

    salvar(df, os.path.join(EXPORTS_PATH, "asset_data.csv"))

    for category in df["type"].unique():
        salvar(df[df["type"] == category], os.path.join(EXPORTS_PATH, f"{category}.csv"))

    latest = df.sort_values("date").groupby("ticker").last().reset_index()
    salvar(latest, os.path.join(EXPORTS_PATH, "latest_prices.csv"))