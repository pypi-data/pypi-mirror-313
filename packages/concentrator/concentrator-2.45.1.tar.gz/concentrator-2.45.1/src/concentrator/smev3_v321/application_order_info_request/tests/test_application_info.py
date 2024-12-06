import datetime

from django.db.models.signals import post_save, pre_save
from factory.django import mute_signals

from concentrator.smev3_v321.application_order_info_request.tests.base import \
    BaseApplicationOrderInfoTC
from concentrator.smev3_v321.application_order_info_request.utils import (
    ChildApplicationOrderInfoUpdater, OrderRequestRequiredFieldsChecker,
    DelegateApplicationOrderInfoUpdater)
from kinder.core.children.constants import DEFAULT_ZAGS_ACT_NUMBER
from kinder.core.children.models import Children, Delegate
from kinder.core.children.tests.factory_child import ChildF, DelegateF
from kinder.core.declaration.tests.factory_declaration import DeclarationF

from kinder.core.dict.models import DULTypeEnumerate, DULDelegateType
from kinder.core.helpers import get_instance


test_date = datetime.date(2020, 1, 1)
DATE_FORMAT = '%Y-%m-%d'
DUL_DELEGATE_TYPE_ENSI = 2


def get_test_data_for_template(has_rf_document):
    """Получение словаря с тестовыми данными для шаблона запроса

    :param has_rf_document: Наличие рооссийского документа

    :return: Словарь с тестовыми данными для шаблона запроса
    """
    data = dict(
        person=dict(
            surname='Тестовый',
            name='Родитель',
            phone='+7999999-99-99',
            email='123@mail.ru',
        ),
        person_doc_info=dict(
            series='1234',
            number='123456',
            dul_type_doc_ensi=DUL_DELEGATE_TYPE_ENSI,
            issue_date=test_date.strftime(DATE_FORMAT),
            issue_code='123',
            issued_by='МФЦ',
        ),
        child=dict(
            surname='Тестовый',
            name='Ребенок',
            birth_date=test_date.strftime(DATE_FORMAT),
        )
    )
    common_document_data = dict(
        series='9876',
        number='654321',
        issue_date=test_date.strftime(DATE_FORMAT),
        issued_by='ЗАГС',
    )
    if has_rf_document:
        data['child_rf_doc_info'] = dict(
            act_number='456',
            act_date=test_date.strftime(DATE_FORMAT),
            **common_document_data,
        )
    else:
        data['child_foreign_doc_info'] = dict(
            name='Документ',
            **common_document_data
        )

    return data


