import base64
from typing import Dict, List, Optional

import requests
from pydantic import TypeAdapter

from deeploy.enums import AuthType, PredictionVersion
from deeploy.enums.artifact import Artifact
from deeploy.models import (
    ActualResponse,
    CreateActuals,
    CreateAzureMLDeployment,
    CreateDeployment,
    CreateEnvironmentVariable,
    CreateEvaluation,
    CreateExternalDeployment,
    CreateRegistrationDeployment,
    CreateSageMakerDeployment,
    Deployment,
    EnvironmentVariable,
    Evaluation,
    GetPredictionLogsOptions,
    PredictionLog,
    RawEnvironmentVariable,
    Repository,
    UpdateAzureMLDeployment,
    UpdateDeployment,
    UpdateDeploymentDescription,
    UpdateExternalDeployment,
    UpdateRegistrationDeployment,
    UpdateSageMakerDeployment,
    V1Prediction,
    V2Prediction,
    Workspace,
)
from deeploy.models.create_job_schedule import CreateJobSchedule
from deeploy.models.job_schedule import JobSchedule
from deeploy.models.prediction_log import RequestLog
from deeploy.models.test_job_schedule import TestJobSchedule
from deeploy.models.update_job_schedule import UpdateJobSchedule


class DeeployService(object):
    """
    A class for interacting with the Deeploy API
    """

    request_timeout = 300

    def __init__(
        self,
        host: str,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        token: Optional[str] = None,
        insecure: Optional[bool] = False,
    ) -> None:
        self.__access_key = access_key
        self.__secret_key = secret_key
        self.__token = token
        self.__host = f"http://api.{host}" if insecure else f"https://api.{host}"

        if not (access_key and secret_key) and not token:
            raise Exception(
                "No authentication method provided. Please provide a token or personal key pair"
            )

    def get_repositories(self, workspace_id: str) -> List[Repository]:
        url = "%s/workspaces/%s/repositories" % (self.__host, workspace_id)

        repositories_response = requests.get(
            url,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        repositories = TypeAdapter(List[Repository]).validate_python(repositories_response.json())

        return repositories

    def get_repository(self, workspace_id: str, repository_id: str) -> Repository:
        url = "%s/workspaces/%s/repositories/%s" % (
            self.__host,
            workspace_id,
            repository_id,
        )

        repository_response = requests.get(
            url,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )
        if not self.__request_is_successful(repository_response):
            raise Exception("Repository does not exist in the workspace.")

        repository = TypeAdapter(Repository).validate_python(repository_response.json())

        return repository

    def create_environment_variable(
        self, workspace_id: str, environment_variable: CreateEnvironmentVariable
    ) -> EnvironmentVariable:
        url = "%s/workspaces/%s/environmentVariables" % (self.__host, workspace_id)
        data = environment_variable.to_request_body()

        environment_variable_response = requests.post(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(environment_variable_response):
            raise Exception(
                "Failed to create environment variable: %s"
                % str(environment_variable_response.json())
            )

        environment_variable = TypeAdapter(EnvironmentVariable).validate_python(
            environment_variable_response.json()["data"]
        )

        return environment_variable

    def get_all_environment_variables(self, workspace_id: str) -> List[EnvironmentVariable]:
        url = "%s/workspaces/%s/environmentVariables" % (self.__host, workspace_id)

        environment_variables_response = requests.get(
            url,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(environment_variables_response):
            raise Exception("Failed to get environment variables.")

        environment_variables = TypeAdapter(List[EnvironmentVariable]).validate_python(
            environment_variables_response.json()
        )

        return environment_variables

    def get_environment_variable_ids_for_deployment_artifact(
        self, workspace_id: str, deployment_id: str, artifact: Artifact
    ) -> List[str]:
        url = "%s/workspaces/%s/environmentVariables/raw" % (self.__host, workspace_id)
        params = {
            "deploymentId": "eq:%s" % deployment_id,
            "artifact": "eq:%s" % artifact,
        }

        environment_variables_response = requests.get(
            url,
            params=params,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(environment_variables_response):
            raise Exception("Failed to get environment variables.")

        raw_environment_variables = TypeAdapter(List[RawEnvironmentVariable]).validate_python(
            environment_variables_response.json()["data"]
        )
        environment_variable_ids = list(map(lambda env: env.id, raw_environment_variables))

        return environment_variable_ids

    def get_deployment(
        self, workspace_id: str, deployment_id: str, withExamples: bool = False
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        params = {
            "withExamples": withExamples,
        }
        deployment_response = requests.get(
            url,
            params=params,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )
        if not self.__request_is_successful(deployment_response):
            raise Exception(
                "Failed to retrieve the deployment: %s" % str(deployment_response.json())
            )

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def create_deployment(self, workspace_id: str, deployment: CreateDeployment) -> Deployment:
        url = "%s/workspaces/%s/deployments" % (self.__host, workspace_id)
        data = deployment.to_request_body()

        deployment_response = requests.post(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to create the Deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def create_sagemaker_deployment(
        self, workspace_id: str, deployment: CreateSageMakerDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments" % (self.__host, workspace_id)
        data = deployment.to_request_body()

        deployment_response = requests.post(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to create the Deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def create_azure_ml_deployment(
        self, workspace_id: str, deployment: CreateAzureMLDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments" % (self.__host, workspace_id)
        data = deployment.to_request_body()

        deployment_response = requests.post(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to create the Deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def create_external_deployment(
        self, workspace_id: str, deployment: CreateExternalDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments" % (self.__host, workspace_id)
        data = deployment.to_request_body()

        deployment_response = requests.post(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to create the Deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def create_registration_deployment(
        self, workspace_id: str, deployment: CreateRegistrationDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments" % (self.__host, workspace_id)
        data = deployment.to_request_body()

        deployment_response = requests.post(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to create the Deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def update_deployment(
        self, workspace_id: str, deployment_id: str, update: UpdateDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        data = update.to_request_body()

        deployment_response = requests.patch(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to update the Deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def update_sagemaker_deployment(
        self, workspace_id: str, deployment_id: str, update: UpdateSageMakerDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        data = update.to_request_body()

        deployment_response = requests.patch(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to update the Deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def update_azure_ml_deployment(
        self, workspace_id: str, deployment_id: str, update: UpdateAzureMLDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        data = update.to_request_body()

        deployment_response = requests.patch(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to update the Deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def update_external_deployment(
        self, workspace_id: str, deployment_id: str, update: UpdateExternalDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        data = update.to_request_body()

        deployment_response = requests.patch(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to update the Deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def update_registration_deployment(
        self, workspace_id: str, deployment_id: str, update: UpdateRegistrationDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        data = update.to_request_body()

        deployment_response = requests.patch(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to update the Deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json())

        return deployment

    def update_deployment_description(
        self, workspace_id: str, deployment_id: str, update: UpdateDeploymentDescription
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/%s/description" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        data = update.to_request_body()
        deployment_response = requests.patch(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )
        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to update the deployment: %s" % str(deployment_response.json()))

        deployment = TypeAdapter(Deployment).validate_python(deployment_response.json()["data"])

        return deployment

    def create_job_schedule(self, workspace_id: str, options: CreateJobSchedule) -> JobSchedule:
        url = "%s/workspaces/%s/jobSchedules" % (
            self.__host,
            workspace_id,
        )
        data = options.to_request_body()
        job_schedule_response = requests.post(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(job_schedule_response):
            raise Exception("Failed to create job schedule: %s" % str(job_schedule_response.json()))

        job_schedule = TypeAdapter(JobSchedule).validate_python(
            job_schedule_response.json()["data"]
        )

        return job_schedule

    def test_job_schedule(self, workspace_id: str, options: TestJobSchedule) -> List[Dict]:
        url = "%s/workspaces/%s/jobSchedules/test" % (
            self.__host,
            workspace_id,
        )
        data = options.to_request_body()
        data_response = requests.post(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(data_response):
            raise Exception("Job schedule test failed: %s" % str(data_response.json()))

        return data_response.json()

    def update_job_schedule(
        self, workspace_id: str, job_schedule_id: str, options: UpdateJobSchedule
    ) -> JobSchedule:
        url = "%s/workspaces/%s/jobSchedules/%s" % (
            self.__host,
            workspace_id,
            job_schedule_id,
        )
        data = options.to_request_body()
        job_schedule_response = requests.patch(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(job_schedule_response):
            raise Exception("Failed to update job schedule: %s" % str(job_schedule_response.json()))

        job_schedule = TypeAdapter(JobSchedule).validate_python(
            job_schedule_response.json()["data"]
        )

        return job_schedule

    def deactivate_job_schedule(self, workspace_id: str, job_schedule_id: str) -> JobSchedule:
        url = "%s/workspaces/%s/jobSchedules/%s/deactivate" % (
            self.__host,
            workspace_id,
            job_schedule_id,
        )
        job_schedule_response = requests.patch(
            url,
            json={},
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(job_schedule_response):
            raise Exception(
                "Failed to deactivate job schedule: %s" % str(job_schedule_response.json())
            )

        job_schedule = TypeAdapter(JobSchedule).validate_python(
            job_schedule_response.json()["data"]
        )

        return job_schedule

    def activate_job_schedule(self, workspace_id: str, job_schedule_id: str) -> JobSchedule:
        url = "%s/workspaces/%s/jobSchedules/%s/activate" % (
            self.__host,
            workspace_id,
            job_schedule_id,
        )
        job_schedule_response = requests.patch(
            url,
            json={},
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(job_schedule_response):
            raise Exception(
                "Failed to activate job schedule: %s" % str(job_schedule_response.json())
            )

        job_schedule = TypeAdapter(JobSchedule).validate_python(
            job_schedule_response.json()["data"]
        )

        return job_schedule

    def get_workspace(self, workspace_id: str) -> Workspace:
        url = "%s/workspaces/%s" % (self.__host, workspace_id)

        workspace_response = requests.get(
            url,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )
        if not self.__request_is_successful(workspace_response):
            raise Exception("Workspace does not exist.")

        workspace = TypeAdapter(Workspace).validate_python(workspace_response.json())

        return workspace

    def predict(self, workspace_id: str, deployment_id: str, request_body: dict) -> object:
        url = "%s/workspaces/%s/deployments/%s/predict" % (
            self.__host,
            workspace_id,
            deployment_id,
        )

        prediction_response = requests.post(
            url,
            json=request_body,
            headers=self.__get_headers(AuthType.ALL),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(prediction_response):
            raise Exception(f"Failed to call predictive model: {prediction_response.json()}")

        prediction = prediction_response.json()
        return prediction

    def explain(
        self,
        workspace_id: str,
        deployment_id: str,
        request_body: dict,
        image: bool = False,
    ) -> object:
        url = "%s/workspaces/%s/deployments/%s/explain" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        params = {
            "image": str(image).lower(),
        }

        explanation_response = requests.post(
            url,
            json=request_body,
            params=params,
            headers=self.__get_headers(AuthType.ALL),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(explanation_response):
            raise Exception(f"Failed to call explainer model: {explanation_response.json()}")

        explanation = explanation_response.json()
        return explanation

    def get_one_prediction_log(
        self,
        workspace_id: str,
        deployment_id: str,
        request_log_id: str,
        prediction_log_id: str,
    ) -> PredictionLog:
        url = "%s/workspaces/%s/deployments/%s/requestLogs/%s/predictionLogs/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
            request_log_id,
            prediction_log_id,
        )

        log_response = requests.get(
            url,
            headers=self.__get_headers(AuthType.ALL),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(log_response):
            raise Exception("Failed to get log %s." % prediction_log_id)

        log = TypeAdapter(PredictionLog).validate_python(log_response.json())
        return log

    def get_prediction_logs(
        self, workspace_id: str, deployment_id: str, params: GetPredictionLogsOptions
    ) -> List[PredictionLog]:
        url = "%s/workspaces/%s/deployments/%s/predictionLogs" % (
            self.__host,
            workspace_id,
            deployment_id,
        )

        logs_response = requests.get(
            url,
            params=params.to_params(),
            headers=self.__get_headers(AuthType.ALL),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(logs_response):
            raise Exception("Failed to get logs.")

        logs = TypeAdapter(List[PredictionLog]).validate_python(logs_response.json())
        return logs

    def get_request_logs(self, workspace_id: str, deployment_id: str) -> List[RequestLog]:
        url = "%s/workspaces/%s/deployments/%s/requestLogs" % (
            self.__host,
            workspace_id,
            deployment_id,
        )

        logs_response = requests.get(
            url,
            headers=self.__get_headers(AuthType.ALL),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(logs_response):
            raise Exception("Failed to get logs.")

        logs = TypeAdapter(List[RequestLog]).validate_python(logs_response.json())
        return logs

    def evaluate(
        self,
        workspace_id: str,
        deployment_id: str,
        prediction_log_id: str,
        evaluation_input: CreateEvaluation,
    ) -> Evaluation:
        url = "%s/workspaces/%s/deployments/%s/predictionLogs/%s/evaluatePrediction" % (
            self.__host,
            workspace_id,
            deployment_id,
            prediction_log_id,
        )

        if evaluation_input.agree is True and ("desired_output" in evaluation_input):
            raise Exception(
                "A desired_output can not be provided when agreeing with the inference."
            )

        data = evaluation_input.to_request_body()
        evaluation_response = requests.post(
            url,
            json=data,
            headers=self.__get_headers(AuthType.TOKEN),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(evaluation_response):
            if evaluation_response.status_code == 409:
                raise Exception("Log has already been evaluated.")
            elif evaluation_response.status_code in (401, 403):
                raise Exception("No permission to perform this action.")
            else:
                raise Exception(
                    "Failed to request evaluation. Response code: %s"
                    % evaluation_response.status_code
                )

        evaluation = TypeAdapter(Evaluation).validate_python(evaluation_response.json())
        return evaluation

    def actuals(
        self, workspace_id: str, deployment_id: str, actuals_input: CreateActuals
    ) -> List[ActualResponse]:
        url = "%s/workspaces/%s/deployments/%s/actuals" % (
            self.__host,
            workspace_id,
            deployment_id,
        )

        data = actuals_input.to_request_body()
        actuals_response = requests.put(
            url,
            json=data,
            headers=self.__get_headers(AuthType.TOKEN),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(actuals_response):
            if actuals_response.status_code == 401:
                raise Exception("No permission to perform this action.")
            else:
                raise Exception("Failed to submit actuals.")

        actuals = TypeAdapter(List[ActualResponse]).validate_python(actuals_response.json())
        return actuals

    def __request_is_successful(self, request: requests.Response) -> bool:
        if str(request.status_code)[0] == "2":
            return True
        return False

    def __check_prediction_version(self, prediction_response: dict) -> PredictionVersion:
        if len(prediction_response.json()) > 1:
            return PredictionVersion.V2
        else:
            return PredictionVersion.V1

    def __parse_prediction(self, prediction_response: dict) -> V1Prediction or V2Prediction:
        if self.__check_prediction_version(prediction_response) == PredictionVersion.V1:
            prediction = TypeAdapter(V1Prediction).validate_python(prediction_response.json())
        else:
            prediction = TypeAdapter(V2Prediction).validate_python(prediction_response.json())
        return prediction

    def __get_headers(self, supported_auth: AuthType):
        headers = {}
        if (self.__access_key and self.__secret_key) and (
            supported_auth == AuthType.BASIC or supported_auth == AuthType.ALL
        ):
            credentials = self.__access_key + ":" + self.__secret_key
            b64Val = base64.b64encode(credentials.encode()).decode()
            headers["Authorization"] = "Basic %s" % b64Val
        elif (self.__token) and (
            supported_auth == AuthType.TOKEN or supported_auth == AuthType.ALL
        ):
            headers["Authorization"] = "Bearer " + self.__token
        elif (self.__access_key and self.__secret_key) and not (
            supported_auth == AuthType.BASIC or supported_auth == AuthType.ALL
        ):
            raise Exception("This function currently does not support Basic authentication.")
        else:
            raise Exception("This function currently does not support Token authentication.")

        return headers
