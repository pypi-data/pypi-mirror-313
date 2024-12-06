"""Набор тестов приложения concentrator/dict."""

from django.db.models import Q

from kinder import settings as kinder_settings
from kinder.core.dict.models import DouType
from kinder.core.dict.models import UnitKind
from kinder.core.unit.models import Unit
from kinder.core.unit.models import UnitStatus
from kinder.core.unit.tests.factory_unit import UnitDouFactory
from kinder.test.base import BaseTC

from concentrator.dict.constants import OperationEnumerate
from concentrator.dict.constants.proxy import UnitProxy


class UnitProxyTC(BaseTC):
    u"""Тесты, связанные с получением списка ДОО."""

    def setUp(self):
        u"""Загрузка данных."""
        super(UnitProxyTC, self).setUp()
        self.unit_dou_factory_1 = UnitDouFactory.create()
        self.unit_dou_factory_2 = UnitDouFactory.create()
        self.unit_proxy = UnitProxy()

    def test_get_query(self):
        u"""Тест на получение списка ДОО."""
        print(u'Тест на получение списка ДОО')
        # Все ДОО
        query_unit = Unit.objects.filter(kind_id=UnitKind.DOU)
        # Расширенный фильтр: Только государственные ДОО
        # Действует при включенном параметре SMEV_ONLY_GOV_DOU_OR_EMPTY
        if kinder_settings.SMEV_ONLY_GOV_DOU_OR_EMPTY:
            query_unit = query_unit.filter(
                Q(dou_type__code__in=DouType.GOVERNMENT_TYPES) |
                Q(dou_type__isnull=True)
            )
        # Поменяем статус организации на "Закрыто", который не входит
        # в настройки списка организаций для добавления/изменения и
        # входит в список для удаления данных из справочника организации в ЕПГУ
        self.unit_dou_factory_1.status = UnitStatus.CLOSED
        self.unit_dou_factory_1.save()
        # Фильтр для добавления/изменения
        query_unit_filter = query_unit.filter(
            is_not_show_on_poral=False,
            status__in=self.unit_proxy.unit_statuses_for_add
        )
        query = self.unit_proxy.get_query(OperationEnumerate.ADD)
        self.assertEqual(len(query), len(query_unit_filter))
        # Фильтр для удаления
        query_unit_filter = query_unit.filter(
            is_not_show_on_poral=False,
            status__in=self.unit_proxy.unit_statuses_for_delete
        )
        query = self.unit_proxy.get_query(OperationEnumerate.DELETE)
        self.assertEqual(len(query), len(query_unit_filter))
