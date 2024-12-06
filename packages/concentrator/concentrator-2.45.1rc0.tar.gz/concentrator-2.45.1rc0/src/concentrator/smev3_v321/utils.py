from __future__ import annotations

from typing import Any
from typing import TYPE_CHECKING
import datetime
import traceback

from aio_client.base import RequestTypeEnum
from aio_client.provider.api import push_request
from aio_client.provider.models import PostProviderRequest
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from educommon.ws_log.models import SmevLog
from educommon.ws_log.models import SmevSourceEnum
from m3.plugins import ExtensionManager

from kinder.core.children.models import Delegate
from kinder.core.children.models import DelegateTypeEnumerate
from kinder.core.children.models import GenderEnumerate
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import DeclarationStatusLog
from kinder.core.declaration_status.enum import DSS
from kinder.core.declaration_status.models import DeclarationStatusTransfer
from kinder.core.direct.models import DRS
from kinder.core.direct.models import TEXT_CHANGE_STATUS
from kinder.core.direct.models import Direct
from kinder.core.direct.models import DirectRefusalReason
from kinder.core.direct.models import DirectStatusLog
from kinder.core.direct.models import RefusalReasonInitiatorType
from kinder.core.group.models import Pupil
from kinder.core.group.models import PupilHistory
from kinder.core.services.constants import ARCHIVE_DECL_FOR_OLD_KIDS_COMMENTARY
from kinder.settings import REGION_CODE
from kinder.webservice.api.declaration import get_declaration_by_client_id
from kinder.webservice.api.exceptions import ApiException

from concentrator.settings import SMEV3_FORM_DATA_MESSAGE_TYPE
from concentrator.smev3_v321.base.utils import is_cancel_allowed
from concentrator.smev3_v321.base.utils import render_type2xml
from concentrator.smev3_v321.order.constants import CreateOrderStatusMapper

from .constants import AGE_7_REASON
from .constants import CACHE_REJECTED_WITH_CANCEL_REQUEST
from .constants import CHANGES_DATA_TEMPATE
from .constants import DECLARATION_AWAITING_COMMENT
from .constants import DECLARATION_CONCIDERING_STARTED
from .constants import DECLARATION_RECEIVED_COMMENT
from .constants import DECLARATION_REVIEWED_COMMENT
from .constants import DECLARATION_STATUS_MAP
from .constants import DEFAULT_CODE_COMMENT
from .constants import DEFAULT_REFUSED_COMMENT
from .constants import DIRECT_REJECT_COMMENT
from .constants import DIRECT_STATUS_MAP
from .constants import DIRECTED_WITHOUT_RESPONSE
from .constants import FROM_ARCHIVE_STATUS_COMMENT
from .constants import NO_REQUEST_REQUIRED_DECLARATION_STATUSES
from .constants import PROVIDE_DOCUMENT_STATUSES
from .constants import PROVIDE_DOCUMENTS_COMMENT
from .constants import REFUSED_COMMENT
from .constants import REGION_REFUSED_COMMENT_MAP
from .enums import StatusCode
from .models import ApplicantAnswer
from .models import DeclarationOriginMessageID
from .models import DeclarationPortalID
from .service_types import kinder_conc

if TYPE_CHECKING:
    from requests import Response

    from django.db.models import QuerySet

    from concentrator.constants import DeclarationChanges


def check_cancel_request_sended_before(declaration_id: int) -> bool:
    """Проверка, что отмена заявления была в результате получения cancelRequest

    :param declaration_id: Заявление, по которому проверяется cancelRequest
    :return: По заявлению был получен cancelRequest
    """
    cache_value = CACHE_REJECTED_WITH_CANCEL_REQUEST.format(declaration_id)

    cancel_request_sended = cache.get(cache_value)
    cache.delete(cache_value)

    return cancel_request_sended or False


