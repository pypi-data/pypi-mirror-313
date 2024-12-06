import os
from datetime import date

from kinder.core.children.models import Children
from kinder.core.children.models import Delegate
from kinder.core.children.models import DULDelegateType
from kinder.core.children.tests.factory_child import ChildF
from kinder.core.children.tests.factory_child import ChildrenDelegateF
from kinder.core.children.tests.factory_child import DelegateF
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.tests import factory_declaration
from kinder.core.declaration_status.enum import DSS
from kinder.core.declaration_status.models import DeclarationStatus
from kinder.core.dict.models import DULTypeEnumerate
from kinder.core.privilege.tests.factory_privilege import PrivilegeF
from kinder.core.unit.tests import factory_unit
from kinder.test.base import BaseTC

from concentrator.settings import SMEV3_FORM_DATA_MESSAGE_TYPE
from concentrator.smev3_v321.model import FormDataMessage

from concentrator.smev3_v321.application_request import application


TEST_REQUEST = os.path.join(
    os.path.dirname(__file__), 'ApplicationRequest.xml')


class Smev3v321ApplicationRequestTestCase(BaseTC):
    """Тестируем работу сервиса ApplicationRequest"""

    def setUp(self):
        super().setUp()

        # Тестовое ДОО
        region = factory_unit.UnitRFactory.create(name='Татарстан')
        mo = factory_unit.UnitMoFactory.create(name='Казань', parent=region)
        self.dou = factory_unit.UnitDouFactory.create(
            parent=mo,
            full_name='МАДОУ "ЦРР-Детский сад № 396" '
                      'Приволжского района г.Казани',
        )

        # Тестовый ребенок
        self.child_data = {
            'surname': 'Кашапова',
            'firstname': 'Замира',
            'patronymic': 'Сабитовна',
            'date_of_birth': date(2017, 1, 1),
            'dul_type': DULTypeEnumerate.SVID,
            'dul_date': date(2018, 1, 1),
            'dul_series': 'I-КБ',
            'dul_number': '222222',
            'zags_act_number': '11111111',
            'zags_act_date': date(2020, 1, 1),
        }
        self.child = ChildF.create(**self.child_data)

        # Тестовый представитель
        DULDelegateType.objects.filter(
            code=DULDelegateType.RF_PASSPORT).update(esnsi_code='1')
        self.delegate_data = {
            'surname': 'Кашапова',
            'firstname': 'Эльвира',
            'patronymic': 'Шавкатовна',
            'dul_type': DULDelegateType.objects.get(esnsi_code='1'),
            'dul_series': '9999',
            'dul_number': '111111',
            'email': 'test@yandex.ru',
            'phones': '+7(000)1234567',
        }
        self.delegate = DelegateF.create(**self.delegate_data)

        ChildrenDelegateF.create(children=self.child, delegate=self.delegate)

        # Добавляем заявку не в активном статусе
        self.declaration = factory_declaration.DeclarationF(
            children=self.child,
            status=DeclarationStatus.objects.get(code=DSS.ACCEPTED)
        )

        PrivilegeF.create(esnsi_code='1')

        with open(TEST_REQUEST, 'r') as test_r:
            test_data = test_r.read()
            test_data = test_data.format(dou_id=self.dou.id)

            self.application_manager = (
                application.ApplicationManager(
                    FormDataMessage({
                        'message_id': '',
                        'body': test_data,
                        'message_type': SMEV3_FORM_DATA_MESSAGE_TYPE,
                        'is_test_message': True,
                        'replay_to': ''
                    })))
            self.application_manager.run()

    def test_children_duplicate(self):
        """
        Проверка того, что сервис не создал дубль ребенка.
        Используется метод поиска дубля из самого сервиса.
        """
        children_count = (
            self.application_manager.find_existing_children().count())

        self.assertEqual(children_count, 1)

    def test_update_children_data(self):
        """
        Проверка обновления данных найденного ребенка, по тегам
        ChildBirthDocIssueDate и ChildBirthDocActNumber.
        """
        child = Children.objects.get(id=self.child.id)
        self.assertEqual(child.zags_act_number, '2222222')
        self.assertEqual(child.zags_act_date, date(2022, 2, 2))

    def test_delegate_duplicate(self):
        """
        Проверка того, что сервис не создал дубль представителя.
        Используется метод поиска дубля из самого сервиса."""
        delegates_query, _ = application.Application(
            self.application_manager.application_type
        )._existing_delegates_query(self.child)

        delegates_count = delegates_query.count()

        self.assertEqual(delegates_count, 1)

    def test_update_delegate_data(self):
        """
        Проверка обновления данных найденного представителя, по тегам
        PersonPhone и PersonEmail.
        """
        delegate = Delegate.objects.get(id=self.delegate.id)
        self.assertEqual(delegate.email, 'mail@mail.ru')
        self.assertEqual(delegate.phones, '+7(123)1111111')

    def test_declaration_created(self):
        """
        Проверка того, что сервис создал еще одну заявку, т.к. добавленная
        нами тут была не в активном статусе.
        """
        declarations_count = Declaration.objects.filter(
            children=self.child).count()

        self.assertEqual(declarations_count, 2)
