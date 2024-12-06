from django.conf import settings
from django.db import migrations, models
import kinder.core.common


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('smev3_v321', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachmentRequest',
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
                              (4, 'Отменен'), (5, 'Ошибка'),
                              (6, 'Переотправлен')],
                     default=0,
                     verbose_name='Статус сообщения')),
                ('response',
                 models.TextField(blank=True, null=True,
                                  verbose_name='Ответ')),
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
                'abstract': False,
            },
        ),
    ]
