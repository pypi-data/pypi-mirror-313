from collections import defaultdict
from datetime import datetime
import os

from django.core.files.base import File
from django.db.models import Count
from django.utils.safestring import mark_safe
from kinder.controllers import log_to_journal
from kinder.controllers import obs
from kinder.core.children.actions import DelegateForDeclarationPack
from kinder.core.children.models import ChildrenDelegate
from kinder.core.children.models import Delegate
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import DeclarationPrivilege
from kinder.core.dict.actions import NameFieldDuplicateCheckClass
from kinder.core.pupil_transfer.models import PupilTransfer
from kinder.core.queue_module.api import prepare_notify_print_context
from kinder.core.unit.models import Unit
from kinder.plugins.privilege_attributes.helpers import (
    get_privilege_confirm_attributes)
from kinder.plugins.privilege_attributes.models import (
    PrivilegeOwnerEnum as POE)
from kinder.plugins.privilege_attributes.models import (
    PrivilegeConfirmationAttributes)
from kinder.plugins.privilege_attributes.constants import (
    PRIVILEGE_CONFIRMATION_STATUSES_MAP as PCS)
from m3 import date2str
from m3 import RelatedError
from m3.actions import Action
from m3.actions import ApplicationLogicException
from m3.actions import ControllerCache
from m3.actions import OperationResult
from m3.actions import PreJsonResult
from m3_ext.ui import all_components as ext
from objectpack.actions import BaseAction
from objectpack.actions import BaseWindowAction
from objectpack.actions import ObjectEditWindowAction
from objectpack.actions import ObjectListWindowAction
from objectpack.actions import ObjectPack
from objectpack.actions import ObjectSaveAction
from objectpack.slave_object_pack.actions import SlavePack
from objectpack.ui import ModelEditWindow
from objectpack.ui import model_fields_to_controls

from lipetsk_specifics.forms import AddResponseWindow
from lipetsk_specifics.forms import PassingSmevListWindow
from lipetsk_specifics.forms import RefuseReasonWindow
from lipetsk_specifics.models import DeclarationPassingSmev
from lipetsk_specifics.models import Department
from lipetsk_specifics.models import DepartmentAttributes
from lipetsk_specifics.models import ExtendedPrivilege
from lipetsk_specifics.models import PassingSmev
from lipetsk_specifics.report import GenericPrintReport
from lipetsk_specifics.reports.passing_smev.constants import (
    builder_report_types)

from .constants import ATTRIBUTES_FIELDS_MAP
from .constants import ReturnReasonEnum
from .utils import reject_upd


class DepartmentAttributesPack(SlavePack):
    """
    Атрибуты ведомства
    """
    __PERMISSION_NS = (
        "kinder.plugins.lipetsk_specifics.actions.DepartmentAttributesPack")
    title = u'Атрибуты ведомства'
    model = DepartmentAttributes
    need_check_permission = True

    id_param_name = 'id'
    column_name_on_select = 'attribute'

    field_list = ['attribute']

    add_window = ModelEditWindow.fabricate(
        model,
        model_register=obs,
        field_list=field_list)

    parents = ['department']

    columns = [
        {
            'data_index': 'attribute',
            'header': u"Атрибут",
            'sortable': True,
        },
    ]

    def __init__(self, *args, **kwargs):
        super(DepartmentAttributesPack, self).__init__(*args, **kwargs)
        self.replace_action('list_window_action',
                            DepartmentAttributesListWindowAction())
        self.replace_action('new_window_action',
                            DepartmentAttributesNewWindowAction())

    def save_row(self, obj, create_new, request, context):
        error_text = u'Данный атрибут уже добавлен.'
        if self.model.objects.filter(
            department_id=context.department_id,
            attribute=context.attribute
        ).exists():
            raise ApplicationLogicException(error_text)

        super(DepartmentAttributesPack, self).save_row(
            obj, create_new, request, context)


class DepartmentAttributesListWindowAction(ObjectListWindowAction):
    verbose_name = u'Просмотр'


class DepartmentAttributesNewWindowAction(ObjectEditWindowAction):
    verbose_name = u'Добавление'


