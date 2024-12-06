"""
Менедж-команда для обработки запросов с заявлениями, для которых упала
ошибка 404, за определенный период.

Принцип работы: ищет неудачные запросы с ошибкой 404 в логах СМЭВ за
указанный период. В данных записях находится orderId, по нему производится
поиск исходного запроса АИО, проверяется наличие заявления по orderId.
Проверяет дату из запроса (из тега FilingDate) и "Дата подачи заявки"
заявления. Если дата в теге меньше даты в заявке, то данную заявку
переводим в архив.
Данные выводятся в файл. Если менедж-команда запущена в тестовом режиме, 
на этом всё заканчивается. Иначе запросы АИО помечаются неотправленными и 
запускается задача celery для их повторной обработки. Далее информация о 
работе менедж-команды выводится в файл.

Запуск менедж-команды:
- Проверить, что в plugins.conf подключен плагин "concentrator.smev3_v321"
- Проверить, что версия concentrator больше 2.13.2
- Запустить воркер celery (нужно будет для обработки заявлений).
При этом celery beat желательно не запускать.
- Запустить менедж-команду

Пример запуска:
    process_404_declarations 01.08.2021 20.08.2021 --dry

Аргументы менедж-команды:
    дата начала периода в формате дд.мм.гггг;
    дата конца периода в формате дд.мм.гггг;
    --set_to_archive - Переносить ли заявку в архив, при выполнении условия
    --dry - параметр для тестирования (выводит информацию об ошибочных запросах
        без попытки их обработать).

В результате работы менедж-команды выводится 2 файла 
(при --dry только первый из них):
 - информация о найденных запросах:
    - id записи логов СМЭВ с ошибкой 404.
    - Дата данной записи в логах СМЭВ
    - orderId данной записи из логов СМЭВ
    - message_id запроса АИО, который найден по указанному orderId и который
        будет переотправлен
    - Комментарий о наличии заявления или о том, что запрос будет переотправлен.

 - информация о результатах работы менедж-команды:
    - orderId
    - ФИО ребёнка (если будет создано заявление)
    - Дата создания заявления
    - orgCode из ответа на запрос

Информация о названиях файлов будет указана в консоли. Файлы должны появиться
в текущей директории.
"""

from __future__ import annotations

import datetime
import json
import re
import time
import urllib

from aio_client import configs as aio_client_settings
from aio_client.provider.models import GetProviderRequest
from aio_client.provider.models import PostProviderRequest
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.db.transaction import atomic
from django.utils import timezone
from educommon.ws_log.models import SmevLog
from xlsxwriter import Workbook

from kinder.core.declaration.models import Declaration
from kinder.core.declaration_status.enum import DSS
from kinder.core.declaration_status.models import DeclarationStatus
from kinder.core.helpers import prep_date
from kinder.settings import DATE_FORMAT

from concentrator.smev3_v321.base.tasks import FormDataMessageProcessingTask


# Регулярные выражения для поиска параметров
ORDER_ID_REG_EXP = re.compile('<orderId>(\d+)</orderId>')
ORG_CODE_REG_EXP = re.compile(
    '<(?:[a-z0-9]+:)?orgCode>(.*)</(?:[a-z0-9]+:)?orgCode>')

FILLING_DATE_REG_EXP = re.compile(
    r'<(?:[a-z0-9]+:)?FilingDate>(.*)<\/(?:[a-z0-9]+:)?FilingDate>')

# Информация для заголовка файла с информацией о неудачных запросах
REQUESTS_INFO_HEADER = [
    ('id записи логов СМЭВ с ошибкой 404', 50),
    ('Дата в логах СМЭВ', 50),
    ('orderId из логов СМЭВ', 50),
    ('message_id запроса АИО', 50),
    ('Комментарий', 50),
]

# Информация для заголовка файла с информацией о результате работы 
# менедж-команды
RESULTS_INFO_HEADER = [
    ('orderId', 50),
    ('ФИО ребенка', 50),
    ('Дата рождения', 50),
    ('Серия и номер документа', 50),
    ('Идентификатор заявки (уже созданной ранее в системе)', 50),
    ('Дата подачи заявки (уже созданной ранее в системе)', 50),
    ('Дата подачи через Концентратор (из запроса)', 50),
    ('orgCode ответа', 50),
    ('message_id запроса АИО', 50),
    ('Удаленные вложения (если такие были и их не удалось обработать)', 50),
]
# Сообщения об ошибках
ORDER_ID_NOT_FOUND = 'Не найден orderId для лога СМЭВ с id={}'
AIO_REQUEST_NOT_FOUND = (
    'Не найден запрос АИО для лога СМЭВ с id={} (orderId={})')
