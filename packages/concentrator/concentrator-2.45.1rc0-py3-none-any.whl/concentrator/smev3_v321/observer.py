from datetime import timedelta

from django.apps.registry import apps
from django.db import transaction

from kinder.core.children.models import Children
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import DeclarationStatusLog
from kinder.core.declaration.models import DeclarationUnit
from kinder.core.declaration_status.enum import DSS
from kinder.core.direct.models import DirectStatusLog
from kinder.core.direct.models import DRS
from kinder.core.direct.models import TEXT_CHANGE_STATUS
from kinder.core.observer import ChangesObserver
from kinder.core.unit.models import Unit
from kinder.core.unit.models import UnitStatus
from kinder.core.dict.models import UnitKind

from concentrator.models import ChangeDeclaration
from concentrator.models import ChangeStatus

from .base.tasks import PushChangeOrderInfoRequestTask
from .constants import DECLARATION_CHANGES_REFUSED_CODE
from .constants import DECLARATION_CHANGES_REFUSED_COMMENT
from .constants import NO_REQUEST_REQUIRED_DIRECT_STATUSES
from .esnsi.classifiers import EduControlUnitClassifier
from .esnsi.classifiers import MaxDooClassifier
from .esnsi.classifiers import UnitClassifier
from .esnsi.helpers import ESNSIUnitTaskFactory
from .esnsi.helpers import get_classifier_instance
from .utils import send_order_info_for_declaration
from .models import DeclarationOriginMessageID
from .models import OrderRequest
from .models import UpdateClassifierRequest
from .order.enums import PendingUpdateOrderRequestSourceVersionEnum
from .order.helpers import DispatchOrderRequestSMEV3RequestManager


class _ChangesObserver(ChangesObserver):
    """Класс для отслеживания изменения значений полей объектов моделей.

    Добавлена версия источника.
    """

    source_version = None


class DeclarationStatusChangesObserver(_ChangesObserver):
    """
    Класс для отправки запроса UpdateOrderRequest при изменении
    статуса заявления.
    """

    model = Declaration
    tracked_fields = ['status']
    source_version = PendingUpdateOrderRequestSourceVersionEnum.V_2

    def post_save(self, instance, created, **kwargs):
        """
        Отправляет запрос UpdateOrderRequest при изменении
        статуса заявления
        """

        try:
            order_request = instance.orderrequest
        except OrderRequest.DoesNotExist:
            return

        if not self.has_changes(instance):
            return

        old_status, new_status = self.get_changes(instance)['status']

        last_status_log = instance.declarationstatuslog_set.order_by(
            'datetime').last()
        auto_change = (
            last_status_log and last_status_log.comment == TEXT_CHANGE_STATUS)
        auto_change_to_directed = (
                new_status.code == DSS.DIRECTED and auto_change)
        # При авто-смене статуса заявления на Не явился обрабатываем отправку
        # OrderRequest в observer для смены статуса направления
        # При смене статуса с Зачислен на Архивная не отправляем запрос
        status_not_send = (
            new_status.code == DSS.DIDNT_COME or (
            old_status.code == DSS.ACCEPTED and new_status.code == DSS.ARCHIVE)
        )
        # Если произошла авто-смена на Направлен в ДОО, не отправляем запрос
        # повторно
        if not created and not status_not_send and not auto_change_to_directed:
            DispatchOrderRequestSMEV3RequestManager(
                order_request, self.source_version,
                {
                    'declaration_id': instance.id,
                    'declaration_status_changed': True
                }).run()


class DeclarationStatusLogObserver(ChangesObserver):
    """
    Класс для отправки запроса changeOrderInfo при изменении
    статуса заявления.
    """

    model = DeclarationStatusLog

    def post_save(self, instance, created, **kwargs):
        """
        Отправляет запрос changeOrderInfo при изменении
        статуса заявления
        """

        send_order_info_for_declaration(instance)


