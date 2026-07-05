"""
Pipeline de Dados para Monitoramento de Ativos Financeiros
----------------------------------------------------------
Coleta dados de ações, criptomoedas e índices via yfinance,
processa indicadores e salva no SQLite. Exporta CSVs para Power BI.

Uso:
    python pipeline.py               # roda coleta + indicadores + export
    python pipeline.py --only-export # só gera os CSVs (sem coletar)
"""

import sys
from datetime import datetime

import database
import collector
import indicators
import export


def run_pipeline():
    start = datetime.now()
    print(f"\n{'='*50}")
    print(f"  Pipeline iniciado: {start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

    # 1. Garante que o banco e as tabelas existem
    print("[1/4] Verificando banco de dados...")
    database.setup_db()

    # 2. Coleta os dados
    print("\n[2/4] Coletando dados dos ativos...")
    collected = collector.fetch_all()

    if not collected:
        print("[!] Nenhum dado coletado. Verifique sua conexão.")
        sys.exit(1)

    # 3. Processa e salva
    print(f"\n[3/4] Processando e salvando {len(collected)} ativo(s)...")

    for ticker, info in collected.items():
        df = info["data"]
        name = info["name"]
        category = info["category"]

        asset_id = database.upsert_asset(ticker, name, category)

        # Salva preços
        price_rows = [
            (
                asset_id,
                row["date"],
                row["open"],
                row["high"],
                row["low"],
                row["close"],
                row["volume"]
            )
            for _, row in df.iterrows()
        ]
        database.insert_prices(price_rows)

        # Calcula e salva indicadores
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
        print(f"  ✓ {ticker} — {len(price_rows)} registros salvos")

    # 4. Exporta CSVs para Power BI
    print("\n[4/4] Exportando CSVs para Power BI...")
    export.export_all()

    elapsed = (datetime.now() - start).total_seconds()
    print(f"\n{'='*50}")
    print(f"  Pipeline finalizado em {elapsed:.1f}s")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    if "--only-export" in sys.argv:
        print("[modo] Apenas exportação...")
        export.export_all()
    else:
        run_pipeline()