def get_code_and_comment(instance: Declaration | Direct) -> tuple[int, str]:
    """Возвращает код и комментарий для передачи сообщения при смене статуса
    заявления или направления.

    :param instance: Заявление или направление.

    :return: Код и комментарий.

    """
    
    if isinstance(instance, Declaration):
        code, comment = DECLARATION_STATUS_MAP.get(
            instance.status.code, DEFAULT_CODE_COMMENT)

        if (
            instance.status.code == DSS.REFUSED
            and check_cancel_request_sended_before(instance.id)
        ):
            comment = REGION_REFUSED_COMMENT_MAP.get(
                REGION_CODE, DEFAULT_REFUSED_COMMENT)

            return code, comment

        decl_status_log = DeclarationStatusLog.objects.filter(
            declaration=instance, status=instance.status
        ).latest('datetime')

        doc_date_before = get_auto_change_days(decl_status_log)

        if instance.status.code in DSS.status_queue_privilege():
            declaration_reviewed_check(instance)
            declaration_awaiting_direction_check(instance)
            return 0, ''

        if instance.status.code == DSS.ZAGS_CHECKING:
            tat_specifics_comment_for_zags_check = ExtensionManager().execute(
                'kinder.plugins.tat_specifics_smev3.extensions.'
                'get_comment_for_change_order_info_zags_check'
            )
            if tat_specifics_comment_for_zags_check:
                comment = tat_specifics_comment_for_zags_check

        data = {
            'mo': instance.mo.name,
            'comment': decl_status_log.comment,
            'mo_address': instance.mo.address_full,
            'doc_date_before': doc_date_before,
        }
    else:
        status_log = DirectStatusLog.objects.filter(
            direct=instance, status=instance.status
        ).latest('created_at')

        mo_dogovor_days = instance.declaration.mo.days_for_direct_dogovor

        if mo_dogovor_days is None:
            dogovor_days = None
        else:
            dogovor_days = status_log.created_at + datetime.timedelta(
                days=mo_dogovor_days)
        data = {
            'doo': instance.group.unit.name,
            'group': instance.group.name,
            'age_cat': instance.group.age_cat.name,
            'document_details': instance.document_details,
            'mo': instance.declaration.mo.name,
            'unit_address': instance.group.unit.address_full,
        }
        if instance.status.code == DRS.REFUSED:
            reason = DirectRefusalReason.objects.filter(
                direct_status_log=status_log,
            ).select_related('reason').first()
            if (reason and reason.reason.initiator_type ==
                    RefusalReasonInitiatorType.EMPLOYEE):
                data.update({'reason': reason.reason.name})
                code, comment = DIRECT_STATUS_MAP.get(
                    DRS.REJECT, DEFAULT_CODE_COMMENT)
            else:
                code, comment = DIRECT_STATUS_MAP.get(
                    DRS.NEED_CHANGE, DEFAULT_CODE_COMMENT)
        elif instance.status.code == DRS.REGISTER:
            applicant_answer = ApplicantAnswer.objects.filter(
                direct=instance).first()
            if applicant_answer:
                if applicant_answer.answer:
                    code, comment = DIRECT_STATUS_MAP.get(
                        DIRECTED_WITHOUT_RESPONSE)
                else:
                    code, comment = DIRECT_STATUS_MAP.get(DRS.NEED_CHANGE)
            else:
                if instance.manual_create:
                    document_data = f'документом {instance.document_details}'
                else:
                    document_data = (
                        f'номером направления {instance.id} от '
                        f'{instance.date.strftime("%d.%m.%Y")}'
                    )
                code, comment = DIRECT_STATUS_MAP.get(DRS.REGISTER)
                data.update(document_details=document_data)
        else:
            if status_log.old_status.code == DRS.REGISTER:
                # Последняя дата смены статуса направления на "Направлен в ДОО"
                latest_register_date = DirectStatusLog.objects.filter(
                    direct=instance,
                    status__code=DRS.REGISTER
                ).values_list(
                    'created_at', flat=True
                ).order_by('created_at').last()

                days_for_reject_direct = (
                    instance.declaration.mo.days_for_reject_direct or 0)
                if latest_register_date:
                    date_before = (
                        latest_register_date + datetime.timedelta(
                            days=days_for_reject_direct)
                    ).strftime(settings.DATE_FORMAT)
                else:
                    date_before = ''
                data.update(
                    {'reason':
                     f'окончания срока действия направления {date_before}'})
            elif status_log.old_status.code == DRS.DOGOVOR:
                # Последняя дата смены статуса направления на
                # "Заключение договора"
                latest_dogovor_date = DirectStatusLog.objects.filter(
                    direct=instance,
                    status__code=DRS.DOGOVOR
                ).values_list(
                    'created_at', flat=True
                ).order_by('created_at').last()

                days_for_direct_dogovor = (
                    instance.declaration.mo.days_for_direct_dogovor or 0)

                if latest_dogovor_date:
                    dogovor_days = (
                        latest_dogovor_date + datetime.timedelta(
                            days=days_for_direct_dogovor)
                    )

                if dogovor_days is not None:
                    reason = ('окончания срока действия направления '
                              f'{dogovor_days.strftime(settings.DATE_FORMAT)}')
                else:
                    reason = ''
                data.update({'reason': reason})
            if dogovor_days is not None:
                dogovor_days = (
                    f' до {dogovor_days.strftime(settings.DATE_FORMAT)}')
            else:
                dogovor_days = ''
            data.update(
                {'dogovor_days': dogovor_days})
            code, comment = DIRECT_STATUS_MAP.get(
                instance.status.code, DEFAULT_CODE_COMMENT)

        # Если смена статуса происходит со статуса Желает изменить ДОО на
        # Не явился
        if (
            instance.status.code == DRS.REJECT and
            status_log.old_status.code == DRS.NEED_CHANGE
        ):
            code, comment = DIRECT_STATUS_MAP.get(DIRECT_REJECT_COMMENT)

        child = instance.declaration.children
        pupil = Pupil.objects.filter(
            grup=instance.group, children=child).first()

        if pupil:
            date_in_order_to_doo = pupil.date_in_order_to_doo
        else:
            # Если зачисления нет, пытаемся заполнить из истории зачислений
            date_in_order_to_doo = PupilHistory.objects.filter(
                group=instance.group, children=child
            ).order_by('id').values_list(
                'date_in_order_to_doo', flat=True
            ).last()

        data['date_in_order_to_doo'] = (
            date_in_order_to_doo.strftime('%d.%m.%Y')
            if date_in_order_to_doo else ''
        )

        days_for_reject_direct = (
            instance.group.unit.get_days_for_reject_direct())
        if days_for_reject_direct:
            date_before = status_log.created_at + datetime.timedelta(
                days=days_for_reject_direct)
            date_before = f' до {date_before.strftime(settings.DATE_FORMAT)}'
        else:
            date_before = ''

        data.update({'date_before': date_before})

    return code, comment.format(**data)


