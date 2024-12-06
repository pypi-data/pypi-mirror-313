from __future__ import annotations

from kinder.core.declaration_status.enum import DSS
from kinder.core.direct.models import DRS
from kinder.core.models import RegionCode as RC

from .enums import StatusCode


APPLICANT_ANSWER_PARAM = 'applicant_answer'

SUCCESS_MESSAGE = 'Успешно'

PRIVILEGE_DOC_ISSUED = 'ведомством'

LOG_TIME_FORMAT = '%d.%m.%Y %H:%M'

PROVIDE_DOCUMENTS_COMMENT = (
    'Для подтверждения данных вам необходимо представить в '
    '{mo} {doc_date_before}следующие документы: {comment}.')

DECLARATION_CONCIDERING_STARTED = 'Начато рассмотрение заявления.'

REFUSED_COMMENT = (
    'Вам отказано в предоставлении услуги по текущему заявлению по '
    'причине {comment}. Вам необходимо обратиться по адресу: '
    '{mo_address}.')

ADDITIONAL_PRIV_CONFIRMATING_COMMENT = (
    ' До момента подтверждения льготы заявление будет находиться'
    ' в общей очереди.'
)

PROVIDE_DOCUMENTS_CODE_AND_COMMENT = (
    StatusCode.CODE_130.value, PROVIDE_DOCUMENTS_COMMENT)

PROVIDE_DOCUMENT_STATUSES = (
    DSS.DUL_CONFIRMATING, DSS.MED_CONFIRMATING,
    DSS.TUTOR_CONFIRMATING, DSS.ZAGS_CHECKING)

# Соответствие статусов и кодов, отправляемых при смене статуса заявления
DECLARATION_STATUS_MAP = {
    DSS.ACCEPTED_FOR_CONSIDERING: (
        StatusCode.CODE_120.value, DECLARATION_CONCIDERING_STARTED),
    DSS.REFUSED: (StatusCode.CODE_150.value, REFUSED_COMMENT),
    DSS.WANT_CHANGE_DOU: (
        StatusCode.CODE_220.value,
        'Действия по заявлению приостановлены по причине Вашего отказа '
        'от предоставленного места. Вам необходимо изменить заявление '
        'либо отозвать его.'),
    DSS.PRIV_CONFIRMATING: (
        StatusCode.CODE_130.value,
        PROVIDE_DOCUMENTS_COMMENT + ADDITIONAL_PRIV_CONFIRMATING_COMMENT
    )
}

# Соответствие кодов регионов (настройка REGION_CODE) и комментариев
# для случая отправки ChangeOrderInfo при смене статуса на Отказано в услуге
# (после cancelRequest)
REGION_REFUSED_COMMENT_MAP: dict[int, str] = {
    RC.VLADIMIR: 'Действия по заявлению приостановлены по причине Вашего '
        'отзыва заявления. Если данная услуга необходима, Вы можете подать '
        'новое заявление.',
    RC.VOLOGDA: 'Обработка Вашего заявления прекращена в связи с отменой '
        'заявления по Вашей инициативе. Для консультации по подаче заявления '
        'Вы можете обратиться в Управление образования муниципального '
        'района/округа.',
    RC.KARELIA: 'Вам отказано в предоставлении услуги по текущему заявлению '
        'по причине отзыва Вами заявления на ЕПГУ.',
    RC.ROSTOV: 'Вам отказано в предоставлении услуги по текущему заявлению '
        'по причине Вашей отмены данного заявления.',
}

# Комментарий для статуса Отказано в услуге в случае, если код региона не указан
# (настройка REGION_CODE)
DEFAULT_REFUSED_COMMENT: str = (
    'Работа по текущему заявлению остановлена по причине '
    'Вашей отмены данного заявления.'
)

for status in PROVIDE_DOCUMENT_STATUSES:
    DECLARATION_STATUS_MAP[status] = PROVIDE_DOCUMENTS_CODE_AND_COMMENT

DEFAULT_CODE_COMMENT = (
    StatusCode.CODE_130.value, 'Необходимо подтвердить данные заявления')

DIRECTED_WITHOUT_RESPONSE = 'DIRECTED_WITHOUT_RESPONSE'
DIRECT_REJECT_COMMENT = 'DIRECT_REJECT_COMMENT'

