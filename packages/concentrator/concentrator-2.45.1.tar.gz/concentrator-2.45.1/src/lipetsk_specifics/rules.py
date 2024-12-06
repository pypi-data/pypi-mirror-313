import datetime

from dateutil.relativedelta import relativedelta

from kinder.core.children.models import DelegateTypeEnumerate
from kinder.core.children.models import DULDelegateType
from kinder.core.children.models import DULTypeEnumerate
from kinder.core.declaration_status.enum import DSS
from kinder.plugins.privilege_attributes.models import PrivilegeOwnerEnum

from concentrator.rules import DictRule

from .constants import ConcentratorChildrenDocType
from .constants import LipetskDelegateDocType


class DelegateTypeRule(DictRule):
    """Правило соотвествия Типа заявителя."""

    _person = u'представителя'
    # значение концетратора: системное значение
    IN_RULE = {
        1: DelegateTypeEnumerate.MOTHER,
        2: DelegateTypeEnumerate.FATHER,
        3: DelegateTypeEnumerate.LEX
    }
    OUT_RULE = {
        DelegateTypeEnumerate.MOTHER: 1,
        DelegateTypeEnumerate.FATHER: 2,
        DelegateTypeEnumerate.LEX: 3
    }


class PrivilegeTypeRule(DictRule):
    """
    Правило соотвествия Типы льготы
    """
    _person = u'Тип льготы'
    # значение концетратора: системное значение
    IN_RULE = {
        1: 1,
        2: 3,
        3: 2
    }
    OUT_RULE = {
        1: 1,
        2: 3,
        3: 2
    }


class WorkTypeRule(DictRule):
    """Правило соотвествия Режим работы групп"""
    _person = u'Время пребывания'
    # значение концетратора: системное значение
    IN_RULE = {
        1: 4,  # полный
        2: 2,  # сокращенный
        3: 1,  # продленный
        4: 3,  # кратковременный
        5: 5,  # круглосуточный
    }

    # FIXME: придумать реализацию для базоваго класса,
    #  чтобы не пришлось определять OUT_RULE у наследников
    OUT_RULE = DictRule.invert(IN_RULE)


class SexTypeRule(DictRule):
    """
    Правило соотвествия пола
    """
    _person = u'пола'
    # значение концетратора: системное значение
    IN_RULE = {
        1: 1,
        2: 2,
    }
    OUT_RULE = {
        1: 1,
        2: 2,
    }


class DelegateDocTypeRule(DictRule):
    """Правило соответствия типов документов
    представителя в ЭДС и концентраторе"""

    _person = u'документа представителя'

    IN_RULE = {
        LipetskDelegateDocType.RF_PASSPORT: DULDelegateType.RF_PASSPORT,
        LipetskDelegateDocType.OTHER: DULDelegateType.OTHER
    }
    DEFAULT_IN = DULDelegateType.OTHER

    OUT_RULE = DictRule.invert(IN_RULE)
    DEFAULT_OUT = LipetskDelegateDocType.OTHER


class ChildrenDocTypeRule(DictRule):
    """
    Правило соответствия типов документов
    ребенка в ЭДС и концентраторе
    """

    _person = u'документа ребенка'

    @classmethod
    def get_system(cls, spyne_doc_type):
        """
        Получаем тип документа в ЭДС по типу из концентратора
        """

        spyne_doc_type = ChildrenDocTypeRule._get_int_present(
            spyne_doc_type)

        if spyne_doc_type == ConcentratorChildrenDocType.BIRTH_CERTIFICATE:
            dul_type = DULTypeEnumerate.SVID
        else:
            dul_type = DULTypeEnumerate.OTHER

        return dul_type


AUTO_ARCHIVE = 'auto_archive'


class DeclarationStatusCodeRule(DictRule):
    """
    Правило соответствия кода статусов заявки
    """

    OUT_RULE = {
        DSS.ZAGS_CHECKING: 1,
        DSS.TUTOR_CONFIRMATING: 12,
        DSS.MED_CONFIRMATING: 4,
        DSS.DUL_CONFIRMATING: 2,
        DSS.ACCEPTED_FOR_CONSIDERING: 2,
        DSS.RECEIVED: 2,
        DSS.PRIV_CONFIRMATING: 4,
        DSS.WANT_CHANGE_DOU: 6,
        DSS.REGISTERED: 6,
        DSS.ACCEPTED: 7,
        DSS.DIRECTED: 7,
        DSS.REFUSED: 8,
        DSS.DIDNT_COME: 9,
        DSS.ARCHIVE: 10,
        AUTO_ARCHIVE: 11
    }

    @classmethod
    def get_system(cls, spyne_value):
        pass


