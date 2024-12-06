from os.path import join
from typing import Any

from joblib import dump
from sklearn.base import BaseEstimator

from deeploy.enums import ModelType

from . import BaseModel


class SKLearnModel(BaseModel):
    __sklearn_model: BaseEstimator

    def __init__(self, model_object: Any, **kwargs) -> None:
        if not issubclass(type(model_object), BaseEstimator):
            raise Exception("Not a valid SKLearn class")

        self.__sklearn_model = model_object

    def save(self, local_folder_path: str) -> None:
        dump(self.__sklearn_model, join(local_folder_path, "model.joblib"))

    def get_model_type(self) -> ModelType:
        return ModelType.SKLEARN
