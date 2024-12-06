from __future__ import annotations

from collections import Callable
from datetime import date
from datetime import datetime
from datetime import timedelta
from typing import TYPE_CHECKING
from typing import Any
import re

from django.conf import settings

from kinder.core.declaration.models import DSS
from kinder.core.direct.models import DRS
from kinder.core.direct.models import DirectStatusLog
from kinder.core.group.models import Pupil
from kinder.core.helpers import recursive_getattr

from concentrator.smev3_v321.constants import (
    ADDITIONAL_PRIV_CONFIRMATING_COMMENT)
from concentrator.smev3_v321.enums import StatusCode
from concentrator.smev3_v321.models import ApplicantAnswer


if TYPE_CHECKING:
    from kinder.core.declaration.models import Declaration
    from kinder.core.direct.models import Direct

    from concentrator.constants import DeclarationChanges


# Относятся к смене статуса направления (при этом должен менятся статус заявки)
# Направлен в дошкольную образовательную организацию
DIRECTED_TO_DOO = 3

# Формирование заявления о приеме
DECLARATION_FORMATION = 6
PROVIDE_DOCUMENTS_COMMENT = (
    'Для подтверждения данных вам необходимо представить в '
    '{declaration__mo__address_full} в срок{auto_change_days}'
    'следующие документы: {doc_comment_format}'
)

CREATE_ORDER_STATUS_MAP = {
    (DSS.RECEIVED, ): (
        StatusCode.CODE_110.value,
        'Заявление передано в региональную систему доступности '
        'дошкольного образования.  Заявление зарегистрировано '
        '{declaration__date} с номером {declaration__id}. '
        'Ожидайте рассмотрения в течение 7 дней. '),
    (DSS.PRIV_CONFIRMATING, ): (
        StatusCode.CODE_130.value,
        PROVIDE_DOCUMENTS_COMMENT + ADDITIONAL_PRIV_CONFIRMATING_COMMENT
    ),
    (DSS.ACCEPTED_FOR_CONSIDERING, ): (
        StatusCode.CODE_120.value, 'Начато рассмотрение заявления.'),
    (
        DSS.DUL_CONFIRMATING, DSS.MED_CONFIRMATING,
        DSS.TUTOR_CONFIRMATING, DSS.ZAGS_CHECKING
    ): (
        StatusCode.CODE_130.value,
        PROVIDE_DOCUMENTS_COMMENT
    ),
    (DSS.REFUSED, ): (
        StatusCode.CODE_150.value,
        'Вам отказано в предоставлении услуги по текущему заявлению по '
        'причине {comment}. Вам необходимо обратиться по адресу: '
        '{declaration__mo__address_full}.'),
    (DIRECTED_TO_DOO, ): (
        StatusCode.CODE_190.value,
        'Вам предоставлено место в {direct__group__unit__name} в '
        'группу {direct__group__name} ({direct__group__sub_age_cat__name}) в '
        'соответствии с {get_direct_document_details}. '
        'Вам необходимо явиться по адресу {direct__group__unit__address_full}'
        ' {get_direct_reject_date}.'),
    (DECLARATION_FORMATION, ): (
        StatusCode.CODE_230.value,
        'Согласие с предоставленным местом направлено на рассмотрение в '
        '{declaration__mo__name}.'),
    (DSS.ACCEPTED, ): (
        StatusCode.CODE_250.value,
        'Ваш ребенок зачислен в {last_pupil__grup__unit__name}, '
        'расположенную по адресу {last_pupil__grup__unit__address_full}. '
        'На основании договора от {last_pupil__date_in_order_to_doo}.'),
}

APPLICATION_REVIEWED = (
    StatusCode.CODE_140.value,
    'Ваше заявление рассмотрено. Индивидуальный номер заявления '
    '{declaration__id}. Ожидайте направления в выбранную образовательную '
    'организацию после {declaration__desired_date}.')