class ChangeDeclarationObserver(ChangesObserver):
    """
    Класс для отправки запроса при отклонении изменений заявления
    """

    model = ChangeDeclaration
    tracked_fields = ['state']

    def post_save(self, instance, created, **kwargs):
        """
        Отправляет запрос ChangeOrderInfo при отклонении
        изменений заявления
        """

        declaration_message_id = DeclarationOriginMessageID.objects.filter(
            declaration=instance.declaration).first()

        if created or not declaration_message_id:
            return

        if instance.state == ChangeStatus.REJECT:
            message_id = declaration_message_id.message_id
            org_code = DECLARATION_CHANGES_REFUSED_CODE
            comment = DECLARATION_CHANGES_REFUSED_COMMENT.format(
                comment=instance.commentary)
            transaction.on_commit(
                lambda: PushChangeOrderInfoRequestTask().apply_async(
                    (instance.declaration_id, org_code, comment, message_id,
                     declaration_message_id.replay_to)
                )
            )

        declaration_log = DeclarationStatusLog.objects.filter(
            declaration=instance.declaration).order_by('datetime').last()

        if declaration_log:
            send_order_info_for_declaration(declaration_log)


class DeclarationFieldsChangesObserver(_ChangesObserver):
    """
    Класс для отправки запроса UpdateOrderRequest при изменении полей
    заявления, кроме статуса, используемых в сервисе OrderRequest.
    """

    model = Declaration
    tracked_fields = [
        'date', 'desired_date', 'spec', 'work_type', 'children',
        'consent_full_time_group', 'desired_group_type', 'consent_dev_group',
        'consent_care_group', 'offer_other', 'best_privilege'
    ]
    source_version = PendingUpdateOrderRequestSourceVersionEnum.V_3

    def post_save(self, instance, created, **kwargs):

        try:
            order_request = instance.orderrequest
        except OrderRequest.DoesNotExist:
            return

        if self.has_changes(instance) and not created:

            DispatchOrderRequestSMEV3RequestManager(
                order_request, self.source_version,
                {'declaration_id': instance.id}).run()


class DeclarationUnitChangesObserver(_ChangesObserver):
    """
    Класс для отправки запроса UpdateOrderRequest при изменении полей
    желаемых учреждений заявления.
    """

    model = DeclarationUnit
    source_version = PendingUpdateOrderRequestSourceVersionEnum.V_4

    def post_save(self, instance, created, **kwargs):

        try:
            order_request = instance.declaration.orderrequest
        except OrderRequest.DoesNotExist:
            return

        if not created:

            DispatchOrderRequestSMEV3RequestManager(
                order_request, self.source_version,
                {'declaration_id': instance.declaration.id}).run()


class DirectStatusChangesObserver(_ChangesObserver):
    """
    Класс для отправки запроса UpdateOrderRequest при изменении статуса
    направления.
    """

    model = DirectStatusLog
    source_version = PendingUpdateOrderRequestSourceVersionEnum.V_5

    def post_save(self, instance, created, **kwargs):

        try:
            order_request = instance.direct.declaration.orderrequest
        except OrderRequest.DoesNotExist:
            order_request = None

        # Если статус направления сменился на Заключение договора, Не явился
        # Направлен в ДОО, отправляем UpdateOrderRequest
        transition_to_dogovor_status = instance.status.code in [
            DRS.DOGOVOR, DRS.REJECT, DRS.REGISTER]

        if order_request and (not created or transition_to_dogovor_status):

            DispatchOrderRequestSMEV3RequestManager(
                order_request, self.source_version,
                {
                    'declaration_id': instance.direct.declaration.id,
                    'direct': instance.direct.id,
                    'direct_status_log': {
                        'id': instance.id,
                        'old_status': instance.old_status.code,
                        'status': instance.status.code,
                        'created_at': instance.created_at
                    }
                }).run()

        declaration_message_id = DeclarationOriginMessageID.objects.filter(
            declaration=instance.direct.declaration).first()

        last_log_query = DeclarationStatusLog.objects.filter(
            declaration=instance.direct.declaration,
            datetime__gte=instance.created_at - timedelta(seconds=1)
        )
        declaration_changed = (
                last_log_query.exists() and
                last_log_query.latest('datetime').status.code in
                DSS.status_queue_full())
        if not instance.old_status or not declaration_message_id or (
                instance.old_status == instance.status) or (
                instance.status.code in NO_REQUEST_REQUIRED_DIRECT_STATUSES
        ) or declaration_changed:
            return

        message_id = declaration_message_id.message_id
        transaction.on_commit(
            lambda: PushChangeOrderInfoRequestTask().apply_async(
                (instance.direct.declaration_id, None, None,
                 message_id, declaration_message_id.replay_to,
                 PushChangeOrderInfoRequestTask.DIRECT_TYPE,
                 instance.direct_id)
            )
        )


