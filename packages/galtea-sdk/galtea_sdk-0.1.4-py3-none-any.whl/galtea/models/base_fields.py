from pydantic import BaseModel, Field

class BaseTemplateFields(BaseModel):
    id: int
    metadata: dict = Field(default_factory=dict)
    