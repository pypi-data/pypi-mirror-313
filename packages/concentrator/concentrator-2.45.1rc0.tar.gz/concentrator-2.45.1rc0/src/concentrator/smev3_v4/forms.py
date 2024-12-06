from __future__ import annotations

from educommon.m3.extensions import BaseEditWinExtender
from m3_ext.ui.fields import ExtCheckBox

from kinder.controllers import obs
from kinder.core.children.models import Delegate
from kinder.core.declaration.models import Declaration
from kinder.core.dict.models import GroupType
from kinder.core.dict.models import GroupTypeEnumerate
from kinder.core.helpers import extend_window_plugins


class DeclarationEditWindowExtender(BaseEditWinExtender):
    """Расширение окна редактирования заявления."""

    model = Declaration
    model_fields = ['adapted_program_consent']
    model_register = obs

    def _extend_edit_win(self):
        self.model_fields_to_controls(self.model_fields)
        self._win.child_info_tab.doc_pan_checkbox_form.items.insert(7,
            self._win.field__adapted_program_consent)
        self._win.comp_type = GroupType.objects.get(code=GroupTypeEnumerate.COMP).id

        extend_window_plugins(self._win, 'ui-js/decl_edit_extend_smev4.js')

    def set_params(self, params):
        if not params['has_edit_perm']:
            self._win.field__adapted_program_consent.read_only = True



class DelegateEditWinExtender(BaseEditWinExtender):
    """Добавляет чек-бокс Документ о праве нахождения в РФ"""

    model = Delegate
    model_fields = ['confirming_rights_located_rf', ]
    model_register = obs

    def get_item_index(self, item_name: str) -> int | None:
        """Возвращает индекс элемента в карточке представителя по его названию

        :param item_name: Название элемента
        :return: Индекс элемента
        """
        return next(
            (i for i, item in enumerate(self._win.delegate_pan.items)
             if item.label == item_name), None
        )

    def _extend_edit_win(self):
        confirming_rights_located_rf = ExtCheckBox(
            label='Документ о праве нахождения в РФ',
            name='confirming_rights_located_rf',
            label_style={'width': '220px'}
        )
        default_index = len(self._win.delegate_pan.items) - 1
        index = (
            self.get_item_index('Гражданство') or
            self.get_item_index('Тип оповещения') or default_index
        )

        self._win.delegate_pan.items.insert(
            index + 1, confirming_rights_located_rf)
