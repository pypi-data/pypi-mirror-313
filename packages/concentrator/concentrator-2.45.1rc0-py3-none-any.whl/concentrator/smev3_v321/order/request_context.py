import datetime
from contextlib import suppress

from kinder.core.declaration.models import Declaration
from kinder.core.direct.models import Direct

from .constants import CreateOrderStatusMapper
from .constants import UpdateOrderStatusMapper


class OrderRequestContext:
    """Объект-контекст для запроса OrderRequest."""

    # Понятные имена параметров
    verbose_names = {
        'declaration_id': 'id заявления',
        'order_id':
            'Номер заявления на получение информации об этапах и результатах '
            'оказания услуги зачисления в дошкольную организацию',
        'direct': 'Направление',
        'delegate_id': 'id представителя',
    }

    def __init__(
            self, declaration_id, order_id, direct=None, delegate_id=None, parser_module=None
    ):
        self.declaration_id = declaration_id
        self.declaration = Declaration.objects.get(id=declaration_id)
        self.order_id = order_id
        self.direct = (
            Direct.objects.filter(id=direct).first() if direct
            else self.declaration.direct_set.first()
        )
        self.delegate_id = delegate_id

        self.epgu_status_mapper = (
            CreateOrderStatusMapper(self.declaration, self.direct))
        self.parser_module = parser_module


class UpdateOrderRequestContext(OrderRequestContext):
    """Объект-контекст для запроса UpdateOrderRequest."""

    # Понятные имена параметров
    verbose_names = {
        **OrderRequestContext.verbose_names,
        'declaration_status_changed': 'Признак смены статуса заявления',
        'event': 'Событие',
        'direct_status_log': 'Данные записи лога статуса направления',
        'declaration_changes_rows': 'Данные изменения заявления',
        'reject_changes_comment': 'Комментарий отмены изменений',

    }

    def __init__(
            self, declaration_id, order_id, direct=None, delegate_id=None,
            parser_module=None, declaration_status_changed=False, event=None,
            direct_status_log=None, declaration_changes_rows=None,
            reject_changes_comment=None
    ):
        super().__init__(declaration_id, order_id, direct, delegate_id, parser_module)

        self.declaration_status_changed = declaration_status_changed
        self.event = event
        self.direct_status_log = direct_status_log
        self.declaration_changes_rows = declaration_changes_rows
        self.reject_changes_comment = reject_changes_comment

        self.epgu_status_mapper = UpdateOrderStatusMapper(
            self.declaration, self.direct, self.declaration_status_changed,
            self.direct_status_log, self.event, self.declaration_changes_rows,
            self.reject_changes_comment)
