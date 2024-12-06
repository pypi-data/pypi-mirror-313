import json

from educommon.m3.extensions import BaseEditWinExtender
from m3.actions import ActionContext
from m3.actions import ControllerCache
from m3_ext.ui import all_components as ext
from m3_ext.ui.containers import ExtContextMenu
from m3_ext.ui.containers import ExtToolbarMenu
from m3_ext.ui.controls.buttons import ExtButton
from m3_ext.ui.fields.complex import ExtDictSelectField
from m3_ext.ui.icons import Icons
from objectpack.ui import BaseEditWindow
from objectpack.ui import BaseListWindow
from objectpack.ui import ModelEditWindow
from objectpack.ui import ObjectGridTab
from objectpack.ui import make_combo_box
from objectpack.ui import model_fields_to_controls

from kinder.controllers import obs
from kinder.core import ui_helpers
from kinder.core.declaration.models import Declaration
from kinder.core.declaration_status.enum import DSS
from kinder.core.queue_module.declaration.forms import (
    CustomDelegateSelectWindow)
from kinder.plugins.helpers import extend_template_globals
from kinder.plugins.privilege_attributes.helpers import (
    get_privilege_confirm_attributes)
from kinder.plugins.privilege_attributes.models import (
    PrivilegeConfirmationAttributes)

from lipetsk_specifics.models import PassingSmev

from .constants import NOTIFICATION_MODE
from .constants import ReturnReasonEnum
from .models import Department
from .models import ExtendedPrivilege
from .models import ReportType


class PupilTransferListWindowExtension:
    """
    Расширяем окно списка переводов детей
    """
    @classmethod
    def build_extension(cls, list_win):
        pack = ControllerCache.find_pack(
            'lipetsk_specifics.actions.PupilTransferPrintPack')
        list_win.print_url = pack.print_action.get_absolute_url()
        list_win.template_globals = 'ui-js/pupil-transfer-list-print-window.js'
        list_win.items[0].top_bar.items.insert(
            4,
            ExtButton(
                text=u'Распечатать заявление',
                icon_cls=Icons.PRINTER,
                handler='print_transfer_info'
            )
        )
        return list_win


class DeclarationListWindowExtension:
    u"""Расширение спискового окно реестра заявлений."""

    @classmethod
    def add_passing_smev(cls, list_win):
        list_win.passing_smev_menu = ExtContextMenu()
        list_win.passing_smev_menu.add_item(
            text=u'Минуя СМЭВ (запрос)', handler='passingSmevRequest')
        list_win.passing_smev_menu.add_item(
            text=u'Минуя СМЭВ (история)', handler='passingSmevHistory')

        index = len(list_win.grid.top_bar.items) - 2
        list_win.grid.top_bar.items.insert(
            index,
            ExtToolbarMenu(text=u'Минуя СМЭВ', menu=list_win.passing_smev_menu)
        )

        template = "ui-js/declaration-list-window-extension.js"

        if hasattr(list_win, "plugins"):
            list_win.plugins.append(template)
        else:
            list_win.plugins = [template]


