DB_PATH = "data/assets.db"
EXPORTS_PATH = "exports"

# Período de histórico que o pipeline vai buscar (em dias)
PERIOD_DAYS = 90

# Ativos monitorados
ATIVOS = {
    "acoes_br": {
        "PETR4.SA": "Petrobras PN",
        "VALE3.SA": "Vale ON",
        "ITUB4.SA": "Itaú Unibanco PN",
        "BBDC4.SA": "Bradesco PN",
        "WEGE3.SA": "WEG ON",
    },
    "cripto": {
        "BTC-USD": "Bitcoin",
        "ETH-USD": "Ethereum",
    },
    "indices": {
        "^BVSP": "Ibovespa",
        "^GSPC": "S&P 500",
    }
}
