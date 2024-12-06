import copy
from contextlib import suppress
from datetime import datetime

from django.db import models

from m3.db import BaseEnumerate
from m3.plugins import ExtensionManager

from kinder.core.audit_log_kndg.managers import AuditLog
from kinder.core.declaration.models import Declaration
from kinder.core.direct.models import Direct
from kinder.core.models import DateAwareModel
from kinder.core.children.models import ChildrenDelegate
from kinder.core.models import LogableModel
from kinder.core.models import RawJSONField
from kinder.core.helpers import AdditionalEncoder
from kinder.webservice.smev3.models.consumer import BaseConsumerSmevRequest

from .esnsi.classifiers import EduControlUnitClassifier
from .esnsi.classifiers import MaxDooClassifier
from .esnsi.classifiers import UnitClassifier
from .order.enums import PendingUpdateOrderRequestSourceVersionEnum


class ESNSIClassifier(LogableModel):
    """Справочники для передачи в ЕСНСИ"""

    audit_log = AuditLog()

    classifiers_classes = (
        UnitClassifier,
        MaxDooClassifier,
        EduControlUnitClassifier,
    )

    classifiers_classes_choices = (
        (UnitClassifier.__name__, 'Организации (детсады)'),
        (MaxDooClassifier.__name__,
         'Максимальное количество детсадов, которое может выбрать заявитель'),
        (EduControlUnitClassifier.__name__, 'Органы управления образованием')
    )

    uid = models.CharField(
        'Уникальный идентификатор классификатора', max_length=36,
        null=True, blank=True
    )

    code = models.CharField(
        'Код классификатора', max_length=100, null=True, blank=True
    )

    name = models.CharField(
        'Наименование справочника', max_length=250, default='',
    )

    classifier_class = models.CharField(
        'Класс классификатора', max_length=50, default='', unique=True,
        choices=classifiers_classes_choices
    )

    class Meta:
        verbose_name = 'Справочник для передачи в ЕСНСИ (СМЭВ 3)'
        verbose_name_plural = 'Справочник для передачи в ЕСНСИ (СМЭВ 3)'
        app_label = 'smev3_v321'
        db_table = 'concentrator_smev3_v321_esnsiclassifier'

    def get_model_by_classifier_name(self, classifier_name):
        for cl in self.classifiers_classes:
            if cl.__name__ == classifier_name:
                return cl.model

    def get_classifier_class_by_name(self):
        """Возвращает класс классификатора по наименованию."""
        for cl in self.classifiers_classes:
            if cl.__name__ == self.classifier_class:
                return cl


class UpdateClassifierRequest(BaseConsumerSmevRequest):
    """
    Запрос отправки справочника в ЕСНСИ
    """

    audit_log = AuditLog()

    RESULT_SUCCESS = 1
    RESULT_FAILURE = 2

    RESULT_CHOICES = (
        (RESULT_SUCCESS, 'Успешно'),
        (RESULT_FAILURE, 'Ошибка'),
    )

    UPDATE_CLASSIFIERS = 'update'
    DELETE_CLASSIFIERS = 'delete'

    REQUEST_TYPE_CHOICES = (
        (UPDATE_CLASSIFIERS, 'Обновление данных справочника'),
        (DELETE_CLASSIFIERS, 'Удаление данных справочника'),
    )

    request_result = models.PositiveSmallIntegerField(
        verbose_name='Результат',
        choices=RESULT_CHOICES,
        null=True, blank=True
    )

    request_sent = models.DateTimeField(
        verbose_name='Дата и время запроса',
        null=True, blank=True
    )

    response_returned = models.DateTimeField(
        verbose_name='Дата и время ответа',
        null=True, blank=True
    )

    request_type = models.CharField(
        verbose_name='Тип запроса',
        max_length=32,
        choices=REQUEST_TYPE_CHOICES
    )
    classifier = models.ForeignKey(
        'smev3_v321.ESNSIClassifier',
        blank=True, null=True,
        on_delete=models.CASCADE
    )

    data = RawJSONField(
        verbose_name='Данные запроса',
        null=False, blank=False
    )

    class Meta:
        verbose_name = 'Запрос на обновление данных в ЕСНСИ (СМЭВ 3)'
        verbose_name_plural = 'Запросы на обновление данных в ЕСНСИ (СМЭВ 3)'
        app_label = 'smev3_v321'
        db_table = 'concentrator_smev3_v321_updateclassifierrequest'


class ApplicantAnswersEnum(BaseEnumerate):
    """Значения поля "Ответ заявителя"."""

    values = {
        True: 'Согласен',
        False: 'Отказался',
    }

    # Словарь со значениями для использования в фильтре в реестре направлений
    values_for_filter = values.copy()
    values_for_filter['empty'] = 'Пусто'


class ApplicantAnswer(LogableModel):
    """Ответ заявителя для направления."""

    direct = models.OneToOneField(
        Direct, on_delete=models.CASCADE,
        related_name='smev3_v321_applicant_answer',
        verbose_name='Направление'
    )

    answer = models.BooleanField(verbose_name='Ответ заявителя')

    comment = models.CharField(
        max_length=2048, null=True, blank=True,
        verbose_name='Комментарий заявителя',
    )

    audit_log = AuditLog()

    class Meta:
        verbose_name = 'Ответ заявителя'
        db_table = 'concentrator_smev3_v321_applicantanswer'


class AttachmentRequest(BaseConsumerSmevRequest):
    """
    Запросы по взаимодействию с ВС 
    "Получение списков детей, получивших места в дошкольных организациях"
    """

    class Meta:
        verbose_name = 'Запрос по взаимодействию с ВС AttachmentRequest'
        verbose_name_plural = (
            'Запросы по взаимодействию с ВС AttachmentRequest')