class DeclarationEditWindowExtension:
    """
    Расширяем окно редактирования заявки
    Добавляем в грид поле статус подтверждения льготы
    """

    @classmethod
    def build_extension(cls, edit_win):
        # не известно где восстанавливается кнопка,
        # поэтому кнопка "Распечатать заявление" пока будет отображаться
        edit_win.print_declaration_button.hidden = True
        edit_win.print_pd_confirm_button.hidden = True

        edit_win.print_declaration_with_pd_button = ext.ExtButton(
            text=u'Распечатать заявление с обработкой ПД',
            handler='function chooseDeclWithPDDelegate(){chooseDelegate('
                    '%s);}' % CustomDelegateSelectWindow.PRINT_DECL_WITH_PD,
            name='printDeclWithPDButton',
        )

        edit_win.buttons.insert(
            0, edit_win.print_declaration_with_pd_button)

        edit_win.HistoryTab_grid.template_globals = (
            'ui-js/declaration-edit-win-history-tab-extension.js')

        return edit_win

    @classmethod
    def add_print_decline(cls, win, context):
        try:
            Declaration.objects.get(
                id=context.declaration_id,
                status__code=DSS.REFUSED
            )
        except Declaration.DoesNotExist:
            return

        print_decline_button = ext.ExtButton(
            text=u'Распечатать уведомление об отказе',
            handler='''
                function () {
                    win.actionContextJson["printDecline"] = true;
                    chooseDelegate(3);
                    delete win.actionContextJson["printDecline"];
                }
            '''
        )
        win.buttons.insert(0, print_decline_button)

    @classmethod
    def history_tab_configure(cls, win, context):
        u"""Настройка вкладки "История изменений"."""
        refuse_change_data_button = ext.ExtButton(
            text=u'Распечатать отказ в изменении данных',
            handler='printRefuseToChangeData',
            icon_cls='icon-printer'
        )
        win.HistoryTab_grid.top_bar.items.append(refuse_change_data_button)

    @classmethod
    def add_passing_smev_tab(cls, win, context):
        u"""Добавляет вкладку "Минуя СМЭВ"."""
        win.passing_smev_tab = ObjectGridTab.fabricate_from_pack(
            pack_name='lipetsk_specifics/PassingSmevPack',
            pack_register=obs,
            tab_class_name='PassingSmevTab'
        )()

        win.passing_smev_tab.init_components(win)
        tab = win.passing_smev_tab._create_tab()
        win.passing_smev_tab.do_layout(win, tab)
        # Располагаем вкладку после вкладки СМЭВ
        smev_tab_index = win.tabs.index(win.smev_tab)
        win._tab_container.items.insert(smev_tab_index + 1, tab)

        win.passing_smev_tab.set_params(win, None)


class DeclarationPrivilegeAddEditWindowExtension:
    """
    Расширяем окно редактирования льготы
    Добавляем принадлежность льготы
    Добавляем владельца льготы
    Добавляем статус подтверждения льготы
    Добавляем кнопку подтверждения льготы
    Убираем поля документа
    """

    additional_privilege_attributes_fields = (
        'military_document',
        'personal_number',
        'dismissal_date',
        'military_unit',
        'name_of_unit',
        'force_kind',
        'document',
        'rank',
        'ovd'
    )

    @classmethod
    def bind_additional_fields(cls, win, instance):
        for field_name in cls.additional_privilege_attributes_fields:
            field = getattr(win, 'field__{}'.format(field_name))
            field.value = getattr(instance, field_name)

    @classmethod
    def build_extension(cls, add_edit_win, action, context):
        win = add_edit_win

        extend_template_globals(win, 'ui-js/privileges-edit-window.js')

        pack = ControllerCache.find_pack(
            'lipetsk_specifics.actions.PrivilegeConfirmationAttributesPack')

        win.form.items.remove(win.field__doc_type_id)
        win.form.items.remove(win.field__doc_series)
        win.form.items.remove(win.field__doc_number)

        win.confirm_privilege_button = ext.ExtButton(
            text=u"Просмотр/изменение данных",
            handler='privilegeConfirmation',
            icon_cls=Icons.ACCEPT,
            disabled=True)

        win.get_report_type_url = pack.get_report_type_action.absolute_url()
        model_fields_to_controls(PrivilegeConfirmationAttributes, win, (
                cls.additional_privilege_attributes_fields
            ), anchor='100%', hidden=True)

        # Поля для отображения исходя из типа отчета в льготе
        win.privilege_report_type_fields = json.dumps({
            ReportType.SECOND: (
                win.field__name_of_unit.client_id,
                win.field__rank.client_id
            ),
            ReportType.THIRD: (
                win.field__ovd.client_id,
                win.field__rank.client_id
            ),
            ReportType.FOURTH: (
                win.field__personal_number.client_id,
                win.field__force_kind.client_id,
                win.field__military_unit.client_id,
                win.field__dismissal_date.client_id,
                win.field__document.client_id,
                win.field__military_document.client_id,
                win.field__name_of_unit.client_id
            )
        })

        # Убираем поле статуса льготы, чтобы вставить его в конец
        win.form.items.remove(win.privilege_confirmation_status)
        win.form.items.extend([
            win.field__personal_number,
            win.field__rank,
            win.field__force_kind,
            win.field__military_unit,
            win.field__dismissal_date,
            win.field__document,
            win.field__military_document,
            win.field__name_of_unit,
            win.field__ovd,
            win.privilege_confirmation_status,
        ])

        win.buttons.insert(0, win.confirm_privilege_button)

        if context.decl_privilege_id:
            win.privilege_confirmation_url = (
                pack.edit_window_action.get_absolute_url())

            declaration_privilege = action.parent.get_row(
                context.decl_privilege_id)

            extended_privilege = ExtendedPrivilege.objects.filter(
                privilege_id=declaration_privilege.privilege_id).first()
            win.privilege_report_type = extended_privilege.report_type if (
                extended_privilege) else None

            attributes = get_privilege_confirm_attributes(
                declaration_privilege)
            if attributes:
                owner = attributes.privilege_owner
                cls.bind_additional_fields(win, attributes)
            else:
                owner = None

            win.confirm_privilege_button.disabled = False if owner else True
        else:
            win.privilege_confirmation_url = (
                pack.new_window_action.get_absolute_url())

        return win


