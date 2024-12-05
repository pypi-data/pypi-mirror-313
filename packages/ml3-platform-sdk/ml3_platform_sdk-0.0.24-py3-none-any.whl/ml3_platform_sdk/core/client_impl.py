import json
import logging
import os
import sys
import time
from typing import Any, TypeVar

from pydantic import TypeAdapter
from requests import Response
from tabulate import tabulate

from ml3_platform_sdk.core.connection import Connection
from ml3_platform_sdk.core.enums import (
    DataCategory,
    HTTPMethod,
    RawDataSourceType,
)
from ml3_platform_sdk.core.requests import (
    AddHistoricalRequest,
    AddKPIDataRequest,
    AddProductionRequest,
    AddTargetRequest,
    AddUserProjectRoleRequest,
    AzureSPCredentials,
    ChangeCompanyOwnerRequest,
    ChangeUserCompanyRoleRequest,
    ComputeLlmSecurityReportRequest,
    ComputeRagEvaluationReportRequest,
    ComputeRetrainingReportRequest,
    ComputeTopicModelingReportRequest,
    CreateApiKeyRequest,
    CreateAWSCompatibleIntegrationCredentialsRequest,
    CreateAWSIntegrationCredentialsRequest,
    CreateAzureIntegrationCredentialsRequest,
    CreateCompanyRequest,
    CreateCompanyUserRequest,
    CreateDataSchemaRequest,
    CreateDetectionEventRuleRequest,
    CreateGCPIntegrationCredentialsRequest,
    CreateKPIRequest,
    CreateLLMSpecsRequest,
    CreateModelRequest,
    CreateProjectRequest,
    CreateTaskRequest,
    CreateUserApiRequest,
    DataInfo,
    DeleteApiKeyRequest,
    DeleteCompanyUserRequest,
    DeleteUserApiKeyRequest,
    DeleteUserProjectRoleRequest,
    EmbeddingDataInfo,
    GCPAccountInfo,
    GetDataSchemaRequest,
    GetDataSchemaTemplateRequest,
    GetJobRequest,
    GetKPIRequest,
    GetKPIsRequest,
    GetModelRequest,
    GetModelsRequest,
    GetMonitoringStatusRequest,
    GetPresignedUrlRequest,
    GetRetrainingReportRequest,
    GetSuggestionsRequest,
    GetTaskRequest,
    GetTasksRequest,
    GetUserApiRequest,
    ImageDataInfo,
    LocalDataSourceInfo,
    RemoteDataSourceInfo,
    RetrainModelRequest,
    SetLlmSpecs,
    SetModelReferenceRequest,
    SetModelSuggestionTypeRequest,
    SetTaskDetectionEventUserFeedback,
    TabularDataInfo,
    TestRetrainTriggerRequest,
    TextDataInfo,
    UpdateCompanyRequest,
    UpdateDetectionEventRuleRequest,
    UpdateModelVersionBySuggestionIDRequest,
    UpdateModelVersionFromTimeRangeRequest,
    UpdateModelVersionRequest,
    UpdateProjectRequest,
    UpdateTaskRequest,
)
from ml3_platform_sdk.core.responses import (
    GetPresignedUrlResponse,
    StandardErrorResponse,
)
from ml3_platform_sdk.enums import (
    ApiKeyExpirationTime,
    DataStructure,
    DetectionEventSeverity,
    DetectionEventType,
    ExternalIntegration,
    FileType,
    FolderType,
    JobStatus,
    ModelMetricName,
    MonitoringMetric,
    MonitoringTarget,
    SemanticSegTargetType,
    StoragePolicy,
    StoringDataType,
    SuggestionType,
    TaskType,
    TextLanguage,
    UserCompanyRole,
    UserProjectRole,
)
from ml3_platform_sdk.exceptions import (
    AddDataSchemaException,
    AddHistoricalDataException,
    AddKPIDataException,
    AddProductionDataException,
    AddTargetDataException,
    ComputeLlmSecurityReportException,
    ComputeRagEvaluationReportException,
    ComputeRetrainingReportException,
    ComputeTopicModelingReportException,
    CreateCompanyException,
    CreateDetectionEventRuleException,
    CreateKPIException,
    CreateLLMSpecsException,
    CreateModelException,
    CreateProjectException,
    CreateTaskException,
    GetAllLLMSpecsException,
    GetLlmSecurityReportException,
    GetRagEvaluationReportException,
    GetRetrainingReportException,
    GetTopicModelingReportException,
    InvalidActionList,
    JobFailureException,
    JobNotFoundException,
    JobWaitTimeoutException,
    SDKClientException,
    SetLLMSpecsException,
    SetModelReferenceException,
    SetModelSuggestionTypeException,
    UpdateCompanyException,
    UpdateDetectionEventRuleException,
    UpdateModelVersionException,
    UpdateProjectException,
    UpdateTaskException,
)
from ml3_platform_sdk.models import (
    KPI,
    ApiKey,
    AWSCompatibleCredentials,
    AWSCredentials,
    AzureBlobDataSource,
    AzureCredentials,
    Company,
    CompanyUser,
    Data,
    DataSchema,
    DetectionEvent,
    DetectionEventAction,
    DetectionEventRule,
    EmbeddingData,
    GCPCredentials,
    GCSDataSource,
    ImageData,
    IntegrationCredentials,
    Job,
    LLMSpecs,
    LocalDataSource,
    Model,
    MonitoringQuantityStatus,
    Project,
    RemoteDataSource,
    RetrainAction,
    RetrainingReport,
    RetrainTrigger,
    S3DataSource,
    SecretAWSCredentials,
    SubscriptionPlanInfo,
    SuggestionInfo,
    TabularData,
    Task,
    TaskCostInfoUnion,
    TaskLlmSecReportItem,
    TaskRagEvalReportItem,
    TaskTopicModelingReportDetails,
    TaskTopicModelingReportItem,
    TextData,
)
from ml3_platform_sdk.utils import create_file_hash

logger = logging.getLogger("ML3_PLATFORM_SDK")
logging.basicConfig(level=logging.INFO)

T = TypeVar("T", bound=SDKClientException)


