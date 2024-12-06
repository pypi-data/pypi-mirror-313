from __future__ import annotations

from datetime import date
from datetime import timedelta

from django.template.loader import render_to_string
from unittest.mock import patch

from kinder.core.models import RegionCode as RC
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.tests.factory_declaration import DeclarationF
from kinder.core.declaration_status.enum import DSS
from kinder.core.declaration_status.models import DeclarationStatus
from kinder.core.declaration_status.tests.dss_factory import DeclarationStatusF
from kinder.core.dict.models import GroupAgeSubCathegory
from kinder.core.direct.models import Direct
from kinder.core.direct.models import DirectStatus
from kinder.core.direct.models import DirectStatusLog
from kinder.core.direct.models import DRS
from kinder.core.direct.proxy import DirectModel
from kinder.core.direct.tests.factory_direct import DirectFactory
from kinder.core.group.models import PupilHistory
from kinder.core.group.tests.factory_group import FactGroupF
from kinder.core.unit.tests.factory_unit import UnitDouFactory
from kinder.core.unit.tests.factory_unit import UnitMoFactory
from kinder.test.base import BaseTC
from kinder.test.utils import faker

from concentrator.smev3_v321.cancel_request.executors import (
    CancelRequestExecutor)
from concentrator.smev3_v321.model import FormDataMessage
from concentrator.smev3_v321.utils import get_code_and_comment


class ChangeOrderInfoDirectRegisterTestCase(BaseTC):
    """Тест ChangeOrderInfo при смене статуса Направления на Направлен в ДОО"""

    def setUp(self):
        mo = UnitMoFactory(days_for_reject_direct=15)
        direct_new_status = DirectStatus.objects.get(code=DRS.REGISTER)
        self.declaration_1 = DeclarationF(mo=mo)
        self.declaration_1.status = DeclarationStatus.objects.get(
            code=DSS.DIRECTED)
        self.declaration_1.save()
        self.direct_1 = DirectFactory(
            declaration=self.declaration_1,
            document_details='123456',
            group=FactGroupF(
                sub_age_cat=GroupAgeSubCathegory.objects.get(
                    code=GroupAgeSubCathegory.MIN_CODE),
                unit=UnitDouFactory(
                    address_full=faker('address'), days_for_reject_direct=15)
            ),
            manual_create=False
        )
        DirectModel.change_status(self.direct_1, direct_new_status)
        self.declaration_2 = DeclarationF(mo=mo)
        self.declaration_2.status = DeclarationStatus.objects.get(
            code=DSS.DIRECTED)
        self.declaration_2.save()
        self.direct_2 = DirectFactory(
            declaration=self.declaration_2,
            document_details='123456',
            group=FactGroupF(
                sub_age_cat=GroupAgeSubCathegory.objects.get(
                    code=GroupAgeSubCathegory.MIN_CODE),
                unit=UnitDouFactory(
                    address_full=faker('address'), days_for_reject_direct=15)
            ),
            manual_create=True
        )
        DirectModel.change_status(self.direct_2, direct_new_status)
        DirectStatusLog.objects.update(status=direct_new_status)

    @staticmethod
    def get_direct_reject_days(declaration: Declaration, direct: Direct) -> str:
        """
        Формирует часть сообщения для changeOrderInfo с количеством дней,
        в течение которых надо явиться
        :param declaration: Заявление
        :param direct: Направление
        :return: Дата, до которой нужно явиться
        """
        days_for_reject_direct = declaration.mo.days_for_reject_direct
        end_date = direct.created + timedelta(days=days_for_reject_direct)
        return f'до {end_date.strftime("%d.%m.%Y")}'

    def test_register_direct_status_system_create(self):
        """
        Проверяет сообщение для changeOrderInfo при смене статуса направления
        на Направлен в ДОО и создании направления системой
        """
        result = get_code_and_comment(self.direct_1)
        direct_reject_date = self.get_direct_reject_days(
            self.declaration_1, self.direct_1
        )
        expected_result = (
            190,
            f'Вам предоставлено место в {self.direct_1.group.unit.name} в '
            f'группу {self.direct_1.group.name} '
            f'({self.direct_1.group.age_cat.name}) в '
            f'соответствии с номером направления {self.direct_1.id} '
            f'от {self.direct_1.date.strftime("%d.%m.%Y")}. Вам необходимо '
            f'явиться по адресу {self.direct_1.group.unit.address_full} '
            f'{direct_reject_date}.'
        )
        self.assertEqual(result, expected_result)

    def test_register_direct_status_manual_create(self):
        """
        Проверяет сообщение для changeOrderInfo при смене статуса направления
        на Направлен в ДОО и ручном создании направления
        """
        result = get_code_and_comment(self.direct_2)
        direct_reject_date = self.get_direct_reject_days(
            self.declaration_2, self.direct_2
        )
        expected_result = (
            190,
            f'Вам предоставлено место в {self.direct_2.group.unit.name} в '
            f'группу {self.direct_2.group.name} '
            f'({self.direct_2.group.age_cat.name}) в '
            f'соответствии с документом {self.direct_2.document_details}. '
            'Вам необходимо явиться по адресу '
            f'{self.direct_2.group.unit.address_full} {direct_reject_date}.'
        )
        self.assertEqual(result, expected_result)