class DeclarationOriginMessageID(models.Model):
    """
    Модель для хранения идентификаторов запроса
    при подаче заявления в методе Application Request,
    и при создании через  GetApplicationRequest
    """

    message_id = models.CharField(
        max_length=100, null=True,
        verbose_name='Уникальный идентификатор сообщения', db_index=True)
    replay_to = models.CharField(
        max_length=4000, verbose_name='Индекс сообщения в СМЭВ', null=True)
    declaration = models.OneToOneField(Declaration, models.CASCADE)
    reviewed_sent = models.BooleanField(
        'Показатель отправки сообщения changeOrderInfo', default=False)

    class Meta:
        verbose_name = (
            'Связь заявления и идентификатора запроса '
            'ApplicationOrderInfoRequest')
        verbose_name_plural = (
            'Связи заявления и идентификатора запроса '
            'ApplicationOrderInfoRequest')


class OrderRequest(BaseConsumerSmevRequest):
    """
    Запросы по взаимодействию с ВС
    "Передача заявлений на запись в дошкольную организацию".
    """

    request_order_id = models.CharField(
        'Order_id запроса', max_length=100, null=True
    )

    declaration = models.OneToOneField(
        Declaration, verbose_name='Заявление', on_delete=models.CASCADE
    )

    order_id = models.CharField(
        'Идентификатор заявления в концентраторе СМЭВ 3',
        max_length=100, null=True
    )

    class Meta:
        verbose_name = 'Запрос передачи данных заявления в ЛК ЕПГУ'
        db_table = 'concentrator_smev3_v321_orderrequest'


class UpdateOrderRequest(BaseConsumerSmevRequest):
    """
    Запросы по взаимодействию с ВС
    "Передача заявлений на запись в дошкольную организацию".
    """

    declaration = models.ForeignKey(
        Declaration, verbose_name='Заявление', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = (
            'Запрос передачи данных об изменении статуса заявления в ЛК ЕПГУ')
        db_table = 'concentrator_smev3_v321_updateorderrequest'


class DeclarationPortalID(models.Model):
    """
    Модель для хранения связи заявлений с идентификатором заявлений на портале.
    Необходима для того, чтобы идентифицировать заявления не только по
    client_id, но и по portal_id, если такие заявления были сопоставлены.
    Таблица заполняется менедж-командой smev3_import_declarations, после чего
    запросы BC FormData с блоками:
    ApplicationRequest
    GetApplicationQueueRequest
    GetApplicationQueueReasonRequest
    GetApplicationRequest
    GetApplicationAdmissionRequest
    ApplicationRejectionRequest
    cancelRequest
    ApplicationAdmissionRequest
    должны при получении в тэге order_id сопоставляться с заявлениями как
    по значению client_id, так и по значению portal_id,
    """

    portal_id = models.CharField(
        max_length=100, unique=True,
        verbose_name='Идентифкатор заявления на портале')
    declaration = models.OneToOneField(Declaration, models.CASCADE)

    class Meta:
        verbose_name = 'Связь заявлений с идентификатором на портале'
        verbose_name = 'Связи заявлений с идентификаторами на портале'


class PendingUpdateOrderRequest(DateAwareModel):
    """Отложенный запрос передачи данных об изменении статуса заявления
    в ЛК ЕПГУ.
    """

    order_request = models.ForeignKey(
        OrderRequest,
        verbose_name='Запрос передачи данных заявления в ЛК ЕПГУ',
        on_delete=models.CASCADE)

    source_version = models.PositiveSmallIntegerField(
        'Версия источника',
        choices=PendingUpdateOrderRequestSourceVersionEnum.get_choices())

    data = models.JSONField(
        verbose_name='Данные для отправки данных об изменении',
        encoder=AdditionalEncoder, null=True, blank=True, default=dict)

    class Meta:
        verbose_name = (
            'Отложенный запрос передачи данных об изменении '
            'статуса заявления в ЛК ЕПГУ')
        db_table = 'concentrator_smev3_v321_pendingupdateorderrequest'

    @property
    def decoded_data(self):
        """Получает декодированные данные JSON, преобразует строки в объекты."""
        if self.data is None:
            return self.data

        data = copy.deepcopy(self.data)
        if isinstance(data, dict) and 'direct_status_log' in data:
            created_at = data['direct_status_log'].get('created_at')
            if isinstance(created_at, str):
                with suppress(ValueError):
                    data['direct_status_log']['created_at'] = (
                        datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S'))

        return data


class ExtendedChildrenDelegate(LogableModel):
    """Расширенная модель Представителя ребенка.

    Содержит поля:
        1. Идентификатор (order_id),
            который является идентфикатором запроса СМЭВ 3
            и идентификатором заявления. Необходим для корректной работы
            сервиса приема заявлений (ApplicationRequest) для однозначного
            определения представителя при обновлении данных ранее
            поданного заявления.

            Сервис СМЭВ работает только с одним представителем, а ЭДС
            со множеством (просто полезно помнить).

    """

    children_delegate = models.OneToOneField(
        ChildrenDelegate, verbose_name='Представитель ребенка',
        on_delete=models.CASCADE)

    order_id = models.CharField(
        max_length=100, unique=True, verbose_name='Идентификатор')

    audit_log = AuditLog()

    class Meta:
        verbose_name = 'Дополнительные данные представителя ребенка (СМЭВ 3)'
        db_table = 'concentrator_smev3_v321_children_delegate'
