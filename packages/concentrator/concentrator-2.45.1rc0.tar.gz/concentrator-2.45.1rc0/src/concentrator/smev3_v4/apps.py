from django.apps import AppConfig


class Smev3V4Config(AppConfig):
    """Конфиг приложения"""

    name = __package__
    label = 'smev3_v4'
    verbose_name = 'СМЭВ 3 4.0.1'

    def ready(self):
        """Выполняет доп. операции, когда приложение готово.

        Выполняет регистрацию исполнителей сервисов СМЭВ (AIO).

        """
        from .executors import ApplicationAdmissionRequestExecutorV4
        from .executors import ApplicationOrderInfoRequestExecutorV4
        from .executors import ApplicationRejectionRequestExecutorV4
        from .executors import ApplicationRequestExecutorV4
        from .executors import CancelRequestExecutorV4
        from .executors import GetApplicationAdmissionRequestExecutorV4
        from .executors import GetApplicationQueueReasonRequestExecutorV4
        from .executors import GetApplicationQueueRequestExecutorV4
        from .executors import GetApplicationRequestExecutorV4
        from .executors import RepositoryExecutorsSmev3V4

        # Настройка всех исполнителей для сервисов СМЭВ3 4.0.1.
        executors = (
            ApplicationRequestExecutorV4,
            GetApplicationAdmissionRequestExecutorV4,
            ApplicationRejectionRequestExecutorV4,
            GetApplicationQueueRequestExecutorV4,
            GetApplicationRequestExecutorV4,
            CancelRequestExecutorV4,
            ApplicationOrderInfoRequestExecutorV4,
            GetApplicationQueueReasonRequestExecutorV4,
            ApplicationAdmissionRequestExecutorV4,)

        for executor in executors:
            RepositoryExecutorsSmev3V4.set_executor(executor)