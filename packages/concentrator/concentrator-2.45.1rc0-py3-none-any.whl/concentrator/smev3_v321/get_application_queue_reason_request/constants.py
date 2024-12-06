from __future__ import annotations

from concentrator.smev3_v321.enums import StatusCode


class GetApplicationQueueReasonRequest:
    """Сообщения для результата обработки запроса
    GetApplicationQueueReasonRequest.
    """

    NOT_EXISTS: str = 'Заявление по указанным параметрам не найдено'
    NOT_QUEUED: str = 'Заявление не участвует в очереди в ДОО'
    NO_CHANGES: str = (
        'В указанном периоде изменения по позиции в очереди отсутствуют')

    values: dict[str, int] = {
        NOT_EXISTS: StatusCode.CODE_150.value,
        NOT_QUEUED: StatusCode.CODE_150.value,
        NO_CHANGES: StatusCode.CODE_150.value,
    }
