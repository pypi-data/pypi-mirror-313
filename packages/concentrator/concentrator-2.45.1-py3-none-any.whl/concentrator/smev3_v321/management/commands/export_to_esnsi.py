"""Формирование файлов для для загрузки в ЛК ЕСНСИ.

Параметры запуска:
--code_dict: код справочника из списка доступных для обновления
             справочника в ЕСНСИ;
--uid_dict: UUID справочника;
--bind_fields: сопоставление выгружаемых полей и их UUID;
--encoding: кодировка xml-файла (необязательный, по умолчанию - utf-8).

Примеры запуска:
Организации (детсады)
export_to_esnsi --code_dict Unit
--uid_dict 380b6d13-06a9-4cbc-9bf3-468b784871ab
--bind_fields "CODE" "91f0ebe7-de01-404f-926a-f0d6a4225283"
"TITLE" "6020c6a1-24a3-4be7-bfa1-4d543fb1ae0f"
"REGOKATO" "a500b525-36b2-447d-83a2-a742f6ca2776"
"ADDRESS" "d435c48b-3ff1-4baf-98ac-7398909e2049"
"FIAS" "a8de4140-ef18-4d41-9362-2fe7018007c3"
"PHONE" "ddb417cc-2e0f-11eb-adc1-0242ac120002"
"EMAIL" "ec9a5e86-2e0f-11eb-adc1-0242ac120002"
"SCHEDULE" "f5eebe64-2e0f-11eb-adc1-0242ac120002"
"OKTMO" "99f9624c-d191-4f28-80c7-ae1804f4c6bc"
"WEBSITE" "3230e452-8b8b-495b-b2ee-febb186f5659"

Максимальное количество детсадов, которое может выбрать заявитель
export_to_esnsi --code_dict MaxDoo
--uid_dict 380b6d13-06a9-4cbc-9bf3-468b784871ab
--bind_fields "CODE" "91f0ebe7-de01-404f-926a-f0d6a4225283"
"TITLE" "6020c6a1-24a3-4be7-bfa1-4d543fb1ae0f"
"REGOKATO" "a500b525-36b2-447d-83a2-a742f6ca2776"
"EDUORGMAX" "d435c48b-3ff1-4baf-98ac-7398909e2049"

Данная команда - адаптированная версия
https://jira.bars.group/browse/EDUSCHL-14452
"""
import codecs
import os
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any
from typing import List
from typing import NoReturn
from typing import Optional
from typing import Type
from typing import Union
from uuid import uuid4

from django.conf import settings
from django.core.management import BaseCommand
from django.db.models import QuerySet
from django.template.loader import get_template
from django.utils.functional import cached_property

from concentrator.smev3_v321.esnsi.classifiers import ClassifierBase
from concentrator.smev3_v321.esnsi.classifiers import FieldInfo
from concentrator.smev3_v321.esnsi.enums import DataTypesEnum as DT
from concentrator.smev3_v321.models import ESNSIClassifier


