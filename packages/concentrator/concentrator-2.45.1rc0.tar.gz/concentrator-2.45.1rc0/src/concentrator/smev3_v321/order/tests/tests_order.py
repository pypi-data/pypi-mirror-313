from __future__ import annotations

from datetime import date
from datetime import timedelta

from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from factory.django import mute_signals

from concentrator.smev3_v321.order.constants import CreateOrderStatusMapper
from concentrator.smev3_v321.order.constants import UpdateOrderStatusMapper
from concentrator.smev3_v321.tests.factory import ApplicantAnswerF
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.tests.factory_declaration import DeclarationF
from kinder.core.declaration_status.enum import DSS
from kinder.core.declaration_status.models import DeclarationStatus
from kinder.core.dict.models import GroupAgeSubCathegory
from kinder.core.direct.models import Direct
from kinder.core.direct.models import DirectStatus
from kinder.core.direct.models import DRS
from kinder.core.direct.proxy import DirectModel
from kinder.core.direct.tests.factory_direct import DirectFactory
from kinder.core.group.tests.factory_group import FactGroupF
from kinder.core.group.tests.factory_group import PupilF
from kinder.core.group.tests.factory_group import PlanGroupF
from kinder.core.unit.tests.factory_unit import UnitDouFactory
from kinder.core.unit.tests.factory_unit import UnitMoFactory
from kinder.test.base import BaseTC
from kinder.test.utils import faker


class OrderRequestBaseTestCase(BaseTC):
    """Базовый класс для тестирования OrderRequest"""

    fixtures = ['status_initial_data']

    @staticmethod
    def create_declaration_and_direct(
        declaration_status_code: str, direct_status_code: str,
        manual_create: bool = False
    ) -> tuple[Declaration, Direct]:
        """Создание заявления с направлением

        :param declaration_status_code: Код статуса заявления
        :param direct_status_code: Код статуса направления
        :param manual_create: Ручное создание направления

        :return: Кортеж (заявление, направление)
        """
        mo = UnitMoFactory(days_for_reject_direct=15)
        declaration = DeclarationF(mo=mo)
        # Меняем статус заявления так, чтобы появилась запись истории смены
        declaration.status = DeclarationStatus.objects.get(
            code=declaration_status_code)
        declaration.save()

        direct = DirectFactory(
            declaration=declaration,
            document_details='123456',
            group=FactGroupF(
                sub_age_cat=GroupAgeSubCathegory.objects.get(
                    code=GroupAgeSubCathegory.MIN_CODE),
                unit=UnitDouFactory(address_full=faker('address'))
            ),
            manual_create=manual_create
        )
        # Меняем статус направление так, чтобы появилась запись истории смены
        DirectModel.change_status(
            direct, DirectStatus.objects.get(code=direct_status_code))

        return declaration, direct


class CreateOrderRequestTestCase(OrderRequestBaseTestCase):
    """Тестируем работу сервиса CreateOrderRequest"""

    @mute_signals(pre_save, post_save)
    def test_order_request_without_applicant_answer(self):
        """
        Проверка кода и статуса при переходе направления в статус
        Направлен в ДОО без ответа заявителя
        """

        declaration, direct = self.create_declaration_and_direct(
            declaration_status_code=DSS.DIRECTED,
            direct_status_code=DRS.REGISTER,
        )

        status_mapper = CreateOrderStatusMapper(declaration, direct)
        actual_result = status_mapper[{'status__code': declaration.status.code}]

        days_for_reject_direct = declaration.mo.days_for_reject_direct
        end_date = direct.created + timedelta(days=days_for_reject_direct)
        direct_reject_date = f'до {end_date.strftime("%d.%m.%Y")}'

        expected_result = (
            190,
            f'Вам предоставлено место в {direct.group.unit.name} в '
            f'группу {direct.group.name} ({direct.group.sub_age_cat.name}) в '
            f'соответствии с номером направления {direct.id} от '
            f'{direct.date.strftime("%d.%m.%Y")}. Вам необходимо явиться '
            f'по адресу {direct.group.unit.address_full} {direct_reject_date}.'
        )
        self.assertEqual(actual_result, expected_result)

    @mute_signals(pre_save, post_save)
    def test_order_request_manual_create_without_applicant_answer(self):
        """
        Проверка кода и статуса при переходе направления в статус
        Направлен в ДОО без ответа заявителя и при ручном создании направления
        """

        declaration, direct = self.create_declaration_and_direct(
            declaration_status_code=DSS.DIRECTED,
            direct_status_code=DRS.REGISTER,
            manual_create=True
        )

        status_mapper = CreateOrderStatusMapper(declaration, direct)
        actual_result = status_mapper[{'status__code': declaration.status.code}]

        days_for_reject_direct = declaration.mo.days_for_reject_direct
        end_date = direct.created + timedelta(days=days_for_reject_direct)
        direct_reject_date = f'до {end_date.strftime("%d.%m.%Y")}'

        expected_result = (
            190,
            f'Вам предоставлено место в {direct.group.unit.name} в '
            f'группу {direct.group.name} ({direct.group.sub_age_cat.name}) в '
            f'соответствии с документом {direct.document_details}. '
            'Вам необходимо явиться по адресу '
            f'{direct.group.unit.address_full} {direct_reject_date}.'
        )
        self.assertEqual(actual_result, expected_result)

    @mute_signals(pre_save, post_save)
    def test_order_request_with_applicant_answer(self) -> None:
        """
        Проверка кода и статуса при переходе направления в статус
        Направлен в ДОО при наличии ответа заявителя
        """
        declaration, direct = self.create_declaration_and_direct(
            declaration_status_code=DSS.DIRECTED,
            direct_status_code=DRS.REGISTER,
        )
        ApplicantAnswerF(direct=direct, answer=True)

        status_mapper = CreateOrderStatusMapper(declaration, direct)
        actual_result = status_mapper[{'status__code': declaration.status.code}]

        expected_result = (
            230, 'Согласие с предоставленным местом направлено на '
                 f'рассмотрение в {declaration.mo.name}.')
        self.assertEqual(actual_result, expected_result)


