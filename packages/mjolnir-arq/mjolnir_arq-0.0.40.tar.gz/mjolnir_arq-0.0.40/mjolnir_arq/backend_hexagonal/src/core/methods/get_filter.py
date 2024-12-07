from typing import Any, List, TypeVar

from sqlalchemy import inspect
from src.core.enums.condition_type import CONDITION_TYPE
from src.core.models.base import Base
from src.core.models.filter import FilterManager

T = TypeVar("T", bound=Base)


def get_filter(query: Any, filters: List[FilterManager], entity: T) -> Any:
    valid_columns = {column.key for column in inspect(entity).mapper.column_attrs}
    for filter_obj in filters:
        if filter_obj.field in valid_columns:
            column = getattr(entity, filter_obj.field)
            if filter_obj.condition == CONDITION_TYPE.EQUALS.value:
                query = query.filter(column == filter_obj.value)
            elif filter_obj.condition == CONDITION_TYPE.GREATER_THAN.value:
                query = query.filter(column > filter_obj.value)
            elif filter_obj.condition == CONDITION_TYPE.LESS_THAN.value:
                query = query.filter(column < filter_obj.value)
            elif filter_obj.condition == CONDITION_TYPE.GREATER_THAN_OR_EQUAL_TO.value:
                query = query.filter(column >= filter_obj.value)
            elif filter_obj.condition == CONDITION_TYPE.LESS_THAN_OR_EQUAL_TO.value:
                query = query.filter(column <= filter_obj.value)
            elif filter_obj.condition == CONDITION_TYPE.DIFFERENT_THAN.value:
                query = query.filter(column != filter_obj.value)
            elif filter_obj.condition == CONDITION_TYPE.LIKE.value:
                query = query.filter(column.like(f"%{filter_obj.value}%"))

    return query
