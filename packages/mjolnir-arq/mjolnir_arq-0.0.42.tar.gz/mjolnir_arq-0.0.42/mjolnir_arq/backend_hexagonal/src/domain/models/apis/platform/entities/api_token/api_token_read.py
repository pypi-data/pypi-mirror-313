from pydantic import UUID4, BaseModel, field_validator, Field

class ApiTokenRead(BaseModel):
    id: UUID4 = Field(...)
