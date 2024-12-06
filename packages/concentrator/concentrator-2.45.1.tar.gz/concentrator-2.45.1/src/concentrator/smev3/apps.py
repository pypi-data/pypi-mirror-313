from django.apps import AppConfig
from django.apps.registry import apps


class Smev3Config(AppConfig):

    name = 'concentrator.smev3'
    label = 'concentrator.smev3'
    verbose_name = 'СМЭВ 3'

    def ready(self):
        if apps.is_installed('concentrator.smev3_v321'):
            raise RuntimeError(
                'Плагины "concentrator.smev3" и "concentrator.smev3_v321" '
                'не могут быть подключены одновременно'
            )

        # Данные из контингента тянутся в сервисах смэв3
        if not apps.is_installed('kinder.plugins.contingent'):
            raise RuntimeError('Contingent plugin must be installed')
        # Иначе не видят таски
        import concentrator.smev3.base.tasks

        from concentrator.smev3.base.utils import SMEV3RepositoryExecutors
        from concentrator.smev3.application_choose.helpers import (
            ApplicationChooseRequestExecutor)
        from concentrator.smev3.applicationrequest.helpers import (
            ApplicationRequestExecutor)
        from concentrator.smev3.getapplication.helpers import (
            GetApplicationRequestExecutor)
        from concentrator.smev3.getapplicationqueue.helpers import (
            GetApplicationQueueRequestExecutor)
        from concentrator.smev3.cancel_request_service.helpers import (
            CancelRequestExecutor)

        config = [
            ApplicationRequestExecutor,
            ApplicationChooseRequestExecutor,
            GetApplicationRequestExecutor,
            GetApplicationQueueRequestExecutor,
            CancelRequestExecutor,
        ]

        if apps.is_installed('kinder.plugins.message_exchange'):
            from concentrator.smev3.text_request.helpers import (
                TextRequestExecutor)

            config.append(TextRequestExecutor)

        SMEV3RepositoryExecutors.set_up(config)
