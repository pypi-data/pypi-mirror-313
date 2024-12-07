from pydantic import UUID4, BaseModel, field_validator, Field

class UserRead(BaseModel):
    id: UUID4 = Field(...)
