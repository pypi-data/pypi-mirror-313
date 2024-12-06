from __future__ import annotations

from concentrator.smev3_v321.enums import StatusCode


class GetApplicationQueueMessage:
    """Сообщения для результата обработки заявления."""

    NOT_EXISTS: str = 'Заявление по указанным параметрам не найдено'
    NOT_QUEUED: str = 'Заявление не участвует в очереди в ДОО'

    values: dict[str, int] = {
        NOT_EXISTS: StatusCode.CODE_150.value,
        NOT_QUEUED: StatusCode.CODE_150.value,
    }
