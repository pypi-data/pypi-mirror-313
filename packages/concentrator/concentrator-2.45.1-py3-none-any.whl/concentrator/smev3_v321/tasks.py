from __future__ import annotations

import traceback

from celery import states
from celery.schedules import crontab
from django.utils.safestring import mark_safe
from educommon.async_task.models import AsyncTaskType

from kinder import celery_app
from kinder.core.async_tasks.tasks import AsyncTask
from kinder.core.async_tasks.tasks import PeriodicAsyncTask
from kinder.core.utils.address import GarConnectionException

from .executors import RepositoryExecutors
from .loggers import OutgoingMessageSmevLogLogger
from .application_request.resending_helpers import (
    ApplicationRequestsStatusChanger)
from .model import FormDataMessage
from .settings import GAR_TIMEOUT_RESEND_SECONDS
from .settings import RESEND_APPLICATION_REQUESTS_TASK_ENABLED
from .settings import RESEND_APPLICATION_REQUESTS_TASK_HOUR
from .settings import RESEND_APPLICATION_REQUESTS_TASK_MINUTE


class GarTimeoutFormDataResendTask(AsyncTask):
    """
    Задача повторной обработки сообщения СМЭВ FormData (AIO) при
    ошибке доступа сервиса ГАР.
    """

    routing_key = 'aio_high_priority'
    description: str = __doc__
    task_type = AsyncTaskType.ASYNC_REQUEST

    def process(self, message, *args, **kwargs):
        form_data_message = FormDataMessage(message)
        executor = RepositoryExecutors.get_executor(form_data_message)

        self.set_progress(
            progress=(
                f'Повторная обработки сообщения типа {executor.name_service}'
            )
        )

        try:
            execution_result = executor.process(form_data_message)
        except GarConnectionException as exc:
            self.set_progress(
                progress=f'{exc.get_message()}. Задача будет перезапущена '
                f'через {GAR_TIMEOUT_RESEND_SECONDS} секунд.',
                task_state=states.SUCCESS
            )
            self.apply_async(
                (message, ),
                countdown=GAR_TIMEOUT_RESEND_SECONDS,
            )
        except Exception as e:
            values = {
                'Ошибка': str(e),
                'Текст': traceback.format_exc()
            }
            self.set_progress(
                values=values,
                progress=str(e),
                task_state=states.FAILURE,
            )
        else:
            OutgoingMessageSmevLogLogger.create_log(
                form_data_message, **execution_result.logging_data)
            self.set_progress(
                progress='Завершено', task_state=states.SUCCESS)

        return self.state


class ResendApplicationRequestsTask(PeriodicAsyncTask):
    """
    Задача для смены статусов запросов для Поставщика с "Отправлен" на
    "Не отправлен" для повторной обработки
    """

    routing_key = 'aio_low_priority'
    description: str = (
        'Смена статусов запросов ApplicationRequest на "Не отправлен"')
    run_every = crontab(
        hour=RESEND_APPLICATION_REQUESTS_TASK_HOUR,
        minute=RESEND_APPLICATION_REQUESTS_TASK_MINUTE,
    )
    task_type = AsyncTaskType.SYSTEM

    def process(self, *args, **kwargs):
        self.set_progress('Выполняется')

        changer = ApplicationRequestsStatusChanger(
            set_progress=self.set_progress)
        result = changer.change_statuses_and_write_results_to_csv()

        url = result.file_download_url
        self.set_progress(
            progress='Завершено',
            task_state=states.SUCCESS,
            values={
                'Ссылка для скачивания csv-файла': (
                    mark_safe(f'<a href="{url}" target="_blank">Скачать</a>')
                    if url else 'Файл отсутствует'
                ),
            }
        )
        return self.state


if RESEND_APPLICATION_REQUESTS_TASK_ENABLED:
    celery_app.register_task(ResendApplicationRequestsTask)
celery_app.register_task(GarTimeoutFormDataResendTask)
