from collections import namedtuple
from kinder.core.declaration.models import DSS

Event = namedtuple('Event', ['code', 'comment'])

NEW_DIRECT_EVENT_CODE = '100'
NEW_DIRECT_EVENT_COMMENT_PATTERN = (
    '{unit_name} ({unit_full_address}) рассматривает '
    'вопрос о предоставлении вашему ребёнку места в группе {group_name}.')
NEW_DIRECT_EVENT_FULL_COMMENT_PATTERN = (
    f'{NEW_DIRECT_EVENT_COMMENT_PATTERN} '
    'Просим вас в течении {days_for_reject_direct} календарных дней '
    'с момента получения уведомления отправить своё решение '
    'о согласии или несогласии с направлением в предложенное '
    'образовательное учреждение.')

ACCEPT_DIRECT_EVENT_CODE = '101'
ACCEPT_DIRECT_EVENT = Event(
    ACCEPT_DIRECT_EVENT_CODE, 'Получено согласие на зачисление')
REJECT_DIRECT_EVENT_CODE = '102'
REJECT_DIRECT_EVENT = Event(
    REJECT_DIRECT_EVENT_CODE, 'Получен отказ на зачисление')
# коды для передачи информационных событий
INFO_VENT_LIST = (
    NEW_DIRECT_EVENT_CODE,
    ACCEPT_DIRECT_EVENT_CODE,
    REJECT_DIRECT_EVENT_CODE)


DEFAULT_STATUS = 7
DEFAULT_COMMENT = ''
# Маппинг переходов для отправки события в концентратор
# согласно 3.1.5 https://conf.bars.group/pages/viewpage.action?pageId=52791572
MAP_STATUS = {
    (
        #обходим 'in <string>' requires string as left operand, not NoneType
        ('None',),
        (DSS.RECEIVED,)
     ): (6, ''),

    (
        (DSS.ACCEPTED_FOR_CONSIDERING,),
        (DSS.DUL_CONFIRMATING,)
    ): (7, ''),

    (
        (DSS.DUL_CONFIRMATING,),
        (DSS.MED_CONFIRMATING, DSS.PRIV_CONFIRMATING,
         DSS.TUTOR_CONFIRMATING, DSS.ZAGS_CHECKING, DSS.FMS_CHECKING)
    ): (7, ''),

    (
        (DSS.MED_CONFIRMATING, DSS.PRIV_CONFIRMATING,
         DSS.TUTOR_CONFIRMATING, DSS.ZAGS_CHECKING, DSS.FMS_CHECKING,
         DSS.REGISTERED),
        (DSS.DUL_CONFIRMATING,),
    ): (7, 'Промежуточные результаты от ведомства.'),

    (
        (DSS.DUL_CONFIRMATING, DSS.MED_CONFIRMATING, DSS.PRIV_CONFIRMATING,
         DSS.TUTOR_CONFIRMATING, DSS.ZAGS_CHECKING, DSS.FMS_CHECKING,
         DSS.REFUSED,),
        (DSS.REGISTERED, DSS.WANT_CHANGE_DOU),
    ): (1, ''),

    (
        (DSS.REGISTERED,),
        (DSS.DIRECTED,),
    ): (7, 'По Вашему заявлению выдано направление в ДОО'),

    (
        (DSS.DIRECTED,),
        (DSS.ACCEPTED,),
    ): (3, ''),

    (
        tuple(DSS.values.keys()),
        (DSS.REFUSED,),
    ): (4, ''),

    (
        (DSS.ARCHIVE, DSS.REGISTERED, DSS.ACCEPTED, DSS.DIDNT_COME),
        (DSS.WANT_CHANGE_DOU,),
    ): (1, ''),

    (
        (DSS.WANT_CHANGE_DOU,),
        (DSS.ACCEPTED,),
    ): (3, ''),

    (
        (DSS.WANT_CHANGE_DOU,),
        (DSS.DUL_CONFIRMATING,),
    ): (7, 'По заявлению требуется дополнительная информация. '
           'Просим Вас обратиться лично в районный отдел образования'),

    (
        (DSS.WANT_CHANGE_DOU,),
        (DSS.REGISTERED,),
    ): (1, ''),

    (
        (DSS.WANT_CHANGE_DOU,),
        (DSS.DIRECTED,),
    ): (7, 'По Вашему заявлению выдано направление в ДОО.'
           ' Просим Вас обратиться лично в районный отдел образования'),
}
