import inspect
from os.path import join
from typing import Any

import dill
from omnixai.explainers.tabular import TabularExplainer

from deeploy.enums import ExplainerType

from . import BaseExplainer


class OmniTabularExplainer(BaseExplainer):
    __omni_explainer: TabularExplainer

    def __init__(self, explainer_object: Any) -> None:
        if not issubclass(type(explainer_object[0]), TabularExplainer):
            raise Exception("Not a valid class")

        self.__omni_explainer = explainer_object
        return

    def save(self, local_folder_path: str) -> None:
        with open(join(local_folder_path, "explainer.dill"), "wb") as f:
            dill.dump(self.__omni_explainer, f)
        return

    def get_explainer_type(self) -> ExplainerType:
        base_classes = list(
            map(
                lambda x: x.__module__ + "." + x.__name__,
                inspect.getmro(type(self.__omni_explainer[0])),
            )
        )

        if (
            "omnixai.explainers.tabular.auto.TabularExplainer" in base_classes
        ) and "pdp" in self.__omni_explainer[0].explainer_names:
            return ExplainerType.PDP_TABULAR

        if (
            "omnixai.explainers.tabular.auto.TabularExplainer" in base_classes
            and "mace" in self.__omni_explainer[0].explainer_names
        ):
            return ExplainerType.MACE_TABULAR
