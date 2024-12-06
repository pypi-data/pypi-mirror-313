from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .executors import AbstractExecutor
    from .model import AbstractRequestMessage


class ContentFailure(Exception):
    """Исключение при невозможности сформировать ответ.

    Должно быть обработано и передано в соответствующих тэгах.

    """

    def __init__(
            self,
            content_failure_code: str | int,
            content_failure_comment: str, *args
    ) -> None:
        super().__init__(content_failure_code, content_failure_comment, *args)

        self.content_failure_code = content_failure_code
        self.content_failure_comment = content_failure_comment


class MessageParseException(Exception):
    """Ошибка парсинга тела запроса."""

    def __init__(self, exception: Exception, *args) -> None:
        super().__init__(exception, *args)

        self.exception = exception

    def __str__(self) -> str:
        return f'Ошибка при разборе входящего сообщения - {self.exception}.'


class UnknownMessageTypeException(Exception):
    """Неизвестный тип сообщения СМЭВ (AIO)."""

    def __init__(self, message: AbstractRequestMessage, *args) -> None:
        super().__init__(message, *args)

        self.message = message

    def __str__(self) -> str:
        return f'Неизвестный тип сообщения - {self.message.service_type_name}.'


class ExecutorRegistered(Exception):
    """Исполнитель сервиса уже зарегистрирован."""

    def __init__(self, executor: type[AbstractExecutor], *args) -> None:
        super().__init__(executor, *args)

        self.executor = executor

    def __str__(self) -> str:
        return (
            f'Исполнитель для сервиса {self.executor.service_type_name} '
            f'уже зарегистрирован.')
