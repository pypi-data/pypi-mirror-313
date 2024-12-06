import datetime
import os

from django.conf import settings
from educommon.m3 import extensions
from kinder.controllers import obs
from kinder.core.children.models import ChildrenDelegate
from kinder.core.declaration.declaration_history.models import (
    DeclarationHistory)
from kinder.core.declaration.declaration_history.enum import ActionEnum
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import DeclarationPrivilege
from kinder.core.declaration_status.models import DSS
from kinder.core.helpers import extract_date
from kinder.plugins.privilege_attributes.helpers import (
    get_privilege_confirm_attributes)
from kinder.plugins.privilege_attributes.models import (
    PrivilegeConfirmationAttributes)
from kinder.plugins.privilege_attributes.constants import (
    PRIVILEGE_CONFIRMATION_STATUSES_MAP as PCS)
from kinder.urls import dict_controller
from m3 import date2str
from m3.actions import OperationResult

from concentrator.change import ChildrenChangeHelper
from concentrator.change import DelegateChangeHelper
from concentrator.change import StorageHelper
from concentrator.changes.rules import display_changes_map
from concentrator.models import ChangeDeclaration
from lipetsk_specifics.actions import DeclLipetskPrintNotificationPack
from lipetsk_specifics.actions import DepartmentAttributesPack
from lipetsk_specifics.actions import DepartmentPack
from lipetsk_specifics.actions import LipetskDelegateForDeclarationPack
from lipetsk_specifics.actions import PassingSmevPack
from lipetsk_specifics.actions import PrivilegeConfirmationAttributesPack
from lipetsk_specifics.actions import PupilTransferPrintPack
from lipetsk_specifics.changes.actions import LipetskChangesDetailPack
from lipetsk_specifics.changes.actions import LipetskChangesPack
from lipetsk_specifics.forms import ChangeReasonWindow
from lipetsk_specifics.forms import DeclarationEditWindowExtension
from lipetsk_specifics.forms import DeclarationListWindowExtension
from lipetsk_specifics.forms import DeclarationPrivilegeAddEditWindowExtension
from lipetsk_specifics.forms import PrintDeclNotificationWindowExtension
from lipetsk_specifics.forms import PrivilegeEditWindowExtension
from lipetsk_specifics.forms import PupilTransferListWindowExtension
from lipetsk_specifics.models import Department
from lipetsk_specifics.tasks import ChangeInDeclarationPushTask

from .change import DeclarationChangeHelper
from .change import DeclarationUnitChangeHelper
from .change import LipetskDeclarationPrivilegeChangeHelper
from .change import PrivConfAttrsChangeHelper
from .constants import NOTIFICATION_MODE
from .forms import PrivilegeEditWinExtender


def register_actions():
    dict_controller.packs.extend([
        DepartmentAttributesPack(),
        DepartmentPack(),
        PrivilegeConfirmationAttributesPack(),
        PupilTransferPrintPack(),
        DeclLipetskPrintNotificationPack(),
        PassingSmevPack(),
    ])

    register_change_handlers()


def register_change_handlers():
    """Свои обработчики изменений."""
    StorageHelper.register_change_helper(
        'Declaration', DeclarationChangeHelper)
    StorageHelper.register_change_helper(
        'DeclarationUnit', DeclarationUnitChangeHelper)

    # расширение обработчиков изменений
    StorageHelper.register_change_helper(
        'DeclarationPrivilege', LipetskDeclarationPrivilegeChangeHelper)
    StorageHelper.register_change_helper(
        'PrivilegeConfirmationAttributes', PrivConfAttrsChangeHelper)
    StorageHelper.register_change_helper('Delegate', DelegateChangeHelper)
    StorageHelper.register_change_helper('Children', ChildrenChangeHelper)

    # расширение функций отображения изменений
    display_changes_map.set(
        'PrivilegeConfirmationAttributes', _get_priv_conf_attr)


