import warnings
from typing import Dict, List, Optional

from deeploy.enums.artifact import Artifact
from deeploy.models import (
    ActualResponse,
    ClientConfig,
    CreateActuals,
    CreateAzureMLDeployment,
    CreateDeployment,
    CreateEvaluation,
    CreateExplainerReference,
    CreateExternalDeployment,
    CreateMetadata,
    CreateModelReference,
    CreateRegistrationDeployment,
    CreateSageMakerDeployment,
    CreateTransformerReference,
    Deployment,
    Evaluation,
    GetPredictionLogsOptions,
    PredictionLog,
    UpdateAzureMLDeployment,
    UpdateDeployment,
    UpdateDeploymentDescription,
    UpdateExternalDeployment,
    UpdateRegistrationDeployment,
    UpdateSageMakerDeployment,
    V1Prediction,
    V2Prediction,
)
from deeploy.models.create_environment_variable import CreateEnvironmentVariable
from deeploy.models.create_job_schedule import CreateJobSchedule
from deeploy.models.environment_variable import EnvironmentVariable
from deeploy.models.job_schedule import JobSchedule
from deeploy.models.metadata_json import MetadataJson
from deeploy.models.prediction_log import RequestLog
from deeploy.models.reference_json import (
    ExplainerReferenceJson,
    ModelReferenceJson,
    TransformerReferenceJson,
)
from deeploy.models.test_job_schedule import TestJobSchedule
from deeploy.models.update_job_schedule import UpdateJobSchedule
from deeploy.services import (
    DeeployService,
    FileService,
    GitService,
)