class DepartmentPack(NameFieldDuplicateCheckClass, ObjectPack):
    """
    Справочник "Ведомства"
    """
    __PERMISSION_NS = "kinder.plugins.lipetsk_specifics.actions.DepartmentPack"
    title = u'Справочник "Ведомства"'
    model = Department
    need_check_permission = True

    id_param_name = 'department_id'
    column_name_on_select = 'name'

    add_window = edit_window = ModelEditWindow.fabricate(
        model,
        model_register=obs)

    columns = [
        {
            'data_index': 'code',
            'header': u"Код",
            'sortable': True,
        },
        {
            'data_index': 'name',
            'header': u"Ведомство",
            'searchable': True,
            'sortable': True,
        }
    ]

    def __init__(self, *args, **kwargs):
        super(DepartmentPack, self).__init__(*args, **kwargs)
        self.replace_action('list_window_action', DepartmentListWindowAction())
        self.replace_action('new_window_action', DepartmentNewWindowAction())
        self.replace_action('edit_window_action', DepartmentEditWindowAction())

        self.sub_permissions = super(
            DepartmentPack, self
        ).sub_permissions.copy()
        self.sub_permissions[self.list_window_action.perm_code] = (
            self.list_window_action.verbose_name)
        self.sub_permissions[self.edit_window_action.perm_code] = (
            self.edit_window_action.verbose_name)

    def extend_menu(self, menu):
        return menu.SubMenu(
            u"Справочники",
            menu.Item(self.title, self.list_window_action),
            icon='menu-dicts-16',
        )


class DepartmentListWindowAction(ObjectListWindowAction):
    __PERMISSION_NS = (
        "kinder.plugins.lipetsk_specifics.actions.DepartmentListWindowAction")
    need_check_permission = True
    verbose_name = u'Просмотр'

    def configure_window(self):
        super(DepartmentListWindowAction, self).configure_window()

        if not self.parent.has_perm(
                self.request,
                self.parent.edit_window_action.perm_code):
            self.win.make_read_only()


class DepartmentNewWindowAction(ObjectEditWindowAction):
    __PERMISSION_NS = (
        "kinder.plugins.lipetsk_specifics.actions.DepartmentNewWindowAction")
    need_check_permission = True
    verbose_name = u'Редактирование'


class DepartmentEditWindowAction(DepartmentNewWindowAction):
    def create_window(self):
        super(DepartmentEditWindowAction, self).create_window()

        self.win.form.department_attributes = ext.ExtObjectGrid()
        ControllerCache.find_pack(
            'lipetsk_specifics.actions.'
            'DepartmentAttributesPack').configure_grid(
            self.win.form.department_attributes)

        self.win.width = 500
        self.win.form.department_attributes.height = 400

        self.win.form.items.append(self.win.form.department_attributes)


class PrivilegeConfirmationAttributesPack(ObjectPack):
    """
    Подтверждение льготы
    """
    __PERMISSION_NS = (
        "kinder.plugins.lipetsk_specifics.actions"
        ".PrivilegeConfirmationAttributesPack"
    )

    title = u'Подтверждение льготы'
    model = PrivilegeConfirmationAttributes
    need_check_permission = True

    id_param_name = 'decl_privilege_id'

    exclude_list = ['declaration_privilege_id',
                    'delegate_id']

    add_window = edit_window = ModelEditWindow.fabricate(
        model,
        model_register=obs,
        exclude_list=exclude_list)

    def __init__(self, *args, **kwargs):
        super(
            PrivilegeConfirmationAttributesPack, self
        ).__init__(*args, **kwargs)
        self.get_report_type_action = PrivilegeGetReportTypeAction()
        self.actions.append(self.get_report_type_action)
        self.replace_action('new_window_action',
                            PrivilegeConfirmationAttributesNewWindowAction())
        self.replace_action('edit_window_action',
                            PrivilegeConfirmationAttributesEditWindowAction())
        self.replace_action('save_action',
                            PrivilegeConfirmationAttributesSaveAction())
        self.replace_action('list_window_action',
                            PrivilegeConfirmationListWindowAction())


    def declare_context(self, action):
        context = super().declare_context(action)

        extended_context = {
            'declaration_id': {'type': int},
            'decl_privilege_id': {'type': int},
            'parent_window_id': {'type': str, 'default': ''},
            'delegate_id': {'type': int, 'default': 0},
            'privilege_owner': {'type': int, 'default': 0}
        }

        context.update(extended_context)

        return context

    def get_row(self, fake_row_id):
        try:
            declaration_privilege = DeclarationPrivilege.objects.select_related(
                'privilegeconfirmationattributes'
            ).get(id=fake_row_id)
        except DeclarationPrivilege.DoesNotExist:
            raise ApplicationLogicException(u"Выбранная льгота не найдена.")

        confirm_attributes = get_privilege_confirm_attributes(
            declaration_privilege)
        real_row_id = confirm_attributes.id if confirm_attributes else 0

        record = super().get_row(real_row_id)

        record.doc_type_id = declaration_privilege.doc_type_id
        record.doc_series = declaration_privilege.doc_series
        record.doc_number = declaration_privilege.doc_number

        return record

    def save_row(self, obj, create_new, request, context):
        obj.privilege_owner = context.privilege_owner
        obj.confirmed = True
        obj.declaration_privilege_id = context.decl_privilege_id
        obj.delegate_id = context.delegate_id or None

        obj.declaration_privilege.doc_type_id = context.doc_type_id or None
        obj.declaration_privilege.doc_series = context.doc_series
        obj.declaration_privilege.doc_number = context.doc_number

        obj.declaration_privilege.save()

        super(PrivilegeConfirmationAttributesPack, self).save_row(
            obj, create_new, request, context)


