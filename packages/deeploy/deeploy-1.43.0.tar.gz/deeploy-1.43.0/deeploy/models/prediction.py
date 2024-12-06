from typing import Any, List, Optional

from pydantic import BaseModel


class Prediction(BaseModel):
    pass


class V1Prediction(Prediction):
    predictions: List[Any]


class V2Prediction(Prediction):
    predictions: List[Any]
    featureLabels: Optional[List[str]] = None
    requestLogId: Optional[str] = None
    predictionLogIds: Optional[List[str]] = None
