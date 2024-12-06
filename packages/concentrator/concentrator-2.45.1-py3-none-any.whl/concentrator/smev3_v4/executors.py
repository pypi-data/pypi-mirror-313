from __future__ import annotations

from abc import ABC
from types import ModuleType

from concentrator.smev3_v321.application_admission_request.executors import (
    ApplicationAdmissionRequestExecutor)
from concentrator.smev3_v321.application_order_info_request.executors import (
    ApplicationOrderInfoRequestExecutor)
from concentrator.smev3_v321.application_rejection_request.executors import (
    ApplicationRejectionRequestExecutor)
from concentrator.smev3_v321.application_request.executors import (
    ApplicationRequestExecutor)
from concentrator.smev3_v321.cancel_request.executors import (
    CancelRequestExecutor)
from concentrator.smev3_v321.exceptions import ExecutorRegistered
from concentrator.smev3_v321.executors import AbstractExecutor
from concentrator.smev3_v321.get_application_admission_request.executors import (
    GetApplicationAdmissionRequestExecutor)
from concentrator.smev3_v321.get_application_queue.executors import (
    GetApplicationQueueRequestExecutor)
from concentrator.smev3_v321.get_application_queue_reason_request.executors import (
    GetApplicationQueueReasonRequestExecutor)
from concentrator.smev3_v321.get_application_request.executors import (
    GetApplicationRequestExecutor)
from concentrator.smev3_v321.model import AbstractRequestMessage
from concentrator.smev3_v4.service_types import kinder_conc4

class AbstractExecutorV4(AbstractExecutor, ABC):
    """Абстрактный класс исполнителя сервиса СМЭВ3 4.0.1"""
    parser_module: ModuleType = kinder_conc4


class RepositoryExecutorsSmev3V4:
    """Хранилище исполнителей сервисов СМЭВ3 4.0.1"""

    __store: dict[str, type[AbstractExecutorV4]] = {}

    @classmethod
    def set_executor(cls, executor: type[AbstractExecutorV4]):
        """Добавляет исполнителя в хранилище исполнителей.

        :param executor: Исполнитель сервиса.

        """

        if executor.service_type_name in cls.__store:
            raise ExecutorRegistered(executor)

        cls.__store[executor.service_type_name] = executor

    @classmethod
    def get_executor(
            cls, message: AbstractRequestMessage
    ) -> type[AbstractExecutor] | None:
        """Определяет исполнителя для полученного сообщения.

        :param message: Сообщение СМЭВ (AIO).

        :return: Возвращает исполнителя для указанного сообщения СМЭВ,
            если он задан в хранилище.

        """
        return cls.__store.get(message.service_type_name)


class ApplicationRequestExecutorV4(ApplicationRequestExecutor, AbstractExecutorV4):
    """Исполнитель сервиса ApplicationRequest СМЭВ3 4.0.1"""
    service_type_name: str = kinder_conc4.ApplicationType.__name__

class ApplicationRejectionRequestExecutorV4(ApplicationRejectionRequestExecutor, AbstractExecutorV4):
    """Исполнитель сервиса ApplicationRejectionRequest СМЭВ3 4.0.1"""
    service_type_name: str = kinder_conc4.ApplicationRejectionRequestType.__name__

class ApplicationOrderInfoRequestExecutorV4(ApplicationOrderInfoRequestExecutor, AbstractExecutorV4):
    """Исполнитель сервиса ApplicationOrderInfoRequest СМЭВ3 4.0.1"""
    service_type_name: str = kinder_conc4.ApplicationOrderInfoRequestType.__name__

class ApplicationAdmissionRequestExecutorV4(ApplicationAdmissionRequestExecutor, AbstractExecutorV4):
    """Исполнитель сервиса ApplicationAdmissionRequest СМЭВ3 4.0.1"""
    service_type_name: str = kinder_conc4.ApplicationAdmissionRequestType.__name__

class CancelRequestExecutorV4(CancelRequestExecutor, AbstractExecutorV4):
    """Исполнитель сервиса CancelRequest СМЭВ3 4.0.1"""
    service_type_name: str = kinder_conc4.cancelRequestType.__name__

class GetApplicationAdmissionRequestExecutorV4(GetApplicationAdmissionRequestExecutor, AbstractExecutorV4):
    """Исполнитель сервиса GetApplicationAdmissionRequest СМЭВ3 4.0.1"""
    service_type_name: str = kinder_conc4.GetApplicationAdmissionRequestType.__name__

class GetApplicationQueueRequestExecutorV4(GetApplicationQueueRequestExecutor, AbstractExecutorV4):
    """Исполнитель сервиса GetApplicationQueueRequest СМЭВ3 4.0.1"""
    service_type_name: str = kinder_conc4.GetApplicationQueueRequestType.__name__

class GetApplicationQueueReasonRequestExecutorV4(GetApplicationQueueReasonRequestExecutor, AbstractExecutorV4):
    """Исполнитель сервиса GetApplicationQueueReasonRequest СМЭВ3 4.0.1"""
    service_type_name: str = kinder_conc4.GetApplicationQueueReasonRequestType.__name__

class GetApplicationRequestExecutorV4(GetApplicationRequestExecutor, AbstractExecutorV4):
    """Исполнитель сервиса GetApplicationRequest СМЭВ3 4.0.1"""
    service_type_name: str = kinder_conc4.GetApplicationRequestType.__name__
