from typing import Dict, Optional

from pydantic import BaseModel

from deeploy.enums.risk_classification import RiskClassification


class UpdateDeploymentDescription(BaseModel):
    """Class that contains the options for updating a model that doesn't require restarting pods"""

    name: Optional[str] = None
    """str: name of the Deployment"""
    description: Optional[str] = None
    """str, optional: the description of the Deployment"""
    risk_classification: Optional[RiskClassification] = None
    """str, optional: enum value from RiskClassification class"""

    def to_request_body(self) -> Dict:
        request_body = {
            "name": self.name,
            "description": self.description,
            "riskClassification": self.risk_classification.value
            if self.risk_classification
            else None,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        return {k: v for k, v in request_body.items() if v is not None and v != {}}
