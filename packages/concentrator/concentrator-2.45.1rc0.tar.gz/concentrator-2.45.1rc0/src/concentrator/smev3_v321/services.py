from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Iterator
from datetime import datetime
from typing import TYPE_CHECKING

from aio_client.base import RequestTypeEnum
from aio_client.base.exceptions import AioClientException
from aio_client.provider.api import get_requests
from django.db.transaction import atomic
from lxml import etree
from m3.plugins import ExtensionManager

from kinder import logger
from kinder.core.utils.address import GarConnectionException
from kinder.webservice.smev3.utils.error_logging import (
    GarTimeoutExceptionLogger)

from concentrator import settings

from .constants import LOG_TIME_FORMAT
from .constants import GAR_RESEND_MESSAGE
from .converters import AioClientExceptionConverter
from .converters import BroadExceptionConverter
from .converters import ExceptionConverter
from .exceptions import MessageParseException
from .exceptions import UnknownMessageTypeException
from .executors import RepositoryExecutors
from .loggers import OutgoingMessageSmevLogLogger
from .model import FormDataMessage
from .service_types import kinder_conc
from .settings import GAR_TIMEOUT_RESEND_SECONDS
from .tasks import GarTimeoutFormDataResendTask


if TYPE_CHECKING:
    from .converters import AbstractExceptionConverter
    from .loggers import AbstractMessageLogger
    from .model import AbstractRequestMessage
    from .model import ExecutionData


class AbstractMessageProcessingService(ABC):
    """Абстрактный класс обработки сообщения СМЭВ (AIO)."""

    description: str

    message_type: str

    message_wrapper_cls: type[AbstractRequestMessage]

    logger_cls: type[AbstractMessageLogger]

    # Отображение ожидаемых исключений вида:
    # {Класс исключения: Класс логгера исключения}
    catchable_exceptions: dict[
        type[Exception], type[AbstractExceptionConverter]
    ] = {
        AioClientException: AioClientExceptionConverter,
    }

    __execution_log: list[str]

    @abstractmethod
    def get_messages(self) -> Iterator[message_wrapper_cls]:
        """Возвращает итератор по сообщениям СМЭВ (AIO)."""

    def create_log(self, message: message_wrapper_cls, **kwargs) -> None:
        """Создает лог запроса.

        :param message: Входящее сообщение.
        :param kwargs: Дополнительные параметры для записи лога.

        """
        self.logger_cls.create_log(message, **kwargs)

    def process_error(
            self, message: message_wrapper_cls,
            error: Exception,
            converter: type[AbstractExceptionConverter]
    ) -> None:
        """Обработка ошибки.

        Сохраняет комментарий хода выполнения обработки сообщения.
        Создает лог запроса.

        :param message: Входящее сообщение.
        :param error: Ошибка.
        :param converter: Конвертер для ошибки.

        """

        error_message = converter.convert(error)
        self.__execution_log.append(
            f'Ответ на сообщение {message.origin_message_id} '
            f'не удалось отправить - {error_message}')
        self.create_log(message, result=error_message)

    @abstractmethod
    def process_message(
            self, message: message_wrapper_cls, **kwargs
    ) -> ExecutionData:
        """Выполняет обработку сообщения СМЭВ (AIO).

        :param message: Входящее сообщение СМЭВ.

        :return: Возвращает объект с информацией о выполнении.

        """

    def run(self, *args, **kwargs) -> None:
        """Запускает процесс выполнения обработка входящих сообщения СМЭВ (AIO).


        Выполняет запись соответствующих комментариев по ходу выполения
        обработки сообщения для дальнейшего логирования в файл на сервере
        (Уровень лога Info).

        Запрашивает все запросы к системе у AIO клиента и оборачивает
        в спец. класс обертку. После выполняет обработку каждого полученного
        сообщения с логированием.

        :param args: Параметры выполнения.
        :param kwargs: Доп. параметры выполения.

        """

        _get_current_time = lambda: datetime.now().strftime(LOG_TIME_FORMAT) # noqa

        self.__execution_log = [
            self.description,
            f'Получаем запросы {self.message_type} ({_get_current_time()})']

        message_count = 0
        error_message_count = 0

        for message_count, message in enumerate(self.get_messages(), start=1):

            is_error = True

            self.__execution_log.append(
                f'Отправка ответа в СМЭВ на сообщение - '
                f'{message.origin_message_id}')

            try:
                with atomic():
                    execution_result = self.process_message(message, **kwargs)
                    self.create_log(message, **execution_result.logging_data)
            except tuple(self.catchable_exceptions) as exc:
                self.process_error(
                    message, exc, self.catchable_exceptions[exc.__class__])
                continue
            except Exception as exc:
                self.process_error(message, exc, BroadExceptionConverter)
                continue
            else:
                is_error = False
            finally:
                if is_error:
                    error_message_count += 1

        self.__execution_log.append(
            f'Общее количество сообщений - {message_count}')

        if error_message_count:
            self.__execution_log.append(
                f'Количество сообщений, по которым не удалось отправить ответ '
                f'- {error_message_count}')

        self.__execution_log.append(
            f'Время завершения ({_get_current_time()})')

        logger.info('\n'.join(self.__execution_log))