class ChangeOrderInfoAcceptStatusTestCase(BaseTC):
    """Тест ChangeOrderInfo при смене статуса направления на Зачислен."""

    def setUp(self):
        # Тестовые данные
        self.doo_name = 'Тестовое ДОО'
        self.address_full = 'г. Казань, ул. Амирхана д.3'
        self.date_in_order = date.today() + timedelta(days=7)

        self.unit = UnitDouFactory(
            name=self.doo_name, address_full=self.address_full)
        self.direct = DirectFactory(group=FactGroupF(unit=self.unit))
        old_status = self.direct.status
        self.child = self.direct.declaration.children
        self.accept_status = DirectStatus.objects.get(code=DRS.ACCEPT)

        fake_context_class = type('Context', (object,), {})
        context = fake_context_class()
        context.date_in_order = self.date_in_order

        DirectModel.change_status(
            self.direct, self.accept_status, context=context)
        DirectStatusLog.objects.register_status(
            direct=self.direct,
            old_status=old_status,
            status=self.accept_status,
            comment=''
        )

        self.last_pupil = self.child.pupil_set.filter(
            grup=self.direct.group).order_by('id').last()

    @staticmethod
    def get_expected_result(expected_date: date | None) -> tuple[int, str]:
        """Получение ожидаемого результата."""
        _date = (expected_date.strftime('%d.%m.%Y')
                 if expected_date else '')
        return (
            250,
            'Ваш ребенок зачислен в Тестовое ДОО, расположенную по адресу '
            f'г. Казань, ул. Амирхана д.3. На основании договора от {_date}.'
        )

    def test_pupils_count(self):
        """Проверка наличия зачисления"""
        self.assertEqual(
            self.child.pupil_set.filter(grup=self.direct.group).count(), 1,
            'Должно быть одно зачисление'
        )

    def test_normal_accept_status(self):
        """
        Проверяет сообщение для changeOrderInfo при смене статуса направления
        на Зачислен
        """
        result = get_code_and_comment(self.direct)
        self.assertEqual(result, self.get_expected_result(self.date_in_order))

    def test_accept_status_when_pupil_not_exists(self):
        """
        Симулируем ситуацию, когда статус не успел отправиться, а ребёнка
        уже перевели в другую группу/отчислили
        """
        self.assertEqual(PupilHistory.objects.count(), 1)
        self.last_pupil.delete()
        self.assertEqual(PupilHistory.objects.count(), 1)

        # Проверяем, что дата зачисления в истории совпадает с изначальной
        pupil_history = PupilHistory.objects.filter(
            children=self.child,
            group=self.direct.group,
        ).order_by('id').last()
        self.assertEqual(
            pupil_history.date_in_order_to_doo, self.date_in_order)

        # Проверяем результат обработки
        result = get_code_and_comment(self.direct)
        self.assertEqual(result, self.get_expected_result(self.date_in_order))

        # Крайний случай (вряд ли возможен, но лучше отправить хоть что-то)
        pupil_history.delete()
        result = get_code_and_comment(self.direct)
        self.assertEqual(result, self.get_expected_result(None))


