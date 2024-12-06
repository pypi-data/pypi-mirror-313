from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
import traceback

from django.db.models import Q

from kinder import logger
from kinder.core.children.models import Delegate
from kinder.core.dict.models import DULDelegateType
from kinder.core.helpers import get_q
from kinder.core.helpers import recursive_py_getattr

from concentrator.smev3_v321.order.helpers import (
    OrderRequestRequiredFieldsChecker)
from concentrator.smev3_v321.service_types import kinder_conc

from .constants import APPLICATION_ORDER_INFO_REQUEST_CHILD_DATA_ERROR_COMMENT
from .constants import (
    APPLICATION_ORDER_INFO_REQUEST_DELEGATE_DATA_ERROR_COMMENT)
from .constants import APPLICATION_ORDER_INFO_REQUEST_DELEGATE_ERROR_COMMENT


if TYPE_CHECKING:
    from kinder.core.children.models import Children
    from kinder.core.declaration.models import Declaration


# Соответствие полей представителя в ЭДС (обязательные поля для OrderRequest)
# и полей из блока ApplicationOrderInfoRequest
DELEGATE_FIELDS_MAP = {
    'firstname': 'PersonInfo.PersonName',
    'surname': 'PersonInfo.PersonSurname',
    'phones': 'PersonInfo.PersonPhone',
    'phone_for_sms': 'PersonInfo.PersonPhone',
    'email': 'PersonInfo.PersonEmail',
    'dul_series': 'PersonIdentityDocInfo.IdentityDocSeries',
    'dul_number': 'PersonIdentityDocInfo.IdentityDocNumber',
    'dul_date': 'PersonIdentityDocInfo.IdentityDocIssueDate',
    'dul_issued_by': 'PersonIdentityDocInfo.IdentityDocIssued',
    'dul_type_id': (
        'PersonIdentityDocInfo.IdentityDocName.code',
        lambda code: DULDelegateType.objects.filter(
            esnsi_code=code).values_list('id', flat=True).first()
    ),
}

# Соответствие полей детей в ЭДС (обязательные поля для OrderRequest)
# и полей из блока ApplicationOrderInfoRequest.
# Вместо '{doc_param}' должно быть ChildBirthDocRF или ChildBirthDocForeign
CHILDREN_FIELDS_MAP = {
    'surname': 'ChildInfo.ChildSurname',
    'firstname': 'ChildInfo.ChildName',
    'date_of_birth': 'ChildInfo.ChildBirthDate',
    'dul_number': 'ChildInfo.{doc_param}.ChildBirthDocNumber',
    'dul_date': 'ChildInfo.{doc_param}.ChildBirthDocIssueDate',
    'zags_act_place': 'ChildInfo.{doc_param}.ChildBirthDocIssued',
}

# Соответствие полей документов детей в ЭДС (обязательные поля для OrderRequest)
# и полей из блока ApplicationOrderInfoRequest. Указаны поля, которые есть
# только у российских документов
RF_DOC_CHILDREN_FIELDS_MAP = {
    'dul_series': 'ChildInfo.ChildBirthDocRF.ChildBirthDocSeries',
    'zags_act_number': 'ChildInfo.ChildBirthDocRF.ChildBirthDocActNumber',
    'zags_act_date': 'ChildInfo.ChildBirthDocRF.ChildBirthDocActDate',
}


def get_children_fields_map(is_rf_birth_doc: bool) -> dict[str, Any]:
    """Получение маппинга полей ребенка и полей из ApplicationOrderInfoRequest

    :param is_rf_birth_doc: Наличие российского свидетельства о рождении

    :return: Маппинг полей ребенка и полей из ApplicationOrderInfoRequest
    """
    mapping = CHILDREN_FIELDS_MAP.copy()

    if is_rf_birth_doc:
        mapping.update(RF_DOC_CHILDREN_FIELDS_MAP)
        doc_param = 'ChildBirthDocRF'
    else:
        doc_param = 'ChildBirthDocForeign'

    for key, value in mapping.items():
        if isinstance(value, str) and '{doc_param}' in value:
            mapping[key] = value.format(doc_param=doc_param)
    return mapping


class BaseApplicationOrderInfoUpdater:
    """
    Базовый класс для обновления данных на основе данных запроса
    ApplicationOrderInfo.
    """
    def __init__(
            self,
            obj: Children | Delegate,
            request_data: kinder_conc.ApplicationOrderInfoRequestType
    ):
        """
        :param obj: Изменяемый объект (ребенок или представитель)
        :param request_data: Данные запроса ApplicationOrderInfo
        """
        self.obj = obj
        self.request_data = request_data

        self.fields_mapping = self.get_fields_mapping()
        self.changed_fields = []

    def get_fields_mapping(self):
        """Маппинг для полей объекта и полей из запроса."""
        return {}

    def get_request_value(self, field: str) -> Any:
        """Получение значения из запроса.

        :param field: Название поля модели

        :return: Значение из запроса для обновления в объекте
        """
        if field not in self.fields_mapping:
            return None

        mapping_value = self.fields_mapping[field]
        if isinstance(mapping_value, tuple):
            req_field, req_function = mapping_value
            req_value = recursive_py_getattr(self.request_data, req_field)
            return req_function(req_value) if req_value is not None else None
        else:
            return recursive_py_getattr(self.request_data, mapping_value)

    def get_empty_fields(self) -> list[str]:
        """Получение пустых полей, которые надо заполнить."""
        return []

    def run(self) -> bool:
        """Основной метод для применения изменений к объекту

        :return: Было ли изменение (сохранение) объекта модели
        """
        for field_name in self.get_empty_fields():
            value = self.get_request_value(field_name)
            if value:
                setattr(self.obj, field_name, value)
                self.changed_fields.append(field_name)

        if self.changed_fields:
            self.obj.save()

        return bool(self.changed_fields)

    def run_with_error_handling(self):
        """Метод для применения изменений к объекту с обработкой ошибок

        :return: Кортеж (было ли изменение (сохранение) объекта модели,
            наличие ошибок)
        """
        has_error = False
        result = None
        try:
            result = self.run()
        except Exception:
            logger.error(traceback.format_exc())
            has_error = True
        return result, has_error


