from django.db.models import BooleanField
from django.db.models import F
from django.db.models import Case
from django.db.models import Value
from django.db.models import When
from lxml import etree
from lxml.etree import XMLSyntaxError
from m3_ext.ui import all_components as ext
from m3_ext.ui.misc import ExtDataStore

from kinder.core.direct.models import DRS
from kinder.webservice.smev3.utils.request_builder import BaseRequestBuilder

from .base.utils import get_order_id
from .event_service.helpers import get_text_message_event_request
from .models import ApplicantAnswer
from .models import ApplicantAnswersEnum
from .service_types.kinder_conc_event import EventServiceResponseType

APPLICANT_ANSWER_PARAM = 'applicant_answer'


def add_applicant_answer_column(columns, ext_result):
    """Добавляет столбец "Ответ заявителя" в реестр направлений."""

    _columns = columns.copy()
    index = [
        _columns.index(x) for x in _columns if x[0] == 'group.unit.name'
    ][0]

    _columns.insert(
        index + 1, (APPLICANT_ANSWER_PARAM, 'Ответ заявителя', 50)
    )

    return _columns


def add_applicant_answer_column_filter(win, name, ext_result):
    """
    Добавляет колоночный фильтр для столбца "Ответ заявителя"
    в реестре направлений.

    """

    applicant_answer_filter = ext.ExtDictSelectField(
        region='north',
        anchor='100%',
        ask_before_deleting=False,
        allow_blank=True,
        hide_edit_trigger=True,
        hide_clear_trigger=False,
        hide_dict_select_trigger=True,
        hide_trigger=False,
    )

    filter_store = ApplicantAnswersEnum.get_choices()
    filter_store.extend(list({2: 'Пусто'}.items()))
    applicant_answer_filter.set_store(
        ExtDataStore(filter_store)
    )

    win.add_grid_column_filter(
        APPLICANT_ANSWER_PARAM, applicant_answer_filter.render())


def add_applicant_answer_data(obj, ext_result):
    """
    Добавляет значение для атрибута столбца "Ответ заявителя" и атрибут для
    окрашивания строк в синий цвет, если "Ответ заявителя" = True и направление
    в статусе "Направлен в ДОО".

    """

    if obj.applicant_answer is None:
        obj.applicant_answer = ''
    else:
        # Атрибут для окрашивания строки в синий цвет
        obj.applicant_answer_highlight = obj.status.code == DRS.REGISTER
        # Человекочитаемое значение поля "Ответ заявителя"
        obj.applicant_answer = ApplicantAnswersEnum.values.get(
            obj.applicant_answer, '')

    return obj


def applicant_answer_update_filter_list(fields_list, ext_result):
    """Обновляет список стоблцов с кастомными колоночными фильтрами."""

    return fields_list.append(APPLICANT_ANSWER_PARAM)


def apply_applicant_answer_filter(query, context, ext_result):
    """
    Фильтрация направлений через колоночный фильтр и сортировка по стоблцу
    "Ответ заявителя".

    """

    query = query.annotate(
        applicant_answer=Case(
            When(applicantanswer__isnull=True, then=Value(None)),
            When(applicantanswer__answer=True, then=Value(True)),
            When(applicantanswer__answer=False, then=Value(False)),
            output_field=BooleanField()
        )
    )

    # Фильтрация запроса
    if hasattr(context, APPLICANT_ANSWER_PARAM):
        param = getattr(context, APPLICANT_ANSWER_PARAM, None)

        if param == 'true':
            param = True
        elif param == 'false':
            param = False

        if param not in ApplicantAnswersEnum.values:
            param = None

        query = query.filter(applicant_answer=param)

    return query


def apply_applicant_answer_sort(query, request, ext_result):
    """
    Сортировка по полю "Ответ заявителя"
    """
    sorting_key = request.POST.get('sort')
    if sorting_key == 'applicant_answer':
        reverse = request.POST.get('dir') == 'DESC'
        if reverse:
            query = query.order_by(
                F('applicant_answer').asc(nulls_first=True)
            )
        else:
            query = query.order_by(
                F('applicant_answer').desc(nulls_last=True)
            )

    return query


def handle_text_message_response(request, ext_result):
    """
    Возвращает code и message из ответа на запрос

    :param request: Объект TextMessageEventRequest
    :type request: TextMessageEventRequest
    :param ext_result: результат выполнения предыдущего обработчика точки
        расширения (в случае, если таковых несколько)
    :type ext_result: Any
    :return: Код и сообщение
    :rtype: tuple
    """

    node = etree.fromstring(request.response)
    response = EventServiceResponseType().build(node)

    return response.code, response.message


def get_text_message_event_builder(ext_result):
    """Возвращает класс билдера для TextMessageEventRequest

    :param ext_result: результат выполнения предыдущего обработчика точки
        расширения (в случае, если таковых несколько)
    :type ext_result: Any
    :return: Класс билдера
    :rtype: TextMessageEventRequestBuilder
    """

    class TextMessageEventRequestBuilder(BaseRequestBuilder):
        """Класс билдера для запроса отправки сообщений"""

        def build(self):
            """
            Метод построения запроса

            :return: Текст запроса
            :rtype: str
            """

            order_id = get_order_id(self.request.message_exchange.declaration)
            return get_text_message_event_request(order_id, self.request)

    return TextMessageEventRequestBuilder


def validate_text_message_response(response, ext_result):
    """
    Валидация eventServiceResponse

    :param response: Текст ответа на запрос
    :type response: str
    :param ext_result: результат выполнения предыдущего обработчика точки
        расширения (в случае, если таковых несколько)
    :type ext_result: Any
    :return: Есть ли ошибка в сообщении
    :rtype: bool
    """

    try:
        node = etree.fromstring(response)
        response = EventServiceResponseType().build(node)
    except XMLSyntaxError:
        return False
    else:
        return response.code or response.message or False
