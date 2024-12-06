import abc
import datetime
from collections import defaultdict

from django.db.models.fields import NOT_PROVIDED
from educommon.contingent import catalogs

from kinder.core.children.models import Children
from kinder.core.declaration.models import DeclarationPrivilege
from kinder.core.declaration.models import DeclarationUnit
from kinder.core.dict.models import GroupType
from kinder.core.helpers import recursive_getattr
from kinder.core.helpers import recursive_get_verbose_name
from kinder.core.privilege.models import Privilege
from kinder.core.unit.models import Unit

from concentrator.change import BaseStorageHelper
from concentrator.change import ChangeHelper
from concentrator.change import ChangesMap
from concentrator.change import ChildrenChangeHelper
from concentrator.change import DeclarationChangeHelper
from concentrator.change import DeclarationDocsChangeHelper
from concentrator.change import DelegateChangeHelper
from concentrator.changes import rules
from concentrator.models import ChangeStatus

from . import compare
from .rules import DelegateConfRightsRule
from .utils import get_address_place_code
from .utils import get_application_request_full_address
from .utils import process_attachments

ESNSI = 'esnsi'
NULL_ESNSI = 'null_esnsi'
PARENTS = 'parents'
BOOL_NOT_NULL = 'bool_not_null'
PARENT_DOC = 'parent_doc'
HEALTH_NEED = 'health_need'
FIAS = 'fias'
FIAS_PLACE = 'fias_place'
FIAS_FULL_ADDRESS = 'fias_full_address'


