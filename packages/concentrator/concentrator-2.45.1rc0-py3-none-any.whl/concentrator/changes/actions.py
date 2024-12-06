import contextlib
import copy
import datetime
import json
import traceback
from typing import List

from django.core.exceptions import ValidationError
from m3.actions import ACD
from m3.actions import ControllerCache
from m3.actions import OperationResult
from m3.actions import PreJsonResult
from m3.actions.exceptions import ApplicationLogicException
from m3.plugins import ExtensionManager
from m3_ext.ui import all_components as ext
from m3_ext.ui.icons import Icons
from objectpack.actions import BaseAction
from objectpack.actions import ObjectListWindowAction
from objectpack.actions import ObjectPack
from objectpack.actions import ObjectRowsAction

from kinder.core.declaration.enum import DeclarationSourceEnum
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import DeclarationStatusLog
from kinder.core.declaration.permissions import check_privilege_fields
from kinder.core.declaration.proxy import DeclarationProxy
from kinder.core.declaration.validators import validate_desired_date
from kinder.core.declaration_status.enum import DSS
from kinder.core.declaration_status.helpers import get_status
from kinder.core.direct.models import DRS
from kinder.core.helpers import get_instance
from kinder.core.helpers import get_report_filepath
from kinder.core.helpers import make_full_name
from kinder import logger

from concentrator.changes.reports.report import ReportChanges
from concentrator.constants import MESSAGE_PLUGIN_SMEV3_REQUIRED
from concentrator.models import ChangeDeclaration
from concentrator.models import ChangeSource
from concentrator.models import ChangeStatus
from concentrator.rules import DeclarationStatusChangeRule
from concentrator.webservice.service import send_update_application_state

from .constants import DECLARATION_HAS_FORMED_DIRECT_ERROR
from .helpers import get_storage_helper


class ChangesPack(ObjectPack):
    """Пак для вкладки "Изменения с ЕПГУ"."""

    title = 'Изменения с ЕПГУ'
    __PERMISSION_NS = 'kinder.plugins.concentrator.changes.actions.ChangesPack'
    need_check_permission = True

    columns = [
        {
            'data_index': 'create',
            'header': 'Дата',
            'searchable': False,
            'sortable': True,
        },
        {
            'data_index': 'fields',
            'header': 'Поля',
            'searchable': False,
            'sortable': False,
        },
        {
            'data_index': 'old_values',
            'header': 'Старое значение',
            'searchable': False,
            'sortable': False,
        },
        {
            'data_index': 'new_values',
            'header': 'Новое значение',
            'searchable': False,
            'sortable': False,
        },
        {
            'data_index': 'state',
            'header': 'Статус',
            'searchable': False,
            'sortable': True,
        },
        {
            'data_index': 'user',
            'header': 'Пользователь',
            'searchable': False,
            'sortable': True,
        },
        {
            'data_index': 'commentary',
            'header': 'Комментарий',
            'searchable': False,
            'sortable': True,
        },
    ]

    def __init__(self):
        super().__init__()

        self.changes_print_action = ChangesPrintAction()
        self.changes_rows_action = ChangesRowsAction()
        self.perm_priv_grid_action = PermPrivGridAction()

        self.replace_action('rows_action', self.changes_rows_action)
        self.replace_action('list_window_action', ChangesListWindowAction())

        self.actions.extend([
            self.changes_print_action,
            self.perm_priv_grid_action,
        ])

    def declare_context(self, action):
        """Декларация контекста для экшенов."""

        result = super().declare_context(action)

        if action in (self.changes_rows_action, self.perm_priv_grid_action):
            result.update({'declaration_id': {
                'type': 'int', 'required': True, 'default': None, }})

        return result


