from __future__ import annotations

from kinder.core.models import RegionCode
from kinder.settings import REGION_CODE


class BaseApplicationRequestMessageEnum:
    """Сообщения для результата обработки заявки."""

    SUCCESS: str = 'Заявление принято к рассмотрению'
    CHANGES_SUCCESS: str = 'Изменения приняты'
    NO_CHANGES: str = 'Изменений не найдено'
    DATA_ERROR: str = 'Ошибка в данных запроса'
    MULTIPLE: str = (
        'Заявление на ребенка с указанными параметрами существует{}')
    OLD: str = 'Превышен допустимый возраст - 8 лет'
    DESIRED_DATE_ERROR: str = (
        'Указанная желаемая дата зачисления раннее, чем {}')
    UNIT_NOT_EXISTS: str = 'Организация с id={} не существует'

    ORG_CODE_110: int = 110
    ORG_CODE_150: int = 150

    values: dict[str, int] = {
        SUCCESS: ORG_CODE_110,
        CHANGES_SUCCESS: ORG_CODE_110,
        NO_CHANGES: ORG_CODE_150,
        DATA_ERROR: ORG_CODE_150,
        MULTIPLE: ORG_CODE_150,
        OLD: ORG_CODE_150,
        DESIRED_DATE_ERROR: ORG_CODE_150,
        UNIT_NOT_EXISTS: ORG_CODE_150,
    }


class MurmanskApplicationRequestMessageEnum(BaseApplicationRequestMessageEnum):
    """Сообщения для результата обработки заявки для Мурманска."""

    # {child_fullname} {declaration_id} {declaration_date}
    MULTIPLE: str = (
        'Вам отказано в предоставлении услуги по текущему заявлению '
        'по причине того, что на ребёнка {} ранее уже зарегистрировано '
        'заявление с номером {} от {}. Вам необходимо отредактировать его '
        'в личном кабинете портала Госуслуг, если оно было подано '
        'Вами через портал Госуслуги. Если заявление было подано Вами лично, '
        'то обратитесь в орган местного самоуправления, реализующего '
        'полномочия в сфере образования, для внесения необходимых изменений.')

    values: dict[str, int] = {
        **BaseApplicationRequestMessageEnum.values,
        MULTIPLE: BaseApplicationRequestMessageEnum.ORG_CODE_150
    }


class VladimirApplicationRequestMessageEnum(BaseApplicationRequestMessageEnum):
    """Сообщения для результата обработки заявки для Владимира."""

    # {declaration_id} {declaration_date} {declaration_status}
    MULTIPLE: str = (
        'Вам отказано в предоставлении услуги по текущему заявлению '
        'по причине повторной подачи заявления. Есть заявление с номером '
        '{} от {} в статусе {}. Вы можете откорректировать свое заявление '
        'и отследить его статус в личном кабинете на портале Госуслуг.')

    values: dict[str, int] = {
        **BaseApplicationRequestMessageEnum.values,
        MULTIPLE: BaseApplicationRequestMessageEnum.ORG_CODE_150
    }

# Соответствие кодов регионов (настройка REGION_CODE) и классов сообщений
# для результата обработки заявки.
REGION_APPLICATION_REQUEST_MESSAGE_MAP: dict[
    int, type[BaseApplicationRequestMessageEnum]
] = {
    RegionCode.VLADIMIR: VladimirApplicationRequestMessageEnum,
    RegionCode.MURMANSK: MurmanskApplicationRequestMessageEnum,
}

ApplicationRequestMessageEnum = (
    REGION_APPLICATION_REQUEST_MESSAGE_MAP.get(
        REGION_CODE, BaseApplicationRequestMessageEnum))
