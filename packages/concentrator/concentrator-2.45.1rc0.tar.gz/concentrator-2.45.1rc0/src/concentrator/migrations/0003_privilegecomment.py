import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concentrator', '0002_auto_20170206_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivilegeComment',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('concentrator_comment',
                 models.TextField(
                     verbose_name='Комментарий из концентратора')),
                ('declaration_privilege',
                 models.OneToOneField(
                     on_delete=django.db.models.deletion.CASCADE,
                     related_name='declaration_privilege',
                     to='declaration.DeclarationPrivilege')),
            ],
        ),
    ]
