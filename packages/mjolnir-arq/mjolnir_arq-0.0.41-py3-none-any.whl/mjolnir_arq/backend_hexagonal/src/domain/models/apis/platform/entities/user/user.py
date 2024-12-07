from pydantic import BaseModel, Field, UUID4
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: Optional[UUID4] = Field(default=None)
    platform_id: Optional[UUID4] = Field(default=None)
    password: str = Field(..., max_length=255)
    email: str = Field(..., max_length=255)
    first_name: Optional[str] = Field(default=None, max_length=255)
    last_name: Optional[str] = Field(default=None, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=20)
    refresh_token: Optional[str] = Field(default=None)
    state: bool = Field(default=True)
    created_date: Optional[datetime] = Field(default_factory=datetime.now)
    updated_date: Optional[datetime] = Field(default_factory=datetime.now)

    def dict(self, *args, **kwargs):
        exclude = kwargs.pop("exclude", set())
        exclude.update({"created_date", "updated_date"})
        return super().model_dump(*args, exclude=exclude, **kwargs)
