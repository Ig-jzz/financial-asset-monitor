# Financial Asset Monitor

Projeto pessoal que desenvolvi pra praticar construção de pipelines de dados. A ideia surgiu da vontade de acompanhar ações e cripto de forma automatizada, sem depender de apps prontos — e aproveitar pra aplicar Python, SQL e Power BI num contexto real.

O pipeline coleta preços diariamente, calcula alguns indicadores e exporta tudo pro Power BI. Roda de segunda a sexta via n8n, sem precisar de intervenção manual.

## O que faz

Monitora 9 ativos: Petrobras, Vale, Itaú, Bradesco, WEG, Bitcoin, Ethereum, Ibovespa e S&P 500.

Para cada ativo, coleta 90 dias de histórico e calcula:
- Variação diária, semanal e mensal (%)
- Médias móveis de 7 e 30 dias
- Volume médio dos últimos 7 dias

## Stack

- **Python** — coleta (yfinance), processamento (pandas) e orquestração
- **SQLite** — armazenamento local dos dados históricos
- **n8n** — agendamento automático de segunda a sexta às 8h
- **Power BI** — dashboard com histórico, médias móveis e tabela de variações

## Como rodar

```bash
pip install -r requirements.txt
python pipeline.py
```

O pipeline cria o banco automaticamente na primeira execução e exporta os CSVs pra pasta `exports/`. Pra atualizar sem rebuscar dados:

```bash
python pipeline.py --only-export
```

## Estrutura

```
├── config.py        # lista de ativos monitorados
├── collector.py     # coleta via yfinance
├── indicators.py    # cálculo de MA, variações
├── database.py      # operações SQLite
├── export.py        # geração dos CSVs
├── pipeline.py      # entrada principal
├── requirements.txt
└── n8n_workflow/
    └── pipeline_workflow.json
```

## Observações

Os dados são coletados com `auto_adjust=True` (preços ajustados por dividendos e splits). O pipeline usa `INSERT OR REPLACE`, então rodar mais de uma vez no mesmo dia não duplica registros.

Num ambiente com Windows em português, o CSV é exportado com vírgula como separador decimal pra compatibilidade com o Power BI.
