from typing import Any

from deeploy.enums import ModelType


class BaseModel:
    def __init__(self, model_object: Any, **kwargs) -> None:
        return

    def save(self, local_folder_path: str) -> None:
        return

    def get_model_type(self) -> ModelType:
        return