class PrivilegeGetReportTypeAction(BaseAction):

    u"""Экшен получения типа отчета у привилегии."""

    def context_declaration(self):
        return {'privilege_id': {'type': 'int'}}

    def run(self, request, context):
        privilege = ExtendedPrivilege.objects.filter(
            privilege_id=context.privilege_id).first()
        result = dict(report_type=privilege.report_type if privilege else None)
        return PreJsonResult(result)


class PrivilegeConfirmationAttributesNewWindowAction(ObjectEditWindowAction):
    verbose_name = u'Подтверждение'

    def create_window(self):
        super(PrivilegeConfirmationAttributesNewWindowAction,
              self).create_window()

        label_width = 150

        win = self.win

        win.form._items = []

        try:
            declaration_privilege = DeclarationPrivilege.objects.select_related(
                'privilegeconfirmationattributes', 'privilege',
            ).get(id=self.context.decl_privilege_id)
        except DeclarationPrivilege.DoesNotExist:
            raise ApplicationLogicException("Выбранная льгота не найдена.")

        privilege_confirm_attributes = get_privilege_confirm_attributes(
            declaration_privilege)
        department_attributes = (
            declaration_privilege.privilege.department_set.values_list(
                'departmentattributes__attribute', flat=True))

        win.documents_fieldset = ext.ExtFieldSet(
            label_width=label_width,
            anchor='100%',
            title=u"Документ, подтверждающий наличие льготы")

        win.attributes_fieldset = ext.ExtFieldSet(
            label_width=label_width,
            anchor='100%',
            style={'padding': 0},
            border=False)

        win.documents_fields = model_fields_to_controls(
            DeclarationPrivilege, win, model_register=obs,
            field_list=['doc_type_id', 'doc_series', 'doc_number'])

        if not self.win_params['create_new']:
            obj = self.win_params['object']
            win.field__doc_type_id.value = obj.doc_type_id
            win.field__doc_series.value = obj.doc_series
            win.field__doc_number.value = obj.doc_number

        win.documents_fields.extend([
            win.field__document_issued_by,
            win.field__document_date])

        for field in win.documents_fields:
            field.anchor = '100%'

        for attribute, description in ATTRIBUTES_FIELDS_MAP:
            # Если ведоство требует данный аттрибут
            if attribute in department_attributes:
                # Если fieldset
                if isinstance(description, tuple):
                    fieldset_title, fields = description
                    fieldset = ext.ExtFieldSet(
                        label_width=label_width,
                        anchor='100%',
                        title=fieldset_title)

                    # Выдергиваем все поля принадлежащие fieldset'у
                    for field in fields:
                        try:
                            fieldset_field = getattr(
                                win, 'field__{0}_{1}'.format(attribute, field))
                        # Поле не найдено, продолжаем
                        except:
                            continue
                        # Если поле существует
                        else:
                            fieldset.items.append(fieldset_field)

                    win.attributes_fieldset.items.append(fieldset)
                # Если field
                elif isinstance(description, str):
                    try:
                        field = getattr(
                            win, 'field__{0}'.format(attribute))
                    # Поле не найдено, продолжаем
                    except:
                        continue
                    # Если поле существует
                    else:
                        # Оборачиваем каждое поле fieldset'ом
                        # для исправления верстки
                        # TODO: Найти способ исправления верстки без fieldset
                        field_wrapper = ext.ExtFieldSet(
                            anchor='100%',
                            label_width=label_width,
                            style={'padding-top': 0,
                                   'padding-bottom': 0,
                                   'margin': 0},
                            border=False)

                        field_wrapper.items.append(field)
                        win.attributes_fieldset.items.append(field_wrapper)

        win.documents_fieldset.items.extend(win.documents_fields)

        fields = [
            win.documents_fieldset]

        if privilege_confirm_attributes.privilege_owner in POE.NEED_ATTRIBUTES:
            fields = [
                win.documents_fieldset,
                win.attributes_fieldset]

        win.form.items.extend(fields)


