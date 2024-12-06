from datetime import datetime

from kinder.webservice.smev3.utils.request_builder import BaseRequestBuilder

from concentrator import settings
from concentrator.smev3.base.utils import get_order_id
from concentrator.smev3.base.utils import render_type2xml
from concentrator.smev3.service_types import kinder_conc_event
from concentrator.smev3.event_service.events import INFO_VENT_LIST


class EventType:
    """Класс для получения запроса информационных событий <ns:infoEvent>
    """

    def __init__(self, code):
        self.code = code

    def get_data(self):
        return kinder_conc_event.EventType(
            infoEvent=kinder_conc_event.InfoEventType(
                code=self.code
            )
        )


class ChangeStatusEventType(EventType):
    """Класс для получения запроса Передача статуса в ЛК ЕПГУ
     <ns:orderStatusEvent>
    """
    def get_data(self):
        return kinder_conc_event.EventType(
            orderStatusEvent=kinder_conc_event.OrderStatusEventType(
                statusCode=kinder_conc_event.statusCodeType(
                    techCode=self.code),
                cancelAllowed=True,
                sendMessageAllowed=True
            )
        )


class EventServiceRequestBuilder(BaseRequestBuilder):
    """Строитель запроса о возникновении события."""

    def build(self):
        """Формирует запрос eventServiceRequest.

        :return: запрос xml
        :rtype: str
        """

        if self.request.event_code in INFO_VENT_LIST:
            event_type = EventType(self.request.event_code)
        else:
            event_type = ChangeStatusEventType(self.request.event_code)

        request = kinder_conc_event.EventServiceRequestType(
            env=settings.EVENT_SERVICE_ENV,
            orderId=get_order_id(self.request.declaration),
            eventDate=datetime.now(),
            eventComment=self.request.event_comment,
            event=event_type.get_data())

        return render_type2xml(request, name_type='eventServiceRequest')
