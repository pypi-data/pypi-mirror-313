from typing import Any

from kinder.core.declaration.models import Declaration
from kinder.core.declaration_status.enum import DSS
from m3.actions import ControllerCache

from concentrator.smev3_v4.forms import DeclarationEditWindowExtender
from concentrator.smev3_v4.forms import DelegateEditWinExtender
from educommon.m3.extensions import BaseEditWinListener
from educommon.m3.extensions import BaseSaveListener

from kinder.controllers import obs


class EditDeclarationListener(BaseEditWinListener):
    """Добавляет в окно редактирования заявления чек-бокс Согласие на обучение по адаптированной
    образовательной программе
    """

    ui_extender_cls = DeclarationEditWindowExtender
    listen = [
        'kinder.core.declaration/DeclarationPack/DeclarationEditAction',
        'kinder.core.declaration/DeclarationPack/DeclarationAddAction',
        'kinder.core.queue_module.declaration/'
        'QueueDeclarationPack/QueueDeclarationEditAction',
        'kinder.core.queue_module.declaration'
        '/QueueDeclarationPack/DeclarationAddAction',
    ]
    parent_model_field = 'id'

    def _get_id(self, context):
        return getattr(context, self.action.parent.id_param_name, None)

    @staticmethod
    def add_decl_edit_perm_to_params(params: dict[str, Any], declaration: Declaration, request: Any) -> None:
        """Дополнение параметров окна значением возможности редактирования заявления

        :param params: Параметры окна
        :param declaration: Объект заявления
        :param request: Запрос
        """

        decl_pack = ControllerCache.find_pack('kinder.core.declaration.actions.DeclarationPack')
        has_edit_perm = (
            decl_pack.has_perm(request, decl_pack.EDIT_DECL) and
            declaration.status.code in DSS.status_confirmating()
        )
        params.update(dict(has_edit_perm=has_edit_perm))

    def after(self, request, context, response):
        extender = self.ui_extender_cls(response.data)
        row_id = self._get_id(context)
        if not row_id:
            return
        instance = self._get_instance(row_id)
        if not instance:
            return

        extender.bind_from_object(instance)
        params = self._get_params(instance, context)
        self.add_decl_edit_perm_to_params(params, instance, request)
        extender.set_params(params)


class DeclarationSaveListener(BaseSaveListener):
    """Сохранение дополнительных видов согласия для заявления"""

    listen = [
        'kinder.core.queue_module.declaration/'
        'QueueDeclarationPack/DeclarationSaveAction'
    ]

    ui_extender_cls = DeclarationEditWindowExtender
    parent_model_field = 'id'

    def _declare_additional_context(self):
        return {
            "adapted_program_consent": {
                "type": 'js_checkbox',
                'default': False
            },

        }

    def post_save(self, arguments):
        parent_model_instance, context = arguments
        super().post_save((parent_model_instance.declaration.id, context))

        return parent_model_instance, context


class DelegateEditWindowListener(BaseEditWinListener):
    """Добавляет в окно создания/редактирования карточки родителя чек-бокс
    Документ о праве нахождения в РФ
    """

    ui_extender_cls = DelegateEditWinExtender
    parent_model_field = 'id'

    listen = [
        'kinder.core.children/DelegateActionPack/DelegateEditAction',
        'kinder.core.children/'
        'DelegateForChildrenPack/CustomEditWindowAction',
        'kinder.core.children/'
        'DelegateForChildrenPack/DelegateNewAction',
        'kinder.core.children/'
        'DelegateForDeclarationPack/CustomEditWindowAction',
        'kinder.core.children/'
        'ForSelectWindowDelegatePack/DelegateSelectOrCreateWindowAction',
        'kinder.core.children/ForSelectWindowDelegatePack/DelegateNewAction',
        '.*/LipetskDelegateForDeclarationPack/CustomEditWindowAction',
        '.*/LipetskDelegateForDeclarationPack/ShowDataAction',
        '.*/DelegateForDeclarationPack/ShowDataAction',
    ]

    def _get_id(self, context):
        return getattr(context, self.action.parent.id_param_name, None)


class DelegateSaveActionListener(BaseSaveListener):
    """Выполняет сохранение карточки родителя с данными чек-бокса
    Документ о праве нахождения в РФ
    """

    ui_extender_cls = DelegateEditWinExtender
    parent_model_field = 'id'

    listen = [
        'kinder.core.children/DelegateActionPack/DelegateSaveAction',
        'kinder.core.children/DelegateForChildrenPack/DelegateSaveAction',
        'kinder.core.children/DelegateForDeclarationPack/DelegateSaveAction',
        'kinder.core.children/ForSelectWindowDelegatePack/DelegateSaveAction',
        '.*/LipetskDelegateForDeclarationPack/DelegateSaveAction',
        'kinder.core.children/DelegateForDeclarationPack/'
        'ContingentDelegateSaveAction',
    ]

    def _declare_additional_context(self):
        return {
            "confirming_rights_located_rf": {
                "type": 'js_checkbox',
                'default': False
            }
        }

    def _get_instance(self, parent_model_instance, context):
        """Модель не расширяется какой-либо другой моделью, поэтому возвращаем
        модель Delegate
        """
        return parent_model_instance


def register_listeners():
    obs.subscribe(EditDeclarationListener)
    obs.subscribe(DeclarationSaveListener)
    obs.subscribe(DelegateEditWindowListener)
    obs.subscribe(DelegateSaveActionListener)
