import datetime

from celery.schedules import crontab
from kinder.webservice.smev3.tasks.consumer import ReceivingAsConsumerTask
from kinder.webservice.smev3.tasks.consumer import SendingAsConsumerTask

from concentrator import settings as base_settings
from concentrator.smev3.event_service.builders import (
    EventServiceRequestBuilder)
from concentrator.smev3.models import EventServiceRequest


class EventServiceSendingTask(SendingAsConsumerTask):
    """Задача отправки сообщения о возникновении события СМЭВ 3."""

    description = 'Отправка сообщения о возникновении события'

    model = EventServiceRequest
    message_type = base_settings.EVENT_SERVICE_MESSAGE_TYPE
    request_builder = EventServiceRequestBuilder

    def send(self, message):
        """Отправка сообщения.

        Переопределен для записи в инстанс запроса:
        тела запроса и даты отправки запроса.

        :param message: объект сообщения и инстанса запроса
        :return: None
        """

        super().send(message)

        message.request.request = message.message.body
        message.request.request_sent = datetime.datetime.now()
        message.request.save()


class EventServiceReceivingTask(ReceivingAsConsumerTask):
    """Задача обработки полученных ответов о возникновении события."""

    description = 'Получение ответов о возникновении событий'

    model = EventServiceRequest
    message_type = base_settings.EVENT_SERVICE_MESSAGE_TYPE

    run_every = crontab(
        hour=base_settings.EVENT_SERVICE_RESPONSE_HOURS,
        minute=base_settings.EVENT_SERVICE_RESPONSE_MINUTES)

    def _process(self, request):
        pass

    def process_message(self, message):
        super().process_message(message)
        message.request.response_returned = datetime.datetime.now()
        message.request.save()

    def validate_response(self, response):
        return True
