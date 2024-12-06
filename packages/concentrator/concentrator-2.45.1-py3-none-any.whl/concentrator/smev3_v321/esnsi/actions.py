from django.utils.translation import ugettext as _
from m3.actions import PreJsonResult
from objectpack.actions import BaseAction
from objectpack.actions import BaseWindowAction
from objectpack.actions import ObjectPack
from objectpack.actions import ObjectListWindowAction
from objectpack.ui import ModelEditWindow

from kinder.controllers import obs

from concentrator.smev3_v321.esnsi.forms import AvailableClassifierWindow
from concentrator.smev3_v321.esnsi.helpers import ESNSITaskFacade
from concentrator.smev3_v321.models import ESNSIClassifier
from concentrator.smev3_v321.models import UpdateClassifierRequest


class ClassifierListWindowAction(ObjectListWindowAction):
    """
    Экшн окна списка

    Переопределён для переименования права
    """
    perm_code = 'view'
    verbose_name = 'Доступные для обновления справочники'
    need_check_permission = True


class ClassifierListPack(ObjectPack):
    """Доступные для обновления справочники."""

    title = "Отправка справочников в ЕСНСИ"
    model = ESNSIClassifier

    edit_window = ModelEditWindow.fabricate(
        model,
        model_register=obs,
        field_list=['code', 'uid'],
    )
    can_delete = False

    need_check_permission = True

    columns = [
        dict(
            header='Код',
            data_index='code',
            sortable=True,
            width=120,
        ),
        dict(
            header='Наименование',
            data_index='name',
            sortable=False,
            width=120,
        ),
    ]

    def __init__(self):
        super().__init__()
        self.replace_action("list_window_action", ClassifierListWindowAction())
        self.sub_permissions = self.sub_permissions.copy()
        self.sub_permissions[
            self.list_window_action.perm_code] = self.list_window_action.verbose_name

    def get_rows_query(self, request, context):
        query = super().get_rows_query(request, context)

        return query.order_by('id')

    def configure_grid(self, grid, *args, **kwargs):
        super().configure_grid(grid)

        grid.cls = 'task-details'

    def create_edit_window(self, create_new, request, context):
        win = super().create_edit_window(create_new, request, context)
        win.template_globals = 'ui-js/classifier-edit-window.js'
        win.handler_beforesubmit = 'beforeSubmit'
        win.field__code.invalid_text = win.field__uid.invalid_text = (
            'Одно из полей формы должно быть заполнено')
        return win

    def format_window_title(self, action):
        return f'Доступный для обновления справочник: {action}'

    def extend_menu(self, menu):
        return menu.SubMenu(
            'Администрирование',
            menu.SubMenu(
                'Отправка справочников в ЕСНСИ', menu.Item(
                    self.list_window_action.verbose_name, self.list_window_action
                ),
                icon='menu-dicts-16'
            )
        )


class UpdateClassifierAction(BaseWindowAction):
    """Экшн окна 'Обновление справочников в ЕСНСИ'"""
    __PERMISSION_NS = (
        "kinder.users.actions.ENSIActionPack.UpdateClassifierAction")
    verbose_name = 'Обновление справочников в ЕСНСИ'
    need_check_permission = True
    perm_code = 'edit'

    def create_window(self):
        self.win = AvailableClassifierWindow()

    def set_window_params(self):
        self.win_params['form_url'] = (
            self.get_absolute_url())


class UpdateClassifierRowsAction(BaseAction):
    """Экшн создания грида окна 'Обновление справочников в ЕСНСИ'"""

    def run(self, request, context):

        query = ESNSIClassifier.objects.values(
            'id','updateclassifierrequest__id', 'name',
            'updateclassifierrequest__request_sent',
            'updateclassifierrequest__request_result',
        ).order_by('classifier_class','-updateclassifierrequest__id').distinct(
            'classifier_class')

        rows = [{
            'id': obj['id'], 'name': obj['name'],
            'last_load_date': obj['updateclassifierrequest__request_sent'] or '',
            'status': dict(UpdateClassifierRequest.RESULT_CHOICES).get(
                obj['updateclassifierrequest__request_result']
            ) or ('В ожидании' if obj['updateclassifierrequest__request_sent'] else '')}
            for obj in query]

        return PreJsonResult({'rows': rows, 'total': len(rows)})


class ESNSISetTaskAction(BaseAction):
    """Экшн постановки задачи для справочников в ЕСНСИ"""

    def context_declaration(self):
        context = super().context_declaration()

        context['classifier'] = {
            'type': 'int_list',
            'default': None
        }
        context['action_type'] = {
            'type': 'str',
            'default': None
        }

        return context

    def run(self, request, context):
        if context.action_type not in (
                UpdateClassifierRequest.UPDATE_CLASSIFIERS,
                UpdateClassifierRequest.DELETE_CLASSIFIERS
        ):
            return PreJsonResult(data={'success': False})

        all_classifiers = ESNSIClassifier.objects.filter(
            id__in=context.classifier)

        for classifier in all_classifiers:

            # Получает класс классификатора и создает выборку данных
            # для последующего формирования запроса
            classifier_class = classifier.get_classifier_class_by_name()
            classifier_obj = classifier_class()
            data_queryset = classifier_obj.data_queryset()
            data = data_queryset.filter(classifier_obj.queryset_filter())

            ESNSITaskFacade(
                classifier=classifier,
                request_type=context.action_type,
                instances=list(data),
                all_=True
            ).chose_factory_set_task()

        return PreJsonResult(data={'success': True})


class ClassifierUpdatePack(ObjectPack):
    """Пак для обновления справочников в ЕСНСИ"""

    __PERMISSION_NS = "kinder.users.actions.ENSIActionPack"

    title = _('Отправка справочников в ЕСНСИ')
    width = 800
    height = 400

    list_readonly = False
    need_check_permission = True
    PERM_VIEW = 'edit'
    sub_permissions = {
        PERM_VIEW: 'Обновление справочников в ЕСНСИ',
    }

    columns = [
        dict(
            header='Наименование справочника',
            data_index='name',
            sortable=True,
        ),
        dict(
            header='Дата последней выгрузки',
            data_index='last_load_date',
            sortable=False,
        ),
        dict(
            header='Состояние',
            data_index='status',
            sortable=False,
        ),
    ]

    def __init__(self,):
        super(ClassifierUpdatePack, self).__init__()

        self.update_classifier = UpdateClassifierAction()
        self.rows_action = UpdateClassifierRowsAction()
        self.set_task_action = ESNSISetTaskAction()

        self.actions.extend([
            self.update_classifier,
            self.rows_action,
            self.set_task_action
        ])

    def extend_menu(self, desk):
        return desk.SubMenu(
            _('Администрирование'),
            desk.SubMenu(
                _('Отправка справочников в ЕСНСИ'),
                desk.Item(
                    _('Обновление справочников в ЕСНСИ'),
                    pack=self.update_classifier
                ),
                icon='menu-dicts-16',
            ),
            icon='menu-dicts-16',
        )
