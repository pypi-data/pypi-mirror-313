from typing import Any

from torch.nn import Module

from deeploy.enums import ModelType

from . import BaseModel


class PyTorchModel(BaseModel):
    __pytorch_model: Module
    __model_file_path: str
    __handler_file_path: str = None

    def __init__(
        self,
        model_object: Any,
        pytorch_model_file_path: str,
        pytorch_torchserve_handler_name: str,
        **kwargs,
    ) -> None:
        self.__pytorch_model = model_object
        self.__model_file_path = pytorch_model_file_path
        self.__handler_name = pytorch_torchserve_handler_name

    def save(self, local_folder_path: str) -> None:
        raise NotImplementedError("Saving PyTorch models is not implemented in the Python client yet. Use torch-model-archiver CLI to save the model.")
    
    def get_model_type(self) -> ModelType:
        return ModelType.PYTORCH
