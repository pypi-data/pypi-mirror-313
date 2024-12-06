import django.db.models.deletion
import kinder.core.common

from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('declaration', '0024_declaration_type_interaction'),
        ('direct', '0013_change_direct_status'),
        ('concentrator.smev3', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventServiceRequest',
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
                ('external_id',
                 models.CharField(blank=True,
                                  db_index=True,
                                  max_length=32,
                                  null=True)),
                ('message_id',
                 models.UUIDField(blank=True,
                                  null=True,
                                  verbose_name='Идентификатор сообщения')),
                ('message_status',
                 models.PositiveSmallIntegerField(
                     choices=[(0, 'Создано'), (1, 'Отправлено'),
                              (2, 'Получен ответ'),
                              (3, 'Получен некорректный ответ'),
                              (4, 'Отменен'), (5, 'Ошибка')],
                     default=0,
                     verbose_name='Статус сообщения')),
                ('response',
                 models.TextField(blank=True, null=True,
                                  verbose_name='Ответ')),
                ('event_code',
                 models.PositiveSmallIntegerField(verbose_name='Код события')),
                ('event_comment',
                 models.TextField(blank=True,
                                  verbose_name='Комментарий события')),
                ('request', models.TextField(verbose_name='Запрос')),
                ('request_sent',
                 models.DateTimeField(blank=True,
                                      null=True,
                                      verbose_name='Дата и время запроса')),
                ('response_returned',
                 models.DateTimeField(blank=True,
                                      null=True,
                                      verbose_name='Дата и время ответа')),
                ('declaration',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='declaration.Declaration',
                                   verbose_name='Заявление')),
                ('direct',
                 models.ForeignKey(blank=True,
                                   null=True,
                                   on_delete=django.db.models.deletion.CASCADE,
                                   to='direct.Direct',
                                   verbose_name='Направление')),
                ('user',
                 models.ForeignKey(
                     blank=True,
                     null=True,
                     on_delete=models.SET(
                         kinder.core.common.get_sentinel_user),
                     to=settings.AUTH_USER_MODEL,
                     verbose_name='Пользователь, инициировавший запрос')),
            ],
            options={
                'verbose_name': 'Запрос о возникновении события (СМЭВ3)',
                'verbose_name_plural':
                'Запросы о возникновении событий (СМЭВ3)',
            },
        ),
    ]
