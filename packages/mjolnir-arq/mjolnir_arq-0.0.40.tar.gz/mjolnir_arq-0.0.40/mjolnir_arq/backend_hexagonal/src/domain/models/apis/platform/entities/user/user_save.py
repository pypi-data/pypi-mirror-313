from pydantic import BaseModel, Field, UUID4
from typing import Optional
from datetime import datetime

class UserSave(BaseModel):
    platform_id: Optional[UUID4] = Field(default=None)
    password: str = Field(..., max_length=255)
    email: str = Field(..., max_length=255)
    first_name: Optional[str] = Field(default=None, max_length=255)
    last_name: Optional[str] = Field(default=None, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=20)
    refresh_token: Optional[str] = Field(default=None)
    state: bool = Field(default=True)
