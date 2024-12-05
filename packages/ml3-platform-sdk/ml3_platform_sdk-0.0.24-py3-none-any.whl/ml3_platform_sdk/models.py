from __future__ import annotations

from abc import abstractmethod
from datetime import date, datetime  # noqa: TCH003
from typing import Any

from pydantic import Extra, SerializeAsAny, model_validator

from ml3_platform_sdk.core.enums import RawDataSourceType
from ml3_platform_sdk.core.models import ML3BaseModel as BaseModel
from ml3_platform_sdk.enums import (
    ColumnRole,
    ColumnSubRole,
    Currency,
    DataStructure,
    DataType,
    DetectionEventActionType,
    DetectionEventSeverity,
    DetectionEventType,
    ExternalIntegration,
    FileType,
    FolderType,
    ImageMode,
    JobStatus,
    KPIStatus,
    ModelMetricName,
    MonitoringMetric,
    MonitoringStatus,
    MonitoringTarget,
    ProductKeyStatus,
    RetrainTriggerType,
    StoragePolicy,
    SubscriptionType,
    SuggestionType,
    TaskType,
    UserCompanyRole,
)

# Used for polymorphic classes (de)serialization
subclass_registry: dict = {}


class Company(BaseModel):
    """
    Company model

    Attributes:
        company_id: str
        name: str
        address: str
        vat: str
    """

    company_id: str
    name: str
    address: str
    vat: str


class Project(BaseModel):
    """
    Project model

    Attributes:
        project_id: str
        name: str

    """

    project_id: str
    name: str


class TaskCostInfo(BaseModel):
    """
    Base class for task cost info.
    It depends on TaskType because classification is different from
    regression in terms of business costs due to errors
    """

    currency: Currency

    class Config:
        """
        Allow extra fields
        """

        extra = Extra.allow


class RegressionTaskCostInfo(TaskCostInfo):
    """
    Regression cost info is expressed in two terms:
    - cost due to overestimation
    - cost due to underestimation

    Fields:
        currency
        overestimation_cost
        underestimation_cost
    """

    overestimation_cost: float
    underestimation_cost: float


class BinaryClassificationTaskCostInfo(TaskCostInfo):
    """
    Binary classification cost info is expressed in two terms:
    - cost of false positive
    - cost of false negative
    """

    false_positive_cost: float
    false_negative_cost: float


class MulticlassClassificationTaskCostInfo(TaskCostInfo):
    """
    Multiclass classification cost info is expressed in terms of
    the misclassification costs for each class
    """

    misclassification_cost: dict[str | int, float]


class MultilabelClassificationTaskCostInfo(TaskCostInfo):
    """
    Multilabel classification cost info is expressed in terms of
    false positive and false negative costs for each class
    """

    false_positive_costs: dict[str, float]
    false_negative_costs: dict[str, float]


# type to use in BaseModels
TaskCostInfoUnion = (
    RegressionTaskCostInfo
    | BinaryClassificationTaskCostInfo
    | MulticlassClassificationTaskCostInfo
    | MultilabelClassificationTaskCostInfo
)


class Task(BaseModel):
    """
    Task model

    Attributes:
        task_id: str
        name: str
        type: TaskType
        cost_info: TaskCostInfoUnion | None = None
        optional_target: bool
        monitoring_targets: list[MonitoringTarget]
        monitoring_metrics: (
            None
            | dict[MonitoringTarget, list[tuple[MonitoringMetric, str | None]]]
        ) = None
        monitoring_status: list[MonitoringQuantityStatus]
    """

    task_id: str
    name: str
    type: TaskType
    cost_info: TaskCostInfoUnion | None = None
    optional_target: bool
    monitoring_targets: list[MonitoringTarget]
    monitoring_metrics: (
        None
        | dict[MonitoringTarget, list[tuple[MonitoringMetric, str | None]]]
    ) = None
    monitoring_status: list[MonitoringQuantityStatus]


class RetrainTrigger(BaseModel):
    """
    Base model to define a retrain trigger

    Fields:
        type
        credentials_id
    """

    type: RetrainTriggerType
    credentials_id: str