class ChangesRowsAction(ObjectRowsAction):
    """
    Экшн преобразует набор изменений для грида во вкладке "Изменения с ЕПГУ".
    """

    def _get_row(self, request, context, row):
        change_set = {
            'fields': [],
            'old_values': [],
            'new_values': []
        }

        storage_helper_cls = get_storage_helper(row.declaration)
        if storage_helper_cls is not None:
            try:
                changes_rows = storage_helper_cls.get_change(row)
            except Exception:
                changes_rows = storage_helper_cls.get_old_change(row)

            for changes_row in changes_rows:
                change_set['fields'].append(changes_row['field'])
                change_set['old_values'].append(str(changes_row['old_value']))
                change_set['new_values'].append(str(changes_row['new_value']))

        return {
            'id': row.id,
            'create': row.create,
            'fields': u', '.join(change_set['fields']),
            'old_values': u', '.join(change_set['old_values']),
            'new_values': u', '.join(change_set['new_values']),
            'state': ChangeStatus.values[row.state],
            'user': row.user.get_full_name().title() if row.user else '',
            'commentary': row.commentary
        }

    def run(self, request, context):
        new_self = copy.copy(self)
        new_self.request = request
        new_self.context = context

        new_self.query = ChangeDeclaration.objects.filter(
            declaration_id=context.declaration_id
        ).order_by(
            'create'
        ).select_related('declaration', 'user')

        total = new_self.get_total_count()

        new_self.apply_sort_order()
        new_self.apply_limit()

        rows = [self._get_row(request, context, row) for row in new_self.query]

        return PreJsonResult({'rows': rows, 'total': total})


class ChangesPrintAction(BaseAction):
    """
    Экшн отдает .xls файл с пустым/заполненным заявлением на изменение данных
    """

    __PERMISSION_NS = (
        'kinder.plugins.concentrator.changes.actions.ChangesPrintAction')

    verbose_name = 'Печать'
    need_check_permission = True

    def context_declaration(self):
        return [
            ACD(name='blank', required=True, type=bool),
            ACD(name='id', required=False, type=int)
        ]

    def run(self, request, context):
        templates = {
            True: 'changes_blank.xls',
            False: 'changes.xls'
        }

        template = templates[context.blank]
        (_, xls_file_abs, url) = get_report_filepath('xls')
        rep = ReportChanges(template, xls_file_abs, request, context)
        rep.make_report()

        return OperationResult(code="function() {location.href='%s';}" % url)


class PermPrivGridAction(ObjectRowsAction):
    """Экшн проверки прав на редактирование таблицы льгот в заявке."""

    def run(self, request, context):

        try:
            declaration_proxy = DeclarationProxy.objects.get(
                id=context.declaration_id)
        except DeclarationProxy.DoesNotExist:
            declaration_proxy = None

        return PreJsonResult({
            'perm': bool(declaration_proxy and check_privilege_fields(
                declaration_proxy, request))})


class ChangesDetailPack(ObjectPack):
    """Пак детального просмотра набора изменений."""

    __PERMISSION_NS = (
        'kinder.plugins.concentrator.changes.actions.ChangesDetailPack')
    title = 'Изменения с ЕПГУ'

    need_check_permission = True

    allow_paging = False

    columns = [
        {
            'data_index': 'field',
            'header': 'Поле',
            'searchable': False,
            'sortable': False,
        },
        {
            'data_index': 'old_value',
            'header': 'Старое значение',
            'searchable': False,
            'sortable': False,
        },
        {
            'data_index': 'new_value',
            'header': 'Новое значение',
            'searchable': False,
            'sortable': False,
        },
    ]

    def __init__(self):
        super().__init__()

        self.replace_action('list_window_action', ChangesDetailWindowAction())
        self.changes_apply_action = ChangesApplyAction()
        self.changes_reject_action = ChangesRejectAction()
        self.check_changes_apply_action = CheckChangesApplyAction()
        self.changes_rows_action = ChangesDetailRowsAction()

        self.replace_action('rows_action', self.changes_rows_action)

        self.actions.extend([
            self.changes_apply_action,
            self.changes_reject_action,
            self.check_changes_apply_action,
        ])

        self.sub_permissions = super().sub_permissions.copy()
        self.sub_permissions[self.list_window_action.perm_code] = (
            self.list_window_action.verbose_name)


