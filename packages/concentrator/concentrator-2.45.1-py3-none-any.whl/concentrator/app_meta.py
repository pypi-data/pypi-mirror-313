from kinder.controllers import dict_controller

from concentrator.changes.actions import ChangesDetailPack
from concentrator.changes.actions import ChangesPack
from concentrator.dict import signals
from concentrator.dict.actions import ServicesPack
from concentrator.update_conf.actions import UpdateConfigPack
import concentrator.changes.app_meta


def register_actions():
    """
    Метод регистрации Action'ов для приложения в котором описан
    """

    dict_controller.packs.extend([
        UpdateConfigPack(),
        ChangesDetailPack(),
        ChangesPack(),
        ServicesPack()
    ])
