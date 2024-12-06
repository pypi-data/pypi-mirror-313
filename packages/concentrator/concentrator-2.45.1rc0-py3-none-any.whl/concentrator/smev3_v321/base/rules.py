from kinder.core.dict.models import DULDelegateType
from kinder.core.dict.models import GroupTypeEnumerate
from kinder.core.dict.models import HNE
from kinder.core.dict.models import WorkType
from kinder.core.rules import BaseDictRule


class Smev3BaseDictRule(BaseDictRule):
    """Базовый класс, описывающий сопоставления системных значений и значений
    требуемых сервису СМЭВ 3.
    """

    # Содержат описание правил в виде словаря,
    # где ключом является список значений и требуется проверка на
    # наличие проверяемого значения в нем
    _IN_RULE_LIST = {}
    _OUT_RULE_LIST = {}

    @classmethod
    def get_system_list(cls, service_value, default_value=None):
        """Преобразует значение, полученное из сервиса, в системное.

        Проверяет наличие значения в списке ключа.
        """

        for key in cls._IN_RULE_LIST.keys():
            if service_value in key:
                return cls._IN_RULE_LIST[key]

        return default_value

    @classmethod
    def get_service_list(cls, system_value, default_value=None):
        """Преобразует значение, полученное из сервиса, в системное."""

        for key in cls._OUT_RULE_LIST.keys():
            if system_value in key:
                return cls._OUT_RULE_LIST[key]

        return default_value


class WorkTypeRule(Smev3BaseDictRule):
    """Правило соответствия Режима работы."""

    _OUT_RULE_LIST = {
        # Продленный день (13-14-часового пребывания), Сокращенный день
        # (8-10-часового пребывания) на ЕПГУ отправлять с кодом 1,
        # как Полный день (8-14 часов) на ЕПГУ
        (WorkType.EXTEND, WorkType.ABREV): ('1', 'Полный день (8-14 часов)'),
    }


class GroupTypeRule(Smev3BaseDictRule):
    """Правило соответствия Желаемая направленность группы."""

    # Комбинированный, Для детей раннего возраста на ЕПГУ,
    # Группа по присмотру и уходу, Семейные детские группы
    # отправлять с кодом 1, как Общеразвивающая на ЕПГУ
    _OUT_RULE_LIST = {
        (
            GroupTypeEnumerate.COMBI, GroupTypeEnumerate.YOUNG,
            GroupTypeEnumerate.CARE, GroupTypeEnumerate.FAMILY
        ): ('1', 'Общеразвивающая'),
    }


class HealthNeedRule(Smev3BaseDictRule):
    """Правило соответствия Специфика группы."""

    _OUT_RULE = {
        # Специфика (при этом направленность группы "компенсирующая")
        # с иными физическими ограничениями на ЕПГУ отправлять с кодом 10,
        # как Для детей с тяжелыми и множественными нарушениями развития
        # на ЕПГУ
        (HNE.RESTRICTION, GroupTypeEnumerate.COMP): (
            '10', 'Для детей с тяжелыми и множественными нарушениями развития'
        ),
        # Специфика (при этом направленность группы "компенсирующая")
        # с умственной отсталостью умеренной, тяжелой степени на ЕПГУ
        # отправлять с кодом 9, как Для детей с умственной отсталостью
        # (нарушением интеллекта) на ЕПГУ
        (HNE.BACKHARD, GroupTypeEnumerate.COMP): (
            '9', 'Для детей с умственной отсталостью (нарушением интеллекта)'),
        # Специфика (при этом направленность группы "компенсирующая")
        # дети с фонетико-фонематическими нарушениями на ЕПГУ отправлять
        # с кодом 5, как Для детей с тяжелыми нарушениями речи на ЕПГУ
        (HNE.PHONETICS, GroupTypeEnumerate.COMP): (
            '5', 'Для детей с тяжелыми нарушениями речи'),
        # Специфика (при этом направленность группы "оздоровительная") другие,
        # с необходимостью комплексных оздоровительных мероприятий на ЕПГУ
        # отправлять с кодом 2, как Для часто болеющих детей на ЕПГУ
        (HNE.OTHER, GroupTypeEnumerate.HEALTH): (
            '2', 'Для часто болеющих детей'),
        # Специфика (при этом направленность группы "комбинированная") дети
        # с фонетико-фонематическими нарушениями на ЕПГУ
        # отправлять с кодом 5, как "Для детей с тяжелыми нарушениями речи"
        (HNE.PHONETICS, GroupTypeEnumerate.COMBI): (
            '5', 'Для детей с тяжелыми нарушениями речи'),
        # Специфика (при этом направленность группы "комбинированная")
        # с иными физическими ограничениями на ЕПГУ
        # отправлять с кодом 10, как
        # "Для детей с тяжелыми и множественными нарушениями развития"
        (HNE.RESTRICTION, GroupTypeEnumerate.COMBI): (
            '10', 'Для детей с тяжелыми и множественными нарушениями развития'
        ),
        # Специфика (при этом направленность группы "комбинированная")
        # с умственной отсталостью умеренной, тяжелой степени на ЕПГУ
        # отправлять с кодом 9, как
        # "Для детей с умственной отсталостью (нарушением интеллекта)"
        (HNE.BACKHARD, GroupTypeEnumerate.COMBI): (
            '9', 'Для детей с умственной отсталостью (нарушением интеллекта)'
        ),
    }