class ChangesDetailWindowAction(ObjectListWindowAction):
    """Экшн отдает окно с детализацией изменений."""

    __PERMISSION_NS = (
        'kinder.plugins.concentrator.changes.actions.ChangesDetailWindowAction')

    verbose_name = 'Подтверждение'
    need_check_permission = True

    def context_declaration(self):
        return [ACD(name='id', required=True, type=int)]

    def configure_window(self):

        self.win.template_globals = 'ui-js/changes_detail.js'
        self.win.grid_id = self.win.grid.client_id
        self.win.grid.top_bar.hidden = True
        self.win.modal = True
        self.win.comment_max_length = (
            ChangeDeclaration._meta.get_field('commentary').max_length)

        change = ChangeDeclaration.objects.get(id=self.context.id)

        changes_pack = ControllerCache.find_pack(
            'concentrator.changes.actions.ChangesPack')

        self.win.perm_priv_grid_url = (
            changes_pack.perm_priv_grid_action.absolute_url())

        if change.state in (ChangeStatus.WAIT, ChangeStatus.ACCEPT):

            self.win.print_button = ext.ExtButton(
                text='Распечатать заявление',
                handler='printChanges',
                icon_cls=Icons.PRINTER)

            self.win.buttons.insert(0, self.win.print_button)

            self.win.changes_print_url = (
                changes_pack.changes_print_action.get_absolute_url())

        if change.state == ChangeStatus.WAIT:

            self.win.apply_button = ext.ExtButton(
                text='Применить изменения',
                handler='applyChanges',
                icon_cls=Icons.ACCEPT)

            self.win.buttons.insert(0, self.win.apply_button)

            self.win.reject_button = ext.ExtButton(
                text='Отказать',
                handler='rejectChanges',
                icon_cls=Icons.M3_DELETE)

            self.win.buttons.insert(0, self.win.reject_button)

            self.win.changes_apply_url = (
                self.parent.changes_apply_action.get_absolute_url())
            self.win.changes_reject_url = (
                self.parent.changes_reject_action.get_absolute_url())
            self.win.check_changes_apply_url = (
                self.parent.check_changes_apply_action.get_absolute_url())

            self.win.layout = 'border'
            self.win.comment_field = ext.ExtTextArea(region='south')
            self.win.grid.region = 'center'
            self.win.items.append(self.win.comment_field)


class ChangesDetailRowsAction(ObjectRowsAction):
    """
    Экшн преобразует набор изменений для грида с детализацией изменений
    """

    def context_declaration(self):
        return [ACD(name='id', required=True, type=int)]

    def run(self, request, context):
        changes = (
            ChangeDeclaration.objects.select_related(
                'declaration'
            ).get(id=context.id))

        storage_helper_cls = get_storage_helper(changes.declaration)
        if storage_helper_cls is None:
            return OperationResult.by_message(MESSAGE_PLUGIN_SMEV3_REQUIRED)

        try:
            rows = storage_helper_cls.get_change(changes)
        except Exception:
            rows = storage_helper_cls.get_old_change(changes)

        return PreJsonResult({'rows': rows, 'total': len(rows)})


