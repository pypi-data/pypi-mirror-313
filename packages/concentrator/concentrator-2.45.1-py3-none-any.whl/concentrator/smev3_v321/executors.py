from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from types import ModuleType
from typing import TYPE_CHECKING

from .service_types import kinder_conc
from .exceptions import ExecutorRegistered


if TYPE_CHECKING:
    from .model import AbstractRequestMessage
    from .model import ExecutionData


class AbstractExecutor(ABC):
    """Абстрактный класс исполнителя сервиса СМЭВ3 3.2.1 (AIO)."""

    name_service: str
    service_type_name: str
    parser_module: ModuleType = kinder_conc


    @classmethod
    def __subclasshook__(cls, subclass):

        if cls is AbstractExecutor:
            return any(
                True for sub in subclass.__mro__
                if sub.__dict__.get('process') is not None)

        return NotImplemented

    @classmethod
    @abstractmethod
    def process(
            cls, message: AbstractRequestMessage, **kwargs
    ) -> ExecutionData:
        """Запускает выполнение логики обработки сервиса.

        :param message: Сообщение СМЭВ (AIO).

        :return: Обьект данных выполения.

        """


class RepositoryExecutors:
    """Хранилище исполнителей сервисов СМЭВ (AIO)."""

    # Отображение след. формата:
    # {
    #     Наименование типа сервиса: Исполнитель сервиса,
    #     ...
    # }
    __store: dict[str, type[AbstractExecutor]] = {}

    @classmethod
    def set_executor(cls, executor: type[AbstractExecutor]) -> None:
        """Добавляет исполнителя в хранилище исполнителей.

        :param executor: Исполнитель сервиса.

        """

        if executor.service_type_name in cls.__store:
            raise ExecutorRegistered(executor)

        cls.__store[executor.service_type_name] = executor

    @classmethod
    def get_executor(
            cls, message: AbstractRequestMessage
    ) -> type[AbstractExecutor] | None:
        """Определяет исполнителя для полученного сообщения.

        :param message: Сообщение СМЭВ (AIO).

        :return: Возвращает исполнителя для указанного сообщения СМЭВ,
            если он задан в хранилище.

        """
        return cls.__store.get(message.service_type_name)
