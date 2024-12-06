from collections import defaultdict
import datetime
import json

from django.conf import settings as kinder_settings
from django.utils import timezone
from kinder.core.audit_log_kndg.helpers import get_field
from kinder.core.audit_log_kndg.helpers import get_model
from kinder.core.audit_log_kndg.models import AdditionalEncoder
from kinder.core.children.models import Delegate
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import DeclarationPrivilege
from kinder.core.declaration.models import DeclarationStatus
from kinder.core.declaration.models import DeclarationUnit
from kinder.core.declaration_status.models import DSS
from kinder.core.privilege.models import Privilege
from kinder.core.unit.models import Unit
from kinder.plugins.privilege_attributes.models import (
    PrivilegeConfirmationAttributes)
from kinder.plugins.privilege_attributes.models import PrivilegeOwnerEnum
from m3 import ApplicationLogicException
from yadic.container import Injectable

from concentrator.change import ChangeHelper
from concentrator.changes import rules
from concentrator.constants import PRIVILEGE_COMMENT
from concentrator.changes.helpers import format_change
from concentrator.exceptions import ValidationError
from concentrator.models import ChangeDeclaration
from concentrator.models import ChangeSource
from concentrator.models import ChangeStatus
from concentrator.models import PrivilegeComment
from concentrator.models import UpdateParams
from concentrator.rules import DeclarationStatusChangeRule

from .models import Changes
from .webservice.django_objects_proxy import DelegatePrivilegeProxy
from .webservice.helpers import get_decl_priv
from .webservice.helpers import get_priv_data

TYPE_CHOICE = 'choices'


