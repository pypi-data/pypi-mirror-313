from aio_client.base.signals import get_data_done
from aio_client.provider.models import GetProviderRequest
from django.dispatch import receiver

from kinder import logger

from .services import FormDataMessageProcessingService


@receiver(
    get_data_done, sender=GetProviderRequest,
    dispatch_uid='aio_client.execute_get_provider_request')
def execute_get_provider_request(**kwargs):
    """Обработчик запросов от СМЭВ (AIO)."""

    # Отправитель сигнала гасит ошибки. Залогируем их.
    try:
        FormDataMessageProcessingService().run(**kwargs)
    except Exception as exc:
        logger.error(exc)
        raise