class PrivilegeConfirmationAttributesEditWindowAction(
    PrivilegeConfirmationAttributesNewWindowAction
):
    pass


class PrivilegeConfirmationAttributesSaveAction(ObjectSaveAction):

    def run(self, request, context):
        result = super(PrivilegeConfirmationAttributesSaveAction,
                       self).run(request, context)

        result.code = u"""(
        function(){
            win = Ext.getCmp('%s');
            form = win.getForm();
            form.setValues({'privilege_confirmed': '%s'});
        }()
        )""" % (context.parent_window_id,
                PCS[True])

        return result


class PupilTransferPrintPack(ObjectPack):

    def __init__(self):
        super(PupilTransferPrintPack, self).__init__()
        self.print_action = PrintAction()
        self.actions.append(self.print_action)


class PrintAction(Action):
    url = r'/transfer_print'

    def context_declaration(self):
        return {
            'transfer_id': {
                'type': int,
                'required': True
            }
        }

    def run(self, request, context):
        try:
            tr = PupilTransfer.objects.get(id=context.transfer_id)
        except PupilTransfer.DoesNotExist:
            raise ApplicationLogicException(
                u"Информация о переводе не найдена.")

        delegate_fullname = tr.children.childrendelegate_set.order_by(
            'id').values_list(
            'delegate__fullname', flat=True)[:1] or [u""]

        result = dict(boss=tr.from_unit.get_mo().boss_fio,
                      # Берем только одного родителя
                      parent=delegate_fullname[0],
                      children=tr.children.fullname,
                      birthday=tr.children.date_of_birth.strftime('%d.%m.%Y'),
                      from_dou=tr.from_unit.name,
                      to_dou=tr.to_unit.name if tr.to_unit else None,
                      create_date=tr.registered_date.strftime('%d.%m.%Y'))

        rep = GenericPrintReport(
            ['templates', 'xls/transfer_print.xls'], vars=result)
        rep.make_report()
        url = rep.get_result_url()
        return OperationResult(code="function() {location.href='%s';}" % url)


class DeclLipetskPrintNotificationPack(ObjectPack):
    """
    Переопределяем печать уведомления заявления
    """

    def __init__(self):
        super(DeclLipetskPrintNotificationPack, self).__init__()
        self.print_notification_action = PrintNotificationAction()
        self.print_decline_action = PrintDeclineAction()
        self.print_change_notification_action = PrintChangeNotifyAction()
        self.refuse_to_change_data_window_action = (
            RefuseToChangeDataWindowAction())
        self.print_refuse_to_change_data_action = (
            PrintRefuseToChangeDataAction())

        self.actions.extend([self.print_notification_action,
                             self.print_decline_action,
                             self.print_change_notification_action,
                             self.refuse_to_change_data_window_action,
                             self.print_refuse_to_change_data_action,
                             RejectNotificationAction(),
                             ReturnNotificationAction()])


