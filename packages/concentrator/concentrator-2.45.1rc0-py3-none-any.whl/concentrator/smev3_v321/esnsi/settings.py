import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from kinder import logger
from kinder.settings import conf


def get_param(section, name, default):
    result = str(conf.get(section, name))
    return result or default


# Тип сообщения для запроса
UPDATE_CLASSIFIER_REQUEST_MSG_TYPE = get_param(
    'esnsi_smev3', 'UPDATE_CLASSIFIER_REQUEST_MSG_TYPE', 'UpdateNSI')

# Периодичность получения ответов из АИО
UPDATE_CLASSIFIER_RESPONSE_HOURS = get_param(
    'esnsi_smev3', 'UPDATE_CLASSIFIER_RESPONSE_HOURS', '*')
UPDATE_CLASSIFIER_RESPONSE_MINUTES = get_param(
    'esnsi_smev3', 'UPDATE_CLASSIFIER_RESPONSE_MINUTES', '*/5')

# Данные для авторизации
UPDATE_CLASSIFIER_REQUEST_AUTH = get_param(
    'esnsi_smev3', 'UPDATE_CLASSIFIER_REQUEST_AUTH', None)


if UPDATE_CLASSIFIER_REQUEST_AUTH is None:
    raise ImproperlyConfigured(
        'Укажите данные для авторизации запросов к ЕСНСИ')

UPDATE_CLASSIFIER_MEDIA_HOST = get_param(
    'esnsi_smev3', 'UPDATE_CLASSIFIER_MEDIA_HOST', None)

# Код ЭДС при регистрации в ЕПГУ
UPDATE_CLASSIFIER_REGOKATO = get_param(
    'esnsi_smev3', 'UPDATE_CLASSIFIER_REGOKATO', '-')

PLUGIN_DIR = os.path.join(settings.DOWNLOADS_DIR, 'esnsi_smev3')
PLUGIN_URL = f'{settings.DOWNLOADS_URL}/esnsi_smev3'
if not os.path.exists(PLUGIN_DIR):
    try:
        os.makedirs(PLUGIN_DIR)
    except:
        logger.error("Can't create %s" % PLUGIN_DIR)