def _get_priv_conf_attr(change):
    """В липецке льгота всегда одна,поэтому и атрибуты подверждения будут в 1
    экземпляре, либо не будут вообще
    """
    return PrivilegeConfirmationAttributes.objects.filter(
        declaration_privilege__in=(
            display_changes_map.declarationprivilege(change).all())
    ).first()


@obs.subscribe
class DeclarationListWindowListener:
    """Листенер настройки спискового окна реестра заявлений."""

    listen = [
        'kinder.core.queue_module.declaration/'
        'QueueDeclarationPack/QueueDeclaratonListWindowAction'
    ]

    def configure_list_window(self, params):
        win = params['win']
        context = params['context']

        if settings.USE_DECL_SMEV_TAB:
            DeclarationListWindowExtension.add_passing_smev(win)

        return params


@obs.subscribe
class DeclarationEditWindowListener:
    """Листенер настройки окна редактирования заявления."""

    listen = [
        'kinder.core.queue_module.declaration/'
        'QueueDeclarationPack/QueueDeclarationEditAction'
    ]

    def configure_edit_window(self, params):
        win = params['win']
        context = params['context']

        DeclarationEditWindowExtension.build_extension(win)

        DeclarationEditWindowExtension.add_print_decline(win, context)
        DeclarationEditWindowExtension.history_tab_configure(win, context)
        if settings.USE_DECL_SMEV_TAB:
            DeclarationEditWindowExtension.add_passing_smev_tab(win, context)

        return params


@obs.subscribe
class MakeObjectRowsActionExtension:
    """
    Перехватываем rows action. Добавляем статус подтверждения льготы
    """

    listen = [
        'kinder.core.declaration.declaration_privilege/'
        'DeclarationPrivilegePack/ObjectRowsAction'
    ]

    def get_rows(self, res):
        for row in res:
            declaration_privilege = self.action.parent.get_row(row['id'])
            confirmed = PrivilegeConfirmationAttributes.objects.filter(
                declaration_privilege=declaration_privilege,
                confirmed=True,
            ).exists()
            row['status'] = PCS[confirmed]

        return res


@obs.subscribe
class MakeObjectSaveActionExtension:
    """
    Перехватываем save action для возврата id записи
    """

    listen = [
        'kinder.core.declaration.declaration_privilege/'
        'DeclarationPrivilegePack/DeclarationPrivilegeSaveAction',
    ]
    # Позже чем kinder.plugins.privilege_attributes.listeners.
    # DeclarationPrivilegeSaveActionListener
    priority = 50

    def bind_additional_fields(self, context, instance):
        win = DeclarationPrivilegeAddEditWindowExtension
        for field_name in win.additional_privilege_attributes_fields:
            value = getattr(context, field_name)
            if value:
                setattr(instance, field_name, value)

    # Перехватываем для восстановления полей doc_* т.к. поля на другой форме
    # И для определения изменения льготы
    def save_object(self, obj):
        if obj.id:
            try:
                orig_obj = DeclarationPrivilege.objects.get(id=obj.id)
            except DeclarationPrivilege.DoesNotExist:
                pass
            else:
                obj.doc_type_id = orig_obj.doc_type_id
                obj.doc_series = orig_obj.doc_series
                obj.doc_number = orig_obj.doc_number

        return obj

    def after(self, request, context, result):
        try:
            declaration_privilege = (
                DeclarationPrivilege.objects.select_related(
                    'privilegeconfirmationattributes'
                ).get(
                    declaration_id=context.declaration_id,
                    privilege_id=context.privilege_id))
        except DeclarationPrivilege.DoesNotExist:
            return

        confirmation = get_privilege_confirm_attributes(declaration_privilege)
        if not confirmation:
            confirmation = PrivilegeConfirmationAttributes(
                declaration_privilege=declaration_privilege)

        if getattr(context, 'dismissal_date'):
            context.dismissal_date = extract_date(
                request, 'dismissal_date')
        self.bind_additional_fields(context, confirmation)
        confirmation.save()

        if context.privilege_confirmation == 'true':
            result.code = f"""(
            function(){{
                win = Ext.getCmp('{context.m3_window_id}');
                context = win.actionContextJson;
                context.decl_privilege_id = {declaration_privilege.id};
                context.privilege_confirmation = false;
                context.privilege_owner = {context.privilege_owner};
            }}()
            )"""