def push_change_order_info_request(
        declaration: Declaration, org_code: int, comment: str, message_id: str,
        replay_to: str, log_to_smevlog: bool = True
) -> tuple[Response | None, Exception | None]:
    """Отправляет сообщение ChangeOrderInfo.

    :param declaration: Заявление.
    :param org_code: Код статуса.
    :param comment: Комментарий.
    :param message_id: Уникальный идентификатор цепочки взаимодействия в АИО.
    :param replay_to: Индекс сообщения в СМЭВ.
    :param log_to_smevlog: Признак логирования в СМЭВ лог.

    :return: Кортеж след. вида:
        (Ответ AIO сервера, Ошибка при выполнении отправки).

    """

    response_body = None
    response = None
    error_traceback = None
    exception = None

    parser_module = ExtensionManager().execute(
        'concentrator.smev3_v4.extensions.get_parsing_module') or kinder_conc

    try:
        order_id, _ = get_declaration_portal_id_or_client_id(declaration)
        response_body = render_type2xml(
            parser_module.FormDataResponseType(
                changeOrderInfo=parser_module.changeOrderInfoType(
                    orderId=parser_module.orderIdType(int(order_id)),
                    statusCode=parser_module.statusCodeType(orgCode=org_code),
                    comment=comment,
                    cancelAllowed=is_cancel_allowed(declaration.status)
                )),
            name_type='FormDataResponse'
        )

        response = push_request(PostProviderRequest(
            origin_message_id=message_id,
            body=response_body,
            message_type=SMEV3_FORM_DATA_MESSAGE_TYPE,
            attachments=None,
            content_failure_code=None,
            content_failure_comment='',
            replay_to=replay_to,
            is_test_message=False))
    except Exception as e:
        exception = e
        error_traceback = traceback.format_exc()

    if log_to_smevlog:
        SmevLog.objects.create(
            service_address=RequestTypeEnum.get_url(
                RequestTypeEnum.PR_POST),
            method_name='changeOrderInfo',
            method_verbose_name=(
                'FormData (Взаимодействие с формой-концентратором по СМЭВ 3)'),
            direction=SmevLog.OUTGOING,
            interaction_type=SmevLog.IS_SMEV,
            source=SmevSourceEnum.CONCENTRATOR,
            request=response_body,
            response=response.text if response else None,
            result=error_traceback)

    return response, exception