class ChangesMap(object):
    """Соответствие полей django-моделей и полей моделей сервиса
    с учетом их типа.

    """

    _map = {
        # TODO: удалить проверку тех полей, которых никто
        #  никогда не будет изменять на строне концетратора
        'Declaration': [
            ('date', datetime.datetime, r'SubmitDate'),
            ('desired_date', datetime.date, r'EntryDate'),
            ('offer_other', bool, r'EduOrganizations\AllowOfferOther'),
            ('comment_privileges', str, r'Benefits\BenefitsDocInfo'),
            ('work_type', TYPE_CHOICE, r'Schedule\ScheduleType'),
        ],
        'Delegate': [
            ('firstname', str, r'Applicant\FirstName'),
            ('surname', str, r'Applicant\LastName'),
            ('patronymic', str, r'Applicant\MiddleName'),
            ('snils', str, r'Applicant\Snils'),
            ('dul_type', TYPE_CHOICE, r'Applicant\DocType'),
            ('dul_series', str, r'Applicant\DocSeria'),
            ('dul_number', str, r'Applicant\DocNumber'),
            ('dul_issued_by', str, r'Applicant\DocIssuerName'),
            ('dul_place', str, r'Applicant\DocIssuerDepartmentCode'),
            ('dul_date', datetime.date, r'Applicant\DocIssueDate'),
            ('type', int, r'Applicant\ApplicantType'),
            ('email', str, r'Applicant\Email'),
            ('phones', str, r'Applicant\PhoneNumber'),
            ('notification_type', int, r'Applicant\NotificationType'),
        ],
        'Children': [
            ('firstname', str, r'DeclaredPerson\FirstName'),
            ('surname', str, r'DeclaredPerson\LastName'),
            ('patronymic', str, r'DeclaredPerson\MiddleName'),
            ('snils', str, r'DeclaredPerson\Snils'),
            ('address_full', str, r'DeclaredPerson\AddressResidence'),
            ('reg_address_full', str,
             r'DeclaredPerson\AddressRegistration'),
            ('dul_series', str, r'DeclaredPerson\BirthDocSeria'),
            ('dul_number', str, r'DeclaredPerson\BirthDocNumber'),
            ('dul_date', datetime.date,
             r'DeclaredPerson\BirthDocIssueDate'),
            ('gender', int, r'DeclaredPerson\Sex'),
            ('health_need', TYPE_CHOICE, r'AdaptationProgramType'),
            ('zags_act_number', str, r'DeclaredPerson\BirthDocActNumber'),
            ('zags_act_place', str, r'DeclaredPerson\BirthDocIssuer'),
            ('zags_act_date', datetime.date, r'DateOfActNumber'),
            ('birthplace', str, r'DeclaredPerson\BirthPlace'),
        ],
        'PrivilegeComment': [
            ('concentrator_comment', str, r'BenefitItem\Comment')
        ],
        'PrivilegeConfirmationAttributes': [
            ('privilege_owner', int, r'WhoHaveBenefit\Type'),
            ('delegate.firstname', str, r'WhoHaveBenefit\FirstName'),
            ('delegate.surname', str, r'WhoHaveBenefit\LastName'),
            ('delegate.patronymic', str, r'WhoHaveBenefit\MiddleName'),
            ('delegate.snils', str, r'WhoHaveBenefit\Snils'),
            ('delegate.dul_type', TYPE_CHOICE, r'WhoHaveBenefit\DocType'),
            ('delegate.dul_series', str, r'WhoHaveBenefit\DocSeria'),
            ('delegate.dul_number', str, r'WhoHaveBenefit\DocNumber'),
            ('delegate.dul_place', str,
             r'WhoHaveBenefit\DocIssuerDepartmentCode'),
            ('delegate.dul_issued_by', str,
             r'WhoHaveBenefit\DocIssuerName'),
            ('delegate.dul_date', datetime.date,
             r'WhoHaveBenefit\DocIssueDate'),
        ]
    }

    @property
    def model_name_list(self):
        u"""
        Список имён классов моделей.

        :rtype: list

        """

        return sorted(self._map.keys())

    def extend_changes_map(self, model_name, fields_description):
        u"""
        Расширение (плагинами) соответствия полей.

        :param str model_name: имя класса джанга-модели
        :param list fields_description: список кортежей из:
            - имя поля джанга модели,
            - тип поля,
            - имя поля модели веб-сервиса

        """

        assert isinstance(fields_description, list)
        self._map[model_name] = fields_description

    def get(self, model_name):
        u"""Получение данных об обрабатываемых полях по имени модели."""
        return self._map[model_name]

    def get_field_info(self, name_field, name_model):
        """
        отдает информацию по полю
        :return:

        """

        tmp_list = [x for x in self.get(name_model) if x[0] == name_field]
        if len(tmp_list) != 1:
            raise Exception(u"Поле %s не найдено в описании модели %s" %
                            (name_field, name_model))
        return tmp_list[0]

    def get_read_only_fields(self):
        """
        Возвращает список полей недоступных для редактирования в ЕПГУ
        Это все поля из списка self._map,
        и не указанные в справочнике доступных

        :rtype: list

        """

        result = []
        editable_list = UpdateParams.objects.all().values_list(
            'model_name', 'field_name')
        for model_name in self.model_name_list:
            for sys_name, type_value, conc_name in self.get(model_name):
                if (model_name, sys_name) in editable_list:
                    continue
                result.append(conc_name)

        return result

    def get_function_compare(self, type_value):
        u"""
        Возвращает функцию сравнения, в зависимости от типа данных.

        Если не включено USE_TZ джанга хранит Naive datetime objects,
        а из сервсов приходят aware datetime objects,
        для их сравнения необходимо приведение.

        :raise: Exception
        :rtype: callable
        :returns: функция сравнения

        """

        if type_value == TYPE_CHOICE:
            def compare(x, y):
                if x and y:
                    return x.id == y.id
                else:
                    return x == y
            return lambda x, y: compare(x, y)

        elif type_value is datetime.date:
            def compare_dates(x, y):
                new_x = x
                new_y = y
                if isinstance(x, datetime.datetime):
                    new_x = x.date()
                if isinstance(y, datetime.datetime):
                    new_y = y.date()
                return new_x == new_y
            return lambda x, y: compare_dates(x, y)

        elif type_value is str:
            def compare_str(x, y):
                new_x = x if x else ''
                new_y = y if y else ''
                return new_x.lower() == new_y.lower()
            return lambda x, y: compare_str(x, y)

        elif type_value in [bool, int]:
            return lambda x, y: x == y

        elif type_value is datetime.datetime:
            def compare_datetimes(x, y):
                new_x = (
                    timezone.make_naive(x, timezone.get_default_timezone())
                    if timezone.is_aware(x) else x
                )
                new_y = y
                return new_x == new_y
            if kinder_settings.USE_TZ:
                return lambda x, y: x == y
            else:
                return lambda x, y: compare_datetimes(x, y)
        else:
            raise Exception(u'Неизвестный тип поля')

    def get_store_models(self):
        u"""
        Возвращает список моделей для интерфейса
        "Параметры для изменения данных через ЕПГУ"

        :rtype: list

        """

        return [(model_name, get_model(model_name)._meta.verbose_name)
                for model_name in self.model_name_list]

    def get_fields(self):
        u"""
        Список полей в привязке к моделям для интерфейса
        "Параметры для изменения данных через ЕПГУ".

        :returns: словарь вида
            {'Declaration':[('date', 'Дата подачи'),
            ('desired_date', '')],...}
        :rtype: dict

        """

        result = defaultdict(list)
        for model_name, field_description in self._map.items():
            model = get_model(model_name)
            list_fields = []
            for field_name, _, _ in field_description:
                field = get_field(model, field_name)
                if field and hasattr(field, 'verbose_name'):
                    verbose_name_field = field.verbose_name
                else:
                    continue
                list_fields.append((field_name, verbose_name_field))
            result[model_name] = list_fields
        return dict(result)


