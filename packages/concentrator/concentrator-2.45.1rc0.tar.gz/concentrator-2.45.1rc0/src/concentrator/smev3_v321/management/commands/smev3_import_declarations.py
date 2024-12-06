import csv
import os.path

from django.core.management.base import BaseCommand
from kinder.core.declaration.models import Declaration
from kinder.core.declaration_status.enum import DSS

from concentrator.smev3_v321.models import DeclarationPortalID


class Command(BaseCommand):
    """
    Команда для присвоения заявлениям идентификатора ЕПГУ.

    Команда имеет следующие параметры:
    Обязательные:
    --in Путь до входящего .csv файла;
    Необязательные:
    --out Путь до директории, где будет создан результирующий .csv файл
    --dry Запустить команду без изменений в БД (в режиме тестирования)
    --ignore Игнорирует все ошибки, которые могут возникнуть при записи в БД
    --encoding Кодировка входящего файла

    Принцип работы:
    Значения из второго столбца исходящего файла
    (Идентификатор заявления в ИС КУ) сопоставляются с declaration.client_id.
    Если соответствие найдено, проверяется вхождение declaration.status__code
    в перечень недопустимых статусов и наличие записей в таблице
    smev3_v321_declarationoriginmessageid ссылающихся на соответствующие записи
    в declaration. В результате выполнения команды создается .csv файл с
    записями из входящего .csv файла разделенными на 4 группы:
    1.) client_id совпал. статус допустимый, записи в
    smev3_v321_declarationoriginmessageid для этого заявления еще нет
    2.) client_id совпал, запись в smev3_v321_declarationoriginmessageid есть
    3.) client_id не совпал
    4.) client_id совпал, статус недопустимый
    Если параметр --dry не был указан, для заявлений из пункта №1 создаются
    записи в таблице smev3_v321_declarationoriginmessageid
    """

    SUCCESS = 'Идентификатор заявления на портале присвоен'
    EXISTS = 'Соответствующее заявление создано ранее!'
    NO_MATCH = 'Соответствующее заявление не найдено!'
    WRONG_STATUS = 'Соответствующее заявление не в промежуточном статусе!'
    WRONG_STATUSES = [DSS.REFUSED, DSS.ACCEPTED]

    def add_arguments(self, parser):
        parser.add_argument(
            '--in', type=str,
            help='Путь до входящего .csv файла', default=None)
        parser.add_argument(
            '--out', type=str,
            help='Путь до исходящего .csv файла', default='')
        parser.add_argument(
            '--encoding', type=str,
            help='Кодировка', default='cp1251')
        parser.add_argument(
            '--dry', action='store_true',
            help='Запустить команду в режиме тестирования')
        parser.add_argument(
            '--ignore', action='store_true',
            help='Игнорировать ошибки в БД')

    def handle(self, *args, **options):
        input_file_name = options['in']
        is_test_mode = options['dry']
        out_path = options['out']
        encoding = options['encoding']
        ignore_conflicts = True if options['ignore'] else False
        wrong_statuses = self.WRONG_STATUSES

        if input_file_name is None:
            self.stdout.write(
                'Необходимо указать путь до входящего .csv файла')
            return

        if not os.path.isfile(input_file_name):
            self.stdout.write(
                'Указан некорректный путь до входящего .csv файла')
            return

        if out_path and not os.path.isdir(out_path):
            self.stdout.write(
                'Указан некорректный путь до директории исходящего .csv файла')
            return

        if is_test_mode:
            self.stdout.write('Команда запущена в режиме тестирования')

        with open(input_file_name, newline='', encoding=encoding) as in_file:

            reader = csv.reader(in_file, delimiter=';')

            try:
                # Пропуск шапки
                next(reader)
            # В тестовом примере первая строка не читается
            except UnicodeDecodeError:
                pass

            # Сей маневр нужен для того, чтобы сократить количество запросов
            bulk_dict = {}

            for row in reader:
                bulk_dict.update({row[1]: row[0]})

            bulk_keys = bulk_dict.keys()

            declarations = Declaration.objects.filter(
                client_id__in=bulk_keys)
            smev_declarations = DeclarationPortalID.objects.all(
            ).values_list('declaration_id', flat=True)

            duplicate_ids = declarations.filter(
                id__in=smev_declarations).values_list(
                'client_id', flat=True)

            wrong_status_ids = declarations.filter(
                status__code__in=wrong_statuses).exclude(
                id__in=smev_declarations).values_list(
                'client_id', flat=True)

            not_matching_ids = set(bulk_keys) - set(declarations.values_list(
                'client_id', flat=True))

            matching_declarations = declarations.exclude(
                status__code__in=wrong_statuses
            ).exclude(id__in=smev_declarations)

            with open(os.path.join(
                    out_path, 'out_smev3_import_declarations.csv'), 'w'
            ) as output_file:
                writer = csv.writer(output_file, delimiter=';')

                writer.writerow([
                    'Идентификатор заявления в ИС КУ',
                    'Идентификатор заявления на портале',
                    'Результат',
                ])
                for _id in matching_declarations.values_list(
                        'client_id', flat=True):
                    writer.writerow([_id, bulk_dict[_id], self.SUCCESS])
                for _id in duplicate_ids:
                    writer.writerow([_id, bulk_dict[_id], self.EXISTS])
                for _id in not_matching_ids:
                    writer.writerow([_id, bulk_dict[_id], self.NO_MATCH])
                for _id in wrong_status_ids:
                    writer.writerow([_id, bulk_dict[_id], self.WRONG_STATUS])

            if not is_test_mode and matching_declarations.exists():
                bulk_objects = [DeclarationPortalID(
                    portal_id=bulk_dict[obj.client_id], declaration=obj
                ) for obj in matching_declarations]
                DeclarationPortalID.objects.bulk_create(
                    bulk_objects, ignore_conflicts=ignore_conflicts)
