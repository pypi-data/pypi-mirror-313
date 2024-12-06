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

        win.applicant_comment = ext.ExtTextArea(
            anchor='100%',
            label='Комментарий заявителя',
            name='applicant_comment',
            allow_blank=True,
            read_only=True,
            height=40,
            style={'margin-top': '4px'},
        )

        win.applicant_answer.editable = False
        win.applicant_comment.editable = False

        applicant_answer = ApplicantAnswer.objects.filter(
            direct_id=context.id).first()

        if applicant_answer:
            win.applicant_answer.value = (
                ApplicantAnswersEnum.values[applicant_answer.answer])
            win.applicant_comment.value = applicant_answer.comment or ''

        free_row_num = 2
        # Если направление создано вручную, то поля перестают быть скрытыми,
        # поэтому поля ответа и комментария надо расположить ниже
        if (not win.hand_create_reason.hidden and
                not win.document_details.hidden):
            free_row_num += 2

        win.direct_info_top_panel.set_item(
            free_row_num, 1, win.applicant_answer)
        win.direct_info_top_panel.set_item(
            free_row_num + 1, 1, win.applicant_comment)
        win.direct_info_top_panel.set_row_height(free_row_num + 1, 45)


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

        win.need_confirmation_only = ext.ExtCheckBox(
            box_label='На подтверждение')
        if not hasattr(win, 'menu'):
            win.menu = ext.ExtContextMenu()
            win.options_toolbar = ext.ExtToolbarMenu(
                text='Отобразить только направления', menu=win.menu)
            win.grid.top_bar.items.insert(6, win.options_toolbar)
        win.menu.items.append(win.need_confirmation_only)

        extend_template_globals(win, 'ui-js/smev3-v321-direct-list-window.js')

        win.grid.get_row_class = lambda: 'highlightRow'