class FormDataMessageProcessingService(AbstractMessageProcessingService):
    """Класс обработки сообщения СМЭВ FormData (AIO)."""

    description: str = 'Взаимодействие с формой-концентратором по СМЭВ 3'

    message_type: str = settings.SMEV3_FORM_DATA_MESSAGE_TYPE

    message_wrapper_cls: type[FormDataMessage] = FormDataMessage

    logger_cls: type[AbstractMessageLogger] = OutgoingMessageSmevLogLogger

    catchable_exceptions: dict[
        type[Exception], type[AbstractExceptionConverter]
    ] = {
        **AbstractMessageProcessingService.catchable_exceptions,
        MessageParseException: ExceptionConverter,
        UnknownMessageTypeException: ExceptionConverter,
        GarConnectionException: GarTimeoutExceptionLogger,
    }

    @classmethod
    def get_method_verbose_name(cls) -> str:
        """Возвращает наименование метода."""
        return f'{cls.message_type} ({cls.description})'

    def get_messages(self) -> Iterator[message_wrapper_cls]:
        """Возвращает итератор по сообщениям СМЭВ с типом ВС FormData (AIO)."""
        for message in get_requests(self.message_type):
            yield self.message_wrapper_cls(message)

    def create_log(self, message: message_wrapper_cls, **kwargs) -> None:
        """Создает лог запроса.

        :param message: Входящее сообщение.
        :param kwargs: Дополнительные параметры для записи лога.

        """

        default_options = {
            'service_address':
                RequestTypeEnum.get_url(RequestTypeEnum.PR_POST),
            'method_verbose_name': self.get_method_verbose_name(),
        }

        super().create_log(message, **{**default_options, **kwargs})

    @staticmethod
    def get_executors_repository(message: message_wrapper_cls):
        """Возвращает класс исполнителей запроса (СМЭВ3 3.2.1 или 4.0.1)

        :param message: Запрос, обернутый в FormDataMessage
        :return: Класс исполнителей запроса (СМЭВ3 3.2.1 или 4.0.1)
        """
        return ExtensionManager().execute(
            'concentrator.smev3_v4.extensions.get_executors', message) or RepositoryExecutors

    def process_message(
            self, message: message_wrapper_cls, **kwargs
    ) -> ExecutionData:
        """Выполняет обработку сообщения СМЭВ FormData (AIO).

        :param message: Входящее сообщение СМЭВ.

        :return: Возвращает объект с информацией о выполнении.

        """

        # Выполняет разбор входящего сообщения.
        try:
            _ = message.parse_body
        except (
                etree.XMLSyntaxError, kinder_conc.GDSParseError, ValueError
        ) as exc:
            raise MessageParseException(exc)

        # Выполняет поиск подходящего исполнителя для данного сервиса.
        # Так как для FormData сразу нельзя определить,
        # какой сервис требуется, то просматривает по следующему тэгу.
        executor = self.get_executors_repository(message).get_executor(message)

        if executor is None:
            raise UnknownMessageTypeException(message)

        try:
            return executor.process(message, **kwargs)
        except GarConnectionException:
            GarTimeoutFormDataResendTask().apply_async(
                (message.message, ),
                countdown=GAR_TIMEOUT_RESEND_SECONDS,
            )

            raise GarConnectionException(
                message=GAR_RESEND_MESSAGE.format(
                    time=GAR_TIMEOUT_RESEND_SECONDS)
            )
