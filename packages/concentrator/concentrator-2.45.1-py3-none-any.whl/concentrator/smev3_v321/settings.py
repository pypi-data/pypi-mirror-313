import os

from django.conf import settings

from kinder import config_parser as config
from kinder import logger

from .order.constants import DEFAULT_ORDER_REQUEST_MESSAGE_TYPE


DEFAULT_CONFIG = {
    ('webservice', 'ATTACHMENT_REQUEST_MESSAGE_TYPE'): 'AttachmentRequest',
    ('webservice', 'ATTACHMENT_REQUEST_MEDIA_HOST'): None,
}

conf = config.ProjectConfig(
    filenames=[
        os.path.normpath(
            os.path.join(settings.CONFIG_PATH, 'concentrator.conf'))
    ],
    defaults=DEFAULT_CONFIG
)

ATTACHMENT_REQUEST_MESSAGE_TYPE = (
    conf.get('webservice', 'ATTACHMENT_REQUEST_MESSAGE_TYPE'))
ATTACHMENT_REQUEST_MEDIA_HOST = (
    conf.get('webservice', 'ATTACHMENT_REQUEST_MEDIA_HOST'))

PLUGIN_DIR_NAME = 'concentrator'
PLUGIN_DIR = os.path.join(settings.PLUGINS_DIR, PLUGIN_DIR_NAME)
PLUGIN_URL = f'{settings.PLUGINS_URL}/{PLUGIN_DIR_NAME}'
if not os.path.exists(PLUGIN_DIR):
    try:
        os.makedirs(PLUGIN_DIR)
    except:
        logger.error("Can't create %s" % PLUGIN_DIR)

# Атрибут, код тестовой среды ЕПГУ для запроса OrderRequest
# (EPGU / UAT / EXUAT / SVCDEV / TCOD / DEV).
# В продуктивной среде возможно только значение «EPGU»
ORDER_REQUEST_SERVICE_ENV = conf.get(
    'webservice', 'ORDER_REQUEST_SERVICE_ENV') or 'DEV'

ORDER_REQUEST_MESSAGE_TYPE = (
    conf.get('webservice', 'ORDER_REQUEST_MESSAGE_TYPE')
    or DEFAULT_ORDER_REQUEST_MESSAGE_TYPE)

# Время в секундах, через которое будет пересылатся запрос или будет
# обрабатываться сообщение FormData. По умолчанию = 1 час.
GAR_TIMEOUT_RESEND_SECONDS = conf.get_int(
    'webservice', 'GAR_TIMEOUT_RESEND_SECONDS', default=1*60*60)

# Включена ли задача смены статусов ApplicationRequest на "Не отправлен"
RESEND_APPLICATION_REQUESTS_TASK_ENABLED = conf.get_bool(
    'webservice', 'RESEND_APPLICATION_REQUESTS_TASK_ENABLED')
# Время запуска задачи смены статусов ApplicationRequest на "Не отправлен"
RESEND_APPLICATION_REQUESTS_TASK_HOUR = conf.get_int_hour(
    'webservice', 'RESEND_APPLICATION_REQUESTS_TASK_HOUR', default=22)
RESEND_APPLICATION_REQUESTS_TASK_MINUTE = conf.get_int_minute(
    'webservice', 'RESEND_APPLICATION_REQUESTS_TASK_MINUTE', default=0)
# Количество месяцев, старше которого запросы не переотправляются
RESEND_APPLICATION_REQUESTS_YOUNGER_THAN_IN_MONTHS = conf.get_int(
    'webservice', 'RESEND_APPLICATION_REQUESTS_YOUNGER_THAN_IN_MONTHS',
    default=3, min_value=1,
)