class ChildApplicationOrderInfoUpdaterTC(BaseApplicationOrderInfoTC):
    """Тесты для класса ChildApplicationOrderInfoUpdater."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # Данные для российского документа
        cls.rf_doc_test_data = get_test_data_for_template(has_rf_document=True)
        cls.rf_doc_request_data = cls.get_prepared_request(cls.rf_doc_test_data)
        # Данные для иностранного документа
        cls.foreign_doc_test_data = get_test_data_for_template(
            has_rf_document=False)
        cls.foreign_doc_request_data = cls.get_prepared_request(
            cls.foreign_doc_test_data)

    def assert_not_have_empty_fields(self, empty_fields):
        """Проверка, что нет пустых полей

        :param empty_fields: Незаполненные поля
        """
        self.assertFalse(
            empty_fields,
            f'Есть незаполненные поля: {",".join(empty_fields)}'
        )

    @staticmethod
    def get_dul_type_params(has_rf_document):
        """Получение словаря с паметрами документа ребенка.

        :param has_rf_document: Наличие российского документа
        """
        return dict(
            dul_type=(DULTypeEnumerate.SVID if has_rf_document
                      else DULTypeEnumerate.INT_SVID)
        )

    @staticmethod
    def create_declaration_with_minimal_data(**params):
        """Создания заявления на ребенка с минимумом данных."""

        child_params = dict(
            surname='Тестовый',
            firstname='Ребенок',
            date_of_birth=test_date,
        )
        child_params.update(params)

        with mute_signals(pre_save, post_save):
            empty_child = Children.objects.create(**child_params)
            empty_declaration = DeclarationF.create(children=empty_child)
        return empty_declaration

    @staticmethod
    def create_declaration_with_data(**params):
        """Создания заявления на ребёнка, где все нужные данные заполнены."""
        with mute_signals(pre_save, post_save):
            full_child = ChildF.create(
                zags_act_place='ЗАГС',
                zags_act_number='123',
                zags_act_date=test_date,
                address_full='Полный адрес',
                **params,
            )
            full_declaration = DeclarationF.create(children=full_child)
        return full_declaration

    def _test_should_to_be_filled(self, request_data, has_rf_document):
        """Проверка, когда данные ребёнка должны обновиться.

        :param request_data: Данные запроса
        :param has_rf_document: Наличие российского документа
        """

        declaration = self.create_declaration_with_minimal_data(
            **self.get_dul_type_params(has_rf_document)
        )
        child = declaration.children
        child_before_changes = get_instance(child.id, Children)

        updater = ChildApplicationOrderInfoUpdater(child, request_data)
        updated = updater.run()

        # Проверка, что обновления было и незаполненных полей не осталось
        self.assertTrue(updated)
        self.assertTrue(updater.changed_fields)
        empty_fields = OrderRequestRequiredFieldsChecker.check_child(child)
        self.assertEqual(len(empty_fields), 1)
        self.assertIn('address_full', empty_fields)
        # Проверка, что нужные поля были пустые и действительно изменились
        for changed_field in updater.changed_fields:
            self.assertFalse(getattr(child_before_changes, changed_field))
            self.assertTrue(getattr(child, changed_field))

    def _test_should_not_update(self, request_data, has_rf_document):
        """Проверка, когда данные ребёнка не должны обновляться.

        :param request_data: Данные запроса
        :param has_rf_document: Наличие российского документа
        """

        declaration = self.create_declaration_with_data(
            **self.get_dul_type_params(has_rf_document)
        )
        child = declaration.children

        updater = ChildApplicationOrderInfoUpdater(child, request_data)
        # Проверка, что все нужные поля заполнены
        self.assertFalse(OrderRequestRequiredFieldsChecker.check_child(child))

        updated = updater.run()

        # Проверка, что обновления не было и незаполненных полей нет
        self.assertFalse(
            updated, f'Обновленные поля - {updater.changed_fields}')
        self.assertFalse(updater.changed_fields)
        self.assert_not_have_empty_fields(
            OrderRequestRequiredFieldsChecker.check_child(child))

    def test_zags_act_number(self):
        """Проверка обновления номера актовой записи

        При номере актовой записи "000" поле считается незаполненным
        """
        request_data = self.rf_doc_request_data
        declaration = self.create_declaration_with_data(
            **self.get_dul_type_params(has_rf_document=True)
        )
        child = declaration.children

        child.zags_act_number = DEFAULT_ZAGS_ACT_NUMBER
        child.save()

        updater = ChildApplicationOrderInfoUpdater(child, request_data)
        updated = updater.run()

        # Проверка, что обновление поля было для "000"
        self.assertTrue(updated)
        self.assertIn('zags_act_number', updater.changed_fields)
        zags_act_number = child.zags_act_number
        self.assertTrue(
            zags_act_number and zags_act_number != DEFAULT_ZAGS_ACT_NUMBER)

        updater = ChildApplicationOrderInfoUpdater(child, request_data)
        updated = updater.run()

        # Проверка, что обновления поля не было
        self.assertFalse(updated)
        self.assertNotIn('zags_act_number', updater.changed_fields)

    def test_rf_child_document(self):
        """Проведение проверок для ребёнка с российским документом."""
        tests_args = self.rf_doc_request_data, True
        self._test_should_not_update(*tests_args)
        self._test_should_to_be_filled(*tests_args)

    def test_foreign_child_document(self):
        """Проведение проверок для ребёнка с иностранным документом."""
        tests_args = self.foreign_doc_request_data, False
        self._test_should_not_update(*tests_args)
        self._test_should_to_be_filled(*tests_args)


class DelegateApplicationOrderInfoUpdaterTC(BaseApplicationOrderInfoTC):
    """Тесты для класса DelegateApplicationOrderInfoUpdater."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # Данные для российского документа
        cls.test_data = get_test_data_for_template(has_rf_document=True)
        cls.request_data = cls.get_prepared_request(cls.test_data)
        cls.has_rf_document = True

        # Выставляем код ЕСНСИ для документа родителя
        DULDelegateType.objects.filter(id=DULDelegateType.RF_PASSPORT).update(
            esnsi_code=DUL_DELEGATE_TYPE_ENSI)

    def assert_not_have_empty_fields(self, empty_fields):
        """Проверка, что нет пустых полей

        :param empty_fields: Незаполненные поля
        """
        self.assertFalse(
            bool(empty_fields),
            f'Есть незаполненные поля: {",".join(empty_fields)}'
        )

    @classmethod
    def create_delegate_with_minimal_data(cls, **dop_params):
        """Создания представителя с минимумом данных."""

        params = dict(
            surname='Тестовый',
            firstname='Родитель',
            date_of_birth=test_date,
        )
        params.update(dop_params)

        with mute_signals(pre_save, post_save):
            delegate = Delegate.objects.create(**params)
        return delegate

    @classmethod
    def create_delegate_with_data(cls, **dop_params):
        """Создания представителя с минимумом данных."""

        person_info = cls.test_data['person']
        doc_info = cls.test_data['person_doc_info']
        params = dict(
            surname='Тестовый',
            firstname='Родитель',
            date_of_birth=test_date,
            phones=person_info['phone'],
            email=person_info['email'],
            dul_issued_by=doc_info['issued_by'],
        )
        params.update(dop_params)

        with mute_signals(pre_save, post_save):
            delegate = DelegateF.create(**params)
        return delegate

    def test_should_to_be_filled(self):
        """Проверка, когда данные представителя должны обновиться."""

        delegate = self.create_delegate_with_minimal_data()
        delegate_before_changes = get_instance(delegate.id, Delegate)

        updater = DelegateApplicationOrderInfoUpdater(
            delegate, self.request_data)
        updated = updater.run()

        # Проверка, что обновления было и незаполненных полей не осталось
        self.assertTrue(updated)
        self.assertTrue(updater.changed_fields)
        self.assert_not_have_empty_fields(
            OrderRequestRequiredFieldsChecker.check_delegate(delegate))

        # Проверка, что нужные поля были пустые и действительно изменились
        for changed_field in updater.changed_fields:
            self.assertFalse(getattr(delegate_before_changes, changed_field))
            self.assertTrue(getattr(delegate, changed_field))

    def test_should_not_update(self):
        """Проверка, когда данные представителя не должны обновляться."""

        delegate = self.create_delegate_with_data()
        updater = DelegateApplicationOrderInfoUpdater(
            delegate, self.request_data)
        # Проверка, что все нужные поля заполнены
        self.assertFalse(
            OrderRequestRequiredFieldsChecker.check_delegate(delegate))

        updated = updater.run()

        # Проверка, что обновления не было и незаполненных полей нет
        self.assertFalse(updated)
        self.assertFalse(updater.changed_fields)
        self.assert_not_have_empty_fields(
            OrderRequestRequiredFieldsChecker.check_delegate(delegate))
