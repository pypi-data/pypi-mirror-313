from typing import Dict, Optional

from pydantic import BaseModel

from deeploy.enums import ExplainerType, ModelType, TransformerType


class UpdateDeploymentBase(BaseModel):
    """Class that contains the base options for updating a Deployment"""

    repository_id: Optional[str] = None
    """str, optional: uuid of the Repository"""
    branch_name: Optional[str] = None
    """str, optional: the branch name of the Repository to deploy"""
    commit: Optional[str] = None
    """str, optional: the commit sha on the selected branch"""
    contract_path: Optional[str] = None
    """str, optional: relative repository subpath that contains the Deeploy contract to deploy from"""
    model_type: Optional[ModelType] = None
    """int: enum value from ModelType class"""
    explainer_type: Optional[ExplainerType] = None
    """int, optional: enum value from ExplainerType class. Defaults to 0 (no explainer)"""
    transformer_type: Optional[TransformerType] = None
    """int, optional: enum value from TransformerType class. Defaults to 0 (no transformer)"""
    model_config = {
        "protected_namespaces": (),  # For pydantic version 2x need to disable namespace protection for property model_*
    }

    def to_request_body(self) -> Dict:
        return {
            "repositoryId": self.repository_id,
            "branchName": self.branch_name,
            "commit": self.commit,
            "contractPath": self.contract_path,
            "modelType": self.model_type.value if self.model_type else None,
            "explainerType": self.explainer_type.value if self.explainer_type else None,
            "transformerType": self.transformer_type.value if self.transformer_type else None,
        }