map_changes = ChangesMap()


class StorageHelper(metaclass=Injectable):
    """
    Отвечает за управлением изменений по разным моделям в целом
    Работает со списком изменений пришедших от концентратора,и в зависмости от
    модели применяет различные ChangeHelper

    """

    depends_on = ("source",)

    # карта соответствия Модель <-> ChangeHelper
    _map_change_helpers = {
        'Default': ChangeHelper
    }
    # переопределяемые обработчики изменений
    _map_override_change_helpers = {}

    @classmethod
    def register_change_helper(cls, model_name, change_helper):
        u"""
        Регистрация обработчика изменений модели во внутреннем кеше.

        :param str model_name: имя модели, подлежайшей изменению
        :param change_helper: класс обработчик изменений
        :type change_helper: Type[ChangeHelper]

        """

        assert issubclass(change_helper, ChangeHelper)
        cls._map_change_helpers[model_name] = change_helper

    @classmethod
    def register_override_change_helper(cls, model_name, change_helper):
        u"""
        Регистрация переопределенного обработчика изменений модели.

        :param str model_name: имя модели, подлежайшей изменению
        :param change_helper: класс обработчик изменений
        :type change_helper: Type[ChangeHelper]

        """

        assert issubclass(change_helper, ChangeHelper)
        cls._map_override_change_helpers[model_name] = change_helper

    @classmethod
    def get_change_helper(cls, model_name):
        u"""
        Получение ChangeHelper в зависимости от модели.

        :rtype: Type[ChangeHelper]

        """

        override = cls._map_override_change_helpers.get(model_name)
        if override:
            return override
        else:
            return cls._map_change_helpers.get(
                model_name,
                cls._map_change_helpers['Default']
            )

    @classmethod
    def create_change(cls, declaration, list_ch_help, raw_data=None,
                      source=ChangeSource.NEW_APPLICATION,
                      case_number=None):
        """
        :param list_ch_help : Список инстансов классов,каждый из
        котрых хранит изменени по 1 модели

        """

        result = {}
        if raw_data:
            result.update(raw_data)

        for ch_help in list_ch_help:
            assert isinstance(ch_help, ChangeHelper)
            diff = ch_help.get_result()
            if diff:
                result[ch_help.name_model] = diff

        is_only_comment = (len(result) == 1 and PRIVILEGE_COMMENT in result)
        if result and not is_only_comment:
            change = ChangeDeclaration(
                declaration=declaration,
                data=json.dumps(result, cls=AdditionalEncoder),
                source=source,
                case_number=case_number
            )
            change.save()
            return True
        return False

    @classmethod
    def get_change(cls, changes):
        """
        :param changes запись из ChangeDeclaration
        :return: Возвращает кортеж, первое значение которго говорит о том,
        нужно ли отклонить набор изменений, полученных с ЕПГУ. А это необходимо
        при наличии невалидных данных.
        Второе значение кортежа содержит данные об изменениях
        :rtype: (bool, list)

        """

        result = []
        for name_model, difference in json.loads(changes.data).items():
            class_model = get_model(name_model)
            change_helper = cls.get_change_helper(name_model)
            ch_help = change_helper(class_model, name_model)
            rows = ch_help.show_change(difference, changes)
            result.extend(rows)
        return result

    @classmethod
    def apply_changes(cls, changes, request, comment):
        """
        Сохраняет изменений, меняет статус на Исполнено
        :param cls:
        :param changes:
        :param request:
        :param comment:
        :return:

        """

        updated_fields = {}
        for name_model, difference in json.loads(changes.data).items():
            class_model = get_model(name_model)
            change_helper = cls.get_change_helper(name_model)
            ch_help = change_helper(class_model, name_model)
            updated_fields.update(ch_help.apply_change(difference, changes))
        changes.user = request.user
        changes.state = ChangeStatus.ACCEPT
        changes.commentary = comment
        changes.save()
        return updated_fields


