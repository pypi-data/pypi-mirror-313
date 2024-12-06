from django.db import migrations, models

from concentrator.models import ChangeDeclaration

import json


def move_privelege_comment_field(apps, schema_editor):
    """
    Метод уберет словарь с ключем comment_privileges из списка значений по ключу Declaration
    в поле data модели ChangeDeclaration, которое содержит словарь, и добавит новый словарь
    в список значений ключа PrivilegeComment вида {"concentrator_comment": []}.
    Значение concentrator_comment будет равно значению comment_privileges.
    """
    changes = ChangeDeclaration.objects.all()
    for change in changes:
        change_data = json.loads(change.data)
        if 'Declaration' in change_data:
            for i in range(len(change_data['Declaration'])):
                if 'comment_privileges' in change_data['Declaration'][i]:
                    if 'PrivilegeComment' not in change_data:
                        change_data['PrivilegeComment'] = []
                    change_data['PrivilegeComment'].append(
                        {'concentrator_comment': change_data['Declaration'][i]['comment_privileges']})
                    del change_data['Declaration'][i]
                    break
        change.data = json.dumps(change_data)
        change.save()


class Migration(migrations.Migration):
    dependencies = [
        ('concentrator', '0004_migrate_privileges'),
    ]

    operations = [
        migrations.RunPython(
            move_privelege_comment_field, reverse_code=migrations.RunPython.noop),
        migrations.AlterModelOptions(
            name='privilegecomment',
            options={'verbose_name': 'Комментарий к льготе'},
        ),
        migrations.AlterField(
            model_name='privilegecomment',
            name='concentrator_comment',
            field=models.TextField(
                null=True, verbose_name='Комментарий из концентратора'),
        ),
    ]
