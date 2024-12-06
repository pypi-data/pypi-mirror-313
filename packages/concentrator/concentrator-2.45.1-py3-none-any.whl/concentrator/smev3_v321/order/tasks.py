import datetime

from aio_client.base import RequestTypeEnum
from aio_client.consumer.models import PostConsumerRequest
from celery.schedules import crontab
from educommon.ws_log.models import SmevLog
from educommon.ws_log.models import SmevSourceEnum
from lxml import etree
from m3.plugins import ExtensionManager

from kinder import celery_app
from kinder.core.utils.address import GarConnectionException
from kinder.webservice.smev3.exceptions import RequestNotFoundError
from kinder.webservice.smev3.tasks.consumer import ReceivingAsConsumerTask
from kinder.webservice.smev3.tasks.consumer import RequestMessage
from kinder.webservice.smev3.tasks.consumer import SendingAsConsumerTask
from kinder.webservice.smev3.utils.error_logging import ErrorLogger

from concentrator import settings
from concentrator.smev3_v321 import settings as smev3_settings
from concentrator.smev3_v321.constants import GAR_RESEND_MESSAGE
from concentrator.smev3_v321.models import OrderRequest
from concentrator.smev3_v321.models import UpdateOrderRequest
from concentrator.smev3_v321.service_types import kinder_order

from .builders import OrderRequestBuilder
from .builders import UpdateOrderRequestBuilder
from .constants import CREATE_ORDER_RESPONSE_SUCCESS_CODE
from .constants import DEFAULT_CREATE_ORDER_REQUEST_METHOD_NAME
from .constants import DEFAULT_UPDATE_ORDER_REQUEST_METHOD_NAME


class OrderRequestSendingTask(SendingAsConsumerTask):
    """Формирование и отправка запроса OrderRequest СМЭВ 3 с блоком
    CreateOrderRequest.
    """

    description = 'Формирование и отправка запроса OrderRequest СМЭВ 3.'

    model = OrderRequest
    message_type = smev3_settings.ORDER_REQUEST_MESSAGE_TYPE
    method_name = DEFAULT_CREATE_ORDER_REQUEST_METHOD_NAME

    @property
    def request_builder(self) -> type[OrderRequestBuilder]:
        """Возвращает билдер запроса в OrderRequest в зависимости от версии
        начального ApplicationOrderInfoRequest
        """
        request_context = self.request.args[1]

        return ExtensionManager().execute(
            'concentrator.smev3_v4.extensions.get_order_request_builder',
            request_context.parser_module) or OrderRequestBuilder

    def log(self, message, result, **kwargs):
        """Логирование запроса.

        :param message: Сообщение
        :param result: Результат
        :param kwargs: Дополнительные параметры
        """

        data = {
            'result': result,
            'service_address':
                RequestTypeEnum.get_url(RequestTypeEnum.CS_POST),
            'method_name': self.method_name,
            'method_verbose_name':
                f'{self.message_type} (Формирование и отправка запроса '
                f'OrderRequest "Передача данных заявления в ЛК ЕПГУ".)',
            'interaction_type': SmevLog.IS_SMEV,
            'source': SmevSourceEnum.CONCENTRATOR,
        }

        smev_log = message.get_log(self.ROLE, **{**kwargs, **data})
        smev_log.save()

    def create_message(self, request_id, context, *args, **kwargs):
        """Создание сообщения.

        Добавлен аргумент для строителя запроса.
        Доп. данные для формирования тела запроса, которые отсутствуют
        в объекте запроса.

        :rtype: Message
        """

        try:
            request = self.model.objects.get(pk=request_id)
        except self.model.DoesNotExist:
            raise RequestNotFoundError(request_id, self.model)

        request.generate_message_id()
        builder = self.request_builder(request, context, *args, **kwargs)

        try:
            body = builder.build()
        except GarConnectionException:
            self.apply_async(
                (request_id, context),
                countdown=smev3_settings.GAR_TIMEOUT_RESEND_SECONDS
            )
            raise GarConnectionException(
                message=GAR_RESEND_MESSAGE.format(
                    time=smev3_settings.GAR_TIMEOUT_RESEND_SECONDS)
            )

        return RequestMessage(PostConsumerRequest(
            message_id=str(request.message_id),
            body=body,
            message_type=self.message_type,
            attachments=builder.attachments,
        ), request)

    def send(self, message):
        """Отправка запроса.

        :param message: Запрос
        :type message: RequestMessage
        """

        super().send(message)
        message.request.request = message.message.body
        message.request.request_sent = datetime.datetime.now()
        message.request.save()


class OrderRequestReceivingTask(ReceivingAsConsumerTask):
    """Задача обработки полученных ответов на запрос OrderRequest СМЭВ 3."""

    description = (
        'Задача обработки полученных ответов на запрос OrderRequest СМЭВ 3')

    model = OrderRequest
    message_type = smev3_settings.ORDER_REQUEST_MESSAGE_TYPE

    catchable_exceptions = {
        **ReceivingAsConsumerTask.catchable_exceptions,
        ValueError: ErrorLogger,
        etree.XMLSyntaxError: ErrorLogger,
        kinder_order.GDSParseError: ErrorLogger,
    }

    run_every = crontab(
        minute=settings.SMEV3_FORM_DATA_TASK_EVERY_MINUTE,
        hour=settings.SMEV3_FORM_DATA_TASK_EVERY_HOUR)

    def _process(self, request):
        """Обработчик ответа.

        :param request: инстанс запроса
        :return: None

        :raises: XMLSyntaxError, GDSParseError, ValueError
        """

        data = kinder_order.parseString(request.response)

        order_response = data.CreateOrderResponse
        if order_response.code != CREATE_ORDER_RESPONSE_SUCCESS_CODE:
            return

        request.order_id = order_response.orderId
        request.save()

        from concentrator.smev3_v321.order.helpers import (
            UpdateOrderRequestSMEV3RequestManager)
        from concentrator.smev3_v321.order.request_context import (
            UpdateOrderRequestContext)

        # Выполняет отправку отложенных запросов UpdateOrderRequest.
        pending_requests = request.pendingupdateorderrequest_set.order_by(
            'modified').all()

        for pending_request in pending_requests:
            UpdateOrderRequestSMEV3RequestManager(
                UpdateOrderRequestContext(
                    **pending_request.decoded_data,
                    order_id=request.order_id,
                )
            ).apply_async()

    def validate_response(self, response):
        return True


class UpdateOrderRequestSendingTask(OrderRequestSendingTask):
    """Формирование и отправка запроса OrderRequest СМЭВ 3 с блоком
    UpdateOrderRequest.
    """

    description = 'Формирование и отправка запроса UpdateOrderRequest СМЭВ 3.'
    model = UpdateOrderRequest
    message_type = smev3_settings.ORDER_REQUEST_MESSAGE_TYPE
    method_name = DEFAULT_UPDATE_ORDER_REQUEST_METHOD_NAME

    @property
    def request_builder(self) -> type[UpdateOrderRequestBuilder]:
        """Возвращает билдер запроса UpdateOrderRequest в зависимости от
        версии начального запроса ApplicationOrderInfoRequest
        """

        request_context = self.request.args[1]

        return ExtensionManager().execute(
            'concentrator.smev3_v4.extensions.get_update_order_request_builder',
            request_context.parser_module) or UpdateOrderRequestBuilder

celery_app.register_task(OrderRequestSendingTask)
celery_app.register_task(OrderRequestReceivingTask)
celery_app.register_task(UpdateOrderRequestSendingTask)