class AWSEventBridgeRetrainTrigger(RetrainTrigger):
    """
    Base model to define an AWS EventBridge retrain trigger

    Fields:
        type
        credentials_id
        aws_region_name
        event_bus_name
    """

    type: RetrainTriggerType = RetrainTriggerType.AWS_EVENT_BRIDGE
    aws_region_name: str
    event_bus_name: str


class GCPPubSubRetrainTrigger(RetrainTrigger):
    """
    Base model to define a GCP PubSub retrain trigger

    Fields:
        type
        credentials_id
        topic_name
    """

    type: RetrainTriggerType = RetrainTriggerType.GCP_PUBSUB
    topic_name: str


class AzureEventGridRetrainTrigger(RetrainTrigger):
    """
    Base model to define an Azure EventGrid retrain trigger

    Fields:
        type
        credentials_id
        topic_endpoint
    """

    type: RetrainTriggerType = RetrainTriggerType.AZURE_EVENT_GRID
    topic_endpoint: str


class LLMPrompt(BaseModel):
    """
    Base model to define llm prompts

    Attributes:
        role: str
        task: str
        behavior_guidelines: str
        security_guidelines: str
    """

    role: str | None
    task: float | None
    behavior_guidelines: list[str]
    security_guidelines: list[str]


class LLMSpecs(BaseModel):
    """
    Base model to define llm specs

    Attributes:
        llm: str
        temperature: float
        prompt: LLMPrompt
    """

    llm: str | None
    temperature: float | None
    prompt: LLMPrompt


class Model(BaseModel):
    """
    Base model to define model item

    Attributes:
        model_id: str
        task_id: str
        name: str
        version: str
        metric_name: performance or error metric associated with
            the model
        creation_datetime: Optional[datetime]
        retrain_trigger: Optional[RetrainTrigger]
        retraining_cost: float
        llm_specs: Optional[LLMSpecs]
    """

    model_id: str
    task_id: str
    name: str
    version: str
    metric_name: ModelMetricName | None = None
    creation_datetime: datetime | None = None
    retrain_trigger: (
        AWSEventBridgeRetrainTrigger
        | GCPPubSubRetrainTrigger
        | AzureEventGridRetrainTrigger
        | None
    ) = None
    retraining_cost: float
    llm_specs: LLMSpecs | None


class Job(BaseModel):
    """
    Job information item model

    Attributes:
        job_id: str
        job_group: str
        project_id: str
        project_name: str
        task_id: str
        task_name: str
        model_id: Optional[str]
        model_name: Optional[str]
        status: str
        error: Optional[str]
    """

    job_id: str
    job_group: str
    project_id: str
    project_name: str
    task_id: str
    task_name: str
    model_id: str | None = None
    model_name: str | None = None
    status: str
    error: str | None = None


class ColumnInfo(BaseModel):
    """
    Column base model

    Attributes:
        name: str
        role: ColumnRole
        is_nullable: bool
        data_type: DataType
        predicted_target: Optional[str] = None
        possible_values: Optional[list[str | int | bool]] = None
        model_id: Optional[str] = None
        dims: Optional[tuple[int]] = None
            it is mandatory when data_type is Array
        classes_names: Optional[list[str]] = None
            it is mandatory when the column is the target
            in multilabel classification tasks
        subrole: Optional[ColumnSubRole] = None
            Indicates the subrole of the column. It's used in
            RAG tasks to define the role of the input columns
            (e.g. user input or retrieved context)
        image_mode: Optional[ImageMode] = None
            Indicates the mode of the image. It must be provided
            when the data type is an image
    """

    name: str
    role: ColumnRole
    is_nullable: bool
    data_type: DataType
    predicted_target: str | None = None
    possible_values: list[str | int | bool] | None = None
    model_id: str | None = None
    dims: tuple[int, ...] | None = None
    classes_names: list[str] | None = None
    subrole: ColumnSubRole | None = None
    image_mode: ImageMode | None = None


class DataSchema(BaseModel):
    """
    Data schema base model

    Attributes:
        columns: List[ColumnInfo]
    """

    columns: list[ColumnInfo]


class KPI(BaseModel):
    """
    KPI base model

    Attributes:
        kpi_id: str
        name: str
        status: ModelStatus
        status_kpi_start_timestamp: Optional[datetime]
        status_insert_datetime: datetime
    """

    kpi_id: str
    name: str
    status: KPIStatus
    status_kpi_start_timestamp: datetime | None = None
    status_insert_datetime: datetime


