import django.contrib.postgres.fields.jsonb

from django.db import migrations

import kinder.core.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('smev3_v321', '0012_pendingupdateorderrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendingupdateorderrequest',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(
                blank=True,
                default=dict,
                encoder=kinder.core.helpers.AdditionalEncoder,
                null=True,
                verbose_name='Данные для отправки данных об изменении'),
        ),
    ]
