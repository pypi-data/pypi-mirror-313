from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict

from deeploy.common.functions import to_lower_camel


class RequestLog(BaseModel):
    id: str
    team_id: str
    deployment_id: str
    commit: str
    request_content_type: str
    response_time_m_s: int
    status_code: int
    personal_keys_id: Optional[str] = None
    token_id: Optional[str] = None
    created_at: str
    prediction_logs: Optional[Dict] = None
    model_config = ConfigDict(alias_generator=to_lower_camel)


class PredictionLog(BaseModel):
    id: str
    team_id: str
    request_body: Optional[Dict] = None
    response_body: Optional[Dict] = None
    request_log: Dict
    evaluation: Optional[Dict] = None
    actual: Optional[Dict] = None
    created_at: str
    tags: Dict
    model_config = ConfigDict(alias_generator=to_lower_camel)