def get_declaration_reviewed_params(
        declaration: Declaration
) -> tuple[int, str] | None:
    """Возвращает данные для запроса changeOrderInfo,
    если требуется его отправка.

    :param declaration: Заявление.

    """

    if CreateOrderStatusMapper(
            declaration, None
    ).check_is_application_reviewed(declaration.status.code):
        comment = DECLARATION_REVIEWED_COMMENT.format(
            **{
                'order_id': declaration.client_id,
                'desired_date':
                    declaration.desired_date.strftime(settings.DATE_FORMAT)
            })

        return StatusCode.CODE_140.value, comment


def declaration_reviewed_check(
        declaration: Declaration
) -> bool:
    """Проверка для статуса концентратора Заявление рассмотрено и
    отправка запроса changeOrderInfo, если требуется.

    :param declaration: Заявление

    :return: Признак удовлетворения условиям статуса

    """

    request_params = get_declaration_reviewed_params(declaration)

    if request_params:
        code, comment = request_params
        message_id = declaration.declarationoriginmessageid.message_id
        push_change_order_info_request(
            declaration, code,
            comment, message_id,
            declaration.declarationoriginmessageid.replay_to)
        DeclarationOriginMessageID.objects.filter(
            declaration=declaration).update(reviewed_sent=True)
        return True

    return False


def get_awaiting_direction_params(
        declaration: Declaration
) -> tuple[int, str] | None:
    """Возвращает данные для запроса changeOrderInfo,
    если требуется его отправка.

    :param declaration: Заявление.

    """

    if CreateOrderStatusMapper(
            declaration, None
    ).check_is_awaiting_direction(declaration.status.code):
        return StatusCode.CODE_160.value, DECLARATION_AWAITING_COMMENT


def declaration_awaiting_direction_check(declaration: Declaration) -> bool:
    """Проверка для статуса концентратора Ожидает направления и отправка
    запроса changeOrderInfo, если требуется

    :param declaration: Заявление

    :return: Признак удовлетворения условиям статуса.

    """
    request_params = get_awaiting_direction_params(declaration)

    if request_params:
        code, comment = request_params
        message_id = declaration.declarationoriginmessageid.message_id
        push_change_order_info_request(
            declaration, code, comment, message_id,
            declaration.declarationoriginmessageid.replay_to)
        return True

    return False


