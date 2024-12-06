from django.db import models
from django.dispatch import receiver
from m3.db import BaseEnumerate

from kinder.core.audit_log_kndg.managers import AuditLog
from kinder.core.declaration.enum import DeclarationSourceEnum
from kinder.core.declaration.enum import DeclarationTypeInteractionEnum as DTIE
from kinder.core.declaration.models import DSS
from kinder.core.declaration.models import Declaration
from kinder.core.declaration_status.signals import declaration_status_change
from kinder.core.direct.models import Direct
from kinder.core.models import LogableModel
from kinder.webservice.smev3.models.consumer import BaseConsumerSmevRequest

from concentrator.smev3.event_service.events import NEW_DIRECT_EVENT_CODE
from concentrator.smev3.event_service.events import (
    NEW_DIRECT_EVENT_COMMENT_PATTERN)
from concentrator.smev3.event_service.events import (
    NEW_DIRECT_EVENT_FULL_COMMENT_PATTERN)
from concentrator.smev3.event_service.events import Event


@receiver(declaration_status_change, sender=Declaration)
def declaration_status_changed_handler(
        declaration,
        user,
        old_status,
        commentary,
        is_auto,
        log_id,
        reject_reason_id,
        **kwargs
):
    """Обработка смены статуса заявки на "Направлен в ДОО" и
    отправка события об изменении статуса заявки
    """

    if (
        declaration.source == DeclarationSourceEnum.CONCENTRATOR
        and declaration.type_interaction is not None
        and declaration.type_interaction == DTIE.SMEV_3
    ):

        from concentrator.smev3.event_service.helpers import (
            EventServiceSMEV3RequestManager)
        from concentrator.smev3.event_service.helpers import (
            get_event_data_for_change_status)

        for direct in declaration.direct_set.all():

            if (old_status != DSS.DIRECTED
                    and declaration.status.code == DSS.DIRECTED):

                days_for_reject_direct = (
                    direct.group.unit.get_days_for_reject_direct())

                if days_for_reject_direct:
                    event_comment = (
                        NEW_DIRECT_EVENT_FULL_COMMENT_PATTERN.format(
                            unit_name=direct.group.unit.name,
                            unit_full_address=direct.group.unit.address_full,
                            group_name=direct.group.name,
                            days_for_reject_direct=days_for_reject_direct
                        ))
                else:
                    event_comment = NEW_DIRECT_EVENT_COMMENT_PATTERN.format(
                        unit_name=direct.group.unit.name,
                        unit_full_address=direct.group.unit.address_full,
                        group_name=direct.group.name)

                event = Event(NEW_DIRECT_EVENT_CODE, event_comment)

                EventServiceSMEV3RequestManager(
                    {
                        'declaration_id': declaration.id,
                        'event': event,
                        'direct_id': direct.id
                    }).apply_async()

        event = get_event_data_for_change_status(
            old_status, declaration.status.code)
        if declaration.status.code == DSS.REFUSED:
            # неизменяемы тип, поэтому пересоздаем.
            # При автоматической смене статуса заявки комментарий отсутствует.
            event = Event(event.code, commentary or '')

        EventServiceSMEV3RequestManager(
            {
                'declaration_id': declaration.id,
                'event': event
            }).apply_async()


class ApplicantAnswersEnum(BaseEnumerate):
    """Значения поля "Ответ заявителя"."""

    values = {
        True: 'Согласен',
        False: 'Отказался'
    }


class ApplicantAnswer(LogableModel):
    """Ответ заявителя для направления. Сервис ApplicationChooseRequest."""

    direct = models.OneToOneField(
        Direct, on_delete=models.CASCADE,
        verbose_name='Направление'
    )

    answer = models.BooleanField(verbose_name='Ответ заявителя')

    audit_log = AuditLog()

    class Meta:
        verbose_name = 'Ответ заявителя'
        db_table = 'concentrator_smev3_applicantanswer'


class EventServiceRequest(BaseConsumerSmevRequest):
    """Запрос о возникновении события СМЭВ 3."""

    declaration = models.ForeignKey(Declaration, verbose_name='Заявление',
        on_delete=models.CASCADE)
    direct = models.ForeignKey(
        Direct, verbose_name='Направление', null=True, blank=True,
        on_delete=models.CASCADE)

    event_code = models.PositiveSmallIntegerField('Код события')

    event_comment = models.TextField(
        verbose_name='Комментарий события', blank=True)

    # Тело запроса
    request = models.TextField(verbose_name='Запрос', null=False, blank=False)

    request_sent = models.DateTimeField(
        verbose_name='Дата и время запроса', null=True, blank=True)

    response_returned = models.DateTimeField(
        verbose_name='Дата и время ответа', null=True, blank=True)

    audit_log = AuditLog()

    class Meta:
        verbose_name = 'Запрос о возникновении события (СМЭВ3)'
        verbose_name_plural = 'Запросы о возникновении событий (СМЭВ3)'