class DeclarationChangeHelper(ChangeHelper):
    """
    Переопределяем, из за специфичной обработки
    смены статуса заявки

    """

    NAME_FIELD = 'status'

    def get_new_status(self):
        """
        :return:

        """

        return DeclarationStatus.objects.get(code=DSS.ARCHIVE)

    def get_status_change(self, declaration):
        status_verbose_name = Declaration.status.field.verbose_name
        return [
            {self.NAME_FIELD: (
                status_verbose_name,
                self.get_new_status().id,
                declaration.status.id)}
        ]

    def apply_change(self, difference, changes):
        """
        применит изменение в системе
        :return:

        """

        if not [x for x in difference if self.NAME_FIELD in list(x.keys())]:
            updated_fields = super(DeclarationChangeHelper,
                                   self).apply_change(difference, changes)
        else:
            new_status = self.get_new_status()
            DeclarationStatusChangeRule.change(changes.declaration, new_status)
            updated_fields = {'declaration.status_id': new_status.id}
        return updated_fields


class SetChangeHelper(ChangeHelper):
    NEW_NAME = 'conc_unit'
    SYS_NAME = 'sys_unit'
    MO_NAME = 'decl_mo'


class DeclarationUnitChangeHelper(SetChangeHelper):
    """
    Изменения желаемых организаций храним в другом формате,
    поэтому переопределяем методы сохранения, показа и применения изменений

    """

    def check_diff(self, conc_object, save_object, declaration_mo,
                   requested_mo):
        """
        Проверяет пришли ли изменения по объекту из концетратра
        - если пришли сохраняем желаемое состояние
        и текущее состояния, для показа в дальнейшем истории изменений
        :param conc_object: список из (id, ord)
        жел. организаций из запроса на изменение
        :param save_object: список из (id, ord) текущих
        жел. организаций
        :param declaration_mo: текущее МО из заявления
        :param requested_mo: общее МО для новых желаемых организаций
        :return: сохраняет в self.result данные об изменениях, вида:
        [{"conc_unit": [4, 1]}, {"conc_unit": [24, 2]}, {"sys_unit": [4, 1]}]

        """

        set_conc = set(conc_object)
        set_sys = set(save_object)
        if set_conc ^ set_sys:
            diff = [{self.NEW_NAME: tuple(el)}
                    for el in conc_object]
            diff.extend([
                {self.SYS_NAME: tuple(el)} for el in save_object
            ])
            if (declaration_mo and requested_mo and
                    declaration_mo != requested_mo):
                diff.extend([
                    {self.MO_NAME: (declaration_mo.id, requested_mo.id)}
                ])
            self._result.extend(diff)

    def _get_diff_data(self, current_state, future_state):
        """
        Разврачивает изменения на 3 списка:
            1. добавление
            2. удаление
            3. изменение

        :param list current_state: это список состоящий из кортежей
            двух элементов: [(718, 1)]
        :param list future_state: это список состоящий из словарей
            такого вида: [{'conc_unit': [718, 2]}, ]

        :returns tuple: (values_to_add, values_to_remove, values_to_update)

        """

        values_to_add = []
        values_to_remove = list(current_state)
        values_to_update = []

        # Проверяет что добавилось, удалилось или изменилось
        for change in future_state:
            future_unit_id, future_position = change[self.NEW_NAME]

            if (future_unit_id, future_position) in current_state:
                # если данные не изменились, удалять не нужно
                values_to_remove.remove(
                    (future_unit_id, future_position)
                )
                continue

            for current_unit_id, current_position in current_state:
                unit_id_matches = current_unit_id == future_unit_id

                if unit_id_matches:
                    values_to_update.append(
                        (future_unit_id, future_position, current_position)
                    )
                    values_to_remove.remove(
                        (current_unit_id, current_position)
                    )
                    break
            else:
                values_to_add.append((future_unit_id, future_position, 0))

        # все словари должны содержать туплы из 3 значений
        values_to_remove = [(x[0], 0, x[1]) for x in values_to_remove]
        return values_to_add, values_to_remove, values_to_update

    def _extend_show_result(self, get_field, get_old, get_new, list_changes,
                            rows):
        for uni_id, new_ord, old_ord in list_changes:
            try:
                unit = Unit.objects.get(id=uni_id)
                rows.append({
                    'field': get_field(unit),
                    'old_value': get_old(unit, old_ord),
                    'new_value': get_new(unit, new_ord),
                })
            except Unit.DoesNotExist:
                pass
        return rows

    def _get_future_state(self, difference):
        return [x for x in difference if self.NEW_NAME in list(x.keys())]

    def _get_current_state(self, difference, changes):
        if changes.state == ChangeStatus.WAIT:
            # состояние модели на текущий момент
            get_data = rules.display_changes_map.get(self.name_model)
            data_now = get_data(changes)
            curent_state = list(data_now.all().values_list('unit_id', 'ord'))
        else:
            curent_state = [
                tuple(x[self.SYS_NAME]) for x in [
                    x for x in difference if self.SYS_NAME in list(x.keys())
                ]
            ]
        return curent_state

    def show_change(self, difference, changes):
        """
        Метод вернет информацию об изменении в человекопонятном виде
        - перед изменениями покажет разницу с текущим состоянием БД
        - после изменения с состонияем на обработку сервиса
        :return: список из { имени поля, формат. старого значения,
                 формат. нового значения }
        :rtype:(bool, list)

        """

        rows = []
        verbose_name = self.model._meta.verbose_name
        curent_state = self._get_current_state(difference, changes)
        future_state = self._get_future_state(difference)
        new_list, delete_list, update_list = self._get_diff_data(
            curent_state, future_state)

        # Для показа изменений МО в заявлении, если они есть
        new_mo_info = self._get_mo_if_need_change(difference)
        if new_mo_info:
            old_unit, new_unit = new_mo_info
            rows.append({
                'field': 'Заявление: МО',
                'old_value': old_unit.display(),
                'new_value': new_unit.display(),
            })

        self._extend_show_result(
            lambda x: verbose_name,
            lambda x, y: '-',
            lambda x, y: x.display(),
            new_list,
            rows
        )
        self._extend_show_result(
            lambda x: verbose_name,
            lambda x, y: x.display(),
            lambda x, y: '-',
            delete_list,
            rows
        )
        self._extend_show_result(
            lambda x: format_change(
                '%s - %s' % (verbose_name, x.display()), u'Приоритет'),
            lambda x, y: y,
            lambda x, y: y,
            update_list,
            rows
        )
        return rows

    def _get_mo_if_need_change(self, difference):
        """
        Возвращает список старого и нового МО для заявления,
        если они есть в данных на изменение, иначе вернет пустой список.
        :param difference: список id жел. организаций, МО заявления и МО
        жел. организаций
        :return: список старого и нового МО или []
        """

        new_mo_info = []
        # Парсим изменения, и достаем относящиеся только к смене МО в заявке
        new_mo_state = [tuple(x[self.MO_NAME]) for x in [
                x for x in difference if self.MO_NAME in list(x.keys())]]

        if new_mo_state:
            old_unit_id, new_unit_id = new_mo_state[0]
            old_unit = Unit.objects.get(pk=old_unit_id).get_mo()
            new_unit = Unit.objects.get(pk=new_unit_id).get_mo()

            new_mo_info = [old_unit, new_unit]

        return new_mo_info

    def _change_mo_if_need(self, difference, changes):
        """
        Если хотят изменить сад, находящийся в другом МО, отличном от текущего,
        то меняем МО в заявлении.
        :param difference: список id жел. организаций, их МО и МО заявления
        :param changes: запись из ChangeDeclaration
        """
        new_unit_info = self._get_mo_if_need_change(difference)

        if new_unit_info:
            new_unit = new_unit_info[1]
            declaration = rules.display_changes_map.declaration(changes)
            declaration.mo = new_unit
            declaration.save()

    def apply_change(self, difference, changes):
        """
        применяет изменения в системе
        не возвращаем дикт с изменениями, тк он работает
        только для моделей заявки и ребенка
        :return:

        """

        current_state = self._get_current_state(difference, changes)
        future_state = self._get_future_state(difference)
        new_list, delete_list, update_list = self._get_diff_data(
            current_state, future_state)

        # Меняем МО в заявке, если это необходимо
        self._change_mo_if_need(difference, changes)

        for unit_id, new_ord, old_ord in new_list:
            DeclarationUnit.objects.create(
                declaration=changes.declaration,
                unit_id=unit_id,
                ord=new_ord
            )
        for unit_id, new_ord, old_ord in update_list:
            du_qs = DeclarationUnit.objects.filter(
                declaration=changes.declaration,
                unit_id=unit_id,
            )
            if du_qs.count() == 1:
                du = du_qs[0]
                du.ord = new_ord
                du.save()

        for unit_id, _, _ in delete_list:
            du_qs = DeclarationUnit.objects.filter(
                declaration=changes.declaration,
                unit_id=unit_id,
            )
            if du_qs.count() == 1:
                du = du_qs[0]
                du.delete()
        return {}