class PrintNotificationAction(Action):
    u"""
    Распечатка уведомления в статусе Желает изменить ДОО
    """
    url = '/lipetsk_print-notification'

    def context_declaration(self):
        return {
            'kind': {
                'type': int,
                'required': True
            },
            'delegate_id': {
                'type': int,
                'required': True
            },
            'declaration_id': {
                'type': int,
                'required': True
            }
        }

    def update_data(self, context, variables):
        return 'xls/in_queue_notification.xls', variables

    def run(self, request, context):
        profile = request.user.get_profile()

        variables = prepare_notify_print_context(context, profile)

        decl = Declaration.objects.get(id=context.declaration_id)
        variables['mo'] = decl.mo.name
        variables['units_list'] = [
            dict(unit_num=f"{unit['num']}.", unit_name=unit['unit_name'])
            for unit in variables['units']]
        variables['user_name'] = profile.get_fio()

        template, variables = self.update_data(context, variables)

        rep = GenericPrintReport(['templates', template], vars=variables)
        rep.make_report()

        log_to_journal('print', u'печатает уведомление '
                                u'представителю (ID=%s)' %
                       context.delegate_id)

        return OperationResult(
            code="function() {location.href='%s';}" % rep.get_result_url())


class RejectNotificationAction(PrintNotificationAction):
    url = '/reject_print-notification'

    def context_declaration(self):
        context = super(RejectNotificationAction, self).context_declaration()
        return context

    def update_data(self, context, variables):
        return "xls/reject_notification.xls", reject_upd(variables, context)


class ReturnNotificationAction(PrintNotificationAction):
    url = '/return_print-notification'

    def context_declaration(self):
        context = super(ReturnNotificationAction, self).context_declaration()
        context.update(return_reason={
            'type': int,
            'required': True,
        })
        return context

    def update_data(self, context, variables):
        variables['return_reason'] = ReturnReasonEnum.values[
            context.return_reason]
        return 'xls/change_dou_notification.xls', variables


class LipetskDelegateForDeclarationPack(DelegateForDeclarationPack):

    u"""Пак для замены с целью фильтрации делегатов из доп.атрибутов льгот."""

    def get_rows_query(self, request, context):
        u"""Возвращает кверисет для всех строк."""
        q1 = super(LipetskDelegateForDeclarationPack, self).get_rows_query(
            request, context
        )

        q2_params = {
            'privilegeconfirmationattributes__declaration_privilege__'
            'declaration': context.declaration_id
        }
        q2 = Delegate.objects.filter(**q2_params).exclude(
            childrendelegate__isnull=True)

        # union-объединение двух кверисетов
        ids = list(
            q1.values_list('id', flat=True)
        ) + list(
            q2.values_list('id', flat=True)
        )

        query = Delegate.objects.filter(pk__in=set(ids))

        return query

    def delete_row(self, id_, request, context):
        """
        Переопределил метод, чтобы выкидывать исключение если есть льгота,
        потому что без этого метода, ошибка выходила, но представитель всё равно удалялся
        :param id_:
        :param request:
        :param context:
        :return:
        """
        if PrivilegeConfirmationAttributes.objects.filter(
                delegate_id=id_
        ).exists():
            raise RelatedError(
                f'Не удалось удалить элемент "{id_}", '
                f'так как на него ссылаются льготы')
        return super().delete_row(id_, request, context)

class PrintDeclineAction(Action):
    """
    Распечатка уведомления об отказе
    """
    url = '/lipetsk_print-decline'

    def context_declaration(self):
        return {
            'delegate_id': {
                'type': 'int',
                'required': True
            },
            'declaration_id': {
                'type': 'int',
                'required': True
            }
        }

    def update_data(self, context, variables):
        return 'xls/in_queue_notification.xls', variables

    def run(self, request, context):
        profile = request.user.get_profile()

        try:
            decl = Declaration.objects.get(id=context.declaration_id)
        except Declaration.DoesNotExist:
            raise ApplicationLogicException(u'Выбранная заявка не найдена')

        status = decl.declarationstatuslog_set.all().latest('datetime')

        try:
            delegate = Delegate.objects.get(id=context.delegate_id)
        except Delegate.DoesNotExist:
            raise ApplicationLogicException(
                u'Выбранный представитель не найден'
            )

        child = decl.children

        if child.date_of_birth:
            child_birthday = date2str(child.date_of_birth)
        else:
            child_birthday = u''

        variables = {
            'delegate_fio': delegate.fullname,
            'print_date': date2str(datetime.now()),
            'child_surname': child.surname,
            'child_firstname': child.firstname,
            'child_patronymic': child.patronymic,
            'child_birthday': child_birthday,
            'comment': status.comment,
            'mo_name': decl.mo.name,
            'user_name': profile.get_fio(),
        }

        units_from_decl = Unit.objects.filter(
            declarationunit__declaration=decl
        ).order_by('declarationunit__ord').values_list('name', flat=True)
        variables['units'] = u', '.join(units_from_decl)

        template = 'xls/lipetsk_decline.xls'

        rep = GenericPrintReport(['templates', template], vars=variables)
        rep.make_report()

        log_to_journal('print', u'печатает уведомление '
                                u'представителю (ID=%s)' %
                       context.delegate_id)

        return OperationResult(
            code="function() {location.href='%s';}" % rep.get_result_url())


