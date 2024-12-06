from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from m3.plugins import ExtensionManager

from kinder import settings as kinder_settings
from kinder.core.declaration.enum import DeclarationSourceEnum
from kinder.core.declaration.enum import DeclarationTypeInteractionEnum as DTIE
from kinder.core.declaration.models import Declaration
from kinder.core.declaration_status.signals import declaration_status_change
from kinder.core.dict.models import DouType
from kinder.core.dict.models import GroupAgeSubCathegory
from kinder.core.dict.models import HealthNeed
from kinder.core.dict.models import UnitKind
from kinder.core.privilege.models import Privilege
from kinder.core.unit.models import Unit
from kinder.core.unit.models import UnitStatus
from concentrator import settings
from concentrator.dict.proxy import GroupAgeSubCathegoryProxy
from concentrator.dict.proxy import HealthNeedProxy
from concentrator.dict.proxy import PrivilegeProxy
from concentrator.dict.proxy import UnitProxy
from concentrator.dict.signal_handlers import obj_delete_handler
from concentrator.dict.signal_handlers import obj_save_handler
from concentrator.tasks import SendUpdateApplicationState


# -----------------------------------------------------------------------------
# Для модели Организации более сложное поведение,
# создание отправляем:
# - при создании c типом ДОО
# - при смене типа на ДОО
# обновление отправляем:
# - если были внесены изменения в организацию с типом ДОО
# удаление отправляем:
# - при удалении организации с типом ДОО
# - при смене типа с ДОО на любой другой
# -----------------------------------------------------------------------------
@receiver(post_save, sender=Unit)
def sign_unit_save(sender, instance, **kwargs):
    """
    В концентратор уходят только организации с типом ДОО
    , при создании с типом ДОО, при смене типа с любого другого на ДОО
    , с разрешением на отображение на портале, пустым либо гос. типом ДОО
    @param sender:
    @param instance:
    @param kwargs:
    @return:
    """

    def is_for_ignore(instance):
        """
        Проверка следует ли игнорировать организацию
        Условия:
            Запрет на отображение на портале
            Тип ДОО не гос. (только при включенном SMEV_ONLY_GOV_DOU_OR_EMPTY)
        """

        result = (
            # Если запрет показа на портале
            instance.is_not_show_on_poral or
            # Или статус организации который нельзя отправлять на портал
            instance.status in UnitProxy.unit_statuses_for_delete
        )

        if kinder_settings.SMEV_ONLY_GOV_DOU_OR_EMPTY:
            # Если тип ДОО не None или не гос.
            result |= (instance.dou_type_id is not None
                       and instance.dou_type.code not in
                       DouType.GOVERNMENT_TYPES)

        return result

    def is_for_delete(instance):
        """
        Проверка следует ли посылать запрос на удаление организации
        Условия:
            Запрет на отображение на портале
            Тип ДОО не гос. (только при включенном SMEV_ONLY_GOV_DOU_OR_EMPTY)
        """
        previous_status = previous_state['status']
        previous_is_not_show_on_poral = previous_state['is_not_show_on_poral']
        original_dou_type_id = previous_state['dou_type_id']

        # Если была смена запрета на показ на портале False -> True
        result = (instance.is_not_show_on_poral
                  and not previous_is_not_show_on_poral)

        result = result or (
            # Если статус был который можно было отправлять на портал
            previous_status not in UnitProxy.unit_statuses_for_delete and
            # И установили тот что нельзя
            instance.status in UnitProxy.unit_statuses_for_delete
        )

        if kinder_settings.SMEV_ONLY_GOV_DOU_OR_EMPTY:
            # Если была смена типа ДОО (None, гос.) -> любой другой
            result |= ((instance.dou_type_id is not None
                       and instance.dou_type.code
                        not in DouType.GOVERNMENT_TYPES)
                       and instance.dou_type_id != original_dou_type_id)

            # Если ранее не было случаев подпадающих под удаление
            result &= not (
                (instance.is_not_show_on_poral
                 == previous_is_not_show_on_poral is True)
                or ((instance.dou_type_id is not None
                     and instance.dou_type.code not in DouType.GOVERNMENT_TYPES
                     ) and instance.dou_type_id == original_dou_type_id)
            )

        return result

    def is_for_create(instance):
        """
        Проверка следует ли посылать запрос на создание организации
        """
        previous_status = previous_state['status']
        previous_is_not_show_on_poral = previous_state['is_not_show_on_poral']
        original_dou_type_id = previous_state['dou_type_id']

        # Если была смена запрета на показ на портале True -> False
        result = (not instance.is_not_show_on_poral
                  and previous_is_not_show_on_poral)

        result = result or (
            # Если раньше статус был который нельзя показывать на портале
            previous_status in UnitProxy.unit_statuses_for_delete and
            # И заменили на тот что можно
            instance.status not in UnitProxy.unit_statuses_for_delete
        )

        if kinder_settings.SMEV_ONLY_GOV_DOU_OR_EMPTY:
            # Если была смена типа ДОО любой другой -> (None, гос.)
            result |= ((instance.dou_type_id is None
                       or instance.dou_type.code in DouType.GOVERNMENT_TYPES)
                       and
                       instance.dou_type_id != original_dou_type_id)

        return result

    if not kwargs['created']:
        previous_state = instance.previous_state()
        original_kind = previous_state['kind_id']
        # Создание ДОО при смене типа организации на ДОО
        if (instance.kind_id == UnitKind.DOU
            and original_kind != UnitKind.DOU):

            if not is_for_ignore(instance):
                obj_save_handler(instance, UnitProxy, True)
        # Обновление ДОО при внесении изменений в организацию с типом ДОО
        elif (instance.kind_id == UnitKind.DOU
              and original_kind == UnitKind.DOU):

            if is_for_delete(instance):
                obj_delete_handler(instance, UnitProxy)
            elif not is_for_ignore(instance):
                obj_save_handler(instance, UnitProxy, is_for_create(instance))
        # Удаление ДОО при смене типа с ДОО на любой другой
        elif (instance.kind_id != UnitKind.DOU
              and original_kind == UnitKind.DOU):
            obj_delete_handler(instance, UnitProxy)

    # Создание ДОО, если тип организации ДОО
    elif (kwargs['created']
          and instance.kind_id == UnitKind.DOU
          and not is_for_ignore(instance)):
        obj_save_handler(instance, UnitProxy, True)


