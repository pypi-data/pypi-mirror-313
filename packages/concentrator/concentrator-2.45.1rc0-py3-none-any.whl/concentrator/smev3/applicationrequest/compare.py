import datetime

from django.utils import timezone


def compare_model_id(concentrator_val, instance_val):
    return concentrator_val == instance_val.id


def compare_dict_code(concentrator_val, instance_val):
    return str(concentrator_val) == getattr(instance_val, 'code', '')


def compare_date(concentrator_val, instance_val):
    clean_conc_val = concentrator_val
    clean_inst_val = instance_val
    if isinstance(concentrator_val, datetime.datetime):
        clean_conc_val = concentrator_val.date()
    if isinstance(instance_val, datetime.datetime):
        clean_inst_val = instance_val.date()
    return clean_conc_val == clean_inst_val


def compare_str(concentrator_value, instance_value):
    clean_conc_val = concentrator_value or ''
    clean_inst_val = instance_value or ''
    return clean_conc_val.lower() == clean_inst_val.lower()


def compare_bool_int(concentrator_value, instance_value):
    return concentrator_value == instance_value


def compare_datetime(concentrator_value, instance_value):
    clean_conc_val = (
        timezone.make_naive(
            concentrator_value, timezone.get_default_timezone())
        if timezone.is_aware(concentrator_value) else concentrator_value)

    clean_inst_val = instance_value
    return clean_conc_val == clean_inst_val
