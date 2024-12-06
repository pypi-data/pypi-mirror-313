import django.contrib.postgres.fields.jsonb
import django.db.models.deletion

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('smev3_v321', '0011_auto_20211129_1647'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingUpdateOrderRequest',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('created',
                 models.DateTimeField(auto_now_add=True,
                                      db_index=True,
                                      null=True,
                                      verbose_name='Создан')),
                ('modified',
                 models.DateTimeField(auto_now=True,
                                      db_index=True,
                                      null=True,
                                      verbose_name='Изменен')),
                ('source_version',
                 models.PositiveSmallIntegerField(
                     choices=[(0, 'Отказ в изменении заявления'),
                              (1, 'Создание изменений заявления'),
                              (2, 'Изменение статуса заявления'),
                              (3,
                               'Изменение данных заявления (кроме статуса)'),
                              (4, 'Изменение желаемых ДОО заявления'),
                              (5, 'Изменение статуса направления заявления'),
                              (6, 'Изменение данных ребенка')],
                     verbose_name='Версия источника')),
                ('data',
                 django.contrib.postgres.fields.jsonb.JSONField(
                     blank=True,
                     default=dict,
                     null=True,
                     verbose_name='Данные для отправки данных об изменении')),
                ('order_request',
                 models.ForeignKey(
                     on_delete=django.db.models.deletion.CASCADE,
                     to='smev3_v321.OrderRequest',
                     verbose_name='Запрос передачи данных заявления в ЛК ЕПГУ')
                 ),
            ],
            options={
                'verbose_name':
                'Отложенный запрос передачи данных об изменении статуса заявления в ЛК ЕПГУ',
                'db_table':
                'concentrator_smev3_v321_pendingupdateorderrequest',
            },
        ),
    ]
