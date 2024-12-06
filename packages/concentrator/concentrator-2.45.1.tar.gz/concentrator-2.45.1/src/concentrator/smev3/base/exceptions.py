class ContentFailure(Exception):
    """
    Исключение при невозможности сформировать ответ
    Должно быть обработано и передано в соответствующих тегах
    """
    def __init__(self, content_failure_code, content_failure_comment):
        self.content_failure_code = content_failure_code
        self.content_failure_comment = content_failure_comment
