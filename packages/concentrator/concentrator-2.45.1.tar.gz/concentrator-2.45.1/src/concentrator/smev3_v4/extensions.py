from __future__ import annotations

from types import ModuleType
from typing import Any

from concentrator.smev3_v321.model import FormDataMessage
from concentrator.smev3_v321.esnsi.classifiers import FieldInfo
from concentrator.smev3_v321.esnsi.classifiers import MaxDooClassifier
from concentrator.smev3_v321.esnsi.enums import DataTypesEnum as DT
from concentrator.smev3_v4.executors import RepositoryExecutorsSmev3V4
from concentrator.smev3_v4.utils import check_v4_message
from concentrator.smev3_v4.order.builders import OrderRequestBuilderV101
from concentrator.smev3_v4.order.builders import UpdateOrderRequestBuilderV101
from concentrator.smev3_v4.service_types import kinder_conc4
from concentrator.smev3_v4.service_types.kinder_conc4 import EduOrganizationDataType

from kinder.core.declaration.models import Declaration
from kinder.core.unit.models import Unit
from kinder.core.unit.models import UnitKind
from kinder.core.dict.models import WorkTypeEnumerate


def get_parsing_module(message: str = '', ext_result: Any = None) -> kinder_conc4:
    """Возвращает модуль для парсинга запроса по СМЭВ3 4.0.1,
    если запрос этой версии
    """

    if message and not check_v4_message(message):
        return

    return kinder_conc4

def service_type_smev4(ext_result: Any) -> type[kinder_conc4.GeneratedsSuper]:
    """Возвращает базовый тип объектов запроса версии СМЭВ3 4.0.1"""

    return kinder_conc4.GeneratedsSuper

def get_executors(
        message: FormDataMessage, ext_result: Any
) -> type[RepositoryExecutorsSmev3V4]:

    """Получение исполнителей запросов для версии СМЭВ3 4.0.1"""

    if check_v4_message(message.body):
        return RepositoryExecutorsSmev3V4

def get_unit_params(
        parser_module: ModuleType, declaration: Declaration, ext_result: Any
) -> dict[str, EduOrganizationDataType] | None:

    """Возвращает EduOrganizationDataType для версии запроса СМЭВ3 4.0.1

    :param declaration: Заявление
    :param parser_module: Модуль парсинга запроса
    :return: Словарь параметров
    """
    if parser_module == kinder_conc4:
        return {
            'EduOrganizationData': EduOrganizationDataType(
                EduOrganizationCode=declaration.unit_code,
                EduOrganizationName=declaration.unit_name
            )
        }

def get_agreement_on_other_group(declaration: Declaration, ext_result: Any) -> bool:

    """Возвращает значение AgreementOnOtherDayGroup для версии запроса СМЭВ3 4.0.1

    :param declaration: Заявление
    :return: Согласие на зачисление в группы с другим режимом
    """
    decl_work_type = declaration.work_type

    if not decl_work_type:
        return False

    return (
        decl_work_type.code == WorkTypeEnumerate.FULL and declaration.consent_short_time_group or
        decl_work_type.code == WorkTypeEnumerate.ALLDAY and declaration.consent_full_time_group
    )

def get_order_request_builder(
    parser_module: str, ext_result: Any) -> type[OrderRequestBuilderV101] | None:
    """Возвращает модуль для парсинга запроса по СМЭВ3 4.0.1"""

    if parser_module == kinder_conc4.__name__:
        return OrderRequestBuilderV101

def get_update_order_request_builder(
    parser_module: str, ext_result: Any) -> type[UpdateOrderRequestBuilderV101] | None:
    """Возвращает модуль для парсинга запроса по СМЭВ3 4.0.1"""

    if parser_module == kinder_conc4.__name__:
        return UpdateOrderRequestBuilderV101


def extend_esnsi_classifier_fields(classifier: type, fields: dict, ext_result: Any) -> None:
    """Добавляет дополнительные поля в справочник ЕСНСИ"""
    if classifier is MaxDooClassifier:
        fields.update(
            EDU_DEPARTMENT_OKTMO=FieldInfo(type=DT.STRING, length=500, required=True)
        )


def extend_esnsi_classifier_data(classifier: type, obj: Any, data: dict, ext_result: Any) -> None:
    """Добавляет поля в итоговые данные"""
    region = Unit.objects.filter(kind_id=UnitKind.REGION).first()
    if classifier is MaxDooClassifier:
        data.update(
            EDU_DEPARTMENT_OKTMO=region.octmo
        )
