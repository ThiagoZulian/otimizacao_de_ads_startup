import pandas as pd
from IPython.display import Markdown, display


def display_df(
    df: pd.DataFrame, caption: str | None = None, format_dict: dict | None = None
) -> None:
    styler = df.style.set_table_styles(
        [
            {
                "selector": "caption",
                "props": [
                    ("text-align", "left"),
                    ("font-size", "19px"),
                    ("font-weight", "bold"),
                ],
            }
        ]
    )
    if caption:
        styler = styler.set_caption(caption.capitalize())
    if format_dict:
        styler = styler.format(format_dict)
    display(styler)


def full_describe(df: pd.DataFrame) -> None:
    display(Markdown("### DESCRIÇÃO COMPLETA"))

    # Info geral
    display(df.info())

    # Categóricas
    cols_cat = df.select_dtypes(include=["object", "category"]).columns
    if len(cols_cat) > 0:
        df_cat = df[cols_cat].describe().T
        display_df(df_cat, caption="Descrição de Categóricas")

    # Numéricas
    cols_num = df.select_dtypes(include=["number"]).columns
    if len(cols_num) > 0:
        df_num = df[cols_num].describe().T
        df_num["cv"] = df_num["std"] / df_num["mean"]
        display_df(df_num, caption="Descrição de Numéricas")

    # Amostra
    display_df(df.head(), caption="Linhas iniciais da tabela")


def value_counts(df: pd.DataFrame) -> None:
    display(Markdown("### VALORES ÚNICOS" + "\n__apenas top 10 valores__"))

    for col in df.select_dtypes(include=["object", "category"]).columns:
        counts = df[col].value_counts()
        percents = df[col].value_counts(normalize=True).mul(100).round(2)

        summary = pd.DataFrame({"qtd": counts, "percentual": percents}).sort_values(
            "qtd", ascending=False
        )
        summary.index.name = None

        display_df(
            df=summary.head(10), caption=f"{col}", format_dict={"percentual": "{:.2f}"}
        )
