from m3_ext.ui import all_components as ext

from kinder.controllers import obs
from kinder.plugins.helpers import extend_template_globals

from .models import ApplicantAnswer
from .models import ApplicantAnswersEnum


@obs.subscribe
class DirectEditWindowListener:
    """
    Слушатель экшна окна редактирования направления.
    """

    listen = [
        'kinder.core.direct/DirectActionPack/DirectEditAction$'
    ]

    def after(self, request, context, response):
        win = response.data

        win.applicant_answer = ext.ExtStringField(
            anchor='100%',
            label='Ответ заявителя',
            name='applicant_answer',
            allow_blank=True,
            read_only=True,
            style={'margin-top': '4px'},
        )
        win.applicant_answer.editable = False

        applicant_answer = ApplicantAnswer.objects.filter(
            direct_id=context.id).values_list('answer', flat=True).first()

        if applicant_answer is not None:
            win.applicant_answer.value = (
                ApplicantAnswersEnum.values[applicant_answer])

        free_row_num = 2
        # Если направление создано вручную, то поля перестают быть скрытыми,
        # поэтому поля ответа и комментария надо расположить ниже
        if (not win.hand_create_reason.hidden and
                not win.document_details.hidden):
            free_row_num += 2

        win.direct_info_top_panel.set_item(
            free_row_num, 1, win.applicant_answer)


@obs.subscribe
class DirectListWindowListener:
    """
    Слушатель экшна окна редактирования направления.
    """

    listen = [
        'kinder.core.direct/DirectActionPack/DirectListWindowAction'
    ]

    def after(self, request, context, response):
        win = response.data

        extend_template_globals(win, 'ui-js/smev3-direct-list-window.js')

        win.grid.get_row_class = lambda: 'highlightRow'
