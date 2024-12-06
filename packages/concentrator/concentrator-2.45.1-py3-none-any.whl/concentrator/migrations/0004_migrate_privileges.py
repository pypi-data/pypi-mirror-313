from django.db import migrations
from django.db.models import Q

from kinder.core.declaration.enum import DeclarationSourceEnum


DSE = DeclarationSourceEnum


def migrate_privileges(apps, schema_editor):
    u"""Переносит комментарий концентратора по льготе в льготу"""

    privileges = apps.get_model('declaration', 'DeclarationPrivilege')
    privilege_comment = apps.get_model('concentrator', 'PrivilegeComment')

    q_comment_privileges_empty = Q(declaration__comment_privileges='')
    q_comment_privileges_null = Q(declaration__comment_privileges=None)

    for obj in privileges.objects.filter(
            declaration__source=DSE.CONCENTRATOR).exclude(q_comment_privileges_empty |
                                                          q_comment_privileges_null).iterator():
        concentrator_comment = privilege_comment(
            declaration_privilege_id=obj.id,
            concentrator_comment=obj.declaration.comment_privileges)
        concentrator_comment.save()


class Migration(migrations.Migration):

    dependencies = [
        ('concentrator', '0003_privilegecomment'),
        ('declaration', '0012_declaration_defer_demand')
    ]

    operations = [
        migrations.RunPython(
            migrate_privileges, reverse_code=migrations.RunPython.noop),
    ]
