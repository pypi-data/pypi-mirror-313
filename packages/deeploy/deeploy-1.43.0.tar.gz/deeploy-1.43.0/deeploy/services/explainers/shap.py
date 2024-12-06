from os.path import join
from typing import Any

import dill
from shap.explainers._explainer import Explainer

from deeploy.enums import ExplainerType

from . import BaseExplainer


class SHAPKernelExplainer(BaseExplainer):
    __shap_explainer: Explainer

    def __init__(self, explainer_object: Any) -> None:
        if not issubclass(type(explainer_object), Explainer):
            raise Exception("Not a valid SHAP class")

        self.__shap_explainer = explainer_object
        return

    def save(self, local_folder_path: str) -> None:
        with open(join(local_folder_path, "explainer.dill"), "wb") as f:
            dill.dump(self.__shap_explainer, f)
        return

    def get_explainer_type(self) -> ExplainerType:
        return ExplainerType.SHAP_KERNEL
