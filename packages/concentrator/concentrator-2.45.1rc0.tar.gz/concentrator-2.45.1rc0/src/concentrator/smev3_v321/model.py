from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from types import ModuleType
from typing import TYPE_CHECKING
from typing import Any

from django.utils.functional import cached_property
from m3.plugins import ExtensionManager

from .service_types import kinder_conc


if TYPE_CHECKING:
    from requests import Response


@dataclass
class AbstractRequestMessage(ABC):
    """Абстрактный класс обертка сообщения СМЭВ (AIO) для RequestMessage."""

    message: dict[str, Any]

    @property
    def message_id(self) -> str:
        """Уникальный идентификатор сообщения."""
        return self.message.get('message_id')

    @property
    def origin_message_id(self) -> str | None:
        """Уникальный идентификатор цепочки взаимодействия в АИО."""
        return self.message.get('origin_message_id')

    @property
    def body(self) -> str:
        """Бизнес-данные запроса."""
        return self.message.get('body')

    @property
    def message_type(self) -> str:
        """Вид сведений."""
        return self.message.get('message_type')

    @property
    def attachments(self) -> list[str] | str | None:
        """Вложения запроса."""
        return self.message.get('attachments')

    @cached_property
    @abstractmethod
    def parse_body(self) -> Any:
        """Распарсенное тело запроса."""

    @cached_property
    @abstractmethod
    def service_type_name(self) -> Any:
        """Наименование типа сервиса."""


@dataclass
class AbstractGetProviderRequest(AbstractRequestMessage, ABC):
    """Абстрактный класс обертка сообщения СМЭВ (AIO) для GetProviderRequest."""

    @property
    def is_test_message(self) -> bool:
        """Признак тестового взаимодействия."""
        return self.message.get('is_test_message')

    @property
    def replay_to(self) -> str:
        """Индекс сообщения в СМЭВ."""
        return self.message.get('replay_to')


@dataclass
class FormDataMessage(AbstractGetProviderRequest):
    """Класс обертка сообщения СМЭВ FormData (AIO)."""

    @cached_property
    def parsing_module(self) -> ModuleType:
        """Модуль для парсинга запроса по СМЭВ3 версии 3.2.1 или 4.0.1"""

        return ExtensionManager().execute(
            'concentrator.smev3_v4.extensions.get_parsing_module', self.body
        ) or kinder_conc

    @cached_property
    def parse_body(self) -> 'FormDataType':
        """Сгенерированное тело."""

        return self.parsing_module.parseString(self.body, silence=True)

    @cached_property
    def service_type_name(self) -> str | None:
        """Наименование типа сервиса."""

        return next(
            iter(_type.__class__.__name__
                 for _type in self.parse_body.__dict__.values()
                 if isinstance(_type, self.parsing_module.GeneratedsSuper)), None)


@dataclass
class ExecutionData:
    """Класс обертка данных выполнения исполнителя сервиса."""

    response: Response | None
    logging_data: dict
