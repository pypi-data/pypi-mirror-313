import datetime

from django.db import IntegrityError
from django.db.models import Q

from aio_client.base import const as aio_base_const
from aio_client.provider.api import PostProviderRequest
from aio_client.provider.api import push_request

from kinder.core.direct.models import DRS
from kinder.core.direct.models import Direct
from kinder.core.unit.models import Unit
from kinder.webservice.api.declaration import get_decl_by_client_id
from kinder.webservice.api.exceptions import ApiException

from concentrator.smev3.base.constants import SUCCESS_MESSAGE
from concentrator.smev3.base.exceptions import ContentFailure
from concentrator.smev3.base.utils import BaseExecutor
from concentrator.smev3.base.utils import SMEV3Response
from concentrator.smev3.base.utils import get_oktmo_region
from concentrator.smev3.base.utils import get_order_id
from concentrator.smev3.base.utils import render_type2xml
from concentrator.smev3.event_service import events
from concentrator.smev3.event_service.helpers import (
    EventServiceSMEV3RequestManager)
from concentrator.smev3.models import ApplicantAnswer
from concentrator.smev3.models import EventServiceRequest
from concentrator.smev3.service_types import kinder_conc

from . import constants


class ApplicationChooseRequestExecutor(BaseExecutor):
    """Исполнитель сервиса ApplicationChooseRequest."""

    name_service = 'ApplicationChooseRequest'
    type_service = kinder_conc.ApplicationChooseRequestType

    @classmethod
    def process(cls, message, request_body):

        try:
            declaration = get_decl_by_client_id(
                request_body.ApplicationChooseRequest.orderId)
        except ApiException:
            declaration = None

        doo_code = request_body.ApplicationChooseRequest.EduOrganizationCode
        answer = request_body.ApplicationChooseRequest.EduOrganizationAnswer

        try:
            response_body = render_type2xml(
                cls.get_response(declaration, doo_code, answer),
                name_type='FormDataResponse')
            content_failure_code = None
            content_failure_comment = None
        except ContentFailure as exc:
            response_body = 'null'
            content_failure_code = exc.content_failure_code
            content_failure_comment = exc.content_failure_comment

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
    def get_response(cls, declaration, doo_code, answer):
        """Формирует ответ на ApplicationChooseRequest.

        :param declaration: Заявление
        :type declaration: Declaration
        :param doo_code: Идентификатор ДОО
        :type doo_code: int
        :param answer: Признак согласия заявителя
        :type answer: bool

        :return: Сформированный ответ
        :rtype: FormDataResponseType

        :raise: ContentFailure
        """

        if not declaration:
            raise ContentFailure(
                aio_base_const.FAILURE,
                'Заявление по указанным параметрам не найдено')

        try:
            unit = Unit.objects.get(id=doo_code)
        except (Unit.DoesNotExist, Unit.MultipleObjectsReturned):
            raise ContentFailure(
                aio_base_const.FAILURE,
                'Организация по указанным параметрам не найдена')

        event_service_request = (
            EventServiceRequest.objects.filter(
                declaration=declaration,
                direct__group__unit__id=doo_code,
                event_code=events.NEW_DIRECT_EVENT_CODE,
                request_sent__isnull=False
            ).values_list('request_sent', flat=True).order_by('id').last())

        days_for_reject_direct = unit.get_days_for_reject_direct()

        if (
            event_service_request
            and days_for_reject_direct
            and (datetime.date.today() - event_service_request.date()
                 > datetime.timedelta(days_for_reject_direct))
        ):
            result_status_code = constants.APPLICATION_CHOOSE_ERROR_CODE
            result_comment = constants.APPLICATION_CHOOSE_ERROR_COMMENT
        else:

            cls.application_choose_process(declaration, doo_code, answer)
            result_status_code = constants.APPLICATION_CHOOSE_SUCCESS_CODE
            result_comment = constants.APPLICATION_CHOOSE_SUCCESS_COMMENT

            if answer:
                event = events.ACCEPT_DIRECT_EVENT
            else:
                event = events.REJECT_DIRECT_EVENT

            # Отправляет запрос о событии
            EventServiceSMEV3RequestManager(
                {
                    'declaration_id': declaration.id,
                    'event': event
                }).apply_async()

        response = kinder_conc.FormDataResponseType(
            oktmo=get_oktmo_region(),
            changeOrderInfo=kinder_conc.changeOrderInfoType(
                orderId=kinder_conc.orderIdType(get_order_id(declaration)),
                statusCode=kinder_conc.statusCodeType(result_status_code),
                comment=result_comment))

        return response

    @classmethod
    def application_choose_process(cls, declaration, doo_code, answer):
        """Обработка ответа пользователя.

        :param declaration: Заявление
        :type declaration: Declaration
        :param doo_code: Идентификатор ДОО
        :type doo_code: int
        :param answer: Признак согласия заявителя
        :type answer: bool

        :raise: ContentFailure
        """

        try:
            direct = (
                Direct.objects.get(
                    ~Q(status__code__in=(
                        DRS.ACCEPT,
                        DRS.REJECT,
                        DRS.REFUSED,
                    )),
                    group__unit__id=doo_code,
                    declaration=declaration))
        except (Direct.DoesNotExist, Direct.MultipleObjectsReturned):
            raise ContentFailure(
                aio_base_const.FAILURE,
                'Направление по указанным параметрам не найдено')

        applicant_answer = (
            ApplicantAnswer.objects.filter(direct=direct).first())

        try:
            if applicant_answer:
                applicant_answer.answer = answer
                applicant_answer.save()
            else:
                ApplicantAnswer.objects.create(direct=direct, answer=answer)
        except IntegrityError:
            raise ContentFailure(
                aio_base_const.FAILURE,
                'Ошибка при обработке ответа заявителя')
