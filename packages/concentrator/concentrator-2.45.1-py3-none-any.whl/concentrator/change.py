from __future__ import annotations

from collections import defaultdict
from itertools import chain
from typing import TYPE_CHECKING
from typing import Any
import datetime
import json

from django.conf import settings as kinder_settings
from django.db import transaction
from django.utils import timezone
from m3 import ApplicationLogicException
from m3_gar_client.utils import get_address_object
from m3_gar_client.utils import get_address_object_name
from yadic.container import Injectable

from kinder.core.audit_log_kndg.helpers import get_field
from kinder.core.audit_log_kndg.helpers import get_model
from kinder.core.audit_log_kndg.models import AdditionalEncoder
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import DeclarationDoc
from kinder.core.declaration.models import DeclarationPrivilege
from kinder.core.declaration.models import DeclarationStatus
from kinder.core.declaration.models import DeclarationUnit
from kinder.core.declaration_status.models import DSS
from kinder.core.helpers import recursive_get_verbose_name
from kinder.core.helpers import recursive_getattr
from kinder.core.helpers import recursive_setattr
from kinder.core.privilege.models import Privilege
from kinder.core.unit.models import Unit

from concentrator import settings as concentrator_settings
from concentrator.changes import rules
from concentrator.changes.helpers import convert_value
from concentrator.changes.helpers import format_change
from concentrator.models import ChangeDeclaration
from concentrator.models import ChangeStatus
from concentrator.models import PrivilegeComment
from concentrator.rules import DeclarationStatusChangeRule
from concentrator.webservice.helpers import DocumentWorker

from .constants import PRIVILEGE_COMMENT
from .models import ChangeSource
from .models import DocExtraInfo
from .models import UpdateParams


if TYPE_CHECKING:
    from .constants import DeclarationChanges


TYPE_CHOICE = 'choices'


class ChangesMap:
    """Соответствие полей django-моделей и полей моделей сервиса
    с учетом их типа.
    """

    notification_type_mapping = (
        'notification_type', int, r'Applicant\NotificationType'
    )

    _map = {
        # TODO: удалить проверку тех полей, которых никто
        #  никогда не будет изменять на строне концетратора
        # Структура: {model: [(sys_name, type_value, conc_name), ], }
        'Declaration': [
            ('desired_date', datetime.date, r'EntryDate'),
            ('offer_other', bool, r'EduOrganizations\AllowOfferOther'),
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
        ],
        'Children': [
            ('firstname', str, r'DeclaredPerson\FirstName'),
            ('surname', str, r'DeclaredPerson\LastName'),
            ('patronymic', str, r'DeclaredPerson\MiddleName'),
            ('snils', str, r'DeclaredPerson\Snils'),
            ('address_full', str, r'DeclaredPerson\AddressResidence'),
            ('reg_address_full', str,
             r'DeclaredPerson\AddressRegistration'),
            ('dul_type', int, r'DeclaredPerson\BirthDocForeign'),
            ('dul_series', str, r'DeclaredPerson\BirthDocSeria'),
            ('dul_number', str, (r'DeclaredPerson\BirthDocNumber',
                                 r'DeclaredPerson\BirthDocForeignNumber')),
            ('dul_date', datetime.date,
             r'DeclaredPerson\BirthDocIssueDate'),
            ('gender', int, r'DeclaredPerson\Sex'),
            ('health_need', TYPE_CHOICE, r'AdaptationProgramType'),
            # Поиск Документа, подтверждающий специфику происходит
            # по направлению специфики (AdaptationProgramType)
            ('health_need_confirmation', TYPE_CHOICE, r'AdaptationProgramType'),
            ('health_issued_by', str, r'AdaptationProgramDocInfo'),
            ('zags_act_number', str, r'DeclaredPerson\BirthDocActNumber'),
            ('zags_act_place', str, r'DeclaredPerson\BirthDocIssuer'),
            ('zags_act_date', datetime.date, r'DateOfActNumber'),
            ('birthplace', str, r'DeclaredPerson\BirthPlace'),
        ],
        # Сейчас для применения изменений всегда используется
        # концентраторский ChangesMap, а для сервисных методов липецкий,
        # поэтому пришлось продублировать.
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
            ('delegate.dul_issued_by', str, r'WhoHaveBenefit\DocIssuerName'),
            ('delegate.dul_date', datetime.date,
             r'WhoHaveBenefit\DocIssueDate'),
        ]
    }

    IGNORED_MODEL_ATTRS = {
        'Delegate': ('esia_id',)
    }

    def __init__(self):
        if concentrator_settings.SET_NOTIFICATION_TYPE:
            if self.notification_type_mapping not in self._map['Delegate']:
                self._map['Delegate'].append(self.notification_type_mapping)

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
        """Возвращает список полей недоступных для редактирования в ЕПГУ
        Это все поля из списка self._map,
        и не указанные в справочнике доступных

        :rtype: list
        """
        result = []
        editable_list = UpdateParams.objects.all().values_list(
            'model_name', 'field_name')
        for model_name in self.model_name_list:
            for sys_name, type_value, conc_names in self.get(model_name):
                if not isinstance(conc_names, tuple):
                    conc_names = (conc_names,)

                if (model_name, sys_name) in editable_list:
                    continue
                result.extend(conc_names)

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
        return [
            (model_name, get_model(model_name)._meta.verbose_name)
            for model_name in self.model_name_list if get_model(model_name)
        ]

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


