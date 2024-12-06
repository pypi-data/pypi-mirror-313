from enum import Enum


class ModelType(Enum):
    """Class that contains model types"""

    TENSORFLOW = 0
    PYTORCH = 1
    SKLEARN = 2
    XGBOOST = 3
    ONNX = 4
    TRITON = 5
    CUSTOM = 6
    LIGHTGBM = 7
    PMML = 8
    HUGGINGFACE = 9


class ModelFrameworkVersion(Enum):
    """Class that contains model framework versions"""
    XGBOOST_CURRENT = "2.0.2"
    SKLEARN_CURRENT = "1.3.0"
    LIGHTGBM_CURRENT = "3.3.2"
    XGBOOST_1_7_5 = "xgboost_1_7_5"
