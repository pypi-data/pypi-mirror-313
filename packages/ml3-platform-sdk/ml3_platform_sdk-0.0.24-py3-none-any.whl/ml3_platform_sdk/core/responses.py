from pydantic import BaseModel, Field


class StandardErrorResponse(BaseModel):
    """
    Standard error response
    """

    error_code: str = Field(validation_alias="errorCode")
    error_message: str = Field(validation_alias="errorMessage")


class GetPresignedUrlResponse(BaseModel):
    """
    Get presigned url response
    """

    storing_process_id: str
    presigned_url: dict
    expiration_time: str