class Client(object):
    """
    A class for interacting with Deeploy
    """

    def __init__(
        self,
        host: str,
        workspace_id: str,
        access_key: str = None,
        secret_key: str = None,
        deployment_token: str = None,
    ) -> None:
        """Initialise the Deeploy client
        Parameters:
            host (str): The host at which Deeploy is located, i.e. deeploy.example.com
            workspace_id (str): The ID of the workspace in which your repository
                is located
            access_key (str, optional): Personal Access Key generated from the Deeploy UI
            secret_key (str, optional): Secret Access Key generated from the Deeploy UI
            deployment_token (str, optional): Deployment token generated from the Deeploy UI
        """

        self.__config = ClientConfig(
            **{
                "host": host,
                "workspace_id": workspace_id,
                "access_key": access_key,
                "secret_key": secret_key,
                "token": deployment_token,
            }
        )

        self.__deeploy_service = DeeployService(host, access_key, secret_key, deployment_token)

        self.__file_service = FileService()

    def validate_personal_key(func):
        def _validate(self, *args, **kwargs):
            if not (self.__config.access_key and self.__config.secret_key):
                raise Exception(
                    "access_key and secret_key not found, please define them when initiating the client."
                )
            return func(self, *args, **kwargs)

        return _validate

    @validate_personal_key
    def create_environment_variable(
        self, options: CreateEnvironmentVariable
    ) -> EnvironmentVariable:
        """Create an environment variable in a Workspace"
        Parameters:
            options (CreateEnvironmentVariable): An instance of the CreateEnvironmentVariable class
                containing the environment variable configuration options
        """

        return self.__deeploy_service.create_environment_variable(
            self.__config.workspace_id, CreateEnvironmentVariable(**options)
        )

    @validate_personal_key
    def get_all_environment_variables(self) -> List[EnvironmentVariable]:
        """Get all environment variables from your Workspace"""

        return self.__deeploy_service.get_all_environment_variables(self.__config.workspace_id)

    @validate_personal_key
    def get_environment_variable_ids_for_deployment_artifact(
        self, deployment_id: str, artifact: Artifact
    ) -> List[str]:
        """Get the current environment variable IDs for an artifact of your Deployment
        This method can be used to help update your Deployment
        Parameters:
            deployment_id (str): The uuid of the Deployment of which to retrieve the environment variable IDs
            artifact (str): The artifact of which to retrieve the environment variable IDs from
        """

        return self.__deeploy_service.get_environment_variable_ids_for_deployment_artifact(
            self.__config.workspace_id, deployment_id, artifact
        )

    @validate_personal_key
    def create_deployment(
        self,
        options: CreateDeployment,
        local_repository_path: Optional[str] = None,
    ) -> Deployment:
        """Create a Deployment on Deeploy
        Parameters:
            options (CreateDeployment): An instance of the CreateDeployment class
                containing the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """

        options = self.__check_local_git_config(local_repository_path, options)

        return self.__deeploy_service.create_deployment(
            self.__config.workspace_id, CreateDeployment(**options)
        )

    @validate_personal_key
    def create_sagemaker_deployment(
        self,
        options: CreateSageMakerDeployment,
        local_repository_path: Optional[str] = None,
    ) -> Deployment:
        """Create a SageMaker Deployment on Deeploy
        Parameters:
            options (CreateSageMakerDeployment): An instance of the CreateSageMakerDeployment class
                containing the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """

        options = self.__check_local_git_config(local_repository_path, options)

        return self.__deeploy_service.create_sagemaker_deployment(
            self.__config.workspace_id, CreateSageMakerDeployment(**options)
        )

    @validate_personal_key
    def create_azure_ml_deployment(
        self,
        options: CreateAzureMLDeployment,
        local_repository_path: Optional[str] = None,
    ) -> Deployment:
        """Create an Azure Machine Learning Deployment on Deeploy
        Parameters:
            options (CreateAzureMLDeployment): An instance of the CreateAzureMLDeployment class
                containing the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """

        options = self.__check_local_git_config(local_repository_path, options)

        return self.__deeploy_service.create_azure_ml_deployment(
            self.__config.workspace_id, CreateAzureMLDeployment(**options)
        )

    @validate_personal_key
    def create_external_deployment(
        self,
        options: CreateExternalDeployment,
        local_repository_path: Optional[str] = None,
    ) -> Deployment:
        """Create a Deployment on Deeploy
        Parameters:
            options (CreateExternalDeployment): An instance of the CreateExternalDeployment class
                containing the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """

        if ("repository_id" in options) and ("branch_name" in options):
            options = self.__check_local_git_config(local_repository_path, options)
        elif ("repository_id" not in options) and ("branch_name" not in options) is None:
            pass
        else:
            raise Exception(
                "Both repository ID and branch name not provided. Either set them both null or provide both."
            )

        return self.__deeploy_service.create_external_deployment(
            self.__config.workspace_id, CreateExternalDeployment(**options)
        )

    @validate_personal_key
    def create_registration_deployment(
        self,
        options: CreateRegistrationDeployment,
        local_repository_path: Optional[str] = None,
    ) -> Deployment:
        """Create a Deployment on Deeploy
        Parameters:
            options (CreateRegistrationDeployment): An instance of the CreateRegistrationDeployment class
                containing the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """

        if ("repository_id" in options) and ("branch_name" in options):
            options = self.__check_local_git_config(local_repository_path, options)
        elif ("repository_id" not in options) and ("branch_name" not in options) is None:
            pass
        else:
            raise Exception(
                "Both repository ID and branch name not provided. Either set them both null or provide both."
            )

        return self.__deeploy_service.create_registration_deployment(
            self.__config.workspace_id, CreateRegistrationDeployment(**options)
        )

    @validate_personal_key
    def update_deployment(
        self,
        deployment_id: str,
        options: UpdateDeployment,
        local_repository_path: Optional[str] = None,
    ) -> Deployment:
        """Update a Deployment on Deeploy
        Parameters:
            deployment_id (str): The uuid of the Deployment to update
            options (UpdateDeployment): An instance of the UpdateDeployment class
                containing the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """

        current_deployment = self.__deeploy_service.get_deployment(
            self.__config.workspace_id, deployment_id
        )

        if not (current_deployment):
            raise Exception(
                "Deployment was not found in the Deeploy Workspace. \
                 Make sure the deployment_id is correct."
            )

        options = self.__check_local_git_config(local_repository_path, options)

        return self.__deeploy_service.update_deployment(
            self.__config.workspace_id, deployment_id, UpdateDeployment(**options)
        )

    @validate_personal_key
    def update_sagemaker_deployment(
        self,
        deployment_id: str,
        options: UpdateSageMakerDeployment,
        local_repository_path: Optional[str] = None,
    ) -> Deployment:
        """Update a SageMaker Deployment on Deeploy
        Parameters:
            deployment_id (str): The uuid of the Deployment to update
            options (UpdateSageMakerDeployment): An instance of the UpdateSageMakerDeployment class
                containing the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """

        current_deployment = self.__deeploy_service.get_deployment(
            self.__config.workspace_id, deployment_id
        )

        if not (current_deployment):
            raise Exception(
                "Deployment was not found in the Deeploy Workspace. \
                 Make sure the deployment_id is correct."
            )

        options = self.__check_local_git_config(local_repository_path, options)

        return self.__deeploy_service.update_sagemaker_deployment(
            self.__config.workspace_id, deployment_id, UpdateSageMakerDeployment(**options)
        )

    @validate_personal_key
    def update_azure_ml_deployment(
        self,
        deployment_id: str,
        options: UpdateAzureMLDeployment,
        local_repository_path: Optional[str] = None,
    ) -> Deployment:
        """Update an Azure Machine Learning Deployment on Deeploy
        Parameters:
            deployment_id (str): The uuid of the Deployment to update
            options (UpdateAzureMLDeployment): An instance of the UpdateAzureMLDeployment class
                containing the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """

        current_deployment = self.__deeploy_service.get_deployment(
            self.__config.workspace_id, deployment_id
        )

        if not (current_deployment):
            raise Exception(
                "Deployment was not found in the Deeploy Workspace. \
                 Make sure the deployment_id is correct."
            )

        options = self.__check_local_git_config(local_repository_path, options)

        return self.__deeploy_service.update_azure_ml_deployment(
            self.__config.workspace_id, deployment_id, UpdateAzureMLDeployment(**options)
        )

    @validate_personal_key
    def update_external_deployment(
        self,
        deployment_id: str,
        options: UpdateExternalDeployment,
        local_repository_path: Optional[str] = None,
    ) -> Deployment:
        """Update a Deployment on Deeploy
        Parameters:
            deployment_id (str): The uuid of the Deployment to update
            options (UpdateExternalDeployment): An instance of the UpdateExternalDeployment class
                containing the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """

        current_deployment = self.__deeploy_service.get_deployment(
            self.__config.workspace_id, deployment_id
        )

        if not (current_deployment):
            raise Exception(
                "Deployment was not found in the Deeploy Workspace. \
                 Make sure the deployment_id is correct."
            )

        if ("repository_id" in options and options["repository_id"] is not None) or (
            "branch_name" in options and options["branch_name"] is not None
        ):
            options = self.__check_local_git_config(local_repository_path, options)
        elif (
            "repository_id" not in options
            or ("repository_id" in options and options["repository_id"] is None)
        ) and (
            "branch_name" not in options
            or ("branch_name" in options and options["branch_name"] is None)
        ):
            pass
        else:
            raise Exception(
                "Both repository ID and branch name not provided. Either set them both null or provide both."
            )

        return self.__deeploy_service.update_external_deployment(
            self.__config.workspace_id, deployment_id, UpdateExternalDeployment(**options)
        )

    @validate_personal_key
    def update_registration_deployment(
        self,
        deployment_id: str,
        options: UpdateRegistrationDeployment,
        local_repository_path: Optional[str] = None,
    ) -> Deployment:
        """Update a Deployment on Deeploy
        Parameters:
            deployment_id (str): The uuid of the Deployment to update
            options (UpdateRegistrationDeployment): An instance of the UpdateRegistrationDeployment class
                containing the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """

        current_deployment = self.__deeploy_service.get_deployment(
            self.__config.workspace_id, deployment_id
        )

        if not (current_deployment):
            raise Exception(
                "Deployment was not found in the Deeploy Workspace. \
                 Make sure the deployment_id is correct."
            )

        if ("repository_id" in options and options["repository_id"] is not None) or (
            "branch_name" in options and options["branch_name"] is not None
        ):
            options = self.__check_local_git_config(local_repository_path, options)
        elif (
            "repository_id" not in options
            or ("repository_id" in options and options["repository_id"] is None)
        ) and (
            "branch_name" not in options
            or ("branch_name" in options and options["branch_name"] is None)
        ):
            pass
        else:
            raise Exception(
                "Both repository ID and branch name not provided. Either set them both null or provide both."
            )

        return self.__deeploy_service.update_registration_deployment(
            self.__config.workspace_id, deployment_id, UpdateRegistrationDeployment(**options)
        )

    @validate_personal_key
    def update_deployment_description(
        self, deployment_id: str, options: UpdateDeploymentDescription
    ) -> Deployment:
        """Update the description of a Deployment on Deeploy
        Parameters:
            deployment_id (str): The uuid of the Deployment to update
            options (UpdateDeploymentDescription): An instance of the UpdateDeploymentDescription class
                containing the deployment description options
        """

        current_deployment = self.__deeploy_service.get_deployment(
            self.__config.workspace_id, deployment_id
        )

        if not (current_deployment):
            raise Exception(
                "Deployment was not found in the Deeploy Workspace. \
                 Make sure the deployment_id is correct."
            )

        return self.__deeploy_service.update_deployment_description(
            self.__config.workspace_id, deployment_id, UpdateDeploymentDescription(**options)
        )

    @validate_personal_key
    def create_job_schedule(self, options: CreateJobSchedule) -> List[Dict]:
        """Create a job schedule in a Workspace"
        Parameters:
            options (CreateJobSchedule): An instance of the CreateJobSchedule class
                containing the job schedule configuration options
        """

        return self.__deeploy_service.create_job_schedule(
            self.__config.workspace_id, CreateJobSchedule(**options)
        )

    @validate_personal_key
    def test_job_schedule(self, options: TestJobSchedule) -> JobSchedule:
        """Test a job schedule in a Workspace"
        Parameters:
            options (TestJobSchedule): An instance of the TestJobSchedule class
                containing the test job schedule configuration options
        """

        return self.__deeploy_service.test_job_schedule(
            self.__config.workspace_id, TestJobSchedule(**options)
        )

    @validate_personal_key
    def update_job_schedule(self, job_schedule_id: str, options: UpdateJobSchedule) -> JobSchedule:
        """Create a job schedule in a Workspace"
        Parameters:
            job_schedule_id (str): The uuid of the job schedule to update
            options (UpdateJobSchedule): An instance of the UpdateJobSchedule class
                containing the job schedule configuration options
        """

        return self.__deeploy_service.update_job_schedule(
            self.__config.workspace_id, job_schedule_id, UpdateJobSchedule(**options)
        )

    @validate_personal_key
    def deactivate_job_schedule(self, job_schedule_id: str) -> JobSchedule:
        """Deactivate a job schedule in a Workspace"
        Parameters:
            job_schedule_id (str): The uuid of the job schedule to deactivate
        """

        return self.__deeploy_service.deactivate_job_schedule(
            self.__config.workspace_id, job_schedule_id
        )

    @validate_personal_key
    def activate_job_schedule(self, job_schedule_id: str) -> JobSchedule:
        """Activate a job schedule in a Workspace"
        Parameters:
            job_schedule_id (str): The uuid of the job schedule to activate
        """

        return self.__deeploy_service.activate_job_schedule(
            self.__config.workspace_id, job_schedule_id
        )

    def predict(self, deployment_id: str, request_body: dict) -> V1Prediction or V2Prediction:
        """Make a predict call
        Parameters:
            deployment_id (str): ID of the Deeploy deployment
            request_body (dict): Request body with input data for the model
        """

        return self.__deeploy_service.predict(
            self.__config.workspace_id, deployment_id, request_body
        )

    def explain(self, deployment_id: str, request_body: dict, image: bool = False) -> object:
        """Make an explain call
        Parameters:
            deployment_id (str): ID of the Deeploy deployment
            request_body (dict): Request body with input data for the model
            image (bool): Return image or not
        """

        return self.__deeploy_service.explain(
            self.__config.workspace_id, deployment_id, request_body, image
        )

    def get_request_logs(self, deployment_id: str) -> List[RequestLog]:
        """Retrieve request logs
        Parameters:
            deployment_id (str): ID of the Deeploy deployment
        """

        return self.__deeploy_service.get_request_logs(self.__config.workspace_id, deployment_id)

    def get_prediction_logs(
        self, deployment_id: str, params: GetPredictionLogsOptions
    ) -> List[PredictionLog]:
        """Retrieve prediction logs
        Parameters:
            deployment_id (str): ID of the Deeploy deployment
            params (GetPredictionLogsOptions): An instance of the GetPredictionLogsOptions class
                containing the params used for the retrieval of prediction logs
        """

        return self.__deeploy_service.get_prediction_logs(
            self.__config.workspace_id, deployment_id, GetPredictionLogsOptions(**params)
        )

    def get_one_prediction_log(
        self, deployment_id: str, request_log_id: str, prediction_log_id: str
    ) -> PredictionLog:
        """*** Deprecated in favor of get_prediction_logs ***

        Retrieve one prediction log
        Parameters:
            deployment_id (str): ID of the Deeploy deployment
            request_log_id (str): ID of the request_log containing the prediction
            prediction_log_id (str): ID of the prediction_log to be retrieved
        """

        return self.__deeploy_service.get_one_prediction_log(
            self.__config.workspace_id, deployment_id, request_log_id, prediction_log_id
        )

    def evaluate(
        self,
        deployment_id: str,
        prediction_log_id: str,
        evaluation_input: CreateEvaluation,
    ) -> Evaluation:
        """Evaluate a prediction log
        Parameters:
            deployment_id (str): ID of the Deeploy deployment
            log_id (int): ID of the log to be evaluated
            evaluation_input (CreateEvaluation): An instance of the CreateEvaluation class
                containing the evaluation input
        """

        return self.__deeploy_service.evaluate(
            self.__config.workspace_id,
            deployment_id,
            prediction_log_id,
            CreateEvaluation(**evaluation_input),
        )

    def upload_actuals(
        self, deployment_id: str, actuals_input: CreateActuals
    ) -> List[ActualResponse]:
        """Upload actuals for prediction logs
        Parameters:
            deployment_id (str): ID of the Deeploy deployment
            actuals_input (CreateActuals): An instance of the CreateActuals class
                containing the prediction log id's and corresponding actuals
        """

        return self.__deeploy_service.actuals(
            self.__config.workspace_id, deployment_id, CreateActuals(**actuals_input)
        )

    def generate_metadata_json(
        self, target_path: str, metadata_input: CreateMetadata
    ) -> MetadataJson:
        """Generate a metadata.json file
        Parameters:
            target_path (str): Absolute path to the directory in which the
                metadata.json should be saved.
            metadata_input (CreateMetadata): An instance of the CreateMetadata
                class containing the keys and values you would like to include
                in your metadata.json
        """

        return self.__file_service.generate_metadata_json(
            target_path, CreateMetadata(**metadata_input)
        )

    def generate_model_reference_json(
        self, target_path: str, reference_input: CreateModelReference
    ) -> ModelReferenceJson:
        """Generate a reference.json file for your model
        Parameters:
            target_path (str): Absolute path to the directory in which the
                model directory with reference.json file should be saved.
            reference_input (CreateModelReference): An instance of the CreateModelReference
                class containing the configuration options of your model
        """

        return self.__file_service.generate_reference_json(
            target_path, CreateModelReference(**reference_input)
        )

    def generate_explainer_reference_json(
        self, target_path: str, reference_input: CreateExplainerReference
    ) -> ExplainerReferenceJson:
        """Generate a reference.json file for your explainer
        Parameters:
            target_path (str): Absolute path to the directory in which the
                explainer directory with reference.json file should be saved.
            reference_input (CreateExplainerReference): An instance of the CreateExplainerReference
                class containing the configuration options of your explainer
        """

        return self.__file_service.generate_reference_json(
            target_path, CreateExplainerReference(**reference_input)
        )

    def generate_transformer_reference_json(
        self, target_path: str, reference_input: CreateTransformerReference
    ) -> TransformerReferenceJson:
        """Generate a reference.json file for your transformer
        Parameters:
            target_path (str): Absolute path to the directory in which the
                transformer directory with reference.json file should be saved.
            reference_input (CreateTransformerReference): An instance of the CreateTransformerReference
                class containing the configuration options of your transformer
        """

        return self.__file_service.generate_reference_json(
            target_path, CreateTransformerReference(**reference_input)
        )

    def __check_local_git_config(self, local_repository_path: str, options: dict) -> dict:
        """Check local Git config in repository
        Parameters:
            options (CreateDeployment, CreateSagemakerDeployment, CreateAzureMLDeployment, CreateExternalDeployment, CreateRegistrationDeployment
                     UpdateDeployment,  UpdateSagemakerDeployment, UpdateAzureMLDeployment, UpdateExternalDeployment, UpdateRegistrationDeployment):
                An instance of the CreateDeployment classcontaining the deployment configuration options
            local_repository_path (str, optional): Absolute path to the local git repository
                which is connected to Deeploy used to check if your Repository is present in the Workspace
        """
        if local_repository_path:
            git_service = GitService(local_repository_path)
            if "repository_id" in options:
                warnings.warn(
                    """The repository_id that you defined in the create_options will
                                be overwritten by the git configuration in your local_repository_path""",
                    stacklevel=2,
                )
            options["repository_id"] = self.__get_repository_id(git_service)
            if "branch_name" in options:
                warnings.warn(
                    """The branch_name that you defined in the create_options will
                                be overwritten by the git configuration in your local_repository_path""",
                    stacklevel=2,
                )
            options["branch_name"] = git_service.get_branch_name()
            if "commit" in options:
                warnings.warn(
                    """The commit that you defined in the create_options will
                                be overwritten by the git configuration in your local_repository_path""",
                    stacklevel=2,
                )
            options["commit"] = git_service.get_commit()
        else:
            if "repository_id" not in options:
                raise Exception("Missing repository_id in your create options.")
            if "branch_name" not in options:
                raise Exception("Missing branch_name in your create options.")
        return options

    def __get_repository_id(self, git_service: GitService) -> str:
        remote_url = git_service.get_remote_url()
        workspace_id = self.__config.workspace_id

        repositories = self.__deeploy_service.get_repositories(workspace_id)

        correct_repositories = list(
            filter(
                lambda x: x.remote_path == self.__parse_url_ssh_to_https(remote_url)
                or x.remote_path == remote_url,
                repositories,
            )
        )

        if len(correct_repositories) == 1:
            repository_id = correct_repositories[0].id
        else:
            raise Exception(
                "Repository ID was not found in Deeploy Workspace. \
                             Make sure you have connected it before deploying."
            )

        return repository_id

    def __parse_url_ssh_to_https(self, remote_path: str) -> str or None:
        if remote_path[:4] != "git@":
            # https to ssh
            path_tokens = remote_path.split("/")
            provider = path_tokens[2]
            user = path_tokens[3]
            path = path_tokens[4:]
            link = "git@" + provider + ":" + user
            for sub_directory in path:
                link += "/" + sub_directory
        else:
            # ssh to https
            path_tokens = remote_path.split("@")
            link = "https://" + path_tokens[1].replace(":", "/")
        return link