class DeclarationStatusNameRule(DictRule):
    """
    Правило соответствия имени статусов заявки
    """

    OUT_RULE = {
        DSS.ZAGS_CHECKING: u'Передача заявления по '
                           u'месту предоставления услуги',
        DSS.TUTOR_CONFIRMATING: u'Ошибка',
        DSS.MED_CONFIRMATING: u'Ожидает рассмотрения',
        DSS.DUL_CONFIRMATING: u'Заявление передано по '
                              u'месту предоставления услуги',
        DSS.ACCEPTED_FOR_CONSIDERING: 'Заявление принято к рассмотрению',
        DSS.RECEIVED: 'Заявление поступило',
        DSS.PRIV_CONFIRMATING: u'Ожидает рассмотрения',
        DSS.WANT_CHANGE_DOU: u'Поставлен в очередь',
        DSS.REGISTERED: u'Поставлен в очередь',
        DSS.ACCEPTED: u'Принято решение о зачислении',
        DSS.DIRECTED: u'Принято решение о зачислении',
        DSS.REFUSED: u'Отказано в услуге',
        DSS.DIDNT_COME: u'Не явился',
        DSS.ARCHIVE: u'Архив',
        AUTO_ARCHIVE: u'Отозвано'
    }

    @classmethod
    def get_system(cls, spyne_value):
        pass


def get_age_group_type(date_of_birth):
    """
    Вычисление кода <AgeGroupType> по дате рождения ребенка
    """

    now = datetime.datetime.now().date()

    def _get_date(y=0, m=0):
        """
        Вернет дату Сегодня - y лет - m месяцев
        """

        return now - relativedelta(years=y, months=m)

    age_group_map = {
        (_get_date(m=6), now): 1,
        (_get_date(y=1), _get_date(m=6)): 2,
        (_get_date(y=1, m=6), _get_date(y=1)): 3,
        (_get_date(y=2), _get_date(y=1, m=6)): 4,
        (_get_date(y=2, m=6), _get_date(y=2)): 5,
        (_get_date(y=3), _get_date(y=2, m=6)): 6,
        (_get_date(y=3, m=6), _get_date(y=3)): 7,
        (_get_date(y=4), _get_date(y=3, m=6)): 8,
        (_get_date(y=4, m=6), _get_date(y=4)): 9,
        (_get_date(y=5), _get_date(y=4, m=6)): 10,
        (_get_date(y=5, m=6), _get_date(y=5)): 11,
        (_get_date(y=6), _get_date(y=5, m=6)): 12,
        (_get_date(y=6, m=6), _get_date(y=6)): 13,
        (_get_date(y=7), _get_date(y=6, m=6)): 14,
        (_get_date(y=7, m=6), _get_date(y=7)): 15
    }

    for age_range in age_group_map:
        down_border, up_border = age_range
        if down_border < date_of_birth < up_border:
            return str(age_group_map[age_range])

    # Если он старше 7.5 лет до учитываем в категории от 7 до 7.5 лет
    return '15'


class DeclarationStatusChangeRule:
    """
    Правило смены статуса заявки
    """

    STATUS_TRANSFER_COMMENT = u"""
        Авто-смена статуса в связи с поступившей заявкой
        на отказ от участия в очереди поступила с ЕПГУ.
        Необходимо уточнить актуальность запроса у законных
        представителей.
    """

    @classmethod
    def change(cls, record, new_status):

        record.change_status(
            new_status, why_change=cls.STATUS_TRANSFER_COMMENT,
            is_auto=True
        )


class WorkTypeRules(DictRule):
    """
    """
    _person = u'Время пребывания'
    # значение концетратора: системное значение
    IN_RULE = {
        1: 4,
        2: 1,
        3: 3,
        4: 2,
        5: 5
    }
    OUT_RULE = {
        4: 1,
        1: 2,
        3: 3,
        2: 4,
        5: 5,
    }


class DelegateWhoHaveBenefits(DictRule):
    """
    Соотвествие наших типов представителя и типов для портала
    """
    _person = u'владельца льготы'
    OUT_RULE = {
        DelegateTypeEnumerate.MOTHER: PrivilegeOwnerEnum.PARENT,
        DelegateTypeEnumerate.FATHER: PrivilegeOwnerEnum.PARENT,
        DelegateTypeEnumerate.LEX: PrivilegeOwnerEnum.DELEGATE
    }