class ChangeHelper:
    """
    Класс выполняет роль ЧЯ
    Принимает изменения, хранит, выводит и применяет их
    Скрывает механизм хранения и обработки
    """

    NAME_MODEL: str | None = None

    # несуществующее значение для методов get_{new/old}_value_field(...)
    _NON_EXISTENT = object()

    def __init__(self, model, name_model, map_changes=None):
        self.model = model
        self.map_changes = map_changes or ChangesMap()
        # из map_changes и rules.display_changes_map
        self.name_model = name_model
        self._result = []
        self.model_field = dict([(f.name, f) for f in model._meta.fields])

    @classmethod
    def get_changes_field(cls, difference, field_name):
        u"""
        Возвращает данные измненеия поля  в diff-ке,
        либо _NON_EXISTENT если их нет/
        :return tuple|object: (verbose_name, new_val, old_val)

        """

        for obj in difference:
            result = obj.get(field_name)
            if result:
                return result
        return cls._NON_EXISTENT

    @classmethod
    def get_new_value_field(cls, difference, field_name):
        u"""Возвращает новое значение поля из диффки, либо константу"""
        result = cls.get_changes_field(difference, field_name)
        if result is not cls._NON_EXISTENT:
            _, new_val, _ = result
            return new_val
        return cls._NON_EXISTENT

    @classmethod
    def get_old_value_field(cls, difference, field_name):
        u"""Возвращает старое/текущее значение поля из диффки,
        либо константу

        """

        result = cls.get_changes_field(difference, field_name)
        if result is not cls._NON_EXISTENT:
            _, _, old_val = result
            return old_val
        return cls._NON_EXISTENT

    @classmethod
    def filter_difference(cls, difference, func):
        u"""
        Возврашает новую диффку отфильтрованную
        по функции с сингатурой func(model_field).
        Замечание: obj.keys()[0] обусловлено структурой difference

        """

        return [obj for obj in difference if func(list(obj.keys())[0])]

    def check_diff(self, conc_object, save_object):
        """Проверяет пришли ли изменения по объекту из концетратра
        Заполяняет параметр self._result, котрый содержит поля,
        по котрым пришли измененения
        :param conc_object: объект построенный по данным из концетратора
        :param save_object: объект из БД
        :return: сохраняет в self.result данные об изменениях, вида:

        """

        instanse_model = save_object or conc_object
        for field, type_value, _ in self.map_changes.get(self.name_model):
            conc_value = recursive_getattr(conc_object,
                                           field.replace('.', '__'))
            save_value = recursive_getattr(save_object,
                                           field.replace('.', '__'))
            compare_func = self.map_changes.get_function_compare(type_value)
            if not compare_func(conc_value, save_value):
                self._handling_change(field, type_value, conc_value,
                                      save_value, instanse_model)

    def _handling_change(self, field, type_value, conc_value, save_value,
                         instanse_model):
        """
        :param field: имя поля модели
        :param type_value: тип значения поля: int, str и тд
        :param conc_value: значение поля модели из концентратора
        :param save_value: текущее значение поля модели
        :param instanse_model: инстанс django модели ,
        для получения verbose_name поля
        :return:

        """

        if '.' in field:
            name_field = recursive_get_verbose_name(instanse_model,
                                                    field.replace('.', '__'))
        else:
            name_field = self.model_field[field].verbose_name

        if type_value == TYPE_CHOICE:
            self._result.append(
                {field: (name_field,
                         conc_value.id if conc_value else conc_value,
                         save_value.id if save_value else save_value)})
        else:
            self._result.append(
                {field: (name_field, conc_value, save_value)})

    def get_result(self):
        return self._result

    def is_related(self, data):
        """
        если есть model то это _set а не field
        :param data:
        :return:

        """

        return hasattr(data, 'model')

    def is_ignored_attr(self, name_field):
        """
        осуществляет проверку игнорировать данное поле или нет
        :param name_field: имя поля модели
        :return: возвращает True или False в зависимости от того, содержится ли
                name_field в IGNORED_MODEL_ATTRS[self.name_model]
        :rtype: bool
        """

        return name_field in (
            ChangesMap.IGNORED_MODEL_ATTRS.get(self.name_model, ()))

    @staticmethod
    def find_fias_name(value: str) -> str:
        """
        Метод, возвращающий наименование объекта, расшифрованное из
        кода ФИАС, если такое есть
        """
        fias_object = get_address_object(value)
        if fias_object:
            new_value = get_address_object_name(fias_object)
        else:
            new_value = '-'

        return new_value

    def show_change(self, difference, changes):
        """
        Метод вернет информацию об изменении в человекопонятном виде
        :return: список из { имени поля, формат. старого значения,
                формат. нового значения }
        :rtype: list
        """
        rows = []
        get_data = rules.display_changes_map.get(self.name_model)
        # состояние модели на текущий момент
        data_now = get_data(changes)

        for change_field in difference:
            name_field = list(change_field.keys())[0]
            verbosename_field, new_value, old_value = list(change_field.values())[0]

            # для улицы и города конвертируем ФИАС-код в читаемый вид
            if name_field in ('address_place', 'address_street'):
                new_value = self.find_fias_name(new_value)
                old_value = self.find_fias_name(old_value)

            # тк есть зависмость от именей полей в ChangesDetailRowsAction
            rows.append({
                'field': format_change(self.model._meta.verbose_name,
                                       verbosename_field),
                'old_value': convert_value(
                    rules.DISPLAY_TYPES_MAP, data_now,
                    name_field, old_value),
                'new_value': convert_value(
                    rules.DISPLAY_TYPES_MAP, data_now,
                    name_field, new_value)
            })

        return rows

    def apply_change(self, difference, changes):
        """
        - применяет изменения в системе
        - возаращает список изменений в окно
        :return:

        """

        updated_fields = {}
        list_reference = []

        get_data = rules.display_changes_map.get(self.name_model)
        # состояние модели на текущйи момент
        data_now = get_data(changes)
        # FIXME Чудодейственный костыль, призванный вызывать исключение только
        #  в момент непосредственного сохранения изменений с ЕПГУ, в которых
        #  присутствует комментарий для несуществующей привилегии. Голос разума
        #  подсказывает, что проверка должна производиться на уровне получения
        #  PrivilegeComment, заместо подсовывания пустого значения для
        #  ошибочного кейса.
        if self.name_model == 'PrivilegeComment' and data_now == '':
            raise ApplicationLogicException('Применить изменения невозможно.'
                                            ' Льгота удалена после поступления'
                                            ' изменений с ЕПГУ.')
        for change_field in difference:
            postfix = ''
            name_field = list(change_field.keys())[0]
            # Если поле в списке игнорируемых, то продолжаем
            if self.is_ignored_attr(name_field):
                continue
            verbosename_field, new_value, old_value = list(change_field.values())[0]
            new_value = convert_value(
                rules.FIELD_TYPES_MAP, data_now, name_field, new_value)
            # Если были изменения по fk, мы их должны запомнить,
            # тк их сохранять нужно отдельно
            update_obj = recursive_setattr(
                data_now, name_field.replace('.', '__'), new_value)
            if update_obj != data_now and update_obj not in list_reference:
                list_reference.append(update_obj)

            # для FK Нужно подправить имя поля
            field_info = self.map_changes.get_field_info(
                name_field, self.name_model)
            show_value = convert_value(rules.RESULT_TYPES_MAP, data_now,
                                       name_field, new_value)
            if field_info[1] == TYPE_CHOICE:
                postfix = '_id'
                show_value = show_value.id if show_value else ''

            updated_fields['{0}.{1}{2}'.format(
                self.name_model.lower(), name_field, postfix)] = show_value
        # Сохранем все измения по FK
        list(map(lambda x: x.save(), list_reference))
        # Затем сам объект
        if data_now:
            data_now.save()
        return updated_fields


