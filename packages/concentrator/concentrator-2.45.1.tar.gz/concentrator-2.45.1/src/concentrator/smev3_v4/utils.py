def check_v4_message(message: str) -> bool:
    """Проверка, что сообщение относится к СМЭВ3 версии 4.0.1

    :param message: Запрос
    :return: Запрос относится к версии СМЭВ3 4.0.1
    """

    return 'http://epgu.gosuslugi.ru/concentrator/kindergarten/4.0.1' in message
