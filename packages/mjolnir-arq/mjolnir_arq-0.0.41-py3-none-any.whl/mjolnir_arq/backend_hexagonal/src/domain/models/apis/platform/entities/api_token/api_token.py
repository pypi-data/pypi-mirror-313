from pydantic import BaseModel, Field, UUID4
from typing import Optional
from datetime import datetime

class ApiToken(BaseModel):
    id: Optional[UUID4] = Field(default=None)
    rol_id: Optional[UUID4] = Field(default=None)
    token: str = Field(...)
    state: bool = Field(default=True)
    created_date: Optional[datetime] = Field(default_factory=datetime.now)
    updated_date: Optional[datetime] = Field(default_factory=datetime.now)

    def dict(self, *args, **kwargs):
        exclude = kwargs.pop("exclude", set())
        exclude.update({"created_date", "updated_date"})
        return super().model_dump(*args, exclude=exclude, **kwargs)
