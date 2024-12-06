from django.db import IntegrityError
from django.db.models import OuterRef
from django.db.models import Prefetch
from django.db.models import Subquery

from aio_client.base import const as aio_base_const
from aio_client.provider.api import PostProviderRequest
from aio_client.provider.api import push_request
from m3 import ApplicationLogicException

from kinder.core.children.models import ChildrenDelegate
from kinder.core.declaration.models import Declaration
from kinder.plugins.message_exchange.models import MessageExchange
from kinder.webservice.api.declaration import get_declaration_by_client_id
from kinder.webservice.api.exceptions import ApiException

from concentrator.smev3.base.constants import SUCCESS_MESSAGE
from concentrator.smev3.base.exceptions import ContentFailure
from concentrator.smev3.base.utils import BaseExecutor
from concentrator.smev3.base.utils import SMEV3Response
from concentrator.smev3.base.utils import render_type2xml
from concentrator.smev3.base.utils import get_oktmo_region
from concentrator.smev3.base.utils import get_order_id
from concentrator.smev3.service_types import kinder_conc


class TextRequestExecutor(BaseExecutor):
    """Исполнитель сервиса textRequest."""

    name_service = 'textRequest'
    type_service = kinder_conc.textRequestType

    @classmethod
    def prepare_query(cls):
        """Выполняет подготовку запроса."""

        subquery_first_delegate = (
            ChildrenDelegate.objects.filter(
                id=Subquery(
                    ChildrenDelegate.objects.filter(
                        children_id=OuterRef('children_id')
                    ).order_by('id').values('id')[:1])
            ).select_related('delegate').only(
                'delegate__surname', 'delegate__firstname',
                'delegate__patronymic', 'children_id'))

        query = Declaration.objects.prefetch_related(
            Prefetch('children__childrendelegate_set',
                     queryset=subquery_first_delegate,
                     to_attr='first_childrendelegate'))

        return query

    @classmethod
    def process(cls, message, request_body):

        try:
            declaration = get_declaration_by_client_id(
                cls.prepare_query(),
                request_body.textRequest.orderId)
        except ApiException:
            declaration = None

        try:
            response_body = render_type2xml(
                cls.get_response(declaration, request_body.textRequest.text),
                name_type='FormDataResponse')
            content_failure_code = None
            content_failure_comment = None
        except ContentFailure as exc:
            response_body = 'null'
            content_failure_code = exc.content_failure_code
            content_failure_comment = exc.content_failure_comment
        except ApplicationLogicException as exc:
            response_body = 'null'
            content_failure_code = aio_base_const.FAILURE
            content_failure_comment = str(exc)  # exception_message

        response = push_request(PostProviderRequest(
            origin_message_id=message['origin_message_id'],
            body=response_body,
            message_type=message['message_type'],
            attachments=None,
            content_failure_code=content_failure_code,
            content_failure_comment=content_failure_comment or '',
            replay_to=message['replay_to'],
            is_test_message=message['is_test_message']
        ))

        return SMEV3Response(
            response,
            {
                'method_name': cls.name_service,
                'response': response_body,
                'result': content_failure_comment or SUCCESS_MESSAGE
            })

    @classmethod
    def get_response(cls, declaration, text):
        """Формирует ответ на textRequest.

        :param declaration: Заявление
        :type declaration: Declaration
        :param text: Текстовое сообщение
        :type text: str
        :return: ответ
        :rtype: FormDataResponseType
        :raise: ContentFailure
        """

        if not declaration:
            raise ContentFailure(
                aio_base_const.FAILURE,
                'Заявление по указанным параметрам не найдено')

        children_delegate, *_ = (
            declaration.children.first_childrendelegate or (None, ))
        if not children_delegate:
            raise ContentFailure(
                aio_base_const.FAILURE, 'Не найден представитель')
        try:
            MessageExchange.objects.create(
                declaration=declaration,
                author=children_delegate.delegate._make_full_name(),
                message=text, from_applicant=True)
        except IntegrityError:
            raise ContentFailure(
                aio_base_const.FAILURE,
                'Ошибка при обработке текстового сообщения')

        response = kinder_conc.FormDataResponseType(
            oktmo=get_oktmo_region(),
            textResponse=kinder_conc.textResponseType(
                orderId=get_order_id(declaration),
                result=kinder_conc.TextResponseResultType.OK))

        return response
