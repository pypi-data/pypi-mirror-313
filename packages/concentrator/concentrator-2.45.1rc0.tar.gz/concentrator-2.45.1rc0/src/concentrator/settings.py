from os.path import join
from os.path import normpath
import json

from django.conf import settings
from kinder import config_parser as config


DEFAULT_CONFIG = {
    ('webservice', 'SMEV_CONCENTRATOR_REG_CODE'): '',
    ('webservice', 'SMEV_CONCENTRATOR_WSDL_URL'): '',
    ('webservice', 'SMEV_CONCENTRATOR_WSDL_FILE'): '',
    ('webservice', 'TNS'): '',
    ('webservice', 'ADDXSITYPE'): False,
    ('webservice', 'GET_APPQ_FULL'): True,
    ('webservice', 'SET_NOTIFICATION_TYPE'): False,
    ('webservice', 'MAX_BINARY_DATA_SIZE'): 0
}

conf = config.ProjectConfig(
    filenames=[normpath(join(settings.CONFIG_PATH, 'concentrator.conf'))],
    defaults=DEFAULT_CONFIG
)
# Код региона
SMEV_CONCENTRATOR_REG_CODE = conf.get('webservice',
                                      'SMEV_CONCENTRATOR_REG_CODE')
# Адрес концентратора для отправки справочникоа
SMEV_CONCENTRATOR_WSDL_URL = conf.get('webservice',
                                      'SMEV_CONCENTRATOR_WSDL_URL')
# Адрес до файла с wsdl концентратора для формирования запроса на отправку,
# по умолчанию совпадает с SMEV_CONCENTRATOR_WSDL_URL
SMEV_CONCENTRATOR_WSDL_FILE = (conf.get('webservice',
                                        'SMEV_CONCENTRATOR_WSDL_FILE')
                              or SMEV_CONCENTRATOR_WSDL_URL)
TNS = conf.get('webservice', 'TNS')
# Настройка для подменый неймспеса у тэга AppData
ADDXSITYPE = conf.get_bool('webservice', 'ADDXSITYPE')
# Признак отдавать или нет детальную очередт в сервисе GetApplicationQueue
GET_APPQ_FULL = conf.get_bool('webservice', 'GET_APPQ_FULL')

LOAD_DATA_TIMEOUT = conf.get_int(
    'webservice', 'LOAD_DATA_TIMEOUT', 90)

SET_NOTIFICATION_TYPE = conf.get_bool('webservice', 'SET_NOTIFICATION_TYPE')

SEND_STATE_WITH_USER_COMMENTARY = conf.get_bool(
    'webservice', 'SEND_STATE_WITH_USER_COMMENTARY')

MAX_BINARY_DATA_SIZE = conf.get_int(
    'webservice', 'MAX_BINARY_DATA_SIZE', 0)

# Настройки периодической задачи по обработке запросов СМЭВ 3 из aio
SMEV3_FORM_DATA_TASK_EVERY_MINUTE = (
        conf.get('webservice', 'SMEV3_FORM_DATA_TASK_EVERY_MINUTE') or '*/5')
SMEV3_FORM_DATA_TASK_EVERY_HOUR = (
        conf.get('webservice', 'SMEV3_FORM_DATA_TASK_EVERY_HOUR') or '*')
SMEV3_FORM_DATA_MESSAGE_TYPE = (
        conf.get('webservice', 'SMEV3_FORM_DATA_MESSAGE_TYPE')
        or 'FormData')

EVENT_SERVICE_ENV = conf.get('webservice', 'EVENT_SERVICE_ENV') or 'DEV'
EVENT_SERVICE_MESSAGE_TYPE = (
    conf.get('webservice', 'EVENT_SERVICE_MESSAGE_TYPE') or 'eventService')
EVENT_SERVICE_RESPONSE_MINUTES = (
    conf.get('webservice', 'EVENT_SERVICE_RESPONSE_MINUTES') or '*/5')
EVENT_SERVICE_RESPONSE_HOURS = (
    conf.get('webservice', 'EVENT_SERVICE_RESPONSE_HOURS') or '*')

