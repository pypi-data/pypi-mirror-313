from m3.plugins import ExtensionHandler
from m3.plugins import ExtensionPoint
from m3.plugins import ExtensionManager

from .extensions import get_agreement_on_other_group
from .extensions import get_executors
from .extensions import get_order_request_builder
from .extensions import get_parsing_module
from .extensions import get_unit_params
from .extensions import get_update_order_request_builder
from .extensions import service_type_smev4
from .extensions import extend_esnsi_classifier_fields
from .extensions import extend_esnsi_classifier_data
from .listeners import register_listeners

register_listeners()

def register_extensions():
    """Регистрация точек расширения плагина"""

    ExtensionManager().register_point(ExtensionPoint(
        name='concentrator.smev3_v4.extensions.get_parsing_module',
        default_listener=ExtensionHandler(handler=get_parsing_module)
    ))
    ExtensionManager().register_point(ExtensionPoint(
        name='concentrator.smev3_v4.extensions.service_type_smev4',
        default_listener=ExtensionHandler(handler=service_type_smev4)
    ))
    ExtensionManager().register_point(ExtensionPoint(
        name='concentrator.smev3_v4.extensions.get_executors',
        default_listener=ExtensionHandler(handler=get_executors)
    ))
    ExtensionManager().register_point(ExtensionPoint(
        name='concentrator.smev3_v4.extensions.get_unit_params',
        default_listener=ExtensionHandler(handler=get_unit_params)
    ))
    ExtensionManager().register_point(ExtensionPoint(
        name='concentrator.smev3_v4.extensions.get_agreement_on_other_group',
        default_listener=ExtensionHandler(handler=get_agreement_on_other_group)
    ))
    ExtensionManager().register_point(ExtensionPoint(
        name='concentrator.smev3_v4.extensions.get_order_request_builder',
        default_listener=ExtensionHandler(handler=get_order_request_builder)
    ))
    ExtensionManager().register_point(ExtensionPoint(
        name='concentrator.smev3_v4.extensions.get_update_order_request_builder',
        default_listener=ExtensionHandler(handler=get_update_order_request_builder)
    ))
    ExtensionManager().register_point(ExtensionPoint(
        name='concentrator.smev3_v4.extensions.extend_esnsi_classifier_fields',
        default_listener=ExtensionHandler(handler=extend_esnsi_classifier_fields)
    ))
    ExtensionManager().register_point(ExtensionPoint(
        name='concentrator.smev3_v4.extensions.extend_esnsi_classifier_data',
        default_listener=ExtensionHandler(handler=extend_esnsi_classifier_data)
    ))
