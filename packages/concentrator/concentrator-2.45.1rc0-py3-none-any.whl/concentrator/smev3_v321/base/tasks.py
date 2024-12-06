from __future__ import annotations

import datetime

from aio_client.base import RequestTypeEnum
from aio_client.consumer.models import GetConsumerResponse
from aio_client.consumer.models import PostConsumerRequest
from celery import states
from celery.schedules import crontab
from django.db.models import OuterRef
from django.db.models import Subquery
from django.db.models import TextField
from django.db.models.functions import Cast
from django_celery_beat.models import PeriodicTask
from educommon.async_task.models import AsyncTaskType
from educommon.ws_log.models import SmevLog
from educommon.ws_log.models import SmevSourceEnum
from m3 import ApplicationLogicException

from kinder import celery_app
from kinder.core.async_tasks.tasks import AsyncTask
from kinder.core.async_tasks.tasks import PeriodicAsyncTask
from kinder.core.declaration.models import Declaration
from kinder.core.direct.models import DRS
from kinder.core.direct.models import Direct
from kinder.core.direct.models import DirectStatusLog
from kinder.core.helpers import get_instance

from concentrator import settings
from concentrator.smev3_v321.attachment_request.helpers import (
    AttachmentRequestHelper)
from concentrator.smev3_v321.constants import LOG_TIME_FORMAT
from concentrator.smev3_v321.models import AttachmentRequest
from concentrator.smev3_v321.services import FormDataMessageProcessingService
from concentrator.smev3_v321.utils import declaration_awaiting_direction_check
from concentrator.smev3_v321.utils import declaration_reviewed_check
from concentrator.smev3_v321.utils import get_code_and_comment
from concentrator.smev3_v321.utils import push_change_order_info_request


class FormDataMessageProcessingTask(AsyncTask):
    """Задача обработки сообщения СМЭВ FormData (AIO).

    Задача оставлена для корректной работы скрипта, также проставлена очередь аио с высоким приоритетом,
    как было раньше установлено через настройку.

    """

    routing_key = 'aio_high_priority'
    hidden: bool = True
    task_type = AsyncTaskType.ASYNC_REQUEST

    description: str = FormDataMessageProcessingService.description

    processing_service: type[FormDataMessageProcessingService] = (
        FormDataMessageProcessingService)

    def process(self, *args, **kwargs):
        self.set_progress(
            progress=(
                f'Получаем запросы {self.processing_service.message_type}'),
            values={
                'Время начала':
                    datetime.datetime.now().strftime(LOG_TIME_FORMAT)
            })

        self.processing_service().run(*args, **kwargs)

        self.set_progress(
            progress='Завершено',
            task_state=states.SUCCESS,
            values={
                'Время выполнения':
                    datetime.datetime.now().strftime(LOG_TIME_FORMAT)
            })

        return self.state


class Smev3StatusChangePeriodicAsyncTask(PeriodicAsyncTask):
    """Периодическая таска, которая проверяет происходила ли смена статуса
    направлений на "Направлен в ДОО" с момента выполнения данной асинхронной
    задачи ранее и обрабатывает ответы AttachmentRequests
    """

    routing_key = 'aio_low_priority'
    run_every = crontab(
        minute=settings.SMEV3_STATUS_CHANGE_TASK_EVERY_MINUTE,
        hour=settings.SMEV3_STATUS_CHANGE_TASK_EVERY_HOUR)

    service_name = AttachmentRequestHelper.service_name
    description = 'Проверка смены статуса направления'
    stop_executing = False

    SEND_REQUEST = 'Отправка запроса'
    GET_RESPONSE = 'Получение ответа по запросу'

    def log(self, message, message_type, result=None, logging_data=None):
        """Логирование запроса СМЭВ 3.

        :param message: Сообщение
        :param message_type: Тип сообщения
        :param result: Результат
        :param logging_data: Дополнительные параметры
        """

        logging_data = logging_data or {}

        data = {
            'service_address':
                RequestTypeEnum.get_url(RequestTypeEnum.PR_POST),
            'method_verbose_name': f'{message_type} {self.service_name}',
            'direction': SmevLog.OUTGOING,
            'interaction_type': SmevLog.IS_SMEV,
            'source': SmevSourceEnum.CONCENTRATOR,
            'request': message,
            'result': result,
            'method_name': self.service_name,
            **logging_data
        }

        return SmevLog(**data).save()

    def process(self, *args, **kwargs):
        values = {
            'Время начала':
                datetime.datetime.now().strftime(LOG_TIME_FORMAT),
        }
        self.set_progress(
            progress='Проверка смены статусов направлений',
            values=values)

        last = PeriodicTask.objects.filter(name=self.name).last()
        directs = DirectStatusLog.objects.filter(
            status__code=DRS.REGISTER
        )
        if last.last_run_at:
            directs = directs.filter(created_at__gt=last.last_run_at)
        if not directs.exists():
            values.update({'Подходящих ДОО найдено': 0})
            self.set_progress(
                progress='Завершено',
                task_state=states.SUCCESS,
                values=values)

        units = directs.distinct('direct__group__unit').values_list(
            'direct__group__unit', flat=True)

        unit_counter = 0

        # отправка запросов для подходящих организаций
        for unit_id in units:
            helper = AttachmentRequestHelper(unit_id)
            request, attachments = helper.get_request()
            result = helper.send_request(request, attachments)
            status = 'Успешно' if result else 'Ошибка'
            unit_counter += 1
            self.log(request, self.SEND_REQUEST, result=status)

        # получение ответов с записью в СМЭВ лог
        requests_to_change = AttachmentRequest.objects.filter(
            response__isnull=True).annotate(
            message_id_str=Cast('message_id', output_field=TextField())
        ).annotate(resp=Subquery(GetConsumerResponse.objects.filter(
            origin_message_id=OuterRef('message_id_str')
        ).values('body')[:1])).annotate(
            req=Subquery(PostConsumerRequest.objects.filter(
                message_id=OuterRef('message_id_str')
            ).values('body')[:1])).filter(resp__isnull=False)

        for request in requests_to_change:
            request.response = request.resp
            request.save()
            self.log(request.req, self.GET_RESPONSE, result='Успешно',
                     logging_data={'response': request.resp})

        if unit_counter:
            values.update({'Подходящих ДОО найдено': unit_counter})
            self.set_progress(
                progress='Завершено',
                task_state=states.SUCCESS,
                values=values)

        return self.state


