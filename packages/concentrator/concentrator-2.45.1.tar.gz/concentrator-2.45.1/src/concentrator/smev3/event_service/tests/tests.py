from django.test import modify_settings
from lxml import etree

from kinder.core.declaration.enum import DeclarationSourceEnum
from kinder.core.declaration.models import DSS
from kinder.core.declaration.tests import factory_declaration
from kinder.core.unit.tests import factory_unit
from kinder.test.base import BaseTC
from kinder.test.mixins import XMLMixin

from concentrator.smev3.event_service.events import DEFAULT_COMMENT
from concentrator.smev3.event_service.events import DEFAULT_STATUS
# from concentrator.smev3.event_service.events import NEW_DIRECT_EVENT
from concentrator.smev3.event_service.helpers import (
    EventServiceSMEV3RequestManager)
from concentrator.smev3.event_service.builders import (
    EventServiceRequestBuilder)
from concentrator.smev3.event_service.helpers import (
    get_event_data_for_change_status)


@modify_settings(INSTALLED_APPS={'append': [
    'aio_client', 'concentrator', 'concentrator.smev3']})
class Smev3EventServiceTestCase(BaseTC, XMLMixin):
    """Тестируем работу хелперов для сервисов Передача статуса в ЛК ЕПГУ"""

    def setUp(self):
        super().setUp()

        self.unit_K = factory_unit.UnitMoFactory.create(name='Казань')
        self.unit_dou = factory_unit.HeadFactory.create(
            name='головное', parent=self.unit_K
        )
        self.decl = factory_declaration.DeclarationF.create(
            mo=self.unit_K, source=DeclarationSourceEnum.CONCENTRATOR)
        factory_declaration.DUnitF.create(
            declaration=self.decl,
            unit=self.unit_dou,
            ord=1
        )
        self.parser = etree.XMLParser(
            ns_clean=True, recover=True, encoding='utf-8')

    def test_get_event_data_for_change_status(self):
        """Проверяем что хелпер корретно ищет переходы
        статусов"""
        event = get_event_data_for_change_status(None, DSS.DUL_CONFIRMATING)
        self.assertSequenceEqual(
            (event.code, event.comment),
            (6, ''))
        # тут дб неописанный переход в MAP_STATUS,
        # чтобы проверить что в таком случае отдает дефолтные параметры
        event = get_event_data_for_change_status(None, DSS.DURING_EXCHANGE)
        self.assertSequenceEqual(
            (event.code, event.comment),
            (DEFAULT_STATUS, DEFAULT_COMMENT))

    # TODO: Переписать код
    # def test_get_info_event_request(self):
    #     """Проверяем Формирования тела запроса"""
    #
    #     event = NEW_DIRECT_EVENT
    #     request_db = EventServiceSMEV3RequestManager({
    #             'declaration_id': self.decl.id,
    #             'event': event
    #         }).create_request()
    #     body = EventServiceRequestBuilder(request_db).build()
    #     request = etree.fromstring(
    #         str(body).encode('utf-8'), parser=self.parser)
    #
    #     self.assertInXML(request, './/{*}code', event.code)
    #     self.assertInXML(request, './/{*}eventComment', event.comment)
    #
    #     event = get_event_data_for_change_status(
    #         DSS.WANT_CHANGE_DOU, DSS.ACCEPTED)
    #     request_db = EventServiceSMEV3RequestManager({
    #         'declaration_id': self.decl.id,
    #         'event': event
    #     }).create_request()
    #     body = EventServiceRequestBuilder(request_db).build()
    #     request = etree.fromstring(
    #         str(body).encode('utf-8'), parser=self.parser)
    #
    #     self.assertInXML(request, './/{*}techCode', 3)
    #     self.assertInXML(request, './/{*}eventComment', '')
