from typing import Any
import ast
from src.core.enums.condition_type import CONDITION_TYPE
from src.core.models.base import Base
from src.core.models.filter import FilterManager
from sqlalchemy import and_, or_
from sqlalchemy.sql.elements import Label


def get_filter_with_alias(
    query: Any, filters: list[FilterManager], alias_map: dict[str, Label]
) -> Any:
    and_conditions = []
    or_groups = {}

    for filter_obj in filters:

        if filter_obj.field in alias_map:
            column = alias_map[filter_obj.field]

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
                to_list = ast.literal_eval(filter_obj.value)
                if isinstance(to_list, (list, set, tuple)):
                    condition = column.in_(to_list)
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
