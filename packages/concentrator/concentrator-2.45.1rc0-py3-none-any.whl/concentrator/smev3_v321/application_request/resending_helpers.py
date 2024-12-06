from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from datetime import date
from pathlib import Path

from aio_client.provider.models import GetProviderRequest
from dateutil.relativedelta import relativedelta
from django.conf import settings
from typing import Any
from typing import Callable

from django.db.models.query import RawQuerySet

from concentrator.smev3_v321.settings import (
    RESEND_APPLICATION_REQUESTS_YOUNGER_THAN_IN_MONTHS)
from kinder import logger


YES = 'Да'
NO = 'Нет'
# Путь до папки, где будут находиться результирующие файлы
RESULTS_DIR_PATH = Path(settings.DOWNLOADS_DIR).joinpath(
    'application_requests_status_change')
# Формат пути до csv файла
CSV_FILE_PATH_FORMAT = '%Y/%m/%Y_%m_%d %H:%M:%S.csv'
# Разделитель в csv файле
CSV_FILE_DELIMITER = ','
# Заголовок csv-файла
CSV_FILE_HEADER = (
    'origin_message_id', 'orderId из запроса', 'Запрос переотправлялся ранее')


def get_resending_application_requests(
        months_for_requests: int = (
                RESEND_APPLICATION_REQUESTS_YOUNGER_THAN_IN_MONTHS)
) -> RawQuerySet:
    """
    Получение запросов ApplicationRequest, которым необходимо сменить статус
    для повторного приёма

    :param months_for_requests: Количество месяцев, старше которого
        запросы не рассматриваются

    :return: Запросы ApplicationRequest, которым необходимо сменить статус
        для повторного приёма
    """
    date_for_filtering = (
        date.today() - relativedelta(months=months_for_requests))

    # Используется сырой запрос вместо ORM из-за проверки на наличие заявления
    # (операторы exists и in выполняются очень долго в этом случае -
    # до нескольких часов).
    # В запросе используется несколько основных join:
    # 1. Соединяем таблицу с самой собой для фильтрации и подсчёта order_id
    # 2. Проверка, что такого заявления ещё нет по client_id/portal_id
    # 3. Соединение для проверки отсутствия ответа по запросу
    raw_query = GetProviderRequest.objects.raw(
        """
        SELECT aio_client_getproviderrequest.*, main_table.order_id
        FROM aio_client_getproviderrequest

        INNER JOIN (
        SELECT
            provider_request.id,
            (substring(body FROM 'orderId>(\d+?)</')) AS order_id
        FROM aio_client_getproviderrequest provider_request
        INNER JOIN "aio_client_requestlog" request_log
        ON provider_request.request_id_id = request_log.id
        WHERE (
          provider_request."body"::text LIKE %s
          AND provider_request."message_type" = %s
          AND request_log.timestamp_created::date >= %s::date
          AND provider_request.state = %s
        )
        ) main_table on aio_client_getproviderrequest.id = main_table.id

        LEFT JOIN (
            SELECT client_id FROM "declaration"
            UNION
            SELECT portal_id FROM "smev3_v321_declarationportalid"
        ) client_portal_ids
        on main_table.order_id=client_portal_ids.client_id

        LEFT JOIN (
            SELECT DISTINCT ON (origin_message_id) origin_message_id, id
            FROM aio_client_postproviderrequest
            ORDER BY origin_message_id, id
        ) response_table on aio_client_getproviderrequest.origin_message_id = 
        response_table.origin_message_id

        WHERE client_portal_ids.client_id IS NULL
        AND response_table.id IS NULL
        """,
        ('%ApplicationRequest%', 'FormData', str(date_for_filtering),
         GetProviderRequest.SENT)
    )
    return raw_query


