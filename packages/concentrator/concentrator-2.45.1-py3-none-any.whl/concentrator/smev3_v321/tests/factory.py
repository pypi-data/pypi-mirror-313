import uuid
import factory

from aio_client.base import RequestLog
from aio_client.provider.models import GetProviderRequest
from aio_client.provider.models import PostProviderRequest

from concentrator.smev3_v321.models import ApplicantAnswer


class RequestLogF(factory.DjangoModelFactory):
    """Фабрика для создания экземпляров модели RequestLogF"""
    class Meta:
        model = RequestLog


class GetProviderRequestF(factory.DjangoModelFactory):
    """Фабрика для создания экземпляров модели GetProviderRequestF"""
    class Meta:
        model = GetProviderRequest

    request_id = factory.SubFactory(RequestLogF)
    body = ''
    is_test_message = False

    @classmethod
    def _create(cls, *args, **kwargs):
        obj = super()._create(*args, **kwargs)
        # Генерирует message_id и origin_message_id
        obj.origin_message_id = str(uuid.uuid4())
        obj.message_id = obj.origin_message_id
        obj.save()
        return obj


class PostProviderRequestF(factory.DjangoModelFactory):
    """Фабрика для создания экземпляров модели PostProviderRequestF"""
    class Meta:
        model = PostProviderRequest

    request_id = factory.SubFactory(RequestLogF)
    body = ''
    is_test_message = False


class ApplicantAnswerF(factory.DjangoModelFactory):
    """Фабрика для создания экземпляров модели ApplicantAnswer."""
    class Meta:
        model = ApplicantAnswer
