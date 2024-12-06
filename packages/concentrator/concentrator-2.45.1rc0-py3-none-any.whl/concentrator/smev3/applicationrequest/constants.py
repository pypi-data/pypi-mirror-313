from collections import namedtuple

Response = namedtuple('Response', 'order_id, status_code, comment')

MAX_AGE = 8


class ApplicationRequestMessage:
    """Сообщения для результата обработки заявки."""

    SUCCESS = 'Заявление принято к рассмотрению'
    CHANGES_SUCCESS = 'Изменения приняты'
    NO_CHANGES = 'Изменений не найдено'
    DATA_ERROR = 'Ошибка в данных запроса'
    MULTIPLE = 'Заявление на ребенка с указанными параметрами существует'
    OLD = 'Превышен допустимый возраст - 8 лет'
