import pandas as pd


def compute(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recebe um DataFrame com colunas [date, close, volume]
    e retorna um DataFrame com os indicadores calculados.
    """
    df = df.sort_values("date").copy()
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce")

    # Variação diária (%)
    df["daily_change_pct"] = df["close"].pct_change() * 100

    # Variação em relação a 7 e 30 dias atrás
    df["change_7d_pct"] = df["close"].pct_change(periods=7) * 100
    df["change_30d_pct"] = df["close"].pct_change(periods=30) * 100

    # Médias móveis simples
    df["ma_7"] = df["close"].rolling(window=7).mean()
    df["ma_30"] = df["close"].rolling(window=30).mean()

    # Volume médio 7 dias
    df["volume_avg_7d"] = df["volume"].rolling(window=7).mean()

    return df[[
        "date",
        "daily_change_pct",
        "change_7d_pct",
        "change_30d_pct",
        "ma_7",
        "ma_30",
        "volume_avg_7d"
    ]]
