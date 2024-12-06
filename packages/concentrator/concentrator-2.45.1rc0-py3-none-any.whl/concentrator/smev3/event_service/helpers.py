from datetime import datetime

from concentrator import settings
from concentrator.smev3.models import EventServiceRequest
from concentrator.smev3.base.utils import render_type2xml
from concentrator.smev3.service_types import kinder_conc_event
from concentrator.smev3.event_service.events import DEFAULT_COMMENT
from concentrator.smev3.event_service.events import DEFAULT_STATUS
from concentrator.smev3.event_service.events import Event
from concentrator.smev3.event_service.events import MAP_STATUS
from concentrator.smev3.event_service.tasks import EventServiceSendingTask


class EventServiceSMEV3RequestManager:
    """Хелпер запуска задачи по отправке запросов о возникновении события.

    Формирует данные из контекста для запроса.
    Создает запись запроса в БД.
    Создает задачу по отправке запроса о возникновении события.
    Начинает выполнение задачи.
    """

    task = EventServiceSendingTask
    model = EventServiceRequest

    def __init__(self, context):
        self.context = context

    def get_params(self):
        """Формирует параметры для создания запроса из контекста.

        :return: словарь данных
        :rtype: dict
        """

        event = self.context.get('event')

        return {
            'declaration_id': self.context.get('declaration_id'),
            'event_code': event.code,
            'event_comment': event.comment,
            'direct_id': self.context.get('direct_id'),
        }

    def create_request(self):
        """Создает запрос.

        :return: инстанс созданного запроса
        :rtype: model
        """

        return self.model.objects.create(**self.get_params())

    def create_task(self):
        """Создает задачу.

        :return: инстанс созданной задачи
        :rtype: task
        """

        return self.task()

    def apply_async(self):
        """Запускает задачу."""

        task = self.create_task()
        request = self.create_request()

        return task.apply_async((request.id,))


def get_event_data_for_change_status(old_status, new_status):
    """ Ищем нужныЙ статус и комментари в MAP_STATUS
    если находим отдаем, иначе дефолтные значения

    @param old_status: с какого статуса был переход у заявления
    @param new_status: Новый статус заявления
    @return: экземпляр класса concentrator.smev3.event_service.events.Event
    """
    # обходим 'in <string>' requires string as left operand, not NoneType
    old_status = old_status or 'None'
    event_status = DEFAULT_STATUS
    comment = DEFAULT_COMMENT
    for key in MAP_STATUS.keys():
        start, end = key
        if old_status in start and new_status in end:
            event_status, comment = MAP_STATUS[key]
            break
    return Event(event_status, comment)


def get_text_message_event_request(order_id, request):
    """
    Возвращает тело запроса для отправки

    :param order_id: ID заявки на портале
    :type order_id: int
    :param request: Запрос
    :type request: TextMessageEventRequest
    :return: Тело запроса
    :rtype: str
    """

    message_exchange = request.message_exchange

    text_message_event_type = kinder_conc_event.TextMessageEventType()

    event_type = kinder_conc_event.EventType(
        textMessageEvent=text_message_event_type)

    request = kinder_conc_event.EventServiceRequestType(
        env=settings.EVENT_SERVICE_ENV,
        orderId=order_id,
        eventDate=datetime.now(),
        eventComment=message_exchange.message,
        event=event_type)

    return render_type2xml(
        request, name_type='eventServiceRequest')
