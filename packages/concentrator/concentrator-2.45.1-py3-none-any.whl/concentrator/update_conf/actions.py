# coding: utf-8

from django.db import IntegrityError
from kinder.core.audit_log_kndg.helpers import get_field
from kinder.core.audit_log_kndg.helpers import get_model
from m3.actions import ApplicationLogicException
from objectpack.actions import ObjectListWindowAction
from objectpack.actions import ObjectPack
from objectpack.actions import ObjectRowsAction

from . import forms
from ..models import UpdateParams


class UpdateConfigRowsAction(ObjectRowsAction):
    """
    Экшн получения данных для отображения в окне справочника
    Параметры для изменений данных через ЕПГУ
    """

    def run(self, request, context):
        """
        Переопределили для корректного расчета количества возвращаемых строк
        """
        
        result = super(UpdateConfigRowsAction, self).run(request, context)
        result.data['total'] = len(result.data['rows'])
        return result


class UpdateConfigPack(ObjectPack):
    __PERMISSION_NS = (
        "kinder.plugins.concentrator.update_conf.actions.UpdateConfigPack")
    title = u'Параметры для изменения данных через ЕПГУ'
    model = UpdateParams
    edit_window = add_window = forms.EditWindow
    need_check_permission = True

    columns = [
        {
            'header': u'Наименование модели',
            'data_index': 'model_name',
            'sortable': True,
        },
        {
            'header': u'Наименование поля',
            'data_index': 'field_name',
            'width': 50,
        },

    ]

    def __init__(self):
        super(UpdateConfigPack, self).__init__()
        self.replace_action(
            'list_window_action', UpdateConfigListWindowAction())
        self.replace_action(
            'rows_action', UpdateConfigRowsAction())
        self.sub_permissions = super(
            UpdateConfigPack, self
        ).sub_permissions.copy()
        self.sub_permissions[self.list_window_action.perm_code] = (
            self.list_window_action.verbose_name)

    def prepare_row(self, obj, request, context):
        """
        Подменяем на verbose_name
        @param obj:
        @param request:
        @param context:
        @return:
        """
        obj = super(
            UpdateConfigPack, self
        ).prepare_row(obj, request, context)
        model_cls = get_model(obj.model_name)

        if not model_cls:
            return None

        if hasattr(model_cls._meta, 'verbose_name'):
            obj.model_name = get_model(obj.model_name)._meta.verbose_name

        field = get_field(model_cls, obj.field_name)
        if field and hasattr(field, 'verbose_name'):
            obj.field_name = field.verbose_name
        return obj

    def save_row(self, obj, create_new, request, context):
        try:
            obj.clean()
            super(
                UpdateConfigPack, self
            ).save_row(obj, create_new, request, context)
        except IntegrityError:
            raise ApplicationLogicException(
                u'Поле для данной модели уже добавлено в справочник.')

    def extend_menu(self, desk):
        return desk.SubMenu(
            u'Справочники',
            desk.Item(name=self.title, pack=self.list_window_action),
            icon='menu-dicts-16',
        )


class UpdateConfigListWindowAction(ObjectListWindowAction):
    __PERMISSION_NS = (
        "kinder.plugins.concentrator.update_conf.actions"
        ".UpdateConfigListWindowAction")

    need_check_permission = True
    verbose_name = u'Просмотр и редактирование'
