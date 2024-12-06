from objectpack.actions import ObjectListWindowAction

from concentrator.changes.actions import ChangesDetailPack
from concentrator.changes.actions import ChangesPack
from concentrator.changes.actions import ChangesRowsAction
from concentrator.models import ChangeDeclaration


class LipetskChangesPack(ChangesPack):
    """Пак для вкладки "Изменения с ЕПГУ" Липецка."""

    columns = [
        {
            'data_index': 'case_number',
            'header': 'Идентификатор изменения',
            'searchable': False,
            'sortable': True,
        }] + ChangesPack.columns

    def __init__(self):
        super().__init__()

        self.changes_rows_action = LipetskChangesRowsAction()

        self.replace_action('rows_action', self.changes_rows_action)
        self.replace_action('list_window_action', ChangesListWindowAction())


class LipetskChangesRowsAction(ChangesRowsAction):
    """Экшн преобразует набор изменений для грида во вкладке
    "Изменения с ЕПГУ" Липецка.

    """

    def _get_row(self, request, context, row):
        original_row = super()._get_row(request, context, row)
        original_row['case_number'] = row.case_number
        return original_row


class LipetskChangesDetailPack(ChangesDetailPack):
    """Пак детального просмотра набора изменений Липецка."""

    def declare_context(self, action):
        result = super().declare_context(action)

        if action is self.list_window_action:
            result['id'] = {'type': 'int'}

        return result

    def get_list_window_params(self, params, request, context):
        params = super().get_list_window_params(params, request, context)

        changes_case_number = (
            ChangeDeclaration.objects.values_list(
                'case_number', flat=True).get(id=context.id))

        params['title'] = f'{self.title} ({changes_case_number})'

        return params


class ChangesListWindowAction(ObjectListWindowAction):
    """
    Переопределили для задания verbose_name
    """
    verbose_name = 'Просмотр'
