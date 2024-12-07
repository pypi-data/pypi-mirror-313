from typing import Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field, ConfigDict
from src.core.models.access_token import AccessToken
from src.core.enums.response_type import RESPONSE_TYPE


class Config(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    db: Optional[Any] = None
    async_db: Optional[AsyncSession] = None
    language: Optional[str] = None
    request: Optional[Any] = None
    response_type: RESPONSE_TYPE = Field(default=RESPONSE_TYPE.DICT.value)
    token: Optional[AccessToken] = Field(default=None)
    token_code: Optional[str] = Field(default=None)
