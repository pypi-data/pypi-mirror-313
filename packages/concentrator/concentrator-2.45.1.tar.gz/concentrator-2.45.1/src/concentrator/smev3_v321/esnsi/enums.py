from m3.db import BaseEnumerate


class DataTypesEnum(BaseEnumerate):
    """Типы атрибутов классификатора в xml."""

    STRING = 'string'
    TEXT = 'text'
    INTEGER = 'integer'
    BOOL = 'bool'
    DATE = 'date'
    DECIMAL = 'decimal'
    REFERENCE = 'reference'
    CODE = 'code'
    STRING_KEY = 'string-key'
    DATE_KEY = 'date-key'
    INTEGER_KEY = 'integer-key'
    DECIMAL_KEY = 'decimal-key'