class DeclarationPrivilegeChangeHelper(SetChangeHelper):

    @staticmethod
    def _is_benefit_changed(old, new):
        u"""Проверка изменения льготы."""
        return len(old) == len(new) == 1

    @staticmethod
    def _display_privilege_by_id(privilege_id):
        u"""Возврат отображения модели льготы."""
        try:
            privilege = Privilege.objects.get(id=privilege_id)
            result = privilege.display()
        except Privilege.DoesNotExist:
            result = None

        return result

    def check_diff(self, conc_object, save_object):
        """
        Проверяет пришли ли изменения по объекту из концетратра
        - если пришли сохраняем желаемое состояние
        и текущее состояния, для показа в дальнейшем истории изменений
        :param conc_object: список из id
        жел. организаций из запроса на изменение
        :param save_object: список из id текущих льгот
        :return: сохраняет в self.result данные об изменениях, вида:
            [{"conc_unit": [1]}, {"sys_unit": [1, 6]}]

        """

        set_conc = set(conc_object)
        set_sys = set(save_object)
        if set_conc ^ set_sys:
            self._result.extend(
                [{self.NEW_NAME: tuple(conc_object)},
                 {self.SYS_NAME: tuple(save_object)}])

    def _get_diff_data(self, curent_state, future_state):
        """
        Разврачивает изменения на 2 списка,  на удаление и на добавление
        :param curent_state:
        :param future_state:
        :return: new_list, delete_list

        """

        set_sys = set(curent_state)
        set_cur = set(future_state)
        new_list = list(set_cur - set_sys)
        delete_list = list(set_sys - set_cur)
        return new_list, delete_list

    def _extend_show_result(self, get_field, get_old, get_new, list_changes,
                            rows):
        for priv_id in list_changes:
            try:
                priv = Privilege.objects.get(id=priv_id)
                rows.append({
                    'field': get_field(priv),
                    'old_value': get_old(priv),
                    'new_value': get_new(priv),
                })
            except Privilege.DoesNotExist:
                pass
        return rows

    def _get_future_state(self, difference):
        """
        возвращает список льгот на добавление
        :param difference:
        :return:

        """

        future_state_l = [
            x[self.NEW_NAME] for x in [
                x for x in difference if self.NEW_NAME in list(x.keys())
            ]
        ]

        try:
            future_state = future_state_l[0]
        except IndexError:
            raise ValidationError
        return future_state

    def _get_current_state(self, difference, changes):
        """
        возвращает список id льгот заявки
        :param difference:
        :param changes:
        :return:

        """

        if changes.state == ChangeStatus.WAIT:
            # состояние модели на текущий момент
            get_data = rules.display_changes_map.get(self.name_model)
            data_now = get_data(changes)
            curent_state = list(data_now.all().values_list(
                'privilege_id', flat=True))
        else:
            curent_state = [
                x[self.SYS_NAME] for x in [
                    x for x in difference if self.SYS_NAME in list(x.keys())
                ]
            ]
            curent_state = curent_state[0]
        return curent_state

    def show_change(self, difference, changes):
        """
        Метод вернет информацию об изменении в человекопонятном виде
        - перед изменениями покажет разницу с текущим состоянием БД
        - после изменения с состоянием на обработку сервиса
        :return:
            список из { имени поля, формат. старого значения,
                        формат. нового значения })
        :rtype: (bool, list)

        """

        verbose_name = self.model._meta.verbose_name
        rows = []
        curent_state = self._get_current_state(difference, changes)
        future_state = self._get_future_state(difference)

        new_list, delete_list = self._get_diff_data(
            curent_state, future_state)

        if self._is_benefit_changed(delete_list, new_list):
            old_privilege_id = delete_list[0]
            self._extend_show_result(
                lambda x: verbose_name,
                lambda x: self._display_privilege_by_id(old_privilege_id),
                lambda x: x.display(),
                new_list,
                rows
            )
        else:
            self._extend_show_result(
                lambda x: verbose_name,
                lambda x: '-',
                lambda x: x.display(),
                new_list,
                rows
            )
            self._extend_show_result(
                lambda x: verbose_name,
                lambda x: x.display(),
                lambda x: '-',
                delete_list,
                rows
            )
        return rows

    def _create_new(self, new_list, changes):
        """
        создаем привязку льготы к заявлению
        :param new_list:
        :return:

        """

        for priv_id in new_list:
            DeclarationPrivilege.objects.create(
                declaration=changes.declaration,
                privilege_id=priv_id
            )

    def apply_change(self, difference, changes):
        """
        применяит изменение в системе
        не возвращаем дикт с изменениями, тк он работает
        только для моделей заявки и ребенка
        :return:

        """

        current_state = self._get_current_state(difference, changes)
        future_state = self._get_future_state(difference)
        new_list, delete_list = self._get_diff_data(
            current_state, future_state)

        if self._is_benefit_changed(delete_list, new_list):
            old_privilege_id, new_privilege_id = delete_list[0], new_list[0]
            declaration_privilege, _ = (
                DeclarationPrivilege.objects.get_or_create(
                    declaration=changes.declaration,
                    privilege_id=old_privilege_id)
            )
            declaration_privilege.privilege_id = new_privilege_id
            declaration_privilege.save()

            comment = json.loads(changes.data).get(
                "ConcentratorPrivilegeComment")
            if comment:
                comment_obj = PrivilegeComment.objects.get_or_create(
                    declaration_privilege_id=declaration_privilege.id)[0]
                comment_obj.concentrator_comment = comment
                comment_obj.save()
            # Обновили льготу в записи, обновляем ее в изменениях заявки,
            # чтобы не делать лишний запрос
            changes.declaration.best_privilege.id = new_privilege_id
        else:
            self._create_new(new_list, changes)
            for priv_id in delete_list:
                pr_qs = DeclarationPrivilege.objects.filter(
                    declaration=changes.declaration,
                    privilege_id=priv_id
                )
                if pr_qs.count() == 1:
                    priv = pr_qs[0]
                    priv.delete()
        return {}


