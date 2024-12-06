import datetime
import sys
import traceback

from celery import states
from celery.schedules import crontab
from lxml import etree

from aio_client.base import RequestTypeEnum
from aio_client.base.exceptions import AioClientException
from aio_client.provider.api import get_requests
from educommon.ws_log.models import SmevLog
from educommon.ws_log.models import SmevSourceEnum
from kinder.core.async_tasks.tasks import PeriodicAsyncTask

from concentrator import settings
from concentrator.smev3.base.utils import SMEV3RepositoryExecutors
from concentrator.smev3.service_types import kinder_conc


class Smev3PeriodicAsyncTask(PeriodicAsyncTask):
    """Периодическая таска, которая проверяет наличие в клиенте заявок
    с видом сведений message_type, запускает по ним формирование
    и отправку ответа.
    """

    message_type = settings.SMEV3_FORM_DATA_MESSAGE_TYPE

    run_every = crontab(
        minute=settings.SMEV3_FORM_DATA_TASK_EVERY_MINUTE,
        hour=settings.SMEV3_FORM_DATA_TASK_EVERY_HOUR)

    description = 'Взаимодействие с формой-концентратором по СМЭВ 3'
    stop_executing = False
    LOG_TIME_FORMAT = '%d.%m.%Y %H:%M'

    _error_key = (
        'Ответ на сообщение {} не удалось отправить')

    def log(self, message, result=None, logging_data=None):
        """Логирование запроса СМЭВ 3.

        :param message: Сообщение
        :param result: Результат
        :param logging_data: Дополнительные параметры
        """

        logging_data = logging_data or {}

        data = {
            'service_address':
                RequestTypeEnum.get_url(RequestTypeEnum.PR_POST),
            'method_verbose_name': f'{self.message_type} ({self.description})',
            'direction': SmevLog.OUTGOING,
            'interaction_type': SmevLog.IS_SMEV,
            'source': SmevSourceEnum.CONCENTRATOR,
            'request': message.get('body'),
            'result': result,
            **logging_data
        }

        return SmevLog(**data).save()

    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)

        values = {
            'Время начала':
                datetime.datetime.now().strftime(self.LOG_TIME_FORMAT),
        }
        self.set_progress(
            progress=f'Получаем запросы {self.message_type}',
            values=values)

        result = get_requests(self.message_type)
        values['Кол-во сообщений'] = str(len(result))
        error_list = []

        for message in result:
            origin_message_id = message['origin_message_id']
            values[f'Сообщение {origin_message_id}'] = (
                'Отправка ответа в СМЭВ')

            body = message.get('body')

            try:
                request_body = kinder_conc.parseString(body)
            except (
                etree.XMLSyntaxError, kinder_conc.GDSParseError, ValueError
            ) as exc:
                error_list.append(origin_message_id)
                error_message = (
                    f'Ошибка при разборе входящего сообщения - {exc}')
                values[self._error_key.format(origin_message_id)] = (
                    error_message)
                self.log(message, error_message)
                continue

            executor = SMEV3RepositoryExecutors.get_executor(request_body)
            if executor:
                try:
                    response = executor(message, request_body)
                    self.log(message, logging_data=response.logging_data)
                except AioClientException as exc:
                    error_list.append(origin_message_id)
                    error_message = (
                        f'{exc.message} (код ошибки - {exc.code})')
                    values[self._error_key.format(origin_message_id)] = (
                        error_message)
                    self.log(message, error_message)
                    continue
                except Exception:
                    error_list.append(origin_message_id)
                    error_message = (
                        '\n'.join(traceback.format_exception(*sys.exc_info())))
                    values[self._error_key.format(origin_message_id)] = (
                        error_message)
                    self.log(message, error_message)
                    continue
            else:
                error_list.append(origin_message_id)
                error_message = 'Неизвестный тип сообщения'
                values[self._error_key.format(origin_message_id)] = (
                    error_message)
                self.log(message, error_message)
                continue

            values[f'Сообщение {origin_message_id}'] = (
                'Отправка ответа в СМЭВ прошла успешно')

        if error_list:

            _key = 'Кол-во сообщений, по которым не удалось отправить ответ'
            values[_key] = str(len(error_list))

        values['Время окончания'] = (
            datetime.datetime.now().strftime(self.LOG_TIME_FORMAT))
        self.set_progress(
            progress='Завершено',
            task_state=states.SUCCESS,
            values=values)

        return self.state
