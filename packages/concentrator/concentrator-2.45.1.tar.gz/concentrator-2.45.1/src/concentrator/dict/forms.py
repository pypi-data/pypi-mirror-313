from m3_ext.ui import all_components as ext
from objectpack.ui import BaseEditWindow
from objectpack.ui import make_combo_box

from .constants import ModelForSend
from .constants import OperationEnumerate


class ParamsWindow(BaseEditWindow):

    def _init_components(self):
        super(ParamsWindow, self)._init_components()
        self.operation = make_combo_box(data=OperationEnumerate.get_choices(),
                                        label=u'Тип операции',
                                        name='operation',
                                        anchor='100%',)
        self.dict_name = make_combo_box(data=ModelForSend.get_choices(),
                                        label=u'Справочник',
                                        name='dict_name',
                                        anchor='100%',)
        self.message_size = ext.ExtNumberField(label=u'Размер сообщения',
                                               name='message_size',
                                               allow_negative=False,
                                               min_value=1,
                                               max_value=200,
                                               allow_decimals=False,
                                               value=200,
                                               allow_blank=False,
                                               anchor='100%',)
        self.save_btn.text = u'Запустить'

    def _do_layout(self):
        super(ParamsWindow, self)._do_layout()
        self.layout = 'form'
        self.form.items.extend([
            self.operation,
            self.dict_name,
            self.message_size
        ])

    def set_params(self, params):
        super(ParamsWindow, self).set_params(params)
        self.template_globals = 'ui-js/params_window.js'
        self.height = 200
