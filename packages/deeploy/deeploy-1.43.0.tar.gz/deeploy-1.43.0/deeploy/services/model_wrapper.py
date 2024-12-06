import inspect
from typing import Any, List

from deeploy.enums import ModelFrameworkVersion, ModelType
from deeploy.services.models import BaseModel


class ModelWrapper:
    __model_helper: BaseModel

    def __init__(self, model_object: Any, **kwargs) -> None:
        self.__model_helper = self.__get_model_helper(model_object, **kwargs)

        return

    def save(self, local_folder_path: str) -> None:
        # Check model type
        model_type = self.get_model_type()
        self._check_framework_version(model_type)

        self.__model_helper.save(local_folder_path)
        return

    def get_model_type(self) -> ModelType:
        return self.__model_helper.get_model_type()

    def __get_model_type(self, model_object: Any) -> ModelType:
        base_classes = list(
            map(
                lambda x: x.__module__ + "." + x.__name__,
                inspect.getmro(type(model_object)),
            )
        )

        if self.__is_sklearn(base_classes):
            return ModelType.SKLEARN
        if self.__is_xgboost(base_classes):
            return ModelType.XGBOOST
        if self.__is_pytorch(base_classes):
            return ModelType.PYTORCH
        if self.__is_tensorflow(base_classes):
            return ModelType.TENSORFLOW

        raise NotImplementedError("This model type is not implemented by Deeploy")

    def __get_model_helper(self, model_object, **kwargs) -> BaseModel:
        model_type = self.__get_model_type(model_object)

        # only import the helper class when it is needed
        if model_type == ModelType.SKLEARN:
            from deeploy.services.models.sklearn import SKLearnModel

            return SKLearnModel(model_object, **kwargs)
        if model_type == ModelType.XGBOOST:
            from deeploy.services.models.xgboost import XGBoostModel

            return XGBoostModel(model_object, **kwargs)
        if model_type == ModelType.PYTORCH:
            from deeploy.services.models.pytorch import PyTorchModel

            return PyTorchModel(model_object, **kwargs)
        if model_type == ModelType.TENSORFLOW:
            from deeploy.services.models.tensorflow import TensorFlowModel

            return TensorFlowModel(model_object, **kwargs)
        
        if model_type == ModelType.LIGHTGBM:
            from deeploy.services.models.lightgbm import LightGBMModel

            return LightGBMModel(model_object, **kwargs)

    def __is_sklearn(self, base_classes: List[str]) -> bool:
        return (
            "sklearn.base.BaseEstimator" in base_classes
            and "xgboost.sklearn.XGBModel" not in base_classes
        )

    def __is_xgboost(self, base_classes: List[str]) -> bool:
        return "xgboost.sklearn.XGBModel" in base_classes or "xgboost.core.Booster" in base_classes

    def __is_pytorch(self, base_classes: List[str]) -> bool:
        return "torch.nn.modules.module.Module" in base_classes

    def __is_tensorflow(self, base_classes: List[str]) -> bool:
        return "tensorflow.python.module.module.Module" in base_classes
    
    def __is_lightgbm(self, base_classes: List[str]) -> bool:
        return "lightgbm.basic.Booster" in base_classes

    def _check_framework_version(self, model_type: ModelType) -> None:
        framework_mismatch = ""
        
        if model_type == ModelType.SKLEARN:            
            import sklearn
            if sklearn.__version__ != ModelFrameworkVersion.SKLEARN_CURRENT:
                framework_mismatch = f"sklearn ({sklearn.__version__})"

        if model_type == ModelType.XGBOOST:            
            import xgboost
            if xgboost.__version__ != ModelFrameworkVersion.XGBOOST_CURRENT:
                framework_mismatch = f"xgboost ({xgboost.__version__})"
        
        if model_type == ModelType.LIGHTGBM:            
            import lightgbm
            if lightgbm.__version__ != ModelFrameworkVersion.LIGHTGBM_CURRENT:
                framework_mismatch = f"lightgbm ({lightgbm.__version__})"
            
        if framework_mismatch:  
            import logging
            logger = logging.getLogger(__name__)  
            warning_message = \
                f"WARNING: Your version of {framework_mismatch} is not recommended for Deeploy." + \
                "Issues may arise when deploying the model. \n" + \
                "Check Deeploy docs to find the current supported version: https://docs.deeploy.ml/supported-versions"
            logger.warning(warning_message)