AWAITING_DIRECTION = (
    StatusCode.CODE_160.value,
    'В настоящее время в образовательных организациях, указанных в '
    'заявлении, нет свободных мест, соответствующих запрашиваемым в '
    'заявлении условиях. ')

DEFAULT_STATUS = (
    StatusCode.CODE_130.value, 'Необходимо подтвердить данные заявления.')

# После отправки в ЭДС запроса ApplicationRequest с изменениями заявления
DECLARATION_CHANGED = 1
# Вкладка "Изменения с ЕПГУ" - выбрать запись - Отказать
DECLARATION_CHANGED_REFUSED = 2
# Потребность в получении места не подтверждена
NEED_NOT_CONFIRMED = 4
# Заявитель отказался от предоставленного места
DELEGATE_REFUSED = 5
# Ожидание заключения договора
WAITING_FOR_CONTRACT = 7

UPDATE_ORDER_STATUS_MAP = {
    (DECLARATION_CHANGED,): (
        StatusCode.CODE_170.value,
        'В заявления для направления были внесены следующие изменения: '
        '{get_declaration_changes}.'
    ),
    (DECLARATION_CHANGED_REFUSED,): (
        StatusCode.CODE_180.value,
        'Вам отказано в изменении заявления по причине: {get_refused_reason}.'
    ),
    (NEED_NOT_CONFIRMED,): (
        StatusCode.CODE_210.value,
        'Действие Вашего заявления приостановлено по причине '
        '{didnt_come_comment_format}.'
    ),
    (DELEGATE_REFUSED,): (
        StatusCode.CODE_220.value,
        'Действия по заявлению приостановлены по причине Вашего отказа от '
        'предоставленного места. Вам необходимо изменить заявление '
        'либо отозвать его.'
    ),
    (WAITING_FOR_CONTRACT,): (
        StatusCode.CODE_240.value,
        'Ваше заявление рассмотрено. Вам необходимо заключить договор до '
        '{get_date_for_contract}.'
    )
}


