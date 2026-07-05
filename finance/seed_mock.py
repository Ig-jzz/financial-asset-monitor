"""
seed_mock.py — Popula o banco com dados sintéticos para testar o pipeline.
Útil para desenvolvimento offline. Não use em produção.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import database
import indicators

np.random.seed(42)

MOCK_ASSETS = {
    "PETR4.SA": ("Petrobras PN", "acoes_br", 38.50),
    "VALE3.SA": ("Vale ON", "acoes_br", 62.10),
    "BTC-USD": ("Bitcoin", "cripto", 67000.00),
    "^BVSP":   ("Ibovespa", "indices", 128000.0),
}

def gerar_precos(preco_inicial, n_dias=90):
    precos = [preco_inicial]
    for _ in range(n_dias - 1):
        variacao = np.random.normal(0, 0.015)  # ~1.5% de volatilidade diária
        precos.append(round(precos[-1] * (1 + variacao), 2))
    return precos


def run():
    database.setup_db()

    hoje = datetime.today()
    datas = [(hoje - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(89, -1, -1)]

    for ticker, (name, category, preco_base) in MOCK_ASSETS.items():
        asset_id = database.upsert_asset(ticker, name, category)

        closes = gerar_precos(preco_base)

        price_rows = []
        for i, date in enumerate(datas):
            close = closes[i]
            open_  = round(close * np.random.uniform(0.99, 1.01), 2)
            high   = round(close * np.random.uniform(1.00, 1.02), 2)
            low    = round(close * np.random.uniform(0.98, 1.00), 2)
            volume = int(np.random.uniform(5_000_000, 50_000_000))
            price_rows.append((asset_id, date, open_, high, low, close, volume))

        database.insert_prices(price_rows)

        df = pd.DataFrame(price_rows, columns=["asset_id", "date", "open", "high", "low", "close", "volume"])
        ind_df = indicators.compute(df)

        ind_rows = [
            (
                asset_id,
                row["date"],
                row["daily_change_pct"],
                row["change_7d_pct"],
                row["change_30d_pct"],
                row["ma_7"],
                row["ma_30"],
                row["volume_avg_7d"]
            )
            for _, row in ind_df.iterrows()
        ]
        database.insert_indicators(ind_rows)
        print(f"  ✓ {ticker} ({name}) — {len(price_rows)} dias inseridos")

    print("\n[seed] Banco populado com dados mock.")


if __name__ == "__main__":
    run()
