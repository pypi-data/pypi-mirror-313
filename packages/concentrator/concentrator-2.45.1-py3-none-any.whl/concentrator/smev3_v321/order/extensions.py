from django.db.models import Exists
from django.db.models import OuterRef
from m3_ext.ui import all_components as ext

from concentrator.smev3_v321.models import OrderRequest

from .constants import DECLARATION_CHANGED
from .enums import PendingUpdateOrderRequestSourceVersionEnum
from .helpers import DispatchOrderRequestSMEV3RequestManager


def send_update_order_request(
        declaration_id, declaration_changes_rows, reject_changes_comment,
        ext_result
):
    """Точка расширения для отправки UpdateOrderRequest после
    отклонения изменений с концентратора.

    :param declaration_id: Идентификатор заявления
    :type declaration_id: int
    :param declaration_changes_rows: Список изменений заявления
    :type declaration_changes_rows: list
    :param reject_changes_comment: Комментарий причины отклонения изменений
    :type reject_changes_comment: str

    """

    try:
        order_request = (
            OrderRequest.objects.get(declaration_id=declaration_id))
    except OrderRequest.DoesNotExist:
        return

    DispatchOrderRequestSMEV3RequestManager(
        order_request, PendingUpdateOrderRequestSourceVersionEnum.V_0,
        {
            'declaration_id': declaration_id,
            'event': DECLARATION_CHANGED,
            'declaration_changes_rows': declaration_changes_rows,
            'reject_changes_comment': reject_changes_comment,
        }).run()


def set_epgu_subscribed_checkbox(win, declaration_id, ext_result):
    """
    Добавляет чек-бокс "Подписан на уведомления через ЕПГУ" в карточку заявки.
    """

    is_order_id = OrderRequest.objects.filter(
        declaration_id=declaration_id,
        order_id__isnull=False
    ).exists()

    win.is_subscribed_cont = ext.ExtContainer(
        anchor='100%', label_width=400, layout='form')

    is_epgu_subscribed = ext.ExtCheckBox(
        label='Подписан на уведомления через ЕПГУ',
        name='is_subscribed',
        read_only=True,
        checked=is_order_id
    )
    win.is_subscribed_cont.items.append(is_epgu_subscribed)
    win.decl_pan.items.insert(11, win.is_subscribed_cont)


def apply_epgu_subscribed_only_filter(query, context, ext_result):
    """
    Фильтрация заявлений в зависимости от значения чек-бокса
    "Подписан на уведомления через ЕПГУ".
    """
    if int(getattr(context, 'is_epgu_subscribed_only', 0)):
        order_request_exists = Exists(
            OrderRequest.objects.filter(
                declaration_id=OuterRef('id'),
                order_id__isnull=False
            )
        )

        query = query.annotate(
            order_request_exists=order_request_exists
        ).filter(
            order_request_exists=True
        )

    return query
