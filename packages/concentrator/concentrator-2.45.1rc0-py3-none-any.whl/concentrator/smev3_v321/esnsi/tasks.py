from datetime import datetime

from celery.schedules import crontab
from lxml import etree
from m3.actions import ApplicationLogicException

from kinder import celery_app
from kinder.webservice.smev3.tasks.consumer import ReceivingAsConsumerTask
from kinder.webservice.smev3.tasks.consumer import SendingAsConsumerTask
from kinder.webservice.smev3.utils.error_logging import BaseExceptionLogger

from concentrator.smev3_v321.models import UpdateClassifierRequest
from concentrator.smev3_v321.service_types import (
    update_classifier as update_schema)

from .builders import RemoveMissingRequestBuilder
from .builders import UpdateClassifierRequestBuilder
from .settings import UPDATE_CLASSIFIER_REQUEST_MSG_TYPE
from .settings import UPDATE_CLASSIFIER_RESPONSE_HOURS
from .settings import UPDATE_CLASSIFIER_RESPONSE_MINUTES


class _ApplicationErrorLogger(BaseExceptionLogger):
    """
    Логируем ошибки приложения
    """
    def get_message(self):
        return (
            'Ошибка приложения - %s' % str(self.exc))


class EsnsiSendingTask(SendingAsConsumerTask):
    """
    Задача отправки запросов к ЕСНСИ
    """
    description = 'Отправка запросов к ЕСНСИ'
    model = UpdateClassifierRequest
    message_type = UPDATE_CLASSIFIER_REQUEST_MSG_TYPE
    request_builder = UpdateClassifierRequestBuilder
    catchable_exceptions = {
        **SendingAsConsumerTask.catchable_exceptions,
        ApplicationLogicException: _ApplicationErrorLogger
    }

    def send(self, message):
        super().send(message)
        message.request.request_sent = datetime.now()
        message.request.save()


class EsnsiSendingAllTask(EsnsiSendingTask):
    """
    Задача отправки запросов к ЕСНСИ с removeMissing=True

    Использовать только если отправляются все значения справочника
    """
    request_builder = RemoveMissingRequestBuilder


class EsnsiReceivingTask(ReceivingAsConsumerTask):
    """
    Задача принятия ответов от ЕСНСИ
    """
    model = UpdateClassifierRequest
    message_type = UPDATE_CLASSIFIER_REQUEST_MSG_TYPE
    description = 'Получение ответов от ЕСНСИ'
    catchable_exceptions = {
        **ReceivingAsConsumerTask.catchable_exceptions,
        ApplicationLogicException: _ApplicationErrorLogger
    }

    run_every = crontab(
        hour=UPDATE_CLASSIFIER_RESPONSE_HOURS,
        minute=UPDATE_CLASSIFIER_RESPONSE_MINUTES,
    )

    def _process(self, request):
        response = request.response
        node = etree.fromstring(response)
        cnsi_response = update_schema.CnsiResponse().build(node)

        result = None

        if request.request_type == UpdateClassifierRequest.UPDATE_CLASSIFIERS:
            result = (
                cnsi_response.UpdateClassifierData.ClassifierUpdateSuccessful)
        elif (request.request_type ==
              UpdateClassifierRequest.DELETE_CLASSIFIERS):
            result = (
                cnsi_response.DeleteClassifierData.ClassifierDeleteSuccessful)
        else:
            raise ApplicationLogicException('Тип запроса не определён')

        request.request_result = (
            UpdateClassifierRequest.RESULT_SUCCESS
            if result else UpdateClassifierRequest.RESULT_FAILURE
        )
        request.save()

    def process_message(self, message):
        super().process_message(message)
        message.request.response_returned = datetime.now()
        message.request.save()

    def validate_response(self, response):
        return True


celery_app.register_task(EsnsiSendingTask)
celery_app.register_task(EsnsiSendingAllTask)
celery_app.register_task(EsnsiReceivingTask)
