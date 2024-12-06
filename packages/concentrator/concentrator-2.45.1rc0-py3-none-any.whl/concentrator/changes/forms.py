import json

from m3.actions import ControllerCache
from m3_ext.ui import all_components as ext
from m3_ext.ui.icons import Icons
from objectpack.ui import ObjectGridTab

from kinder.controllers import obs


class DeclarationEditWindowExtension:
    """
    добавляем вкладку Изменения с ЕПГУ
    """

    @classmethod
    def build_extension(cls, edit_win):
        pack = ControllerCache.find_pack(
            'concentrator.changes.actions.ChangesPack')

        # Инициализация
        edit_win.changes_tab = (
            ObjectGridTab.fabricate_from_pack(
                pack_name=pack.__class__,
                pack_register=obs,
                tab_class_name='ChangesTab'
            )())

        edit_win.changes_tab.template = 'ui-js/changes_tab.js'

        edit_win.changes_tab.changes_open_url = ControllerCache.find_action(
            'concentrator.changes.actions.ChangesDetailWindowAction'
        ).absolute_url()

        edit_win.changes_tab.changes_print_url = (
            pack.changes_print_action.get_absolute_url())
        edit_win.changes_tab.perm_priv_grid_url = (
            pack.perm_priv_grid_action.get_absolute_url())

        edit_win.tabs.append(edit_win.changes_tab)

        edit_win.changes_tab.init_components(edit_win)
        tab = edit_win.changes_tab._create_tab()
        edit_win.changes_tab.do_layout(edit_win, tab)
        edit_win._tab_container.items.append(tab)
        edit_win.tabs_templates.append(edit_win.changes_tab.template)
        edit_win.changes_tab.set_params(edit_win, None)

        # Конфигурирование
        edit_win.changes_tab.grid.top_bar.items[3].disabled = False

        edit_win.changes_tab.open_button = ext.ExtButton(
            text='Открыть', icon_cls=Icons.M3_EDIT,
            handler='openChanges', flex=1)
        edit_win.changes_tab.grid.handler_dblclick = 'openChanges'
        edit_win.changes_tab.print_button = ext.ExtButton(
            text='Распечатать шаблон', icon_cls=Icons.PRINTER,
            handler='printChanges', flex=1)

        edit_win.changes_tab.grid.top_bar.items.insert(
            0,
            edit_win.changes_tab.open_button)
        edit_win.changes_tab.grid.top_bar.items.append(
            edit_win.changes_tab.print_button)

        fields_to_add_tooltip = (
            'new_values',
            'old_values',
            'fields'
        )
        tooltip_plugin_conf = tuple(
            {
                'field': field,
                'tpl': "{[values['%s']]}" % field
            } for field in fields_to_add_tooltip
        )
        edit_win.changes_tab.grid.plugins.append(
            f'new Ext.ux.plugins.grid.CellToolTips({json.dumps(tooltip_plugin_conf)})'
        )

        return edit_win


class DeclarationListWindowExtension:
    """
    Добавляем фильтр 'Отобразить только заявки на подтверждение'
    """

    @classmethod
    def build_extension(cls, list_win):
        list_win.need_confirmation_only = ext.ExtCheckBox(
            box_label=u'Только заявки на подтверждение')
        list_win.menu.items.append(list_win.need_confirmation_only)
        list_win.template_globals.append(
            'ui-js/queue_declaration_list.js'
        )
        list_win.grid.get_row_class = lambda: 'highlightRow'

        return list_win
