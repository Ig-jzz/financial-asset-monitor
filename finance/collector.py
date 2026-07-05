import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from config import ATIVOS, PERIOD_DAYS


def fetch_ticker(ticker):
    start = (datetime.today() - timedelta(days=PERIOD_DAYS)).strftime("%Y-%m-%d")

    try:
        raw = yf.download(ticker, start=start, progress=False, auto_adjust=True)
        if raw.empty:
            print(f"  [!] Sem dados para {ticker}")
            return None

        df = raw.reset_index()

        # yfinance às vezes retorna MultiIndex nas colunas
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0].lower() for col in df.columns]
        else:
            df.columns = [c.lower() for c in df.columns]

        df = df.rename(columns={"date": "date"})
        df["ticker"] = ticker
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

        return df[["ticker", "date", "open", "high", "low", "close", "volume"]]

    except Exception as e:
        print(f"  [!] Erro ao coletar {ticker}: {e}")
        return None


def fetch_all():
    collected = {}

    for category, tickers in ATIVOS.items():
        for ticker, name in tickers.items():
            print(f"  Coletando {ticker} ({name})...")
            df = fetch_ticker(ticker)
            if df is not None:
                collected[ticker] = {
                    "name": name,
                    "category": category,
                    "data": df
                }

    return collected
