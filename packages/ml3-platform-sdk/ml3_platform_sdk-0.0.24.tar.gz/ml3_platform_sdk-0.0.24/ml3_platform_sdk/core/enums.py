from enum import Enum


class HTTPMethod(Enum):
    """
    Enum class to represent HTTP methods
    """

    GET = "GET"
    PUT = "PUT"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"


class DataCategory(Enum):
    """
    **Fields:**

        - INPUT
        - PREDICTION
        - TARGET
        - INPUT_MAPPING
        - TARGET_MAPPING
        - PREDICTION_MAPPING
        - INPUT_ADDITIONAL_EMBEDDING
        - TARGET_ADDITIONAL_EMBEDDING
        - PREDICTION_ADDITIONAL_EMBEDDING
        - USER_INPUT
        - RETRIEVED_CONTEXT
    """

    PREDICTION = "prediction"
    TARGET = "target"
    INPUT = "input"
    INPUT_MAPPING = "input_mapping"
    TARGET_MAPPING = "target_mapping"
    PREDICTION_MAPPING = "prediction_mapping"
    INPUT_ADDITIONAL_EMBEDDING = "input_additional_embedding"
    TARGET_ADDITIONAL_EMBEDDING = "target_additional_embedding"
    PREDICTION_ADDITIONAL_EMBEDDING = "prediction_additional_embedding"


class RawDataSourceType(Enum):
    """
    Enumeration of raw data source types.
    """

    AWS_S3 = "aws_s3"
    GCS = "gcs"
    ABS = "azure_blob_storage"
    LOCAL = "local"
