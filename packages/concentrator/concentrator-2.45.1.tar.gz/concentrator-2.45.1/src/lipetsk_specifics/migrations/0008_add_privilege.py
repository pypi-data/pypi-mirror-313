from django.db import migrations

from kinder.core.dict.models import PrivilegeOrderType
from kinder.core.dict.models import PrivilegeType
from kinder.core.privilege.models import Privilege as OriginalPrivilege
from kinder.core.privilege.models import PrivilegeOperateTypeEnum


# Данные о льготе
privilege_dict = dict(
    code='',
    name=('Дети сотрудников органов принудительного исполнения '
          'Российской Федерации по месту жительства'),
    type_id=PrivilegeType.FED,
    order_type_id=PrivilegeOrderType.FIRST_ORDER,
    operate_type=PrivilegeOperateTypeEnum.SIMPLE,
    duration_type=OriginalPrivilege.ENDLESS
)


def create_new_privilege(apps, schema_editor):
    """Создание новой льготы, используя данные из словаря privilege_dict."""

    Privilege = apps.get_model('privilege', 'Privilege')
    Privilege.objects.create(**privilege_dict)


def delete_privilege(apps, schema_editor):
    """Удаление льготы с наименованием из словаря privilege_dict."""

    Privilege = apps.get_model('privilege', 'Privilege')
    Privilege.objects.filter(name=privilege_dict['name']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('privilege', '0008_auto_20200207_1326'),
        ('lipetsk_specifics', '0007_auto_20190617_1350'),
    ]

    operations = [
        migrations.RunPython(create_new_privilege, delete_privilege)
    ]
