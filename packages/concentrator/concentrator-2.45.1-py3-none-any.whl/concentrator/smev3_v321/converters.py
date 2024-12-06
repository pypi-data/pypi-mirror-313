from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
import sys
import traceback


if TYPE_CHECKING:
    from aio_client.base.exceptions import AioClientException


class AbstractExceptionConverter(ABC):
    """Абстрактный класс преобразователя сообщения из ошибки (СМЭВ 3)."""

    @classmethod
    @abstractmethod
    def convert(cls, exception: Exception) -> str:
        """Сообщение об ошибке."""


class ExceptionConverter(AbstractExceptionConverter):
    """Конвертер стандартных ошибок.

    Вызывает __str__() указанного исключения.

    """

    @classmethod
    def convert(cls, exception: Exception) -> str:
        return f'{exception}'


class AioClientExceptionConverter(AbstractExceptionConverter):
    """"""

    @classmethod
    def convert(cls, exception: AioClientException) -> str:
        return f'{exception.message} (код ошибки - {exception.code})'


class BroadExceptionConverter(AbstractExceptionConverter):
    """Конвертер исключения с полным трейсом."""

    @classmethod
    def convert(cls, exception: Exception) -> str:
        return '\n'.join(traceback.format_exception(*sys.exc_info()))
