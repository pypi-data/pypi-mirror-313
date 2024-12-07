from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, Field


class AccessToken(BaseModel):
    rol_id: str = Field(...)
    rol_code: str = Field(...)
    user_id: str = Field(...)
    location_id: str = Field(...)
    currency_id: str = Field(...)
    company_id: str = Field(...)
    token_expiration_minutes: int = Field(...)
    exp: Optional[datetime] = Field(default=None)
    permissions: List[str] = Field(...)
