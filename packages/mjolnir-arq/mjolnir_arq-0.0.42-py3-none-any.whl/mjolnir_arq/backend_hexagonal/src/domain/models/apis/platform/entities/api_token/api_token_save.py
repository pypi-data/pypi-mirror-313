from pydantic import BaseModel, Field, UUID4
from typing import Optional
from datetime import datetime

class ApiTokenSave(BaseModel):
    rol_id: Optional[UUID4] = Field(default=None)
    token: str = Field(...)
    state: bool = Field(default=True)
