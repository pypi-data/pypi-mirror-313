from pydantic import BaseModel, ConfigDict


class ML3BaseModel(BaseModel):
    """
    Base BaseModel of pydantic
    """

    model_config = ConfigDict(
        protected_namespaces=(), arbitrary_types_allowed=True
    )
