from os.path import join
from typing import Any

from lightgbm import LGBMClassifier

from deeploy.enums import ModelType

from . import BaseModel


class LightGBMModel(BaseModel):
    __lightgbm_model: LGBMClassifier

    def __init__(self, model_object: Any, **kwargs) -> None:
        if not issubclass(type(model_object), LGBMClassifier):
            raise Exception("Not a valid LightGBM class")

        self.__lightgbm_model = model_object

    def save(self, local_folder_path: str) -> None:
        self.__lightgbm_model.save_model(join(local_folder_path, "model.bst"))

    def get_model_type(self) -> ModelType:
        return ModelType.LIGHTGBM