# Настройки списка статусов организаций для отправки справочника Организации
# через метод LoadData, по умолчанию (если не настроен) включены статусы
# 0, 1, 2, 3, 4, 5.
STATUS_UNIT_LIST = json.loads(
    '['+conf.get('webservice', 'STATUS_UNIT_LIST')+']') or [0, 1, 2, 3, 4, 5]

# Ограничение желаемых ДОО для сервиса очереди GetApplicationQueueRequest
QUEUE_DOO_LIMIT_COUNT = conf.get_int(
    'webservice', 'QUEUE_DOO_LIMIT_COUNT', allow_none=True)

DUL_CONFIRMATING = conf.get_bool('cancel_allowed', 'DUL_CONFIRMATING') or False
ZAGS_CHECKING = conf.get_bool('cancel_allowed', 'ZAGS_CHECKING') or False
MED_CONFIRMATING = conf.get_bool('cancel_allowed', 'MED_CONFIRMATING') or False
DIDNT_COME = conf.get_bool('cancel_allowed', 'DIDNT_COME') or False
WANT_CHANGE_DOU = conf.get_bool('cancel_allowed', 'WANT_CHANGE_DOU') or False
REFUSED = conf.get_bool('cancel_allowed', 'REFUSED') or False
TUTOR_CONFIRMATING = conf.get_bool(
    'cancel_allowed', 'TUTOR_CONFIRMATING') or False
ACCEPTED = conf.get_bool('cancel_allowed', 'DUL_CONFIRMATING') or False
PRIV_CONFIRMATING = conf.get_bool(
    'cancel_allowed', 'PRIV_CONFIRMATING') or False
DIRECTED = conf.get_bool('cancel_allowed', 'DIRECTED') or False
REGISTERED = conf.get_bool('cancel_allowed', 'REGISTERED') or False
ARCHIVE = conf.get_bool('cancel_allowed', 'ARCHIVE') or False
FMS_CHECKING = conf.get_bool('cancel_allowed', 'FMS_CHECKING') or False
PRIOR_DOU_SELECTING = conf.get_bool(
    'cancel_allowed', 'PRIOR_DOU_SELECTING') or False
NOT_ATTENDED = conf.get_bool('cancel_allowed', 'NOT_ATTENDED') or False
DURING_EXCHANGE = conf.get_bool('cancel_allowed', 'DURING_EXCHANGE') or False
OTHER_STATUS = conf.get_bool('cancel_allowed', 'OTHER_STATUS') or False

# Настройки периодической задачи по проверке смены статуса направлений
SMEV3_STATUS_CHANGE_TASK_EVERY_MINUTE = (
        conf.get('webservice', 'SMEV3_STATUS_CHANGE_TASK_EVERY_MINUTE'
                 ) or '*/5')
SMEV3_STATUS_CHANGE_TASK_EVERY_HOUR = (
        conf.get('webservice', 'SMEV3_STATUS_CHANGE_TASK_EVERY_HOUR') or '*')
SMEV3_CHECK_DECLARATION_STATUS_CHANGES_MINUTE = (
    conf.get_int(
        'webservice', 'SMEV3_CHECK_DECLARATION_STATUS_CHANGES_MINUTE', 0))
SMEV3_CHECK_DECLARATION_STATUS_CHANGES_HOUR = (
    conf.get_int(
        'webservice', 'SMEV3_CHECK_DECLARATION_STATUS_CHANGES_HOUR', 4))

# Отключить передачу справочников на ЕПГУ по СМЭВ 2 (по умолчанию True)
DISABLE_LOAD_DATA_SMEV2 = conf.get_bool(
    'webservice', 'DISABLE_LOAD_DATA_SMEV2', allow_none=True)
if DISABLE_LOAD_DATA_SMEV2 is None:
    DISABLE_LOAD_DATA_SMEV2 = True

# Отключить передачу статусов заявлений по концентратору СМЭВ 2
DISABLE_UPDATE_APPLICATION_STATE = conf.get_bool(
    'webservice', 'DISABLE_UPDATE_APPLICATION_STATE', default=True)
