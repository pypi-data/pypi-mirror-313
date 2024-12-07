from typing import Any, List, Optional
from pydantic import BaseModel, Field

from src.core.enums.condition_type import CONDITION_TYPE


class FilterManager(BaseModel):
    field: str = Field(...)
    condition: CONDITION_TYPE = Field(...)
    value: Any = Field(...)


class Pagination(BaseModel):
    skip: Optional[int] = Field(default=None)
    limit: Optional[int] = Field(default=None)
    all_data: Optional[bool] = Field(default=False)
    filters: Optional[List[FilterManager]] = Field(default=None)
