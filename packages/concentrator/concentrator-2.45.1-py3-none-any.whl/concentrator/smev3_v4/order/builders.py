from concentrator.smev3_v321.order.builders import OrderRequestBuilder
from concentrator.smev3_v321.order.builders import UpdateOrderRequestBuilder
from concentrator.smev3_v4.service_types import kinder_order101


class OrderRequestBuilderV101(OrderRequestBuilder):
    """Билдер запроса OrderRequest СМЭВ 3 с блоком CreateOrderRequest версии 1.0.1"""
    parser_module = kinder_order101

class UpdateOrderRequestBuilderV101(UpdateOrderRequestBuilder):
    """Билдер запроса UpdateOrderRequest СМЭВ 3 версии 1.0.1"""
    parser_module = kinder_order101