@obs.subscribe
class AddDepartment:
    """
    Добавляем поле "Ведомство" для льготы
    """

    listen = [
        'kinder.core.privilege/'
        'PrivilegeDictPack/ObjectEditWindowAction',
    ]

    def create_window(self, win):
        return PrivilegeEditWindowExtension.build_extension(win)

    def after(self, request, context, result):
        result.data = PrivilegeEditWindowExtension.set_value(
            result.data, self.action, context)


@obs.subscribe
class MakeDictSaveActionExtension:
    """
    Перехватываем экшн сохранения льготы
    Добавляем привязку льготы к ведомству
    """

    listen = [
        'kinder.core.privilege/'
        'PrivilegeDictPack/ObjectSaveAction'
    ]

    def after(self, request, context, result):
        # TODO: Тут всегда пересохранется привязка ведомства к льготе,
        #  надо исправить и реализовать отображение привязок
        priv_pack = self.action.parent

        privilege_id = getattr(context, priv_pack.id_param_name)
        department_id = getattr(context, DepartmentPack.id_param_name, None)

        if privilege_id:
            privilege = self.action.parent.get_row(privilege_id)
            privilege.department_set.clear()

            if department_id:
                try:
                    department = Department.objects.get(id=department_id)
                except Department.DoesNotExist:
                    pass
                else:
                    privilege.department_set.add(department)


@obs.subscribe
class AddPrivilegeConfirmationButton:
    """
    Добавляем статус подтверждения льготы
    Добавляем кнопку подтверждения льготы
    Убираем поля документа
    """

    listen = [
        'kinder.core.declaration.declaration_privilege/'
        'DeclarationPrivilegePack/ObjectEditWindowAction',
        'kinder.core.declaration.declaration_privilege/'
        'DeclarationPrivilegePack/ObjectAddWindowAction'
    ]
    # Ставим больше, чем в плагине подтверждения льгот (позже него)
    # kinder.plugins.privilege_attributes.listeners.
    # AddPrivilegeConfirmationButton
    priority = 50

    def after(self, request, context, result):
        result.data = DeclarationPrivilegeAddEditWindowExtension.build_extension(
            result.data, self.action, context)


@obs.subscribe
class PrintPupilTransferExtension:
    """
    Кнопка печати информации о переводе ребенка
    """

    listen = [
        'kinder.core.pupil_transfer/PupilTransferPack'
        '/PupilTransferListWindowAction'
    ]

    def after(self, request, context, result):
        result.data = PupilTransferListWindowExtension.build_extension(
            result.data)


@obs.subscribe
class PrintDeclNotificationExtension:
    """
    Перехватываем печать уведомления для заявлений
    """

    listen = [
        'kinder.core.queue_module.declaration'
        '/QueueDeclarationPack/QueueDeclDelegateChoiceAction'
    ]

    @staticmethod
    def get_notification_mode(status_code):
        if status_code == DSS.WANT_CHANGE_DOU:
            return NOTIFICATION_MODE['WANT_CHANGE_DOU']
        elif status_code in [DSS.REGISTERED, DSS.PRIV_CONFIRMATING]:
            return NOTIFICATION_MODE['IN_QUEUE']
        elif status_code == DSS.REFUSED:
            return NOTIFICATION_MODE['REJECT']
        return None

    def after(self, request, context, result):

        try:
            declaration_status_code = (
                Declaration.objects.values_list(
                    'status__code', flat=True).get(id=context.declaration_id))
        except Declaration.DoesNotExist:
            return

        if (
                result.data and
                context.kind == result.data.PRINT_NOTIFICATION and
                self.get_notification_mode(declaration_status_code)
        ):
            if getattr(context, 'printDecline', None):
                result.data = (
                    PrintDeclNotificationWindowExtension.change_form_url(
                        result.data))
            else:
                result.data = (
                    PrintDeclNotificationWindowExtension.build_extension(
                        result.data,
                        self.get_notification_mode(declaration_status_code)))