class SuggestionInfo(BaseModel):
    """
    SuggestionInfo base model

    Attributes:
        id: str
        executed: bool
        timestamp: float
    """

    id: str
    executed: bool
    timestamp: float


class Suggestion(BaseModel):
    """
    Suggestion base model

    Attributes:
        suggestion_id: str
        suggestion_type: SuggestionType
        sample_ids: List[str]
    """

    suggestion_id: str
    suggestion_type: SuggestionType
    sample_ids: list[str]

    class Config:
        """
        Config class for Suggestion
        """

        extra = Extra.allow


class SampleWeightsSuggestion(Suggestion):
    """
    SampleWeightsSuggestion base model

    Attributes:
        suggestion_id: str
        suggestion_type: SuggestionType
        sample_ids: List[str]
        sample_weights: List[float]
    """

    sample_weights: list[float]


class ResampledDatasetSuggestion(Suggestion):
    """
    ResampledDatasetSuggestion base model

    Attributes:
        suggestion_id: str
        suggestion_type: SuggestionType
        sample_ids: List[str]
        sample_counts: List[int]
    """

    sample_counts: list[int]


class RetrainingReport(BaseModel):
    """
    base model for Retraining Report

    Attributes:
        report_id: str
        suggestion: Suggestion
        effective_sample_size: float
        model_metric_name: str
        performance_upper_bound: float
        performance_lower_bound: float
        cost_upper_bound: float
        cost_lower_bound: float
    """

    report_id: str
    suggestion: SerializeAsAny[Suggestion]
    effective_sample_size: float
    model_metric_name: str
    performance_upper_bound: float | None
    performance_lower_bound: float | None
    cost_upper_bound: float | None = None
    cost_lower_bound: float | None = None


class TaskRagEvalReportItem(BaseModel):
    """
    base model for Rag Evaluation Report

    Attributes:
        id: str
        creation_datetime: datetime
        name: str
        status: JobStatus
        from_datetime: datetime
        to_datetime: datetime
    """

    id: str
    creation_datetime: datetime
    name: str
    status: JobStatus
    from_datetime: datetime
    to_datetime: datetime


class TaskTopicModelingReportItem(BaseModel):
    """
    Task Topic Modeling Report Item base model

    Attributes:
        id: str
        creation_datetime: datetime
        name: str
        status: JobStatus
        from_date: datetime
        to_date: datetime
    """

    id: str
    creation_datetime: datetime
    name: str
    status: JobStatus
    from_date: datetime
    to_date: datetime


class TaskTopicModelingReportDetails(TaskTopicModelingReportItem):
    """
    Task Topic Modeling Report Details base model

    Attributes:
        sample_ids: list[str]
        topics: list[str]
    """

    sample_ids: list[str]
    topics: list[str]


class CompanyUser(BaseModel):
    """
    base model for company user

    Attributes:
        user_id: str
        company_role: UserCompanyRole
    """

    user_id: str
    company_role: UserCompanyRole


class ApiKey(BaseModel):
    """
    base model for api key

    Attributes:
        api_key: str
        name: str
        expiration_time: str | None
    """

    api_key: str
    name: str
    expiration_time: str | None = None


class MonitoringQuantityStatus(BaseModel):
    """
    Base model to store the monitoring status
    of a monitoring quantity (target or metric)

    Attributes:
        monitoring_target: MonitoringTarget
        status: MonitoringStatus
        monitoring_metric: MonitoringMetric | None
    """

    status: MonitoringStatus
    monitoring_target: MonitoringTarget
    monitoring_metric: MonitoringMetric | None = None
    specification: str | None = None


class DetectionEvent(BaseModel):
    """
    An event created during the detection process.

    Attributes:
        event_id: str
        event_type: DetectionEventType
        monitoring_target: MonitoringTarget
        monitoring_metric: MonitoringMetric | None
        severity_type: Optional[DetectionEventSeverity]
        insert_datetime: str
        sample_timestamp: float
        sample_customer_id: str
        model_id: Optional[str]
        model_name: Optional[str]
        model_version: Optional[str]
        user_feedback: Optional[bool]
        specification: Optional[str]
    """

    event_id: str
    event_type: DetectionEventType
    monitoring_target: MonitoringTarget
    monitoring_metric: MonitoringMetric | None = None
    severity_type: DetectionEventSeverity | None = None
    insert_datetime: str
    sample_timestamp: float
    sample_customer_id: str
    model_id: str | None = None
    model_name: str | None = None
    model_version: str | None = None
    user_feedback: bool | None = None
    specification: str | None = None


