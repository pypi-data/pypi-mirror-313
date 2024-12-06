from datetime import date

from django.db.models.signals import post_save, pre_save
from factory.django import mute_signals

from concentrator.smev3.applicationrequest.changes import (Smev3ChangeHelper,
                                                           Smev3ChangesMap,
                                                           Smev3DeclarationPrivilegeChangeHelper,
                                                           Smev3DeclarationUnitChangeHelper)
from kinder.core.children.models import DelegateTypeEnumerate
from kinder.core.children.tests.factory_child import ChildF, DelegateF
from kinder.core.declaration.models import (DeclarationPrivilege,
                                            DeclarationUnit)
from kinder.core.declaration.tests.factory_declaration import (DeclarationF,
                                                               DPrivilegeF,
                                                               DUnitF)
from kinder.core.dict.models import DULDelegateType, WorkType

from .base import ApplicationTC


class DiffTC(ApplicationTC):

    def _diff(self, instance):
        changes_map = Smev3ChangesMap()
        helper = Smev3ChangeHelper(
            instance.__class__,
            instance.__class__.__name__,
            map_changes=changes_map)
        helper.check_diff(self.application, instance)
        return helper.get_result()

    def _diff_fields(self, diff):
        for change in diff:
            for key in list(change.keys()):
                yield key

    def _msg(self, diff, field):
        diff_dict = [d for d in diff if field in list(d.keys())]
        if diff_dict:
            return '{}: {} != {}'.format(*diff_dict[0][field])
        return '{} not in diff'.format(field)

    def assertFieldNotChanged(self, instance, field):
        diff = self._diff(instance)
        diff_fields = tuple(self._diff_fields(diff))
        self.assertNotIn(
            field, diff_fields, msg=self._msg(diff, field).encode('utf-8'))


class DeclarationChangesTC(DiffTC):

    def test_desired_date(self):
        decl = DeclarationF.create(desired_date=date(2018, 9, 1))
        self.assertFieldNotChanged(decl, 'desired_date')

    def test_offer_other(self):
        decl = DeclarationF.create(offer_other=True)
        self.assertFieldNotChanged(decl, 'offer_other')

    def test_work_type(self):
        decl = DeclarationF.create()
        decl.work_type = WorkType.objects.get(code=WorkType.ALLDAY)
        decl.save()
        self.assertFieldNotChanged(decl, 'work_type')


class ChildrenChangesTC(DiffTC):

    def test_first_name(self):
        child = ChildF.create(firstname='Василий')
        self.assertFieldNotChanged(child, 'firstname')

    def test_surname(self):
        child = ChildF.create(surname='Иванов')
        self.assertFieldNotChanged(child, 'surname')

    def test_patronymic(self):
        child = ChildF.create(patronymic='Александрович')
        self.assertFieldNotChanged(child, 'patronymic')

    def test_reg_address_full(self):
        child = ChildF.create(
            reg_address_full='121351, Москва г., Бобруйская ул., 4 д., 2 корп.')
        self.assertFieldNotChanged(child, 'reg_address_full')

    def test_dul_series(self):
        child = ChildF.create(dul_series='VII-ЛД')
        self.assertFieldNotChanged(child, 'dul_series')

    def test_dul_number(self):
        child = ChildF.create(dul_number='132564')
        self.assertFieldNotChanged(child, 'dul_number')

    def test_dul_date(self):
        child = ChildF.create(dul_date=date(2016, 2, 10))
        self.assertFieldNotChanged(child, 'dul_date')

    def test_zags_act_number(self):
        child = ChildF.create(zags_act_number='13245')
        self.assertFieldNotChanged(child, 'zags_act_number')

    def test_birthplace(self):
        child = ChildF.create(birthplace='г. Самара')
        self.assertFieldNotChanged(child, 'birthplace')