class ChildrenChangesObserver(_ChangesObserver):
    """
    Класс для отправки запроса UpdateOrderRequest при изменении данных ребенка.
    """

    model = Children
    tracked_fields = [
        'surname', 'firstname', 'patronymic', 'date_of_birth',  'dul_series',
        'dul_number', 'dul_date', 'zags_act_number', 'zags_act_date',
        'zags_act_place', 'dul_type', 'reg_address_place',
        'reg_address_street', 'reg_address_house_guid', 'reg_address_full',
        'health_need', 'health_need_special_support', 'health_series',
        'health_number', 'health_need_start_date', 'health_issued_by',
        'health_need_expiration_date',
    ]
    source_version = PendingUpdateOrderRequestSourceVersionEnum.V_6

    def post_save(self, instance, created, **kwargs):
        for declaration in instance.declaration_set.all():
            try:
                order_request = declaration.orderrequest
            except OrderRequest.DoesNotExist:
                continue

            if self.has_changes(instance) and not created:

                DispatchOrderRequestSMEV3RequestManager(
                    order_request, self.source_version,
                    {'declaration_id': declaration.id}).run()


class UnitObserver(ChangesObserver):
    """Класс для отправки запроса при изменении и удалении организации (ДОО).

    При наличии изменений определённых полей
    (Наименование, Адрес, Код ФИАС населенного пункта, Телефон, E-mail,
    Часы работы, ОКТМО, Адрес сайта)
    организации (ДОО) отправляется запрос CnsiRequest
    с вложением ClassifierDataUpdateRequest.

    При удаление организации (ДОО), при изменении статуса на ("Закрыто",
    "Ликвидировано", "Присоединена к другой организации")
    или проставлении признака "Не показывать на портале" отправляется
    запрос CnsiRequest с вложением ClassifierDataDeleteRequest.
    """

    model = Unit

    tracked_fields = [
        'name', 'address_full', 'address_place', 'telephone', 'email',
        'reception_time', 'octmo', 'site',
    ]

    unit_kind = UnitKind.DOU

    def pre_save(self, instance, context, **kwargs):
        """Сохраняется словарь с параметрами объекта до сохранения.

        Дополнительно сохраняет в инстансе атрибуты:
            1. esnsi_created - Признак того, что объект был создан в ЕСНСИ;
            2. esnsi_remove - Признак того, что объект возможно следует
                удалить в ЕСНСИ;
        """

        if not self.tracked_fields:
            self._pre_saved_instance_dict = {}

        elif instance.id is None:
            self._pre_saved_instance_dict = (
                self.get_instance_dict(instance, True))

            # Проставляет признак того, что новая организация еще
            # не создана в ЕСНСИ.
            instance.esnsi_created = False

        else:
            obj = self.model.objects.filter(id=instance.id).first()

            self._pre_saved_instance_dict = (
                self.get_instance_dict(obj) if obj else None)

            # Проставляет признак того, что организация была создана.
            # Если в БД у нее статус ("Закрыто", "Ликвидировано",
            # "Присоединена к другой организации") или проставлен чек-бокс
            # "Не показывать на портале".
            instance.esnsi_created = not (
                    obj.status in UnitStatus.ALL_CLOSED_STATUS
                    or obj.is_not_show_on_poral)

        # Если текущий статус организации:
        # "Закрыто", "Ликвидировано", "Присоединена к другой организации"
        # или проставлен чек-бокс "Не показывать на портале",
        # то проставляет признак возможного удаления.
        instance.esnsi_remove = (
                instance.status in UnitStatus.ALL_CLOSED_STATUS
                or instance.is_not_show_on_poral)

    def validate(self, instance):
        """Выполняет валидацию объекта.

        След. проверки:
            1. Организация является ДОО;
            2. Статус не "Закрыто", "Ликвидировано",
                "Присоединена к другой организации";
            3. Не проставлен признак "Не показывать на портале".

        :param instance: Организация
        :type instance: Unit

        :return: Признак успешности валидации
        :rtype: bool
        """

        return instance.kind_id == self.unit_kind and (
                instance.status not in UnitStatus.ALL_CLOSED_STATUS
                or not instance.is_not_show_on_poral)

    def post_save(self, instance, created, **kwargs):

        if instance.kind_id != self.unit_kind:
            return

        # Если организация уже была создана и нужно удалить,
        # то отправляет запрос на удаление.
        if instance.esnsi_created and instance.esnsi_remove:
            self.pre_delete(
                instance=instance,
                context=self._get_context(instance),
            )
            return

        # Если организация была создана и удалять не нужно,
        # то запросов не будет.
        if not instance.esnsi_created and instance.esnsi_remove:
            return

        if (
                (created or self.has_changes(instance))
                and self.validate(instance)
        ):
            ESNSIUnitTaskFactory(
                get_classifier_instance(UnitClassifier),
                UpdateClassifierRequest.UPDATE_CLASSIFIERS,
                instance
            ).set_task()

    def pre_delete(self, instance, context, **kwargs):

        instance.octmo = instance.get_mo_octmo() or instance.octmo
        if self.validate(instance) and instance.octmo:
            ESNSIUnitTaskFactory(
                get_classifier_instance(UnitClassifier),
                UpdateClassifierRequest.DELETE_CLASSIFIERS,
                instance
            ).set_task()


