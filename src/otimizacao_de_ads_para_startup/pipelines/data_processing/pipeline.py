"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 1.0.0
"""

from kedro.pipeline import Node, Pipeline  # noqa
from .nodes import process_df_perfil


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            Node(
                func=process_df_perfil,
                inputs=["campanhas", "categorias"],
                outputs="perfis",
                name="process_df_perfil_node",
            ),
        ]
    )