def send_order_info_for_declaration(status_log: DeclarationStatusLog) -> None:
    """
    Отправляет запрос changeOrderInfo для заявления по логу смены статуса

    :param status_log: Лог смены статуса
    """

    declaration_message_id = DeclarationOriginMessageID.objects.filter(
        declaration=status_log.declaration).first()

    if not status_log.old_status or not declaration_message_id or (
            status_log.old_status == status_log.status) or (
            status_log.status.code in NO_REQUEST_REQUIRED_DECLARATION_STATUSES
            and status_log.comment == TEXT_CHANGE_STATUS
    ):
        return

    code = None
    comment = None

    if status_log.status.code == DSS.ARCHIVE:
        if status_log.old_status.code in (DSS.REFUSED, DSS.ACCEPTED):
            return

        code = StatusCode.CODE_150.value

        if status_log.comment == ARCHIVE_DECL_FOR_OLD_KIDS_COMMENTARY:
            reason = AGE_7_REASON
        elif status_log.comment:
            reason = f'. {status_log.comment}'
        else:
            reason = '.'

        comment = FROM_ARCHIVE_STATUS_COMMENT.format(
            declaration_id=status_log.declaration.id, reason=reason)

    message_id = declaration_message_id.message_id

    from concentrator.smev3_v321.base.tasks import (
        PushChangeOrderInfoRequestTask)
    transaction.on_commit(
        lambda: PushChangeOrderInfoRequestTask().apply_async(
            (status_log.declaration_id, code, comment, message_id,
             declaration_message_id.replay_to,
             PushChangeOrderInfoRequestTask.DECLARATION_TYPE,
             status_log.declaration_id)
        )
    )


def get_declaration_by_client_or_portal_id(
        query: QuerySet,
        client_or_portal_id: str | int
) -> tuple[Declaration | None, bool]:
    """Выполняет get_declaration_by_client_id(), в случае ошибки
    осуществляет поиск связанного с DeclarationPortalID заявления.
    Возвращает объект declaration или None и признак сопоставления
    заявления через DeclarationPortalID

    :param query: query для поиска заявления через client_id
    :param client_or_portal_id: айдишник, по которому ведется поиск заявления

    """

    try:
        declaration = get_declaration_by_client_id(query, client_or_portal_id)
    except ApiException:
        try:
            declaration = query.get(
                declarationportalid__portal_id=client_or_portal_id)
            return declaration, True
        except Declaration.DoesNotExist:
            return None, False
    return declaration, False


def get_declaration_portal_id_or_client_id(
        declaration: Declaration) -> tuple[str, bool]:
    """Возвращает идентификатор заявления

    Либо это будет portal_id из DeclarationPortalID заявления, либо это будет
    client_id. Использование данной функции необходимо для правильной обработки
    заявлений, которые были созданы до полного перехода/миграции на СМЭВ3,
    поскольку при переходе были изменены идентификаторы заявлений
    (новые идентификаторы как раз были записаны в portal_id, а старые client_id
    в этом случае не изменялись)

    :param declaration: Заявление

    :return: Кортеж (идентификатор заявления - portal_id, если есть,
        иначе client_id; булевая переменная, является ли идентификатор
        portal_id)
    """

    try:
        return declaration.declarationportalid.portal_id, True
    except DeclarationPortalID.DoesNotExist:
        return declaration.client_id, False


def get_auto_change_days(declaration_status_log: DeclarationStatusLog) -> str:
    """Возвращает срок предоставления документов при смене статуса заявления

    :param declaration_status_log: Лог смены статуса заявления.

    """

    status_transfer = DeclarationStatusTransfer.objects.filter(
        from_status=declaration_status_log.old_status,
        to_status=declaration_status_log.status
    ).first()

    if status_transfer and status_transfer.auto_change_days is not None:
        date_before = datetime.date.today() + datetime.timedelta(
            days=status_transfer.auto_change_days)
        doc_date_before = (
            f'до {date_before.strftime(settings.DATE_FORMAT)} ')
    else:
        doc_date_before = ''

    return doc_date_before