DECLARATION_FOR_ORDER_ID_EXISTS = (
    'Заявление для orderId={} существует (заявления - {})')
DECLARATION_NOT_FOUND = 'Заявление не найдено'


class WorkBookWriter:
    """Класс-помощник для записи данных в excel файл для простых скриптов."""

    def __init__(self, file_name, header_info, header_style=None):
        """
        :param file_name: Название выходного файла
        :type file_name: str
        """
        self.file_name = file_name
        # Список кортежей типа (название, ширина) для формирования заголовка
        self.header_info = header_info
        # Словарь с параметрами стиля заголовка
        self._header_style = (
            header_style if header_style is not None else {'bold': True})

    def write_header(self):
        """Запись заголовка."""
        style = self.workbook.add_format(self._header_style)
        # Запись заголовка в файл
        for col, (header, width) in enumerate(self.header_info):
            self.sheet.set_column(col, col, width)
            self.sheet.write(0, col, header, style)

    def __enter__(self):
        self.workbook = Workbook(self.file_name)
        self.sheet = self.workbook.add_worksheet()
        self.write_header()
        self.row_number = 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.workbook.close()

    def write_row_data(self, row_data):
        """Запись строки данных в excel файл

        :param row_data: Кортеж с данными строки для записи в файл
        :type row_data: tuple
        """
        for col_number, data in enumerate(row_data):
            self.sheet.write(self.row_number, col_number, data)
        self.row_number += 1


def get_error_smev_log_query(start_date, end_date):
    """Получение запроса логов СМЭВ с ошибкой 404 за указанные даты

    :param start_date: Начало периода
    :param end_date: Конец периода

    :return: Запроса логов СМЭВ с ошибкой 404 за указанные даты
    """
    start_datetime = datetime.datetime.combine(start_date, datetime.time.min)
    end_datetime = datetime.datetime.combine(end_date, datetime.time.max)

    service = FormDataMessageProcessingTask.processing_service

    query = SmevLog.objects.filter(
        method_name=service.message_type,
        method_verbose_name=service.get_method_verbose_name(),
        time__gte=start_datetime,
        time__lte=end_datetime,
        result__isnull=False,
        request__contains='<ApplicationRequest>',
        result__contains='HTTP Error 404: Not Found',
    )
    if not query.exists():
        print('Не найдено ни одной подходящей записи в логах запросов СМЭВ')
        exit()

    return query


def get_provider_request(order_id: str) -> GetProviderRequest:
    """Получение входящего запроса к РИС с указанным orderId."""
    return GetProviderRequest.objects.filter(
        Q(body__contains='<ApplicationRequest>') &
        Q(body__contains=f'<orderId>{order_id}</orderId>'),
        state=GetProviderRequest.SENT,
        message_type='FormData',
    ).last()


def print_warning_messages(error_messages):
    """Вывод сообщений об ошибках, если они есть."""
    if error_messages:
        print('\nПредупреждения (не критично):')
        for message in error_messages:
            print(message)
        print()


def get_declaration_by_order_id(order_id: str):
    """Получение заявления по orderId."""
    return (
        Declaration.objects.select_related('status').filter(
            client_id=order_id).first())


def write_requests_info_to_file(requests_data):
    """Вывод в эксель файл информации о неудавшихся запросах

    :param requests_data: Информация о неудавшихся запросах
    """
    file_name = 'requests_info.xlsx'
    with WorkBookWriter(file_name, REQUESTS_INFO_HEADER) as writer:
        # Сортировка данных по наличию заявления и id логов СМЭВ
        sorted_data = sorted(
            requests_data, key=lambda x: (int(bool(x[3])), x[0].id))

        for smev_log, order_id, aio_request, declaration in sorted_data:
            comment = (
                f'Заявление уже создано ({str(declaration)})' if declaration
                else 'Запрос будет переотправлен'
            )

            writer.write_row_data(
                (smev_log.id, str(smev_log.time), order_id,
                 aio_request.message_id, comment)
            )
    print(f'Данные о неуспешных запросах выгружены в файл "{file_name}"')


def process_provider_requests(
        provider_requests: list[GetProviderRequest]
) -> None:
    """Обрабатываем ранее необработанные запросы

    :param provider_requests: Запросы с ошибкой
    """
    # Помечаем запросы неотправленными
    for request in provider_requests:
        request.state = request.NOT_SENT
        request.save()

    # Запускаем задачу для обработки запросов
    celery_result = FormDataMessageProcessingTask().apply_async(
        kwargs={'compare_with_filing': True})

    print('Задача для обработки ошибочных запросов отправлена в celery. '
          'Проверьте, что celery запущен')
    # Почему-то не работает celery_result.get/wait, поэтому так
    while not celery_result.ready():
        time.sleep(1)
    print('Обработка запросов завершена')