class UpdateOrderRequestTestCase(OrderRequestBaseTestCase):
    """Тестируем работу сервиса UpdateOrderRequest"""

    @mute_signals(pre_save, post_save)
    def test_order_request_when_accepted(self) -> None:
        """
        Проверка кода и статуса UpdateOrderRequest при переходе направления и
        заявления в статус Зачислен
        """
        declaration, direct = self.create_declaration_and_direct(
            declaration_status_code=DSS.ACCEPTED,
            direct_status_code=DRS.ACCEPT,
        )
        fact_pupil = PupilF.create(
            grup=direct.group,
            children=declaration.children,
            date_in_order_to_doo=date(2022, 5, 5))
        status_mapper = UpdateOrderStatusMapper(
            declaration, direct, declaration_status_changed=True)
        actual_result = status_mapper[{'status__code': declaration.status.code}]

        expected_result = (
            250,
            f'Ваш ребенок зачислен в {direct.group.unit.name}, '
            f'расположенную по адресу {direct.group.unit.address_full}. '
            f'На основании договора от '
            f'{fact_pupil.date_in_order_to_doo.strftime("%d.%m.%Y")}.'
        )
        self.assertEqual(actual_result, expected_result)

    @mute_signals(pre_save, post_save)
    def test_order_request_when_accepted_with_multiple_pupils(self) -> None:
        """
        Проверка кода и статуса UpdateOrderRequest при переходе направления
        и заявления в статус Зачислен при наличии фактического и планового
        зачисления.
        """
        declaration, direct = self.create_declaration_and_direct(
            declaration_status_code=DSS.ACCEPTED,
            direct_status_code=DRS.ACCEPT,
        )
        PupilF.create(
            grup=direct.group,
            children=declaration.children,
            date_in_order_to_doo=date(2022, 5, 5)
        )
        # создаем второе направление и зачисление по нему в плановую группу
        direct2 = DirectFactory(declaration=declaration, group=PlanGroupF(
            unit=UnitDouFactory(address_full=faker('address'))))
        DirectModel.change_status(
            direct2, DirectStatus.objects.get(code=DRS.ACCEPT))
        plan_pupil = PupilF.create(
            grup=direct2.group, children=declaration.children,
            date_in_order_to_doo=date(2024, 5, 5)
        )
        status_mapper = UpdateOrderStatusMapper(
            declaration, direct, declaration_status_changed=True)
        actual_result = status_mapper[{'status__code': declaration.status.code}]

        expected_result = (
            250,
            f'Ваш ребенок зачислен в {direct2.group.unit.name}, '
            f'расположенную по адресу {direct2.group.unit.address_full}. '
            f'На основании договора от '
            f'{plan_pupil.date_in_order_to_doo.strftime("%d.%m.%Y")}.'
        )
        self.assertEqual(actual_result, expected_result)