class TestChangeOrderAfterCancelRequest(BaseTC):
    """Тест ChangeOrderInfo при смене статуса заявления на Отказано в услуге
    после обработки cancelRequest
    """

    def setUp(self):
        self.decl_status = DeclarationStatusF.create(code=DSS.DUL_CONFIRMATING)
        self.declaration = DeclarationF.create(
            status=self.decl_status,
            client_id='12345'
        )

    @staticmethod
    def create_cancel_request():
        """Создает cancelRequest для отмены заявления"""

        cancel_request_msg = render_to_string('tests/cancel_request.xml')
        executor = CancelRequestExecutor()
        message = FormDataMessage({
            'message_id': '',
            'body': cancel_request_msg,
            'message_type': 'FormData',
            'is_test_message': True,
            'replay_to': ''
        })
        request = message.parse_body.cancelRequest

        with patch(
            'concentrator.smev3_v321.cancel_request.executors.is_cancel_allowed'
        ) as cancel_allowed_func:
            cancel_allowed_func.return_value = True
            executor.get_response(request)

    def check_region_and_comment(
            self, region_code: int | None, expected_comment: str):
        """Проверка кода отказа и комментария в зависимости от настройки
        REGION_CODE

        :param region_code: Номер региона
        :param expected_comment: Ожидаемый комментарий для региона
        """
        # Создаем отменяющий заявление cancelRequest
        self.create_cancel_request()
        # Меняем статус на Отказано в услуге
        decl_refused_status = DeclarationStatusF.create(code=DSS.REFUSED)
        self.declaration.status = decl_refused_status
        self.declaration.save()
        # Получаем код и комментарий
        with patch('concentrator.smev3_v321.utils.REGION_CODE', region_code):
            actual_result = get_code_and_comment(self.declaration)
        expected_result = (150, expected_comment)

        self.assertEqual(actual_result, expected_result)

    def test_default_regions(self):
        """Проверка комментария для регионов без специфичного комментария или
        если не указана настройка REGION_CODE"""
        # Если настройка REGION_CODE не указана, возвращает по умолчанию '00'
        region_code_not_specified = None

        default_region_codes = [
            region_code_not_specified, RC.DAGESTAN, RC.KBR, RC.LIPETSK,
            RC.MAGADAN, RC.MURMANSK, RC.NAO, RC.RYAZAN, RC.TATARSTAN, RC.TUMEN,
            RC.UDMURTIA, RC.HAKASIA, RC.HMAO
        ]

        for code in default_region_codes:
            self.check_region_and_comment(
                code,
                'Работа по текущему заявлению остановлена по причине '
                'Вашей отмены данного заявления.'
            )

    def test_specific_regions(self):
        """Проверка комментария для регионов со специфичным комментарием"""

        self.check_region_and_comment(
            RC.VLADIMIR,
            'Действия по заявлению приостановлены по причине Вашего отзыва '
            'заявления. Если данная услуга необходима, '
            'Вы можете подать новое заявление.'
        )

        self.check_region_and_comment(
            RC.VOLOGDA,
            'Обработка Вашего заявления прекращена в связи с отменой заявления '
            'по Вашей инициативе. Для консультации по подаче заявления Вы '
            'можете обратиться в Управление образования '
            'муниципального района/округа.'
        )

        self.check_region_and_comment(
            RC.KARELIA,
            'Вам отказано в предоставлении услуги по текущему заявлению '
            'по причине отзыва Вами заявления на ЕПГУ.'
        )

        self.check_region_and_comment(
            RC.ROSTOV,
            'Вам отказано в предоставлении услуги по текущему заявлению '
            'по причине Вашей отмены данного заявления.'
        )