def get_filling_date(request):
    """Достаем дату из запроса."""
    filling_date = FILLING_DATE_REG_EXP.search(request.body)
    if filling_date:
        filling_date = filling_date.groups()[0]
    else:
        filling_date = ''

    return filling_date


@atomic
def check_declaration_to_archive(
        declaration: Declaration,
        provider_request: GetProviderRequest
) -> None:
    """
    Проверяет дату из запроса (из тега FilingDate) и "Дата подачи заявки"
    заявления. Если дата в теге меньше даты в заявке, то данную заявку
    переводим в архив.

    :param declaration: Найденная в системе заявка
    :param provider_request: Запрос
    """

    status_checked = (
        declaration.status.code not in [DSS.REFUSED, DSS.ARCHIVE, DSS.ACCEPTED]
    )

    filling_date = get_filling_date(provider_request)
    filling_date = datetime.datetime.strptime(
        filling_date, '%Y-%m-%dT%H:%M:%S%z') if filling_date else None

    if (status_checked and filling_date and
            filling_date < timezone.make_aware(declaration.date)):
        archive_status = DeclarationStatus.objects.get(code=DSS.ARCHIVE)

        declaration.change_status(
            archive_status,
            why_change='Авто смена статуса при поступлении '
                       'заявления с источником Концентратор',
            is_auto=True
        )


def get_error_requests_info(start_date, end_date, dry, set_to_archive):
    """Получение информации о неудавшихся запросах за указанные даты

    :param start_date: Дата начала периода
    :param end_date: Дата конца периода

    :return: Кортеж (информация о запросах, список с сообщениями об ошибках)
    """
    warning_messages = []
    data = []

    smev_log_query = get_error_smev_log_query(start_date, end_date)
    for smev_log in smev_log_query.iterator():
        # Нахождение orderId в логе СМЭВ
        order_id_result = ORDER_ID_REG_EXP.search(smev_log.request)
        if not order_id_result:
            warning_messages.append(ORDER_ID_NOT_FOUND.format(smev_log.id))
            continue

        # Нахождение запроса АИО по найденному orderId
        order_id = order_id_result.groups()[0]
        provider_request = get_provider_request(order_id)
        if not provider_request:
            warning_messages.append(
                AIO_REQUEST_NOT_FOUND.format(smev_log.id, order_id))
            continue

        # Проверка, что заявление уже создано для данного orderId
        declaration = get_declaration_by_order_id(order_id)

        # Проверка, нужно ли перенсти заявление в архив
        if not dry and set_to_archive and declaration:
            check_declaration_to_archive(declaration, provider_request)

        data.append((smev_log, order_id, provider_request, declaration))

    return data, warning_messages


def get_response_info(data):
    """Получение информации о результатах работы

    :param data: Данные о неудавшихся запросах

    :return: Информация о результатах работы
    """
    response_data = []

    for _, order_id, request, attachments_str in data:
        # Получение org_code из ответа
        response = PostProviderRequest.objects.filter(
            origin_message_id=request.origin_message_id
        ).last()
        if response and response.body:
            result = ORG_CODE_REG_EXP.search(response.body)
            org_code = result.groups()[0] if result else 'orgCode не найден'
        else:
            org_code = 'Ответ не найден'

        # Получение данных из заявления
        declaration = get_declaration_by_order_id(order_id)
        if declaration:
            fullname = declaration.children.fullname
            declaration_date = prep_date(declaration.date)
            date_of_birth = prep_date(declaration.children.date_of_birth)
            dul_series_number = (
                f'{declaration.children.dul_series} '
                f'{declaration.children.dul_number}'
            )
            declaration_id = declaration.id
        else:
            fullname = declaration_date = DECLARATION_NOT_FOUND
            date_of_birth = ''
            dul_series_number = ''
            declaration_id = ''

        filling_date = get_filling_date(request)

        response_data.append((
            order_id, fullname, date_of_birth, dul_series_number,
            declaration_id,
            declaration_date,
            filling_date,
            org_code,
            request.origin_message_id,
            attachments_str
        ))
    return response_data


