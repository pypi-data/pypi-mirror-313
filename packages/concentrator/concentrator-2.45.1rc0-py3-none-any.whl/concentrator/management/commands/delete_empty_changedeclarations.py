import json
from itertools import chain

from django.core.management.base import BaseCommand
from django.db.models import Q
from tqdm import tqdm

from concentrator.change import StorageHelper
from concentrator.constants import PRIVILEGE_COMMENT
from concentrator.models import ChangeDeclaration
from concentrator.models import ChangeStatus


def _get_changes_with_only_comment(query):
    """
    Возвращает записи ChangeDeclaration из запроса, в которых содержится
    только комментарий к льготе
    :param query: Queryset, в котором будет производиться поиск
    :type query: Queryset
    :return: список ChangeDeclaration, содержащих только комментарий
    :rtype: List[ChangeDeclaration]
    """
    objects_with_only_comment = []
    query_with_comment_iterator = query.filter(
        data__startswith='{"ConcentratorPrivilegeComment":').iterator()
    for obj in query_with_comment_iterator:
        data = json.loads(obj.data)
        if len(data) == 1 and PRIVILEGE_COMMENT in data:
            objects_with_only_comment.append(obj)
    return objects_with_only_comment


def _search_irrelevant_changes(query):
    """
    Ищет записи ChangeDeclaration из запроса, содержащие изменения, но которые
    стали уже неактуальны (т.е. на текущий момент изменений нет).
    Также выводит прогресс-бар в консоль для отслеживания прогресса поиска
    :param query: Queryset, в котором будет производиться поиск
    :type query: Queryset
    :return: список неактуальных записей ChangeDeclaration
    :rtype: List[ChangeDeclaration]
    """
    irrelevant_changes_query = query.select_related()
    irrelevant_changes = []
    for changes in tqdm(irrelevant_changes_query.iterator(),
                        total=irrelevant_changes_query.count()):
        try:
            if not StorageHelper.get_change(changes):
                irrelevant_changes.append(changes)
        except ValueError:
            continue
    return irrelevant_changes


class Command(BaseCommand):
    """
    Выполняет поиск и удаление пустых изменений с ЕПГУ в статусе
    'Ожидает решения'. Под пустой записью понимается запись ChangeDeclaration,
    у которой поле data содержит:
    -null,
    -пустую строку,
    -только комментарий к льготе,
    -изменения, которые на текущий момент стали неактуальны, потому что они
    уже содержатся в базе данных.
    При просмотре подобных записей на вкладке "Изменения с ЕПГУ"
    не отображаются изменения
    """

    help = 'Удаление пустых записей с изменениями заявки с ЕПГУ'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry', dest='dry_run', action='store_true',
            help='Тестовый запуск (не вносит изменения в базу)'
        )

    def handle(self, *args, **options):

        def print_objects(name, objects):
            """Вывод информации об изменениях ЕПГУ
            :param name: Название группы объектов в множественном числе
            :param objects: Iterable, содержащий объекты ChangeDeclaration
            """
            if not objects:
                print(f'{name} не найдены.\n')
                return
            print(f'{name}:')
            for obj in objects:
                print(f'id: {obj.id}; '
                      f'информация о заявлении: {obj.declaration};'
                      f' значения поля data = {obj.data}')
            print()

        query = ChangeDeclaration.objects.filter(
            state=ChangeStatus.WAIT).select_related('declaration')

        empty_records = query.filter(Q(data__isnull=True) | Q(data=''))
        print_objects('Пустые записи с изменениями заявки с ЕПГУ',
                      empty_records)

        objects_with_only_comment = _get_changes_with_only_comment(query)
        print_objects('Записи, содержащие только комментарий для льготы',
                      objects_with_only_comment)

        print('Поиск записей, содержащих изменения, но которые стали уже '
              'неактуальны (т.е. на текущий момент изменений нет):')
        irrelevant_changes = _search_irrelevant_changes(query)
        print_objects('Неактуальные записи', irrelevant_changes)

        if not options['dry_run']:
            # Удаление записей
            for obj in chain(empty_records, objects_with_only_comment,
                             irrelevant_changes):
                obj.delete()
            print('Удаление прошло успешно')
