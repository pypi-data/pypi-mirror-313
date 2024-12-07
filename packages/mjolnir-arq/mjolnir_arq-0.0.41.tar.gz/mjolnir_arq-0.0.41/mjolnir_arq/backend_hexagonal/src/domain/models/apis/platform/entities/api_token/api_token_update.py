from pydantic import BaseModel, Field, UUID4
from typing import Optional
from datetime import datetime

class ApiTokenUpdate(BaseModel):
    id: UUID4 = Field(...)
    rol_id: UUID4 = Field(...)
    token: str = Field(...)
    state: bool = Field(default=True)
