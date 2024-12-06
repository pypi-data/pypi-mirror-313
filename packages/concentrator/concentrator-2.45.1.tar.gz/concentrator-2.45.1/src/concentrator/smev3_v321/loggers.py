from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Any

from educommon.ws_log.models import SmevLog
from educommon.ws_log.models import SmevSourceEnum


if TYPE_CHECKING:
    from django.db.models import Model

    from .model import AbstractRequestMessage


class AbstractMessageLogger(ABC):
    """Абстрактный класс логгера сообщения для взаимодействия со СМЭВ (AIO)."""

    @classmethod
    @abstractmethod
    def create_log(cls, message: AbstractRequestMessage, *args, **kwargs):
        """Выполняет создание лога для сообщения."""


class AbstractMessageDBLogger(AbstractMessageLogger):
    """Абстрактный класс логгера сообщения в БД для взаимодействия со СМЭВ (AIO).
    """

    log_model_cls: type[Model]

    @classmethod
    @abstractmethod
    def get_log_data(
            cls, message: AbstractRequestMessage, *args, **kwargs
    ) -> dict[str, Any]:
        """Возвращает данные для лога сообщения."""

    @classmethod
    def get_log(
            cls, message: AbstractRequestMessage, *args, **kwargs
    ) -> log_model_cls:
        """Возвращает лог для сообщения."""
        return cls.log_model_cls(**cls.get_log_data(message, *args, **kwargs))

    @classmethod
    def create_log(cls, message: AbstractRequestMessage, *args, **kwargs):
        """Выполняет создание лога для сообщения в БД."""
        return cls.get_log(message, *args, **kwargs).save()


class AbstractMessageSmevLogLogger(AbstractMessageDBLogger, ABC):
    """Абстрактный класс логгера сообщения в БД (SmevLog)
    для взаимодействия со СМЭВ (AIO).

    """

    log_model_cls: type[SmevLog] = SmevLog


class OutgoingMessageSmevLogLogger(AbstractMessageSmevLogLogger):
    """Класс логгера исходящего сообщения в БД (SmevLog)
    для взаимодействия со СМЭВ (AIO).

    """

    @classmethod
    def get_log_data(
            cls, message: AbstractRequestMessage, *args, **kwargs
    ) -> dict[str, Any]:
        """Возвращает данные для СМЭВ лога сообщения."""

        default_options = {
            'service_address': None,
            'direction': cls.log_model_cls.OUTGOING,
            'interaction_type': cls.log_model_cls.IS_SMEV,
            'source': SmevSourceEnum.CONCENTRATOR,
            'request': message.body,
            'result': None,
        }

        return {**default_options, **kwargs}
