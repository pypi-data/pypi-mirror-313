from django.db import migrations
from django.db import models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('children', '0037_set_address_parsed'),
        ('smev3_v321', '0013_auto_20220517_1309'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendedChildrenDelegate',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('order_id',
                 models.CharField(max_length=100,
                                  unique=True,
                                  verbose_name='Идентификатор')),
                ('children_delegate',
                 models.OneToOneField(
                     on_delete=django.db.models.deletion.CASCADE,
                     to='children.ChildrenDelegate',
                     verbose_name='Представитель ребенка')),
            ],
            options={
                'verbose_name':
                'Дополнительные данные представителя ребенка (СМЭВ 3)',
                'db_table': 'concentrator_smev3_v321_children_delegate',
            },
        ),
    ]