def get_declaration_code_and_comment(
        status_log: DeclarationStatusLog
) -> tuple[int, str] | None:
    """Возвращает код и комментарий запроса для передачи сообщения
    при смене статуса заявления.

    :param status_log: Лог изменения статуса заявления.

    """

    comment_params = {
        'mo': status_log.declaration.mo.name,
        'comment': status_log.comment,
        'mo_address': status_log.declaration.mo.address_full,
        'date': status_log.declaration.date.strftime(settings.DATE_FORMAT),
        'declaration_client_id': status_log.declaration.client_id,
    }

    if status_log.status.code == DSS.RECEIVED:
        return (
            StatusCode.CODE_110.value,
            DECLARATION_RECEIVED_COMMENT.format(**comment_params))

    if status_log.status.code == DSS.ACCEPTED_FOR_CONSIDERING:
        return StatusCode.CODE_120.value, DECLARATION_CONCIDERING_STARTED

    if status_log.status.code in PROVIDE_DOCUMENT_STATUSES:
        comment_params['doc_date_before'] = get_auto_change_days(status_log)
        return (
            StatusCode.CODE_130.value,
            PROVIDE_DOCUMENTS_COMMENT.format(**comment_params))

    if status_log.status.code in DSS.status_queue_full():
        reviewed_params = (
            get_declaration_reviewed_params(status_log.declaration))
        awaiting_direction_params = (
            get_awaiting_direction_params(status_log.declaration))

        return reviewed_params or awaiting_direction_params

    if status_log.status.code == DSS.REFUSED:
        return (
            StatusCode.CODE_150.value, REFUSED_COMMENT.format(**comment_params)
        )


def changes_to_str(changes: list[DeclarationChanges]) -> str:
    """Возвращает изменения в виде строки в читаемом виде.

    :param changes: Изменения

    :return: Строка с изменениями

    """
    return ' '.join(
        CHANGES_DATA_TEMPATE.format(index=index, **change)
        for index, change in enumerate(changes, start=1))


def update_middle_name_params(
        middle_name: str, params: dict[str, Any],
        is_parents: bool | None = None, is_initial: bool = False
) -> dict[str, Any]:
    """Обновляет параметры, устанавливая пол и тип представителя,
    если будут совпаданеия по окончанию отчества.

    Пол так же определяется и для ребенка.

    :param middle_name: Отчество представителя/ребенка.
    :param params: Словарь с параметрами.
    :param is_parents: Параметр, является ли родителем.
    :param is_initial: Параметр первичного определения типа представителя
        (до определения его по суффиксу отчества).

    :return: Обновленный словарь с параметрами представителя/ребенка.

    """

    middle_name = middle_name.strip()

    if is_initial and is_parents is not None:
        params['type'] = (
            DelegateTypeEnumerate.MOTHER
            if is_parents else DelegateTypeEnumerate.LEX)

    if middle_name.endswith(('вна', 'кызы', 'ична')):
        params['gender'] = GenderEnumerate.FEMALE

        if is_parents:
            params['type'] = DelegateTypeEnumerate.MOTHER
    elif middle_name.endswith(('ич', 'оглы')):
        params['gender'] = GenderEnumerate.MALE

        if is_parents:
            params['type'] = DelegateTypeEnumerate.FATHER

    return params


def get_delegate(declaration: Declaration) -> Delegate | None:
    """Возвращает представителя ребенка из заявления.

    Выбирает среди всех представителей ребенка из указанного заявления того,
    который был создан/отмечен (при изменении) при получении заявления СМЭВ 3.
    Если представителей нет у ребенка или не был найден нужный, то вернет None.

    :param declaration: Заявление

    :return: инстанс представителя или None

    """

    base_childrendelegate_query = (
        declaration.children.childrendelegate_set.select_related(
            'delegate').only('delegate'))

    # Пытается найти нужного представителя по идентификатору заявления
    # из самого заявления (client_id).
    childrendelegate = (
        base_childrendelegate_query.filter(
            extendedchildrendelegate__order_id=declaration.client_id).first())

    # Если не был найден, то на всякий случай проверяет по portal_id
    # (заявки полученные по СМЭВ 2, но при этом еще могут учавствовать
    # во взаимодействии).
    if childrendelegate is None:
        try:
            portal_id = declaration.declarationportalid.portal_id
        except DeclarationPortalID.DoesNotExist:
            return None

        childrendelegate = (
            base_childrendelegate_query.filter(
                extendedchildrendelegate__order_id=portal_id).first())

    return childrendelegate.delegate if childrendelegate else None