class DelegateChangesTC(DiffTC):

    def test_firstname(self):
        delegate = DelegateF.create(firstname='Елена')
        self.assertFieldNotChanged(delegate, 'firstname')

    def test_surname(self):
        delegate = DelegateF.create(surname='Иванова')
        self.assertFieldNotChanged(delegate, 'surname')

    def test_patronymic(self):
        delegate = DelegateF.create(patronymic='Викторовна')
        self.assertFieldNotChanged(delegate, 'patronymic')

    def test_date_of_birth(self):
        delegate = DelegateF.create(date_of_birth=date(1993, 10, 20))
        self.assertFieldNotChanged(delegate, 'date_of_birth')

    def test_snils(self):
        delegate = DelegateF.create(snils='000-102-103 44')
        self.assertFieldNotChanged(delegate, 'snils')

    def test_dul_type(self):
        delegate = DelegateF.create(dul_type__code=DULDelegateType.RF_PASSPORT)
        self.assertFieldNotChanged(delegate, 'dul_type')

    def test_dul_series(self):
        delegate = DelegateF.create(dul_series='6004')
        self.assertFieldNotChanged(delegate, 'dul_series')

    def test_dul_number(self):
        delegate = DelegateF.create(dul_number='586830')
        self.assertFieldNotChanged(delegate, 'dul_number')

    def test_dul_issued_by(self):
        delegate = DelegateF.create(dul_issued_by='Отделением УФМС России')
        self.assertFieldNotChanged(delegate, 'dul_issued_by')

    def test_dul_date(self):
        delegate = DelegateF.create(dul_date=date(2007, 9, 10))
        self.assertFieldNotChanged(delegate, 'dul_date')

    def test_type(self):
        delegate = DelegateF.create(type=DelegateTypeEnumerate.MOTHER)
        self.assertFieldNotChanged(delegate, 'type')

    def test_email(self):
        delegate = DelegateF.create(email='test@test.ru')
        self.assertFieldNotChanged(delegate, 'email')

    def test_phones(self):
        delegate = DelegateF.create(phones='+7(123)1234567')
        self.assertFieldNotChanged(delegate, 'phones')


class DeclarationUnitChangesTC(ApplicationTC):

    def diff(self, instance):
        helper = Smev3DeclarationUnitChangeHelper(
            DeclarationUnit, 'DeclarationUnit')
        helper.check_diff(self.application, instance)
        return helper.get_result()

    def test_units_not_changed(self):
        """Желаемые учреждения не изменились."""
        decl = DeclarationF.create()
        with mute_signals(pre_save, post_save):
            DUnitF.create(declaration=decl, unit__id=215, ord=1)
            DUnitF.create(declaration=decl, unit__id=219, ord=2)
            DUnitF.create(declaration=decl, unit__id=221, ord=3)
        self.assertEquals(self.diff(decl), [])

    def test_unit_changed_all(self):
        """Добавились новые желаемые учреждения к заявке."""
        decl = DeclarationF.create()
        self.assertEquals(
            self.diff(decl), [
                {'conc_unit': (215, 1)},
                {'conc_unit': (219, 2)},
                {'conc_unit': (221, 3)}
            ])

    def test_unit_changed_order(self):
        """У Желаемого учреждения изменился приоритет."""
        decl = DeclarationF.create()
        with mute_signals(pre_save, post_save):
            DUnitF.create(declaration=decl, unit__id=221, ord=4)
        self.assertEquals(
            self.diff(decl), [
                {'conc_unit': (215, 1)},
                {'conc_unit': (219, 2)},
                {'conc_unit': (221, 3)},
                {'sys_unit': (221, 4)}
            ])


class DeclarationPrivilegeChangesTC(ApplicationTC):

    fixtures = [
        'start_data_dict', 'status_initial_data', 'priv_test_initial_data']

    # Словарь для перевода id льгот из концентратора (из фикстуры)
    # в id льгот системы
    privilege_rules = {
        '5': 30,  # Дети родителей и врачей
        '19': 7,  # Дети военнослужащих
    }

    def diff(self, instance):
        helper = Smev3DeclarationPrivilegeChangeHelper(
            DeclarationPrivilege, 'DeclarationPrivilege')
        helper.check_diff(self.application, instance)
        return helper.get_result()

    def test_benefits_not_changed(self):
        """Льготы не изменились."""
        decl = DeclarationF.create()
        sys_val = self.privilege_rules.get
        DPrivilegeF.create(declaration=decl, privilege__id=sys_val('5'))
        DPrivilegeF.create(declaration=decl, privilege__id=sys_val('19'))
        self.assertEquals(self.diff(decl), [])

    def test_new_benefit(self):
        """Добавление льготы к заявке."""
        decl = DeclarationF.create()
        sys_val = self.privilege_rules.get
        DPrivilegeF.create(declaration=decl, privilege__id=sys_val('5'))
        self.assertEquals(
            self.diff(decl), [
                {'conc_unit': (sys_val('5'), sys_val('19'))},
                {'sys_unit': (sys_val('5'), )}])