class ChangesApplyAction(BaseAction):
    """Экшн применяет набор изменений и возвращает обновленные поля."""

    # Если значение в поле нельзя сменить стандартным способом,
    # то используем для этого кастомные правила.
    # Кастомное правило это класс с classmethod-ом change,
    # в который передается обьект и новое значение поля
    CHANGE_RULE_MAP = {
        ('Declaration', 'status'): DeclarationStatusChangeRule
    }

    def context_declaration(self):
        return [
            ACD(name='id', required=True, type=int),
            ACD(name='comment', required=True, type=str, default=''),
        ]

    @staticmethod
    def get_mvd_passport_context_manager(declaration_id):
        """Получение контекстного менеджера для обработки изменений родителя

        Возвращается контекстный менеджер для МВД, который прослушивает
        сигналы на изменение данных паспорта родителя, в случае
        изменения отправляет запрос на проверку паспорта.
        Если плагин не подключен, возвращается contextlib.nullcontext(),
        который ничего не делает

        :param declaration_id: id заявления
        :type declaration_id: int

        :return: Контекстный менеджер для проверки паспорта родителя или
            contextlib.nullcontext(), если плагин для проверки паспорта отключен
        :rtype: AbstractContextManager
        """
        return ExtensionManager().execute(
            'passport_mvd_smev3.get_temp_passport_validity_request_manager',
            declaration_id,
        ) or contextlib.nullcontext()

    @staticmethod
    def _validate_desired_date_from_change(declaration: Declaration, change_data: dict) -> None:
        """Проверка статуса направления при принятии изменений

        Реализована для проверки желаемой даты из изменения,
        чтобы уже после принятия изменений не словить случайно ошибку при смене статуса заявления

        :param declaration: Заявление
        :param change_data: Преобразованное в словарь содержимое поля data у изменения (model Change)

        :return: None

        :raises m3.actions.exceptions.ApplicationLogicException: если новая желаемая дата не пройдет валидацию
        """

        # До принятия изменения, производим проверку желаемых дат, при наличии в изменении
        declaration_fields: list[dict] = change_data.get('Declaration', [])
        desired_field_data = next(
            (field_data for field_data in declaration_fields
             if isinstance(field_data, dict) and 'desired_date' in field_data),
            None
        )
        if desired_field_data:
            _, new_value, _ = desired_field_data.get('desired_date')
            try:
                declaration.desired_date = datetime.datetime.strptime(new_value, '%Y-%m-%d %H:%M:%S').date()
                validate_desired_date(declaration)
            except ValueError as e:
                logger.exception(str(e))
            except ValidationError as err:
                raise ApplicationLogicException(err.messages)

    @staticmethod
    def _validate_direct_status(declaration: Declaration) -> None:
        """Проверка статуса направления заявления на возможность принятия изменения

        :param declaration: Заявление

        :return: None

        :raises m3.actions.exceptions.ApplicationLogicException:
            если будет хоть одно направление заявки не в конечном статусе
        """

        # Нельзя применять изменение если есть хотя бы одно направление не в статусе "Зачислен", "Не явился", "Отказано"
        directs = declaration.direct_set.exclude(status__code__in=DRS.not_accept_change_statuses())
        if directs.exists():
            raise ApplicationLogicException(DECLARATION_HAS_FORMED_DIRECT_ERROR)

    def run(self, request, context):
        change = get_instance(
            context.id,
            ChangeDeclaration,
            error_message='Список изменений заявки с ЕПГУ не найден.',
            select_related=['declaration'],
        )
        declaration = change.declaration
        change_data = json.loads(change.data)

        self._validate_direct_status(declaration=declaration)
        self._validate_desired_date_from_change(declaration=declaration, change_data=change_data)

        storage_helper_cls = get_storage_helper(declaration)
        if storage_helper_cls is None:
            return OperationResult.by_message(MESSAGE_PLUGIN_SMEV3_REQUIRED)

        with self.get_mvd_passport_context_manager(declaration.id):
            try:
                updated_fields = storage_helper_cls.apply_changes(
                    change, request, context.comment)
            except ApplicationLogicException as e:
                change.commentary = f'Невозможно применить: {e}'
                change.save()
                return OperationResult.by_message(str(e))
            except ValidationError as e:
                return OperationResult.by_message(', '.join(e.messages))

        # При принятии данных поступивших через UpdateApplication
        if change.source == ChangeSource.UPDATE_APPLICATION:
            # Льготы в изменениях
            privileges = change_data.get('DeclarationPrivilege')
            # Проверяем: статус подтверждения изменений "Исполнено",
            # в изменениях есть льготы, и есть новое (отличное от данных в
            # заявке) значение льготы, и статус заявки "Зарегистрировано"
            # или "Желает изменить ДОО"
            if (
                change.state == ChangeStatus.ACCEPT
                    and privileges
                    and [priv for priv in privileges if priv.get('conc_unit') or priv.get('conc_privilege')]
                    and declaration.status.code in (DSS.status_queue_privilege())
            ):
                declaration.change_status(
                    get_status(DSS.PRIV_CONFIRMATING),
                    date_validation_needed=False,
                    why_change=(
                        'Авто-смена смена статуса заявления при подтверждении '
                        'данных, пришедших с ЕПГУ, содержащих льготу'))

        # При принятии данных поступивших через NewApplication
        # (например послали заявку с другими данными ФИО и с тем же externalID,
        elif (
            change.source == ChangeSource.NEW_APPLICATION and
            # "воскрешаем" только Архивные и Отказанные заявления
            declaration.status.code in (DSS.REFUSED, DSS.ARCHIVE)
        ):

            declaration.change_status(
                to_status=get_status(code=DSS.RECEIVED),
                date_validation_needed=False,
                why_change='Авто-смена статуса заявления после поступления '
                           'новой заявки с Концентратора')
            declaration.date = change.create.date()
            declaration.save()

        return PreJsonResult(
            data={
                'updated_fields': updated_fields,
                'success': True,
            }
        )