class ML3PlatformClientImpl:
    """
    Client implementation for interacting with ML3Platform APIs
    """

    connection: Connection | None = None
    allowed_remote_data_sources = [
        S3DataSource,
        GCSDataSource,
        AzureBlobDataSource,
    ]

    def __init__(self, url: str, api_key: str, timeout: int = 60):
        if len(url) > 0 and len(api_key) > 0:
            self.connection = Connection(url, api_key)
            logger.info("Client Initialized")

        self.timeout = timeout

    def _api_call(
        self,
        method: HTTPMethod,
        path: str,
        exception_class: type[SDKClientException],
        json_payload: str | None = None,
        params: dict | None = None,
    ) -> Response:
        """
        Private method to make API calls
        """

        if self.connection is None or not self.connection.initialized:
            logger.info("***ERROR***")
            logger.info("Client NOT INITIALIZED check api_key and url")
            sys.exit(1)

        response = self.connection.send_api_request(
            method=method,
            path=path,
            timeout=self.timeout,
            params=params if method == HTTPMethod.GET else None,
            data=None if method == HTTPMethod.GET else json_payload,
        )

        # If the current task is running other operations
        # the api calls may return 503 error indicating
        # that at the moment the system is busy
        if response.status_code == 401:
            raise SDKClientException(
                error_code="UNAUTHORIZED", error_message="Unauthorized"
            )
        if response.status_code != 200:
            self._default_exception_handler(response, exception_class)

        return response

    @staticmethod
    def _validate_remote_source(
        data_source: RemoteDataSource,
        error_code: str,
        error_type: type[SDKClientException],
    ) -> tuple[str, RawDataSourceType]:
        """
        Validates that the remote data source is allowed, or it raises
        an exception.
        """

        if isinstance(data_source, S3DataSource):
            path = data_source.object_path

            if not path.lower().endswith(".csv"):
                raise error_type(
                    error_code=error_code,
                    error_message="Format not valid, currently only CSV "
                    "files are supported",
                )

            return path, RawDataSourceType.AWS_S3

        elif isinstance(data_source, GCSDataSource):
            path = data_source.object_path

            if not path.lower().endswith(".csv"):
                raise error_type(
                    error_code=error_code,
                    error_message="Format not valid, currently only CSV "
                    "files are supported",
                )

            return path, RawDataSourceType.GCS

        elif isinstance(data_source, AzureBlobDataSource):
            path = data_source.object_path

            if not path.lower().endswith(".csv"):
                raise error_type(
                    error_code=error_code,
                    error_message="Format not valid, currently only CSV "
                    "files are supported",
                )

            return path, RawDataSourceType.ABS

        raise NotImplementedError(
            f"Data source of type {type(data_source).__name__} "
            f"not implemented"
        )

    def _get_presigned_url_and_send_data(
        self,
        data_path: str,
        task_id: str | None,
        data_structure: DataStructure,
        storing_data_type: StoringDataType,
        data_category: DataCategory | None,
        file_type: FileType,
        folder_type: FolderType | None,
        is_folder: bool,
        project_id: str | None = None,
        model_id: str | None = None,
        kpi_id: str | None = None,
    ) -> GetPresignedUrlResponse:
        _, file_name = os.path.split(data_path)

        file_digest = create_file_hash(data_path)

        payload: GetPresignedUrlRequest = GetPresignedUrlRequest(
            project_id=project_id,
            task_id=task_id,
            data_structure=data_structure.value,
            storing_data_type=storing_data_type.value,
            file_name=file_name,
            file_type=file_type.value,
            file_checksum=file_digest,
            data_category=None
            if data_category is None
            else data_category.value,
            model_id=model_id,
            kpi_id=kpi_id,
            is_folder=is_folder,
            folder_type=folder_type.value if folder_type is not None else None,
        )

        get_presigned_url_response = self._get_presigned_url(payload.dict())

        self._send_data(
            data_path=data_path,
            get_presigned_url_response=get_presigned_url_response,
        )

        return get_presigned_url_response

    @staticmethod
    def _default_exception_handler(response, exception_type: type[T]) -> None:
        response_model = StandardErrorResponse.model_validate_json(
            response.content
        )

        ML3PlatformClientImpl._log_error(
            error_code=response_model.error_code,
            error_message=response_model.error_message,
        )

        raise exception_type(
            error_code=response_model.error_code,
            error_message=response_model.error_message,
        )

    @staticmethod
    def _log_error(error_code: str, error_message: str):
        logger.error("%s - %s", error_code, error_message)

    @staticmethod
    def _print_table(items: list[Any], headers: list[str]):
        """
        Utility method to print
        """
        logger.info(
            "\n%s",
            tabulate(
                tabular_data=[list(dict(j).values()) for j in items],
                headers=headers,
            ),
        )

    def _get_presigned_url(self, payload: dict) -> GetPresignedUrlResponse:
        get_presigned_url_raw_response = self._api_call(
            method=HTTPMethod.GET,
            path="/data/presigned-url",
            params=payload,
            exception_class=SDKClientException,
        )
        return GetPresignedUrlResponse.model_validate_json(
            get_presigned_url_raw_response.content
        )

    @classmethod
    def _send_data(
        cls,
        data_path: str,
        get_presigned_url_response: GetPresignedUrlResponse,
    ):
        send_data_raw_response = Connection.send_data(
            presigned_url=get_presigned_url_response.presigned_url,
            data_path=data_path,
        )

        if send_data_raw_response.status_code != 204:
            error_code = "SKD_CLIENT_UPLOAD_DATA_ERROR"
            error_message = "Error uploading data remotely"
            cls._log_error(error_code=error_code, error_message=error_message)
            raise SDKClientException(
                error_code=error_code, error_message=error_message
            )

    def _process_data(
        self,
        task_id: str | None,
        project_id: str | None,
        data: Data | None,
        storing_data_type: StoringDataType,
        data_category: DataCategory | None,
        mapping_data_category: DataCategory | None,
        embedding_data_category: DataCategory | None,
        model_id: str | None,
        kpi_id: str | None,
    ) -> DataInfo | None:
        """
        Process data object by returning its data info.
        """
        if data is None:
            return None

        # process source and then if it is unstructured the mapping as
        # well

        def build_source_info(
            source,
            source_data_category: DataCategory | None,
            data_structure: DataStructure,
        ) -> LocalDataSourceInfo | RemoteDataSourceInfo:
            if isinstance(source, LocalDataSource):
                data_presigned_url: GetPresignedUrlResponse = (
                    self._get_presigned_url_and_send_data(
                        data_path=source.file_path,
                        task_id=task_id,
                        data_structure=data_structure,
                        storing_data_type=storing_data_type,
                        data_category=source_data_category,
                        model_id=model_id,
                        file_type=source.file_type,
                        is_folder=source.is_folder,
                        folder_type=source.folder_type,
                        project_id=project_id,
                        kpi_id=kpi_id,
                    )
                )
                return LocalDataSourceInfo(
                    storing_process_id=data_presigned_url.storing_process_id
                )
            elif isinstance(source, RemoteDataSource):
                return RemoteDataSourceInfo(
                    file_type=source.file_type,
                    data_source_type=source.get_source_type(),
                    remote_path=source.get_path(),
                    is_folder=source.is_folder,
                    folder_type=source.folder_type,
                    credentials_id=source.credentials_id,
                    storage_policy=source.storage_policy,
                )
            else:
                raise ValueError(f"Unknown class for {data}")

        if isinstance(data, TabularData):
            return TabularDataInfo(
                data_structure=data.data_structure,
                source=build_source_info(
                    data.source,
                    source_data_category=data_category,
                    data_structure=DataStructure.TABULAR,
                ),
            )
        elif isinstance(data, EmbeddingData):
            return EmbeddingDataInfo(
                data_structure=data.data_structure,
                source=build_source_info(
                    data.source,
                    source_data_category=data_category,
                    data_structure=DataStructure.EMBEDDING,
                ),
            )
        elif isinstance(data, ImageData):
            return ImageDataInfo(
                source=build_source_info(
                    data.source,
                    source_data_category=data_category,
                    data_structure=data.data_structure,
                ),
                mapping_source=build_source_info(
                    data.mapping_source,
                    source_data_category=mapping_data_category,
                    data_structure=DataStructure.TABULAR,
                ),
                embedding_source=build_source_info(
                    data.embedding_source,
                    source_data_category=embedding_data_category,
                    data_structure=DataStructure.EMBEDDING,
                )
                if data.embedding_source is not None
                else None,
            )
        elif isinstance(data, TextData):
            return TextDataInfo(
                source=build_source_info(
                    data.source,
                    source_data_category=data_category,
                    data_structure=data.data_structure,
                ),
                embedding_source=build_source_info(
                    data.embedding_source,
                    source_data_category=embedding_data_category,
                    data_structure=DataStructure.EMBEDDING,
                )
                if data.embedding_source is not None
                else None,
            )
        else:
            raise ValueError(f"Unknown data class for {data}")

    def create_company(self, name: str, address: str, vat: str) -> str:
        """
        create_company implementation
        """
        payload = CreateCompanyRequest(name=name, address=address, vat=vat)

        response = self._api_call(
            method=HTTPMethod.POST,
            path="/company",
            json_payload=payload.model_dump_json(),
            exception_class=CreateCompanyException,
        )
        return response.json()

    def get_company(self) -> Company:
        """
        get_company implementation
        """

        response = self._api_call(
            method=HTTPMethod.GET,
            path="/company",
            exception_class=SDKClientException,
        )

        return Company.model_validate_json(response.content)

    def update_company(
        self, name: str | None, address: str | None, vat: str | None
    ) -> None:
        """
        update_company implementation
        """
        payload = UpdateCompanyRequest(name=name, address=address, vat=vat)
        self._api_call(
            method=HTTPMethod.PATCH,
            path="/company",
            json_payload=payload.model_dump_json(),
            exception_class=UpdateCompanyException,
        )

    def get_all_company_subscription_plans(self) -> list[SubscriptionPlanInfo]:
        """
        get_all_company_subscription_plans implementation
        """
        response = self._api_call(
            method=HTTPMethod.GET,
            path="/company/subscriptions",
            exception_class=SDKClientException,
        )

        adapter = TypeAdapter(list[SubscriptionPlanInfo])
        return adapter.validate_python(response.json())

    def get_active_subscription_plan(self) -> SubscriptionPlanInfo | None:
        """
        get_active_subscription_plan implementation
        """
        response = self._api_call(
            method=HTTPMethod.GET,
            path="/company/current-subscription",
            exception_class=SDKClientException,
        )

        if response.json() is None:
            return None
        else:
            return SubscriptionPlanInfo.model_validate_json(response.content)

    def create_project(
        self,
        name: str,
        description: str | None,
        default_storage_policy: StoragePolicy,
    ) -> str:
        """
        create_project implementation
        """
        payload = CreateProjectRequest(
            name=name,
            description=description,
            default_storage_policy=default_storage_policy,
        )

        response = self._api_call(
            method=HTTPMethod.POST,
            path="/project",
            json_payload=payload.model_dump_json(),
            exception_class=CreateProjectException,
        )

        return response.json()

    def get_projects(self) -> list[Project]:
        """
        get_projects implementation
        """
        response = self._api_call(
            method=HTTPMethod.GET,
            path="/projects",
            exception_class=SDKClientException,
        )

        adapter = TypeAdapter(list[Project])
        return adapter.validate_python(response.json())

    def get_project(self, project_id: str) -> Project:
        """
        get_project implementation
        """
        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/project/{project_id}",
            exception_class=SDKClientException,
        )
        return Project.model_validate_json(response.content)

    def update_project(
        self,
        project_id: str,
        name: str | None,
        description: str | None,
        default_storage_policy: StoragePolicy | None,
    ) -> None:
        """
        update_project implementation
        """
        payload = UpdateProjectRequest(
            project_id=project_id,
            name=name,
            description=description,
            default_storage_policy=default_storage_policy,
        )

        self._api_call(
            method=HTTPMethod.PATCH,
            path="/project",
            json_payload=payload.model_dump_json(),
            exception_class=UpdateProjectException,
        )

    def show_projects(self) -> None:
        """
        show_projects implementation
        """
        projects = self.get_projects()

        self._print_table(items=projects, headers=["Project Id", "Name"])

    def create_task(
        self,
        project_id: str,
        name: str,
        tags: list[str],
        task_type: TaskType,
        data_structure: DataStructure,
        cost_info: TaskCostInfoUnion | None = None,
        optional_target: bool = False,
        text_language: TextLanguage | None = None,
        positive_class: str | int | bool | None = None,
        rag_contexts_separator: str | None = None,
        llm_default_answer: str | None = None,
        semantic_segmentation_target_type: (
            SemanticSegTargetType | None
        ) = None,
    ) -> str:
        """
        create_task implementation
        """
        payload = CreateTaskRequest(
            project_id=project_id,
            name=name,
            tags=tags,
            task_type=task_type,
            data_structure=data_structure,
            cost_info=cost_info,
            optional_target=optional_target,
            text_language=text_language,
            positive_class=positive_class,
            rag_contexts_separator=rag_contexts_separator,
            llm_default_answer=llm_default_answer,
            semantic_segmentation_target_type=semantic_segmentation_target_type,
        )

        response = self._api_call(
            method=HTTPMethod.POST,
            path="/task",
            json_payload=payload.model_dump_json(),
            exception_class=CreateTaskException,
        )
        return response.json()

    def update_task(
        self,
        task_id: str,
        name: str | None = None,
        tags: list[str] | None = None,
        cost_info: TaskCostInfoUnion | None = None,
    ):
        """
        Update task attributes.
        """
        payload = UpdateTaskRequest(
            task_id=task_id,
            name=name,
            tags=tags,
            cost_info=cost_info,
        )

        self._api_call(
            method=HTTPMethod.PATCH,
            path="/task",
            json_payload=payload.model_dump_json(),
            exception_class=UpdateTaskException,
        )

    def get_tasks(self, project_id: str) -> list[Task]:
        """
        get_tasks implementation
        """
        payload = GetTasksRequest(project_id=project_id)

        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/tasks/{payload.project_id}",
            exception_class=SDKClientException,
        )

        adapter = TypeAdapter(list[Task])
        return adapter.validate_python(response.json())

    def get_task(self, task_id: str) -> Task:
        """
        get_task implementation
        """
        payload = GetTaskRequest(task_id=task_id)

        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/task/{payload.task_id}",
            exception_class=SDKClientException,
        )

        return Task.model_validate_json(response.content)

    def show_tasks(self, project_id: str):
        """
        show_tasks implementation
        """
        tasks = self.get_tasks(project_id)

        self._print_table(
            items=tasks,
            headers=["Task Id", "Name", "Type", "Status", "Status start date"],
        )

    def create_model(
        self,
        task_id: str,
        name: str,
        version: str,
        with_probabilistic_output: bool,
        metric_name: ModelMetricName | None,
        preferred_suggestion_type: SuggestionType | None = None,
        retraining_cost: float = 0.0,
        resampled_dataset_size: int | None = None,
    ) -> str:
        """
        create_model implementation
        """

        payload: CreateModelRequest = CreateModelRequest(
            task_id=task_id,
            name=name,
            version=version,
            metric_name=metric_name.value if metric_name is not None else None,
            retraining_cost=retraining_cost,
            preferred_suggestion_type=preferred_suggestion_type.value
            if preferred_suggestion_type is not None
            else None,
            resampled_dataset_size=resampled_dataset_size,
            with_probabilistic_output=with_probabilistic_output,
        )

        response = self._api_call(
            method=HTTPMethod.POST,
            path="/model",
            json_payload=payload.model_dump_json(),
            exception_class=CreateModelException,
        )
        return response.json()

    def create_llm_specs(
        self,
        model_id: str,
        from_timestamp: list[float],
        to_timestamp: list[float],
        llm: str | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        top_k: int | None = None,
        max_tokens: int | None = 256,
        role: str | None = None,
        task: str | None = None,
        behavior_guidelines: list[str] | None = None,
        security_guidelines: list[str] | None = None,
    ) -> str:
        """
        create_llm_specs implementation
        """
        if behavior_guidelines is None:
            behavior_guidelines = []
        if security_guidelines is None:
            security_guidelines = []
        payload: CreateLLMSpecsRequest = CreateLLMSpecsRequest(
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
            llm=llm,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_tokens=max_tokens,
            role=role,
            task=task,
            behavior_guidelines=behavior_guidelines,
            security_guidelines=security_guidelines,
        )

        response = self._api_call(
            method=HTTPMethod.POST,
            path=f"/model/{model_id}/llm-specs",
            json_payload=payload.model_dump_json(),
            exception_class=CreateLLMSpecsException,
        )
        return response.json()

    def get_all_llm_specs(
        self,
        model_id: str,
    ) -> list[LLMSpecs]:
        """
        get_all_llm_specs implementation
        """
        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/model/{model_id}/all-llm-specs",
            json_payload=None,
            exception_class=GetAllLLMSpecsException,
        )

        adapter = TypeAdapter(list[LLMSpecs])
        return adapter.validate_python(response.json())

    def set_llm_specs(
        self,
        model_id: str,
        llm_specs_id: str,
        starting_timestamp: float,
    ):
        """
        set_llm_specs implementation
        """

        payload = SetLlmSpecs(
            starting_timestamp=starting_timestamp,
        )

        self._api_call(
            method=HTTPMethod.PATCH,
            path=f"/model/{model_id}/llm-specs/{llm_specs_id}",
            json_payload=payload.model_dump_json(),
            exception_class=SetLLMSpecsException,
        )

    def set_model_suggestion_type(
        self,
        model_id: str,
        preferred_suggestion_type: SuggestionType,
        resampled_dataset_size: int | None = None,
    ):
        """
        update_model_info implementation
        """

        payload: SetModelSuggestionTypeRequest = SetModelSuggestionTypeRequest(
            model_id=model_id,
            preferred_suggestion_type=preferred_suggestion_type.value,
            resampled_dataset_size=resampled_dataset_size,
        )

        self._api_call(
            method=HTTPMethod.PUT,
            path="/model/suggestion-type",
            json_payload=payload.model_dump_json(),
            exception_class=SetModelSuggestionTypeException,
        )

    def get_models(self, task_id: str) -> list[Model]:
        """
        get_models implementation
        """
        payload = GetModelsRequest(task_id=task_id)

        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/models/{payload.task_id}",
            exception_class=SDKClientException,
        )

        adapter = TypeAdapter(list[Model])
        return adapter.validate_python(response.json())

    def get_model_by_name_and_version(
        self, task_id: str, model_name: str, model_version: str
    ) -> Model:
        """
        get_model_id implementation
        """

        models: list[Model] = self.get_models(task_id=task_id)

        for model in models:
            if model.name == model_name and model.version == model_version:
                return model

        raise SDKClientException(
            error_code="MODEL_NOT_FOUND",
            error_message=f"No model found with name: {model_name} and version: {model_version}",
        )

    def update_model_version_by_suggestion_id(
        self, model_id: str, new_model_version: str, suggestion_id: str
    ) -> str:
        """
        update_model_version_by_suggestion_id implementation
        """
        payload = UpdateModelVersionBySuggestionIDRequest(
            model_id=model_id,
            new_model_version=new_model_version,
            suggestion_id=suggestion_id,
        )

        response = self._api_call(
            method=HTTPMethod.PATCH,
            path="/model-version-suggestion-id",
            json_payload=payload.model_dump_json(),
            exception_class=UpdateModelVersionException,
        )

        return response.json()

    def update_model_version(
        self, model_id: str, new_model_version: str
    ) -> str:
        """
        update_model_version_by_suggestion_id implementation
        """
        payload = UpdateModelVersionRequest(
            model_id=model_id,
            new_model_version=new_model_version,
        )

        response = self._api_call(
            method=HTTPMethod.PATCH,
            path="/model-version",
            json_payload=payload.model_dump_json(),
            exception_class=UpdateModelVersionException,
        )

        return response.json()

    def update_model_version_from_time_range(
        self,
        model_id: str,
        new_model_version: str,
        from_timestamp: float,
        to_timestamp: float,
    ) -> str:
        """
        update_model_version_from_raw_data implementation
        """
        model = self.get_model(model_id=model_id)
        if model is None:
            raise UpdateModelVersionException(
                error_code="UPDATE_MODEL_REFERENCE_FROM_TIME_RANGE_MODEL_ERROR",
                error_message="Model not found",
            )
        payload = UpdateModelVersionFromTimeRangeRequest(
            model_id=model_id,
            new_model_version=new_model_version,
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
        )

        response = self._api_call(
            method=HTTPMethod.PATCH,
            path="/model-version-time-range",
            json_payload=payload.model_dump_json(),
            exception_class=UpdateModelVersionException,
        )
        return response.json()

    def get_model(self, model_id: str) -> Model:
        """
        get_model implementation
        """
        payload = GetModelRequest(model_id=model_id)

        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/model/{payload.model_id}",
            exception_class=UpdateModelVersionException,
        )

        return Model.model_validate_json(response.content)

    def show_models(self, task_id: str) -> None:
        """
        show_models implementation
        """

        models = self.get_models(task_id=task_id)

        self._print_table(
            models,
            [
                "Model Id",
                "Task Id",
                "Name",
                "Version",
                "Status",
                "Status start timestamp",
                "Status insert date",
                "Metric Name",
            ],
        )

    def get_suggestions_info(
        self, model_id: str, model_version: str
    ) -> list[SuggestionInfo]:
        """
        get_suggestions_info implementation
        """
        payload = GetSuggestionsRequest(
            model_id=model_id, model_version=model_version
        )

        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/suggestions/{payload.model_id}/{payload.model_version}",
            exception_class=SDKClientException,
        )

        adapter = TypeAdapter(list[SuggestionInfo])
        return adapter.validate_python(response.json())

    def show_suggestions(self, model_id: str, model_version: str) -> None:
        """
        show_suggestions implementation
        """

        suggestions = self.get_suggestions_info(
            model_id=model_id, model_version=model_version
        )

        self._print_table(
            suggestions,
            [
                "SuggestionInfo Id",
                "Executed",
                "Timestamp",
            ],
        )

    # TODO controllare validazione DataSchema
    def add_data_schema(self, task_id: str, data_schema: DataSchema) -> None:
        """
        add_data_schema implementation
        """
        payload = CreateDataSchemaRequest(
            task_id=task_id, data_schema=data_schema
        )

        self._api_call(
            method=HTTPMethod.POST,
            path="/data-schema",
            json_payload=payload.model_dump_json(),
            exception_class=AddDataSchemaException,
        )

    def get_data_schema(self, task_id: str) -> DataSchema:
        """
        get_data_schema implementation
        """

        payload = GetDataSchemaRequest(task_id=task_id)

        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/data-schema/{payload.task_id}",
            exception_class=SDKClientException,
        )

        return DataSchema.model_validate_json(response.content)

    def get_data_schema_template(self, task_id: str) -> DataSchema:
        """
        get_data_schema_template implementation
        """

        payload = GetDataSchemaTemplateRequest(task_id=task_id)

        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/data-schema-template/{payload.task_id}",
            exception_class=SDKClientException,
        )

        return DataSchema.model_validate_json(response.content)

    def show_data_schema(self, task_id: str):
        """
        show_data_schema implementation
        """

        data_schema = self.get_data_schema(task_id=task_id)
        self._print_table(
            [] if data_schema is None else data_schema.columns,
            headers=[
                "Column name",
                "Role",
                "Type",
                "Nullable",
                "Predicted Target",
                "Possible Values",
                "Model Id",
                "Dims",
            ],
        )

    def add_historical_data(
        self,
        task_id: str,
        inputs: Data,
        target: Data | None = None,
        predictions: list[tuple[str, Data]] | None = None,
    ) -> str:
        """
        add_historical_data implementation
        """

        inputs_data_info = self._process_data(
            task_id=task_id,
            data=inputs,
            storing_data_type=StoringDataType.HISTORICAL,
            data_category=DataCategory.INPUT,
            mapping_data_category=DataCategory.INPUT_MAPPING,
            embedding_data_category=DataCategory.INPUT_ADDITIONAL_EMBEDDING,
            model_id=None,
            project_id=None,
            kpi_id=None,
        )
        target_data_info = self._process_data(
            task_id=task_id,
            data=target,
            storing_data_type=StoringDataType.HISTORICAL,
            data_category=DataCategory.TARGET,
            mapping_data_category=DataCategory.TARGET_MAPPING,
            embedding_data_category=DataCategory.TARGET_ADDITIONAL_EMBEDDING,
            model_id=None,
            project_id=None,
            kpi_id=None,
        )
        if predictions is not None:
            model_ids: list[str] = [
                model.model_id for model in self.get_models(task_id=task_id)
            ]
            predictions_data_info = []
            for model_id, prediction_data in predictions:
                if model_id not in model_ids:
                    raise AddProductionDataException(
                        error_code="ADD_PRODUCTION_DATA_MODEL_ERROR",
                        error_message=f"Model {model_id} not found",
                    )
                data_info = self._process_data(
                    task_id=task_id,
                    data=prediction_data,
                    storing_data_type=StoringDataType.PRODUCTION,
                    data_category=DataCategory.PREDICTION,
                    mapping_data_category=DataCategory.PREDICTION_MAPPING,
                    embedding_data_category=DataCategory.PREDICTION_ADDITIONAL_EMBEDDING,
                    model_id=model_id,
                    project_id=None,
                    kpi_id=None,
                )
                if data_info is not None:
                    predictions_data_info.append((model_id, data_info))
                else:
                    raise AddProductionDataException(
                        error_code="ADD_PRODUCTION_DATA_MODEL_ERROR",
                        error_message=f"Error in processing predictions "
                        f"of model {model_id}",
                    )
        else:
            predictions_data_info = None

        if inputs_data_info is None:
            raise AddHistoricalDataException("Error in processing task input")

        payload: AddHistoricalRequest = AddHistoricalRequest(
            task_id=task_id,
            inputs=inputs_data_info,
            target=target_data_info,
            predictions=predictions_data_info,
        )
        add_historical_data_response = self._api_call(
            method=HTTPMethod.POST,
            path="/data/historical",
            json_payload=payload.model_dump_json(),
            exception_class=AddHistoricalDataException,
        )
        return add_historical_data_response.json()

    def add_target_data(
        self,
        task_id: str,
        target: Data,
    ) -> str:
        """
        add_target_data implementation
        """

        target_data_info = self._process_data(
            task_id=task_id,
            data=target,
            storing_data_type=StoringDataType.TASK_TARGET,
            data_category=DataCategory.TARGET,
            mapping_data_category=DataCategory.TARGET_MAPPING,
            embedding_data_category=DataCategory.TARGET_ADDITIONAL_EMBEDDING,
            model_id=None,
            project_id=None,
            kpi_id=None,
        )
        if target_data_info is None:
            raise AddTargetDataException("Error in processing data object")
        payload: AddTargetRequest = AddTargetRequest(
            task_id=task_id,
            data=target_data_info,
        )
        add_target_data_response = self._api_call(
            method=HTTPMethod.POST,
            path="/data/target",
            json_payload=payload.model_dump_json(),
            exception_class=AddTargetDataException,
        )
        return add_target_data_response.json()

    def set_model_reference(
        self, model_id: str, from_timestamp: float, to_timestamp: float
    ) -> str:
        """
        Define the model reference by defining timestamp range
        """

        payload: SetModelReferenceRequest = SetModelReferenceRequest(
            model_id=model_id,
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
        )
        response = self._api_call(
            method=HTTPMethod.POST,
            path="/model/reference",
            json_payload=payload.model_dump_json(),
            exception_class=SetModelReferenceException,
        )
        return response.json()

    def add_production_data(
        self,
        task_id: str,
        inputs: Data | None = None,
        target: Data | None = None,
        predictions: list[tuple[str, Data]] | None = None,
    ) -> str:
        """
        add_production_data implementation
        """
        if (inputs is None) & (target is None) & (predictions is None):
            raise AddProductionDataException(
                error_code="ADD_PRODUCTION_DATA_NO_DATA_ERROR",
                error_message="No data provided",
            )

        inputs_data_info = self._process_data(
            task_id=task_id,
            data=inputs,
            storing_data_type=StoringDataType.PRODUCTION,
            data_category=DataCategory.INPUT,
            mapping_data_category=DataCategory.INPUT_MAPPING,
            embedding_data_category=DataCategory.INPUT_ADDITIONAL_EMBEDDING,
            model_id=None,
            project_id=None,
            kpi_id=None,
        )
        target_data_info = self._process_data(
            task_id=task_id,
            data=target,
            storing_data_type=StoringDataType.PRODUCTION,
            data_category=DataCategory.TARGET,
            mapping_data_category=DataCategory.TARGET_MAPPING,
            embedding_data_category=DataCategory.TARGET_ADDITIONAL_EMBEDDING,
            model_id=None,
            project_id=None,
            kpi_id=None,
        )
        if predictions is not None:
            model_ids: list[str] = [
                model.model_id for model in self.get_models(task_id=task_id)
            ]
            predictions_data_info = []
            for model_id, prediction_data in predictions:
                if model_id not in model_ids:
                    raise AddProductionDataException(
                        error_code="ADD_PRODUCTION_DATA_MODEL_ERROR",
                        error_message=f"Model {model_id} not found",
                    )
                data_info = self._process_data(
                    task_id=task_id,
                    data=prediction_data,
                    storing_data_type=StoringDataType.PRODUCTION,
                    data_category=DataCategory.PREDICTION,
                    mapping_data_category=DataCategory.PREDICTION_MAPPING,
                    embedding_data_category=DataCategory.PREDICTION_ADDITIONAL_EMBEDDING,
                    model_id=model_id,
                    project_id=None,
                    kpi_id=None,
                )
                if data_info is not None:
                    predictions_data_info.append((model_id, data_info))
                else:
                    raise AddProductionDataException(
                        error_code="ADD_PRODUCTION_DATA_MODEL_ERROR",
                        error_message=f"Error in processing predictions "
                        f"of model {model_id}",
                    )
        else:
            predictions_data_info = None

        add_production_data_request = AddProductionRequest(
            task_id=task_id,
            inputs=inputs_data_info,
            target=target_data_info,
            predictions=predictions_data_info,
        )

        add_production_data_response = self._api_call(
            method=HTTPMethod.POST,
            path="/data/production",
            json_payload=add_production_data_request.model_dump_json(),
            exception_class=AddProductionDataException,
        )

        return add_production_data_response.json()

    def create_kpi(self, project_id: str, name: str) -> str:
        """
        create_kpi implementation
        """
        payload: CreateKPIRequest = CreateKPIRequest(
            project_id=project_id, name=name
        )

        response = self._api_call(
            method=HTTPMethod.POST,
            path="/kpi",
            json_payload=payload.model_dump_json(),
            exception_class=CreateKPIException,
        )
        return response.json()

    def get_kpi(self, kpi_id: str) -> KPI:
        """
        get_kpi implementation
        """
        payload = GetKPIRequest(kpi_id=kpi_id)

        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/kpi/{payload.kpi_id}",
            exception_class=SDKClientException,
        )

        return KPI.model_validate_json(response.content)

    def get_kpis(self, project_id: str) -> list[KPI]:
        """
        get_models implementation
        """
        payload = GetKPIsRequest(project_id=project_id)

        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/kpis/{payload.project_id}",
            exception_class=SDKClientException,
        )

        adapter = TypeAdapter(list[KPI])
        return adapter.validate_python(response.json())

    def show_kpis(self, project_id: str) -> None:
        """
        show_kpis implementation
        """

        kpis = self.get_kpis(project_id=project_id)

        self._print_table(
            kpis,
            [
                "KPI Id",
                "Name",
                "Status",
                "Status start timestamp",
                "Status insert date",
            ],
        )

    def add_kpi_data(
        self,
        project_id: str,
        kpi_id: str,
        kpi: TabularData,
    ) -> str:
        """
        add_kpi_data implementation
        """
        kpi_data_info = self._process_data(
            task_id=None,
            data=kpi,
            project_id=project_id,
            storing_data_type=StoringDataType.KPI,
            data_category=None,
            embedding_data_category=None,
            mapping_data_category=None,
            model_id=None,
            kpi_id=kpi_id,
        )
        if kpi_data_info is not None:
            payload = AddKPIDataRequest(kpi_id=kpi_id, kpi=kpi_data_info)

            add_kpi_data_response = self._api_call(
                method=HTTPMethod.POST,
                path="/data/kpi",
                json_payload=payload.model_dump_json(),
                exception_class=AddKPIDataException,
            )
            return add_kpi_data_response.json()
        else:
            raise SDKClientException(
                "Problem encountered in processing KPI data"
            )

    def compute_retraining_report(
        self,
        model_id: str,
    ) -> str:
        """
        compute_retraining_report implementation
        """

        payload = ComputeRetrainingReportRequest(model_id=model_id)

        response = self._api_call(
            method=HTTPMethod.POST,
            path="/retraining-report",
            json_payload=payload.model_dump_json(),
            exception_class=ComputeRetrainingReportException,
        )

        return response.json()

    # TODO ricontrollare modelli
    def get_retraining_report(self, model_id: str) -> RetrainingReport:
        """
        get_retraining_report implementation
        """

        payload = GetRetrainingReportRequest(
            model_id=model_id,
        )

        response = self._api_call(
            method=HTTPMethod.GET,
            path="/retraining-report",
            params=payload.model_dump(),
            exception_class=GetRetrainingReportException,
        )

        return RetrainingReport.model_validate_json(response.content)

    def compute_rag_evaluation_report(
        self,
        task_id: str,
        report_name: str,
        from_timestamp: float,
        to_timestamp: float,
    ) -> str:
        """
        compute_rag_evaluation_report implementation
        """

        payload = ComputeRagEvaluationReportRequest(
            task_id=task_id,
            report_name=report_name,
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
        )

        response = self._api_call(
            method=HTTPMethod.POST,
            path="/rag-evaluation",
            json_payload=payload.model_dump_json(),
            exception_class=ComputeRagEvaluationReportException,
        )

        return response.json()

    def get_rag_evaluation_reports(
        self,
        task_id: str,
    ) -> list[TaskRagEvalReportItem]:
        """
        get_rag_evaluation_reports implementation
        """

        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/task/{task_id}/rag-evaluation",
            exception_class=GetRagEvaluationReportException,
        )

        adapter = TypeAdapter(list[TaskRagEvalReportItem])
        return adapter.validate_python(response.json())

    def export_rag_evaluation_report(
        self,
        report_id: str,
        folder: str,
        file_name: str,
    ) -> None:
        """
        export_rag_evaluation_report implementation
        """
        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/rag-evaluation/{report_id}/export",
            exception_class=SDKClientException,
        )

        if not file_name.endswith(".xlsx"):
            file_name = file_name + ".xlsx"

        file_path = os.path.join(folder, file_name)

        with open(file_path, "wb") as f:
            f.write(response.content)

        logger.info(f"RAG evaluation report exported to {file_path}")

    def compute_topic_modeling_report(
        self,
        task_id: str,
        report_name: str,
        from_timestamp: float,
        to_timestamp: float,
    ) -> str:
        """
        compute_topic_modeling_report implementation
        """

        payload = ComputeTopicModelingReportRequest(
            task_id=task_id,
            report_name=report_name,
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
        )

        response = self._api_call(
            method=HTTPMethod.POST,
            path="/topic-modeling",
            json_payload=payload.model_dump_json(),
            exception_class=ComputeTopicModelingReportException,
        )

        return response.json()

    def get_topic_modeling_reports(
        self,
        task_id: str,
    ) -> list[TaskTopicModelingReportItem]:
        """
        get_topic_modeling_reports implementation
        """

        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/task/{task_id}/topic-modeling",
            exception_class=GetTopicModelingReportException,
        )

        adapter = TypeAdapter(list[TaskTopicModelingReportItem])
        return adapter.validate_python(response.json())

    def get_topic_modeling_report(
        self,
        report_id: str,
    ) -> TaskTopicModelingReportDetails:
        """
        get_topic_modeling_reports implementation
        """

        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/topic-modeling/{report_id}",
            exception_class=GetTopicModelingReportException,
        )

        adapter = TypeAdapter(TaskTopicModelingReportDetails)
        return adapter.validate_python(response.json())

    def get_monitoring_status(
        self,
        task_id: str,
        monitoring_target: MonitoringTarget,
        monitoring_metric: MonitoringMetric | None = None,
        specification: str | None = None,
    ) -> MonitoringQuantityStatus:
        """
        get_monitoring_status implementation
        """

        payload = GetMonitoringStatusRequest(
            task_id=task_id,
            monitoring_target=monitoring_target,
            monitoring_metric=monitoring_metric,
            specification=specification,
        )

        response = self._api_call(
            method=HTTPMethod.GET,
            path="/sdk-monitoring-status",
            params=payload.model_dump(),
            exception_class=SDKClientException,
        )
        adapter = TypeAdapter(MonitoringQuantityStatus)
        return adapter.validate_python(response.json())

    def get_jobs(
        self,
        project_id: str | None = None,
        task_id: str | None = None,
        model_id: str | None = None,
        status: JobStatus | None = None,
        job_id: str | None = None,
    ) -> list[Job]:
        """
        get_jobs implementation
        """
        payload = GetJobRequest(
            project_id=project_id,
            task_id=task_id,
            model_id=model_id,
            status=status.value if status is not None else None,
            job_id=job_id,
        )

        response = self._api_call(
            method=HTTPMethod.GET,
            path="/job",
            params=payload.model_dump(),
            exception_class=SDKClientException,
        )
        adapter = TypeAdapter(list[Job])
        return adapter.validate_python(response.json())

    def get_job(self, job_id: str) -> Job:
        """
        get_job implementation
        """
        jobs: list[Job] = self.get_jobs(job_id=job_id)

        if len(jobs) == 0:
            raise SDKClientException(f"No job found with id {job_id}")

        if len(jobs) > 1:
            raise SDKClientException(
                f"Found more than one job with id {job_id}"
            )

        return jobs[0]

    def show_jobs(
        self,
    ) -> None:
        """
        show_jobs implementation
        """

        jobs: list[Job] = self.get_jobs()

        self._print_table(
            items=jobs,
            headers=[
                "Job Id",
                "Job Type",
                "Project Id",
                "Project Name",
                "Task Id",
                "Task Name",
                "Model Id",
                "Model Name",
                "Status",
                "Error",
            ],
        )

    def get_detection_events(self, task_id: str) -> list[DetectionEvent]:
        """
        get_detection_event_rules implementation
        """

        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/task/{task_id}/sdk-detection-events",
            exception_class=SDKClientException,
        )

        adapter = TypeAdapter(list[DetectionEvent])
        return adapter.validate_python(response.json())

    def get_detection_event_rules(
        self, task_id: str
    ) -> list[DetectionEventRule]:
        """
        get_detection_event_rules implementation
        """

        response = self._api_call(
            method=HTTPMethod.GET,
            path="/task/detection-event/rules",
            params={"task_id": task_id},
            exception_class=SDKClientException,
        )

        adapter = TypeAdapter(list[DetectionEventRule])
        return adapter.validate_python(response.json())

    def get_detection_event_rule(self, rule_id: str) -> DetectionEventRule:
        """
        get_detection_event_rule implementation
        """

        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/task/detection-event/rule/{rule_id}",
            exception_class=SDKClientException,
        )

        return DetectionEventRule.model_validate_json(response.content)

    def set_detection_event_user_feedback(
        self, detection_id: str, user_feedback: bool
    ) -> None:
        """
        set detection event user feedback
        """
        payload = SetTaskDetectionEventUserFeedback(
            detection_id=detection_id, user_feedback=user_feedback
        )
        self._api_call(
            method=HTTPMethod.PATCH,
            path="/task-detections/feedback",
            json_payload=payload.model_dump_json(),
            exception_class=SDKClientException,
        )

    @staticmethod
    def _validate_rule_actions(
        actions: list[DetectionEventAction],
        model_name: str | None,
    ) -> list[DetectionEventAction]:
        """
        Action check: if there is RetrainAction it should be valid
        that means:
          1- model_name of the rule is not None
          2- model_name of the action is None or equal to model_name
              of the rule
          3- there is only one retrain action
        """
        retrain_actions = list(
            filter(lambda x: isinstance(x, RetrainAction), actions)
        )
        n_retrain_actions = len(retrain_actions)
        # Only one retrain action is allowed
        if n_retrain_actions > 1:
            raise InvalidActionList(
                f"There are {n_retrain_actions} RetrainAction objects "
                f"but the maximum allowed number is 1"
            )

        if n_retrain_actions > 0:
            # the rule target must be the model
            if model_name is None:
                raise InvalidActionList(
                    "There is a RetrainAction but model_name is missing"
                )
            # if the RetrainAction does not have the model_name we set
            # it equal to the target.
            retrain_action = retrain_actions[0]
            assert isinstance(retrain_action, RetrainAction)
            if retrain_action.model_name is None:
                retrain_action.model_name = model_name
            elif retrain_action.model_name != model_name:
                raise InvalidActionList(
                    f"RetrainAction must have the same model_name as "
                    f"rule target. RetrainAction.model_name = "
                    f"{retrain_action.model_name}"
                    f"model_name ? {model_name}"
                )
        return actions

    def create_detection_event_rule(
        self,
        name: str,
        task_id: str,
        severity: DetectionEventSeverity | None,
        detection_event_type: DetectionEventType,
        monitoring_target: MonitoringTarget,
        actions: list[DetectionEventAction],
        monitoring_metric: MonitoringMetric | None = None,
        model_name: str | None = None,
    ) -> str:
        """
        create_detection_event_rule implementation
        """
        try:
            actions = self._validate_rule_actions(
                actions=actions, model_name=model_name
            )
        except InvalidActionList as e:
            raise CreateDetectionEventRuleException(
                error_code="CREATE_DETECTION_EVENT_RULE_ERROR",
                error_message="Failed rule action validation",
            ) from e

        payload = CreateDetectionEventRuleRequest(
            name=name,
            task_id=task_id,
            model_name=model_name,
            severity=severity,
            detection_event_type=detection_event_type,
            monitoring_target=monitoring_target,
            monitoring_metric=monitoring_metric,
            actions=[a.model_dump() for a in actions],
        )

        response = self._api_call(
            method=HTTPMethod.POST,
            path="/task/detection-event/rule",
            json_payload=payload.model_dump_json(),
            exception_class=CreateDetectionEventRuleException,
        )

        return response.json()

    def update_detection_event_rule(
        self,
        rule_id: str,
        name: str | None = None,
        model_name: str | None = None,
        severity: DetectionEventSeverity | None = None,
        detection_event_type: DetectionEventType | None = None,
        monitoring_target: MonitoringTarget | None = None,
        actions: list[DetectionEventAction] | None = None,
    ):
        """
        update_detection_event_rule implementation
        """
        if actions is not None:
            try:
                actions = self._validate_rule_actions(
                    actions=actions, model_name=model_name
                )
            except InvalidActionList as e:
                raise UpdateDetectionEventRuleException(
                    error_code="UPDATE_DETECTION_EVENT_RULE_ERROR",
                    error_message="Failed rule action validation",
                ) from e
        payload = UpdateDetectionEventRuleRequest(
            rule_id=rule_id,
            name=name,
            model_name=model_name,
            severity=severity,
            detection_event_type=detection_event_type,
            monitoring_target=monitoring_target,
            actions=None if actions is None else [a.dict() for a in actions],
        )

        response = self._api_call(
            method=HTTPMethod.PATCH,
            path="/task/detection-event/rule",
            json_payload=payload.model_dump_json(),
            exception_class=UpdateDetectionEventRuleException,
        )

        return response.json()

    def delete_detection_event_rule(self, rule_id: str):
        """
        delete_detection_event_rule implementation
        """

        self._api_call(
            method=HTTPMethod.DELETE,
            path=f"/task/detection-event/rule/{rule_id}",
            exception_class=SDKClientException,
        )

    def wait_job_completion(self, job_id: str, max_wait_timeout: int):
        """
        Utility function to wait for job completion
        """

        completed = False
        start_timestamp = int(time.time())

        while not completed:
            current_timestamp = int(time.time())
            if current_timestamp - start_timestamp > max_wait_timeout:
                raise JobWaitTimeoutException()

            job = self.get_job(job_id=job_id)
            if job is None:
                raise JobNotFoundException()

            if job.status in [
                JobStatus.ERROR.value,
                JobStatus.ROLLBACK_COMPLETE.value,
            ]:
                raise JobFailureException()

            completed = job.status == JobStatus.COMPLETED.value

            time.sleep(int(os.environ.get("MLCUBE_POLLING", "30")))

    def create_company_user(
        self,
        name: str,
        surname: str,
        username: str,
        password: str,
        email: str,
        company_role: UserCompanyRole,
    ) -> str:
        """
        create_company_user implementation
        """
        payload = CreateCompanyUserRequest(
            name=name,
            surname=surname,
            username=username,
            email=email,
            password=password,
            company_role=company_role,
        )

        response = self._api_call(
            method=HTTPMethod.POST,
            path="/company-user",
            json_payload=payload.model_dump_json(),
            exception_class=SDKClientException,
        )
        return response.json()

    def get_company_users(self) -> list[CompanyUser]:
        """
        get_company_users implementation
        """

        response = self._api_call(
            method=HTTPMethod.GET,
            path="/company-user",
            exception_class=SDKClientException,
        )
        adapter = TypeAdapter(list[CompanyUser])
        return adapter.validate_python(response.json())

    def change_user_company_role(
        self, user_id: str, company_role: UserCompanyRole
    ):
        """
        change_company_role implementation
        """
        request = ChangeUserCompanyRoleRequest(
            user_id=user_id, company_role=company_role
        )

        self._api_call(
            method=HTTPMethod.POST,
            path="/change-user-company-role",
            json_payload=request.model_dump_json(),
            exception_class=SDKClientException,
        )

    def show_company_users(self):
        """
        show_company_users implementation
        """

        items = self.get_company_users()

        self._print_table(
            items,
            ["User Id", "Company Role"],
        )

    def get_user_projects(self, user_id: str) -> list[Project]:
        """
        get_user_projects implementation
        """
        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/user-project/{user_id}",
            exception_class=SDKClientException,
        )

        adapter = TypeAdapter(list[Project])
        return adapter.validate_python(response.json())

    def show_user_projects(self, user_id: str):
        """
        show_user_projects implementation
        """

        items = self.get_user_projects(user_id=user_id)

        self._print_table(
            items,
            ["Project Id", "Name"],
        )

    def add_user_project_role(
        self, user_id: str, project_id: str, project_role: UserProjectRole
    ):
        """
        add_project_role implementation
        """
        request = AddUserProjectRoleRequest(
            user_id=user_id, project_id=project_id, project_role=project_role
        )

        self._api_call(
            method=HTTPMethod.POST,
            path="/user-project-role",
            json_payload=request.model_dump_json(),
            exception_class=SDKClientException,
        )

    def delete_project_role(self, user_id: str, project_id: str):
        """
        delete_project_role implementation
        """
        request = DeleteUserProjectRoleRequest(
            user_id=user_id, project_id=project_id
        )

        self._api_call(
            method=HTTPMethod.DELETE,
            path="/user-project-role",
            json_payload=request.model_dump_json(),
            exception_class=SDKClientException,
        )

    def get_api_keys(self) -> list[ApiKey]:
        """
        get_api_keys implementation
        """

        response = self._api_call(
            method=HTTPMethod.GET,
            path="/api-key",
            exception_class=SDKClientException,
        )

        adatper = TypeAdapter(list[ApiKey])
        return adatper.validate_python(response.json())

    def show_api_keys(self):
        """
        show_api_keys implementation
        """

        items = self.get_api_keys()

        self._print_table(
            items,
            ["Api Key", "Name", "Expiration Time"],
        )

    def create_api_key(
        self, name: str, expiration_time: ApiKeyExpirationTime
    ) -> str:
        """
        create_api_key implementation
        """

        request = CreateApiKeyRequest(
            name=name,
            expiration_time=expiration_time,
        )

        response = self._api_call(
            method=HTTPMethod.POST,
            path="/api-key",
            json_payload=request.model_dump_json(),
            exception_class=SDKClientException,
        )
        return response.json()

    def delete_api_key(self, api_key: str):
        """
        delete_api_key implementation
        """

        request = DeleteApiKeyRequest(api_key=api_key)

        self._api_call(
            method=HTTPMethod.DELETE,
            path=f"/api-key/{request.api_key}",
            exception_class=SDKClientException,
        )

    def show_user_api_keys(self, user_id: str):
        """
        show_user_api_keys implementation
        """
        items = self.get_user_api_keys(user_id=user_id)

        self._print_table(
            items,
            ["Api Key", "Name", "Expiration Time"],
        )

    def get_user_api_keys(self, user_id: str) -> list[ApiKey]:
        """
        get_user_api_keys implementation
        """

        request = GetUserApiRequest(user_id=user_id)

        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/user-api-key/{request.user_id}",
            exception_class=SDKClientException,
        )

        adapter = TypeAdapter(list[ApiKey])
        return adapter.validate_python(response.json())

    def create_user_api_key(
        self, user_id: str, name: str, expiration_time: ApiKeyExpirationTime
    ) -> str:
        """
        create_user_api_key implementation
        """

        request = CreateUserApiRequest(
            user_id=user_id, name=name, expiration_time=expiration_time
        )

        response = self._api_call(
            method=HTTPMethod.POST,
            path="/user-api-key",
            json_payload=request.model_dump_json(),
            exception_class=SDKClientException,
        )
        return response.json()

    def delete_user_api_key(self, user_id: str, api_key: str):
        """
        delete_user_api_key implementation
        """
        request = DeleteUserApiKeyRequest(user_id=user_id, api_key=api_key)

        self._api_call(
            method=HTTPMethod.DELETE,
            path=f"/user-api-key/{request.user_id}/{request.api_key}",
            exception_class=SDKClientException,
        )

    def change_company_owner(self, user_id: str):
        """
        change_company_owner implementation
        """
        request = ChangeCompanyOwnerRequest(
            user_id=user_id,
        )

        self._api_call(
            method=HTTPMethod.POST,
            path=f"/company-owner/{request.user_id}",
            exception_class=SDKClientException,
        )

    def delete_company_user(self, user_id: str):
        """
        delete a user in the company
        """

        request = DeleteCompanyUserRequest(user_id=user_id)

        self._api_call(
            method=HTTPMethod.DELETE,
            path=f"/company-user/{request.user_id}",
            exception_class=SDKClientException,
        )

    def get_integration_credentials(
        self, credentials_id: str
    ) -> IntegrationCredentials:
        """
        get_integration_credentials implementation
        """

        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/integration/credentials/{credentials_id}",
            exception_class=SDKClientException,
        )

        # Parse as the parent class
        credentials = IntegrationCredentials.model_validate_json(
            response.content
        )

        # Cast to the correct subclass
        if credentials.type == ExternalIntegration.AWS:
            return AWSCredentials.model_validate_json(response.content)
        elif credentials.type == ExternalIntegration.AWS_COMPATIBLE:
            return AWSCompatibleCredentials.model_validate_json(
                response.content
            )
        if credentials.type == ExternalIntegration.GCP:
            return GCPCredentials.model_validate_json(response.content)
        if credentials.type == ExternalIntegration.AZURE:
            return AzureCredentials.model_validate_json(response.content)

        raise NotImplementedError(f"{credentials.type} is not supported")

    def get_all_project_integration_credentials(
        self, project_id: str
    ) -> list[IntegrationCredentials]:
        """
        get_all_project_integration_credentials implementation
        """

        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/project/{project_id}/integration-credentials",
            exception_class=SDKClientException,
        )

        # Parse as list of dicts, then cast each one to the subclass
        credentials: list[dict] = response.json()

        casted_credentials: list[IntegrationCredentials] = []

        for cred in credentials:
            # Parse as parent class to access the 'type' field
            generic: IntegrationCredentials = (
                IntegrationCredentials.model_validate(cred)
            )

            # Cast to the correct subclass
            if generic.type == ExternalIntegration.AWS:
                casted_credentials.append(AWSCredentials.model_validate(cred))
            elif generic.type == ExternalIntegration.GCP:
                casted_credentials.append(GCPCredentials.model_validate(cred))
            elif generic.type == ExternalIntegration.AZURE:
                casted_credentials.append(
                    AzureCredentials.model_validate(cred)
                )
            else:
                raise NotImplementedError(f"{generic.type} is not supported")

        return casted_credentials

    def delete_integration_credentials(self, credentials_id: str):
        """
        delete_integration_credentials implementation
        """

        self._api_call(
            method=HTTPMethod.DELETE,
            path=f"/integration/credentials/{credentials_id}",
            exception_class=SDKClientException,
        )

    def set_integration_credentials_as_default(self, credentials_id: str):
        """
        set_integration_credentials_as_default implementation
        """

        self._api_call(
            method=HTTPMethod.POST,
            path=f"/integration/credentials/{credentials_id}/default",
            exception_class=SDKClientException,
        )

    def create_aws_integration_credentials(
        self, name: str, default: bool, project_id: str, role_arn: str
    ) -> SecretAWSCredentials:
        """
        create_aws_integration_credentials implementation
        """

        request = CreateAWSIntegrationCredentialsRequest(
            name=name,
            default=default,
            project_id=project_id,
            role_arn=role_arn,
        )

        response = self._api_call(
            method=HTTPMethod.POST,
            path="/integration/aws/credentials",
            json_payload=request.model_dump_json(),
            exception_class=SDKClientException,
        )

        return SecretAWSCredentials.model_validate_json(response.content)

    def create_aws_compatible_integration_credentials(
        self,
        name: str,
        default: bool,
        project_id: str,
        access_key_id: str,
        secret_access_key: str,
        endpoint_url: str | None = None,
    ) -> AWSCompatibleCredentials:
        """
        create_aws_compatible_integration_credentials implementation
        """

        request = CreateAWSCompatibleIntegrationCredentialsRequest(
            name=name,
            default=default,
            project_id=project_id,
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            endpoint_url=endpoint_url,
        )

        response = self._api_call(
            method=HTTPMethod.POST,
            path="/integration/aws-compatible/credentials",
            json_payload=request.model_dump_json(),
            exception_class=SDKClientException,
        )

        return AWSCompatibleCredentials.model_validate_json(response.content)

    def create_gcp_integration_credentials(
        self,
        name: str,
        default: bool,
        project_id: str,
        service_account_info_json: str,
    ) -> GCPCredentials:
        """
        create_gcp_integration_credentials implementation
        """

        try:
            account_info = GCPAccountInfo.model_validate(
                json.loads(service_account_info_json)
            )
        except Exception as e:
            raise SDKClientException("Invalid credentials format") from e

        request = CreateGCPIntegrationCredentialsRequest(
            name=name,
            default=default,
            project_id=project_id,
            account_info=account_info,
        )

        response = self._api_call(
            method=HTTPMethod.POST,
            path="/integration/gcp/credentials",
            json_payload=request.model_dump_json(),
            exception_class=SDKClientException,
        )

        return GCPCredentials.model_validate_json(response.content)

    def create_azure_integration_credentials(
        self,
        name: str,
        default: bool,
        project_id: str,
        service_principal_credentials_json: str,
    ) -> AzureCredentials:
        """
        create_azure_integration_credentials implementation
        """

        try:
            credentials = AzureSPCredentials.model_validate(
                json.loads(service_principal_credentials_json)
            )
        except Exception as e:
            raise SDKClientException("Invalid credentials format") from e

        request = CreateAzureIntegrationCredentialsRequest(
            name=name,
            default=default,
            project_id=project_id,
            credentials=credentials,
        )

        response = self._api_call(
            method=HTTPMethod.POST,
            path="/integration/azure/credentials",
            json_payload=request.model_dump_json(),
            exception_class=SDKClientException,
        )

        return AzureCredentials.model_validate_json(response.content)

    def set_retrain_trigger(
        self,
        model_id: str,
        trigger: RetrainTrigger | None,
    ):
        """
        set_retrain_trigger implementation
        """

        if trigger is None:
            self._api_call(
                method=HTTPMethod.DELETE,
                path=f"/model/{model_id}/retrain-trigger",
                exception_class=SDKClientException,
            )
        else:
            self._api_call(
                method=HTTPMethod.POST,
                path=f"/model/{model_id}/retrain-trigger",
                json_payload=trigger.model_dump_json(),
                exception_class=SDKClientException,
            )

    def test_retrain_trigger(self, model_id: str, trigger: RetrainTrigger):
        """
        test_retrain_trigger implementation
        """
        payload = TestRetrainTriggerRequest(
            model_id=model_id,
            retrain_trigger=trigger,
        )

        self._api_call(
            method=HTTPMethod.POST,
            path="/test-retrain-trigger",
            json_payload=payload.model_dump_json(),
            exception_class=SDKClientException,
        )

    def retrain_model(
        self,
        model_id: str,
    ) -> str:
        """
        retrain_model implementation
        """

        payload = RetrainModelRequest(
            model_id=model_id,
        )

        response = self._api_call(
            method=HTTPMethod.POST,
            path="/retrain-model",
            json_payload=payload.model_dump_json(),
            exception_class=SDKClientException,
        )

        return response.json()

    def compute_llm_security_report(
        self,
        task_id: str,
        report_name: str,
        from_timestamp: float,
        to_timestamp: float,
    ) -> str:
        """
        compute_llm_security_report implementation
        """

        payload = ComputeLlmSecurityReportRequest(
            task_id=task_id,
            report_name=report_name,
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
        )

        response = self._api_call(
            method=HTTPMethod.POST,
            path="/llm-security",
            json_payload=payload.model_dump_json(),
            exception_class=ComputeLlmSecurityReportException,
        )

        return response.json()

    def get_llm_security_reports(
        self,
        task_id: str,
    ) -> list[TaskLlmSecReportItem]:
        """
        get_llm_security_reports implementation
        """

        response = self._api_call(
            method=HTTPMethod.GET,
            path=f"/task/{task_id}/llm-security",
            exception_class=GetLlmSecurityReportException,
        )

        adapter = TypeAdapter(list[TaskLlmSecReportItem])
        return adapter.validate_python(response.json())