class ResendingPathHandler:
    """Помогает работать с путями к файлам при переотправке."""

    def __init__(self, base_path: Path) -> None:
        """
        :param base_path: Базовый путь, в котором располагаются файлы с
            результатами переотправки
        """
        self.base_path = base_path

    def get_new_file_path(
            self, file_path_format: str = CSV_FILE_PATH_FORMAT) -> Path:
        """Формирует путь до файла

        :param file_path_format: Формат пути файла для формирования на основе
            даты и времени

        :return: Путь до файла, куда можно сохранить результат
        """
        file_path = datetime.now().strftime(file_path_format)
        new_path = self.base_path.joinpath(file_path)
        new_path.parent.mkdir(parents=True, exist_ok=True)
        return new_path

    @staticmethod
    def get_max_file_path_name(
            dir_path: Path | None, is_dir: bool) -> Path | None:
        """Получает путь до файла/директории с "максимальным" названием

        Нужно для нахождения последнего записанного файла

        :param dir_path: Путь до директории, в которой будет поиск
        :param is_dir: Производить поиск только по директориям (True) или только
            по файлам

        :return: Путь файла/директории с "максимальным" названием или None
        """
        if not dir_path or not dir_path.exists():
            return None

        paths = [
            p for p in dir_path.iterdir()
            if (p.is_dir() if is_dir else not p.is_dir())
        ]
        if paths:
            return max(paths)

    def get_last_file_path(self) -> Path | None:
        """Путь последнего файла результата или None."""
        if not self.base_path.exists():
            return None

        year_path = self.get_max_file_path_name(self.base_path, is_dir=True)
        month_path = self.get_max_file_path_name(year_path, is_dir=True)
        file_path = self.get_max_file_path_name(month_path, is_dir=False)
        return file_path


@dataclass
class ResendApplicationRequestsInfo:
    """Информация о переотправках запросов ApplicationRequest"""
    csv_path: Path | None = None
    requests_count: int = 0
    previously_resended_count: int = 0

    @property
    def file_download_url(self) -> str:
        """
        Возвращает ссылку на скачивание файла или пустую строку в случае,
        если путь некорректен
        """
        if (not self.csv_path or
                settings.DOWNLOADS_DIR not in str(self.csv_path)):
            return ''
        return str(self.csv_path).replace(
            settings.DOWNLOADS_DIR, settings.DOWNLOADS_URL)


class ApplicationRequestsStatusChanger:
    """
    Класс для смены статусов запросов ApplicationRequest на "Не отправлен"
    для повторного приёма.
    """

    def __init__(
            self, base_result_path: Path = RESULTS_DIR_PATH,
            set_progress: Callable[[Any], None] | None = None,
    ) -> None:
        """
        :param base_result_path: Базовый путь, в котором располагаются файлы с
            результатами переотправки
        :param set_progress: Функция для обновления прогресса задачи селери
        """
        self._base_path = base_result_path
        self.set_progress = (
            set_progress if set_progress else lambda *args, **kwargs: None)

        self._path_handler = ResendingPathHandler(Path(self._base_path))

    def get_origin_message_ids_from_last_file(self) -> set[str]:
        """Получение всех origin_message_id из файла с прошлой переотправки."""
        try:
            file_path = self._path_handler.get_last_file_path()
            if not file_path:
                return set()

            with open(file_path, 'r') as f:
                csv_reader = csv.reader(f, delimiter=CSV_FILE_DELIMITER)
                headers_data = next(csv_reader)
                return {message_id for message_id, *_ in csv_reader}

        except Exception as e:
            logger.exception(
                f'Не удалось прочитать данные о переотправленных '
                f'запросах ApplicationRequest ({e})')
            return set()

    def change_statuses_and_write_results_to_csv(
            self) -> ResendApplicationRequestsInfo:
        """Смена статусов запросов и запись результатов в csv файл

        :return: Информация о переотправках запросов ApplicationRequests
        """
        resended_message_ids = self.get_origin_message_ids_from_last_file()
        path = self._path_handler.get_new_file_path()
        current_count = previously_resended_count = 0

        with open(path, 'w') as f:
            csv_writer = csv.writer(f, delimiter=CSV_FILE_DELIMITER)
            csv_writer.writerow(CSV_FILE_HEADER)
            self.set_progress('Выполняется запрос к бд')
            for current_count, request in enumerate(
                    get_resending_application_requests().iterator(), 1):

                is_previously_resended = (
                    request.origin_message_id in resended_message_ids)

                if is_previously_resended:
                    previously_resended_count += 1

                csv_writer.writerow((
                    request.origin_message_id,
                    request.order_id,
                    YES if is_previously_resended else NO,
                ))

                request.state = GetProviderRequest.NOT_SENT
                request.save()

                self.set_progress('Обработка запросов', values={
                    'Количество переотправленных запросов': current_count,
                    'Количество запросов, которые ранее уже переотправлялись':
                        previously_resended_count,
                })

        if not current_count:
            self.set_progress(values={
                'Количество переотправленных запросов': current_count,
                'Количество запросов, которые ранее уже переотправлялись':
                    previously_resended_count,
            })
            # Удаляем файл, если нет ни одной записи
            path.unlink()
            return ResendApplicationRequestsInfo()

        return ResendApplicationRequestsInfo(
            path, current_count, previously_resended_count)
