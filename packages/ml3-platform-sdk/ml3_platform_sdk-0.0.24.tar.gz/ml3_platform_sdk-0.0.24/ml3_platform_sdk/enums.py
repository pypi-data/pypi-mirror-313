from enum import Enum


class BaseML3Enum(str, Enum):
    """
    Base class for all enums in the ML3 Platform SDK
    """

    def __str__(self):
        return self.value


class TaskType(BaseML3Enum):
    """
    **Fields:**

        - REGRESSION
        - CLASSIFICATION_BINARY
        - CLASSIFICATION_MULTICLASS
        - CLASSIFICATION_MULTILABEL
        - RAG
        - OBJECT_DETECTION
        - SEMANTIC_SEGMENTATION
    """

    REGRESSION = "regression"
    CLASSIFICATION_BINARY = "classification_binary"
    CLASSIFICATION_MULTICLASS = "classification_multiclass"
    CLASSIFICATION_MULTILABEL = "classification_multilabel"
    RAG = "rag"
    OBJECT_DETECTION = "object_detection"
    SEMANTIC_SEGMENTATION = "semantic_segmentation"


class MonitoringStatus(BaseML3Enum):
    """
    **Fields:**

        - OK
        - WARNING
        - DRIFT
    """

    OK = "ok"
    WARNING = "warning"
    DRIFT = "drift"


class KPIStatus(BaseML3Enum):
    """
    **Fields:**

        - NOT_INITIALIZED
        - OK
        - WARNING
        - DRIFT
    """

    NOT_INITIALIZED = "not_initialized"
    OK = "ok"
    WARNING = "warning"
    DRIFT = "drift"


class DataStructure(BaseML3Enum):
    """
    Represents the typology of the data to send

    **Fields:**

        - TABULAR
        - IMAGE
        - TEXT
        - EMBEDDING
    """

    TABULAR = "tabular"
    IMAGE = "image"
    TEXT = "text"
    EMBEDDING = "embedding"


class StoringDataType(BaseML3Enum):
    """
    **Fields:**

        - HISTORICAL
        - REFERENCE
        - PRODUCTION
        - KPI
    """

    HISTORICAL = "historical"
    PRODUCTION = "production"
    TASK_TARGET = "task_target"
    KPI = "kpi"


class FileType(BaseML3Enum):
    """
    **Fields:**

        - CSV
        - JSON
        - PARQUET
        - PNG
        - JPG
        - NPY
    """

    CSV = "csv"
    JSON = "json"
    PARQUET = "parquet"
    PNG = "png"
    JPG = "jpg"
    NPY = "npy"


class FolderType(BaseML3Enum):
    """
    Type of folder

    **Fields**

        - UNCOMPRESSED
        - TAR
        - ZIP
    """

    UNCOMPRESSED = "uncompressed"
    TAR = "tar"
    ZIP = "zip"


class JobStatus(BaseML3Enum):
    """
    **Fields:**

        - IDLE
        - STARTING
        - RUNNING
        - COMPLETED
        - ERROR
        - ROLLBACK_COMPLETE
    """

    IDLE = "idle"
    STARTING = "starting"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    ROLLBACK_COMPLETE = "rollback_complete"


class UserCompanyRole(BaseML3Enum):
    """
    **Fields:**

        - COMPANY_OWNER
        - COMPANY_ADMIN
        - COMPANY_USER
        - COMPANY_NONE
    """

    COMPANY_OWNER = "COMPANY_OWNER"
    COMPANY_ADMIN = "COMPANY_ADMIN"
    COMPANY_USER = "COMPANY_USER"
    COMPANY_NONE = "COMPANY_NONE"


class UserProjectRole(BaseML3Enum):
    """
    **Fields:**

        - PROJECT_ADMIN
        - PROJECT_USER
        - PROJECT_VIEW
    """

    PROJECT_ADMIN = "PROJECT_ADMIN"
    PROJECT_USER = "PROJECT_USER"
    PROJECT_VIEW = "PROJECT_VIEW"