@atomic
def check_attachments_to_clear(provider_requests_data, dry):
    """
    Проверка достпуности вложений у запроса на аио сервере, если вложения
    не доступны (возвращается 404 ошибка) они будут удалены из запроса
    и сохранении в выходном Excel файле.
    """

    requests_data_with_attachments = []

    for smev_log, order_id, provider_request, attachments_str in (
            provider_requests_data):
        attachments_str = (
            str(provider_request.attachments) if
            provider_request.attachments is not None else ''
        )
        if provider_request.attachments:
            attachments = provider_request.attachments

            # маневр на случай если в attachments прийдет
            # JSON обернутый в список
            if isinstance(attachments, list):
                attachments = [
                    json.loads(attachment) for attachment in attachments]
            else:
                attachments = json.loads(attachments)

            # Получение адреса сервера АИО без лишних частей
            base_aio_url = urllib.parse.urljoin(
                aio_client_settings.AIO_SERVER, '/')

            for attachment in attachments:
                url = attachment[0].strip("/")
                url = urllib.parse.urljoin(base_aio_url, url)
                try:
                    urllib.request.urlopen(url)
                except (urllib.error.HTTPError, urllib.error.URLError):
                    if not dry:
                        provider_request.attachments = None
                        provider_request.save()

                    break

        requests_data_with_attachments.append((
            smev_log, order_id, provider_request, attachments_str
        ))

    return requests_data_with_attachments


def write_response_info_to_file(response_data):
    """Вывод в файл информации о результатах работы менедж-команды

    :param response_data: Информация о результатах работы менедж-команды
    """
    file_name = 'response_info.xlsx'
    with WorkBookWriter(file_name, RESULTS_INFO_HEADER) as writer:
        for row_data in response_data:
            writer.write_row_data(row_data)
    print(f'Результаты работы менедж-команды выгружены в файл "{file_name}"')


def main(start_date, end_date, dry, set_to_archive, clear_attachments):
    if clear_attachments:
        try:
            urllib.request.urlopen(aio_client_settings.AIO_SERVER)
        except (urllib.error.HTTPError, urllib.error.URLError):
            raise urllib.error.URLError(
                'Невозможно запустить менедж-команду с параметром '
                'clear_attachments (производится попытка получить вложения '
                'для запроса (attachments) с сервера АИО), так как АИО '
                'не доступен.'
            )

    # Нахождение информации о неудачных запросах с ошибкой 404
    requests_data, warning_messages = get_error_requests_info(
        start_date, end_date, dry, set_to_archive)

    # Вывод ошибок, если есть
    print_warning_messages(warning_messages)
    # Запись информации о найденных запросах в excel файл
    write_requests_info_to_file(requests_data)

    if dry:
        print('Изменения не будут внесены, менедж-команда '
              'запущена в тестовом режиме')
        return

    # Оставляем только запросы без заявлений
    requests_data = [
        (smev_log, order_id, request, '')
        for smev_log, order_id, request, decl in requests_data if not decl
    ]
    # Информация о неудавшихся запросах в АИО
    provider_requests = [request for _, _, request, _ in requests_data]
    if not provider_requests:
        print('Нет запросов для переотправки')
        return

    if clear_attachments:
        requests_data = check_attachments_to_clear(requests_data, dry)

    # Повторная обработка неудачных запросов
    process_provider_requests(provider_requests)
    # Получение и вывод в файл результатов работы менедж-команды
    response_data = get_response_info(requests_data)
    write_response_info_to_file(response_data)


class Command(BaseCommand):

    help = (
        'Обработка запросов с заявлениями, для которых упала ошибка 404, '
        'за определенный период.'
    )

    def add_arguments(self, parser):
        def parse_date(string):
            """Получение даты из строки."""
            return datetime.datetime.strptime(string, DATE_FORMAT).date()

        parser.add_argument(
            'start_date', type=parse_date, help='Дата начала периода',
        )
        parser.add_argument(
            'end_date', type=parse_date, help='Дата конца периода',
        )
        parser.add_argument(
            '--set_to_archive',
            action='store_true',
            help='Переносить ли заявки в архив (нет по умолчанию)'
        )
        parser.add_argument(
            '--clear_attachments',
            action='store_true',
            help='Проводить ли проверку вложений по запросу '
                 '(с возможной их очисткой)'
        )
        parser.add_argument(
            '--dry',
            action='store_true',
            help='Получить информацию о запросах без изменений в БД'
        )
        return parser

    def handle(self, *args, **options):
        _start_date = options['start_date']
        _end_date = options['end_date']
        _dry = options['dry']
        _set_to_archive = options['set_to_archive']
        _clear_attachments = options['clear_attachments']

        main(_start_date, _end_date, _dry, _set_to_archive, _clear_attachments)
