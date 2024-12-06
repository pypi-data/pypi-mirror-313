from typing import Dict, List, Optional

from pydantic import BaseModel

from deeploy.models.feature import Feature


class CreateMetadata(BaseModel):
    """Class that contains the options for creating a metadata.json"""

    features: Optional[List[Feature]] = None
    """List, optional: list of features"""
    prediction_classes: Optional[dict] = None
    """dict, optional: dict to map class labels to values,
        class label : value as deployment metadata"""
    problem_type: Optional[str] = None
    """str, optional: model problem type classification or regression"""
    example_input: Optional[dict] = None
    """dict, optional: example of a json input that can be consumed by the model"""
    example_output: Optional[dict] = None
    """dict, optional: example of a json output that can be given back by the model"""
    input_tensor_shape: Optional[str] = None
    """str, optional: the tensor dimensions of the json input that can be consumed by the model"""
    output_tensor_shape: Optional[str] = None
    """str, optional: the tensor dimensions of the json output that can be given back by the model"""
    custom_id: Optional[str] = None
    """str: name of the custom id"""

    def map_to_lower_camel(self) -> Dict:
        request_body = {
            "features": list(map(lambda x: self.__map_feature_to_lower_camel(x), self.features))
            if self.features
            else None,
            "predictionClasses": self.prediction_classes,
            "problemType": self.problem_type,
            "exampleInput": self.example_input,
            "exampleOutput": self.example_output,
            "inputTensorShape": self.input_tensor_shape,
            "outputTensorShape": self.output_tensor_shape,
            "customId": self.custom_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        return {k: v for k, v in request_body.items() if v is not None and v != {}}

    def __map_feature_to_lower_camel(self, feature: Feature) -> Dict:
        mapped_feature = {"name": feature.name}

        if feature.observed_min is not None:
            mapped_feature["observedMin"] = feature.observed_min
        if feature.observed_max is not None:
            mapped_feature["observedMax"] = feature.observed_max

        return mapped_feature
