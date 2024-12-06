from m3_ext.ui import all_components as ext

from kinder.controllers import obs
from kinder.plugins.helpers import extend_template_globals


@obs.subscribe
class EpguSubscribedFilterListener:
    """
    Добавляет в реестр заявок фильтр в меню "Отобразить заявки"
    "Только заявки, подписанные на уведомления через ЕПГУ".
    """
    priority = 20

    listen = [
        'kinder.core.queue_module.declaration/'
        'QueueDeclarationPack/QueueDeclaratonListWindowAction'
    ]

    def configure_list_window(self, params):
        win = params['win']
        win.is_epgu_subscribed_only = ext.ExtCheckBox(
            box_label='Только заявки, подписанные на уведомления через ЕПГУ',
            name='is_epgu_subscribed_only',
        )

        win.menu.items.append(win.is_epgu_subscribed_only)

        extend_template_globals(
            win, 'ui-js/smev3-v321-declaration-list-window.js')

        return params
