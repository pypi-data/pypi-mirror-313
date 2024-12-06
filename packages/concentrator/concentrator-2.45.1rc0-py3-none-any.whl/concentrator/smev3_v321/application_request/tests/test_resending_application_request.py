from __future__ import annotations

import csv
import tempfile
from datetime import datetime
from pathlib import Path

from aio_client.provider.models import GetProviderRequest
from dateutil.relativedelta import relativedelta

from concentrator.smev3_v321.application_request.resending_helpers import (
    ResendingPathHandler)
from concentrator.smev3_v321.application_request.resending_helpers import (
    ApplicationRequestsStatusChanger)
from concentrator.smev3_v321.application_request.resending_helpers import (
    get_resending_application_requests)
from concentrator.smev3_v321.application_request.resending_helpers import (
    CSV_FILE_DELIMITER)
from concentrator.smev3_v321.application_request.resending_helpers import YES
from concentrator.smev3_v321.application_request.resending_helpers import NO

from concentrator.smev3_v321.models import DeclarationPortalID
from concentrator.smev3_v321.tests.factory import GetProviderRequestF
from concentrator.smev3_v321.tests.factory import PostProviderRequestF
from kinder.core.declaration.tests.factory_declaration import DeclarationF
from kinder.test.base import BaseTC


class ResendingProviderRequestsPathHandlerTC(BaseTC):
    """Тесты для класса ResendingProviderRequestsPathHandler."""

    def setUp(self) -> None:
        super().setUp()
        self.base_path = Path(tempfile.mkdtemp())
        self.path_handler = ResendingPathHandler(self.base_path)

    def test_get_new_file_path(self):
        """Проверка выбора пути файла и создания промежуточных папок."""
        path = self.path_handler.get_new_file_path()
        self.assertFalse(path.is_dir(), 'Проверка, что создана не директория')
        self.assertTrue(path.parent.exists())
        self.assertTrue(path.parent.parent.exists())
        self.assertEqual(path.suffix, '.csv', 'Проверка расширения')

    def test_get_last_file_path(self):
        """Проверка нахождения последнего файла."""
        self.assertIsNone(self.path_handler.get_last_file_path(), 'Файлов нет')
        incorrect_handler = ResendingPathHandler(Path('123'))
        self.assertIsNone(
            incorrect_handler.get_last_file_path(),
            'Указан несуществующий путь',
        )

        path1 = self.path_handler.get_new_file_path()
        self.assertFalse(path1.exists())
        path1.write_text('')
        self.assertTrue(path1.exists())

        # Проверка, что последний документ обновился
        self.assertEqual(self.path_handler.get_last_file_path(), path1)

        path2 = self.path_handler.get_new_file_path()
        path2.write_text('')
        self.assertEqual(self.path_handler.get_last_file_path(), path2)


class ApplicationRequestsStatusChangerTC(BaseTC):
    """Тесты для класса ApplicationRequestsStatusChanger."""

    def setUp(self):
        super().setUp()
        self.base_path = Path(tempfile.mkdtemp())

    @staticmethod
    def read_data_from_csv(path: Path) -> list[list]:
        """Прочитать данные из csv файла."""
        with open(path) as f:
            reader = csv.reader(f, delimiter=CSV_FILE_DELIMITER)
            headers_data = next(reader)
            return [row for row in reader]

    def test_main(self):
        """Основные тесты для класса"""
        result = ApplicationRequestsStatusChanger(
            self.base_path).change_statuses_and_write_results_to_csv()
        self.assertEqual(
            (result.csv_path, result.requests_count,
             result.previously_resended_count),
            (None, 0, 0)
        )

        application_request_text = Path(__file__).parent.joinpath(
            'ApplicationRequest.xml').read_text()
        order_id_from_file = '14025644457542599'
        origin_message_id = '111'
        request = GetProviderRequestF(
            message_type='FormData',
            origin_message_id=origin_message_id,
            state=GetProviderRequest.SENT,
            body=application_request_text,
        )
        result = ApplicationRequestsStatusChanger(
            self.base_path).change_statuses_and_write_results_to_csv()
        self.assertEqual(result.requests_count, 1)
        self.assertEqual(result.previously_resended_count, 0)
        self.assertTrue(result.csv_path.exists())
        self.assertListEqual(
            self.read_data_from_csv(result.csv_path),
            [[request.origin_message_id, order_id_from_file, NO]]
        )

        # Возвращаем статус запроса, чтобы при повторном запуске уже был
        # повторяющийся запрос
        request.refresh_from_db()
        request.state = GetProviderRequest.SENT
        request.save()

        result = ApplicationRequestsStatusChanger(
            self.base_path).change_statuses_and_write_results_to_csv()
        self.assertEqual(result.requests_count, 1)
        self.assertEqual(result.previously_resended_count, 1)
        self.assertTrue(result.csv_path.exists())
        self.assertListEqual(
            self.read_data_from_csv(result.csv_path),
            [[request.origin_message_id, order_id_from_file, YES]]
        )


