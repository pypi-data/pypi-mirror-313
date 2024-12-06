from m3.actions import ControllerCache
from m3_ext.ui import all_components as ext
from objectpack.ui import BaseEditWindow
from objectpack.ui import ComboBoxWithStore

from concentrator.smev3_v321.models import UpdateClassifierRequest


ACTION_TYPES = (
    (UpdateClassifierRequest.UPDATE_CLASSIFIERS, 'Изменение'),
    (UpdateClassifierRequest.DELETE_CLASSIFIERS, 'Удаление'),
)


class AvailableClassifierWindow(BaseEditWindow):
    """Окно 'Обновление справочников в ЕСНСИ'"""

    def _init_components(self):
        super()._init_components()

        self.width, self.height = 450, 140

        self.action_type = ComboBoxWithStore(
            label='Действие',
            name='action_type',
            data=ACTION_TYPES,
            allow_blank=False,
            editable=False,
            anchor='100%',
        )
        self.classifier = ext.ExtMultiSelectField(
            allow_blank=False,
            delimeter=';',
            hide_trigger=True,
            hide_dict_select_trigger=False,
            ask_before_deleting=False,
            label='Справочник',
            hide_clear_trigger=True,
            pack='concentrator.smev3_v321.esnsi.actions.ClassifierUpdatePack',
            anchor='100%')

    def _do_layout(self):
        super()._do_layout()

        self.form.items.extend([
            self.classifier, self.action_type
        ])

    def set_params(self, params):
        super().set_params(params)

        self.title = 'Обновление справочников в ЕСНСИ'
        self.buttons[0].text = 'Отправить'
        self.buttons[0].handler = 'setTasks'
        self.template_globals = 'ui-js/update_classifiers.js'
        self.set_task_url = ControllerCache.find_pack(
            'concentrator.smev3_v321.esnsi.actions.ClassifierUpdatePack'
        ).set_task_action.get_absolute_url()
