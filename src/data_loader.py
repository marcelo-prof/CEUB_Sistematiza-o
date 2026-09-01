"""
data_loader.py — Módulo 0: Dados Reais
Carrega o dataset de municípios (renda, PIB, população).
"""

import pandas as pd

BD = "data/municipios_renda.csv"

variaveis_numericas = {
    "populacao": "População do município (habitantes)",
    "renda_media_mensal": "Renda média por mês",
    "pib_anual_mil_reais": "PIB anual em reais",
    "pib_per_capita_reais": "PIB per capita em reais"
}

variaveis_categoricas = {
    "regiao": "Região",
    "uf": "Sigla do Estado"
}


def carregar_dados(caminho=BD):
    df = pd.read_csv(caminho, sep=",")
    return df


def obter_serie_numerica(df, coluna):
    return df[coluna].dropna().astype(float).tolist()


def obter_serie_categorica(df, coluna):
    return df[coluna].dropna().astype(str).tolist()
