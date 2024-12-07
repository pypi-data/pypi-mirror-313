from datetime import datetime
from uuid import UUID
from typing import Any, List, Dict
import ast
import asyncpg
from pydantic import UUID4
from sqlalchemy import column
from src.core.enums.condition_type import CONDITION_TYPE
from src.core.models.filter import FilterManager


from uuid import UUID
from datetime import datetime


def normalize_value(value: Any, target_type: Any) -> Any:
    try:
        if (
            isinstance(value, asyncpg.pgproto.pgproto.UUID)
            or target_type == asyncpg.pgproto.pgproto.UUID
        ):
            return UUID(str(value))
        elif target_type == datetime:
            return datetime.fromisoformat(str(value))
        elif target_type == str:
            return str(value).strip().lower()
        elif target_type == int:
            return int(value)
        elif target_type == float:
            return float(value)
        else:
            return value
    except (ValueError, TypeError):
        return value


def compare_values(
    field_value: Any, filter_obj_value: Any, condition_type: CONDITION_TYPE
) -> bool:

    if condition_type == CONDITION_TYPE.EQUALS:
        return field_value == filter_obj_value
    elif condition_type == CONDITION_TYPE.GREATER_THAN:
        return field_value > filter_obj_value
    elif condition_type == CONDITION_TYPE.LESS_THAN:
        return field_value < filter_obj_value
    elif condition_type == CONDITION_TYPE.GREATER_THAN_OR_EQUAL_TO:
        return field_value >= filter_obj_value
    elif condition_type == CONDITION_TYPE.LESS_THAN_OR_EQUAL_TO:
        return field_value <= filter_obj_value
    elif condition_type == CONDITION_TYPE.DIFFERENT_THAN:
        return field_value != filter_obj_value
    elif condition_type == CONDITION_TYPE.LIKE:
        return (
            filter_obj_value.lower() in str(field_value).lower()
            if field_value
            else False
        )
    elif condition_type == CONDITION_TYPE.IN:
        to_list = ast.literal_eval(filter_obj_value)
        if isinstance(to_list, (list, set, tuple)):
            return field_value in to_list
        else:
            raise ValueError("Condition IN requires a list, set, or tuple.")
    else:
        raise ValueError(f"Unsupported condition: {condition_type}")


def apply_memory_filters(
    obj: Any, filters: List[FilterManager], alias_map: Dict[str, Any]
) -> bool:
    and_conditions = []
    or_groups = {}

    for filter_obj in filters:
        if filter_obj.field in alias_map:

            field_value = getattr(obj, alias_map[filter_obj.field], None)
            field_type = type(field_value)

            field_value = normalize_value(field_value, field_type)
            filter_obj_value = normalize_value(filter_obj.value, field_type)

            try:

                condition = compare_values(
                    field_value, filter_obj_value, filter_obj.condition
                )
            except ValueError as e:
                print(f"Unsupported condition: {filter_obj.condition}. Error: {e}")
                return False

            """ print(
                f"field_value: {field_value} ({field_type}) filter_obj.value: {filter_obj_value} result: {condition}"
            ) """

            if filter_obj.group is not None:
                if filter_obj.group not in or_groups:
                    or_groups[filter_obj.group] = []
                or_groups[filter_obj.group].append(condition)
            else:
                and_conditions.append(condition)

    for group_conditions in or_groups.values():
        and_conditions.append(any(group_conditions))

    return all(and_conditions)
