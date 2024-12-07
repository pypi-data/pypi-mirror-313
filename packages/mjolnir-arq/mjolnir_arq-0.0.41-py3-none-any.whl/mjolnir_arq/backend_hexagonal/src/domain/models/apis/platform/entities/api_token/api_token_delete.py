from pydantic import UUID4, BaseModel, field_validator, Field

class ApiTokenDelete(BaseModel):
    id: UUID4 = Field(...)
