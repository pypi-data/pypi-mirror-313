from m3.db import BaseEnumerate

from kinder.core.declaration_status.models import DSS


class LipetskDelegateDocType(BaseEnumerate):
    """Типы документов представителя в Липецкий ЕПГУ"""

    RF_PASSPORT = 1
    OTHER = 2

    values = {
        RF_PASSPORT: u'Паспорт гражданина РФ',
        OTHER: u'Иное'
    }


# TODO: актуализировать все возможные значения
#  на Липецком ЕПГУ и заменить слова концентратор на Lipetsk
class ConcentratorChildrenDocType(BaseEnumerate):
    """
    Типы документов ребенка в концентраторе
    """

    BIRTH_CERTIFICATE = 3
    ABROAD_BIRTH_CERTIFICATE = 23

    values = {
        BIRTH_CERTIFICATE: u'Свидетельство о рождении',
        ABROAD_BIRTH_CERTIFICATE: u'Свидетельство о рождении '
                                  u'выданное уполномоченным '
                                  u'органом иностранного государства'
    }


class ResetDeclarationResponse:

    SUCCESS = u'Успех'
    ALREADY_ENROLLED = u'Ребенок уже зачислен'
    ALREADY_DIRECTED = u'Ребенок уже направлен в ДОО'
    SERVICE_IS_NOT_AVAILABLE = u'Сервис недоступен'

    RESET_AVAILABLE_STATUSES = [
        DSS.PRIV_CONFIRMATING,
        DSS.REGISTERED,
        DSS.WANT_CHANGE_DOU
    ]

    RESPONSES = {
        DSS.ACCEPTED: ALREADY_ENROLLED,
        DSS.ARCHIVE: SUCCESS,
        DSS.DIDNT_COME: SUCCESS,
        DSS.DIRECTED: ALREADY_DIRECTED,
        DSS.DUL_CONFIRMATING: SUCCESS,
        DSS.MED_CONFIRMATING: SUCCESS,
        DSS.PRIV_CONFIRMATING: SUCCESS,
        DSS.REFUSED: SUCCESS,
        DSS.REGISTERED: SUCCESS,
        DSS.TUTOR_CONFIRMATING: SUCCESS,
        DSS.WANT_CHANGE_DOU: SUCCESS,
        DSS.ZAGS_CHECKING: SERVICE_IS_NOT_AVAILABLE,
        DSS.ACCEPTED_FOR_CONSIDERING: SUCCESS,
        DSS.RECEIVED: SUCCESS,
    }


# Последовательность полей на форме соответствует последовательности в кортеже
# ((<fieldset>, (<fieldset_description>, (<field>, ...))), ...)
# ((<field>, <field_description>), ...)
ATTRIBUTES_FIELDS_MAP = (
    ('birthplace', (u"Место рождения", (
        'country',
        'region',
        'city'
    ))),
    ('personal_number', u"Личный номер"),
    ('force_kind', u"Принадлежность к виду или роду войск"),
    ('military_unit', u"Воинская часть (Подразделение)"),
    ('dismissal_date', u"Дата увольнения"),
    ('rank', u"Звание")
)


# Шаблон сообщения о постановки детей в очередь
CHILDREN_APPLY_IN_QUEUE_TMP = (
    u"Ваш ребенок поставлен на учет. Регистрационный номер ({client_id})")


class DepartmentAttribute(BaseEnumerate):
    @classmethod
    def generate(cls):
        # Формируем Enum динамически
        for field, description in ATTRIBUTES_FIELDS_MAP:
            if isinstance(description, tuple):
                # Если fieldset
                description, _ = description

            setattr(cls, field.upper(), field)
            cls.values.update({field: description})


DepartmentAttribute.generate()


NOTIFICATION_MODE = {
    'WANT_CHANGE_DOU': 1,
    'IN_QUEUE': 2,
    'REJECT': 3
}


class ReturnReasonEnum(BaseEnumerate):
    SHORT_STAY_GROUP = 0
    NOT_STATED_DOU = 1
    CHANGE_DATE = 2
    values = {
        SHORT_STAY_GROUP: u'Предоставлением ранее места в'
                          u' группе кратковременного пребывания детей',
        NOT_STATED_DOU: u'Предоставлением ранее места в незаявленной ОО',
        CHANGE_DATE: u'Изменения срока  предоставления места в ОО'
    }