class ChangesRejectAction(BaseAction):
    """Экшн отклоняет набор изменений."""

    def context_declaration(self):
        return [
            ACD(name='id', required=True, type=int),
            ACD(name='comment', required=True, type=str, default=''),
        ]

    def _update_application_state(self, declaration, log_id):
        """
        Отправка информации о заявке.
        """

        send_update_application_state(declaration, log_id=log_id)

    def _reject_status_change(self, changes):
        """
        Имеется ли в наборе изменений изменения статуса заявки
        """

        changes_data = json.loads(
            changes.data)

        if 'Declaration' in changes_data:
            for change in changes_data['Declaration']:
                if 'status' in change:
                    return True

        return False

    def run(self, request, context):
        changes = (
            ChangeDeclaration.objects.select_related(
                'declaration'
            ).get(id=context.id))

        storage_helper_cls = get_storage_helper(changes.declaration)
        if storage_helper_cls is None:
            return OperationResult.by_message(MESSAGE_PLUGIN_SMEV3_REQUIRED)

        try:
            storage_helper_cls.reject_changes(
                changes, request, context.comment)
        except ApplicationLogicException as e:
            changes.commentary = f'Невозможно отклонить: {e}'
            changes.save()
            return OperationResult.by_message(str(e))
        except ValidationError as e:
            return OperationResult.by_message(', '.join(e.messages))

        if (
            changes.source != ChangeSource.NEW_APPLICATION
            and self._reject_status_change(changes)
        ):
            status_log = DeclarationStatusLog.objects.filter(
                declaration=changes.declaration
            ).order_by('id').last()
            self._update_application_state(changes.declaration, status_log.id)

        try:
            rows = storage_helper_cls.get_change(changes)
        except Exception:
            rows = storage_helper_cls.get_old_change(changes)
        # Передается запрос OrderRequest с блоком UpdateOrderRequest
        # со статусом "Отказано в изменении заявления" в ЕПГУ
        ExtensionManager().execute(
            'concentrator.smev3_v321.extensions.send_update_order_request',
            changes.declaration.id, rows, context.comment)

        return OperationResult()


class CheckChangesApplyAction(BaseAction):
    """Экшен дополнительной проверки существования у ребенка заявления
    с источником "Ручной ввод".

    Используется при принятии изменений с ЕПГУ.

    """

    def context_declaration(self):
        return [
            ACD(name='id', required=True, type=int),
        ]

    def run(self, request, context):
        # Получает из БД запись по идентификатору (id)
        change = get_instance(
            context.id,
            ChangeDeclaration,
            error_message='Список изменений заявки с ЕПГУ не найден.')

        # Выполняет доп. проверку на существование в системе
        # заявления на данного ребенка с источником "Ручной ввод"
        declaration_data = Declaration.objects.filter(
            children=change.declaration.children,
            source=DeclarationSourceEnum.INTERFACE
        ).values(
            'children__surname', 'children__firstname', 'children__patronymic',
            'children__date_of_birth', 'children__dul_series',
            'children__dul_number', 'children__dul_date', 'status__name'
        ).first()

        success = declaration_data is not None
        message = ''

        if success:
            fullname_child = (
                make_full_name(declaration_data['children__surname'],
                               declaration_data['children__firstname'],
                               declaration_data['children__patronymic'])
            )

            message = (
                f'Внимание! На ребенка {fullname_child}, '
                f'{declaration_data["children__date_of_birth"]}, '
                f'{declaration_data["children__dul_series"]} '
                f'{declaration_data["children__dul_number"]} '
                f'{declaration_data["children__dul_date"]} '
                f'в системе имеется заявление в статусе '
                f'"{declaration_data["status__name"]}". '
                f'После принятия изменений с ЕПГУ статус текущего заявления '
                f'будет сменен на "Подтверждение документов". '
                f'Принять изменения?'
            )

        return PreJsonResult(
            data={
                'success': success,
                'message': message
            }
        )


class ChangesListWindowAction(ObjectListWindowAction):
    """
    Переопределили для задания verbose_name
    """
    verbose_name = 'Просмотр'