class CreateOrderStatusMapper:
    """
    Маппинг статусов для CreateOrderRequest, в основе используется маппинг
    CREATE_ORDER_STATUS_MAP. Возвращает код и комментарий для ЕПГУ.

    Подготавливает комментарий, заменяя часть сообщения на значения
    атрибутов класса или на результаты вызова функций класса.

    Описание https://conf.bars.group/pages/viewpage.action?pageId=123901022
    """

    def __init__(self, declaration: Declaration, direct: Direct):
        self.declaration = declaration
        self.direct = direct
        self.status_map = CREATE_ORDER_STATUS_MAP

    @property
    def last_pupil(self) -> Pupil | None:
        """Любое последнее зачисление ребёнка (фактическое/плановое/None)

        Не используется информация о направлении, поскольку чаще всего оно
        не указано явно выше в коде и берётся первое попавшееся направление
        ребёнка. Это может привести к неправильному комментарию о зачислении.

        Данный вариант также не идеален, но хотя бы лучше выдать информацию
        о существующем зачислении, чем о зачислении, которого на самом деле нет.
        """
        pupil = Pupil.objects.for_child(
            self.declaration.children_id).order_by('-id').first()
        return pupil

    @staticmethod
    def doc_comment_format(status_data: dict[str, Any]) -> str:
        """Возвращает тип документа для комментария"""

        status_code = status_data['status__code']

        if status_code == DSS.DUL_CONFIRMATING:
            return (
                'Свидетельство о рождении, Документ, подтверждающий прописку.'
            )
        elif status_code == DSS.MED_CONFIRMATING:
            return 'Заключение ПМПК.'
        elif status_code == DSS.TUTOR_CONFIRMATING:
            return 'Документы, подтверждающие опеку.'
        elif status_code == DSS.ZAGS_CHECKING:
            return 'Свидетельство о рождении.'
        elif status_code == DSS.PRIV_CONFIRMATING:
            return 'Документы, подтверждающие льготу.'
        else:
            return ''

    def check_is_application_reviewed(self, status_code: str) -> bool:
        """Проверка для статуса концентратора "Заявление рассмотрено"."""

        application_reviewed = False

        alloc_date_bgn = self.declaration.mo.alloc_date_bgn
        alloc_date_end = self.declaration.mo.alloc_date_end
        alloc_calc_date = self.declaration.mo.alloc_calc_date
        today = date.today()

        check_statuses = [DSS.REGISTERED, DSS.WANT_CHANGE_DOU]

        if alloc_date_bgn and alloc_date_end:
            if alloc_date_bgn <= today <= alloc_date_end:
                if (alloc_calc_date and
                        self.declaration.desired_date > alloc_calc_date and
                        status_code in check_statuses):
                    application_reviewed = True

            elif (self.declaration.desired_date > today and
                    status_code in check_statuses):
                application_reviewed = True

        return application_reviewed

    def check_is_awaiting_direction(self, status_code: str) -> bool:
        """Проверка для статуса концентратора "Ожидает направления"."""

        awaiting_direction = False

        alloc_date_bgn = self.declaration.mo.alloc_date_bgn
        alloc_date_end = self.declaration.mo.alloc_date_end
        alloc_calc_date = self.declaration.mo.alloc_calc_date
        today = date.today()

        check_statuses = [DSS.REGISTERED, DSS.WANT_CHANGE_DOU]

        if alloc_date_bgn and alloc_date_end:
            if alloc_date_bgn <= today <= alloc_date_end:
                if (alloc_calc_date and
                        self.declaration.desired_date <= alloc_calc_date and
                        status_code in check_statuses):
                    awaiting_direction = True

            elif (self.declaration.desired_date <= today and
                    status_code in check_statuses):
                awaiting_direction = True

        return awaiting_direction

    def prepare_comment(
            self, status_data: dict[str, Any], epgu_comment: str
    ) -> str:
        """Подготовка комментария, заменяет часть сообщения на значения
        атрибутов класса или на результат вызова функций класса.

        """

        param_regex = r'({(\S+)})'

        for attr in re.findall(param_regex, epgu_comment):
            comment_attr = recursive_getattr(self, attr[1]) or ' '

            if isinstance(comment_attr, Callable):
                epgu_comment = re.sub(
                    attr[0], comment_attr(status_data) or '', epgu_comment)
            else:
                if isinstance(comment_attr, date):
                    comment_attr = comment_attr.strftime(settings.DATE_FORMAT)
                elif isinstance(comment_attr, datetime):
                    comment_attr = comment_attr.strftime(
                        f'{settings.DATE_FORMAT} %H:%M:%S')

                epgu_comment = re.sub(attr[0], str(comment_attr), epgu_comment)

        return epgu_comment

    def get_direct_reject_date(
            self, status_data: dict[str, Any]
    ) -> str | None:
        """Возвращает срок для явки с учётом времени действия направления
        Направлен в ДОО.
        """
        direct_status_log = DirectStatusLog.objects.filter(
            direct=self.direct).latest('created_at')

        days_for_reject_direct = self.declaration.mo.days_for_reject_direct

        if days_for_reject_direct and direct_status_log:
            end_date = (
                direct_status_log.created_at +
                timedelta(days=days_for_reject_direct)
            )

            return f'до {end_date.strftime("%d.%m.%Y")}'

    def process_directed_status(
            self, status_data: dict[str, Any]
    ) -> tuple[int, str]:
        """Возвращает код и статус при смене статуса направления на
        Направлен в ДОО.
        """
        applicant_answer = ApplicantAnswer.objects.filter(
            direct=self.direct).values_list('answer', flat=True).first()

        if applicant_answer:
            epgu_status, epgu_comment = self.status_map[
                (DECLARATION_FORMATION,)]
        else:
            epgu_status, epgu_comment = self.status_map[
                (DIRECTED_TO_DOO, )]

        return epgu_status, self.prepare_comment(
            status_data, epgu_comment)

    def __getitem__(self, status_data) -> tuple[int, str]:
        status_code = status_data['status__code']

        # Комментарий к смене статуса
        self.comment = status_data.get('comment', '')

        auto_change_days = status_data.get('auto_change_days', None)
        self.auto_change_days = (
            f' {auto_change_days} ' if auto_change_days else '')

        for statuses_keys in self.status_map.keys():
            if status_code in statuses_keys:
                epgu_status, epgu_comment = self.status_map.get(statuses_keys)

                return epgu_status, self.prepare_comment(
                    status_data, epgu_comment)

        if self.check_is_application_reviewed(status_code):
            code, comment = APPLICATION_REVIEWED
            return code, self.prepare_comment(status_data, comment)
        elif self.check_is_awaiting_direction(status_code):
            return AWAITING_DIRECTION
        elif (
                status_code == DSS.DIRECTED and
                self.direct.status.code == DRS.REGISTER):
            return self.process_directed_status(status_data)
        else:
            return DEFAULT_STATUS

    def get_direct_document_details(self, *args) -> str:
        """
        При смене статуса направления на Направлен в ДОО отправляем в ответе
        разные данные направления в зависимости от того,
        было оно создано в ручную или нет
        """
        if self.direct.manual_create:
            return f'документом {self.direct.document_details}'
        return (
            f'номером направления {self.direct.id} от '
            f'{self.direct.date.strftime("%d.%m.%Y")}'
        )