class PrivilegeEditWinExtender(BaseEditWinExtender):
    u"""Класс добавления доп. полей в окно добавления/редактирования льготы."""

    model = ExtendedPrivilege
    model_fields = ('name_to_query_at_depart', 'report_type')

    def _extend_edit_win(self):
        u"""Добавляет доп. поля в форму добавления/редактирования льготы.

        Поля:
            - Наименования для запроса в ведомства
            - Тип отчета
        """
        self._win.name_to_query_at_depart = ext.ExtStringField(
            label=u'Наименования для запроса в ведомства',
            name='name_to_query_at_depart',
            max_length=500,
            anchor='100%'
        )
        self._win.report_type = make_combo_box(
            name='report_type',
            allow_blank=False,
            anchor='100%',
            label=u'Тип отчета',
            data=ReportType.get_choices(),
        )
        self._win.report_type.list_tpl = (
            '<tpl for=".">'
            '<div class="x-combo-list-item" style="white-space: normal;">'
            '{name}</div></tpl>')

        self._win.form.items.extend([
            self._win.name_to_query_at_depart,
            self._win.report_type
        ])


class PrivilegeEditWindowExtension:
    """
    Расширяем окно редактирования льготы
    Добавляем поле "Ведомство" для льготы,
    простовляем текущее значение департамента
    """

    @classmethod
    def build_extension(cls, edit_win):

        edit_win.department = ExtDictSelectField(
            region='north',
            anchor='100%',
            label=u'Ведомство',
            name='department_id',
            display_field='name',
            ask_before_deleting=False,
            hide_edit_trigger=True,
            hide_dict_select_trigger=True,
            hide_trigger=False,
        )
        department_pack = ControllerCache.find_pack(
            'lipetsk_specifics.actions.DepartmentPack')
        edit_win.department.pack = department_pack.__class__
        edit_win.department.editable = False
        edit_win.form.items.append(edit_win.department)

        return edit_win

    @classmethod
    def set_value(cls, edit_win, action, context):
        priv_pack = action.parent
        priv_id = getattr(context, priv_pack.id_param_name)
        # должна быть всегда 1 запись,тк одна льгота принадлежит одному
        # вед-ву, поменять потом на get
        dep_qs = Department.objects.filter(privileges=priv_id)
        if dep_qs:
            edit_win.department.set_value_from_model(dep_qs[0])
        return edit_win


