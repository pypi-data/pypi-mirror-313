from typing import Any, List, Optional
from pydantic import BaseModel, Field
from src.core.enums.context import CONTEXT


class MessageCoreEntity(BaseModel):
    key: str = Field(...)
    context: str = Field(default=CONTEXT.BACKEND.value) 