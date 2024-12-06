# coding: utf-8

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from concentrator.dict.constants import ModelForSend
from concentrator.dict.constants import OperationEnumerate
from concentrator.dict.proxy import GroupAgeSubCathegoryProxy
from concentrator.dict.proxy import GroupStatisticProxy
from concentrator.dict.proxy import HealthNeedProxy
from concentrator.dict.proxy import PrivilegeProxy
from concentrator.dict.proxy import UnitProxy


class Command(BaseCommand):

    help = 'Send dictionaries info to concentrator [-U] [--size]'

    def add_arguments(self, parser):

        parser.add_argument(
            '-O',
            action='store',
            dest='mode',
            choices=[OperationEnumerate.UPDATE,
                     OperationEnumerate.ADD,
                     OperationEnumerate.DELETE],
            default=OperationEnumerate.UPDATE,
            help='Send data to update, delete or adding it'
        )

        parser.add_argument(
            '-D',
            action='store',
            dest='dict',
            choices=list(ModelForSend.values.keys()),
            default=ModelForSend.UNIT,
            help='NameDict'
        )

        parser.add_argument(
            '--size',
            action='store',
            dest='size',
            default=200,
            help='Send data to update instead of adding it'
        )

    def handle(self, *args, **options):
        """
        Если команда вызвана с ключом -U, то данные
        будут отправлены на обновление. В противном случае - на добавление.
        """
        operation = options['mode']
        try:
            size = int(options['size'])
        except ValueError:
            raise CommandError(
                u'option --size must have an integer argument. '
                u'Example: --size 10')

        proxy_classes = (
            GroupAgeSubCathegoryProxy,
            HealthNeedProxy,
            PrivilegeProxy,
            UnitProxy,
            GroupStatisticProxy,
        )
        for proxy_class in proxy_classes:
            if options['dict'] == proxy_class.__name__:
                proxy_class().send_all(operation, size)