class DetectionEventAction(BaseModel):
    """
    Generic action that can be performed

    Attributes:
        type: DetectionEventActionType
    """

    type: DetectionEventActionType

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        subclass_registry[cls.__name__] = cls


class DiscordNotificationAction(DetectionEventAction):
    """
    Action that sends a notification to a Discord server through
    a webhook that you configure

    Attributes:
        type = DetectionEventActionType.DISCORD_NOTIFICATION
        webhook: str
    """

    type: DetectionEventActionType = (
        DetectionEventActionType.DISCORD_NOTIFICATION
    )
    webhook: str


class SlackNotificationAction(DetectionEventAction):
    """
    Action that sends a notification to a Slack channel through
    a webhook that you configure.

    Attributes:
        type = DetectionEventActionType.SLACK_NOTIFICATION
        webhook: str
        channel: str
    """

    type: DetectionEventActionType = (
        DetectionEventActionType.SLACK_NOTIFICATION
    )
    webhook: str
    channel: str


class EmailNotificationAction(DetectionEventAction):
    """
    Base Model for Email Notification Action

    Attributes:
        type = DetectionEventActionType.EMAIL_NOTIFICATION
        address: str
    """

    type: DetectionEventActionType = (
        DetectionEventActionType.EMAIL_NOTIFICATION
    )
    address: str


class TeamsNotificationAction(DetectionEventAction):
    """
    Base Model for Teams Notification Action

    Attributes:
        type: DetectionEventActionType.TEAMS_NOTIFICATION
        webhook: str
    """

    type: DetectionEventActionType = (
        DetectionEventActionType.TEAMS_NOTIFICATION
    )
    webhook: str


class MqttNotificationAction(DetectionEventAction):
    """
    Base Model for Mqtt Notification Action

    Attributes:
        type: DetectionEventActionType.MQTT_NOTIFICATION
        connection_string: str
        topic: str
        payload: str
    """

    type: DetectionEventActionType = DetectionEventActionType.MQTT_NOTIFICATION
    connection_string: str
    topic: str
    payload: str


class RetrainAction(DetectionEventAction):
    """
    Base Model for Retrain Action

    Attributes:
        type: DetectionEventActionType.RETRAIN
        model_name: str
    """

    type: DetectionEventActionType = DetectionEventActionType.RETRAIN
    model_name: str | None = None


def deserialize_actions(**kwargs):
    """
    Deserializes polymorphic actions from dict to their models.
    """

    for index in range(len(kwargs["actions"])):
        current_action = kwargs["actions"][index]
        if isinstance(current_action, dict):
            item_action_keys = sorted(current_action.keys())
            for subclass in subclass_registry.values():
                registered_keys = sorted(subclass.__fields__.keys())
                if (
                    item_action_keys == registered_keys
                    and current_action["type"]
                    == subclass.__fields__["type"].default.value
                ):
                    current_action = subclass(**current_action)
                    break
            kwargs["actions"][index] = current_action


class DetectionEventRule(BaseModel):
    """
    A rule that can be triggered by a detection event, and executes
    a series of actions.

    Attributes:
        rule_id: str
        name: str
        task_id: str
        model_name: Optional[str]
        severity: DetectionEventSeverity
        detection_event_type: DetectionEventType
        monitoring_target: MonitoringTarget
        actions: List[DetectionEventAction]
    """

    rule_id: str
    name: str
    task_id: str
    model_name: str | None = None
    severity: DetectionEventSeverity | None = None
    detection_event_type: DetectionEventType
    monitoring_target: MonitoringTarget
    monitoring_metric: MonitoringMetric | None = None
    actions: list[SerializeAsAny[DetectionEventAction]]

    # Dynamically instantiate the correct subclass of every ActionModel
    # in the list of actions
    def __init__(self, **kwargs):
        if "actions" in kwargs and kwargs["actions"] is not None:
            deserialize_actions(**kwargs)
        super().__init__(**kwargs)


