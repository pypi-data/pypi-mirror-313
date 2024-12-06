from urllib.error import URLError

from django.core.management import call_command
from m3.actions import ACD
from m3.actions import Action
from m3.actions import ActionPack
from m3.actions import ApplicationLogicException
from m3.actions import OperationResult
from m3_ext.ui.results import ExtUIScriptResult

from kinder import logger

from . import forms


class ServicesPack(ActionPack):
    """
    """
    __PERMISSION_NS = "kinder.plugins.concentrator.dict.actions.ServicesPack"
    title = u'Отправка справочников в ЕПГУ'
    url = '/load_data'
    need_check_permission = True

    def __init__(self):
        super(ServicesPack, self).__init__()
        self.list_window_action = ServiceWindowAction()
        self.do_action = ServiceAction()
        self.actions = [
            self.list_window_action,
            self.do_action
        ]

    def extend_menu(self, desk, *args, **kwargs):
        return desk.SubMenu(
            u'Администрирование',
            desk.Item(
                self.title,
                pack=self.list_window_action,
            ),
            icon='menu-dicts-16',
        )


class ServiceWindowAction(Action):
    __PERMISSION_NS = (
        "kinder.plugins.concentrator.dict.actions.ServiceWindowAction")
    need_check_permission = True
    verbose_name = u'Запуск'
    url = '/go'
    perm_code = 'go_perm'

    def run(self, request, context):
        win = forms.ParamsWindow()
        params = dict()
        params['form_url'] = self.parent.do_action.absolute_url()
        params['title'] = self.parent.title
        win.set_params(params=params)
        return ExtUIScriptResult(win)


class ServiceAction(Action):
    url = '/do'

    def context_declaration(self):
        return [ACD(name='operation', required=True, type=str),
                ACD(name='dict_name', required=True, type=str),
                ACD(name='message_size', required=True, type=int),
                ]

    def run(self, request, context):
        try:
            call_command(
                'send_dicts_to_concentrator',
                mode=context.operation,
                dict=context.dict_name,
                size=context.message_size
            )
        except URLError:
            msg = u'Ошибка соединения с сервисом при отправке справочников.'
            logger.exception(msg)
            raise ApplicationLogicException(msg)
        except Exception:
            msg = u'При отправке справочников произошла ошибка.'
            logger.exception(msg)
            raise ApplicationLogicException(msg)

        return OperationResult(success=True, message='')