FROM_ARCHIVE_STATUS_COMMENT = (
    'Заявление с идентификационным номером {declaration_id} '
    'было отменено{reason}')

AGE_7_REASON = ' в связи с достижением возраста ребенка 7 лет.'

# Соответствие статусов и кодов, отправляемых при смене статуса направления
DIRECT_STATUS_MAP = {
    DRS.REGISTER: (
        StatusCode.CODE_190.value,
        'Вам предоставлено место в {doo} в группу {group} ({age_cat}) в '
        'соответствии с {document_details}. Вам необходимо явиться по '
        'адресу {unit_address}{date_before}.'),
    DRS.REJECT: (
        StatusCode.CODE_210.value,
        'Действие Вашего заявления приостановлено по причине {reason}.'),
    DRS.NEED_CHANGE: (
        StatusCode.CODE_220.value,
        'Действия по заявлению приостановлены по причине Вашего отказа '
        'от предоставленного места. Вам необходимо изменить заявление '
        'либо отозвать его.'),
    DIRECTED_WITHOUT_RESPONSE: (
        StatusCode.CODE_230.value,
        'Согласие с предоставленным местом направлено на рассмотрение '
        'в {mo}.'),
    DRS.DOGOVOR: (
        StatusCode.CODE_240.value,
        'Ваше заявление рассмотрено. Вам необходимо заключить договор'
        '{dogovor_days}.'),
    DRS.ACCEPT: (
        StatusCode.CODE_250.value,
        'Ваш ребенок зачислен в {doo}, расположенную по адресу '
        '{unit_address}. На основании договора от {date_in_order_to_doo}.'),
    DIRECT_REJECT_COMMENT: (
        StatusCode.CODE_210.value,
        'Действие Вашего заявления приостановлено по причине того, что '
        'Вы не явились для оформления в желаемое ДОО.'
    )
}

DECLARATION_CHANGES_REFUSED_CODE = StatusCode.CODE_180.value
DECLARATION_CHANGES_REFUSED_COMMENT = (
    'Вам отказано в изменении заявления по причине: '
    '{comment}.')
DECLARATION_CHANGES_REFUSED_REASON = 'Заявление не активно'

DECLARATION_REVIEWED_COMMENT = (
    'Ваше заявление рассмотрено. Индивидуальный номер заявления {order_id}. '
    'Ожидайте направления в выбранную образовательную организацию после '
    '{desired_date}.')

DECLARATION_AWAITING_COMMENT = (
    'В настоящее время в образовательных организациях, указанных в заявлении, '
    'нет свободных мест, соответствующих запрашиваемым в заявлении условиях. ')

CHANGE_DECLARATION_CODE = StatusCode.CODE_170.value
CHANGE_DECLARATION_COMMENT = (
    'В заявления для направления были внесены следующие изменения: {changes}.')
CHANGES_DATA_TEMPATE = (
    '{index}. Поле: {field}. Старое значение: {old_value}. Новое значение: '
    '{new_value}')

DECLARATION_RECEIVED_COMMENT = (
    'Заявление передано в региональную систему доступности дошкольного '
    'образования.  Заявление зарегистрировано. {date} с номером '
    '{declaration_client_id}. Ожидайте рассмотрения в течение 7 дней.')

# Статусы заявлений, при которых не требуется
# отправка сообщений об изменении статуса
NO_REQUEST_REQUIRED_DECLARATION_STATUSES = (
    DSS.DIRECTED,
    DSS.DIDNT_COME,
    DSS.REFUSED,
    DSS.ACCEPTED,
)

# Статусы направлений, при которых не требуется
# отправка сообщений об изменении статуса
NO_REQUEST_REQUIRED_DIRECT_STATUSES = (
    DRS.CONFIRM,
    DRS.NEW,
)

GAR_RESEND_MESSAGE = (
    'Сообщение будет сформированно/обработанно через {time} секунд.')

# Значение, используемое для кеширования признака отмены заявления
# при помощи cancelRequest
CACHE_REJECTED_WITH_CANCEL_REQUEST = 'decl_rejected_with_cancel-request_{}'
