import inspect
from os.path import join
from typing import Any

import dill
from alibi.api.interfaces import Explainer

from deeploy.enums import ExplainerType

from . import BaseExplainer


class AlibiExplainer(BaseExplainer):
    __alibi_explainer: Explainer

    def __init__(self, explainer_object: Any) -> None:
        if not issubclass(type(explainer_object), Explainer):
            raise Exception("Not a valid Alibi class")

        self.__alibi_explainer = explainer_object
        return

    def save(self, local_folder_path: str) -> None:
        with open(join(local_folder_path, "explainer.dill"), "wb") as f:
            dill.dump(self.__alibi_explainer, f)
        return

    def get_explainer_type(self) -> ExplainerType:
        base_classes = list(
            map(
                lambda x: x.__module__ + "." + x.__name__,
                inspect.getmro(type(self.__alibi_explainer)),
            )
        )

        if "alibi.explainers.anchor_text.AnchorText" in base_classes:
            return ExplainerType.ANCHOR_TEXT
        if "alibi.explainers.anchor_image.AnchorImage" in base_classes:
            return ExplainerType.ANCHOR_IMAGES
        if "alibi.explainers.anchor_tabular.AnchorTabular" in base_classes:
            return ExplainerType.ANCHOR_TABULAR