class GetResendingApplicationRequestsTC(BaseTC):
    """Тесты для функции get_resending_application_requests."""

    def test_other_request(self):
        """Проверка других запросов."""
        other_request_text = Path(__file__).parent.joinpath(
            'OtherRequest.xml').read_text()

        GetProviderRequestF(
            message_type='FormData',
            state=GetProviderRequest.SENT,
            body=other_request_text,
        )
        GetProviderRequestF(
            message_type='FormData',
            state=GetProviderRequest.NOT_SENT,
            body=other_request_text,
        )

        self.assertFalse(get_resending_application_requests())

    def test_application_request(self):
        """Проверка ApplicationRequest."""

        application_request_text = Path(__file__).parent.joinpath(
            'ApplicationRequest.xml').read_text()
        order_id_from_file = '14025644457542599'
        other_order_id = '999'

        correct_request = GetProviderRequestF(
            message_type='FormData',
            state=GetProviderRequest.SENT,
            body=application_request_text,
        )
        GetProviderRequestF(
            message_type='FormData',
            state=GetProviderRequest.NOT_SENT,
            body=application_request_text,
        )

        with self.subTest('Находим запрос, поскольку заявления нет'):
            resending_requests = get_resending_application_requests(3)
            self.assertListEqual(
                [r.id for r in resending_requests], [correct_request.id])
            self.assertEqual(resending_requests[0].order_id, order_id_from_file)

        with self.subTest('Проверка отсутствия нужного ответа'):
            PostProviderRequestF(
                message_type='OtherRequest', origin_message_id='123')
            self.assertEqual(
                len(list(get_resending_application_requests(3))), 1)

        with self.subTest('При наличии ответа запрос не находим'):
            response = PostProviderRequestF(
                message_type='FormData',
                origin_message_id=correct_request.origin_message_id
            )
            self.assertEqual(
                len(list(get_resending_application_requests(3))), 0)
            response.delete()

        with self.subTest('Проверка, что на грани срока запрос будет найден'):
            correct_request.request_id.timestamp_created = (
                datetime.now() - relativedelta(months=3))
            correct_request.request_id.save()
            self.assertEqual(
                len(list(get_resending_application_requests(3))), 1)

        with self.subTest('Запрос не найден из-за срока давности'):
            correct_request.request_id.timestamp_created = (
                datetime.now() - relativedelta(months=4))
            correct_request.request_id.save()
            self.assertEqual(
                len(list(get_resending_application_requests(3))), 0)

        # Возвращаем нормальное время запроса
        correct_request.request_id.timestamp_created = datetime.now()
        correct_request.request_id.save()

        with self.subTest(
                'Запрос не будет найден, поскольку есть заявление с client_id'):
            declaration = DeclarationF(client_id=order_id_from_file)
            self.assertEqual(
                len(list(get_resending_application_requests())), 0)

        # Специально меняем client_id на любой другой
        declaration.client_id = other_order_id
        declaration.save()
        self.assertEqual(
            len(list(get_resending_application_requests())), 1)

        with self.subTest(
                'Запрос не будет найден, поскольку есть заявление с portal_id'):
            DeclarationPortalID.objects.create(
                portal_id=order_id_from_file, declaration=declaration)
            self.assertEqual(
                len(list(get_resending_application_requests())), 0)