class DetectionEventSeverity(BaseML3Enum):
    """
    **Fields:**

        - LOW
        - MEDIUM
        - HIGH
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class DetectionEventType(BaseML3Enum):
    """
    **Fields:**

        - WARNING_OFF
        - WARNING_ON
        - DRIFT_ON
        - DRIFT_OFF
    """

    WARNING_OFF = "warning_off"
    WARNING_ON = "warning_on"
    DRIFT_ON = "drift_on"
    DRIFT_OFF = "drift_off"


class MonitoringTarget(BaseML3Enum):
    """
    **Fields:**

        - ERROR
        - INPUT
        - CONCEPT
        - PREDICTION
        - INPUT_PREDICTION
        - USER_INPUT
        - RETRIEVED_CONTEXT
        - USER_INPUT_RETRIEVED_CONTEXT
        - USER_INPUT_MODEL_OUTPUT
        - MODEL_OUTPUT_RETRIEVED_CONTEXT
    """

    ERROR = "error"
    INPUT = "input"
    CONCEPT = "concept"
    PREDICTION = "prediction"
    INPUT_PREDICTION = "input_prediction"
    USER_INPUT = "user_input"
    RETRIEVED_CONTEXT = "retrieved_context"
    USER_INPUT_RETRIEVED_CONTEXT = "user_input_retrieved_context"
    USER_INPUT_MODEL_OUTPUT = "user_input_model_output"
    MODEL_OUTPUT_RETRIEVED_CONTEXT = "model_output_retrieved_context"


class MonitoringMetric(BaseML3Enum):
    """

    Tabular:
        - FEATURE

    Text:
        - TEXT_TOXICITY
        - TEXT_EMOTION
        - TEXT_SENTIMENT
        - TEXT_LENGTH

    Model probabilistic output:
        - MODEL_PERPLEXITY
        - MODEL_ENTROPY

    Image:
        - IMAGE_BRIGHTNESS
        - IMAGE_CONTRAST

    Object detection and semantic segmentation:
        - OBJECTS_PER_IMAGE: number of different objects types detected
        - AVERAGE_AREA_PER_OBJECT_TYPE: average area of identified
          objects of the same type
        - QUANTITY_PER_OBJECT_TYPE: number of identified objects of the
          same type
        - TOTAL_OBJECTS: total number of identified objects
        - OBJECT_TYPES_COUNT: total number of identified object types
    """

    # feature monitoring metric requires specification of feature name
    FEATURE = "feature"
    # text metrics
    TEXT_TOXICITY = "text_toxicity"
    TEXT_EMOTION = "text_emotion"
    TEXT_SENTIMENT = "text_sentiment"
    TEXT_LENGTH = "text_length"
    # model probability
    MODEL_PERPLEXITY = "model_perplexity"
    MODEL_ENTROPY = "model_entropy"
    # image metrics
    IMAGE_BRIGHTNESS = "image_brightness"
    IMAGE_CONTRAST = "image_contrast"
    # both object detection and semantic segmentation metrics
    AVERAGE_AREA_PER_OBJECT_TYPE = "average_area_per_object_type"
    QUANTITY_PER_OBJECT_TYPE = "quantity_per_object_type"
    TOTAL_OBJECTS = "total_objects"
    OBJECT_TYPES_COUNT = "object_types_count"


class DetectionEventActionType(BaseML3Enum):
    """
    **Fields:**

        - DISCORD_NOTIFICATION
        - SLACK_NOTIFICATION
        - EMAIL_NOTIFICATION
        - TEAMS_NOTIFICATION
        - MQTT_NOTIFICATION
        - RETRAIN
        - NEW_PLOT_CONFIGURATION
    """

    DISCORD_NOTIFICATION = "discord_notification"
    SLACK_NOTIFICATION = "slack_notification"
    EMAIL_NOTIFICATION = "email_notification"
    TEAMS_NOTIFICATION = "teams_notification"
    MQTT_NOTIFICATION = "mqtt_notification"
    RETRAIN = "retrain"
    NEW_PLOT_CONFIGURATION = "new_plot_configuration"


class ModelMetricName(BaseML3Enum):
    """
    Name of the model metrics that is associated with the model

    **Fields:**
        - RMSE
        - RSQUARE
        - ACCURACY
        - AVERAGE_PRECISION
    """

    RMSE = "rmse"
    RSQUARE = "rsquare"
    ACCURACY = "accuracy"
    AVERAGE_PRECISION = "average_precision"


class SuggestionType(BaseML3Enum):
    """
    Enum to specify the preferred
    type of suggestion

    **Fields:**
        - SAMPLE_WEIGHTS
        - RESAMPLED_DATASET
    """

    SAMPLE_WEIGHTS = "sample_weights"
    RESAMPLED_DATASET = "resampled_dataset"


class ApiKeyExpirationTime(BaseML3Enum):
    """
    **Fields:**

        - ONE_MONTH
        - THREE_MONTHS
        - SIX_MONTHS
        - ONE_YEAR
        - NEVER

    """

    ONE_MONTH = "one_month"
    THREE_MONTHS = "three_months"
    SIX_MONTHS = "six_months"
    ONE_YEAR = "one_year"
    NEVER = "never"


class ExternalIntegration(BaseML3Enum):
    """
    An integration with a 3rd party service provider

    **Fields:**
        - AWS
        - GCP
        - AZURE
        - AWS_COMPATIBLE
    """

    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"
    AWS_COMPATIBLE = "aws_compatible"


class StoragePolicy(BaseML3Enum):
    """
    Enumeration that specifies the storage policy for the data sent to
    ML cube Platform

    **Fields:**
        - MLCUBE: data are copied and stored into the ML cube Platform
            cloud
        - CUSTOMER: data are kept only in your cloud and ML cube
            Platform will access to this storage source every time
            it needs to read data
    """

    MLCUBE = "mlcube"
    CUSTOMER = "customer"


class RetrainTriggerType(BaseML3Enum):
    """
    Enumeration of the possible retrain triggers

    **Fields:**:
        - AWS_EVENT_BRIDGE
        - GCP_PUBSUB
        - AZURE_EVENT_GRID
    """

    AWS_EVENT_BRIDGE = "aws_event_bridge"
    GCP_PUBSUB = "gcp_pubsub"
    AZURE_EVENT_GRID = "azure_event_grid"


class Currency(BaseML3Enum):
    """
    Currency of to use for the Task

    **Fields:**
        - EURO
        - DOLLAR
    """

    EURO = "euro"
    DOLLAR = "dollar"


class DataType(BaseML3Enum):
    """
    Data type enum
    Describe data type of input

    **Fields:**
        - FLOAT
        - STRING
        - CATEGORICAL
        - ARRAY_1
        - ARRAY_2
        - ARRAY_3
    """

    FLOAT = "float"
    STRING = "string"
    CATEGORICAL = "categorical"

    # array can have multiple dimensions each of them with n elemens
    # for instance, an image is an array with c channels, hence it is
    # an array_3 with [h, w, c] where h is the number of pixels over
    # the height axis, w over the width axis and c is the number of
    # channels (3 for RGB images).

    # array [h]  # noqa
    ARRAY_1 = "array_1"
    # array [h, w]  # noqa
    ARRAY_2 = "array_2"
    # array [h, w, c]  # noqa
    ARRAY_3 = "array_3"


class ColumnRole(BaseML3Enum):
    """
    Column role enum
    Describe the role of a column

    **Fields:**
        - INPUT
        - INPUT_MASK
        - PREDICTION
        - TARGET
        - ERROR
        - ID
        - TIME_ID
        - INPUT_ADDITIONAL_EMBEDDING
        - TARGET_ADDITIONAL_EMBEDDING
        - PREDICTION_ADDITIONAL_EMBEDDING
        - USER_INPUT
        - RETRIEVED_CONTEXT
    """

    INPUT = "input"
    INPUT_MASK = "input_mask"
    PREDICTION = "prediction"
    TARGET = "target"
    ERROR = "error"
    ID = "id"
    TIME_ID = "time_id"
    INPUT_ADDITIONAL_EMBEDDING = "input_additional_embedding"
    TARGET_ADDITIONAL_EMBEDDING = "target_additional_embedding"
    PREDICTION_ADDITIONAL_EMBEDDING = "prediction_additional_embedding"
    USER_INPUT = "user_input"
    RETRIEVED_CONTEXT = "retrieved_context"


class ColumnSubRole(BaseML3Enum):
    """
    Column subrole enum
    Describe the subrole of a column

    Subroles for ColumnRole.INPUT in RAG settings:

    - RAG_USER_INPUT
    - RAG_RETRIEVED_CONTEXT
    - RAG_SYS_PROMPT

    Subroles for ColumnRole.PREDICTION:

    - MODEL_PROBABILITY
    - OBJECT_LABEL_PREDICTION

    Subroles for ColumnRole.TARGET:

    - OBJECT_LABEL_TARGET
    """

    RAG_USER_INPUT = "user_input"
    RAG_RETRIEVED_CONTEXT = "retrieved_context"
    MODEL_PROBABILITY = "model_probability"
    OBJECT_LABEL_TARGET = "object_label_target"
    OBJECT_LABEL_PREDICTION = "object_label_prediction"


class TextLanguage(BaseML3Enum):
    """Enumeration of text language used in nlp tasks.

    **Fields:**
        - ITALIAN
        - ENGLISH
        - MULTILANGUAGE
    """

    ITALIAN = "italian"
    ENGLISH = "english"
    MULTILANGUAGE = "multilanguage"


class ImageMode(BaseML3Enum):
    """
    Image mode enumeration

    **Fields:**
        - RGB
        - RGBA
        - GRAYSCALE
    """

    RGB = "rgb"
    RGBA = "rgba"
    GRAYSCALE = "grayscale"


class SubscriptionType(BaseML3Enum):
    """Type of subscription plan of a company

    **Fields:**:
        - CLOUD: subscription plan for web app or sdk access
        - EDGE: subscription plan for edge deployment
    """

    CLOUD = "cloud"
    EDGE = "edge"


class ProductKeyStatus(BaseML3Enum):
    """Status of a product key

    **Fields:**:
        - NEW = generated but not yet used product key
        - VALIDATING = validation requested from client
        - IN_USE = validated product key, client activated
    """

    NEW = "new"
    VALIDATING = "validating"
    IN_USE = "in use"


class SemanticSegTargetType(BaseML3Enum):
    """Format of the target and prediction for the semantic segmentation
    task.

    POLYGON: each identified object is represented by the vertices of
        the polygon
    """

    POLYGON = "polygon"