class BaseStorageHelper:
    """Отвечает за управлением изменений по разным моделям в целом
    Работает со списком изменений пришедших от концентратора и в зависмости от
    модели применяет различные ChangeHelper.
    """

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
    def create_change(
            cls, declaration: Declaration, list_ch_help: list[ChangeHelper],
            raw_data: dict[str, Any] | None = None,
            source: int = ChangeSource.NEW_APPLICATION,
            case_number: str | int | None = None
    ) -> ChangeDeclaration | None:
        """Создает и возвращает запись изменений по заявлению.

        :param declaration: Заявление.
        :param list_ch_help : Список инстансов классов, каждый из
            котрых хранит изменени по 1 модели.
        :param raw_data: Доп. параметры для записи в изменения по заявлению.
        :param source: Источник изменений.
        :param case_number: Номер заявки.

        :return: Новая запись изменений, если была создана.

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
            return ChangeDeclaration.objects.create(
                declaration=declaration,
                data=json.dumps(result, cls=AdditionalEncoder),
                source=source,
                case_number=case_number)
        return None

    @classmethod
    def get_change(
            cls, changes: ChangeDeclaration
    ) -> list[DeclarationChanges]:
        """Возвращает данные об изменениях заявления.

        :param changes: Запись изменений заявления.

        :return: Данные об изменениях в виде списка словарей
            след. формата:
                [
                    {
                        'field': Наименование поля,
                        'old_value': Старое значение,
                        'new_value': Новое значение
                    },
                    ...
                ]

        """

        result = []
        for name_model, difference in json.loads(changes.data).items():
            class_model = get_model(name_model)
            if not class_model:
                continue
            change_helper = cls.get_change_helper(name_model)
            ch_help = change_helper(class_model, name_model)
            rows = ch_help.show_change(difference, changes)
            result.extend(rows)
        return result

    @classmethod
    def get_old_change(cls, changes):
        """
        Пытаемся оформить старые изменения
        """
        rows = []
        for name_model, difference in json.loads(changes.data).items():
            class_model = get_model(name_model)
            if not class_model:
                continue

            for change in difference:
                try:
                    change = change[0]
                    field, new_value, old_value = change
                except (IndexError, KeyError, ValueError):
                    rows.append({
                        'field': 'Неизвестно',
                        'old_value': str(change),
                        'new_value': '-'
                    })
                    continue

                rows.append({
                    'field':
                        format_change(class_model._meta.verbose_name, field),
                    'old_value': str(old_value),
                    'new_value': str(new_value)
                })

        return rows

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
            if not class_model:
                continue
            change_helper_cls = cls.get_change_helper(name_model)
            change_helper = change_helper_cls(class_model, name_model)
            updated_fields.update(
                change_helper.apply_change(difference, changes)
            )

        changes.user = getattr(request, 'user', None)
        changes.state = ChangeStatus.ACCEPT
        changes.commentary = comment
        # Выполняем валидацию модели перед сохранением
        changes.full_clean()
        changes.save()
        return updated_fields

    @classmethod
    def reject_changes(cls, changes, request, comment):
        """
        Отклоняет изменения
        :return:

        """

        for name_model, difference in json.loads(changes.data).items():
            change_helper = cls.get_change_helper(name_model)
            class_model = get_model(name_model)
            if not class_model:
                continue
            ch_help = change_helper(class_model, name_model)
            if (hasattr(ch_help, 'reject_changes') and
                    callable(ch_help.reject_changes)):
                ch_help.reject_changes(difference, changes)

        changes.user = getattr(request, 'user', None)
        changes.state = ChangeStatus.REJECT
        changes.commentary = comment
        # Выполняем валидацию модели перед сохранением
        changes.full_clean()
        changes.save()


class StorageHelper(BaseStorageHelper, metaclass=Injectable):
    """Предназначен для работы с заявлениями СМЭВ 2."""
    depends_on = ("source",)


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


class DeclarationDocsChangeHelper(ChangeHelper):
    """Отвечает за изменения по документам заявления
    При запросе UpdateApp документы сохраняются в DeclarationDoc с признаком ,
    что изменения не приняты, при принятие флаг меняется на True,
    при отказе удаляются из таблицы
    """
    NAME_MODEL = 'DocExtraInfo'
    NAME_LIST_ID = 'id_list'

    def __init__(self, model, name_model=NAME_MODEL):
        super(DeclarationDocsChangeHelper, self).__init__(model, name_model)

    def check_diff(self, document_references, declaration, binary_data,
                   request_code):
        """Сохраняем документы в таблице DeclarationDoc,
        и сведения о наличие изменений в инстансе класса в self._result

        :param document_references: ссылка на объект из запроса со
        сведениями о приложенных документах
        :param declaration: ссылка на заявление
        :param binary_data: содержимое тега BinaryData в запросе
        :param request_code: содержимое тега RequestCode в запросе
        :return:
        """

        list_of_docs = DocumentWorker(
            declaration, binary_data, request_code
        ).attach(approve=False)

        for ref in document_references:
            self._result.append({'code': (u'Код', ref.Code, None)})
            if ref.Name:
                self._result.append({'name': (u'Имя', ref.Name, None)})
            if ref.Description:
                self._result.append(
                    {'description': (u'Описание', ref.Description, None)})
        if list_of_docs:
            self._result.append(
                {self.NAME_LIST_ID: (
                    u'Список документов',
                    ','.join(str(doc.id) for doc in list_of_docs),
                    None)})

    @transaction.atomic
    def apply_change(self, difference, changes):
        """Применит изменение в системе
        проставит файлам признак что они приняты
        :return:

        """

        updated_fields = {}
        doc_extra_info = DocExtraInfo(declaration=changes.declaration)
        id_list = []

        for change_field in difference:
            postfix = ''
            name_field = list(change_field.keys())[0]
            verbosename_field, new_value, _ = list(change_field.values())[0]
            if name_field in ['code', 'name', 'description']:
                setattr(doc_extra_info, name_field, new_value)
            elif name_field == self.NAME_LIST_ID:
                id_list = new_value.split(',')
                continue
            updated_fields['{0}.{1}{2}'.format(
                self.name_model.lower(), name_field, postfix)] = new_value

        doc_extra_info.save()
        DeclarationDoc.objects.filter(id__in=id_list).update(approve=True)
        return updated_fields

    def show_change(self, difference, changes):
        """Метод вернет информацию об изменении в человекопонятном виде
        :return: список из { имени поля, формат. старого значения,
                формат. нового значения }
        :rtype: list
        """
        rows = []

        for change_field in difference:
            verbosename_field, new_value, old_value = list(
                change_field.values())[0]
            #  тк есть зависмость от именеи полей в ChangesDetailRowsAction
            rows.append({
                'field': format_change(self.model._meta.verbose_name,
                                       verbosename_field),
                'old_value': '-',
                'new_value': new_value
            })

        return rows

    def reject_changes(self, difference, changes):
        """При отказе, необходимо удалить приложенные файлы
        """
        id_list = []

        for change_field in difference:
            name_field = list(change_field.keys())[0]
            _, new_value, _ = list(change_field.values())[0]
            if name_field == self.NAME_LIST_ID:
                id_list = new_value.split(',')
                break
        DeclarationDoc.objects.filter(id__in=id_list).delete()


class SetChangeHelper(ChangeHelper):
    NEW_NAME = 'conc_unit'
    SYS_NAME = 'sys_unit'
    MO_NAME = 'decl_mo'


class DeclarationUnitChangeHelper(SetChangeHelper):
    """
    Изменения желаемых организаций храним в другом формате,
    поэтому переопределяем методы сохранения, показа и применения изменений
    """
    def check_diff(self, conc_object, save_object, declaration_mo=None,
                   requested_mo=None):
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

    def _get_diff_data(self, curent_state, future_state):
        """
        Разврачивает изменения на 3 списка, на изменение, на удаление
        на добавление
        :param curent_state:
        :param future_state:
        :return: new_list, delete_list, update_list

        """

        new_list = []
        delete_list = list(curent_state)
        update_list = []
        # Проверяет что изменилось, удалилось и добавилось
        for change in future_state:
            unit_id, new_ord = change[self.NEW_NAME]
            find = False
            for du_id, du_ord in curent_state:
                if du_id == unit_id and du_ord != new_ord:
                    update_list.append((unit_id, new_ord, du_ord))
                    delete_list.remove((du_id, du_ord))
                    find = True
                    break
                elif du_id == unit_id:
                    delete_list.remove((du_id, du_ord))
                    find = True
                    break
            if not find:
                new_list.append((unit_id, new_ord, 0))
        # все словари должны содержать туплы из 3 значений
        delete_list = [(x[0], 0, x[1]) for x in delete_list]
        return new_list, delete_list, update_list

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

        curent_state = self._get_current_state(difference, changes)
        future_state = self._get_future_state(difference)
        new_list, delete_list, update_list = self._get_diff_data(
            curent_state, future_state)

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
            return []
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
            return list(data_now.all().values_list(
                'privilege_id', flat=True))
        else:
            curent_state = [
                x[self.SYS_NAME] for x in [
                    x for x in difference if self.SYS_NAME in list(x.keys())
                ]
            ]
            return curent_state[0] if curent_state else []

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
            try:
                privilege = Privilege.objects.get(id=priv_id)
            except Privilege.DoesNotExist:
                raise ApplicationLogicException(
                    u'В изменениях добавлена льгота (код {}), которой уже нет '
                    u'в справочнике льгот. '
                    u'Необходимо, отклонить данные изменения.'.format(priv_id)
                )
            declaration_privilege = DeclarationPrivilege.objects.create(
                declaration=changes.declaration,
                privilege=privilege
            )
            # Получаем комментарий и проверяем на пустоту
            comment = json.loads(changes.data).get(
                "ConcentratorPrivilegeComment")
            if comment:
                PrivilegeComment.objects.create(
                    declaration_privilege_id=declaration_privilege.id,
                    concentrator_comment=comment)

    def apply_change(self, difference, changes):
        """
        применяит изменение в системе
        не возвращаем дикт с изменениями, тк он работает
        только для моделей заявки и ребенка
        :return:

        """

        curent_state = self._get_current_state(difference, changes)
        future_state = self._get_future_state(difference)
        new_list, delete_list = self._get_diff_data(
            curent_state, future_state)

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


class DelegateChangeHelper(ChangeHelper):
    """
    Класс принятия изменений для заявителя.

    В зависимости от опции SET_NOTIFICATION_TYPE в concentrator.conf
    возможен вариант при котором изменения сначала пришли с включенной опцией,
    а затем опцию отключили.
    Такие изменения не должны применяться/отображаться.

    """

    @classmethod
    def _filter_difference(cls, difference):
        if not concentrator_settings.SET_NOTIFICATION_TYPE:
            difference = cls.filter_difference(
                difference,
                lambda d: d != 'notification_type',
            )

        return difference

    def apply_change(self, difference, changes):
        return super(DelegateChangeHelper, self).apply_change(
            self._filter_difference(difference), changes
        )

    def show_change(self, difference, changes):
        return super(DelegateChangeHelper, self).show_change(
            self._filter_difference(difference), changes
        )


class ChildrenChangeHelper(ChangeHelper):
    """
    Класс принятия изменений для ребенка.

    При обновлении адреса нужно очистить все его данные и оставить только
    новое текстовое представление.
    Затем периодическая задача разбора `AddressParserTask` разберет его в ФИАС.
    """

    ADDRESS_PREFIX_MAP = {
        'address_full': '',
        'reg_address_full': 'reg_',
    }

    ADDRESS_FIELDS = (
        'address_place',
        'address_street',
        'address_house',
        'address_corps',
        'address_house_guid',
        'address_flat',
    )

    def _clear_address(self, child, addr_prefix):
        for field_name in self.ADDRESS_FIELDS:
            setattr(child, addr_prefix + field_name, None)

        child.save()

    def apply_change(self, difference, changes):
        get_object = rules.display_changes_map.get(self.name_model)
        child = get_object(changes)

        for diff_key in chain(*map(dict.keys, difference)):
            addr_prefix = self.ADDRESS_PREFIX_MAP.get(diff_key)
            if addr_prefix is not None:
                self._clear_address(child, addr_prefix)

        return super().apply_change(difference, changes)
