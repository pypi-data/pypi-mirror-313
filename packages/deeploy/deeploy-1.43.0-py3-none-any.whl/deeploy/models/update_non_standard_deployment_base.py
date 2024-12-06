from typing import Dict, Optional

from pydantic import BaseModel


class UpdateNonStandardDeploymentBase(BaseModel):
    """Class that contains the base options for updating a Deployment"""

    repository_id: Optional[str] = None
    """str, optional: uuid of the Repository"""
    branch_name: Optional[str] = None
    """str, optional: the branch name of the Repository to deploy"""
    commit: Optional[str] = None
    """str, optional: the commit sha on the selected branch"""
    contract_path: Optional[str] = None
    """str, optional: relative repository subpath that contains the Deeploy contract to deploy from"""

    def to_request_body(self) -> Dict:
        return {
            "repositoryId": self.repository_id,
            "branchName": self.branch_name,
            "commit": self.commit,
            "contractPath": self.contract_path,
        }