@obs.subscribe
class AddStatusForNotificationExtension:
    """
    Добавляем кнопку об уведомления в окно заявки в статусе отказано
    """

    listen = [
        'kinder.core.queue_module.declaration'
        '/QueueDeclarationPack/QueueDeclarationEditAction'
    ]

    def additional_statuses(self, statuses):
        return statuses + (DSS.REFUSED,)


@obs.subscribe
class PupilDeclarationExtension:
    """
    История о том как Липецк печать заявления переопределял
    """
    listen = [
        'kinder.core.declaration/DeclarationPackPreview/DeclPrintAction',
        'kinder.core.declaration/DeclarationPack/DeclPrintAction'
    ]

    def additional_param(self, data):

        def get_priv_info(delegate):
            psa = PrivilegeConfirmationAttributes.objects.filter(
                delegate=delegate).first()
            if not psa:
                return dict(
                    priv_owner='',
                    priv_owner_info='',
                )
            owner_info = ''
            priv_owner_info = dict(
                document_issued_by=(
                    'Кем выдан: ', psa.document_issued_by),
                document_date=('Когда выдан', psa.document_date),
                personal_number=(u'Личный номер', psa.personal_number),
                force_kind=('Вид войск', psa.force_kind),
                military_unit=(
                    'Воинская часть (Подразделение)', psa.military_unit),
                dismissal_date=('Дата увольнения', psa.dismissal_date),
                rank=('Звание', psa.rank),
            )
            for key, value in priv_owner_info.items():
                if value[1]:
                    owner_info += '%s: %s\n' % (value[0], value[1])

            return dict(
                priv_owner=delegate.fullname,
                priv_owner_info=owner_info,
            )

        ext_dict = dict(
            zags_number=data['child'].zags_act_number,
            zags_date=data['child'].zags_act_date.strftime('%d.%m.%Y') if
            data['child'].zags_act_date else '',
            zags_place=data['child'].zags_act_place,
            reg_address_full=data['child'].reg_address_full,
            delegate_address=data['delegate'].address_full,
            priv_owner=get_priv_info(data['delegate'])['priv_owner'],
            priv_owner_info=get_priv_info(data['delegate'])['priv_owner_info'],
            current_date=datetime.date.today().strftime('%d.%m.%Y'),
        )
        data['variables'].update(ext_dict)
        return data

    def get_template(self, *args, **kwargs):
        template_name = 'templates/xls/declaration_info_lipetsk.xls'
        template_url = os.path.join(os.path.dirname(__file__), template_name)
        return template_url

    def get_html_template(self, *args, **kwargs):
        return os.path.join(os.path.dirname(__file__),
                            'templates/html/declaration_info_lipetsk.html')

@obs.subscribe
class AfterChangeReject:

    listen = [
        'concentrator.changes/ChangesDetailPack/ChangesRejectAction'
    ]

    def after(self, request, context, result):

        # TODO Переделать, передавать идентификатор заявления
        #  и в целом разобраться с отправкой (в садах сервис),
        #  вроде как там только информация статуса нужна.
        changes = (
            ChangeDeclaration.objects.select_related(
                'declaration').get(id=context.id))

        ChangeInDeclarationPushTask().apply_async(
            kwargs={
                'declaration': changes.declaration,
                'case_number': changes.case_number,
                'decision': False})


@obs.subscribe
class AfterChangeApply:

    listen = [
        'concentrator.changes/ChangesDetailPack/ChangesApplyAction'
    ]

    def after(self, request, context, result):

        # TODO Тот же самый коммент, что и для отмены изменений по заявлению.
        changes = (
            ChangeDeclaration.objects.select_related(
                'declaration').get(id=context.id))

        ChangeInDeclarationPushTask().apply_async(
            kwargs={
                'declaration': changes.declaration,
                'case_number': changes.case_number,
                'decision': True})


