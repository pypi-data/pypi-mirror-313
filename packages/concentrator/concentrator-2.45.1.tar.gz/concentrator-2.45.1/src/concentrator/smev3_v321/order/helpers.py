from __future__ import annotations

from typing import Any

from django.db.transaction import on_commit
from m3.plugins import ExtensionManager

from kinder.core.children.constants import DEFAULT_ZAGS_ACT_NUMBER
from kinder.core.children.models import Children
from kinder.core.children.models import Delegate
from kinder.webservice.smev3.utils.managers import BaseRequestManager

from concentrator.smev3_v321.models import OrderRequest
from concentrator.smev3_v321.models import PendingUpdateOrderRequest
from concentrator.smev3_v321.models import UpdateOrderRequest
from concentrator.smev3_v321.service_types import kinder_conc

from .constants import CHILDREN_REQUIRED_FIELDS
from .constants import CHILDREN_RF_DOC_REQUIRED_FIELDS
from .constants import DELEGATE_REQUIRED_FIELDS
from .constants import DELEGATE_REQUIRED_PHONE_FIELDS
from .request_context import UpdateOrderRequestContext
from .tasks import OrderRequestSendingTask
from .tasks import UpdateOrderRequestSendingTask


class OrderRequestSMEV3RequestManager(BaseRequestManager):
    """Хелпер запуска задачи по отправке запросов OrderRequest СМЭВ 3."""

    task: type[OrderRequestSendingTask] = OrderRequestSendingTask
    model: type[OrderRequest] = OrderRequest

    def create_request(self) -> model:
        """Создает запрос.

        :return: инстанс созданного запроса
        :rtype: model
        """

        return self.model.objects.get_or_create(**self.get_params())

    def get_params(self) -> dict[str, Any]:
        """Формирует параметры для создания запроса из контекста.

        :return: словарь данных
        """

        return {
            'declaration_id': self.context.declaration_id,
            'defaults': {'request_order_id': self.context.order_id},
        }

    def apply_async(self) -> None:
        """Запускает задачу."""

        request, _ = self.create_request()
        task = self.create_task()

        on_commit(lambda: task.apply_async((request.id, self.context),))


class UpdateOrderRequestSMEV3RequestManager(BaseRequestManager):
    """Хелпер запуска задачи по отправке запросов UpdateOrderRequest СМЭВ 3."""

    task = UpdateOrderRequestSendingTask
    model = UpdateOrderRequest

    def get_params(self) -> dict[str, Any]:
        """Формирует параметры для создания запроса из контекста.

        :return: словарь данных.
        """

        return {
            'declaration_id': self.context.declaration_id,
        }

    def apply_async(self) -> None:
        """Запускает задачу."""

        request = self.create_request()
        task = self.create_task()

        on_commit(lambda: task.apply_async((request.id, self.context),))


class DispatchOrderRequestSMEV3RequestManager:
    """Класс для управления данными запроса UpdateOrderRequest.

    Выполняет запуск задачи отправки данных UpdateOrderRequest
    или создание/обновление отложенной задачи по отправке данных.
    """

    def __init__(
            self,
            order_request: OrderRequest,
            source_version: int,
            data: dict[str, Any]
    ) -> None:
        """Конструкор.

        :param order_request: Объект запроса
        :param source_version: Версия источника
        :param data: Данные для отправки
        """

        self.order_request = order_request
        self.source_version = source_version
        self.data = data

    def run(self) -> None:
        parser_module = ExtensionManager().execute(
            'concentrator.smev3_v4.extensions.get_parsing_module') or kinder_conc

        if self.order_request.order_id:
            UpdateOrderRequestSMEV3RequestManager(
                UpdateOrderRequestContext(
                    **{**self.data,
                       'order_id': self.order_request.order_id,
                       'parser_module': parser_module.__name__
                    })
            ).apply_async()
        else:
            PendingUpdateOrderRequest.objects.update_or_create(
                order_request=self.order_request,
                source_version=self.source_version,
                defaults={'data': self.data})


class OrderRequestRequiredFieldsChecker:
    """
    Класс для проверки отсутствующих полей у объектов модели для запроса
    OrderRequest.
    """

    @staticmethod
    def is_field_empty(obj: Children | Delegate, field: str) -> bool:
        """Проверка, что поле пустое

        :param obj: Объект (ребенок или представитель)
        :param field: str

        :return: Считается ли поле пустым
        """
        is_child = isinstance(obj, Children)
        value = getattr(obj, field)
        if is_child and field == 'zags_act_number':
            return not value or value == DEFAULT_ZAGS_ACT_NUMBER
        return not value

    @classmethod
    def check_child(cls, child: Children) -> dict[str, str]:
        """Возвращает пустые поля ребёнка, обязательные для запроса OrderRequest

        :param child: Ребенок

        :return: Словарь {пустое поле модели ребёнка: читаемое название поля}
        """
        mapping = CHILDREN_REQUIRED_FIELDS.copy()
        if child.is_svid:
            mapping.update(CHILDREN_RF_DOC_REQUIRED_FIELDS)

        empty_fields = {
            field: name for field, name in mapping.items()
            if cls.is_field_empty(child, field)
        }
        return empty_fields

    @classmethod
    def check_delegate(cls, delegate: Delegate) -> dict[str, str]:
        """Возвращает пустые поля родителя, обязательные для запроса
        OrderRequest

        :param delegate: Представитель

        :return: Словарь {пустое поле модели представителя:
            читаемое название поля}
        """
        empty_fields = {
            field: name for field, name in DELEGATE_REQUIRED_FIELDS.items()
            if cls.is_field_empty(delegate, field)
        }
        # Должен быть заполнен хотя бы один из телефонов
        # (если пусто, заполняем оба телефона)
        phone_mapping = DELEGATE_REQUIRED_PHONE_FIELDS
        if all(cls.is_field_empty(delegate, field) for field in phone_mapping):
            empty_fields.update(phone_mapping)

        return empty_fields
