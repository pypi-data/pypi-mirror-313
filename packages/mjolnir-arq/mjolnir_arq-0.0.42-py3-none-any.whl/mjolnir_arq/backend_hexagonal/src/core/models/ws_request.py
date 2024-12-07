
from pydantic import BaseModel, Field


class WSRequest(BaseModel):
    language: str = Field(...)
    token: str = Field(...)