class DelegateApplicationOrderInfoUpdater(BaseApplicationOrderInfoUpdater):
    """Класс для заполнения данных представителей на основе запроса."""
    def get_fields_mapping(self) -> dict:
        return DELEGATE_FIELDS_MAP

    def get_empty_fields(self) -> list[str]:
        return list(OrderRequestRequiredFieldsChecker.check_delegate(self.obj))


class ChildApplicationOrderInfoUpdater(BaseApplicationOrderInfoUpdater):
    """Класс для заполнения данных детей на основе запроса."""
    def get_fields_mapping(self) -> dict:
        return get_children_fields_map(self.obj.is_svid)

    def get_empty_fields(self) -> list[str]:
        return list(OrderRequestRequiredFieldsChecker.check_child(self.obj))


def get_declaration_not_full_message(
    child_empty_fields: dict[str, str], delegate_empty_fields: dict[str, str]
) -> str:
    """Получение сообщения о том, что заполнены не все поля

    :param child_empty_fields: Словарь {пустые поля ребенка: читаемые названия}
    :param delegate_empty_fields: Словарь {пустые поля представителя:
        читаемые названия}

    :return: Cообщения о том, что заполнены не все поля
    """
    assert child_empty_fields or delegate_empty_fields

    msg_parts = []
    if child_empty_fields:
        start_msg = APPLICATION_ORDER_INFO_REQUEST_CHILD_DATA_ERROR_COMMENT
        msg_parts.append(
            f'{start_msg} {", ".join(child_empty_fields.values())}.')

    if delegate_empty_fields:
        start_msg = APPLICATION_ORDER_INFO_REQUEST_DELEGATE_DATA_ERROR_COMMENT
        msg_parts.append(
            f'{start_msg} {", ".join(delegate_empty_fields.values())}.')

    return ' '.join(msg_parts)


def update_declaration_from_request(
        declaration: Declaration,
        request: kinder_conc.ApplicationOrderInfoRequestType
) -> tuple[bool, int | None, str]:
    """
    Заполняет данные ребенка и представителей из запроса
    ApplicationOrderInfoRequest, если в бд нет нужных данных для запроса
    OrderRequest

    :param declaration: Заявка
    :param request: Тело запроса ApplicationOrderInfoRequest

    :return: Кортеж (наличие полной информации в заявлении; id представителя,
        у которого заполнены все необходимые данные; сообщение об ошибке)
    """

    child = declaration.children
    doc_info = request.PersonIdentityDocInfo
    order_request_checker = OrderRequestRequiredFieldsChecker

    delegate_series = doc_info.IdentityDocSeries
    delegate_series_q = (
        Q(dul_series=delegate_series) if delegate_series else
        get_q('dul_series', is_empty=True)
    )

    delegate = Delegate.objects.filter(
        delegate_series_q,
        childrendelegate__children=child,
        dul_number=doc_info.IdentityDocNumber,
    ).first()

    child_empty_fields = order_request_checker.check_child(child)
    # Если есть пустые обязательные поля у ребёнка, пытаемся заполнить
    if child_empty_fields:
        child_updater = ChildApplicationOrderInfoUpdater(
            child, request)
        child_updater.run_with_error_handling()
        child_empty_fields = order_request_checker.check_child(child)

    if not delegate:
        msg = APPLICATION_ORDER_INFO_REQUEST_DELEGATE_ERROR_COMMENT
        return False, None, msg

    delegate_empty_fields = order_request_checker.check_delegate(
        delegate)
    # Если есть пустые обязательные поля у родителя, пытаемся заполнить
    if delegate_empty_fields:
        delegate_updater = (
            DelegateApplicationOrderInfoUpdater(delegate, request))
        delegate_updater.run_with_error_handling()
        delegate_empty_fields = order_request_checker.check_delegate(
            delegate)

    correct_delegate_id = delegate.id if not delegate_empty_fields else None
    has_full_info = bool(not child_empty_fields and correct_delegate_id)
    error_message = (
        '' if has_full_info else get_declaration_not_full_message(
            child_empty_fields, delegate_empty_fields)
    )

    return has_full_info, correct_delegate_id, error_message
