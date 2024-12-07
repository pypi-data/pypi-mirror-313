from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, Field


class AccessTokenApi(BaseModel):
    rol_id: str = Field(...)
    rol_code: str = Field(...)
    permissions: List[str] = Field(...)
    date: str = Field(...)
