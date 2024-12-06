from kinder.core.children.models import DelegateTypeEnumerate
from kinder.core.children.models import GenderEnumerate
from kinder.core.dict.models import DULDelegateType
from kinder.core.dict.models import GroupTypeEnumerate
from kinder.core.dict.models import WorkType

from concentrator.smev3.service_types import kinder_conc


class Rule(type):

    def __new__(mcs, *args, **kwargs):
        rule_cls = super(Rule, mcs).__new__(mcs, *args, **kwargs)
        rule_cls.OUT = getattr(
            rule_cls, 'OUT',
            {val: key for key, val in list(rule_cls.IN.items())})
        return rule_cls


class DictRule(metaclass=Rule):

    IN = {}

    @classmethod
    def system_value(cls, concentrator_value):
        return cls.IN.get(concentrator_value)

    @classmethod
    def concentrator_value(cls, system_value):
        return cls.OUT.get(system_value)


class ChildGenderRule(DictRule):
    """Правило соответствия пола ребенка."""

    IN = {
        kinder_conc.GenderType.MALE: GenderEnumerate.MALE,
        kinder_conc.GenderType.FEMALE: GenderEnumerate.FEMALE,
    }


class DulDelegateTypeRule(DictRule):
    """Правило соответствия типа ДУЛ родителя."""

    IN = {
        '1': DULDelegateType.RF_PASSPORT,
    }


class WorktypeRule(DictRule):
    """Правило соответствия режима работы.

    Сопоставляется id записи из концентатора и код режима работы групп из нашей
    системы.
    """

    IN = {
        '1': WorkType.SHORT,
        '2': WorkType.FULL,
        '3': WorkType.ALLDAY,
    }


class GroupTypeRule(DictRule):
    """Правило соответствия Желаемая направленность группы"""

    IN = {
        '1': GroupTypeEnumerate.DEV,
        '2': GroupTypeEnumerate.COMP,
        '3': GroupTypeEnumerate.HEALTH,
        '4': GroupTypeEnumerate.CARE,
        '5': GroupTypeEnumerate.FAMILY,
    }


class DelegateTypeRule(DictRule):
    """Правило соответствия типа представителя."""

    IN = {
        '1': DelegateTypeEnumerate.MOTHER,
        '2': DelegateTypeEnumerate.FATHER,
        '3': DelegateTypeEnumerate.LEX,
    }
