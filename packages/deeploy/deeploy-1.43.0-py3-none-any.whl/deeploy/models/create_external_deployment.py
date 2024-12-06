from typing import Dict, Optional

from pydantic import model_validator

from deeploy.enums import DeploymentType
from deeploy.enums.external_url_authentication_method import ExternalUrlAuthenticationMethod
from deeploy.models import CreateNonStandardDeploymentBase


class CreateExternalDeployment(CreateNonStandardDeploymentBase):
    """Class that contains the options for creating a external deployment"""

    url: str
    """str, optional: url endpoint of external deployment"""
    authentication: ExternalUrlAuthenticationMethod
    """str: enum value from ExternalUrlAuthenticationMethod class."""
    username: Optional[str] = None
    """str, optional: username header for basic authentication"""
    custom_header: Optional[str] = None
    """str, optional: custom header for custom authentication"""
    password: Optional[str] = None
    """str, optional: password/bearer token/key for basic/bearer/custom authentication"""

    @model_validator(mode='before')
    def authentication_is_set(cls, values):
        if (values.get("username") is None or values.get("password") is None) and values.get("authentication") is ExternalUrlAuthenticationMethod.BASIC:
            raise ValueError(
                "when 'authentication' is ExternalUrlAuthenticationMethod.BASIC, 'username' and 'password' cannot be empty"
            )
        elif (values.get("custom_header") is None or values.get("password") is None) and values.get("authentication") is ExternalUrlAuthenticationMethod.CUSTOM:
            raise ValueError(
                "when 'authentication' is ExternalUrlAuthenticationMethod.CUSTOM, 'custom_header' and 'password' cannot be empty"
            )
        elif values.get("password") is None and values.get("authentication") is ExternalUrlAuthenticationMethod.BEARER:
            raise ValueError(
                "when 'authentication' is ExternalUrlAuthenticationMethod.BEARER, 'password' cannot be empty"
            )
        elif (values.get("username") is not None or values.get("custom_header") is not None) and values.get("authentication") is ExternalUrlAuthenticationMethod.BEARER:
            raise ValueError(
                "when 'authentication' is ExternalUrlAuthenticationMethod.BEARER, 'username' and 'custom_header' must be empty"
            )
        elif values.get("username") is not None and values.get("custom_header") is not None:
            raise ValueError(
                "'username' and 'custom_header' both cannot be set simultaneously together."
            )
        return values
    
    def to_request_body(self) -> Dict:
        request_body = {
            **super().to_request_body(deployment_type=DeploymentType.EXTERNAL),
            "url": self.url,
            "username": self.username if self.username else self.custom_header,
            "password": self.password,
            "authentication": self.authentication.value
        }
        filtered_request_body = {k: v for k, v in request_body.items() if v is not None and v != {}}
        return filtered_request_body
