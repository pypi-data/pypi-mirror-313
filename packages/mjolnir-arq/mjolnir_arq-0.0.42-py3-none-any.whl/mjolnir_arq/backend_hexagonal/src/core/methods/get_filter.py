from typing import Any, TypeVar

from sqlalchemy import inspect
from src.core.enums.condition_type import CONDITION_TYPE
from src.core.models.base import Base
from src.core.models.filter import FilterManager
from sqlalchemy import and_, or_, inspect
from sqlalchemy.sql.elements import Label

T = TypeVar("T", bound=Base)


def get_filter(query: Any, filters: list[FilterManager], entity: Any) -> Any:
    valid_columns = {column.key for column in inspect(entity).mapper.column_attrs}

    and_conditions = []
    or_groups = {}

    for filter_obj in filters:
        if filter_obj.field in valid_columns:
            column = getattr(entity, filter_obj.field)

            if filter_obj.condition == CONDITION_TYPE.EQUALS:
                condition = column == filter_obj.value
            elif filter_obj.condition == CONDITION_TYPE.GREATER_THAN:
                condition = column > filter_obj.value
            elif filter_obj.condition == CONDITION_TYPE.LESS_THAN:
                condition = column < filter_obj.value
            elif filter_obj.condition == CONDITION_TYPE.GREATER_THAN_OR_EQUAL_TO:
                condition = column >= filter_obj.value
            elif filter_obj.condition == CONDITION_TYPE.LESS_THAN_OR_EQUAL_TO:
                condition = column <= filter_obj.value
            elif filter_obj.condition == CONDITION_TYPE.DIFFERENT_THAN:
                condition = column != filter_obj.value
            elif filter_obj.condition == CONDITION_TYPE.LIKE:
                condition = column.like(f"%{filter_obj.value}%")
            elif filter_obj.condition == CONDITION_TYPE.IN:
                if isinstance(filter_obj.value, (list, set, tuple)):
                    condition = column.in_(filter_obj.value)
                else:
                    raise ValueError("Condition IN requires a list, set, or tuple.")
            else:
                raise ValueError(f"Unsupported condition: {filter_obj.condition}")

            if filter_obj.group is not None:
                if filter_obj.group not in or_groups:
                    or_groups[filter_obj.group] = []
                or_groups[filter_obj.group].append(condition)
            else:
                and_conditions.append(condition)

    for group_conditions in or_groups.values():
        and_conditions.append(or_(*group_conditions))

    if and_conditions:
        query = query.filter(and_(*and_conditions))

    return query