class DirectStatusCheckPeriodicAsyncTask(PeriodicAsyncTask):
    """
    Периодическая задача, которая отправляет информацию о статусе заявления
    """

    routing_key = 'aio_low_priority'
    run_every = crontab(
        minute=settings.SMEV3_CHECK_DECLARATION_STATUS_CHANGES_MINUTE,
        hour=settings.SMEV3_CHECK_DECLARATION_STATUS_CHANGES_HOUR)

    description = (
        'Проверка необходимости отправки сообщений о статусе заявлений')

    def process(self, *args, **kwargs):
        self.set_progress(
            progress='Началась отправка информации о статусах заявлений')
        sent = 0
        declarations_with_origin_message = Declaration.objects.filter(
            declarationoriginmessageid__isnull=False)

        not_reviewed_declarations = declarations_with_origin_message.filter(
            declarationoriginmessageid__reviewed_sent=False)

        for declaration in not_reviewed_declarations.iterator():
            reviewed = declaration_reviewed_check(declaration)
            if reviewed:
                sent += 1

        awaiting_direction_declarations = (
            declarations_with_origin_message.filter(
                desired_date=datetime.date.today()))

        for declaration in awaiting_direction_declarations.iterator():
            awaiting = declaration_awaiting_direction_check(declaration)
            if awaiting:
                sent += 1

        self.set_progress(
            progress='Завершено',
            task_state=states.SUCCESS,
            values={'Отправлено сообщений': sent})

        return self.state


class PushChangeOrderInfoRequestTask(AsyncTask):
    """Отправка запроса ChangeOrderInfoRequest"""

    routing_key = 'aio_low_priority'
    description = 'Отправка запроса ChangeOrderInfoRequest.'
    # Типы передаваемого параметра
    DECLARATION_TYPE = 'declaration'
    DIRECT_TYPE = 'direct'

    def _get_instance(
            self,
            instance_type: str | None,
            instance_id: int | None
    ) -> Direct | Declaration | None:
        """Получение объекта модели для формирования кода и комментария

        :param instance_type: Тип объекта модели: одно из следующих значений -
            self.DECLARATION_TYPE, self.DIRECT_TYPE или None
        :param instance_id: id объекта модели

        :return: Объект модели (заявление или направление) или None
        """
        if instance_type and instance_type not in (
                self.DECLARATION_TYPE, self.DIRECT_TYPE):
            raise ApplicationLogicException(
                'Некорректно задан параметр instance_type')

        if not instance_type or not instance_id:
            instance = None
        else:
            model = (Declaration if instance_type == self.DECLARATION_TYPE
                     else Direct)
            msg = f'{model._meta.verbose_name} с id={instance_id} не найдено'
            instance = get_instance(instance_id, model, msg)

        return instance

    def process(self, declaration_id, org_code, comment, message_id, replay_to,
            instance_type=None, instance_id=None, *args, **kwargs):

        self.set_progress(
            'Началась отправка запроса ChangeOrderInfoRequest.'
        )

        declaration = get_instance(
            declaration_id, Declaration, error_message='Заявление не найдено')
        instance = self._get_instance(instance_type, instance_id)

        if not (org_code and comment):
            org_code, comment = get_code_and_comment(instance)

        if org_code and comment:
            response, exception = push_change_order_info_request(
                declaration, org_code, comment, message_id, replay_to)
            if exception:
                raise exception
            else:
                self.set_progress(
                    progress='Запрос ChangeOrderInfoRequest успешно '
                             'отправлен',
                    task_state=states.SUCCESS)
        else:
            self.set_progress(
                progress='Отправка запроса ChangeOrderInfoRequest '
                         'не требуется',
                task_state=states.SUCCESS)

        return self.state


celery_app.register_task(FormDataMessageProcessingTask)
celery_app.register_task(Smev3StatusChangePeriodicAsyncTask)
celery_app.register_task(DirectStatusCheckPeriodicAsyncTask)
celery_app.register_task(PushChangeOrderInfoRequestTask)
