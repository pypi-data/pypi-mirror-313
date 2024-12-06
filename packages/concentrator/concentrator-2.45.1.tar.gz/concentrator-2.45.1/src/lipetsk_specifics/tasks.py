from celery.task import Task
from educommon.async_task.models import AsyncTaskType

from kinder import celery_app
from kinder.core.async_tasks.tasks import AsyncTask
from kinder.core.common import get_service_user
from kinder.core.declaration.enum import DeclarationSourceEnum
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import RejectReason
from kinder.core.declaration_status.enum import DSS
from kinder.logger import error
from kinder.users.models import User
from kinder.webservice.push_event.helpers import SimplePushEvent

from .constants import CHILDREN_APPLY_IN_QUEUE_TMP
from .push_event.helpers import ChangeInDeclarationPushEvent
from .push_event.helpers import QueueDirectionDecision


class ChangeInDeclarationPushTask(Task):
    """
    Асинхронная задача по отправке данных
    при принятии или отклонении изменений в заявке.

    """

    def run(self, *args, **kwargs):

        declaration = kwargs.get('declaration')
        decision = kwargs.get('decision', False)
        case_number = kwargs.get('case_number', None)
        user = get_service_user()
        if declaration.source == DeclarationSourceEnum.EPGULIPETSK:
            ChangeInDeclarationPushEvent().make(
                declaration=declaration,
                decision=decision,
                user=user,
                commentary='Асинхронная задача по отправке данных '
                           'при принятии или отклонении изменений в заявке',
                case_number=case_number)


class LipetskPushEventTask(AsyncTask):
    """
    Асинхронная отправка решения о принятии или отклонении участия
    заявки в очереди.

    """

    description = 'Отправка pushEvent с данными на ЕПГУ (Липецк)'
    task_type = AsyncTaskType.ASYNC_REQUEST

    def process(self, *args, **kwargs):
        declaration_id = kwargs.get('declaration')
        declaration = Declaration.objects.get(id=declaration_id)

        user_id = kwargs.get('user')
        user = User.objects.get(id=user_id)

        apply_in_queue = declaration.status.code in (DSS.REGISTERED,
                                                     DSS.PRIV_CONFIRMATING)
        reject_reason_id = kwargs.get('reject_reason_id')
        comment = ''
        decision = False

        if reject_reason_id:
            decision = False
            try:
                reject_reason = RejectReason.objects.get(id=reject_reason_id)
                comment = reject_reason.name
            except RejectReason.DoesNotExist as e:
                error(
                    f'Ошибка при попытке отправить pushEvent: '
                    f'Причина отказа с id={e.msg} не найдена'
                )
                comment = ''
        elif apply_in_queue:
            comment = CHILDREN_APPLY_IN_QUEUE_TMP.format(
                client_id=declaration.client_id)
            decision = True

        if apply_in_queue or reject_reason_id:
            # липецкий PushEvent для Зарегистровано / Подтверждение / Отказа
            if declaration.source == DeclarationSourceEnum.EPGULIPETSK:
                QueueDirectionDecision().make(
                    declaration=declaration,
                    comment=comment,
                    user=user,
                    is_apply=decision)

        else:
            # обычный PushEvent всех регионов в остальных случаях
            SimplePushEvent().make(
                declaration=declaration,
                user=user,
                commentary=kwargs.get('commentary', '')
            )


celery_app.register_task(ChangeInDeclarationPushTask)
celery_app.register_task(LipetskPushEventTask)
