from __future__ import annotations

from typing import TYPE_CHECKING

from m3.db import BaseEnumerate

from kinder.core.declaration_status.models import DSS


if TYPE_CHECKING:

    try:
        from typing import TypedDict
    except ImportError:
        from typing_extensions import TypedDict


    class DeclarationChanges(TypedDict):
        """Словарь данных изменения поля заявления."""

        field: str
        old_value: str
        new_value: str


MESSAGE_PLUGIN_SMEV3_REQUIRED = (
    'Для работы с данным функционалом необходимо подключить плагин')

# Разделить для идентификатора льготы и льготы в МО
DELIMITER_PRIV = '000'
# Муниципальные льготы приходят портала с типом 3
MUNICIPAL_TYPE = 3
# Поле комментария к привилегии, пришедшей с концентратора
PRIVILEGE_COMMENT = 'ConcentratorPrivilegeComment'


class ConcentratorDelegateDocType(BaseEnumerate):
    """
    Типы документов представителя в концентраторе
    """

    USSR_PASSPORT = 1
    ABROAD_USSR_PASSPORT = 2
    IDENTITY_CARD = 4
    CERTIFICATE_OF_RELEASE = 5
    MINMORFLOT_PASSPORT = 6
    MILITARY_ID = 7
    DIPLOMATIC_RF_PASSPORT = 9
    ABROAD_PASSPORT = 10
    CERTIFICATE_OF_REGISTRATION = 11
    RESIDENCE_PERMIT = 12
    REFUGEE_CERTIFICATE = 13
    TEMPORARY_IDENTITY_CARD = 14
    RF_PASSPORT = 21
    ABROAD_RF_PASSPORT = 22
    MARINE_PASSPORT = 26
    MILITARY_ID_RESERVE_OFFICER = 27

    values = {
        USSR_PASSPORT: u'Паспорт гражданина СССР',
        ABROAD_USSR_PASSPORT: u'Загранпаспорт гражданина СССР',
        IDENTITY_CARD: u'Удостоверение личности',
        CERTIFICATE_OF_RELEASE: u'Справка об освобождение',
        MINMORFLOT_PASSPORT: u'Паспорт Минморфлота',
        MILITARY_ID: u'Военный билет',
        DIPLOMATIC_RF_PASSPORT: u'Дипломатический паспорт гражданина РФ',
        ABROAD_PASSPORT: u'Иностранный паспорт',
        CERTIFICATE_OF_REGISTRATION: u'Свидетельство о регистрации '
                                     u'ходатайства иммигранта о '
                                     u'признании его беженцом',
        RESIDENCE_PERMIT: u'Вид на жительство',
        REFUGEE_CERTIFICATE: u'Удостоверение беженца',
        TEMPORARY_IDENTITY_CARD: u'Временное удостоверение '
                                 u'личности гражданина РФ',
        RF_PASSPORT: u'Паспорт гражданина РФ',
        ABROAD_RF_PASSPORT: u'Загранпаспорт гражданина РФ',
        MARINE_PASSPORT: u'Паспорт моряка',
        MILITARY_ID_RESERVE_OFFICER: u'Военный билет офицера запаса'
    }


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