# подмена паков
action_pack_overrides = {
    'kinder.core.children.actions.DelegateForDeclarationPack':
        LipetskDelegateForDeclarationPack(),
    'concentrator.changes.actions.ChangesPack':
        LipetskChangesPack(),
    'concentrator.changes.actions.ChangesDetailPack':
        LipetskChangesDetailPack()}


@obs.subscribe
class SaveDeclarationEditTime:

    listen = [
        'kinder.core.queue_module.declaration/'
        'QueueDeclarationPack/QueueDeclarationEditAction',
        'kinder.core.queue_module.declaration/'
        'QueueDeclarationPack/DeclarationAddAction'
    ]

    def after(self, request, context, response):
        # пихаем в контекст время открытия окна Заявки
        # оно нам будет необходимо при закрытии окна
        # см. DeclarationSaveListener
        context.timestamp = date2str(
            datetime.datetime.now(), '%d.%m.%Y %H:%M:%S')


@obs.subscribe
class DeclarationSaveListener:
    """
    Делаем обработку после сохранения заявки
    """

    listen = [
        'kinder.core.queue_module.declaration'
        '/QueueDeclarationPack/DeclarationSaveAction'
    ]

    priority = 99

    def after(self, request, context, response):
        def get_values(new_value=True, **kwargs):
            value_name = 'new_value' if new_value else 'old_value'

            values = ', '.join(
                history_records.filter(
                    new_value__isnull=False, **kwargs
                ).values_list(
                    value_name, flat=True
                )
            )
            return values

        if isinstance(response.data, dict) and response.data.get('success'):
            win_timestamp = datetime.datetime.strptime(
                context.timestamp, '%d.%m.%Y %H:%M:%S'
            )
            # используем время создания окна для выдергивания истории изменений
            history_records = DeclarationHistory.objects.filter(
                declaration_id=context.declaration_id,
                user_id=request.user.id,
                date__gte=win_timestamp,
            )
            changes = {
                'desired_unit': get_values(
                    table='declaration_unit',
                    field=None
                ),
                'desired_date': get_values(
                    table='declaration', field='desired_date'),
                'fullname': get_values(
                    table='children', field='fullname', new_value=False),
                'address': get_values(table='children', field='address_full'),
                'reg_address': get_values(
                    table='children', field='reg_address_full'),
                'phone': get_values(table='delegate', field='phones'),
                'email': get_values(table='delegate', field='email'),
                'privileges': get_values(
                    table='declaration_privilege', action=ActionEnum.INSERT
                ),
            }
            # если было хоть какое-то из отслеживаемых изменений
            if any(changes.values()):
                delegates = ChildrenDelegate.objects.filter(
                    children_id=context.children_id
                )
                if not delegates.exists():
                    return OperationResult.by_message(
                        u'У ребенка отсутствует законный представитель, '
                        u'необходимо внести сведения о нем'
                    )
                win = ChangeReasonWindow()
                win.set_params({
                    'declaration_id': context.declaration_id,
                    'delegates': delegates.values_list(
                        'delegate__id', 'delegate__fullname'
                    ),
                    'changes': changes,
                })
                response = OperationResult(
                    success=True,
                    code=win.get_script()
                )
                return response


@obs.subscribe
class PrivilegeEditWinLister(extensions.BaseEditWinListener):

    listen = (
        'kinder.core.privilege/PrivilegeDictPack/ObjectAddWindowAction',
        'kinder.core.privilege/PrivilegeDictPack/ObjectEditWindowAction',)

    parent_model_field = 'privilege'
    ui_extender_cls = PrivilegeEditWinExtender

    def _get_id(self, context):
        return getattr(context, self.action.parent.id_param_name, None)


@obs.subscribe
class PrivilegeSaveListener(extensions.BaseSaveListener):

    listen = (
        'kinder.core.privilege/PrivilegeDictPack/PrivilegeReplaceSaveAction',
    )

    parent_model_field = 'privilege'
    ui_extender_cls = PrivilegeEditWinExtender

    def _declare_additional_context(self):
        return {
            'name_to_query_at_depart': {
                'type': 'str',
                'default': ''
            },
            'report_type': {
                'type': 'int'
            }
        }