@receiver(post_delete, sender=Unit)
def sign_unit_delete(sender, instance, **kwargs):
    # удаление организации с типов ДОО
    if instance.kind_id == UnitKind.DOU:
        obj_delete_handler(instance, UnitProxy)


# -----------------------------------------------------------------------------
# Сигналы на создания/изменения в справочниках
# -----------------------------------------------------------------------------
@receiver(post_save, sender=GroupAgeSubCathegory)
def sign_group_age_sub_cathegory_save(sender, instance, **kwargs):
    obj_save_handler(instance, GroupAgeSubCathegoryProxy, kwargs['created'])


@receiver(post_save, sender=HealthNeed)
def sign_health_need_save(sender, instance, **kwargs):
    obj_save_handler(instance, HealthNeedProxy, kwargs['created'])


@receiver(pre_save, sender=Privilege)
def store_original_object(instance, **kwargs):
    instance.original_object = (
        Privilege.objects.get(id=instance.id)
        if instance.id
        else None
    )


@receiver(post_save, sender=Privilege)
def sign_privilege_save(instance, **kwargs):
    if kwargs['created']:
        # Отправляем запрос на добавление, если не указан "Не учитывать"
        if not instance.cant_add:
            obj_save_handler(instance, PrivilegeProxy, True)
    else:
        # Изменение льготы
        if instance.cant_add and not instance.original_object.cant_add:
            # изменили тип на "Не учитывать", отправляем запрос на удаление
            obj_delete_handler(instance, PrivilegeProxy)
        elif not instance.cant_add and instance.original_object.cant_add:
            # изменили тип с "Не учитывать", отправляем запрос на добавление
            obj_save_handler(instance, PrivilegeProxy, True)
        else:
            # тип остался прежним, отправляем запрос на изменение
            obj_save_handler(instance, PrivilegeProxy, False)


# -----------------------------------------------------------------------------
# Сигналы на удаления в справочниках
# -----------------------------------------------------------------------------
@receiver(post_delete, sender=GroupAgeSubCathegory)
def sign_group_age_sub_cathegory_delete(sender, instance, **kwargs):
    obj_delete_handler(instance, GroupAgeSubCathegoryProxy)


@receiver(post_delete, sender=HealthNeed)
def sign_health_need_delete(sender, instance, **kwargs):
    obj_delete_handler(instance, HealthNeedProxy)


@receiver(post_delete, sender=Privilege)
def sign_privilege_delete(sender, instance, **kwargs):
    obj_delete_handler(instance, PrivilegeProxy)


def update_application_state(**kwargs):
    declaration = kwargs['declaration']
    is_auto = kwargs.get('is_auto')
    commentary = kwargs.get('commentary')
    log_id = kwargs['log_id']
    desired_date_changed = kwargs['desired_date_changed']
    auto_archive = kwargs.get('desired_date_changed', True)

    # Проверка существования записи о заявке в таблице DeclarationPortalID
    exists_declarationportalid = ExtensionManager().execute(
        'concentrator.smev3_v321.application_request.extensions.'
        'exists_declarationportalid', declaration)

    # UpdateState выполняется только для заявок пришедших из концентратора
    # по СМЭВ2.
    # https://conf.bars-open.ru/pages/viewpage.action?pageId=3080736
    # у которых изменился статус https://jira.bars.group/browse/EDUKNDG-10893
    if (declaration.client_id
            and declaration.source == DeclarationSourceEnum.CONCENTRATOR
            and kwargs['old_status'] != kwargs['new_status']
            and declaration.type_interaction == DTIE.SMEV_2
            and not exists_declarationportalid):
        SendUpdateApplicationState().apply_async(
            (),
            {
                'declaration_id': declaration.id,
                'is_auto': is_auto,
                'commentary': commentary,
                'log_id': log_id,
                'desired_date_changed': desired_date_changed,
                'auto_archive': auto_archive
            }
        )


if not settings.DISABLE_UPDATE_APPLICATION_STATE:
    declaration_status_change.connect(
        receiver=update_application_state,
        sender=Declaration,
    )
