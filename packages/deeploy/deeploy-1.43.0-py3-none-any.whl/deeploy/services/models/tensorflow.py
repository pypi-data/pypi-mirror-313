from os.path import join
from typing import Any

from tensorflow import Module

from deeploy.enums import ModelType

from . import BaseModel


class TensorFlowModel(BaseModel):
    __tensorflow_model: Module

    def __init__(self, model_object: Any, **kwargs) -> None:
        if not issubclass(type(model_object), Module):
            raise Exception("Not a valid TensorFlow class")
        self.__tensorflow_model = model_object

    def save(self, local_folder_path: str) -> None:
        self.__tensorflow_model.save(join(local_folder_path, "1"))

    def get_model_type(self) -> ModelType:
        return ModelType.TENSORFLOW
