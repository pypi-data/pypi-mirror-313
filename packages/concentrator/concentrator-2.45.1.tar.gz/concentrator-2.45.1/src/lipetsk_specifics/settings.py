# coding:utf-8

from os.path import join
from os.path import normpath

from django.conf import settings
from kinder import config_parser as config


DEFAULT_CONFIG = {
    ('webservice', 'TNS'): '',
}

conf = config.ProjectConfig(
    filenames=[
        normpath(join(settings._CONFIG_PATH, 'lipetsk_specifics.conf'))
    ],
    defaults=DEFAULT_CONFIG
)

TNS = conf.get('webservice', 'TNS')