class PrintChangeNotifyAction(BaseAction):
    """
    Экшн выдачи эксель файла с Уведомлением о внесении изменений в Заявку.
    """

    url = '/print-change-notification'

    def context_declaration(self):
        context = super(PrintChangeNotifyAction, self).context_declaration()

        context.update({
            'declaration_id': {'type': 'int'},
            'delegate_id': {'type': 'int'},
            'changes': {'type': 'json'},
            'reason': {'type': 'unicode'},
        })

        return context

    def run(self, request, context):
        declaration = Declaration.objects.get(id=context.declaration_id)

        change_notification_template = (
            'templates/xls/lipetsk_change_notification.xls'
        )
        template_path = os.path.join(
            os.path.dirname(__file__), change_notification_template
        )

        child_delegate = ChildrenDelegate.objects.get(
            delegate_id=context.delegate_id,
            children_id=declaration.children_id
        )

        declaration_units = declaration.declarationunit_set.all().order_by(
            'ord')

        privilege_data = self.privilege_data(declaration)

        desired_date = u''
        if context.changes['desired_date']:
            desired_date = datetime.strptime(
                context.changes['desired_date'], "%Y-%m-%d"
            ).date().strftime('%d.%m.%Y')

        def get_fio(person):
            """Возвращает ФИО пользователя в формате Фамилия И.О."""
            fio = person.surname + u' '
            if person.firstname:
                fio += person.firstname[0] + u'.'
            if person.patronymic:
                fio += person.patronymic[0] + u'.'
            return fio.title()

        desired_units = []
        data = context.changes['desired_unit'].split(',')
        for item in enumerate(data, start=1):
            desired_units.append(dict(unit=item[1], num=item[0]))

        variables = {
            'mo_name': declaration.mo.name,
            'director_fio': declaration.mo.boss_fio,
            'delegate_fio': child_delegate.delegate.full_name(),
            'declarant_fio': get_fio(child_delegate.delegate),
            'fio': context.changes['fullname']
                if context.changes['fullname']
                else declaration.children.fullname,
            'declaration_units': u', '.join(
                declaration_units.values_list('unit__name', flat=True)),
            'date_of_birth': (
                declaration.children.date_of_birth.strftime('%d.%m.%Y')
            ),
            'reason': context.reason,
            'date': datetime.now().strftime('%d.%m.%Y'),
            'user_fio': request.user.get_profile().get_fio(),
            'desired_units': desired_units,
            'desired_date': desired_date,
            'fullname': declaration.children.fullname
                if context.changes['fullname'] else u'',
            'address': context.changes['address'],
            'reg_address': context.changes['reg_address'],
            'phone': context.changes['phone'],
            'email': context.changes['email'],
            'privileges': context.changes['privileges'],
            'privilege_name': privilege_data['privilege_name'],
            'owner_fio': privilege_data['owner_fio'],
            'owner_date_of_birth': privilege_data['owner_date_of_birth'],
            'owner_snils': privilege_data['owner_snils'],
        }

        rep = GenericPrintReport(template_path, variables)
        rep.make_report()

        return OperationResult(
            code='function() {{location.href="{0}";}}'.format(rep.result_url)
        )

    def privilege_data(self, declaration):
        u"""Возвращает словарь со сведениями о правообладателе льготы.

        :param declaration: Заявление
        :type declaration: kinder.core.declaration.models.Declaration
        """
        data = {
            'privilege_name': '',
            'owner_fio': '',
            'owner_date_of_birth': '',
            'owner_snils': '',
        }
        declaration_privilege = declaration.declarationprivilege_set.first()
        if not declaration_privilege:
            return data

        data['privilege_name'] = declaration_privilege.privilege.name

        privilege_confirm = get_privilege_confirm_attributes(
            declaration_privilege)
        if not privilege_confirm:
            return data

        privilege_owner = privilege_confirm.privilege_owner

        if privilege_owner in POE.NEED_DELEGATE:
            delegate = privilege_confirm.delegate
            data['owner_fio'] = delegate.full_name()
            data['owner_date_of_birth'] = (
                delegate.date_of_birth.strftime('%d.%m.%Y')
                if delegate.date_of_birth else '')
            data['owner_snils'] = delegate.snils
        else:
            data['owner_fio'] = declaration.children.fullname
            data['owner_date_of_birth'] = (
                declaration.children.date_of_birth.strftime('%d.%m.%Y')
            )
            data['owner_snils'] = declaration.children.snils

        return data


