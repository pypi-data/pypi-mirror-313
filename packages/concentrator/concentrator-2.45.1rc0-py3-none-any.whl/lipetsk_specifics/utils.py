# coding: utf-8

from django.conf import settings
from kinder.core.declaration.models import Declaration
from kinder.core.declaration.models import DeclarationStatusLog
from kinder.core.declaration_status.models import DSS


def in_queue_upd(variables, ctx):
    """Выполняет обновление параметров для отчета.

    :param variables: данные для отчета
    :type variables: dict
    :param ctx: контекст (объект генератора)

    :return: возвращает обновленные данные
    """

    mo_name = (
        Declaration.objects.filter(
            id=ctx.declaration_id).values_list('mo__name', flat=True).first())

    variables['mo'] = mo_name
    variables['units_list'] = [
        dict(unit_num=f"{unit['num']}.", unit_name=unit['unit_name'])
        for unit in variables['units']]
    variables['user_name'] = ctx.profile.get_fio()

    return variables


def reject_upd(variables, ctx):
    [variables['reject_reason']] = Declaration.objects.get(
        id=ctx.declaration_id
    ).declarationrejectreason_set.values_list(
        'reject_reason__name', flat=True)[:1] or ['']
    status_date = DeclarationStatusLog.objects.filter(
        declaration__client_id=variables['decl_id'],
        status__code=DSS.REFUSED).latest('datetime')
    variables['status_date'] = status_date.datetime.strftime(
        "%d.%m.%Y") if status_date else ''

    return variables


def date2str(value):
    if value:
        result = '{0} г.'.format(value.strftime('%d.%m.%Y'))
    else:
        result = ''

    return result


def get_upload_dir(instance, filename):
    return '/'.join([settings.DOWNLOADS, filename])