class Command(BaseCommand):
    """Формирует файлы для для загрузки в ЛК ЕСНСИ."""

    def __init__(self, stdout=None, stderr=None, no_color=False):
        """Инициализация."""
        self.help = 'Формирование файлов для для загрузки в ЛК ЕСНСИ'
        # каталог выгрузки относительно MEDIA:
        self._SAVE_FILES_PATH = 'UpdateNSI'
        # контекст для выгрузки XML:
        self.xml_context = defaultdict(str)
        super(Command, self).__init__(stdout, stderr, no_color)

    @property
    def template(self):
        """Шаблон XML для выгрузки.

        rtype: django.template.backends.django.Template
        """
        return get_template(
            Path(__file__).parent.parent.parent
            / 'templates' / 'xml' / 'export_to_nsi.xml')

    @cached_property
    def command_params(self):
        """Словарь параметров командной строки.

        :rtype: dict
        """
        return {
            'code_dict': {
                'type': str,
                'nargs': '?',
                'help': 'Код справочника',
            },
            'uid_dict': {
                'type': str,
                'nargs': '?',
                'help': 'Uid справочника',
            },
            'bind_fields': {
                'nargs': '+',
                'type': str,
                'help': 'Соответствие полей справочника и их uuid',
            },
            'encoding': {
                'type': str,
                'nargs': '?',
                'help': 'Кодировка файла',
            },
        }

    def add_arguments(self, parser):
        """Парсинг аргументов командной строки."""
        for arg_name, arg_dict in self.command_params.items():
            parser.add_argument(
                '--%s' % arg_name,
                nargs=arg_dict['nargs'],
                type=arg_dict['type'],
                help=arg_dict['help'],
            )

    def _get_required_param(self, param: str, params: dict) -> Any:
        """Получение значения обязательного параметра командной строки.

        :param param: Имя параметра
        :param params: Словарь параметров командной строки

        :return: Значение параметра командной строки
        """
        result = params.get(param)
        if not result:
            sys.stdout.write('Отсутствует обязательный параметр "%s"!\n' % (
                self.command_params[param]['help']
            ))

        return result

    def _get_classifier_class(self, nsi_classifier: ESNSIClassifier) -> \
            Optional[Type[ClassifierBase]]:
        """Возвращает класс API справочника по коду сервиса.

        :param nsi_classifier: запись справочника для передачи в ЕСНСИ ПГУ

        :return: Класс API справочника по коду сервиса.
        """

        for cls_cls in ESNSIClassifier().classifiers_classes:
            if cls_cls.get_service_code() == nsi_classifier.code:
                return cls_cls

        return None

    def _get_data_queryset(self) -> QuerySet:
        """Возвращает данные для выгрузки."""

        qs = self.classifier.data_queryset()
        qs = qs.filter(self.classifier.queryset_filter())
        return qs

    def _make_xml_context(self, nsi_classifier: ESNSIClassifier) -> None:
        """Формирование контекста выгрузки в XML.

        :param nsi_classifier: запись справочника для передачи в ЕС НСИ ПГУ
        """
        self.xml_context['code'] = self.code_dict
        self.xml_context['name'] = self.classifier.model._meta.verbose_name_plural
        self.xml_context['uid'] = self.uid_dict
        self.xml_context['public_id'] = nsi_classifier.uid
        self.xml_context['key_attribute_ref'] = self.bind_fields[0][1]
        self.xml_context['records'] = []
        self.xml_context['attributes'] = []

    def _get_classifier_fields_info(self, field_name: str) -> \
            Union[FieldInfo, NoReturn]:
        """Получение информации о поле для выгрузки по названию

        :param field_name: Название поля для выгрузки

        :return: Информация о поле (namedtuple FieldInfo)
        """

        field_info = self.classifier.fields_info.get(field_name)
        if field_info:
            return field_info
        else:
            sys.stdout.write(
                f'Указано некорректное поле для выгрузки - "{field_name}"')
            exit()

    def _add_record_to_xml_context(self, rec: Any) -> None:
        """Дополнение контекста выгрузки в XML данными записи.

        :param rec: запись для выгрузки в XML
        """
        record = defaultdict(str, uid=uuid4(), attributes=[])
        obj = self.classifier.get_obj(rec)
        obj_data = self.classifier.get_data(obj)
        # Данные не прошедшие проверку не записываются в файл
        if not self.classifier.is_data_valid(obj_data):
            return

        for field_name, field_uid in self.bind_fields:
            field_info = self._get_classifier_fields_info(field_name)
            attr_value = obj_data.get(field_name, '')

            record_attributes = defaultdict(
                str,
                uid=field_uid,
                type=field_info.type,
                value=attr_value,
            )
            record['attributes'].append(record_attributes)

        self.xml_context['records'].append(record)

    def _add_specification_to_xml_context(self) -> None:
        """Дополнение контекста выгрузки в XML описанием передаваемых полей."""
        for field_name, field_uid in self.bind_fields:
            fields_info = self._get_classifier_fields_info(field_name)
            specification_el = defaultdict(
                str,
                uid=field_uid,
                name=field_name,
                type=fields_info.type,
                required=str(fields_info.required).lower(),
            )
            if fields_info.type in (DT.STRING, DT.TEXT):
                specification_el['length'] = fields_info.length

            self.xml_context['attributes'].append(specification_el)

    def _get_result_filename(self) -> str:
        """Имя файла для выгрузки."""
        fullpath = os.path.abspath(
            os.path.join(settings.MEDIA_ROOT, self._SAVE_FILES_PATH)
        )
        # Если директории не существует, то создадим её:
        if not os.path.exists(fullpath):
            try:
                os.makedirs(fullpath)
            except OSError:
                sys.stdout.write(
                    'Ошибка создания каталога для сохранения файла'
                )
                return ''

        filename = '%s-%s.xml' % (
            self.code_dict, time.strftime('%Y%m%d-%H%M%S')
        )
        return os.path.abspath(os.path.join(fullpath, filename))

    def _prepare_bind_fields(
            self, bind_fields_param: list) -> Union[List[tuple], NoReturn]:
        """Обработка параметра bind_fields manage команды.

        :param bind_fields_param: Входной параметр bind_fields команды

        :return: Список кортежей для соответствия выгружаемых полей и их UUID
        """
        bind_fields_iter = iter(bind_fields_param)
        bind_fields = [
            (fld, uid) for fld, uid in zip(
                bind_fields_iter, bind_fields_iter
            )
        ]
        if bind_fields:
            return bind_fields
        else:
            sys.stdout.write('Неверно задан параметр "%s"!\n' % (
                self.command_params['bind_fields']['help']
            ))
            exit()

    def _prepare_nsi_classifier(
            self, code_dict: str) -> Union[ESNSIClassifier, NoReturn]:
        """Получение записи классификатора на основе кода справочника.

        :param code_dict: Код справочника

        :return: Запись справочника ЕСНСИ
        """

        nsi_classifier = ESNSIClassifier.objects.filter(
            code=code_dict
        ).first()
        if nsi_classifier:
            return nsi_classifier
        else:
            sys.stdout.write('Указан несуществующий %s!\n' % (
                self.command_params['code_dict']['help']
            ))
            exit()

    def _prepare_classifier_class(self, nsi_classifier: ESNSIClassifier) -> \
            Union[Type[ClassifierBase], NoReturn]:
        """Получение класса API справочника по коду сервиса

        :param nsi_classifier: Входной параметр bind_fields команды

        :return: Класс API справочника
        """

        classifier_class = self._get_classifier_class(nsi_classifier)
        if classifier_class:
            return classifier_class
        else:
            sys.stdout.write('Для параметра %s не определены данные!\n' % (
                self.command_params['code_dict']['help']
            ))
            exit()

    def handle(self, *args, **kwargs):
        """Выполнение."""
        # Получаем параметры:
        self.code_dict = self._get_required_param('code_dict', kwargs)
        self.uid_dict = self._get_required_param('uid_dict', kwargs)
        bind_fields = self._get_required_param('bind_fields', kwargs)
        encoding = kwargs.get('encoding') or 'utf-8'
        if not (self.code_dict and self.uid_dict and bind_fields):
            sys.stdout.write('Один из параметров не заполнен')
            exit()

        # Определяем соответствие полей справочника и uuid:
        self.bind_fields = self._prepare_bind_fields(bind_fields)
        # Находим запись справочника для передачи в ЕС НСИ ПГУ:
        nsi_classifier = self._prepare_nsi_classifier(self.code_dict)
        # Находим класс API:
        classifier_class = self._prepare_classifier_class(nsi_classifier)

        # Формируем имя файла для выгрузки:
        filename = self._get_result_filename()
        if not filename:
            exit()

        self.classifier = classifier_class()
        # Формируем xml:
        self._make_xml_context(nsi_classifier)
        for rec in self._get_data_queryset().iterator():
            self._add_record_to_xml_context(rec)

        self._add_specification_to_xml_context()
        # Сохраняем в файл:
        with codecs.open(filename, 'w', encoding=encoding) as f:
            f.write(self.template.render(self.xml_context))
        sys.stdout.write(f'Данные записаны в файл {filename}')
