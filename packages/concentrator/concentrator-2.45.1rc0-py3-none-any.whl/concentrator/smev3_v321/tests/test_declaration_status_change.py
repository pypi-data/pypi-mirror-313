import datetime

from django.conf import settings

from kinder.core.declaration.tests.factory_declaration import DeclarationF
from kinder.core.declaration_status.enum import DSS
from kinder.core.declaration_status.models import DeclarationStatus
from kinder.core.declaration_status.models import DeclarationStatusTransfer
from kinder.core.declaration_status.tests.dss_factory import DeclarationStatusF
from kinder.core.declaration_status.tests.dss_factory import (
    DeclarationStatusLogF)
from kinder.core.unit.tests.factory_unit import UnitMoFactory
from kinder.test.base import BaseTC
from kinder.test.utils import faker

from concentrator.smev3_v321.constants import PROVIDE_DOCUMENT_STATUSES
from concentrator.smev3_v321.utils import get_declaration_code_and_comment


class DeclarationStatusChangeTestCase(BaseTC):
    """
    Тест для проверки корректности работы хелпера, возвращающего
    код и комментарий для передачи сообщения при смене статуса заявления
    """

    def setUp(self):
        super().setUp()
        self.mo = UnitMoFactory(
            address_full=faker('address')
        )
        self.declaration = DeclarationF(
            mo=self.mo,
        )
        self.declaration_status_log = DeclarationStatusLogF(
            declaration=self.declaration,
            status=DeclarationStatusF(),
        )

    def test_accepted_for_considering_status(self):
        self.declaration_status_log.status = DeclarationStatus.objects.get(
            code=DSS.ACCEPTED_FOR_CONSIDERING)
        result = get_declaration_code_and_comment(
            self.declaration_status_log)
        expected_result = (120, 'Начато рассмотрение заявления.')
        self.assertEqual(result, expected_result)

    def test_confirmation_status(self):
        expected_comment = (
            f'Для подтверждения данных вам необходимо представить в {self.mo} '
            '{date_before}'
            f'следующие документы: {self.declaration_status_log.comment}.')

        for status in PROVIDE_DOCUMENT_STATUSES:
            self.declaration_status_log.status = DeclarationStatus.objects.get(
                code=status)

            status_transfer = DeclarationStatusTransfer.objects.filter(
                from_status=self.declaration_status_log.old_status,
                to_status=self.declaration_status_log.status
            ).first()

            if status_transfer and status_transfer.auto_change_days:
                date_before = datetime.date.today() + datetime.timedelta(
                    days=status_transfer.auto_change_days)
                expected_comment = expected_comment.format(
                    date_before=
                    f'в срок до {date_before.strftime(settings.DATE_FORMAT)} ')
            else:
                expected_comment = expected_comment.format(date_before='')

            expected_result = (130, expected_comment)

            result = get_declaration_code_and_comment(
                self.declaration_status_log)

            with self.subTest(name=status):
                self.assertEqual(result, expected_result)

    def test_refused_status(self):
        self.declaration_status_log.status = DeclarationStatus.objects.get(
            code=DSS.REFUSED)
        result = get_declaration_code_and_comment(
            self.declaration_status_log)
        expected_comment = (
            'Вам отказано в предоставлении услуги по текущему заявлению по '
            f'причине {self.declaration_status_log.comment}. '
            f'Вам необходимо обратиться по адресу: '
            f'{self.mo.address_full}.')
        expected_result = (150, expected_comment)
        self.assertEqual(result, expected_result)

    def test_received_status(self):
        self.declaration_status_log.status = DeclarationStatus.objects.get(
            code=DSS.RECEIVED)
        result = get_declaration_code_and_comment(
            self.declaration_status_log)
        expected_comment = (
            'Заявление передано в региональную систему доступности '
            'дошкольного образования.  Заявление зарегистрировано. '
            f'{self.declaration.date.strftime(settings.DATE_FORMAT)} '
            f'с номером {self.declaration.client_id}. '
            'Ожидайте рассмотрения в течение 7 дней.')
        expected_result = (110, expected_comment)
        self.assertEqual(result, expected_result)

    def test_reviewed_status(self):
        for status in PROVIDE_DOCUMENT_STATUSES:
            self.declaration_status_log.status = DeclarationStatus.objects.get(
                code=status)
