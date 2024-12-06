import sys

from django.core.management.base import BaseCommand

from concentrator.change import StorageHelper
from concentrator.exceptions import ValidationError
from concentrator.models import ChangeDeclaration
from concentrator.models import ChangeStatus


class Command(BaseCommand):

    help = 'Deсline invalid declaration change requests from EPGU'

    def handle(self, *args, **options):
        """
        Отклоняем запросы с ЕПГУ на изменения заявления,
        если они содежрат невалидные данные
        """
        class EmptyObject:
            pass

        query = ChangeDeclaration.objects.filter(
            state=ChangeStatus.WAIT).order_by('create')

        rejected_count = 0
        for row in query:
            try:
                StorageHelper.get_change(row)
            except ValidationError:
                # Если с ЕПГУ были полученны невалидные данные,
                # удаляем запрос на изменение
                row.delete()
                rejected_count += 1
        sys.stdout.write(
            '{rejected_count} change requests were deleted\n'.format(
                rejected_count=rejected_count)
        )