class PrintDeclNotificationWindowExtension:
    """
    Окно уведомления для заявлений в статусе Желает изменить ДОО
    """

    @staticmethod
    def field_by_mode(mode):
        if mode == NOTIFICATION_MODE['WANT_CHANGE_DOU']:
            return (ControllerCache.find_action(
                'lipetsk_specifics.actions.'
                'ReturnNotificationAction').absolute_url(),
                ui_helpers.make_combo_box(
                    data=list(ReturnReasonEnum.get_choices()),
                    label=u'Причины возврата в очередь',
                    name='return_reason', allow_blank=False,
                    width=380))
        elif mode == NOTIFICATION_MODE['REJECT']:
            return (ControllerCache.find_action(
                'lipetsk_specifics.actions.'
                'RejectNotificationAction').absolute_url(),
                    None)
        else:
            return ControllerCache.find_action(
                'lipetsk_specifics.actions.'
                'PrintNotificationAction').absolute_url(), None

    @classmethod
    def build_extension(cls, win, notification_mode):
        url, addition_field = cls.field_by_mode(notification_mode)
        if addition_field:
            win.form.items.insert(1, addition_field)
        win.form.url = url
        return win

    @classmethod
    def change_form_url(cls, win):
        win.form.url = ControllerCache.find_action(
            'lipetsk_specifics.actions.PrintDeclineAction'
        ).absolute_url()
        return win


class BaseReasonWindow(BaseEditWindow):
    u"""Базовое окно выбора представителя ребенка и основания/причины и др."""

    def _init_components(self):
        super(BaseReasonWindow, self)._init_components()

        self.field_delegate = ext.ExtComboBox(
            label=u'Представитель',
            name='delegate_id',
            display_field='fullname',
            value_field='id',
            editable=False,
            trigger_action_all=True,
            allow_blank=False,
            anchor='100%',
        )

        self.field_reason = ext.ExtStringField(
            label=u'Основание',
            name='reason',
            max_length=100,
            allow_blank=False,
            anchor='100%',
        )

    def _do_layout(self):
        super(BaseReasonWindow, self)._do_layout()

        self.form.items.extend([
            self.field_delegate,
            self.field_reason,
        ])

    def set_params(self, params):
        params['title'] = u'Параметры'
        params['height'] = 150

        self.field_delegate.set_store(
            ext.ExtDataStore(params['delegates'])
        )

        super(BaseReasonWindow, self).set_params(params)


class ChangeReasonWindow(BaseReasonWindow):
    u"""Окно выбора представителя ребенка и основания на внесение изменений."""

    def set_params(self, params):
        params['form_url'] = ControllerCache.find_action(
            'lipetsk_specifics.actions.PrintChangeNotifyAction').absolute_url()

        self.action_context = ActionContext(
            declaration_id=params['declaration_id'],
            changes=json.dumps(params['changes']),
        )

        super(ChangeReasonWindow, self).set_params(params)


class RefuseReasonWindow(BaseReasonWindow):
    u"""Окно выбора представителя ребенка и указания причины отказа."""

    def set_params(self, params):
        params['form_url'] = ControllerCache.find_action(
            'lipetsk_specifics.actions.PrintRefuseToChangeDataAction'
        ).absolute_url()

        self.field_reason.label = u'Причины отказа'

        super(RefuseReasonWindow, self).set_params(params)


class PassingSmevListWindow(BaseListWindow):
    u"""Списковое окно реестра запросов в не электронные сервисы."""

    def _do_layout(self):
        super(PassingSmevListWindow, self)._do_layout()
        self.grid.top_bar.button_edit.text = u'Добавить ответ'


class AddResponseWindow(ModelEditWindow):
    u"""Окно добавления ответа к запросу в не электронные сервисы."""

    model = PassingSmev

    field_fabric_params = {
        'field_list': [
            'request', 'result'
        ],
        'model_register': obs,
    }

    def set_params(self, params):
        super(AddResponseWindow, self).set_params(params)
        possible_file_extensions = (
            'doc', 'docx', 'xls', 'xlsx', 'csv', 'pdf', 'jpg',  'jpeg')

        self.field__request.possible_file_extensions = possible_file_extensions
        self.field__result.possible_file_extensions = possible_file_extensions

        self.field__result.label = u'Ответ'

        self.template_globals = 'ui-js/add-response-edit-window.js'