class MaxDooObserver(ChangesObserver):
    """Класс для отправки запроса при изменении и удалении организации (МО).

    При наличии изменений определённых полей
    (Наименование, ОКТМО, Максимальное количество желаемых ДОО в заявке)
    организации (МО) отправляется запрос CnsiRequest
    с вложением ClassifierDataUpdateRequest.

    При удаление организации (МО) отправляется запрос CnsiRequest
    с вложением ClassifierDataDeleteRequest.
    """

    model = Unit

    tracked_fields = ['name', 'octmo', 'max_desired_dou']

    unit_kind = UnitKind.MO

    def validate(self, instance):
        """Выполняет валидацию объекта.

        Проверяет, что организация является МО.

        :param instance: Организация
        :type instance: Unit

        :return: Признак успешности валидации
        :rtype: bool
        """

        return instance.kind_id == self.unit_kind

    def post_save(self, instance, created, **kwargs):

        if (
                (created or self.has_changes(instance))
                and self.validate(instance)
        ):

            ESNSIUnitTaskFactory(
                get_classifier_instance(MaxDooClassifier),
                UpdateClassifierRequest.UPDATE_CLASSIFIERS,
                instance
            ).set_task()

    def post_delete(self, instance, context, **kwargs):

        if self.validate(instance):

            ESNSIUnitTaskFactory(
                get_classifier_instance(MaxDooClassifier),
                UpdateClassifierRequest.DELETE_CLASSIFIERS,
                instance
            ).set_task()


class EduControlUnitObserver(ChangesObserver):
    """Класс для отправки запроса при изменении и удалении организации (МО).

    При наличии изменений определённых полей
    (Наименование, ОКТМО, Адрес, Телефон, Сайт, E-mail)
    организации (МО) отправляется запрос CnsiRequest
    с вложением ClassifierDataUpdateRequest.

    При удаление организации (МО) отправляется запрос CnsiRequest
    с вложением ClassifierDataDeleteRequest.
    """
    model = Unit
    tracked_fields = [
        'name', 
        'octmo', 
        'address_full',
        'telephone',
        'site',
        'email',
    ]
    unit_kind = UnitKind.MO

    def validate(self, instance):
        return instance.kind_id == self.unit_kind

    def post_save(self, instance, created, **kwargs):
        if (
            (created or self.has_changes(instance))
            and self.validate(instance)
        ):
            ESNSIUnitTaskFactory(
                get_classifier_instance(EduControlUnitClassifier),
                UpdateClassifierRequest.UPDATE_CLASSIFIERS,
                instance
            ).set_task()
    
    def post_delete(self, instance, context, **kwargs):
        if self.validate(instance):
            ESNSIUnitTaskFactory(
                get_classifier_instance(EduControlUnitClassifier),
                UpdateClassifierRequest.DELETE_CLASSIFIERS,
                instance
            ).set_task()


declaration_status_changes_observer = DeclarationStatusChangesObserver()
direct_status_changes_observer = DirectStatusChangesObserver()
change_declaration_observer = ChangeDeclarationObserver()
unit_observer = UnitObserver()
max_doo_observer = MaxDooObserver()
declaration_fields_changes_observer = DeclarationFieldsChangesObserver()
declaration_unit_changes_observer = DeclarationUnitChangesObserver()
children_changes_observer = ChildrenChangesObserver()
declaration_status_log_observer = DeclarationStatusLogObserver()

edu_control_unit_observer = None
if apps.is_installed('concentrator.smev3_v4'):
    # Не через m3-plugins т.к. находится на верхнем ур-не
    edu_control_unit_observer = EduControlUnitObserver()