class UpdateOrderStatusMapper(CreateOrderStatusMapper):
    """Маппинг статусов для UpdateOrderRequest"""

    def __init__(
            self, declaration: Declaration, direct: Direct,
            declaration_status_changed: bool = False,
            direct_status_log: dict[str, Any] | None = None,
            event: int | None = None,
            declaration_changes_rows: list[DeclarationChanges] | None = None,
            reject_changes_comment: str | None = None
    ):

        super().__init__(declaration, direct)

        self.declaration_status_changed = declaration_status_changed
        self.direct_status_log = direct_status_log
        self.event = event
        self.declaration_changes_rows = declaration_changes_rows
        self.reject_changes_comment = reject_changes_comment

        self.status_map.update(UPDATE_ORDER_STATUS_MAP)

    def prepare_comment(
            self, status_data: dict[str, Any], epgu_comment: str
    ) -> str:
        """При изменении полей заявления передавать только последний статус и
        фиксированный комментарий
        "Заявление было изменено во время личного приема."

        """

        if (not self.declaration_status_changed and not self.direct_status_log
                and not self.event):
            return 'Заявление было изменено во время личного приема.'
        else:
            return super().prepare_comment(status_data, epgu_comment)

    def get_declaration_changes(self, status_data):
        if self.declaration_changes_rows:
            from concentrator.smev3_v321.utils import changes_to_str

            return changes_to_str(self.declaration_changes_rows)

    def get_refused_reason(self, status_data):
        if self.reject_changes_comment:
            return self.reject_changes_comment

    def get_direct_reject_date(self, status_data):
        created_at = self.direct_status_log['created_at']

        days_for_reject = self.direct.group.unit.get_days_for_reject_direct()
        if days_for_reject and created_at:
            if isinstance(created_at, str):
                try:
                    created_at = (
                        datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S'))
                except ValueError:
                    return ''

            end_date = created_at + timedelta(days=days_for_reject)

            return f'до {end_date.strftime("%d.%m.%Y")}'

    def didnt_come_comment_format(self, status_data):
        """
        Для статуса "Оказано либо отказался" берем текст из поля '
        'Причина. Для статуса "Не явился" пишем: "окончания срока '
        'действия направления [если статус был Направлен в ДОО, '
        'указываем значение Дата смены статуса на '
        '"Направлен в ДОО" + значение из поля "Срок действия направления '
        'в Направлен в ДОО" в справочнике МО, вкладка Комплектование; если '
        'статус Заключение договора, указываем значение Дата смены статуса '
        'на "Заключение договора" + значение из поля '
        '"Срок заключения договора для направления" в справочнике МО, '
        'вкладка Комплектование].

        """

        status_code = status_data.get('new_status_code')
        created_at = status_data.get('created_at')
        reason = status_data.get('reason', '')
        old_status = status_data.get('old_status')

        if status_code == DRS.REFUSED:
            return reason
        elif status_code == DRS.REJECT:
            comment_str = 'окончания срока действия направления '

            if old_status == DRS.REGISTER:
                end_date = created_at + timedelta(
                    days=self.declaration.mo.days_for_reject_direct)

                return comment_str + end_date.strftime(settings.DATE_FORMAT)
            elif old_status == DRS.DOGOVOR:
                end_date = created_at + timedelta(
                    days=self.declaration.mo.days_for_direct_dogovor)

                return comment_str + end_date.strftime(settings.DATE_FORMAT)
            elif old_status == DRS.NEED_CHANGE:
                return 'того, что Вы не явились для оформления в желаемое ДОО'

    def get_date_for_contract(self, status_data):
        """
        Дата смены статуса на Заключение договора + "Срок заключения договора
        для направлений" (если заполнено) в МО,
        которое указано в заявлении.

        """

        days_for_direct_dogovor = self.declaration.mo.days_for_direct_dogovor

        if days_for_direct_dogovor is None:
            return ''

        created_at = status_data.get('created_at')
        end_date = created_at + timedelta(days=days_for_direct_dogovor)

        return end_date.strftime(settings.DATE_FORMAT)


# Наименования по умолчанию типов ВС и кодов методов сервисов семейства
# OrderRequest
DEFAULT_ORDER_REQUEST_MESSAGE_TYPE = 'OrderRequest'
DEFAULT_CREATE_ORDER_REQUEST_METHOD_NAME = 'CreateOrderRequest'
DEFAULT_UPDATE_ORDER_REQUEST_METHOD_NAME = 'UpdateOrderRequest'

# Код успешного ответа CreateOrderResponse
CREATE_ORDER_RESPONSE_SUCCESS_CODE = 0

# Ниже представлены обязательные поля для запроса OrderRequest.
# Для проверки обязательности полей лучше не использовать данные поля напрямую,
# а использовать класс OrderRequestRequiredFieldsChecker.

# Обязательные поля для представителя
DELEGATE_REQUIRED_FIELDS = {
    'firstname': 'Фамилия',
    'surname': 'Имя',
    'email': 'Адрес электронной почты',
    'dul_number': 'Номер',
    'dul_date': 'Дата выдачи документа',
    'dul_issued_by': 'Кем выдан',
    'dul_type_id': 'Тип документа',
}
# Обязательные поля телефона для представителя
DELEGATE_REQUIRED_PHONE_FIELDS = {
    'phone_for_sms': 'Телефон для СМС',
    'phones': 'Телефон',
}
# Обязательные поля для ребёнка
CHILDREN_REQUIRED_FIELDS = {
    'surname': 'Фамилия',
    'firstname': 'Имя',
    'date_of_birth': 'Дата рождения',
    'dul_type': 'Тип документа',
    'dul_number': 'Номер',
    'dul_date': 'Дата выдачи документа',
    'zags_act_place': 'Место государственной регистрации (отдел ЗАГС)',
    'address_full': 'Полный адрес',
}
# Обязательные поля для ребёнка с документами РФ
CHILDREN_RF_DOC_REQUIRED_FIELDS = {
    'dul_series': 'Серия',
    'zags_act_number': 'Номер актовой записи',
    'zags_act_date': 'Дата создания актовой записи',
}