class GroupTypeWithoutHealthNeedRule(Smev3BaseDictRule):
    """Правило соответствия Желаемая направленность группы."""

    _OUT_RULE = {
        # Если в поле "Специфика" в запрашиваемом заявлении указано значение,
        # у которого нет кода концентратора, и в поле "Желаемая направленность
        # группы при зачислении" указано "Оздоровительная", то передавать
        # фиксированное значение 2 - "часто болеющих детей"
        GroupTypeEnumerate.HEALTH: ('2', 'Для часто болеющих детей'),
    }


class DULDelegateTypeRule(Smev3BaseDictRule):
    """Правило соответствия Типы документов представителя."""

    _OUT_RULE_LIST = {
        # Типы документов представителя свидетельство о рождении,
        # другой документ удостоверяющий личность, загранпаспорт гражданина РФ,
        # военный билет, паспорт моряка, паспорт Минморфлота,
        # свидетельство о рождении, выданное уполномоченным
        # органом иностранного государства, справка об освобождении из места
        # лишения свободы, удостоверение личности офицера,
        # удостоверение личности военнослужащего РФ,
        # временное удостоверение, выданное взамен военного билета,
        # удостоверение личности лица без гражданства в РФ, удостоверение
        # личности отдельных категорий лиц, находящихся на территории РФ,
        # подавших заявление о признании гражданами РФ или о приеме
        # в гражданство РФ на ЕПГУ отправлять с кодом 3,
        # как Временное удостоверение личности гражданина РФ  на ЕПГУ
        (
            DULDelegateType.BIRTH_CERTIFICATE, DULDelegateType.OTHER,
            DULDelegateType.INTERNATIONAL_PASSPORT_RF,
            DULDelegateType.MILITARY_PASSPORT, DULDelegateType.SAILOR_PASS,
            DULDelegateType.MINMORFLOT_PASSPORT,
            DULDelegateType.ABROAD_BIRTH_CERTIFICATE,
            DULDelegateType.RELEASE_CERTIFICATE,
            DULDelegateType.OFFICER_IDENTITY_CARD,
            DULDelegateType.SOLDIER_IDENTITY_CARD_RF,
            DULDelegateType.TEMPORARY_CERTIFICATE_MILITARY_PASS,
            DULDelegateType.IDENTITY_CARD_STATELESS_PERSON_RF,
            DULDelegateType.IDENTITY_CARD_APPLICATION_RECOGNITION_CITIZENSHIP_RF
        ): ('3', 'Временное удостоверение личности гражданина РФ'),
        # Типы документов представителя Свидетельство о рассмотрении
        # ходатайства о признании беженцем на территории Российской Федерации,
        # удостоверение личности лица, ходатайствующего о признании беженцем
        # на территории РФ, свидетельство о предоставлении временного убежища
        # на территории Российской Федерации, удостоверение личности лица,
        # получившего временное убежище на территории РФ
        # на ЕПГУ отправлять с кодом 6, как Удостоверение беженца на ЕПГУ
        (
            DULDelegateType.CERTIFICATE_OF_REGISTRATION,
            DULDelegateType.IDENTITY_CARD_RECOGNITION_REFUGEE_RF,
            DULDelegateType.CERTIFICATE_TEMPORARY_ASYLUM_RF,
            DULDelegateType.IDENTITY_CARD_TEMPORARY_ASYLUM_RF
        ): ('6', 'Удостоверение беженца')
    }
