from django.db.models import BooleanField
from django.db.models import Exists
from django.db.models import ExpressionWrapper
from django.db.models import F
from django.db.models import OuterRef
from django.db.models import Q

from m3.actions.utils import extract_int
from m3_ext.ui import all_components as ext

from kinder.controllers import obs
from kinder.core.declaration.helpers import check_health_is_expired
from kinder.core.declaration.models import Declaration
from kinder.core.declaration_status.enum import DSS

from concentrator.changes.forms import DeclarationEditWindowExtension
from concentrator.changes.forms import DeclarationListWindowExtension
from concentrator.models import ChangeDeclaration
from concentrator.models import ChangeStatus
from concentrator.models import PrivilegeComment


@obs.subscribe
class AddChangesTab:
    """ Добавляем вкладку "Изменения с ЕПГУ"."""

    listen = [
        'kinder.core.queue_module.declaration/'
        'QueueDeclarationPack/QueueDeclarationEditAction'
    ]

    def configure_edit_window(self, params):
        win = params['win']
        DeclarationEditWindowExtension.build_extension(win)
        return params


@obs.subscribe
class AddCommentPrivileges:
    """Добавляем поле Комментарий "Изменения с ЕПГУ"."""

    listen = [
        'kinder.core.declaration.declaration_privilege/'
        'DeclarationPrivilegePack/ObjectEditWindowAction',
        'kinder.core.declaration.declaration_privilege/'
        'DeclarationPrivilegePack/ObjectAddWindowAction'
    ]

    def after(self, request, context, result):
        if not context.decl_privilege_id:
            return

        win = result.data

        concentrator_comment = (
            PrivilegeComment.objects.filter(
                declaration_privilege=context.decl_privilege_id
            ).values_list('concentrator_comment', flat=True).first())

        if concentrator_comment is not None:
            win.comment_privileges = ext.ExtStringField(
                label='Комментарий из концентратора',
                name='comment_privileges',
                anchor='100%', read_only=True, value=concentrator_comment)
            win.form.items.append(win.comment_privileges)


@obs.subscribe
class MakeNeedConfirmationExtension:
    """Добавляем checkbox "Отобразить только заявки на подтверждение"."""

    priority = 10

    listen = [
        'kinder.core.queue_module.declaration/'
        'QueueDeclarationPack/QueueDeclaratonListWindowAction'
    ]

    def configure_list_window(self, params):
        win = params['win']
        DeclarationListWindowExtension.build_extension(win)
        return params


@obs.subscribe
class MakeObjectRowsActionExtension:
    """
    Перехватываем rows action. Добавляем фильтр заявок на подтверждение.
    Добавляем метку для подсветки записей с необработанными изменениями.
    """

    listen = [
        'kinder.core.queue_module.declaration/'
        'QueueDeclarationPack/DeclarationRowsAction'
    ]

    def get_rows(self, res):
        declaration_ids = [row['id'] for row in res]
        declarations_query = Declaration.objects.filter(
            id__in=declaration_ids
        ).annotate(
            health_need_code=F('children__health_need__code'),
            health_need_exp_date=F('children__health_need_expiration_date'),
            is_in_queue=ExpressionWrapper(
                Q(status__code__in=DSS.status_queue_full()),
                output_field=BooleanField()
            ),
            changes_await=Exists(
                ChangeDeclaration.objects.filter(
                    declaration_id=OuterRef('id'), state=ChangeStatus.WAIT
                ))
        ).only('id')
        decls_data = {decl.id: decl for decl in declarations_query}

        for row in res:
            declaration = decls_data[row['id']]
            row['changes_await'] = declaration.changes_await
            # Булевый атрибут, используется для подсветки строк в зеленый цвет
            row['expired_health_date'] = check_health_is_expired(
                declaration.health_need_code,
                declaration.health_need_exp_date,
            ) and declaration.is_in_queue

        return res

    def apply_filter(self, query):
        wait_only = extract_int(self.request, 'need_confirmation_only')

        if wait_only:
            query = query.filter(
                changedeclaration__state=ChangeStatus.WAIT).distinct()
        return query