class LipetskDeclarationPrivilegeChangeHelper(
    DeclarationPrivilegeChangeHelper
):
    """Измененим порядок получения изменений по льготам.

    Фиксируем изменения только для льгот пришедших с портала.

    """

    def _get_current_state(self, difference, changes):
        """
        возвращает список id льгот заявки
        :param difference:
        :param changes:
        :return:

        """

        if changes.state == ChangeStatus.WAIT:
            declarationprivilege_set = get_decl_priv(changes.declaration, True)
            curent_state = [x.privilege.id for x in declarationprivilege_set]
        else:
            curent_state = [
                x[self.SYS_NAME] for x in [
                    x for x in difference if self.SYS_NAME in list(x.keys())
                ]
            ]
            curent_state = curent_state[0]
        return curent_state

    def _create_new(self, new_list, changes):
        u"""
        создаем привязку льготы к заявлению и ее подтверждение, если нужно.
        :param new_list: список новых заявок
        :param changes: инстанс диффки

        """

        if len(new_list) > 1 and Changes.objects.filter(
                change_declaration=changes.id).exists():
            raise ApplicationLogicException(
                u"Изменения применить нельзя, так как не должно быть более"
                u" 1 льготы с портала. Отклоните изменения.")
        for priv_id in new_list:
            decl_pr, _create = DeclarationPrivilege.objects.get_or_create(
                declaration_id=changes.declaration_id,
                privilege_id=priv_id,
            )
            if _create:
                changes.declaration.refresh_best_privilege()
            # Если данные по обладателю льготы уже есть,
            # то мы только изменим в нем ссылку на льготу,
            # иначе создадим заново.
            priv_conf_attrs = get_priv_data(changes.declaration)
            if priv_conf_attrs:
                priv_conf_attrs.declaration_privilege = decl_pr
                priv_conf_attrs.confirmed = False
                priv_conf_attrs.save()
            else:
                data = dict(
                    declaration_privilege=decl_pr,
                    portal=True,
                )
                PrivilegeConfirmationAttributes.objects.create(**data)

    def _create_delegate_from_change(self, changes):
        try:
            changes_dict = json.loads(changes.data)
        except ValueError:
            return None

        try:
            confirmation_attributes = changes_dict[
                "PrivilegeConfirmationAttributes"]
        except KeyError:
            return None

        data = {}
        for attribute in confirmation_attributes:
            for field in attribute:
                if field.startswith("delegate."):
                    _, field_name = field.split(".")
                    field_changes_info = attribute[field]
                    _, value, _ = field_changes_info
                    data[field_name] = value

        try:
            delegate = Delegate.objects.create(**data)
        except ValueError:
            return None

        return delegate


