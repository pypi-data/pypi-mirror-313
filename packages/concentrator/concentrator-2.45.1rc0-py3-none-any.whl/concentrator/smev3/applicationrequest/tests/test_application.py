from datetime import date
import os

from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_save
from factory.django import mute_signals

from concentrator.smev3.applicationrequest.application import Application
from concentrator.smev3.base.tests.utils import examples
from concentrator.smev3.service_types import kinder_conc

from kinder.core.children.models import (Children, ChildrenDelegate, Delegate,
                                         DelegateTypeEnumerate,
                                         GenderEnumerate)
from kinder.core.declaration.models import (Declaration, DeclarationPrivilege,
                                            DeclarationSourceEnum,
                                            DeclarationUnit)
from kinder.core.declaration_status.models import DSS, DeclarationStatus
from kinder.core.dict.models import DULDelegateType
from kinder.core.dict.models import GroupType
from kinder.core.dict.models import GroupTypeEnumerate
from kinder.core.dict.models import WorkType
from kinder.core.unit.tests.factory_unit import UnitDouFactory

from .base import ApplicationTC as BaseApplicationTC


class ApplicationTC(BaseApplicationTC):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        with mute_signals(pre_save, post_save):
            for id_ in (215, 219, 221):
                UnitDouFactory.create(id=id_)

        cls.application = Application(cls.application, cls.attachments)

    def test_child(self):
        child = self.application._create_child()
        child_data = {
            'firstname': 'Василий',
            'surname': 'Иванов',
            'patronymic': 'Александрович',
            'gender': GenderEnumerate.MALE,
            'date_of_birth': date(2016, 2, 2),
            'dul_series': 'VII-ЛД',
            'dul_number': '132564',
            'dul_date': date(2016, 2, 10),
            'zags_act_number': '13245',
            'zags_act_place': 'ЗАГС района №5',
            'birthplace': 'г. Самара',
            'reg_address_place': '',
            'reg_address_street': '585eec0b-314c-4309-a497-3fe09300e903',
            'reg_address_full':
                '121351, Москва г., Бобруйская ул., 4 д., 2 корп.',
            'reg_address_house': '4',
            'reg_address_house_guid': '5956b056-0d23-4f59-9c52-f561968bdda0',
            'reg_address_flat': '23',
        }

        for field, expected_value in list(child_data.items()):
            real_value = getattr(child, field, None)
            self.assertEquals(
                real_value, expected_value,
                '{}: {} != {}'.format(field, real_value, expected_value))

    def test_delegate(self):
        delegate = self.application._create_delegate()
        delegate_data = {
            'surname': 'Иванова',
            'firstname': 'Елена',
            'patronymic': 'Викторовна',
            'date_of_birth': date(1993, 10, 20),
            'snils': '000-102-103 44',
            'phones': '+7(123)1234567',
            'email': 'test@test.ru',
            'dul_type':
                DULDelegateType.objects.get(code=DULDelegateType.RF_PASSPORT),
            'dul_series': '6004',
            'dul_number': '586830',
            'dul_date': date(2007, 9, 10),
            'dul_issued_by': 'Отделением УФМС России',
            'type': DelegateTypeEnumerate.MOTHER,
            'reg_address_place': '',
            'reg_address_street': '585eec0b-314c-4309-a497-3fe09300e903',
            'reg_address_full':
                '121351, Москва г., Бобруйская ул., 4 д., 2 корп.',
            'reg_address_house': '4',
            'reg_address_house_guid': '5956b056-0d23-4f59-9c52-f561968bdda0',
            'reg_address_flat': '23',
        }

        for field, expected_value in list(delegate_data.items()):
            real_value = getattr(delegate, field, None)
            self.assertEquals(
                real_value, expected_value,
                '{}: {} != {}'.format(field, real_value, expected_value))

    def test_family(self):
        child = self.application._create_child()
        delegate = self.application._create_delegate()
        self.application._add_child_to_delegate(child, delegate)

        self.assertEquals(ChildrenDelegate.objects.count(), 1)
        cd = ChildrenDelegate.objects.last()
        self.assertEquals(cd.children, child)
        self.assertEquals(cd.delegate, delegate)

    def test_declaration(self):
        declaration = self.application.create()

        self.assertEquals(Declaration.objects.count(), 1)
        self.assertEquals(Children.objects.count(), 1)
        self.assertEquals(Delegate.objects.count(), 1)
        self.assertEquals(ChildrenDelegate.objects.count(), 1)
        self.assertEquals(DeclarationUnit.objects.count(), 3)
        self.assertEquals(DeclarationPrivilege.objects.count(), 2)
        self.assertTrue(
            DeclarationUnit.objects.values_list('declaration_id', flat=True),
            [declaration.id, declaration.id, declaration.id])

        declaration_data = {
            'client_id': 12345678,
            'source': DeclarationSourceEnum.CONCENTRATOR,
            'children': Children.objects.last(),
            'desired_date': date(2018, 9, 1),
            'status': DeclarationStatus.objects.get(
                code=DSS.RECEIVED),
            'work_type': WorkType.objects.get(code=WorkType.ALLDAY),
            'offer_other': True,
            'consent_dev_group': True,
            'desired_group_type': GroupType.objects.get(code=GroupTypeEnumerate.COMP)
        }

        for field, expected_value in list(declaration_data.items()):
            real_value = getattr(declaration, field, None)
            self.assertEquals(
                real_value, expected_value,
                '{}: {} != {}'.format(field, real_value, expected_value))

    def test_unit_not_found(self):
        """при получении несущесвующего учреждения, отдаем ошибку"""
        application_xml = kinder_conc.parseString(
            next(examples(
                os.path.dirname(__file__),
                name='unit_not_found.xml'
            )), silence=True
        ).ApplicationRequest
        application = Application(application_xml, None)

        with self.assertRaises(ValidationError):
            application.create()