class IntegrationCredentials(BaseModel):
    """
    Credentials to authenticate to a 3rd party service provider
    via an integration.

    Attributes:
        credentials_id: str
        name: str
        default: bool
        type: ExternalIntegration
    """

    credentials_id: str
    name: str
    default: bool
    type: ExternalIntegration


class AWSCredentials(IntegrationCredentials):
    """
    AWS integration credentials.

    Attributes:
        credentials_id: str
        name: str
        default: bool
        type: ExternalIntegration
        role_arn: The ARN of the role that should be assumed via STS
    """

    role_arn: str


class SecretAWSCredentials(AWSCredentials):
    """
    AWS integration credentials, that also include the external_id
    you need to set up the trust policy on AWS.

    Attributes:
        credentials_id: str
        name: str
        default: bool
        type: ExternalIntegration
        role_arn: The ARN of the IAM role that should be assumed
        external_id: Secret key used to assume the IAM role via STS
    """

    external_id: str

    def generate_trust_policy(self):
        """
        Generates a JSON trust policy that you can copy into the IAM
        role on AWS.
        """

        return f"""
{{
    "Effect": "Allow",
    "Principal": {{
        "AWS": "arn:aws:iam::883313729965:root"
    }},
    "Action": "sts:AssumeRole",
    "Condition": {{
        "StringEquals": {{
            "sts:ExternalId": "{self.external_id}"
        }}
    }}
}}
        """


class AWSCompatibleCredentials(IntegrationCredentials):
    """
    AWS-compatible integration credentials.

    Attributes:
        credentials_id: str
        name: str
        default: bool
        type: ExternalIntegration
        access_key_id: The access key id
        endpoint_url: The endpoint url (if any)
    """

    access_key_id: str
    endpoint_url: str | None = None


class GCPCredentials(IntegrationCredentials):
    """
    GCP integration credentials.

    Attributes:
        credentials_id: str
        name: str
        default: bool
        type: ExternalIntegration
        gcp_project_id: The id of the project on GCP
        client_email: The email that identifies the service account
        client_id: The client id
    """

    gcp_project_id: str
    client_email: str
    client_id: str


class AzureCredentials(IntegrationCredentials):
    """
    Azure integration credentials.

    Attributes:
        app_id: The id of the service principal
    """

    app_id: str
    display_name: str
    tenant: str


class DataSource(BaseModel):
    """
    Generic data source.

    Attributes:
        file_type: FileType
        is_folder: bool
        folder_type: FolderType | None
    """

    file_type: FileType
    is_folder: bool
    folder_type: FolderType | None = None

    @model_validator(mode="after")
    def check_folder_values(self):
        """Validate model by checking that a folder type is provided when data
        source is a folder and that no folder type is provided when data source
        is not a folder"""

        if self.is_folder and self.folder_type is None:
            raise ValueError("no folder type provided")
        elif not self.is_folder and self.folder_type is not None:
            raise ValueError("folder type provided for no folder data source")
        return self


class LocalDataSource(DataSource):
    """
    Use this data source if you want to upload a file from your
    local disk to the ML cube platform cloud.

    Attributes:
        file_type: FileType
        is_folder: bool
        folder_type: FolderType | None
        file_path: str
    """

    file_path: str


class RemoteDataSource(DataSource):
    """
    A source that identifies where data is stored.

    Attributes:
        file_type: FileType
        is_folder: bool
        folder_type: FolderType | None
        credentials_id: The id of the credentials to use to authenticate
            to the remote data source. If None, the default will be used
    """

    credentials_id: str | None = None
    storage_policy: StoragePolicy | None = None

    @abstractmethod
    def get_path(self) -> str:
        """
        Return the path of the object
        """

    @abstractmethod
    def get_source_type(self) -> RawDataSourceType:
        """
        Returns raw data source type
        """


class S3DataSource(RemoteDataSource):
    """
    A source that identifies a file in an S3 bucket.

    Attributes:
        file_type: FileType
        is_folder: bool
        folder_type: FolderType | None
        credentials_id: The id of the credentials to use to authenticate
            to the remote data source. If None, the default will be used
        object_path: str
    """

    object_path: str

    def get_path(self) -> str:
        return self.object_path

    def get_source_type(self) -> RawDataSourceType:
        return RawDataSourceType.AWS_S3