class PrivConfAttrsChangeHelper(ChangeHelper):
    u"""
    Обработчик изменений доп.аттрибутов льгот
    PrivilegeConfirmationAttributes.

    """

    def apply_change(self, difference, changes):
        u"""
        Если пришли данные на изменения обладателя льготы,
        то в любом случае меняется ссылка на delegate. В случае смены на:
        - Родителя или Зак.представителя - ищем его по ФИО или данным ДУЛ,
        - Ребенка - затираем ссылку и ингорируем изменения по delegate.
        После применяем оставшиеся изменения.

        """

        priv_conf_attrs = get_priv_data(changes.declaration)
        privilege_owner_changes = self.get_changes_field(
            difference, 'privilege_owner')

        # если в БД нет подтверждения льготы, то ее либо не было,
        # либо удалилась до вызова apply_change.
        if not priv_conf_attrs:
            return {}

        if privilege_owner_changes is not self._NON_EXISTENT:
            _, new_owner, old_owner = privilege_owner_changes

            # Случай удаления льготы. Расширяющая модель удалиться каскадно.
            # В применении изменений отсуствует необходимость.
            if new_owner is None:
                return {}

            if new_owner != PrivilegeOwnerEnum.CHILDREN:
                # смена на родителя или Зак.представителя
                delegate = DelegatePrivilegeProxy.get_founded_or_new(
                    changes.declaration,
                    DelegatePrivilegeProxy.get_from_diff(difference))

                priv_conf_attrs.delegate_id = delegate.id
            else:
                # смена на ребенка. затираем ссылку на delegate
                priv_conf_attrs.delegate_id = None
                # исключаем из difference все изменения содержащие 'delegate.'
                difference = self.filter_difference(
                    difference, lambda k: 'delegate.' not in k)

            # перед применением изменений пересохраняем delegate
            priv_conf_attrs.save()

        updated_fields = super(PrivConfAttrsChangeHelper, self).apply_change(
            difference, changes)
        return updated_fields