class RefuseToChangeDataWindowAction(BaseWindowAction):
    u"""Экшн окна настройки печати отказа в изменении данных."""

    def context_declaration(self):
        context = super(
            RefuseToChangeDataWindowAction, self).context_declaration()

        context.update({'children_id': {'type': 'int'}})

        return context

    def create_window(self):
        self.win = RefuseReasonWindow()

    def set_window_params(self):
        delegates = ChildrenDelegate.objects.filter(
            children_id=self.context.children_id)

        if not delegates.exists():
            raise ApplicationLogicException(
                u'У ребенка отсутствует законный представитель, '
                u'необходимо внести сведения о нем'
            )

        self.win_params['delegates'] = delegates.values_list(
            'delegate__id', 'delegate__fullname')


class PrintRefuseToChangeDataAction(BaseAction):
    u"""Экшн печати отказа в изменении данных."""

    def context_declaration(self):
        context = super(
            PrintRefuseToChangeDataAction, self).context_declaration()

        context.update({
            'declaration_id': {'type': 'int'},
            'delegate_id': {'type': 'int'},
            'children_id': {'type': 'int'},
            'reason': {'type': 'unicode'},
        })

        return context

    def run(self, request, context):
        try:
            declaration = Declaration.objects.get(id=context.declaration_id)
        except Declaration.DoesNotExist:
            raise ApplicationLogicException(u'Заявление не найдено')

        try:
            child_delegate = ChildrenDelegate.objects.get(
                delegate_id=context.delegate_id,
                children_id=context.children_id
            )
        except ChildrenDelegate.DoesNotExist:
            raise ApplicationLogicException(u'Представитель не найден')

        child = child_delegate.children

        variables = {
            'delegate_fio': child_delegate.delegate.full_name(),
            'mo': declaration.mo.name,
            'reason': context.reason,
            'child_fio_and_dob': u'{fio}, {date_of_birth}'.format(
                fio=child.fullname,
                date_of_birth=child.date_of_birth.strftime('%d.%m.%Y')),
            'date': datetime.now().strftime('%d.%m.%Y'),
            'user_fio': request.user.get_profile().get_fio(),
        }

        template = 'templates/xls/refuse_to_change_data.xls'
        template_path = os.path.join( os.path.dirname(__file__), template)

        report = GenericPrintReport(template_path, variables)
        report.make_report()

        return OperationResult(
            code='function() {{location.href="{0}";}}'.format(
                report.result_url)
        )