class Smev3ChangesMap(ChangesMap):
    """Карта полей изменений для Smev3."""

    _map = {
        'Declaration': [
            ('desired_date', datetime.date, 'EntryParams\EntryDate'),
            ('work_type', ESNSI, 'EntryParams\Schedule\code'),
            ('spec', ESNSI, 'EntryParams\Language\code'),
            ('consent_full_time_group', bool, 'EntryParams\AgreementOnFullDayGroup'),
            ('offer_other', bool, 'EduOrganizations\AllowOfferOther'),
            ('consent_dev_group', bool, 'AdaptationProgram\AgreementOnGeneralGroup'),
            ('consent_care_group', bool, 'AdaptationProgram\AgreementOnCareGroup'),
            ('desired_group_type', ESNSI, 'AdaptationProgram\AdaptationGroup\code'),
            ('adapted_program_consent', bool, 'AdaptationProgram\AgreementAdaptationEducationGroup'),
        ],
        'Delegate': [
            ('firstname', str, 'PersonInfo\PersonName'),
            ('surname', str, 'PersonInfo\PersonSurname'),
            ('patronymic', str, 'PersonInfo\PersonMiddleName'),
            ('dul_type', ESNSI,
             'PersonIdentityDocInfo\IdentityDocName\code'),
            ('dul_series', str, 'PersonIdentityDocInfo\IdentityDocSeries'),
            ('dul_number', str, 'PersonIdentityDocInfo\IdentityDocNumber'),
            ('dul_issued_by', str, 'PersonIdentityDocInfo\IdentityDocIssued'),
            ('dul_date', datetime.date,
             'PersonIdentityDocInfo\IdentityDocIssueDate'),
            ('email', str, 'PersonInfo\PersonEmail'),
            ('phones', str, 'PersonInfo\PersonPhone'),
            ('type', PARENTS, 'PersonInfo\Parents'),
            ('delegatecontingent.doc_type', PARENT_DOC, 
             'PersonInfo\OtherRepresentative\OtherRepresentativeDocName'),
            ('delegatecontingent.series', str, 
             'PersonInfo\OtherRepresentative\OtherRepresentativeDocSeries'),
            ('delegatecontingent.number', str, 
             'PersonInfo\OtherRepresentative\OtherRepresentativeDocNumber'),
            ('delegatecontingent.date_issue', datetime.date, 
             'PersonInfo\OtherRepresentative\OtherRepresentativeDocDate'),
            ('delegatecontingent.issued_by', str, 
             'PersonInfo\OtherRepresentative\OtherRepresentativeDocIssued'),
            ('confirming_rights_located_rf', bool, 'ConfirmingRightIsLocatedRF'),
        ],
        'Children': [
            ('firstname', str, 'ChildInfo\ChildName'),
            ('surname', str, 'ChildInfo\ChildSurname'),
            ('patronymic', str, 'ChildInfo\ChildMiddleName'),
            ('date_of_birth', datetime.date, 'ChildInfo\ChildBirthDate'),
            ('address_full', FIAS_FULL_ADDRESS, 'Address\FullAddress'),
            ('address_place', FIAS_PLACE, 'Address\Place\code'),
            ('address_street', FIAS, 'Address\Street\code'),
            ('address_house', str, 'Address\House\\valueOf_'),
            ('address_house_guid', FIAS, 'Address\House\code'),
            ('address_corps', str, 'Address\Building1'),
            ('address_flat', str, 'Address\Apartment'),
            ('health_need_special_support', BOOL_NOT_NULL, 'AdaptationProgram\\NeedSpecialCareConditions'),
            ('health_need_confirmation', NULL_ESNSI, 'MedicalReport\DocName\code'),
            ('health_series', str, 'MedicalReport\DocSeries'),
            ('health_number', str, 'MedicalReport\DocNumber'),
            ('health_need_start_date', datetime.date, 'MedicalReport\DocIssueDate'),
            ('health_issued_by', str, 'MedicalReport\DocIssued'),
            ('health_need_expiration_date', datetime.date, 'MedicalReport\DocExpirationDate'),
            ('dul_series', str,
             'ChildInfo\ChildBirthDocRF\ChildBirthDocSeries'),
            ('dul_number', str,
             'ChildInfo\ChildBirthDocRF\ChildBirthDocNumber'),
            ('dul_date', datetime.date,
             'ChildInfo\ChildBirthDocRF\ChildBirthDocIssueDate'),
            ('zags_act_number', str,
             'ChildInfo\ChildBirthDocRF\ChildBirthDocActNumber'),
            ('zags_act_place', str,
             'ChildInfo\ChildBirthDocRF\ChildBirthDocIssued'),
            ('zags_act_date', datetime.date,
             'ChildInfo\ChildBirthDocRF\ChildBirthDocActDate'),
            ('health_need', HEALTH_NEED,
             'AdaptationProgram\AdaptationGroupType\code'),
        ],
    }

    # Функции сравнения значения двух объектов по типу поля
    compare_functions = {
        datetime.date: compare.compare_date,
        datetime.datetime: compare.compare_datetime,
        str: compare.compare_str,
        bool: compare.compare_bool_int,
        int: compare.compare_bool_int,
        ESNSI: compare.compare_esnsi,
        NULL_ESNSI: compare.compare_null_esnsi,
        PARENT_DOC: compare.compare_parent_doc,
        PARENTS: compare.compare_parents,
        BOOL_NOT_NULL: compare.compare_bool_not_null,
        HEALTH_NEED: compare.compare_esnsi,
        FIAS: compare.compare_fias,
        FIAS_PLACE: compare.compare_place_fias,
        FIAS_FULL_ADDRESS: compare.compare_full_address,
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

    convert_rules = {}

    def __init__(self, model, name_model, map_changes=None):
        map_changes = map_changes or Smev3ChangesMap()
        super().__init__(model, name_model, map_changes=map_changes)

    def check_diff(self, conc_object, save_object):
        """Переопределяет проверку изменений между концентратором и системой."""

        instance_model = save_object or conc_object
        for model_field, type_value, conc_field in (
                self.map_changes.get(self.name_model)):

            try:
                conc_value = recursive_getattr(
                    conc_object, conc_field.replace('\\', '__'))
            except AttributeError:
                continue

            if model_field in self.convert_rules:
                conc_value = (
                    self.convert_rules[model_field].system_value(conc_value))

            save_value = recursive_getattr(
                save_object, model_field.replace('.', '__'))
            compare_func = self.map_changes.get_function_compare(type_value)

            if not compare_func(
                    conc_value, save_value, conc_object, save_object
            ):
                self._handling_change(
                    model_field, type_value, conc_value, save_value,
                    instance_model, conc_object, save_object)

    def _handling_change(
            self, field, type_value, conc_value, save_value,
            instanse_model, conc_object, save_object
    ):
        """Переопределили для получения id записей справочника по коду esnsi.

        :param field: имя поля модели
        :param type_value: тип значения поля: int, str и тд
        :param conc_value: значение поля модели из концентратора
        :param save_value: текущее значение поля модели
        :param instanse_model: инстанс django модели ,
        для получения verbose_name поля
        :param conc_object: объект концентратора
        :param save_object: объект БД
        :return:

        """

        if '.' in field:
            name_field = recursive_get_verbose_name(
                instanse_model, field.replace('.', '__'))
        else:
            name_field = self.model_field[field].verbose_name

        # Если тэг с параметром не был передан/оказался пуст
        if conc_value is None:

            if '.' in field:
                remote_field, _field = field.split('.')
                meta = type(instanse_model)._meta.get_field(
                    remote_field).remote_field.model._meta.get_field(_field)
            else:
                meta = type(instanse_model)._meta.get_field(field)

            default = meta.default
            nullable = meta.null
            # Если параметр по умолчанию не был установлен или соответсвующее
            # поле может быть null, выполнение функции не прерывается
            if default != NOT_PROVIDED and not nullable:
                # Если параметр по умолчанию актуален, нет смысла добавлять
                # изменение
                if default != save_value:
                    self._result.append({
                        field: (name_field, default, save_value)
                    })
                return

        if type_value in (ESNSI, NULL_ESNSI):
            dict_model = (
                type(instanse_model)._meta.get_field(field).remote_field.model)
            conc_value = (
                dict_model.objects.only('id').get(esnsi_code=conc_value))
            self._result.append(
                {field: (name_field,
                         conc_value.id if conc_value else conc_value,
                         save_value.id if save_value else save_value)})
        elif type_value == HEALTH_NEED:
            dict_model = (
                type(instanse_model)._meta.get_field(field).remote_field.model)
            adapt_prog = conc_object.AdaptationProgram
            group_type = (
                    adapt_prog.AdaptationGroup
                    and adapt_prog.AdaptationGroup.code)
            if group_type:
                group_type = GroupType.objects.get(esnsi_code=group_type)
                conc_value = dict_model.objects.only('id').get(
                    esnsi_code=conc_value, group_type=group_type)
                self._result.append(
                    {field: (name_field,
                            conc_value.id if conc_value else conc_value,
                            save_value.id if save_value else save_value)})
            else:
                try:
                    conc_value = (
                        dict_model.objects.only('id').get(
                            esnsi_code=conc_value, group_type=group_type))
                except (
                        dict_model.DoesNotExist,
                        dict_model.MultipleObjectsReturned
                ):
                    pass
                else:
                    self._result.append({
                        field: (
                            name_field,
                            conc_value.id if conc_value else conc_value,
                            save_value.id if save_value else save_value)})
        elif type_value == PARENTS:
            from concentrator.smev3_v321.utils import update_middle_name_params

            params = {}
            update_middle_name_params(
                conc_object.PersonInfo.PersonMiddleName, params,
                is_parents=conc_value, is_initial=True)
            conc_value = params.get('type')
            self._result.append(
                {field: (name_field, conc_value, save_value)})
        elif type_value == BOOL_NOT_NULL:
            conc_value = bool(conc_value)
            self._result.append(
                {field: (name_field, conc_value, save_value)})
        elif type_value == PARENT_DOC:
            reverse_map = {
                v: k
                for k, v in catalogs.DocumentConfirmingTypes.values.items()
            }
            conc_value = reverse_map.get(conc_value, None)
            self._result.append(
                {field: (name_field, conc_value, save_value)})
        elif type_value == FIAS_PLACE:
            conc_value = get_address_place_code(conc_object.Address)
            self._result.append(
                {field: (name_field, conc_value, save_value)})
        elif type_value == FIAS_FULL_ADDRESS:
            conc_value = get_application_request_full_address(
                conc_object.Address)
            self._result.append(
                {field: (name_field, conc_value, save_value)})
        else:
            self._result.append(
                {field: (name_field, conc_value, save_value)})


class Smev3DeclarationChangeHelper(Smev3ChangeHelper, DeclarationChangeHelper):
    """
    Хэлпер изменений заявок
    """

    NAME_MODEL = 'Declaration'


class Smev3DelegateChangeHelper(Smev3ChangeHelper, DelegateChangeHelper):
    """
    Хэлпер изменений представителей
    """

    NAME_MODEL = 'Delegate'
    convert_rules = {
        'confirming_rights_located_rf': DelegateConfRightsRule
    }


class Smev3ChildrenChangeHelper(Smev3ChangeHelper, ChildrenChangeHelper):
    """
    Хэлпер изменений ребёнка
    """

    NAME_MODEL = 'Children'

    def check_diff(self, conc_object, save_object):
        """
        Переопределяет проверку изменений между концентратором и системой
        В случае, если изменения касаются иностранных документов ребенка,
        изменяет маппинг изменений на иностранные документы.
        """
        if conc_object.ChildInfo.ChildBirthDocForeign:
            # поля, которые обновляем для иностранных документов
            fields_to_update = [
                'dul_series', 'dul_number', 'dul_date', 'zags_act_place'
            ]
            self.map_changes._map['Children'] = [
                child_field for child_field in self.map_changes._map['Children']
                if child_field[0] not in fields_to_update
            ]

            self.map_changes.extend_changes_map('Children', [
                ('dul_series', str,
                 'ChildInfo\ChildBirthDocForeign\ChildBirthDocSeries'),
                ('dul_number', str,
                 'ChildInfo\ChildBirthDocForeign\ChildBirthDocNumber'),
                ('dul_date', datetime.date,
                 'ChildInfo\ChildBirthDocForeign\ChildBirthDocIssueDate'),
                ('zags_act_place', str,
                 'ChildInfo\ChildBirthDocForeign\ChildBirthDocIssued'),
            ])

        super().check_diff(conc_object, save_object)


class Smev3ComplexChangeHelper(ChangeHelper, metaclass=abc.ABCMeta):
    """
    Хэлпер сложных изменений
    """

    # Основная модель ID который используется для идентификации изменения
    # Например для Желаемого ДОО - это ДОО
    main_model = None
    # Поля заявки по которым строятся кортежи для определения изменений
    fields = ()

    CONC_OBJ = 'conc_obj'
    SYS_OBJ = 'sys_obj'

    # Виды изменений
    NEW = 'new'
    DELETE = 'delete'
    UPDATE_MAIN = 'update'

    # Функции показа изменений
    SHOW_FUNCTIONS = {
        NEW: (
            lambda obj: obj.__class__._meta.verbose_name,
            lambda obj, *old: '-',
            lambda obj, *new: obj.display()
        ),
        DELETE: (
            lambda obj: obj.__class__._meta.verbose_name,
            lambda obj, *old: obj.display(),
            lambda obj, *new: '-'
        ),
        UPDATE_MAIN: (
            lambda obj: obj.__class__._meta.verbose_name,
            lambda obj, *old: f'{obj.display()}: {", ".join(map(str, old))}',
            lambda obj, *new: f'{obj.display()}: {", ".join(map(str, new))}'

        )
    }

    @abc.abstractmethod
    def _get_system_values(self, declaration_obj):
        """
        Получение системных значений из заявки
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _get_concentrator_values(self, concentrator_obj):
        """
        Получение значений из запроса
        """
        raise NotImplementedError
    
    def check_diff(self, conc_object, save_object):
        """
        Проверка наличия изменений
        """
        concentrator_values = self._get_concentrator_values(conc_object)
        system_values = self._get_system_values(save_object)

        set_conc = set(concentrator_values)
        set_sys = set(system_values)

        if set_conc ^ set_sys:
            self._result.extend(
                [{self.CONC_OBJ: tuple(concentrator_values)},
                 {self.SYS_OBJ: tuple(system_values)}])

    def _extend_show_result(
        self, get_field, get_old, get_new, list_changes, rows
    ):
        """
        Показ изменения
        """
        for main_id, *change in list_changes:
            try:
                main_object = self.main_model.objects.get(id=main_id)
                # Делим изменения на 2 половины, 
                # в которых новые и старые значения 
                old_values = change[:len(change) // 2]
                new_values = change[len(change) // 2:]

                rows.append({
                    'field': get_field(main_object),
                    'old_value': get_old(main_object, *old_values),
                    'new_value': get_new(main_object, *new_values)
                })
            except self.main_model.DoesNotExist:
                pass
        
        return rows

    def _get_list(self, main_id, change, current):
        """
        Определения типа изменений
        """
        if change != current:
            return self.UPDATE_MAIN

    def _get_diff_data(self, current_state, future_state):
        """
        Получение списков изменений разделённых по типам
        """
        update_list = defaultdict(list)

        current_state_map = {
            id_: current
            for id_, *current in current_state
        }

        for main_id, *change in future_state:
            current = current_state_map.pop(main_id, None)
            if current is None:
                update_list[self.NEW].append(
                    (main_id, *((None,) * len(change)), *change)
                )
            else:
                list_name = self._get_list(main_id, change, current)
                if list_name:
                    update_list[list_name].append(
                        (main_id, *current, *change)
                    )

        for main_id, current in current_state_map.items():
            update_list[self.DELETE].append(
                (main_id, *current, *((None,) * len(current)))
            )
        
        return update_list
    
    def _get_future_state(self, difference):
        """
        Будущее состояние
        """
        for change in difference:
            if self.CONC_OBJ in change:
                return change[self.CONC_OBJ]
        
        return []

    def _get_current_state(self, difference, changes):
        """
        Текущее состояние
        """
        if changes.state == ChangeStatus.WAIT:
            # состояние модели на текущий момент
            get_data = rules.display_changes_map.get(self.name_model)
            data_now = get_data(changes)
            return list(data_now.all().values_list(*self.fields))
        else:
            for change in difference:
                if self.SYS_OBJ in change:
                    return change[self.SYS_OBJ]
        
        return []
    
    def show_change(self, difference, changes):
        """
        Показ изменений
        """
        rows = []

        curent_state = self._get_current_state(difference, changes)
        future_state = self._get_future_state(difference)

        update_lists = self._get_diff_data(curent_state, future_state)

        for name, update_list in update_lists.items():
            show_functions = self.SHOW_FUNCTIONS.get(name)
            if not show_functions:
                continue
                
            self._extend_show_result(
                *show_functions,
                update_list,
                rows
            )
        
        return rows
    
    @abc.abstractmethod
    def handle_change(self, list_name, data):
        """
        Обработка применения изменения
        """
        raise NotImplementedError
    
    def apply_change(self, difference, changes):
        """
        Применение изменений
        """
        curent_state = self._get_current_state(difference, changes)
        future_state = self._get_future_state(difference)
        update_lists = self._get_diff_data(curent_state, future_state)

        for list_name, list_data in update_lists.items():
            for data in list_data:
                self.handle_change(list_name, changes, data)

        return {}


class Smev3DeclarationUnitChangeHelper(Smev3ComplexChangeHelper):
    """
    Хэлпер изменений желаемых ДОО
    """

    NAME_MODEL = 'DeclarationUnit'

    main_model = Unit
    fields = ('unit_id', 'ord', 'sibling_id', 'sibling__fullname')

    CONC_OBJ = 'conc_unit'
    SYS_OBJ = 'sys_unit'
    MO_ID = 'mo_id'

    UPDATE_PRIORITY = 'update_priority'
    UPDATE_SUBLING = 'update_subling'

    SHOW_FUNCTIONS = {
        **Smev3ComplexChangeHelper.SHOW_FUNCTIONS,
        UPDATE_PRIORITY: (
            lambda obj: f'{obj.__class__._meta.verbose_name} - '
                        f'Приоритет ({obj.name})',
            lambda obj, ord_id, sub_id, sub_fullname: str(ord_id),
            lambda obj, ord_id, sub_id, sub_fullname: str(ord_id)
        ),
        UPDATE_SUBLING: (
            lambda obj: f'{obj.__class__._meta.verbose_name} - Посещает брат/сестра',
            lambda obj, ord_id, sub_id, sub_fullname: str(sub_fullname),
            lambda obj, ord_id, sub_id, sub_fullname: str(sub_fullname)
        ),
    }


    def apply_change(self, difference, changes):
        """Применяет изменения по МО в заявке, если они есть"""
        super().apply_change(difference, changes)

        for diff in difference:
            mo_diff = diff.get(self.MO_ID)
            if mo_diff:
                _, new_mo_id = mo_diff
                if new_mo_id != changes.declaration.mo_id:
                    changes.declaration.mo_id = new_mo_id
                    changes.declaration.save()

        return {}

    def show_change(self, difference, changes):
        """Добавляет изменения по МО, если они есть"""
        rows = super().show_change(difference, changes)

        for diff in difference:
            mo_diff = diff.get(self.MO_ID)
            if not mo_diff:
                continue

            old_mo_id, new_mo_id = mo_diff
            mo_names = dict(
                Unit.objects.filter(id__in=(old_mo_id, new_mo_id)).values_list(
                    'id', 'name')
            )
            rows.extend([
                {
                    'field': 'Муниципальное образование',
                    'old_value': mo_names.get(old_mo_id, ''),
                    'new_value': '-',
                },
                {
                    'field': 'Муниципальное образование',
                    'old_value': '-',
                    'new_value': mo_names.get(new_mo_id, ''),
                },
            ])

        return rows

    def check_diff(self, conc_object, save_object):
        """Проверяется наличие изменений МО в заявке"""
        super().check_diff(conc_object, save_object)

        edu_organizations = conc_object.EduOrganizations.EduOrganization
        if edu_organizations:
            unit_id = int(edu_organizations[0].code)
            new_mo = Unit.objects.get(id=unit_id).mo
            if new_mo.id != save_object.mo.id:
                self.get_result().append(
                    {self.MO_ID: (save_object.mo_id, new_mo.id)})

    def _get_system_values(self, declaration_obj):
        return declaration_obj.declarationunit_set.values_list(*self.fields)

    def _get_concentrator_values(self, concentrator_obj):
        subling_map = {}
        if concentrator_obj.BrotherSisterInfo:
            for info in concentrator_obj.BrotherSisterInfo:
                try:
                    params = {
                        'surname': info.ChildSurname,
                        'firstname': info.ChildName,
                        'pupil__grup__unit_id': int(info.EduOrganization.code)
                    }
                    if info.ChildMiddleName:
                        params['patronymic'] = info.ChildMiddleName
                    child = Children.objects.distinct().get(**params)
                    fullname = child.fullname
                    child = child.id
                except (Children.DoesNotExist, Children.MultipleObjectsReturned) as exc:
                    child = None
                    fullname = ' '.join(filter(None, (
                        info.ChildSurname,
                        info.ChildName,
                        info.ChildMiddleName,
                    )))
                    fullname = f'{fullname} (Ребёнок не найден)'
                
                subling_map[info.EduOrganization.code] = (child, fullname)

        return tuple(
            (
                int(unit.code), 
                int(unit.PriorityNumber),
                *subling_map.get(unit.code, (None, None))
            )
            for unit in concentrator_obj.EduOrganizations.EduOrganization
        )

    def _get_list(self, main_id, change, current):
        n_ord_id, n_sub_id, n_sub_fullname = change
        c_ord_id, c_sub_id, c_sub_fullname = current

        if n_ord_id != c_ord_id:
            return self.UPDATE_PRIORITY
        
        if n_sub_fullname != c_sub_fullname or n_sub_id != c_sub_id:
            return self.UPDATE_SUBLING
    
    def handle_change(self, list_name, changes, data):
        (
            main_id, old_ord, old_subling, old_fullname, 
            new_ord, new_subling, new_fullname
        ) = data
        if list_name == self.NEW:
            DeclarationUnit.objects.create(
                declaration=changes.declaration,
                unit_id=main_id,
                ord=new_ord,
                sibling_id=new_subling
            )
        elif list_name == self.DELETE:
            DeclarationUnit.objects.filter(
                declaration=changes.declaration,
                unit_id=main_id
            ).delete()
        elif list_name == self.UPDATE_PRIORITY:
            du = DeclarationUnit.objects.filter(
                declaration=changes.declaration,
                unit_id=main_id
            ).first()

            if du:
                du.ord = new_ord
                du.save()
        elif list_name == self.UPDATE_SUBLING:
            du = DeclarationUnit.objects.filter(
                declaration=changes.declaration,
                unit_id=main_id
            ).first()

            if du:
                du.sibling_id = new_subling
                du.save()


class Smev3DeclarationPrivilegeChangeHelper(Smev3ComplexChangeHelper):
    """
    Хэлпер изменений льгот
    """

    NAME_MODEL = 'DeclarationPrivilege'

    main_model = Privilege
    fields = ('privilege_id', 'doc_issued_by', 'doc_date', '_privilege_end_date')

    CONC_OBJ = 'conc_privilege'
    SYS_OBJ = 'sys_privilege'

    def _get_system_values(self, declaration_obj):
        return declaration_obj.declarationprivilege_set.values_list(*self.fields)
    
    def _get_concentrator_values(self, concentrator_obj):
        benefit_info = concentrator_obj.BenefitInfo

        if not benefit_info:
            return []

        try:
            privilege = Privilege.objects.get(esnsi_code=benefit_info.BenefitCategory.code)
        except Privilege.DoesNotExist:
            return []
        
        doc_info = (None, None, None)

        if benefit_info.BenefitDocInfo:
            info = benefit_info.BenefitDocInfo
            doc_info = (info.DocIssued, info.DocIssueDate, info.DocExpirationDate)

        return [(privilege.id, *doc_info),]
    
    def handle_change(self, list_name, changes, data):
        (
            main_id, old_doc_issued, old_doc_date, old_end_date,
            new_doc_issued, new_doc_date, new_end_date
        ) = data

        if isinstance(new_doc_date, str):
            new_doc_date = datetime.datetime.strptime(
                new_doc_date, '%Y-%m-%d %H:%M:%S')
        
        if isinstance(new_end_date, str):
            new_end_date = datetime.datetime.strptime(
                new_end_date, '%Y-%m-%d %H:%M:%S')

        if list_name == self.NEW:
            DeclarationPrivilege.objects.create(
                declaration=changes.declaration,
                privilege_id=main_id,
                doc_issued_by=new_doc_issued,
                doc_date=new_doc_date,
                _privilege_end_date=new_end_date
            )
        elif list_name == self.DELETE:
            DeclarationPrivilege.objects.filter(
                declaration=changes.declaration,
                privilege_id=main_id,
            ).delete()
        elif list_name == self.UPDATE_MAIN:
            dp = DeclarationPrivilege.objects.filter(
                declaration=changes.declaration,
                privilege_id=main_id,
            ).first()

            if dp:
                dp.doc_issued_by = new_doc_issued
                dp.doc_date = new_doc_date
                dp._privilege_end_date = new_end_date

                dp.save()


class Smev3DeclarationDocsChangeHelper(DeclarationDocsChangeHelper):
    """Проверка изменения прикреплённых файлов."""

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


class Smev3StorageHelper(BaseStorageHelper):
    """Предназначен для работы с заявлениями СМЭВ 3."""

    # карта соответствия Модель <-> ChangeHelper
    _map_change_helpers = {
        'Default': Smev3ChangeHelper
    }
    # переопределяемые обработчики изменений
    _map_override_change_helpers = {}
