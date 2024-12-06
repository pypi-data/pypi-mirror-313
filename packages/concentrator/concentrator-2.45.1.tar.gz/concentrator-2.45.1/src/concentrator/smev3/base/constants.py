from kinder.core.children.models import DelegateTypeEnumerate
from kinder.core.children.models import GenderEnumerate

from concentrator.smev3.service_types import kinder_conc


CODE_OK = 1
CODE_ERROR = 4
CODE_ERROR_COMMENT = 'Обработка заявления завершена'
# В задаче EDUKNDG-7390 указано, что для услуги GetApplication
# это зафиксированное значение
GETAPP_SERVICE_TYPE = '-10002202018'

SUCCESS_MESSAGE = 'Успешно'

DELEGATE_TYPE_CONC = {
    DelegateTypeEnumerate.MOTHER: (1, 'Мать'),
    DelegateTypeEnumerate.FATHER: (2, 'Отец'),
    DelegateTypeEnumerate.LEX: (3, 'Опекун'),
}

CHILD_GENDER_ENUM = {
    GenderEnumerate.FEMALE: kinder_conc.GenderType.FEMALE,
    GenderEnumerate.MALE: kinder_conc.GenderType.MALE
}

DELEGATE_GENDER_ENUM = {
    DelegateTypeEnumerate.MOTHER: kinder_conc.GenderType.FEMALE,
    DelegateTypeEnumerate.FATHER: kinder_conc.GenderType.MALE,
    DelegateTypeEnumerate.LEX: kinder_conc.GenderType.MALE,
}