class PassingSmevPack(ObjectPack):
    u"""Пак запросов в не электронные ведомства."""

    title = u'Минуя СМЭВ'
    model = PassingSmev
    id_param_name = 'passing_smev_id'
    list_window = PassingSmevListWindow
    edit_window = AddResponseWindow
    can_delete = False
    columns = [
        {
            'data_index': 'time',
            'header': u'Дата и время',
            'searchable': False,
            'sortable': True,
        },
        {
            'data_index': 'department',
            'header': u'Ведомство',
            'searchable': False,
            'sortable': True,
        },
        {
            'data_index': 'request_safe_link',
            'header': u'Запрос',
            'searchable': False,
            'sortable': False,
        },
        {
            'data_index': 'result_safe_link',
            'header': u'Результат',
            'searchable': False,
            'sortable': False,
        },
        {
            'data_index': 'profile',
            'header': u'Пользователь',
            'searchable': False,
            'sortable': False,
        }
    ]

    def __init__(self):
        super(PassingSmevPack, self).__init__()
        self.request_action = PassingSmevRequestAction()
        self.actions.append(self.request_action)

    def prepare_row(self, obj, request, context):
        obj = super(PassingSmevPack, self).prepare_row(obj, request, context)
        obj.request_safe_link = mark_safe(obj.request_link or u'')
        obj.result_safe_link = mark_safe(obj.result_link or u'')
        return obj

    def declare_context(self, action):
        result = super(PassingSmevPack, self).declare_context(action)
        result['declaration_id'] = {'type': 'int_or_none', 'default': None}
        return result

    def get_rows_query(self, request, context):
        query = super(PassingSmevPack, self).get_rows_query(request, context)
        if context.declaration_id:
            query = query.filter(
                declarationpassingsmev__declaration_id=context.declaration_id)
        return query


class PassingSmevRequestAction(BaseAction):

    u"""Экшен минуя СМЭВ (запрос)."""

    def context_declaration(self):
        return {'declaration_ids': {'type': 'int_list'}}

    def create_passing_smev(self, profile, declaration_ids, department_id,
                            report_name, report_type):
        u"""Создает запросы."""

        if report_type not in builder_report_types:
            return

        reporter_cls = builder_report_types.get(report_type)
        reporter = reporter_cls({
            'declaration_ids': declaration_ids,
            'report_name': report_name
        }, {})
        reporter.make_report()

        request_file = open(reporter.out_file_path, 'rb')
        request_django_file = File(request_file)

        passing_smev = PassingSmev.objects.create(
            department_id=department_id,
            profile=profile,
            request=request_django_file
        )
        for declaration_id in declaration_ids:
            DeclarationPassingSmev.objects.create(
                declaration_id=declaration_id,
                passing_smev=passing_smev
            )

    def run(self, request, context):
        declarations = Declaration.objects.filter(
            pk__in=context.declaration_ids)

        # Заявления у которых в льготах не указан обладатель.
        declaration_privilege_without_delegate = declarations.filter(**{
            'declarationprivilege__privilegeconfirmationattributes__delegate'
            '__isnull': True
        })
        if declaration_privilege_without_delegate.exists():
            raise ApplicationLogicException(
                u'У {} не выбран обладатель льготы.'.format(u', '.join(
                    declaration_privilege_without_delegate.values_list(
                        'children__fullname', flat=True
                    ))
                ))

        # Заявления с более чем одной льготой
        declaration_with_several_privileges = declarations.values_list(
            'pk'
        ).annotate(cnt=Count('declarationprivilege')).filter(cnt__gt=1)
        if declaration_with_several_privileges.exists():
            raise ApplicationLogicException(
                u'Для создания отчета, необходимо, выбрать одну льготу.')

        # Создаем расширяющие записи привилегии, если их нет
        for privilege_id in declarations.values_list(
            'declarationprivilege__privilege', flat=True
        ).distinct():
            ExtendedPrivilege.objects.get_or_create(privilege_id=privilege_id)

        privilege_declarations = defaultdict(list)
        privilege_lookup = 'declarationprivilege__privilege'
        extended_lookup = '{}__extendedprivilege'.format(privilege_lookup)

        for dep_id, p_name, name, r_type, pk in declarations.values_list(
            '{}__department__id'.format(privilege_lookup),
            '{}__name'.format(privilege_lookup),
            '{}__name_to_query_at_depart'.format(extended_lookup),
            '{}__report_type'.format(extended_lookup),
            'pk'
        ):
            if not dep_id:
                raise ApplicationLogicException(
                    u'У льготы "{}" не выбрано ведомство.'.format(p_name))
            privilege_declarations[dep_id, r_type, name].append(pk)

        for (department_id, report_type, name), declaration_ids in (
            list(privilege_declarations.items())
        ):
            self.create_passing_smev(
                request.user.get_profile(),
                declaration_ids,
                department_id,
                name,
                report_type
            )

        return OperationResult(message=u'Запросы успешно сформированы')


class PrivilegeConfirmationListWindowAction(ObjectListWindowAction):
    """
    Переопределили для задания verbose_name
    """
    verbose_name = 'Просмотр'
