"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 1.0.0
"""

import numpy as np
import pandas as pd
from unidecode import unidecode


# arrumar nomes das colunas, remover espaços e acentos
def arrumar_nomes(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").map(unidecode)
    return df


def preprocess_campanha(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(
        columns={
            "qte_de_impressões": "impressoes",
            "qte_de_clicks": "cliques",
            "sexo": "genero",
            "valor_investido_no_anúncio": "custo",
            "Qte_de_Vendas_após_Clique": "vendas",
        }
    )

    return arrumar_nomes(df)


def preprocess_categorias(df: pd.DataFrame) -> pd.DataFrame:
    df["descrição_da_categoria"] = df["descrição_da_categoria"].ffill()
    return arrumar_nomes(df)


def process_df_perfil(
    df_campanha: pd.DataFrame, df_categoria: pd.DataFrame
) -> pd.DataFrame:
    df_campanha = preprocess_campanha(df_campanha)
    df_categoria = preprocess_categorias(df_categoria)

    df_campanha_merged = df_campanha.merge(
        df_categoria, how="left", on="categoria_de_interesse"
    )

    df_campanha_merged = df_campanha_merged.astype(
        {
            "campanha": "category",
            "faixa_etaria": "category",
            "genero": "category",
            "categoria_de_interesse": "category",
            "descricao_da_categoria": "category",
        }
    )

    df_campanha_merged["perfil"] = (
        df_campanha_merged["faixa_etaria"].astype(str)
        + " | "
        + df_campanha_merged["genero"].astype(str)
        + " | "
        + df_campanha_merged["categoria_de_interesse"].astype(str)
    ).astype("category")

    df_perfil = (
        df_campanha_merged[
            [
                "perfil",
                "faixa_etaria",
                "genero",
                "categoria_de_interesse",
                "descricao_da_categoria",
                "impressoes",
                "cliques",
                "custo",
                "vendas",
            ]
        ]
        .groupby(
            [
                "faixa_etaria",
                "genero",
                "categoria_de_interesse",
                "descricao_da_categoria",
                "perfil",
            ],
            observed=True,
        )
        .agg("sum")
        .reset_index()
    )

    valor_venda = 85.00

    df_perfil["faturamento"] = df_perfil["vendas"] * valor_venda
    df_perfil["lucro"] = df_perfil["faturamento"] - df_perfil["custo"]
    df_perfil["ctr"] = df_perfil["cliques"] / df_perfil["impressoes"]
    df_perfil["tc"] = df_perfil["vendas"] / df_perfil["cliques"]
    df_perfil["cpc"] = df_perfil["custo"] / df_perfil["cliques"]
    df_perfil["cc"] = df_perfil["custo"] / df_perfil["vendas"]
    df_perfil["roi"] = (df_perfil["faturamento"] - df_perfil["custo"]) / df_perfil[
        "custo"
    ]
    df_perfil["conversao"] = df_perfil["vendas"] / df_perfil["impressoes"]

    df_perfil["cc"] = df_perfil["cc"].replace([np.inf, -np.inf], np.nan)

    return df_perfil
