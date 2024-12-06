import os

from excel_reporting import report_gen
from m3.actions.exceptions import ApplicationLogicException

from concentrator.changes.helpers import get_storage_helper
from concentrator.constants import MESSAGE_PLUGIN_SMEV3_REQUIRED
from concentrator.models import ChangeDeclaration


class ReportChanges(report_gen.BaseReport):
    """
    Генерирование заполненного заявления на изменение данных
    """

    def __init__(self, template, temp_filename, request, context):
        self.template_name = os.path.join(
            os.path.dirname(__file__), 'templates', template)
        self.result_name = temp_filename
        self.request = request
        self.context = context

    def add_row(self, change_set, model, field, old, new):
        """Добавляет запись в словарь change_set.
        :param dict change_set: словарь с изменений по модели
        :param str model:
        :param str field:
        :param old:
        :param new:

        """

        change_set.setdefault(model, {
            'fields': [],
            'old_values': [],
            'new_values': [],
        })
        if field:
            change_set[model]['fields'].append(field)
        change_set[model]['old_values'].append(
            str(old if old is not None else ' - '))
        change_set[model]['new_values'].append(
            str(new if new is not None else ' - '))

    def collect(self, *args, **kwargs):
        change_declaration_id = getattr(self.context, 'id', None)
        if change_declaration_id:
            try:
                change = ChangeDeclaration.objects.get(
                    id=change_declaration_id)
            except ChangeDeclaration.DoesNotExist:
                raise ApplicationLogicException(
                    f'Список изменений по заявке '
                    f'(ID={change_declaration_id}) не найден')

            storage_helper_cls = get_storage_helper(change.declaration)
            if storage_helper_cls is None:
                raise ApplicationLogicException(MESSAGE_PLUGIN_SMEV3_REQUIRED)

            change_set = dict()
            fields = []
            old_values = []
            new_values = []

            # получаем список изменений который отображается
            # на вкладке "Изменения с ЕПГУ"
            for row in storage_helper_cls.get_change(change):
                try:
                    model, field = row['field'].split(':', 1)
                except ValueError:
                    # изменения по Желаемым организациям и
                    # Льготам к заявке обрабатываются иначе
                    model, field = row['field'], ''

                self.add_row(
                    change_set, model, field,
                    row['old_value'], row['new_value'])

            for model, data in list(change_set.items()):
                if data['fields']:
                    fields.append('{0}: {1}'.format(
                        model, ', '.join(data['fields'])))
                else:
                    # Льготы и Желаемые организации отображаются
                    # без списка полей
                    fields.append(model)
                old_values.append('{0}: {1}'.format(
                    model, ', '.join(data['old_values'])))
                new_values.append('{0}: {1}'.format(
                    model, ', '.join(data['new_values'])))

            mo = change.declaration.mo
            children = change.declaration.children
            delegate = children.childrendelegate_set.all()[0].delegate

            row = {
                'director_fullname': mo.boss_fio,
                'delegate_fullname': delegate.fullname,
                'children_fullname': children.fullname,
                'birth_date': children.date_of_birth.strftime('%d.%m.%Y'),
                'fields': '; '.join(fields),
                'old_values': '; '.join(old_values),
                'new_values': '; '.join(new_values),
                'date': change.create.strftime('%d.%m.%Y')
            }

            total = 1
        else:
            row = {}
            total = 0

        return {'rows': [row], 'total': total}
