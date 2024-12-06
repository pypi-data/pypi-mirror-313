from __future__ import annotations

from concentrator.smev3_v321.enums import StatusCode


class ApplicationRejectionMessageEnum:
    """Ответы на запрос ApplicationRejectionRequest."""

    DECL_NOT_FOUND: str = 'Заявление по указанным параметрам не найдено'
    DIRECT_NOT_FOUND: str = (
        'Отказ от предложенной организации не может быть сохранен, так как '
        'направление не найдено.')
    MULTIPLY_DIRECT_FOUND: str = (
        'Отказ от предложенной организации не может быть сохранен, '
        'так как найдено несколько направлений.')
    REJECT_ACCEPTED: str = 'Отказ принят'

    values: dict[str, int] = {
        DECL_NOT_FOUND: StatusCode.CODE_150.value,
        DIRECT_NOT_FOUND: StatusCode.CODE_150.value,
        MULTIPLY_DIRECT_FOUND: StatusCode.CODE_150.value,
        REJECT_ACCEPTED: StatusCode.CODE_140.value,
    }
