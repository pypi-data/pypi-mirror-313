# coding: utf-8

import json

from m3_ext.ui.misc.store import ExtDataStore
from objectpack.ui import ModelEditWindow
from objectpack.ui import make_combo_box

from concentrator.change import map_changes
from concentrator.models import UpdateParams


class EditWindow(ModelEditWindow):
    model = UpdateParams

    def _init_components(self):
        super(EditWindow, self)._init_components()

        self.field__model_name = make_combo_box(
            data=map_changes.get_store_models(),
            label=u'Наименование модели',
            name='model_name',
            allow_blank=False)
        self.field__field_name = make_combo_box(
            label=u'Наименование поля',
            name='field_name', data=(),
            allow_blank=False)
        self._controls = [self.field__model_name, self.field__field_name]

    def set_params(self, params):
        super(EditWindow, self).set_params(params)
        self.template_globals = 'ui-js/edit_update_params.js'
        list_fields = map_changes.get_fields()
        self.model_fields = json.dumps(list_fields)
        if not params['create_new']:
            if self.field__model_name.value in list(list_fields.keys()):
                store = list_fields[self.field__model_name.value]
                self.field__field_name.set_store(
                    ExtDataStore(data=store))
