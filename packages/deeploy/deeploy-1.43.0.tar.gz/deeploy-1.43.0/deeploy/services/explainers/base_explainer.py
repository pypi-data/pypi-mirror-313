from typing import Any

from deeploy.enums import ExplainerType


class BaseExplainer:
    def __init__(self, explainer_object: Any) -> None:
        return

    def save(self, local_folder_path: str) -> None:
        return

    def get_explainer_type(self) -> ExplainerType:
        return