class GCSDataSource(RemoteDataSource):
    """
    A source that identifies a file in a GCS bucket.

    Attributes:
        file_type: FileType
        is_folder: bool
        folder_type: FolderType | None
        credentials_id: The id of the credentials to use to authenticate
            to the remote data source. If None, the default will be used
        object_path: str
    """

    object_path: str

    def get_path(self) -> str:
        return self.object_path

    def get_source_type(self) -> RawDataSourceType:
        return RawDataSourceType.GCS


class AzureBlobDataSource(RemoteDataSource):
    """
    A source that identifies a blob in Azure Storage.

    Attributes:
        file_type: FileType
        is_folder: bool
        folder_type: FolderType | None
        credentials_id: The id of the credentials to use to authenticate
            to the remote data source. If None, the default will be used
        object_path: str
    """

    object_path: str

    def get_path(self) -> str:
        return self.object_path

    def get_source_type(self) -> RawDataSourceType:
        return RawDataSourceType.ABS


class Data(BaseModel):
    """
    Generic data model that contains all information about a data

    Attributes:
        data_structure: DataStructure
        source: DataSource
    """

    data_structure: DataStructure
    source: SerializeAsAny[DataSource]


class TabularData(Data):
    """
    Tabular data model i.e., a data that can be represented via
    DataFrame and is stored in formats like: csv, parquet, json

    Attributes:
        data_structure: DataStructure = DataStructure.TABULAR
        source: DataSource
    """

    data_structure: DataStructure = DataStructure.TABULAR


class EmbeddingData(Data):
    """
    Embedding data model i.e., a data that can be represented via
    DataFrame and is stored in formats like: csv, parquet, json.
    There is only one input that has type array_1

    Attributes:
        data_structure: DataStructure = DataStructure.EMBEDDING
        source: DataSource
    """

    data_structure: DataStructure = DataStructure.EMBEDDING


class ImageData(Data):
    """
    Image data model i.e., images, text or other. Since it is
    composed of multiple files, it needs a mapping between customer ids
    and those files

    Attributes:
        data_structure: DataStructure = DataStructure.IMAGE
        source: DataSource
        mapping_source: DataSource
        embedding_source: DataSource | None
    """

    data_structure: DataStructure = DataStructure.IMAGE
    mapping_source: SerializeAsAny[DataSource]
    embedding_source: SerializeAsAny[DataSource] | None = None


class TextData(Data):
    """
    Text data model for nlp tasks.

    Attributes:
        data_structure: DataStructure = DataStructure.TEXT
        source: DataSource
        embedding_source: DataSource | None
    """

    data_structure: DataStructure = DataStructure.TEXT
    embedding_source: SerializeAsAny[DataSource] | None = None


class SubscriptionPlanInfo(BaseModel):
    """Data model for a subscription plan
    Permission limit set to None means no limit is set
    Expiration date set to None means no expiration is set
    Product key data are set only if a product key is associated to the
    subscription plan

    Attributes:
        subscription_id: str
        type: SubscriptionType
        max_tasks: int | None
        max_users: int | None
        monitoring: bool
        explainability: bool
        retraining: bool
        is_active: bool
        start_date: date
        expiration_date: date | None
        product_key: str | None
        product_key_status: ProductKeyStatus | None
    """

    subscription_id: str
    type: SubscriptionType
    max_tasks: int | None
    max_users: int | None
    monitoring: bool
    explainability: bool
    retraining: bool
    is_active: bool
    start_date: date
    expiration_date: date | None
    product_key: str | None
    product_key_status: ProductKeyStatus | None


class TaskLlmSecReportItem(BaseModel):
    """
    Task LLM security report item model.
    It contains the most important information of
    a LLM security report.

    Attributes:
        id: str
        creation_date: datetime
        name: str
        status: JobStatus
        from_datetime: datetime
        to_datetime: datetime
    """

    id: str
    creation_date: datetime
    name: str
    status: JobStatus
    from_datetime: datetime
    to_datetime: datetime
