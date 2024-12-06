from os.path import join
from typing import Any

from xgboost import Booster, XGBClassifier

from deeploy.enums import ModelType

from . import BaseModel


class XGBoostModel(BaseModel):
    __xgboost_model: XGBClassifier

    def __init__(self, model_object: Any, **kwargs) -> None:
        if not issubclass(type(model_object), XGBClassifier) and not issubclass(
            type(model_object), Booster
        ):
            raise Exception("Not a valid XGBoost class")

        self.__xgboost_model = model_object

    def save(self, local_folder_path: str) -> None:
        self.__xgboost_model.save_model(join(local_folder_path, "model.bst"))

    def get_model_type(self) -> ModelType:
        return ModelType.XGBOOST
