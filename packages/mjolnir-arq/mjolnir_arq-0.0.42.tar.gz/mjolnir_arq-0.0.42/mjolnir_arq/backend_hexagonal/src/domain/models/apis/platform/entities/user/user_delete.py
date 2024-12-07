from pydantic import UUID4, BaseModel, field_validator, Field

class UserDelete(BaseModel):
    id: UUID4 = Field(...)
