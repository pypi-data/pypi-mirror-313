import datetime

from concentrator.change import (ChangeHelper, ChangesMap,
                                 DeclarationPrivilegeChangeHelper,
                                 DeclarationUnitChangeHelper,
                                 DeclarationDocsChangeHelper)
from concentrator.smev3.applicationrequest import compare, rules
from kinder.core.helpers import recursive_getattr
from kinder.core.privilege.models import Privilege

from .utils import process_attachments


ID_CHOICE = 'id'
CODE_CHOICE = 'code'


class Smev3ChangesMap(ChangesMap):
    """Карта полей изменений для Smev3."""

    _map = {
        'Declaration': [
            ('desired_date', datetime.date, 'EntryDate'),
            ('offer_other', bool, 'EduOrganizations\AllowOfferOther'),
            ('work_type', CODE_CHOICE, 'ScheduleType\code'),
        ],
        'Delegate': [
            ('firstname', str, 'PersonInfo\PersonName'),
            ('surname', str, 'PersonInfo\PersonSurname'),
            ('patronymic', str, 'PersonInfo\PersonMiddleName'),
            ('date_of_birth', datetime.date, 'PersonInfo\PersonBirthDate'),
            ('snils', str, 'PersonInfo\PersonSNILS'),
            ('dul_type', CODE_CHOICE,
             'PersonInfo\PersonIdentityDocInfo\IdentityDocName\code'),
            ('dul_series', str,
             'PersonInfo\PersonIdentityDocInfo\IdentityDocSeries'),
            ('dul_number', str,
             'PersonInfo\PersonIdentityDocInfo\IdentityDocNumber'),
            ('dul_issued_by', str,
             'PersonInfo\PersonIdentityDocInfo\IdentityDocIssued'),
            ('dul_date', datetime.date,
             'PersonInfo\PersonIdentityDocInfo\IdentityDocIssueDate'),
            ('type', int, 'PersonInfo\PersonType\code'),
            ('email', str, 'PersonInfo\PersonEmail'),
            ('phones', str, 'PersonInfo\PersonPhone'),
        ],
        'Children': [
            ('firstname', str, 'ChildInfo\ChildName'),
            ('surname', str, 'ChildInfo\ChildSurname'),
            ('patronymic', str, 'ChildInfo\ChildMiddleName'),
            ('reg_address_full', str, 'Address\FullAddress'),
            ('dul_series', str,
             'ChildInfo\ChildBirthDocRF\ChildBirthDocSeries'),
            ('dul_number', str,
             'ChildInfo\ChildBirthDocRF\ChildBirthDocNumber'),
            ('dul_date', datetime.date,
             'ChildInfo\ChildBirthDocRF\ChildBirthDocIssueDate'),
            ('zags_act_number', str,
             'ChildInfo\ChildBirthDocRF\ChildBirthDocActNumber'),
            ('birthplace', str, 'ChildInfo\ChildBirthDocRF\ChildBirthPlace'),
            ('date_of_birth', datetime.date, 'ChildInfo\ChildBirthDate'),
            ('snils', str, 'ChildInfo\ChildSNILS'),
        ],
    }

    # Функции сравнения значения двух объектов по типу поля
    compare_functions = {
        ID_CHOICE: compare.compare_model_id,
        CODE_CHOICE: compare.compare_dict_code,
        datetime.date: compare.compare_date,
        datetime.datetime: compare.compare_datetime,
        str: compare.compare_str,
        bool: compare.compare_bool_int,
        int: compare.compare_bool_int,
    }

    def __init__(self):
        """Переопределен для предотвращения добавления
        в Delegate notification_type_mapping, так как по СМЭВ 3
        данные не передаются в ApplicationType."""
        pass

    def get_function_compare(self, type_value):
        """Переопределяет получение функции сравнения по типу поля."""

        compare_function = self.compare_functions.get(type_value)

        if compare_function is None:
            raise ValueError('Неизвестный тип поля')

        return compare_function


class Smev3ChangeHelper(ChangeHelper):
    """Проверка изменений в полях для Smev3."""

    convert_rules = {
        'work_type': rules.WorktypeRule,
        'dul_type': rules.DelegateTypeRule,
        'type': rules.DelegateTypeRule,
    }

    def check_diff(self, conc_object, save_object):
        """Переопределяет проверку изменений между концентратором и системой."""

        instance_model = save_object or conc_object
        for model_field, type_value, conc_field in (
                self.map_changes.get(self.name_model)):

            conc_value = recursive_getattr(
                conc_object, conc_field.replace('\\', '__'))

            if model_field in self.convert_rules:
                conc_value = (
                    self.convert_rules[model_field].system_value(conc_value))

            save_value = recursive_getattr(
                save_object, model_field.replace('.', '__'))
            compare_func = self.map_changes.get_function_compare(type_value)

            if not compare_func(conc_value, save_value):
                self._handling_change(
                    model_field, type_value, conc_value, save_value,
                    instance_model)


class Smev3DeclarationUnitChangeHelper(DeclarationUnitChangeHelper):
    """Проверка изменений желаемых учреждений."""

    @staticmethod
    def _system_units(declaration_obj):
        """Желаемые учреждения в системе."""

        return declaration_obj.declarationunit_set.values_list(
            'unit_id', 'ord')

    @staticmethod
    def _concentrator_units(concentrator_obj):
        """Желаемые учреждения пришедшие с концентратора."""

        return tuple(
            (int(unit.code), int(order)) for order, unit in
            enumerate(concentrator_obj.EduOrganizations.EduOrganization, 1))

    def check_diff(self, conc_object, save_object):
        """Переопределяет проверку изменений между концентратором и системой."""

        concentrator_units = self._concentrator_units(conc_object)
        system_units = self._system_units(save_object)

        super().check_diff(concentrator_units, system_units)


class Smev3DeclarationPrivilegeChangeHelper(DeclarationPrivilegeChangeHelper):
    """Проверка изменений льгот."""

    @staticmethod
    def _system_benefits(declaration_obj):
        """Льготы по заявке в системе."""

        return declaration_obj.declarationprivilege_set.values_list(
            'privilege_id', flat=True)

    @staticmethod
    def _concentrator_benefits(concentrator_obj):
        """Льготы пришедшие с концентратора."""

        return tuple(
            benefit.BenefitCategory.code
            for benefit in concentrator_obj.BenefitsInfo.BenefitInfo
        )

    def check_diff(self, conc_object, save_object):
        """Переопределяет проверку изменений между концентратором и системой."""

        concentrator_benefits = self._concentrator_benefits(conc_object)
        system_benefits = self._system_benefits(save_object)

        super().check_diff(concentrator_benefits, system_benefits)


class Smev3DeclarationDocsChangeHelper(DeclarationDocsChangeHelper):
    """
    Проверка изменения прикреплённых файлов
    """
    def check_diff(self, declaration, attachments):
        extra_docs = process_attachments(attachments, declaration, False)

        for doc in extra_docs:
            self._result.append({'code': ('Код', doc.name, None)})
            self._result.append({'name': ('Имя', doc.name, None)})

        if extra_docs:
            self._result.append(
                {
                    self.NAME_LIST_ID:
                        ('Список документов',
                         ','.join(str(doc.id) for doc in extra_docs), None)
                })
