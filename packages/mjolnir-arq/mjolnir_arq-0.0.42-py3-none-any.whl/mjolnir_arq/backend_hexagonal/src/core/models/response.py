from dataclasses import dataclass
from typing import Any, Generic, List, TypeVar, Union

from pydantic import BaseModel
from src.core.enums.message_type import MESSAGE_TYPE
from src.core.enums.notification_type import NOTIFICATION_TYPE

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    message_type: MESSAGE_TYPE
    notification_type: NOTIFICATION_TYPE
    message: str
    response: Union[T, List[Union[T, None]], None] = None

    @classmethod
    def success(
        cls,
        response: Union[T, List[Union[T, None]], None] = None,
        message: str = "",
        message_type: str = MESSAGE_TYPE.NONE.value,
    ) -> "Response[T]":
        return cls(
            response=response,
            message_type=message_type,
            notification_type=NOTIFICATION_TYPE.SUCCESS.value,
            message=message,
        )

    @classmethod
    def success_temporary_message(
        cls,
        response: Union[T, List[Union[T, None]], None] = None,
        message: str = "",
        message_type: str = MESSAGE_TYPE.TEMPORARY.value,
    ) -> "Response[T]":
        return cls(
            response=response,
            message_type=message_type,
            notification_type=NOTIFICATION_TYPE.SUCCESS.value,
            message=message,
        )

    @classmethod
    def info(
        cls,
        response: Union[T, List[Union[T, None]], None] = None,
        message: str = "",
        message_type: str = MESSAGE_TYPE.STATIC.value,
    ) -> "Response[T]":
        return cls(
            response=response,
            message_type=message_type,
            notification_type=NOTIFICATION_TYPE.INFO.value,
            message=message,
        )

    @classmethod
    def warning(
        cls,
        response: Union[T, List[Union[T, None]], None] = None,
        message: str = "",
        message_type: str = MESSAGE_TYPE.TEMPORARY.value,
    ) -> "Response[T]":
        return cls(
            response=response,
            message_type=message_type,
            notification_type=NOTIFICATION_TYPE.WARNING.value,
            message=message,
        )

    @classmethod
    def error(
        cls,
        response: Union[T, List[Union[T, None]], None] = None,
        message: str = "",
        message_type: str = MESSAGE_TYPE.STATIC.value,
    ) -> "Response[T]":
        return cls(
            response=response,
            message_type=message_type,
            notification_type=NOTIFICATION_TYPE.ERROR.value,
            message=message,
        )
