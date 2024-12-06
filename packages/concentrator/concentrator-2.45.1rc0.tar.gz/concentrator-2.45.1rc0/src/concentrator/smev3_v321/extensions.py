from django.db import transaction
from django.db.models import BooleanField
from django.db.models import F
from django.db.models import Case
from django.db.models import Value
from django.db.models import When
from m3_ext.ui import all_components as ext
from m3_ext.ui.misc import ExtDataStore

from kinder.core.direct.models import DRS
from kinder.plugins.helpers import extend_template_globals

from concentrator.smev3_v321.application_request.snapshot import (
    get_snapshot_creator_for_model)
from concentrator.smev3_v321.base.tasks import PushChangeOrderInfoRequestTask

from .constants import APPLICANT_ANSWER_PARAM
from .constants import CHANGE_DECLARATION_CODE
from .constants import CHANGE_DECLARATION_COMMENT
from .models import ApplicantAnswersEnum
from .models import DeclarationPortalID
from .models import DeclarationOriginMessageID
from .utils import changes_to_str


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

    filter_store = list(ApplicantAnswersEnum.values_for_filter.items())
    applicant_answer_filter.set_store(ExtDataStore(filter_store))

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
            When(smev3_v321_applicant_answer__isnull=True, then=Value(None)),
            When(smev3_v321_applicant_answer__answer=True, then=Value(True)),
            When(smev3_v321_applicant_answer__answer=False, then=Value(False)),
            output_field=BooleanField()
        )
    )

    # Фильтрация запроса
    if hasattr(context, APPLICANT_ANSWER_PARAM):
        param = getattr(context, APPLICANT_ANSWER_PARAM)
        param = True if param == 'true' else False if param == 'false' else None
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


def apply_need_confirmation_only_filter(query, context, ext_result):
    """
    Фильтрация направлений в зависимости от значения в чекбоксе
    "На подтверждение"
    """
    if int(getattr(context, 'need_confirmation_only', 0)):
        query = query.filter(
            status__code=DRS.REGISTER,
            smev3_v321_applicant_answer__isnull=False)

    return query


def additional_declarations_search_fields(search_fields, ext_result):
    """
    Добавляет новые поля для поиска заявлений
    """
    additional_fields = (
        'declarationportalid__portal_id',
    )

    return search_fields + additional_fields


def exists_declarationportalid(declaration, ext_result):
    """
    Проверка существования записи о заявке в таблице DeclarationPortalID.

    :param declaration: Проверяемая заявка.
    :type declaration: Declaration
    """

    return DeclarationPortalID.objects.filter(declaration=declaration).exists()


def get_snapshot(model, obj_id, ext_result):
    """
    Получение снимка объекта модели
    """
    snapshot_creator = get_snapshot_creator_for_model(model)
    return snapshot_creator(obj_id).get_snapshot()


def get_update_changes(model, obj_id, snapshot, ext_result):
    """
    Получение изменений при обновлении объекта модели
    """
    snapshot_creator = get_snapshot_creator_for_model(model) 
    return snapshot_creator(obj_id).updated(snapshot)


def get_create_changes(model, obj_id, ext_result):
    """
    Получение изменений при создании объекта модели
    """
    snapshot_creator = get_snapshot_creator_for_model(model) 
    return snapshot_creator(obj_id).created()


def get_delete_changes(model, snapshot, ext_result):
    """
    Получение изменений при удалении объекта модели
    """
    snapshot_creator = get_snapshot_creator_for_model(model)
    return snapshot_creator(None).deleted(snapshot)


def send_changes_info(declaration_id, changes, ext_result):
    """
    Отправить запрос об изменениях в заявке

    Отправляет по завершению текущей транзакции, 
    поэтому и вызывать в рамках транзакции где происходят изменения
    """
    if not changes or not declaration_id:
        return
    
    declaration_message_id = DeclarationOriginMessageID.objects.filter(
        declaration_id=declaration_id).first()
    
    if not declaration_message_id:
        return

    transaction.on_commit(lambda: PushChangeOrderInfoRequestTask().apply_async(
        (declaration_id,
         CHANGE_DECLARATION_CODE,
         CHANGE_DECLARATION_COMMENT.format(
             changes=changes_to_str(changes)),
         declaration_message_id.message_id,
         declaration_message_id.replay_to)
    ))


def change_fields_allow_blank(win, ext_result):
    """
    Меняем обязательность полей в филдсете "Документ, удостоверяющий
    положение законного представителя по отношению к ребенку" из контингента.
    """

    extend_template_globals(win, 'ui-js/doc-proving-status-fieldset.js')
