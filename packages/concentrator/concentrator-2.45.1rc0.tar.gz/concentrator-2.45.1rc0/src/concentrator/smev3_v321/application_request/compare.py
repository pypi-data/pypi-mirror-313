import datetime

from django.utils import timezone
from educommon.contingent import catalogs

from kinder.core.utils.address import get_gar_code

from .utils import get_address_place_code
from .utils import get_application_request_full_address


def compare_date(concentrator_val, instance_val, conc_object, save_object):
    """Выполняет сравнение дат."""
    clean_conc_val = concentrator_val
    clean_inst_val = instance_val
    if isinstance(concentrator_val, datetime.datetime):
        clean_conc_val = concentrator_val.date()
    if isinstance(instance_val, datetime.datetime):
        clean_inst_val = instance_val.date()
    return clean_conc_val == clean_inst_val


def compare_str(concentrator_value, instance_value, conc_object, save_object):
    """Выполняет сравнение строк."""
    clean_conc_val = concentrator_value or ''
    clean_inst_val = instance_value or ''
    return clean_conc_val.lower() == clean_inst_val.lower()


def compare_bool_int(concentrator_value, instance_value, conc_object, save_object):
    """Выполняет сравнение целых чисел/булевы."""
    return concentrator_value == instance_value


def compare_bool_not_null(concentrator_value, instance_value, conc_object, save_object):
    """Выполняет сравнение обязательных булевых значений."""
    return bool(concentrator_value) == bool(instance_value)


def compare_datetime(concentrator_value, instance_value, conc_object, save_object):
    """Выполняет сравнение даты с временем."""
    clean_conc_val = (
        timezone.make_naive(
            concentrator_value, timezone.get_default_timezone())
        if timezone.is_aware(concentrator_value) else concentrator_value)

    clean_inst_val = instance_value
    return clean_conc_val == clean_inst_val


def compare_esnsi(concentrator_value, instance_value, conc_object, save_object):
    """Выполняет сравнение записей справочника"""
    return instance_value and instance_value.esnsi_code == concentrator_value


def compare_null_esnsi(concentrator_value, instance_value, conc_object, save_object):
    """Выполняет сравнение записей справочника.

    Блока может и не быть.
    """
    if concentrator_value is None:
        return True
    return instance_value and instance_value.esnsi_code == concentrator_value


def compare_parent_doc(concentrator_value, instance_value, conc_object, save_object):
    """Выполняет сравнение названий документа, подтверждающего права"""
    # Если указано то пытаемся найти, если находим - сравниваем, 
    # если не находим - пропускаем, если не указано, смотрим что не было указано ранее
    if concentrator_value:
        reverse_map = {v: k for k, v in catalogs.DocumentConfirmingTypes.values.items()}
        concentrator_value = reverse_map.get(concentrator_value, None)
        return concentrator_value is None or instance_value == concentrator_value
    else:
        return not bool(instance_value)


def compare_parents(concentrator_value, instance_value, conc_object, save_object):
    """Сравнивает пол родителя."""

    from concentrator.smev3_v321.utils import update_middle_name_params

    midname = conc_object.PersonInfo.PersonMiddleName
    params = {}
    update_middle_name_params(
        midname, params, is_parents=concentrator_value, is_initial=True)

    value = params.get('type')
    return value and value == instance_value


def compare_fias(concentrator_value, instance_value, conc_object, save_object):
    """
    Сравнение кодов ФИАС
    """
    if not concentrator_value:
        return bool(instance_value) == bool(concentrator_value)
    concentrator_value = get_gar_code(concentrator_value)
    return instance_value == concentrator_value


def compare_place_fias(
        concentrator_value, instance_value, conc_object, save_object):
    """
    Сравнение кодов ФИАС для населенного пункта.
    """

    concentrator_value = get_address_place_code(conc_object.Address)
    if concentrator_value:
        return instance_value == concentrator_value
    else:
        return bool(instance_value) == bool(concentrator_value)


def compare_full_address(
        concentrator_value, instance_value, conc_object, save_object):
    """Сравнение полного разобранного адреса из запроса с полным адресом в БД"""
    concentrator_value = get_application_request_full_address(
        conc_object.Address)

    return instance_value == concentrator_value
